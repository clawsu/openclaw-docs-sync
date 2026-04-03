# OpenClaw 文档查询助手 📚

智能查询 OpenClaw 官方文档，支持从 GitHub 自动拉取、过滤、清洗。

## ✨ 特性

- 🔍 **智能搜索** - 根据关键词快速定位文档
- 🌍 **自动过滤** - 仅保留英文文档（剔除多语言冗余）
- ✨ **内容清洗** - 规范化格式，移除无用内容
- 📊 **实时统计** - 文档数量、分类、大小统计
- 🎯 **精准索引** - 685+ 文档快速检索

## 📦 安装方式

### 方式 1：自动拉取（推荐）

从 GitHub 自动拉取、过滤、清洗文档：

```bash
cd /Users/su/.openclaw/workspace/skills-import/openclaw-docs

# 一键安装
python3 scripts/setup.py

# 或手动拉取
python3 scripts/fetch-docs.py
```

**安装过程：**
1. 🔗 Sparse checkout（只拉取 docs/ 目录，节省 50% 流量）
2. 🌍 过滤语言（剔除 zh-CN, ja-JP 等，保留纯英文）
3. ✨ 清洗内容（移除 HTML 注释、规范化格式）
4. 📊 生成索引（自动创建可搜索的索引文件）

**安装后文档位置：**
```
~/.openclaw/docs-cache/     # 清洗后的英文文档（约 400 个文件）
```

### 方式 2：使用现有文档

如果你已有 OpenClaw 文档仓库：

```bash
python3 scripts/setup.py
# 选择使用现有文档
```

### 方式 3：离线打包

将清洗后的文档打包进 Skill：

```bash
# 1. 拉取并清洗
python3 scripts/fetch-docs.py

# 2. 复制到 skill 目录
cp -r ~/.openclaw/docs-cache docs/

# 3. 重新生成索引
python3 scripts/build-index.py

# 4. 打包分发
tar -czf openclaw-docs-offline.tar.gz openclaw-docs/
```

## 🚀 使用方法

### 1. 直接提问（AI 自动查询）

```
你：多智能体怎么配置？
AI：读取 concepts/multi-agent.md → 给出配置示例
```

### 2. 命令行搜索

```bash
# 搜索关键词
python3 scripts/search-docs.py "multi-agent"

# 指定返回数量
python3 scripts/search-docs.py "config" 10

# 搜索中文关键词（匹配英文文档）
python3 scripts/search-docs.py "沙盒"
```

### 3. 查看统计

```bash
python3 scripts/fetch-docs.py  # 会显示统计信息
```

## 📊 文档统计

安装后会显示如下统计：

```
📈 文档统计:
   总文件数: 400
   总行数: 45,832
   总大小: 5.42 MB
   分类数: 16

📁 分类详情:
   - concepts: 29 个文件
   - gateway: 34 个文件
   - channels: 29 个文件
   - tools: 40 个文件
   - cli: 47 个文件
   - ...
```

## 📁 项目结构

```
openclaw-docs/
├── SKILL.md              # 技能定义
├── README.md             # 本文件
├── docs-index.json       # 文档索引（自动生成）
├── config.json           # 配置（自动生成）
└── scripts/
    ├── setup.py          # 安装向导
    ├── fetch-docs.py     # 文档拉取器 ⭐核心
    ├── build-index.py    # 索引生成器
    └── search-docs.py    # 搜索工具
```

## 🔍 核心功能详解

### Sparse Checkout

只从 GitHub 拉取 `docs/` 目录，不下载完整仓库：

```bash
git init
git config core.sparseCheckout true
echo "docs/" > .git/info/sparse-checkout
git pull --depth 1 origin main
```

**效果：** 仅下载约 10MB 文档，而非完整 50MB+ 仓库。

### 语言过滤

自动剔除以下目录：
- `zh-CN/` - 中文文档
- `ja-JP/` - 日文文档
- `ko-KR/` - 韩文文档
- `de-DE/` - 德文文档
- `fr-FR/` - 法文文档
- `es-ES/` - 西班牙文文档
- `.i18n/` - 国际化配置

**效果：** 从 687 个文件减少到约 400 个纯英文文件。

### 内容清洗

对每个 Markdown 文件执行：
1. 移除 HTML 注释 `<!-- ... -->`
2. 规范化代码块标记
3. 移除多余空行
4. 修复 frontmatter 格式

**效果：** 更干净的文档内容，更小的文件体积。

## 🛠️ 高级配置

### 自定义文档源

编辑 `scripts/fetch-docs.py`：

```python
GITHUB_REPO = "https://github.com/your-fork/openclaw.git"
```

### 保留其他语言

编辑 `scripts/fetch-docs.py`，从 `EXCLUDE_LANGS` 移除对应语言：

```python
EXCLUDE_LANGS = {'ja-JP', 'ko-KR'}  # 保留 zh-CN
```

### 环境变量

```bash
# 指定文档保存位置
export OPENCLAW_DOCS_CACHE=/path/to/docs

# 使用代理
export HTTPS_PROXY=http://proxy.example.com:8080
```

## 📚 核心文档速查

| 主题 | 文档路径 |
|------|----------|
| 多智能体路由 | `concepts/multi-agent.md` |
| 委托架构 | `concepts/delegate-architecture.md` |
| Agent 循环 | `concepts/agent-loop.md` |
| Gateway 配置 | `gateway/configuration.md` |
| 沙盒机制 | `gateway/sandboxing.md` |
| Skill 开发 | `tools/skills.md` |
| 定时任务 | `automation/cron-jobs.md` |

## 🤝 贡献

欢迎改进：
- 增加更多清洗规则
- 支持更多语言过滤选项
- 优化索引算法
- 添加文档内容摘要生成

## 📄 License

MIT License - 与 OpenClaw 项目保持一致

---

**Made with ❤️ by Paimon for 苏玖**
