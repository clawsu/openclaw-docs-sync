# OpenClaw Docs Skill 📚

OpenClaw 官方文档智能查询助手。

## ✨ 特性

- 🔍 **智能搜索** - 快速定位文档
- 🌍 **自动过滤** - 仅保留英文文档
- 📊 **索引加速** - 预建索引快速检索
- 🔧 **工具齐全** - 完整的 CLI 工具集

## 🚀 快速开始

### 一键安装

```bash
./scripts/skill-wrapper.sh setup
```

### 常用命令

```bash
# 搜索文档
./scripts/skill-wrapper.sh search "multi-agent"

# 同步最新文档
./scripts/skill-wrapper.sh sync

# 查看统计
./scripts/skill-wrapper.sh stats

# 验证技能结构
./scripts/validate-skill.sh
```

## 📁 项目结构

```
openclaw-docs/
├── SKILL.md                    # 技能核心定义
├── README.md                   # 本文件
├── scripts/                    # 工具脚本
│   ├── skill-wrapper.sh       # 统一命令入口 ⭐
│   ├── validate-skill.sh      # 结构验证
│   ├── fetch-docs.py          # 文档拉取
│   ├── search-docs.py         # 文档搜索
│   ├── build-index.py         # 索引生成
│   └── setup.py               # 安装向导
├── references/                 # 扩展文档
│   ├── usage-guide.md         # 完整使用指南
│   ├── architecture.md        # 架构说明
│   ├── github-actions-setup.md # 自动化部署
│   └── distribution-guide.md  # 分发策略
├── assets/                     # 资源文件
└── .github/                    # GitHub Actions
```

## 📚 详细文档

- `references/usage-guide.md` - 完整使用指南
- `references/architecture.md` - 系统架构
- `references/github-actions-setup.md` - 自动化部署
- `references/distribution-guide.md` - 分发策略

## 🎯 触发词

安装后，在 OpenClaw 中提及以下内容会自动触发本技能：

- 查文档、OpenClaw文档
- 多智能体、skill开发
- gateway配置、定时任务
- memory机制、架构说明

## 📄 License

MIT License
