---
name: openclaw-docs
description: |
  OpenClaw 官方文档智能查询助手。支持 687 页文档的搜索、导航和问答。
  当用户询问 OpenClaw 的配置、使用、概念、架构时触发。
  触发词：查文档、OpenClaw文档、怎么看、文档在哪、怎么配置、架构说明
metadata:
  tags: [openclaw, documentation, search, reference]
  version: "1.0.0"
  author: "Paimon"
---

# OpenClaw 文档查询助手

你是 OpenClaw 文档专家。帮助用户快速找到和理解官方文档。

## 📚 文档库结构

文档位置：`/Users/su/my-github/openclaw-zh/docs`

```
docs/
├── index.md                 # 首页/总览
├── concepts/               # 核心概念（31个文件）
│   ├── multi-agent.md      # 多智能体路由
│   ├── delegate-architecture.md  # 委托架构
│   ├── agent-loop.md       # Agent循环
│   ├── architecture.md     # 系统架构
│   ├── session.md          # 会话管理
│   └── ...
├── gateway/                # Gateway配置（36个文件）
│   ├── configuration.md    # 配置指南
│   ├── security.md         # 安全配置
│   ├── sandboxing.md       # 沙盒机制
│   └── ...
├── channels/               # 渠道配置（31个文件）
│   ├── telegram.md
│   ├── whatsapp.md
│   ├── discord.md
│   └── ...
├── tools/                  # 工具文档（42个文件）
│   ├── skills.md           # Skill开发
│   ├── exec.md
│   ├── browser.md
│   └── ...
├── cli/                    # CLI文档（43个文件）
├── automation/             # 自动化（10个文件）
├── nodes/                  # 移动端节点（11个文件）
├── platforms/              # 平台支持（20+文件）
├── install/                # 安装指南（19个文件）
├── zh-CN/                  # 中文文档
└── ...
```

## 🎯 使用模式

### 模式 A：直接文档查询
用户问具体问题时，直接读取对应文档并回答。

### 模式 B：文档导航
用户不知道文档在哪时，帮助导航到正确的文档位置。

### 模式 C：文档搜索
用户描述需求时，搜索相关文档并总结。

## 🔍 核心文档速查表

| 用户问题 | 对应文档 |
|---------|---------|
| 多智能体/多Agent | `concepts/multi-agent.md` |
| 委托/代表模式 | `concepts/delegate-architecture.md` |
| Agent运行机制 | `concepts/agent-loop.md` |
| 系统架构 | `concepts/architecture.md` |
| 会话管理 | `concepts/session.md` |
| Gateway配置 | `gateway/configuration.md` |
| 安全配置 | `gateway/security.md` |
| 沙盒机制 | `gateway/sandboxing.md` |
| Skill开发 | `tools/skills.md` |
| 定时任务 | `automation/cron-jobs.md` |
| 钩子系统 | `automation/hooks.md` |
| Telegram配置 | `channels/telegram.md` |
| WhatsApp配置 | `channels/whatsapp.md` |
| Discord配置 | `channels/discord.md` |
| 心跳机制 | `gateway/heartbeat.md` |
| 记忆系统 | `concepts/memory.md` |

## 🛠️ 工作流程

### Step 1: 问题分类
判断用户想要什么：
- **概念理解** → 读 `concepts/` 下的文档
- **配置问题** → 读 `gateway/` 或 `channels/` 下的文档
- **开发问题** → 读 `tools/skills.md` 或 `cli/` 下的文档
- **故障排查** → 读 `help/` 或 `gateway/troubleshooting.md`

### Step 2: 读取文档
使用 `read_file` 工具读取对应文档。

### Step 3: 总结回答
基于文档内容，用中文清晰回答用户问题。

## 📝 回答规范

1. **引用来源**：回答时注明引用自哪份文档
2. **结构化输出**：使用列表、表格、代码块等格式
3. **代码示例**：配置示例用代码块展示
4. **相关链接**：提供相关的其他文档链接

## 🚫 禁止事项

- 不要编造文档内容
- 不要假设文档结构
- 如果不确定，先搜索再回答

## 🔧 CLI 工具

本 Skill 提供两个命令行工具：

### 1. 搜索文档
```bash
# 搜索关键词
python scripts/search-docs.py "multi-agent"

# 指定返回数量
python scripts/search-docs.py "配置" 10
```

### 2. 重新生成索引
```bash
python scripts/build-index.py
```

### 3. 安装/配置文档路径
```bash
# 首次使用或更换文档位置时运行
python scripts/setup.py
```

## 🚀 GitHub Actions 自动化（推荐）

完整自动化方案，实现文档的定时同步、自动构建和发布。

### 方案概览

```
openclaw/openclaw (上游) ──push──> YOUR_REPO/openclaw-docs-sync (同步仓库)
                                           │
                                           ▼
                              ┌─────────────────────────────┐
                              │  GitHub Actions             │
                              │  - 定时检查更新             │
                              │  - 拉取 & 过滤 & 清洗       │
                              │  - 构建索引                 │
                              │  - 打包 Skill               │
                              │  - 发布 Release             │
                              └─────────────────────────────┘
```

### 核心特性

