# OpenClaw Docs Skill - 完整规范文档

**版本**: 1.1.0  
**最后更新**: 2025-04-03  
**维护者**: Paimon (派蒙)

---

## 1. 技能概述

### 1.1 定位
OpenClaw Docs Skill 是 OpenClaw 生态的基础技能，提供官方文档的智能查询和导航服务。

### 1.2 核心价值
- **快速查询**: 毫秒级文档检索
- **精准定位**: 直接定位到相关章节
- **中文友好**: 支持中文关键词搜索英文文档
- **实时同步**: 自动保持文档最新

---

## 2. 触发机制

### 2.1 触发词（Keywords）

当用户在 OpenClaw 对话中提及以下词汇时自动触发：

| 类别 | 触发词 | 场景示例 |
|------|--------|----------|
| **查询** | 查文档、OpenClaw文档、怎么看 | "帮我查文档关于多智能体的" |
| **配置** | 怎么配置、如何设置 | "怎么配置 gateway？" |
| **概念** | 架构说明、原理 | "解释一下多智能体架构" |
| **功能** | 多智能体、skill开发 | "多智能体怎么工作的？" |
| **开发** | gateway配置、定时任务 | "定时任务怎么配置？" |
| **数据** | memory机制、记忆系统 | "memory是怎么存储的？" |

### 2.2 触发优先级
- **高优先级**: 直接文档查询（查文档 + 关键词）
- **中优先级**: 配置相关问题（怎么配置 + 功能名）
- **低优先级**: 概念性问题（什么是 + 概念名）

---

## 3. 使用场景

### 场景 A: 直接文档查询
**用户**: "帮我查一下多智能体怎么配置"

**Skill 执行**:
1. 识别关键词 "多智能体"
2. 匹配文档 `concepts/multi-agent.md`
3. 读取文档内容
4. 总结回答 + 提供配置示例

**输出示例**:
```
根据 OpenClaw 官方文档，多智能体配置通过 `agents.list` 实现：

[配置示例代码]

📄 来源: concepts/multi-agent.md
🔗 相关文档: gateway/configuration.md
```

### 场景 B: 故障排查
**用户**: "gateway 连不上怎么办？"

**Skill 执行**:
1. 识别问题类型（连接问题）
2. 搜索相关文档
3. 提供排查步骤

### 场景 C: 概念解释
**用户**: "什么是 delegate 架构？"

**Skill 执行**:
1. 匹配 `concepts/delegate-architecture.md`
2. 解释核心概念
3. 提供使用场景

---

## 4. 工作流程

### 4.1 标准响应流程

```
用户提问
    ↓
[触发检测] → 匹配触发词？
    ↓ 是
[意图识别] → 查询 / 配置 / 概念 / 故障
    ↓
[文档定位] → 速查表 / 搜索索引
    ↓
[内容读取] → read 工具读取文档
    ↓
[总结回答] → 结构化输出 + 引用来源
    ↓
[相关推荐] → 提供相关文档链接
```

### 4.2 文档读取规则

| 规则 | 说明 |
|------|------|
| **引用必须** | 每个回答必须注明文档来源 |
| **代码优先** | 配置类问题优先提供代码示例 |
| **结构化** | 使用表格、列表、代码块 |
| **中文回答** | 即使文档是英文，也用中文解释 |

---

## 5. 文档库结构

### 5.1 本地缓存位置
```
~/.openclaw/docs-cache/
├── concepts/          # 核心概念（30+ 文件）
│   ├── multi-agent.md
│   ├── delegate-architecture.md
│   └── ...
├── gateway/           # Gateway 配置（35+ 文件）
│   ├── configuration.md
│   └── ...
├── tools/             # 工具文档（40+ 文件）
│   ├── skills.md
│   └── ...
├── channels/          # 渠道配置（30+ 文件）
├── cli/               # CLI 文档（45+ 文件）
└── automation/        # 自动化（10+ 文件）
```

### 5.2 文档同步策略
- **自动同步**: 每天 UTC 02:00 检查更新
- **手动同步**: `./scripts/skill-wrapper.sh sync`
- **首次安装**: 自动执行完整同步

---

## 6. 技术实现

### 6.1 索引系统
- **索引文件**: `docs-index.json`
- **生成命令**: `./scripts/skill-wrapper.sh index`
- **更新频率**: 文档同步后自动重建

### 6.2 搜索算法
- **精确匹配**: 文档标题、路径
- **关键词匹配**: 文档内容关键词
- **模糊匹配**: 相似词、同义词

### 6.3 性能指标
- **索引大小**: ~200KB
- **搜索延迟**: <100ms
- **文档覆盖**: 400+ 官方文档

---

## 7. 维护指南

### 7.1 日常维护

```bash
# 检查文档状态
./scripts/skill-wrapper.sh stats

# 手动同步最新文档
./scripts/skill-wrapper.sh sync

# 重新生成索引
./scripts/skill-wrapper.sh index
```

### 7.2 故障排查

| 问题 | 解决步骤 |
|------|----------|
| 文档找不到 | 检查 `~/.openclaw/docs-cache/` 是否存在 |
| 索引损坏 | 删除 `docs-index.json` 后重建 |
| 同步失败 | 检查网络连接，重试 `sync` |

### 7.3 更新发布

1. **版本更新**:
   ```bash
   # 修改 SKILL.md 中的 version
   # 更新 CHANGELOG.md
   git commit -m "chore: bump version to 1.2.0"
   ```

2. **GitHub Actions 发布**:
   - 推送到 main 分支自动触发
   - 自动生成 Release
   - 打包离线版和轻量版

---

## 8. 与 Skill Creator 规范对照

### 8.1 合规检查清单

| 规范要求 | 实现状态 | 说明 |
|----------|----------|------|
| SKILL.md < 300 行 | ✅ | 61 行 |
| 标准目录结构 | ✅ | scripts/, references/, assets/ |
| Frontmatter 完整 | ✅ | name, description, metadata |
| 触发词明确 | ✅ | 10 个触发词 |
| 有参考文档 | ✅ | 4 个 reference 文件 |

### 8.2 最佳实践

1. **SKILL.md 保持精简**
   - 只放核心指令
   - 详细内容放 references/

2. **脚本工具化**
   - 提供统一入口 `skill-wrapper.sh`
   - 每个脚本单一职责

3. **文档可验证**
   - `validate-skill.sh` 检查结构
   - 确保符合规范

---

## 9. 扩展计划

### 9.1 V1.2 规划
- [ ] 语义搜索（向量索引）
- [ ] 文档摘要自动生成
- [ ] 多语言支持（中英混合）

### 9.2 V2.0 规划
- [ ] 技能市场集成
- [ ] 自动更新推送
- [ ] 社区文档贡献

---

## 10. 附录

### 10.1 快速命令参考

```bash
# 安装
./scripts/skill-wrapper.sh setup

# 搜索
./scripts/skill-wrapper.sh search "multi-agent"

# 统计
./scripts/skill-wrapper.sh stats

# 验证
./scripts/validate-skill.sh

# 清理
./scripts/skill-wrapper.sh clean
```

### 10.2 相关链接

- 官方仓库: https://github.com/clawsu/openclaw-docs-sync
- Skill Creator 规范: https://github.com/openclaw/skill-creator
- OpenClaw 文档: https://docs.openclaw.ai

---

**维护记录**:
- 2025-04-03: 按 Skill Creator 规范重构 (Paimon)
- 2025-04-02: 初始版本创建 (Paimon)

**License**: MIT
