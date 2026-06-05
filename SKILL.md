---
name: markdown-to-image
description: "将 Markdown 文档渲染为简约美观的分享图片（PNG）。当用户需要把markdown转成图片、生成分享图、长图、知识卡片、笔记截图时使用。"
---

# Markdown → 分享图片

> **前置条件：** 确保已安装 Python 依赖：`pip install markdown`（Playwright 已预装）

## 触发条件

用户要求将 markdown 转为图片、生成分享图、知识卡片、长图截图，或提到"markdown转图片"、"生成图片"、"分享图"等关键词时使用。

## 快速使用

### 基本用法

```bash
# 最简方式：输入 markdown 文件，输出同名 .png
python3 user/skills/markdown-to-image/render.py /path/to/input.md

# 指定输出路径
python3 user/skills/markdown-to-image/render.py /path/to/input.md /path/to/output.png

# 自定义宽度（默认 800px）和主题
python3 user/skills/markdown-to-image/render.py input.md output.png --width 900 --theme dark
```

### 完整参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input` | 输入的 markdown 文件路径（必填） | — |
| `output` | 输出图片路径（可选） | `<input>.png` |
| `--width` | 图片宽度（像素） | `800` |
| `--scale` | 设备缩放因子（越大越清晰） | `2` |
| `--theme` | 主题：`light` / `dark` | `light` |

## 核心流程

当用户给出 markdown 内容（直接文本或文件路径）时，按以下步骤操作：

### Step 1: 准备 markdown 文件

**如果用户直接给了 markdown 文本：**
```bash
# 将文本保存为临时文件
cat > /opt/data/workspace/tmp/md2img/input.md << 'MARKDOWN_EOF'
（用户的 markdown 内容）
MARKDOWN_EOF
```

**如果用户给了文件路径：** 直接使用该路径。

### Step 2: 确定输出路径

```bash
# 建议输出到临时目录
mkdir -p /opt/data/workspace/tmp/md2img
# 输出路径示例：/opt/data/workspace/tmp/md2img/output.png
```

### Step 3: 执行渲染

```bash
python3 user/skills/markdown-to-image/render.py \
  /opt/data/workspace/tmp/md2img/input.md \
  /opt/data/workspace/tmp/md2img/output.png \
  --width 800 --theme light
```

脚本成功后会输出：`SAVE_PATH: /opt/data/workspace/tmp/md2img/output.png`

### Step 4: 发送图片给用户

**必须按顺序：先发图，后删文件。**

1. 使用 `publish_artifact` 工具将生成的图片发送给用户
2. 发送完毕后删除临时文件，避免磁盘空间被占满

## 支持的 Markdown 特性

| 特性 | 支持 | 说明 |
|------|:---:|------|
| 标题 (h1-h6) | ✅ | 自动编号样式 |
| 段落与换行 | ✅ | 1.75 行高，舒适阅读 |
| 粗体 / 斜体 | ✅ | — |
| 链接 | ✅ | 蓝色带下划线 |
| 图片 | ✅ | 自动转 base64 嵌入 |
| 有序 / 无序列表 | ✅ | 支持嵌套 |
| 引用块 | ✅ | 蓝色左侧边框 |
| 代码块 | ✅ | 围栏代码块 + 语法高亮 |
| 行内代码 | ✅ | 粉红色高亮 |
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

## 注意事项

- **分辨率**：默认 `scale=2`（2x），输出图片清晰度适合 Retina 屏幕和社交媒体分享
- **图片嵌入**：markdown 中的本地图片会自动转为 base64 嵌入，无需手动处理
- **宽度建议**：社交媒体分享推荐 800px；文档长图推荐 900-1000px
- **临时文件**：渲染完成后务必清理 `/opt/data/workspace/tmp/md2img/` 下的临时文件
- **字体渲染**：自动使用系统中文字体（Noto Sans SC / PingFang SC / Microsoft YaHei）

## 示例

### 示例 1：用户直接给文本

用户说："帮我把这段 markdown 转成图片"

```bash
# 1. 保存 markdown
mkdir -p /opt/data/workspace/tmp/md2img
cat > /opt/data/workspace/tmp/md2img/input.md << 'EOF'
# 我的笔记

## 今日收获

- 学会了 Python 装饰器
- 了解了设计模式
- 完成了项目部署

> 每天进步一点点 🚀
EOF

# 2. 渲染
python3 user/skills/markdown-to-image/render.py \
  /opt/data/workspace/tmp/md2img/input.md \
  /opt/data/workspace/tmp/md2img/note.png

# 3. 发送图片（使用 publish_artifact）
# 4. 清理临时文件
```

### 示例 2：用户给了文件路径

用户说："把 notes/weekly.md 转成暗色主题的图片"

```bash
python3 user/skills/markdown-to-image/render.py \
  notes/weekly.md \
  /opt/data/workspace/tmp/md2img/weekly.png \
  --theme dark --width 900
```

### 示例 3：自定义宽度

用户说："生成 1200px 宽的高清图"

```bash
python3 user/skills/markdown-to-image/render.py \
  input.md output.png --width 1200 --scale 3
```
