# 投资大佬知识库 - 项目总结

> 最后更新：2026-04-14

---

## 项目概览

**目标**：构建服务于个人量化投资系统的知识库，整合段永平、巴菲特、芒格等投资大佬的思维框架。

**核心价值**：
- 服务于量化系统 - 提取可执行的、可程序化的投资规则
- 参考大佬Agent - 为投资决策提供大佬视角
- 知识积累 - 构建持续更新的投资知识库
- 可做视频 - 提取适合Remotion的素材

---

## 当前完成度

### 段永平知识库 ✅ 已完成

| 模块 | 状态 | 说明 |
|------|------|------|
| 知识库Wiki | ✅ | entities/topics/synthesis/structured |
| 网站 (8页) | ✅ | 端口3001，含完整页码来源 |
| 书籍消化 | ✅ | 4本，5518页，3626条语录 |
| 采访消化 | ✅ | 方三文采访已消化 |
| 公司评价 | ✅ | 31家公司，含12055条语录 |
| Put交易案例 | ✅ | 含450条期权相关语录 |
| 量化规则 | ✅ | 可执行的DYP规则体系 |
| Skill | ✅ | duanyongping-perspective |

### 其他大佬知识库 ❌ 待开发

- [ ] 巴菲特
- [ ] 芒格
- [ ] 塔勒布
- [ ] 张一鸣
- [ ] 王宁
- [ ] 雷军

---

## 网站内容 (端口3001)

### 页面清单

| 页面 | 文件 | 内容 |
|------|------|------|
| 首页 | index.html | 项目介绍、核心原则、数据统计 |
| 公司评价 | companies.html | 31家公司，按类型筛选，含页码 |
| 主题分类 | topics.html | 12个投资主题 |
| 经典语录 | quotes.html | 精选语录 |
| 案例分析 | cases.html | 网易/苹果/茅台/腾讯/百度 |
| 决策框架 | framework.html | 投资决策框架 |
| Put交易 | puts.html | 期权策略分析，含450条语录 |

### 数据统计

| 指标 | 数量 |
|------|------|
| 已消化书籍 | 4本 (5518页) |
| 消化采访 | 1篇 |
| 提取语录 | 3626条 |
| 公司语录 | 12055条（含页码） |
| 公司评价 | 31家 |
| 网站页面 | 8个 |

---

## 知识库结构

```
wiki/
├── index.md                          # 总索引
├── entities/
│   └── 段永平.md                    # 人物主页
├── topics/
│   ├── 价值投资.md
│   ├── 能力圈.md
│   ├── 平常心.md
│   ├── 本分.md
│   ├── Stop Doing List.md
│   ├── 段永平投资规则-量化版.md    # 可执行规则
│   └── 段永平方三文采访.md         # 采访消化
├── synthesis/
│   └── 段永平投资案例分析.md
└── structured/
    ├── analysis.json                # 主题分析
    └── company_analysis.json        # 公司分析（含页码）
```

---

## 关键文件

| 文件 | 用途 |
|------|------|
| WORK_LOG.md | 工作记录 |
| TODO.md | 待办清单 |
| website/js/companyData.js | 公司数据（含页码来源） |
| wiki/topics/段永平投资规则-量化版.md | 量化规则体系 |
| wiki/topics/段永平方三文采访.md | 采访消化 |
| raw/interviews/duanyongping_fangsanwen_interview.txt | 采访原文 |
| ~/.claude/skills/duanyongping-perspective/SKILL.md | 段永平Skill |

---

## 下一步工作

### 高优先级

1. **其他大佬知识库** 🔴
   - 巴菲特知识库
   - 芒格知识库
   - 塔勒布知识库

### 中优先级

2. **数据接入** 🟡
   - 雪球帖子接入（需用户提供Cookie）
   - 微信公众号博主接入

3. **新人物** 🟡
   - 张一鸣
   - 王宁
   - 雷军

### 低优先级

4. **Remotion视频** 🟢
   - 视频脚本素材
   - Remotion配置

---

## 快速启动

```bash
# 启动网站
cd ~/Desktop/投资大佬agent知识库/website
python3 -m http.server 3001

# 访问
open http://localhost:3001/

# 提取数据
cd ~/Desktop/投资大佬agent知识库
source .venv/bin/activate
python3 scripts/extract_company_quotes.py
```
