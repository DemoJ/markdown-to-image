# Markdown to Image

将 Markdown 文档渲染为简约美观的分享图片（PNG）。

## 功能特性

- 🎨 **精美样式** - 现代卡片设计，渐变装饰条，舒适阅读体验
- 🌓 **双主题支持** - Light / Dark 两种主题随心切换
- 📱 **高清输出** - 支持 2x/3x 缩放因子，适配 Retina 屏幕
- 🖼️ **图片嵌入** - 本地图片自动转 base64，无需额外处理
- 📐 **自定义宽度** - 支持 500px ~ 1200px+ 自定义宽度
- 📝 **完整 Markdown 支持** - 标题、列表、表格、代码块、引用等

## 依赖安装

```bash
pip install markdown playwright

# 首次使用需安装 Playwright 浏览器
playwright install chromium
```

## 快速开始

### 基本用法

```bash
# 最简方式：输入 markdown 文件，输出同名 .png
python render.py input.md

# 指定输出路径
python render.py input.md output.png

# 自定义宽度和主题
python render.py input.md output.png --width 900 --theme dark

# 高清输出（3x 缩放）
python render.py input.md output.png --width 1200 --scale 3
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input` | 输入的 markdown 文件路径（必填） | — |
| `output` | 输出图片路径（可选） | `<input_stem>.png` |
| `--preset` | 预设配置：`mobile` / `desktop` | `mobile` |
| `--width` | 自定义宽度（会覆盖预设宽度） | 预设值 |
| `--scale` | 设备缩放因子（越大越清晰） | `2` |
| `--theme` | 主题：`light` / `dark` | `light` |

## 支持的 Markdown 特性

| 特性 | 支持 | 说明 |
|------|:---:|------|
| 标题 (h1-h6) | ✅ | 自动层级样式 |
| 段落与换行 | ✅ | 1.75 行高，舒适阅读 |
| 粗体 / 斜体 | ✅ | — |
| 链接 | ✅ | 蓝色主题色带下划线 |
| 图片 | ✅ | 自动转 base64 嵌入 |
| 有序 / 无序列表 | ✅ | 支持嵌套 |
| 引用块 | ✅ | 蓝色左侧边框样式 |
| 代码块 | ✅ | 围栏代码块 + 语法高亮 |
| 行内代码 | ✅ | 粉红色高亮背景 |
| 表格 | ✅ | 斑马条纹样式 |
| 分割线 | ✅ | — |
| 任务列表 | ✅ | checkbox 支持 |

## 主题预览

### Light 主题（默认）

- 白色卡片 + 浅灰背景
- 蓝色主色调（#3b82f6）
- 顶部渐变装饰条：蓝 → 紫 → 粉
- 适合：正式文档、技术笔记、知识分享

### Dark 主题

- 深蓝卡片 + 暗色背景
- 亮蓝主色调（#60a5fa）
- 同样渐变装饰条
- 适合：夜间阅读、暗色风格偏好

## 使用示例

### 示例 1：基本转换

```bash
# 将 README.md 转换为图片
python render.py README.md
# 输出：README.png
```

### 示例 2：指定暗色主题

```bash
python render.py notes.md notes-dark.png --theme dark
```

### 示例 3：生成高清分享图

```bash
# 1200px 宽度，3x 缩放，适合社交媒体
python render.py article.md share.png --width 1200 --scale 3
```

### 示例 Markdown 文件

```markdown
# 我的学习笔记

## 今日收获

- 学会了 Python 装饰器
- 了解了设计模式
- 完成了项目部署

> 每天进步一点点 🚀

### 代码示例

\`\`\`python
def decorator(func):
    def wrapper(*args, **kwargs):
        print("Before call")
        result = func(*args, **kwargs)
        print("After call")
        return result
    return wrapper
\`\`\`

| 任务 | 状态 |
|------|:----:|
| 学习 Python | ✅ |
| 完成项目 | 🔄 |
| 写博客 | ⏳ |
```

## 项目结构

```
markdown-to-image/
├── README.md        # 本文档
├── SKILL.md         # Claude Code Skill 定义
├── render.py        # 核心渲染脚本
└── template.html    # HTML 模板（含样式）
```

## 技术实现

- **Markdown 解析**: 使用 `markdown` 库，支持 tables、fenced_code、codehilite 等扩展
- **HTML 渲染**: 使用 `Playwright` 无头浏览器截取高质量图片
- **样式设计**: 纯 CSS 变量实现主题切换，无需外部依赖

## 字体支持

自动使用系统中文字体：

- macOS: PingFang SC, Hiragino Sans GB
- Windows: Microsoft YaHei
- Linux: Noto Sans SC

代码块使用等宽字体：JetBrains Mono, Fira Code, SF Mono, Cascadia Code 等。

## 注意事项

- **分辨率**: 默认 `scale=2`（2x），输出图片清晰度适合 Retina 屏幕和社交媒体分享
- **图片嵌入**: markdown 中的本地图片会自动转为 base64 嵌入，无需手动处理
- **宽度建议**: 手机屏幕分享推荐使用 `mobile` 预设 (500px)；桌面展示推荐使用 `desktop` 预设 (1200px)
- **字体渲染**: 依赖系统中文字体，确保已安装相关字体

## License

MIT