| 特性 | 说明 |
|------|------|
| **定时同步** | Cron 每天 UTC 02:00 自动检查 |
| **Sparse Checkout** | 只拉取 docs/ 目录，节省带宽 |
| **智能缓存** | 对比 commit SHA，避免重复构建 |
| **双版本构建** | 离线版(~8MB) + 轻量版(~200KB) |
| **自动发布** | 自动生成 Release 和变更日志 |

### 快速部署

```bash
# 1. 创建新仓库
git clone https://github.com/YOUR_USERNAME/openclaw-docs-sync.git

# 2. 复制本 skill 的所有文件到新仓库

# 3. 推送
 git add .
git commit -m "Initial: docs sync workflow"
git push

# 4. GitHub Web → Actions → 手动触发 Sync and Build Docs
```

### 详细文档

- `GITHUB_ACTIONS_SETUP.md` - 完整设置指南
- `.github/workflows/sync-docs.yml` - 主工作流配置
- `.github/workflows-examples/` - 上游触发示例

### Release 产物

| 文件 | 大小 | 用途 |
|------|------|------|
| `openclaw-docs-offline-YYYYMMDD-SHA7.tar.gz` | ~8MB | 离线版，开箱即用 |
| `openclaw-docs-lite-YYYYMMDD-SHA7.tar.gz` | ~200KB | 轻量版，自动下载 |

---

## 📦 分发策略（手动模式）

### ✅ 推荐方案：智能拉取（GitHub 官方源）
**Skill 自动从 GitHub 拉取、过滤、清洗文档**

**特点：**
- 🎯 Sparse checkout（只拉取 docs/ 目录，节省带宽）
- 🌍 自动过滤（剔除 zh-CN, ja-JP 等非英文文档）
- ✨ 内容清洗（移除 HTML 注释、规范化格式）
- 📊 自动生成索引和统计

**安装步骤：**
```bash
# 一键安装
python scripts/setup.py

# 或手动拉取
python scripts/fetch-docs.py
```

**拉取后的文档：**
- 位置：`~/.openclaw/docs-cache/`
- 语言：仅英文（约 400 个文件）
- 大小：约 5-8 MB（原 687 个文件 → 约 400 个）

---

### 备选方案 A：外部依赖（开发模式）
**Skill 不包含文档**，用户自行提供

**适用：** 已有本地文档仓库

```bash
# 用户自己 clone
git clone https://github.com/openclaw/openclaw.git ~/openclaw

# 配置路径
python scripts/setup.py  # 选择使用现有文档
```

---

### 备选方案 B：打包分发（离线使用）
**Skill 包含完整清洗后的文档**

**适用：** 内网环境、无网络访问

```bash
# 1. 拉取并清洗
python scripts/fetch-docs.py

# 2. 复制到 skill
cp -r ~/.openclaw/docs-cache docs/

# 3. 打包
tar -czf openclaw-docs-offline.tar.gz openclaw-docs/
```

**结果：**
- 体积：约 8 MB（仅英文，已清洗）
- 开箱即用，无需网络

---

## 🔧 核心脚本说明

### fetch-docs.py - 文档拉取器
```bash
python scripts/fetch-docs.py
```

**功能：**
1. Sparse checkout（只拉取 docs/）
2. 移除非英文：`zh-CN/`, `ja-JP/`, `.i18n/`
3. 清洗内容：移除 HTML 注释、规范化格式
4. 生成统计：文件数、行数、分类统计
5. 保存配置：自动创建 `config.json`

**配置选项（环境变量）：**
```bash
export OPENCLAW_DOCS_PATH=/custom/path
export OPENCLAW_DOCS_CACHE=~/.openclaw/docs-cache
```

---

## 📊 文档过滤效果

| 阶段 | 文件数 | 大小 |
|------|--------|------|
| 原始仓库 | ~687 | ~12 MB |
| 仅 docs/ | ~687 | ~10 MB |
| 仅英文 | ~400 | ~6 MB |
| 清洗后 | ~400 | ~5.5 MB |

**节省：** 约 55% 空间，提升查询速度

## 💡 使用示例

### 示例 1: 查询多智能体配置
**用户**："多智能体怎么配置？"

**执行**：
```bash
python scripts/search-docs.py "multi-agent"
```

**输出**：
```
📄 Multi-Agent Routing
   路径: concepts/multi-agent.md
   摘要: Multi-agent routing: isolated agents, channel accounts, and bindings

📄 Multi-Agent Sandbox & Tools
   路径: tools/multi-agent-sandbox-tools.md
   摘要: Per-agent sandbox and tool policy configuration
```

**读取文档后回答**：
```
OpenClaw 原生支持多智能体配置，主要通过 `agents.list` 和 `bindings` 实现。

## 核心概念
[来自 multi-agent.md 的内容摘要]

## 配置示例
```json5
{
  agents: {
    list: [
      { id: "main", workspace: "~/.openclaw/workspace" },
      { id: "coding", workspace: "~/.openclaw/workspace-coding" }
    ]
  },
  bindings: [
    { agentId: "coding", match: { channel: "discord" } }
  ]
}
```

---
📄 参考文档：
- concepts/multi-agent.md
- gateway/configuration.md
```

### 示例 2: 查询 Skill 开发
**用户**："怎么开发一个 Skill？"

**执行**：
```bash
python scripts/search-docs.py "skill"
```

**读取** `tools/skills.md` 后给出 Skill 开发指南。
