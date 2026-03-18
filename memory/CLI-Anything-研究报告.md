# CLI-Anything 深入研究报告

> 研究时间：2026-03-18 | 研究人：李涯

---

## 一、CLI-Anything 核心方法论

### 1.1 什么是 CLI-Anything？

**CLI-Anything** 是一套将任何 GUI 软件转化为 AI Agent 可用 CLI 工具的完整方法论。它的核心目标是：让 AI 代理能够操作那些原本为人类设计的图形界面软件。

### 1.2 核心原则

| 原则 | 说明 |
|------|------|
| **Agent-Native** | 输出结构化 JSON，让 AI 能解析 |
| **REPL + Subcommand** | 同时支持交互式和脚本化使用 |
| **优先用真后端** | 尽量调用真实软件，而非重新实现 |
| **有状态** | 支持 undo/redo、会话持久化 |

### 1.3 标准化架构

```
<software>/
└── agent-harness/
    ├── <SOFTWARE>.md          # 项目分析文档
    ├── setup.py               # 安装配置
    └── cli_anything/<software>/
        ├── __init__.py
        ├── __main__.py
        ├── <software>_cli.py   # Click CLI 入口
        ├── core/               # 核心业务逻辑
        │   ├── project.py      # 项目管理
        │   ├── session.py     # 会话状态
        │   └── ...
        ├── utils/              # 工具层
        │   ├── <software>_backend.py  # 真实软件封装
        │   └── repl_skin.py    # REPL UI
        └── tests/              # 测试
```

---

## 二、七大案例深度分析

### 2.1 GIMP（图像处理）

**后端策略**：Pillow + GIMP batch mode

| 维度 | 实现 |
|------|------|
| **核心引擎** | Pillow 处理图像 I/O、像素操作、基础滤镜 |
| **高级功能** | 调用 `gimp -i -b` 执行 XCF 和 Script-Fu |
| **项目格式** | 自定义 JSON manifest（而非直接操作 XCF）|
| **关键模块** | canvas, layers, filters, export, media |

**核心命令**：
```bash
gimp-cli canvas create --width 1920 --height 1080
gimp-cli layer add --name "Background" --source image.png
gimp-cli filters apply --name gaussian_blur --radius 3
gimp-cli export --format png output.png
```

**关键洞察**：不直接解析二进制 XCF 格式，而是用 Pillow 重建 + GIMP 后端做桥接

---

### 2.2 Blender（3D 渲染）

**后端策略**：Blender Python API (bpy) + 命令行渲染

| 维度 | 实现 |
|------|------|
| **核心引擎** | bpy 模块直接操作 Blender 场景图 |
| **渲染方式** | `blender -b scene.blend -o //render -f 1` |
| **项目格式** | .blend 文件 + CLI 状态 JSON |
| **关键模块** | scene, objects, materials, lighting, animation, modifiers, render |

**核心命令**：
```bash
blender-cli scene new --name my_scene
blender-cli object add --type cube --name Cube
blender-cli material create --name Metal --metallic 1.0 --roughness 0.2
blender-cli render export --format png --frame 1
```

**关键洞察**：直接利用 Blender 的 Python API，比调用 CLI 更强大

---

### 2.3 Draw.io（流程图/图表）

**后端策略**：直接操作 mxGraph XML + draw.io CLI 导出

| 维度 | 实现 |
|------|------|
| **核心引擎** | 纯 XML 操作，无需外部依赖 |
| **导出方式** | `draw.io --export input.drawio --output out.png` |
| **项目格式** | .drawio (mxGraph XML) |
| **关键模块** | shapes, connectors, pages, export |

**核心命令**：
```bash
drawio-cli shape add --type rectangle --label "Server" --x 100 --y 100
drawio-cli connector add --from server --to database --label "query"
drawio-cli page add --name "Page-2"
drawio-cli export --format pdf output.pdf
```

**关键洞察**：XML 格式完全可解析，直接操作比调用 GUI 更快

---

### 2.4 AnyGen（AI 内容生成）

**后端策略**：HTTP REST API 客户端

| 维度 | 实现 |
|------|------|
| **核心引擎** | requests 库调用 AnyGen OpenAPI |
| **异步模式** | 轮询 `GET /tasks/:id` 直到完成 |
| **项目格式** | JSON 任务描述 |
| **关键模块** | task, export |

**核心命令**：
```bash
anygen-cli task create --type pptx --prompt "介绍建业电影小镇"
anygen-cli task status --id <task_id>
anygen-cli file download --id <task_id> --output ./output.pptx
```

**关键洞察**：无本地软件，纯 API 封装，适合云服务类工具

---

### 2.5 LibreOffice（办公套件）

**后端策略**：纯 Python 生成 ODF 文件（ZIP+XML）

| 维度 | 实现 |
|------|------|
| **核心引擎** | Python stdlib (zipfile, xml.etree) |
| **后端调用** | `libreoffice --headless --convert-to` |
| **项目格式** | ODF (Writer/Calc/Impress) |
| **关键模块** | writer, calc, impress, styles, export |

**核心命令**：
```bash
lo-cli document new --type writer --name Report
lo-cli writer add-paragraph --text "Hello" --bold
lo-cli writer add-table --rows 3 --cols 3
lo-cli export --format pdf report.pdf
```

**关键洞察**：不依赖 LibreOffice 也能生成有效 ODF 文件，可离线使用

---

