# 投资大佬知识库 - Agent 使用指南

> 本知识库结合 Karpathy 的 llm-wiki 方法论与女娲思维蒸馏框架，构建一个持续积累、互相链接的投资智慧库。

---

## 核心工具

| Skill | 功能 | 安装位置 |
|-------|------|----------|
| **karpathy-llm-wiki** | 个人知识库构建与管理 | `~/.claude/skills/karpathy-llm-wiki` |
| **女娲 (nuwa)** | 思维蒸馏 - 从大佬著作中提取思维框架 | `~/.claude/skills/nuwa` |

---

## Part 1: karpathy-llm-wiki 使用指南

### 核心理念

> "The LLM writes and maintains the wiki; the human reads and asks questions."
> "The wiki is a persistent, compounding artifact."

**核心区别**：不是每次问问题 AI 都从头读原始文件，而是把知识编译一次后持续维护，越用越丰富。

### 三层架构

```
raw/           ← 原始素材（不可变）
wiki/          ← AI 整理的知识文章（可编辑）
SKILL.md      ← 配置层（定义工作流程）
```

### 初始化知识库

```bash
# 在知识库文件夹中告诉 Agent：
"帮我初始化一个 llm-wiki 知识库"
```

### 消化素材（Ingest）

```bash
# 消化一本电子书
"帮我消化《穷查理宝典》"

# 消化一个链接
"帮我消化这篇：https://..."

# 消化一个 PDF 文件
"帮我消化这个文件：./巴菲特致股东的信2024.pdf"
```

**消化流程**：
1. Agent 读取原始文件 → 保存到 `raw/`
2. Agent 提取核心知识点 → 生成到 `wiki/`
3. 自动创建/更新实体页、主题页、索引页

### 查询知识库

```bash
# 查询已整理的知识
"关于护城河理论，我知道什么？"
"段永平怎么看能力圈？"
"巴菲特和芒格在风险观点上有什么差异？"
```

### 健康检查（Lint）

```bash
# 检查知识库状态
"检查一下知识库的健康状态"
"帮我 lint 一下"
```

### 结晶化（Crystallize）

```bash
# 把一段有价值的对话保存到知识库
"这段对话很有价值，帮我结晶化"
"把这个分析记进知识库"
```

---

## Part 2: 女娲 (nuwa) 使用指南

### 核心理念

女娲是一个「思维蒸馏框架」——不是简单摘录语录，而是从大佬的著作/言论中提炼出**可复用的思维模型**，让你在分析问题时能用大佬的视角思考。

### 两种入口

#### 入口一：明确人名 → 直接蒸馏

```bash
"造一个巴菲特的 skill"
"蒸馏一个段永平的思维框架"
"做个芒格视角的 skill"
```

#### 入口二：模糊需求 → 诊断推荐 → 再蒸馏

```bash
"我想提升投资决策质量，有什么思维框架能帮我？"
"我需要一个思维顾问，帮我分析商业决策"
```

### 触发词

以下任一触发词都会激活女娲：

| 触发词 | 场景 |
|--------|------|
| 「造skill」 | 想创建新的思维 skill |
| 「蒸馏XX」 | 蒸馏某人的思维框架 |
| 「女娲」 | 直接召唤女娲 |
| 「造人」 | 从零造一个思维体 |
| 「XX的思维方式」 | 获取某人的思考方式 |
| 「做个XX视角」 | 从特定视角分析 |

### 已有的投资类 Skill

可直接安装使用：

```bash
npx skills add Panmax/buffett-skill      # 巴菲特
npx skills add Panmax/dalio-skill        # 达利欧
npx skills add Panmax/marks-skill        # 霍华德·马克斯
npx skills add alchaincyf/munger-skill   # 芒格
npx skills add Panmax/thiel-skill        # 彼得·蒂尔
npx skills add Panmax/lynch-skill        # 彼得·林奇
```

查看更多：[awesome-nuwa](https://github.com/Panmax/awesome-nuwa)

---

## Part 3: 知识库与思维蒸馏的结合

### 推荐工作流

```
1. 素材积累阶段
   ├── 用 karpathy-llm-wiki 消化书籍/文章/PDF
   └── 保存到 raw/ → 整理到 wiki/

2. 思维提炼阶段
   ├── 用女娲从消化后的知识中蒸馏思维框架
   └── 生成可复用的 skill

3. 实战应用阶段
   ├── 遇到投资决策问题时，调用对应 skill
   ├── 用大佬的思维框架分析
   └── 有价值的分析结晶化回知识库
```

### 使用示例

**场景**：读完段永平的投资问答录后

```bash
# Step 1: 消化书籍
"帮我消化《段永平投资问答录》"

# Step 2: 提炼思维框架
"女娲，帮我蒸馏段永平的投资思维"

# Step 3: 用新框架分析
"用段永平的视角分析一下腾讯的投资价值"

# Step 4: 保存有价值分析
"这个分析很好，帮我结晶化"
```

---

## Part 4: 本知识库结构

```
投资大佬agent知识库/
├── raw/                    # 原始素材（只读）
│   ├── buffett/           # 巴菲特相关
│   ├── munger/             # 芒格相关
│   ├── duanyongping/       # 段永平相关
│   └── ...
│
├── wiki/                   # 整理后的知识
│   ├── index.md           # 知识库索引
│   ├── log.md             # 操作日志
│   ├── entities/          # 实体页（概念、人、公司）
│   ├── topics/            # 主题页
│   ├── sources/           # 素材摘要页
│   ├── synthesis/         # 综合分析报告
│   └── queries/           # 保存的问答
│
├── skills/                # 蒸馏出的思维 skill
│   ├── buffett-perspective/
│   ├── munger-perspective/
│   └── ...
│
└── 本指南.md              # 你现在看的这个文件
```

---

## Part 5: 常用命令速查

| 需求 | 命令 |
|------|------|
| 初始化知识库 | `帮我初始化 llm-wiki` |
| 消化书籍 | `帮我消化《书名》` |
| 消化链接 | `帮我消化这篇：URL` |
| 查询知识 | `关于 XX 我知道什么？` |
| 健康检查 | `lint 一下知识库` |
| 结晶化 | `帮我结晶化这段对话` |
| 蒸馏思维 | `造一个 XXX 的 skill` |

---

## 参考资料

- **Karpathy llm-wiki 原版方法论**：
  https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

- **女娲 Skill 集合**：
  https://github.com/Panmax/awesome-nuwa

- **karpathy-llm-wiki Skill**：
  `~/.claude/skills/karpathy-llm-wiki/SKILL.md`

- **女娲 Skill**：
  `~/.claude/skills/nuwa/SKILL.md`

---

## 注意事项

1. **隐私安全**：消化素材前请确认不包含敏感信息（手机号、身份证、API密钥等）
2. **持续积累**：知识库的价值在于积累，不要期望一次消化完所有内容
3. **交叉验证**：不同大佬观点可能矛盾，这是正常的，记录下来并思考
4. **定期体检**：每隔一段时间运行一次 lint，保持知识库健康

---

*最后更新：2026-04-14*
