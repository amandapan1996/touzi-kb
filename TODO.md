# 投资大佬知识库 - 待办事项

> 本文件记录所有待完成的工作，供新session参考。

---

## 项目背景

构建一个服务于个人量化投资系统的知识库，整合段永平、巴菲特、芒格等投资大佬的思维框架。

**核心目标**：
1. 服务于量化系统 - 提取可执行的、可程序化的投资规则
2. 参考大佬Agent - 为投资决策提供大佬视角
3. 知识积累 - 构建持续更新的投资知识库
4. 可做视频 - 提取适合Remotion的素材

---

## 进度概览

| 人物 | 主页 | 书籍消化 | 公司评价 | 量化规则 | Put案例 | 采访消化 | Skill |
|------|------|----------|----------|----------|---------|---------|-------|
| 段永平 | ✅ | ✅ | ✅(全语录+时间线) | ✅ | ✅ | ✅ | ✅ |
| 巴菲特 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 芒格 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 塔勒布 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 张一鸣 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 王宁 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 雷军 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## 已完成工作

### 1. 段永平知识库 ✅

#### 网站（端口3001）
- [x] 首页 (index.html)
- [x] 公司评价 (companies.html) - 含页码来源
- [x] 主题分类 (topics.html)
- [x] 经典语录 (quotes.html)
- [x] 案例分析 (cases.html)
- [x] 决策框架 (framework.html)
- [x] Put交易 (puts.html)
- [x] 导航统一 ✅

#### 数据文件
- [x] analysis.json - 主题分析数据
- [x] company_analysis.json - 公司分析（含页码来源）
- [x] companyData.js - 网站数据

#### Skill
- [x] duanyongping-perspective/SKILL.md

#### 量化规则
- [x] wiki/topics/段永平投资规则-量化版.md

#### 消化书籍（5518页）
- [x] 投资逻辑篇 - 426页
- [x] 商业逻辑篇 - 353页
- [x] 博客文章合集 - 4439页
- [x] 帖子合集 - 300页

#### 采访消化
- [x] 方三文采访 - raw/interviews/duanyongping_fangsanwen_interview.txt
- [x] 采访消化版 - wiki/topics/段永平方三文采访.md

---

## 当前任务（待完成）

### 1. 接入雪球帖子 🔴

**状态**：脚本已创建，需填入Cookie

**文件**：
- `scripts/crawl_xueqiu.py` - 爬虫脚本
- `docs/雪球帖子接入指南.md` - 使用指南
- `raw/xueqiu/` - 数据保存目录

**步骤**：
1. 登录雪球，复制Cookie
2. 编辑 `scripts/crawl_xueqiu.py`，填入 `COOKIE` 常量
3. 运行：`python3 scripts/crawl_xueqiu.py`
4. 数据保存到 `raw/xueqiu/`

### 2. 工作流提炼 🔴

段永平完成后，需要总结标准化知识库构建流程。

---

## 2026-04-15 更新

### 网站页面重构 ✅

#### companies.html - 公司评价页面重构
- 按来源分组展示语录（帖子合集、博客文章合集、投资逻辑篇、商业逻辑篇）
- 展示全部语录，不再限制数量
- 提取语录中的日期信息
- 显示来源、页码、时间

#### cases.html - 案例分析页面重构
- 为每个公司添加具体分析思路
- 包含：一句话总结、为什么买入、观点演变、关键洞见
- 案例：网易、苹果、腾讯、茅台、阿里巴巴、雅虎、百度

### 数据增强脚本 ✅

- `scripts/enhance_company_data.py` - 增强公司评价数据
- `scripts/build_company_timeline.py` - 构建时间线
- `scripts/enhance_with_timeline.py` - 时间线与语录关联

### 输出文件

- `wiki/structured/company_analysis_enhanced.json` - 增强后的公司数据
- `wiki/structured/company_analysis_timeline.json` - 带时间线的公司数据
- `wiki/structured/timeline_raw.json` - 原始时间线数据

---

## 待开发人物

### 中优先级

#### 巴菲特 🟡
#### 芒格 🟡
#### 塔勒布 🟡

### 低优先级

#### 张一鸣 🟢
#### 王宁 🟢
#### 雷军 🟢

---

## 技术信息

### 文件位置
```
~/Desktop/投资大佬agent知识库/
├── wiki/                    # 知识库核心
│   ├── entities/           # 人物主页
│   ├── topics/             # 主题页
│   ├── synthesis/          # 综合分析
│   └── structured/         # 结构化数据
├── website/               # 网站（端口3001）
│   ├── index.html
│   ├── companies.html
│   ├── topics.html
│   ├── quotes.html
│   ├── cases.html
│   ├── framework.html
│   ├── puts.html
│   └── js/companyData.js
├── raw/                    # 原始素材
│   ├── duanyongping/
│   │   └── extracted/     # 已消化的内容
│   ├── interviews/         # 采访原文
│   └── xueqiu/            # 雪球数据（待获取）
├── scripts/               # 工具脚本
├── docs/                  # 文档
└── .ports.json            # 端口配置
```

### Skill位置
```
~/.claude/skills/
├── duanyongping-perspective/SKILL.md  ✅
└── nuwa/                              # 女娲框架
```

### 启动网站
```bash
cd ~/Desktop/投资大佬agent知识库/website
python3 -m http.server 3001
```

---

## 数据统计

| 数据类型 | 数量 |
|----------|------|
| 已消化书籍 | 4本 (5518页) |
| 消化采访 | 1篇 (方三文采访) |
| 提取语录 | 3626条 |
| 公司语录 | 12055条（含页码） |
| 公司评价 | 31家 |
| 网站页面 | 8个 |

---

## 关键文件

| 文件 | 用途 |
|------|------|
| [QUICKSTART.md](QUICKSTART.md) | 新对话快速上手 ⭐ |
| [README.md](README.md) | 项目总结 |
| [WORK_LOG.md](WORK_LOG.md) | 工作记录 |
| [docs/雪球帖子接入指南.md](docs/雪球帖子接入指南.md) | 雪球接入指南 |
| [website/js/companyData.js](website/js/companyData.js) | 公司数据（含页码） |
| [wiki/topics/段永平投资规则-量化版.md](wiki/topics/段永平投资规则-量化版.md) | 量化规则 |

---

*最后更新：2026-04-15*
