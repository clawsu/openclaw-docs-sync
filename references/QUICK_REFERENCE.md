# OpenClaw Docs Skill - 快速参考手册

## 🚀 一分钟上手

### 安装
```bash
cd ~/github-deploy/openclaw-docs-sync
./scripts/skill-wrapper.sh setup
```

### 搜索文档
```bash
# 搜索关键词
./scripts/skill-wrapper.sh search "multi-agent"

# 搜索中文关键词（自动匹配英文文档）
./scripts/skill-wrapper.sh search "多智能体"
```

### 常用命令
```bash
./scripts/skill-wrapper.sh stats      # 查看文档统计
./scripts/skill-wrapper.sh sync       # 同步最新文档
./scripts/skill-wrapper.sh index      # 重新生成索引
./scripts/validate-skill.sh           # 验证技能结构
```

---

## 🎯 触发词速查

在 OpenClaw 对话中提及以下词汇会自动触发：

| 你想问 | 触发词 | 示例 |
|--------|--------|------|
| 查询文档 | 查文档、OpenClaw文档 | "帮我查文档关于多智能体的" |
| 配置问题 | 怎么配置、如何设置 | "怎么配置 gateway？" |
| 概念解释 | 架构说明、原理 | "解释一下多智能体架构" |
| 功能使用 | 多智能体、skill开发 | "多智能体怎么工作的？" |
| 故障排查 | 连不上、报错 | "gateway 连不上怎么办？" |

---

## 📚 核心文档速查表

| 你的问题 | 对应文档 |
|---------|----------|
| 多智能体路由 | `concepts/multi-agent.md` |
| 委托架构 | `concepts/delegate-architecture.md` |
| Agent 运行机制 | `concepts/agent-loop.md` |
| 系统架构 | `concepts/architecture.md` |
| 会话管理 | `concepts/session.md` |
| Gateway 配置 | `gateway/configuration.md` |
| 安全配置 | `gateway/security.md` |
| 沙盒机制 | `gateway/sandboxing.md` |
| Skill 开发 | `tools/skills.md` |
| 定时任务 | `automation/cron-jobs.md` |
| 记忆系统 | `concepts/memory.md` |

---

## 🛠️ 工作流程

### 标准查询流程
```
1. 用户提问（含触发词）
   ↓
2. Skill 识别意图
   ↓
3. 搜索/匹配文档
   ↓
4. 读取文档内容
   ↓
5. 结构化回答 + 引用来源
```

---

## 📁 项目结构

```
openclaw-docs-sync/
├── SKILL.md              # 技能定义（61行精简版）
├── README.md             # 快速入门
├── docs/
│   ├── SKILL_SPECIFICATION.md  # 完整规范
│   └── QUICK_REFERENCE.md      # 本文件
├── scripts/              # 工具脚本
│   ├── skill-wrapper.sh       # 统一命令入口
│   ├── validate-skill.sh      # 结构验证
│   ├── fetch-docs.py          # 文档拉取
│   ├── search-docs.py         # 文档搜索
│   ├── build-index.py         # 索引生成
│   └── setup.py               # 安装向导
└── references/           # 扩展文档
    ├── architecture.md         # 架构说明
    ├── usage-guide.md          # 完整使用指南
    ├── github-actions-setup.md # 自动化部署
    └── distribution-guide.md   # 分发策略
```

---

## ⚡ 快速命令

### 文档操作
```bash
# 安装/配置
./scripts/skill-wrapper.sh setup

# 同步最新文档
./scripts/skill-wrapper.sh sync

# 重新生成索引
./scripts/skill-wrapper.sh index

# 搜索文档
./scripts/skill-wrapper.sh search "关键词"

# 查看统计
./scripts/skill-wrapper.sh stats

# 清理缓存
./scripts/skill-wrapper.sh clean
```

### 开发维护
```bash
# 验证技能结构
./scripts/validate-skill.sh

# 查看帮助
./scripts/skill-wrapper.sh help
```

---

## 🔍 故障排查

| 问题 | 解决步骤 |
|------|----------|
| 文档找不到 | 检查 `~/.openclaw/docs-cache/` 是否存在，运行 `sync` |
| 搜索无结果 | 重新生成索引 `index` |
| 同步失败 | 检查网络，重试 `sync` |
| 权限错误 | 确保脚本有执行权限 `chmod +x scripts/*.sh` |

---

## 📝 回答规范

当 Skill 被触发时，回答必须包含：

1. **结构化内容** - 使用表格、列表、代码块
2. **代码示例** - 配置类问题提供可复制的代码
3. **引用来源** - 注明引用的文档路径
4. **相关链接** - 推荐相关文档

---

## 🔄 更新维护

### 自动更新（GitHub Actions）
- 每天 UTC 02:00 自动同步
- 推送到 main 分支自动发布 Release

### 手动更新
```bash
./scripts/skill-wrapper.sh sync && ./scripts/skill-wrapper.sh index
```

---

## 📖 完整文档

- 规范文档: `docs/SKILL_SPECIFICATION.md`
- 架构说明: `references/architecture.md`
- 使用指南: `references/usage-guide.md`

---

**版本**: 1.1.0  
**更新**: 2025-04-03
