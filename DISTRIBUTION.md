# OpenClaw Docs Skill - 分发指南

## 📦 分发方式选择

根据目标用户和使用场景，选择适合的分发方式：

| 方式 | 体积 | 网络需求 | 适用场景 |
|------|------|----------|----------|
| **智能拉取** | 200KB | 首次需要 | 推荐方案，自动获取 |
| **离线打包** | ~8MB | 无 | 内网环境，无网络 |
| **外部依赖** | 200KB | 无 | 已有文档仓库 |

---

## 🚀 方式一：智能拉取（推荐）

**Skill 体积：** 约 200KB（仅含脚本和索引逻辑）

**用户首次使用时自动：**
1. 从 GitHub sparse checkout 拉取 docs/
2. 过滤非英文文档（剔除 zh-CN, ja-JP 等）
3. 清洗内容（移除 HTML 注释等）
4. 生成索引

### 分发步骤

```bash
# 1. 确保 skill 目录结构正确
cd /Users/su/.openclaw/workspace/skills-import/openclaw-docs
ls
# 应包含: SKILL.md, README.md, scripts/

# 2. 测试脚本可运行
python3 scripts/fetch-docs.py --help

# 3. 打包 skill（不含文档）
tar -czf openclaw-docs-v1.0.0.tar.gz \
  --exclude='docs/' \
  --exclude='docs-index.json' \
  --exclude='config.json' \
  --exclude='__pycache__' \
  openclaw-docs/

# 4. 用户获取后，首次运行自动拉取
python3 scripts/setup.py
# 或
python3 scripts/fetch-docs.py
```

### 用户安装流程

```bash
# 1. 解压 skill
tar -xzf openclaw-docs-v1.0.0.tar.gz

# 2. 进入目录
cd openclaw-docs

# 3. 一键安装（自动拉取文档）
python3 scripts/setup.py

# 4. 开始使用
python3 scripts/search-docs.py "multi-agent"
```

---

## 📦 方式二：离线打包

**Skill 体积：** 约 8MB（含清洗后的 400 个英文文档）

**适用：** 无网络环境、内网部署、快速开箱即用

### 打包步骤

```bash
cd /Users/su/.openclaw/workspace/skills-import/openclaw-docs

# 1. 拉取并清洗文档
python3 scripts/fetch-docs.py --path ./docs

# 2. 确认文档已下载
ls docs/
# 应看到: index.md, concepts/, gateway/, channels/, ...

# 3. 生成索引
python3 scripts/build-index.py

# 4. 打包（含文档）
tar -czf openclaw-docs-offline-v1.0.0.tar.gz \
  --exclude='__pycache__' \
  openclaw-docs/

# 5. 检查体积
ls -lh openclaw-docs-offline-v1.0.0.tar.gz
# 预期: 约 8-10 MB
```

### 用户安装流程

```bash
# 1. 解压（开箱即用，无需网络）
tar -xzf openclaw-docs-offline-v1.0.0.tar.gz
cd openclaw-docs

# 2. 直接使用
python3 scripts/search-docs.py "multi-agent"
```

---

## 🔧 方式三：外部依赖

**Skill 体积：** 约 200KB

**适用：** 用户已有本地文档仓库

### 用户配置

```bash
# 方式 1: 运行向导
python3 scripts/setup.py
# 选择"使用现有文档"

# 方式 2: 手动创建配置
cat > config.json << 'EOF'
{
  "docs_path": "/path/to/existing/openclaw/docs"
}
EOF

# 然后生成索引
python3 scripts/build-index.py
```

---

## 📊 体积对比

| 内容 | 大小 | 说明 |
|------|------|------|
| 原始仓库（全量） | ~50 MB | git clone 完整仓库 |
| 仅 docs/ 目录 | ~10 MB | sparse checkout |
| 英文文档（过滤后） | ~6 MB | 移除多语言 |
| 清洗后 | ~5.5 MB | 移除注释、规范化 |
| 压缩包（tar.gz） | ~2-3 MB | gzip 压缩 |
| **离线版 Skill** | **~8 MB** | 含脚本+索引+文档 |
| **拉取版 Skill** | **~200 KB** | 仅脚本和逻辑 |

---

## 🎯 推荐策略

### 场景 1: 发布到 ClawHub

**推荐：** 智能拉取版（200KB）

- 用户首次使用自动下载
- 文档始终是最新（从 main 分支拉取）
- 减小 ClawHub 存储压力

```bash
# 打包（不含文档）
tar -czf openclaw-docs-v1.0.0.tar.gz \
  --exclude='docs/' \
  --exclude='docs-index.json' \
  --exclude='config.json' \
  openclaw-docs/
```

### 场景 2: 团队内部分享

**推荐：** 离线版（8MB）

- 无需网络，开箱即用
- 文档版本固定，稳定性高
- 适合 Docker 镜像、VM 模板

```bash
# 完整打包（含文档）
tar -czf openclaw-docs-offline-v1.0.0.tar.gz openclaw-docs/
```

### 场景 3: CI/CD 集成

**推荐：** 智能拉取 + 缓存

```yaml
# GitHub Actions 示例
- name: Cache OpenClaw Docs
  uses: actions/cache@v3
  with:
    path: ~/.openclaw/docs-cache
    key: openclaw-docs-${{ hashFiles('scripts/fetch-docs.py') }}

- name: Fetch Docs
  run: python scripts/fetch-docs.py --path ~/.openclaw/docs-cache
```

---

## 🔒 私有部署

如需使用私有文档仓库：

```bash
# 1. 修改 fetch-docs.py
GITHUB_REPO = "https://github.com/your-org/private-docs.git"

# 2. 使用 SSH 或 Token
export GITHUB_TOKEN=ghp_xxxx
python scripts/fetch-docs.py

# 或使用 SSH
git clone git@github.com:your-org/private-docs.git
```

---

## 📋 发布检查清单

- [ ] 脚本可执行权限：`chmod +x scripts/*.py`
- [ ] 测试安装流程：`python scripts/setup.py`
- [ ] 测试搜索功能：`python scripts/search-docs.py test`
- [ ] 验证索引生成：`ls docs-index.json`
- [ ] 检查体积：`du -sh openclaw-docs/`
- [ ] 文档完整性：`ls docs/index.md`
- [ ] 版本号更新：`SKILL.md` 中的 version
- [ ] README 更新：安装步骤和下载链接

---

## 🐛 故障排除

### 问题：Git 命令未找到
```bash
# macOS
brew install git

# Ubuntu/Debian
sudo apt-get install git

# 验证
git --version
```

### 问题：网络超时
```bash
# 使用镜像
export GITHUB_REPO="https://ghproxy.com/https://github.com/openclaw/openclaw.git"
python scripts/fetch-docs.py
```

### 问题：权限拒绝
```bash
# 检查目录权限
chmod 755 ~/.openclaw
chmod 755 ~/.openclaw/docs-cache
```

---

## 📚 相关文档

- `SKILL.md` - 技能定义和使用规范
- `README.md` - 用户指南
- `scripts/fetch-docs.py` - 文档拉取器
- `scripts/setup.py` - 安装向导
