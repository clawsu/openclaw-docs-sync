# GitHub Actions 自动化文档同步方案

## 🎯 方案概述

通过 GitHub Actions 实现：
1. **定时/手动** 从 openclaw 主仓库同步文档
2. **自动过滤** 多语言文档，仅保留英文
3. **自动清洗** 文档内容
4. **自动构建** Skill 包（离线版 + 轻量版）
5. **自动发布** 到 GitHub Release

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────────────────┐
│                    openclaw/openclaw (上游)                      │
│                          ┌──────────┐                           │
│                          │  docs/   │                           │
│                          └────┬─────┘                           │
└───────────────────────────────┼─────────────────────────────────┘
                                │ push (可选 webhook)
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│              YOUR_USERNAME/openclaw-docs-sync (你的仓库)          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  GitHub Actions Workflow                                │   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐          │   │
│  │  │ Check     │→ │ Build     │→ │ Release   │          │   │
│  │  │ Updates   │  │ & Package │  │ & Notify  │          │   │
│  │  └───────────┘  └───────────┘  └───────────┘          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                     │
│                          ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Artifacts                                              │   │
│  │  ├── openclaw-docs-offline-YYYYMMDD-SHA7.tar.gz (~8MB) │   │
│  │  └── openclaw-docs-lite-YYYYMMDD-SHA7.tar.gz (~200KB)  │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### Step 1: 创建同步仓库

在 GitHub 创建新仓库：`openclaw-docs-sync`

```bash
# 克隆到本地
git clone https://github.com/YOUR_USERNAME/openclaw-docs-sync.git
cd openclaw-docs-sync
```

### Step 2: 复制文件

将以下文件复制到新仓库：

```
openclaw-docs-sync/
├── .github/
│   └── workflows/
│       └── sync-docs.yml          # 主工作流
├── scripts/
│   ├── fetch-docs.py              # 文档拉取
│   ├── clean-docs.py              # 内容清洗
│   ├── build-index.py             # 索引生成
│   └── search-docs.py             # 搜索工具
├── SKILL.md                       # 技能定义
├── README.md                      # 用户文档
├── DISTRIBUTION.md                # 分发指南
└── requirements.txt               # Python 依赖
```

### Step 3: 提交并推送

```bash
git add .
git commit -m "Initial commit: docs sync workflow"
git push origin main
```

### Step 4: 手动触发首次运行

1. 打开 GitHub 仓库页面
2. 点击 **Actions** 标签
3. 选择 **Sync and Build Docs** 工作流
4. 点击 **Run workflow** → 选择 **main** 分支 → 点击 **Run workflow**

---

## ⚙️ 工作流配置详解

### 触发方式

| 触发器 | 说明 |
|--------|------|
| `schedule` | 每天 UTC 02:00 自动运行 |
| `workflow_dispatch` | 手动触发，支持参数 |
| `repository_dispatch` | 接收上游仓库的事件 |

### 手动触发参数

- **force_rebuild**: 强制重新构建（忽略缓存）
- **skip_release**: 跳过发布 Release（仅构建）

---

## 📦 构建产物

每次成功构建后，会自动创建 Release 并上传：

| 文件 | 大小 | 说明 |
|------|------|------|
| `openclaw-docs-offline-YYYYMMDD-SHA7.tar.gz` | ~8MB | 离线版，包含完整文档 |
| `openclaw-docs-lite-YYYYMMDD-SHA7.tar.gz` | ~200KB | 轻量版，首次使用自动下载 |

### 版本号规则

```
v20240115-a1b2c3d
│  │          │
│  │          └── 上游 commit 前7位
│  └───────────── 日期 (YYYYMMDD)
└──────────────── 前缀 v
```

---

## 🔗 可选：上游主动触发

如果你希望 openclaw 主仓库在文档更新时**主动通知**你的同步仓库：

### 方案 A：通过 repository_dispatch（需要上游配合）

1. 在 openclaw 主仓库添加工作流（`.github/workflows/notify-docs-sync.yml`）

```yaml
# 此文件需要作为 PR 提交给 openclaw/openclaw
name: Notify Docs Sync

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger docs sync
        run: |
          curl -X POST \
            -H "Authorization: token ${{ secrets.DOCS_SYNC_PAT }}" \
            -H "Accept: application/vnd.github.v3+json" \
            https://api.github.com/repos/YOUR_USERNAME/openclaw-docs-sync/dispatches \
            -d '{"event_type": "docs-updated"}'
```

2. 在 openclaw 仓库添加 Secrets：`DOCS_SYNC_PAT`（Personal Access Token）

### 方案 B：Fork 后自行添加（推荐）

1. Fork openclaw/openclaw 到你的账号
2. 添加上述工作流文件
3. 定期从 upstream 同步

---

## 🔐 权限配置

### GitHub Token 权限

工作流使用默认的 `GITHUB_TOKEN`，需要以下权限：

```yaml
permissions:
  contents: write    # 创建 Release
  actions: read      # 读取工作流
```

### Secrets（可选）

| Secret | 用途 |
|--------|------|
| `DOCS_SYNC_PAT` | 上游仓库触发下游时使用的 Token |
| `NOTIFY_WEBHOOK` | 构建完成后发送通知（如 Discord、Slack） |

---

## 📝 维护指南

### 查看同步状态

在仓库根目录会生成两个文件：

- `.last-sync-commit`: 上次同步的 commit SHA
- `.last-sync-date`: 上次同步时间

### 重新同步

如果同步失败或需要强制更新：

```bash
# 方法 1: GitHub Web UI
# Actions → Sync and Build Docs → Run workflow → force_rebuild: true

# 方法 2: 本地删除缓存
rm .last-sync-commit
git add .last-sync-commit
git commit -m "Reset sync state"
git push
```

### 更新工作流

修改 `.github/workflows/sync-docs.yml` 后推送：

```bash
git add .github/workflows/sync-docs.yml
git commit -m "ci: update workflow"
git push
```

---

## 🐛 故障排查

### 问题：Cron 不触发

**原因**: GitHub Actions 的 cron 在仓库 60 天无活动后会暂停

**解决**: 
- 手动触发一次恢复
- 或使用 [keepalive-workflow](https://github.com/marketplace/actions/keepalive-workflow)

### 问题：Sparse checkout 失败

**日志**: `error: unknown option 'filter'`

**解决**: 更新 Git 版本（工作流已使用 `ubuntu-latest`，通常没问题）

### 问题：Release 创建失败

**原因**: 权限不足

**解决**: 检查仓库 Settings → Actions → General → Workflow permissions 设置为 "Read and write permissions"

---

## 🎨 高级配置

### 添加通知

在工作流末尾添加：

```yaml
- name: Notify Discord
  uses: Ilshidur/action-discord@master
  with:
    args: "✅ OpenClaw 文档已更新: ${{ needs.build.outputs.version }}"
  env:
    DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
```

### 多平台构建

支持 macOS、Windows 用户的 Skill 包：

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
```

### 缓存优化

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.openclaw/docs-cache
    key: docs-${{ github.sha }}
    restore-keys: docs-
```

---

## 📚 相关文档

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Repository Dispatch Event](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
- [Git Sparse Checkout](https://git-scm.com/docs/git-sparse-checkout)

---

## 🤝 贡献

欢迎改进：
- 支持更多语言的过滤选项
- 添加更多的通知渠道
- 优化索引算法
- 添加文档 diff 功能

---

**Made with ❤️ by Paimon for 苏玖**
