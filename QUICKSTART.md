# 投资大佬知识库 - 新对话快速上手

> 本文件是给新对话的快速参考指南。

---

## 项目目标

构建一个**服务于个人量化投资系统**的知识库，整合段永平、巴菲特、芒格等投资大佬的思维框架。

**四个核心需求**：
1. 服务于量化系统 - 提取可执行的、可程序化的投资规则
2. 参考大佬Agent - 为投资决策提供大佬视角
3. 知识积累 - 构建持续更新的投资知识库
4. 可做视频 - 提取适合Remotion的素材

---

## 当前状态（2026-04-15）

### 段永平知识库 ✅ 基本完成

| 模块 | 状态 | 数据 |
|------|------|------|
| 书籍消化 | ✅ | 4本，5518页 |
| 语录提取 | ✅ | 11401条语录 |
| 公司评价 | ✅ | 31家公司，全语录+时间线 |
| 案例分析 | ✅ | 7个公司具体分析思路 |
| 量化规则 | ✅ | DYP规则体系 |
| 网站 | ✅ | 8页，端口3001 |
| Skill | ✅ | duanyongping-perspective |

### 待完成

| 优先级 | 任务 | 说明 |
|--------|------|------|
| 🔴 当前 | 接入雪球帖子 | 爬虫已创建，需Cookie |
| 🔴 当前 | 网站上线 | 部署到Vercel |
| 🟡 后续 | 其他大佬 | 巴菲特/芒格/塔勒布 |
| 🟢 最低 | 新人物 | 张一鸣/王宁/雷军 |

---

## 快速启动

### 1. 启动网站

```bash
cd ~/Desktop/投资大佬agent知识库/website
python3 -m http.server 3001
```

访问：**http://localhost:3001/**

### 2. 使用Skill（Claude Code）

在任意对话中输入：
```
/duanyongping-perspective
```
即可切换到段永平视角模式。

---

## 网站内容

| 页面 | 说明 | 更新 |
|------|------|------|
| 首页 | 项目介绍、核心原则 | ✅ |
| 公司评价 | 31家公司，按来源分组，全语录展示 | ✅ |
| 主题分类 | 12个投资主题 | ✅ |
| 经典语录 | 精选语录 | ✅ |
| 案例分析 | 7个公司的具体分析思路+时间演变 | ✅ |
| 决策框架 | 投资决策框架 | ✅ |
| Put交易 | 期权策略分析 | ✅ |

---

## 关键文件

| 文件 | 用途 |
|------|------|
| [README.md](README.md) | 项目总览 |
| [TODO.md](TODO.md) | 待办清单 |
| [WORK_LOG.md](WORK_LOG.md) | 工作记录 |
| website/js/companyData.js | 公司数据（含页码） |
| wiki/topics/段永平投资规则-量化版.md | 量化规则 |
| docs/雪球帖子接入指南.md | 雪球接入指南 |

---

## 雪球帖子接入（待完成）

脚本已创建：`scripts/crawl_xueqiu.py`

**步骤**：
1. 登录雪球，复制Cookie
2. 编辑脚本填入Cookie
3. 运行：`python3 scripts/crawl_xueqiu.py`
4. 数据保存到：`raw/xueqiu/`

详细说明：[docs/雪球帖子接入指南.md](docs/雪球帖子接入指南.md)

---

## 网站部署（待完成）

计划部署到 Vercel：

```bash
# 1. 初始化Git
cd ~/Desktop/投资大佬agent知识库
git init
git add .
git commit -m "Initial commit"

# 2. 创建GitHub仓库后推送
git remote add origin https://github.com/你的用户名/投资大佬agent知识库.git
git push -u origin main

# 3. 连接Vercel自动部署
# 访问 https://vercel.com 并导入仓库
```

---

## 工作流（知识库构建流程）

### 第一阶段：资料收集
1. 收集原始书籍/PDF/采访等资料
2. 放入 `raw/` 目录

### 第二阶段：消化提取
```bash
# 激活虚拟环境
source .venv/bin/activate

# 提取书籍内容
python3 scripts/extract_duanyongping.py

# 分析内容
python3 scripts/analyze_duanyongping.py

# 提取公司语录
python3 scripts/extract_company_quotes.py
```

### 第三阶段：数据增强
```bash
# 增强公司数据（加入时间维度）
python3 scripts/enhance_company_data.py
python3 scripts/enhance_with_timeline.py
```

### 第四阶段：网站更新
1. 修改 `website/` 下的HTML文件
2. 更新 `website/js/companyData.js` 数据
3. 本地测试后部署

### 第五阶段：Skill创建
1. 创建 `~/.claude/skills/你的skill名/SKILL.md`
2. 包含：身份卡、心智模型、决策启发式、表达DNA

---

## 方法论参考

本项目采用 **Karpathy llm-wiki** 方法论：
- 提取(Extract) → 分类(Index) → 索引(Store) → 展示(Display)
- 核心：用AI辅助构建个人知识库

---

*最后更新：2026-04-15*