### 2.6 Shotcut（视频编辑）

**后端策略**：MLT/FFmpeg + 项目文件 XML

| 维度 | 实现 |
|------|------|
| **核心引擎** | 直接操作 .mlt (XML) 项目文件 |
| **渲染方式** | `melt` (MLT 命令行) |
| **项目格式** | .mlt + 资源文件 |
| **关键模块** | timeline, tracks, clips, filters, export |

---

### 2.7 Inkscape/其他案例

类似 GIMP，Inkscape 使用 SVG 作为中间格式，更易于操作。

---

## 三、案例对比总结

| 案例 | 后端策略 | 项目格式 | 复杂度 | 适用场景 |
|------|----------|----------|--------|----------|
| GIMP | Pillow + GIMP batch | JSON manifest | 中 | 图像处理 |
| Blender | bpy API + CLI | .blend | 高 | 3D 渲染 |
| Draw.io | 纯 XML 操作 | .drawio | 低 | 流程图 |
| AnyGen | HTTP API | JSON | 低 | AI 生成 |
| LibreOffice | 纯 Python 生成 ODF | ODF | 中 | 文档处理 |
| Shotcut | MLT XML 操作 | .mlt | 中 | 视频编辑 |

---

## 四、建业电影小镇 CLI 工具构想

### 4.1 运营场景分析

根据研究，建业电影小镇的核心运营需求：

| 场景 | 当前痛点 | CLI 解决思路 |
|------|----------|--------------|
| **数据报表** | Excel 手动处理 | 自动化报表生成 |
| **GEO 内容** | 重复性写作 | 批量内容生成 |
| **票务管理** | 多平台切换 | 统一 CLI 操作 |
| **营销素材** | 格式转换繁琐 | 自动化转换pipeline |

### 4.2 建议构建的 CLI 工具

#### 工具1：`movie-town-cli`（文旅运营 CLI）

```bash
# 报表管理
movie-town report generate --type daily --date 2026-03-18
movie-town report merge --files "data/*.xlsx" --output monthly.xlsx

# 内容运营
movie-town content generate --platform douyin --topic "清明活动"
movie-town content seo-optimize --input article.md

# 票务
movie-town ticket query --date 2026-04-04
movie-town ticket sync --source platform --target local

# 素材转换
movie-town media convert --input poster.png --format pdf
movie-town media batch-resize --input ./photos --size 800x600
```

#### 工具2：`xiaoyuan-cli`（研学业务 CLI）

```bash
# 课程管理
xiaoyuan course list
xiaoyuan course create --name "电影探秘" --duration 3h

# 报名管理
xiaoyuan enroll import --file students.csv
xiaoyuan enroll export --format xlsx

# 物料生成
xiaoyuan material generate --template certificate --student "张三"
```

---

## 五、OpenClaw 集成方案

### 5.1 当前状态

OpenClaw 已有 `cli-anything` skill，但只是方法论封装。需要增强为：

1. **调用 CLI-Anything 方法论** 自动生成新 CLI
2. **集成已有 CLI 工具** 到 OpenClaw 工具集
3. **构建建业电影小镇专用 CLI**

### 5.2 集成路径

```
OpenClaw Skill
     ↓
cli-anything (方法论)
     ↓
┌─────────────────────────────────┐
│  OpenClaw Agent                 │
│  ├── 读取目标软件源码/GUI分析   │
│  ├── 调用 HARNESS.md SOP        │
│  ├── 生成 CLI 包装器            │
│  └── 测试验证                   │
└─────────────────────────────────┘
     ↓
┌─────────────────────────────────┐
│  生成的 CLI 工具                │
│  ├── cli-anything-movie-town    │
│  └── cli-anything-xiaoyuan      │
└─────────────────────────────────┘
```

### 5.3 技术实现

**方案 A**：在 OpenClaw 中嵌入 CLI-Anything 命令
- 用户说"帮我为 XX 软件生成 CLI"
- OpenClaw 调用 CLI-Anything 方法论
- 输出完整的 CLI 包装器

**方案 B**：预构建建业电影小镇专用 CLI
- 预先为小镇常见运营场景构建 CLI
- 作为 skill 的一部分交付
- 开箱即用

---

## 六、下一步建议

### 6.1 立即可执行

1. ✅ **创建 movie-town-cli 原型**
   - 基于 LibreOffice 模式：Python 生成 Excel/Word
   - 优先实现：日报汇总、票务报表生成

2. ✅ **集成现有 CLI 工具**
   - 检查系统已有 CLI（ffmpeg, libreoffice 等）
   - 封装为 OpenClaw 可调用工具

### 6.2 中期规划

1. 📋 **构建完整文旅运营 CLI 工具链**
2. 📋 **实现 GEO 内容批量生成 CLI**
3. 📋 **测试 CLI-Anything 自动生成能力**

### 6.3 长期愿景

- 🎯 **让 OpenClaw 成为文旅行业的 AI 运营大脑**
- 🎯 **所有运营操作可通过自然语言 → CLI → 自动执行**

---

## 七、参考资料

- CLI-Anything 官方仓库：`~/.openclaw/workspace/CLI-Anything/`
- HARNESS.md 方法论：`~/.openclaw/workspace/CLI-Anything/cli-anything-plugin/HARNESS.md`
- 案例源码：gimp, blender, drawio, anygen, libreoffice, shotcut, inkscape

---

*本报告由李涯于 2026-03-18 生成*
