# OpenClaw Docs Skill 架构说明

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenClaw Gateway                          │
│                     (WebSocket :18789)                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ invoke skill
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              openclaw-docs Skill                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ SKILL.md    │  │ scripts/    │  │ references/         │  │
│  │ (core)      │  │ (tools)     │  │ (extended docs)     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ fetch-docs  │  │ search-docs │  │ build-index         │  │
│  │ (sync)      │  │ (query)     │  │ (index)             │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ read/write
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 Local File System                            │
│  ~/.openclaw/docs-cache/        docs-index.json             │
│  - concepts/                    config.json                  │
│  - gateway/                                                  │
│  - tools/                                                    │
│  - ...                                                       │
└─────────────────────────────────────────────────────────────┘

           GitHub Actions (Optional)
           ┌─────────────────────┐
           │ - Scheduled sync    │
           │ - Auto release      │
           │ - Multi-format pkg  │
           └─────────────────────┘
```

## 数据流

```
1. 触发
   User Query → OpenClaw → Skill Trigger

2. 搜索
   Skill → search-docs.py → docs-index.json → Results

3. 读取
   Skill → read file → docs-cache/ → Content

4. 回答
   Skill → Summarize → Cite Source → User
```

## 模块职责

| 模块 | 职责 | 输入 | 输出 |
|------|------|------|------|
| SKILL.md | 核心指令、触发词、速查表 | - | Skill behavior |
| fetch-docs.py | 拉取、过滤、清洗文档 | GitHub repo | docs-cache/ |
| search-docs.py | 索引搜索 | docs-index.json | Results list |
| build-index.py | 生成搜索索引 | docs-cache/ | docs-index.json |
| setup.py | 安装向导 | User input | Config + docs |

## 扩展点

1. **添加新文档源**
   - 修改 fetch-docs.py 中的 GITHUB_REPO
   - 添加新的语言过滤规则

2. **自定义搜索**
   - 修改 search-docs.py 的搜索算法
   - 支持模糊匹配、语义搜索

3. **集成外部服务**
   - 添加 Algolia/Elasticsearch 索引
   - 实现实时文档同步
