#!/usr/bin/env python3
"""Markdown to Image renderer using Playwright.

Parses a markdown file, injects it into a styled HTML template,
and captures a high-quality PNG screenshot via Playwright.

Usage:
    python3 render.py <input.md> [output.png] [--preset mobile|desktop] [--theme light|dark]

Presets:
    mobile:  width=500px, font-size=18px (default, optimized for phone screens)
    desktop: width=1200px, font-size=14px (optimized for desktop/tablet, formal document style)

If output is not specified, defaults to <input_stem>.png in the same directory.
"""

import argparse
import base64
import mimetypes
import re
import sys
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

# ---------------------------------------------------------------------------
# Preset configurations
# ---------------------------------------------------------------------------
PRESETS = {
    "mobile": {
        "width": 500,
        "font_size": 18,
        "padding": "28px 32px",
    },
    "desktop": {
        "width": 1200,
        "font_size": 14,
        "padding": "32px 40px",
    },
}

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = SCRIPT_DIR / "template.html"
WORKSPACE_TMP = Path("/opt/data/workspace/tmp/md2img")


def read_markdown(path: Path) -> str:
    """Read a markdown file and return its content."""
    return path.read_text(encoding="utf-8")


def md_to_html(md_text: str) -> str:
    """Convert markdown text to HTML with extended extensions."""
    extensions = [
        "tables",
        "fenced_code",
        "codehilite",
        "toc",
        "nl2br",
        "sane_lists",
        "smarty",
        "attr_list",
        "md_in_html",
    ]
    extension_configs = {
        "codehilite": {
            "css_class": "codehilite",
            "guess_lang": True,
            "linenums": False,
        },
        "toc": {
            "permalink": False,
        },
    }
    return markdown.markdown(
        md_text,
        extensions=extensions,
        extension_configs=extension_configs,
        output_format="html5",
    )


def resolve_local_images(html: str, base_dir: Path) -> str:
    """Convert local image paths in <img> tags to base64 data URIs.

    This ensures images render correctly in the headless browser even
    when served from a temporary file:// URL.
    """
    def _replace(match):
        src = match.group(1)
        # Skip external URLs and already-encoded data URIs
        if src.startswith(("http://", "https://", "data:")):
            return match.group(0)
        # Resolve relative to the markdown file's directory
        img_path = (base_dir / src).resolve()
        if not img_path.exists():
            return match.group(0)
        mime, _ = mimetypes.guess_type(str(img_path))
        if not mime:
            mime = "image/png"
        with open(img_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return f'src="data:{mime};base64,{encoded}"'

    return re.sub(r'src="([^"]+)"', _replace, html)


def build_html(body_html: str, template_path: Path, theme: str = "light", font_size: int = 18, padding: str = "28px 32px") -> str:
    """Inject rendered HTML body into the template with dynamic font size and padding."""
    template = template_path.read_text(encoding="utf-8")
    
    # Inject theme class
    template = template.replace(
        '<body class="light">',
        f'<body class="{theme}">',
    )
    
    # Inject dynamic font size and padding for mobile/desktop presets
    # Replace font-size in body style
    template = re.sub(
        r'font-size: \d+px;',
        f'font-size: {font_size}px;',
        template,
        count=1  # Only replace the first occurrence (body font-size)
    )
    
    # Replace padding in .card style
    template = re.sub(
        r'padding: [\d]+px [\d]+px;',
        f'padding: {padding};',
        template,
        count=1  # Only replace the first occurrence (.card padding)
    )
    
    return template.replace("{{CONTENT}}", body_html)


def render_image(
    html_content: str,
    output_path: Path,
    width: int = 500,
    device_scale: int = 2,
) -> Path:
    """Render HTML to a PNG image using Playwright."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": width, "height": 800},
            device_scale_factor=device_scale,
        )
        page.set_content(html_content, wait_until="networkidle")
        # Wait a bit for fonts and layout to settle
        page.wait_for_timeout(300)

        # Get the actual content height
        body_height = page.evaluate("document.body.scrollHeight")

        # Resize viewport to fit content
        page.set_viewport_size({"width": width, "height": body_height})
        page.wait_for_timeout(200)

        # Screenshot the full page
        page.screenshot(path=str(output_path), full_page=True, type="png")
        browser.close()

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Render markdown to image")
    parser.add_argument("input", help="Input markdown file path")
    parser.add_argument("output", nargs="?", help="Output image path (default: <input>.png)")
    parser.add_argument("--preset", choices=["mobile", "desktop"], default="mobile",
                        help="Preset configuration: mobile (500px, 18px font) or desktop (1200px, 14px font). Default: mobile")
    parser.add_argument("--width", type=int, help="Override image width in px (overrides preset)")
    parser.add_argument("--font-size", type=int, help="Override font size in px (overrides preset)")
    parser.add_argument("--padding", type=str, help="Override padding, e.g. '24px 32px' (overrides preset)")
    parser.add_argument("--scale", type=int, default=2, help="Device scale factor (default: 2)")
    parser.add_argument("--theme", choices=["light", "dark", "auto"], default="light",
                        help="Color theme (default: light)")
    args = parser.parse_args()

    # Get preset configuration
    preset = PRESETS[args.preset]
    width = args.width if args.width else preset["width"]
    font_size = args.font_size if args.font_size else preset["font_size"]
    padding = args.padding if args.padding else preset["padding"]

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = Path(args.output).resolve()
    else:
        output_path = input_path.parent / f"{input_path.stem}.png"

    # Read and convert
    md_text = read_markdown(input_path)
    body_html = md_to_html(md_text)
    body_html = resolve_local_images(body_html, input_path.parent)
    full_html = build_html(body_html, TEMPLATE_PATH, theme=args.theme, font_size=font_size, padding=padding)

    # Render
    result = render_image(full_html, output_path, width=width, device_scale=args.scale)
    print(f"SAVE_PATH: {result}")


if __name__ == "__main__":
    main()
