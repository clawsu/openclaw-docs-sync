# OpenClaw Docs Skill - 快速开始指南

## 🎯 三种使用方式

### 方式一：GitHub Actions 自动同步（推荐）

**适合**：保持文档始终最新，自动发布

**步骤**：

```bash
# 1. Fork 或创建新仓库
git clone https://github.com/YOUR_USERNAME/openclaw-docs-sync.git
cd openclaw-docs-sync

# 2. 复制本 skill 文件
cp -r /Users/su/.openclaw/workspace/skills-import/openclaw-docs/* .

# 3. 提交并推送
git add .
git commit -m "Initial commit"
git push origin main

# 4. GitHub Web → Actions → Run workflow
```

**结果**：
- 每天自动检查上游更新
- 自动生成 Release 下载包
- 版本号：`v20240115-a1b2c3d`

---

### 方式二：本地使用（开发调试）

**适合**：开发调试，快速测试

**步骤**：

```bash
cd /Users/su/.openclaw/workspace/skills-import/openclaw-docs

# 1. 安装依赖（可选）
pip install -r requirements.txt

# 2. 拉取文档
python scripts/fetch-docs.py --path ./docs

# 3. 生成索引
python scripts/build-index.py --docs-path ./docs

# 4. 搜索测试
python scripts/search-docs.py "multi-agent"
```

---

### 方式三：作为 OpenClaw Skill 使用

**适合**：在 OpenClaw 中直接使用

**步骤**：

```bash
# 1. 复制 skill 到 workspace
mkdir -p ~/.openclaw/workspace/skills/openclaw-docs
cp -r skills-import/openclaw-docs/* ~/.openclaw/workspace/skills/openclaw-docs/

# 2. 配置文档路径
echo '{"docs_path": "~/.openclaw/docs-cache"}' > ~/.openclaw/workspace/skills/openclaw-docs/config.json

# 3. 拉取文档
python ~/.openclaw/workspace/skills/openclaw-docs/scripts/fetch-docs.py

# 4. 重启 OpenClaw
openclaw gateway restart
```

---

## 📋 文件说明

```
openclaw-docs/
├── SKILL.md                    # 技能定义（必需）
├── README.md                   # 用户文档
├── QUICKSTART.md              # 本文件
├── GITHUB_ACTIONS_SETUP.md    # GitHub Actions 详细指南
├── DISTRIBUTION.md            # 分发指南
├── requirements.txt           # Python 依赖
├── config.json                # 配置（自动生成）
├── docs-index.json            # 索引（自动生成）
├── .github/
│   └── workflows/
│       └── sync-docs.yml      # GitHub Actions 主工作流
└── scripts/
    ├── fetch-docs.py          # 文档拉取器 ⭐核心
    ├── clean-docs.py          # 内容清洗
    ├── build-index.py         # 索引生成
    ├── search-docs.py         # 搜索工具
    └── setup.py               # 安装向导
```

---

## 🔧 常用命令

```bash
# 搜索文档
python scripts/search-docs.py "multi-agent"

# 重新生成索引
python scripts/build-index.py

# 强制重新拉取
python scripts/fetch-docs.py --force

# 跳过清洗快速拉取
python scripts/fetch-docs.py --skip-clean
```

---

## 🐛 常见问题

### Q: 找不到文档？
```bash
# 检查配置
cat config.json
# 应包含: {"docs_path": "/path/to/docs"}

# 重新运行安装向导
python scripts/setup.py
```

### Q: 索引过时？
```bash
# 重新生成
python scripts/build-index.py
```

### Q: 如何更新到最新文档？
```bash
# 本地模式
python scripts/fetch-docs.py --force

# GitHub Actions 模式
# 访问 Actions 页面 → Run workflow
```

---

## 📚 下一步

- 详细配置 → `GITHUB_ACTIONS_SETUP.md`
- 分发指南 → `DISTRIBUTION.md`
- 技能使用 → `SKILL.md`

---

**遇到问题？** 查看 `DISTRIBUTION.md` 的故障排除章节。
