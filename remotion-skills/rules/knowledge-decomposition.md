# 深度知识拆解

把任何复杂的书/概念拆解成可视化视频脚本，核心是展示思考过程而非结论。融合HKRR理论和钩子设计，让人停不下来。

## 核心理念

**结论不重要，思考过程才是价值。**

看视频的人不需要记住结论，而是获得一种**思考能力**——以后遇到类似问题也知道怎么想。

**让人停不下来 = 每一步都有钩子 + 每一步都有获得感**

## 适用范围

- 任何"难的书"（投资哲学、科学原理、商业洞察、历史规律）
- 任何"高大上的概念"（第一性原理、复利效应、护城河）
- 任何"名人智慧"（巴菲特、芒格、乔布斯、马斯克）

---

## HKRR 理论（来自影视飓风）

| 要素 | 定义 | 在知识拆解中的应用 |
|------|------|------------------|
| H (Happiness) | 快乐/轻松 | 用幽默、反差、意外点让内容有趣 |
| K (Knowledge) | 知识/技能 | 核心知识点，必须讲清楚 |
| R (Resonance) | 共鸣 | 戳中观众的困惑/痛点 |
| R (Rhythm) | 节奏 | 紧凑不拖沓，每个Step有节奏感 |

**要求：每个Step至少满足 K + (H/R) 之一**

---

## 五步拆解框架

```
Step 1: 场景入口 —— Hook! 戳中痛点，让人想继续看
Step 2: 原有认知 —— 引发共鸣，让观众"就是我"
Step 3: 认知冲突 —— 制造悬念，让观众"然后呢"
Step 4: 新框架 —— K! 核心知识，详细拆解
Step 5: 验证/应用 —— R! 回答"所以呢"，让观众获得获得感
```

---

## 工作流程

### Step 0: 确定拆解对象

```
你要拆解的是什么？
1. 一本书（告诉我书名和作者）
2. 一个概念（告诉我概念名）
3. 一个原理（告诉我原理名）

另外，告诉我：
- 目标观众是谁？（投资新手/职场人/所有人）
- 他们最常见的困惑是什么？
```

### Step 1: 提取核心知识点

从书中提取3-5个核心知识点（不是结论，是"思考方式"）

**方法**：
- 找作者反复强调的"思维模型"
- 找作者用来支撑观点的"案例"
- 找作者反驳的"主流观点"
- 找反直觉的"洞察"

### Step 2: 为每个知识点设计拆解

对每个Step，必须设计：

```json
{
  "step": 1,
  "name": "场景入口",
  "hkrr": "H+R",
  "hook": "股价暴跌50%你怎么办？",
  "visual": {
    "type": "animation",
    "content": "红色K线向下，恐慌的人脸",
    "animation": "快速下坠 + 震动效果"
  },
  "voiceover": "假如你买了某只股票，突然暴跌50%..."
}
```

---

## 三种核心思考方式（Step 4 核心）

### 方式1：第一性原理

**本质**：回到最基本的不可再分的真理，绕过所有假设

**适用**：创新、颠覆性想法、重新定义问题

**拆解步骤**：
```
第1问：大家都在讨论的表面问题是什么？
第2问：这个问题背后的本质是什么？
第3问：有没有最基本的不可再分的元素？
第4问：能不能重新组合这些元素？
第5问：最优解是什么？
```

**示例：马斯克造火箭**
```
表面问题：火箭太贵，NASA要5000万
本质问题：火箭成本结构
本质元素：燃料、材料、人工、失败率
重新组合：可回收！燃料只占3%
最优解：造可回收火箭 → 成本降96%
```

---

### 方式2：逆向/概率思维

**本质**：从反面想 + 考虑不确定性和赔率

**适用**：投资、风险决策、竞争策略

**拆解步骤**：
```
第1问：顺向大家会怎么想？
第2问：逆向会怎么想？
第3问：什么情况下会亏/失败？
第4问：概率和赔率是多少？
第5问：有没有结构性保护？
```

**示例：巴菲特买银行**
```
顺向：金融危机来了，银行不能买
逆向：不是所有银行都一样
亏的情况：银行倒闭 CEO无能把钱烧光
概率：CEO可信 + 有优先股保护 = 亏的概率很低
保护：优先股，即使倒闭也优先偿还
```

---

### 方式3：框架思维

**本质**：多维度同时考虑，找到关键变量和关系

**适用**：复杂系统、商业分析、战略决策

**拆解步骤**：
```
维度1：有哪些关键变量？
维度2：变量之间是什么关系？
维度3：哪个变量最关键/杠杆效应最大？
维度4：如何调整这个变量影响全局？
```

**示例：分析一家公司**
```
变量：产品、渠道、价格、品牌、组织
关系：产品强→渠道配合→价格支撑→品牌强化→组织迭代
关键变量：产品（产品力是一切的前提）
调整：做出爆款产品 → 整个飞轮转起来
```

---

## 钩子设计指南

### 5种开场钩子

| 类型 | 公式 | 例子 |
|------|------|------|
| 痛点唤醒 | 你是不是也... | "你是不是也总觉得定投赚不了钱？" |
| 反常识 | 你以为...其实... | "你以为价值投资就是买蓝筹股？" |
| 承诺结果 | X分钟让你... | "3分钟让你搞懂巴菲特的买入逻辑" |
| 场景代入 | 想象一下... | "想象你买了股票然后暴跌50%" |
| 数据冲击 | X%的人都... | "90%的人都不知道巴菲特怎么看银行股" |

### Step之间的钩子

- Step 2 → Step 3: "但有一个人不这么看..."
- Step 3 → Step 4: "他是怎么做到的？"
- Step 4 → Step 5: "结果呢？"

---

## 输出格式（标准JSON脚本）

```json
{
  "script": {
    "meta": {
      "source": "《巴菲特致股东信》",
      "topic": "逆向投资思维",
      "duration": 60,
      "target_audience": "投资新手"
    },
    "hook": {
      "type": "场景代入",
      "content": "你买了一只股票，股价暴跌50%，所有人都在抛售..."
    },
    "steps": [
      {
        "step": 1,
        "name": "场景入口",
        "hkrr": "H+R",
        "hook": "股价暴跌50%你怎么办？",
        "visual": {
          "type": "animation",
          "content": "红色K线向下，恐慌的人脸",
          "animation": "快速下坠 + 震动",
          "素材需求": ["股价下跌K线图", "恐慌表情图标"]
        },
        "voiceover": "假如你买了某只股票，突然暴跌50%，朋友圈全是恐慌的消息，所有人都在抛售...你会怎么做？"
      },
      {
        "step": 2,
        "name": "原有认知",
        "hkrr": "R",
        "hook": "大多数人会...",
        "visual": {
          "type": "image",
          "content": "人群抛售的剪影",
          "animation": "淡入 + 缩放"
        },
        "voiceover": "大多数人的反应是：赶紧跑！金融危机来了，银行股不能碰！这就是当时的共识..."
      },
      {
        "step": 3,
        "name": "认知冲突",
        "hkrr": "H+R",
        "hook": "但有一个人不这么看",
        "visual": {
          "type": "animation",
          "content": "问号出现，一个人逆向前行",
          "animation": "问号弹出 + 人物滑入"
        },
        "voiceover": "但有一个人不这么看。巴菲特在2011年做了一个决定：买入美国银行。所有人都觉得他疯了..."
      },
      {
        "step": 4,
        "name": "新框架",
        "hkrr": "K",
        "hook": "他看到了什么？",
        "thinking_type": "reverse_probability",
        "visual": {
          "type": "diagram",
          "content": "框架图：管理层+安全边际+结构性保护",
          "animation": "逐个出现",
          "素材需求": ["投资决策流程图组件"]
        },
        "voiceover": "他看到的是三个问题：第一，这家银行和其他银行有什么不同？第二，管理层值不值得信任？第三，有没有结构性的保护？他用这三个问题建立了投资检查清单..."
      },
      {
        "step": 5,
        "name": "验证/应用",
        "hkrr": "K+R",
        "hook": "结果呢？",
        "visual": {
          "type": "animation",
          "content": "数字从5亿涨到70亿",
          "animation": "数字滚动 + 落定"
        },
        "voiceover": "结果到2018年，这笔投资价值70亿美元，14倍回报。下次遇到恐慌时，你可以用这个框架：先问'有什么不同'，再问'有没有保护'"
      }
    ],
    "takeaway": "不要问会不会涨，要问有什么不同"
  },
  "素材需求": {
    "images": ["股价下跌K线图", "巴菲特2011年照片", "美国银行logo"],
    "components": ["投资决策流程图", "数字滚动组件"],
    "animations": ["K线下坠动画", "数字滚动动画"]
  }
}
```

---

## 可复用的 Remotion 组件

### 1. 思维流程图 (ThinkingFlow)

```tsx
import { AbsoluteFill, Sequence, useCurrentFrame, interpolate, spring } from 'remotion';

interface ThinkingFlowProps {
  steps: string[];
  currentStep: number;
}

export const ThinkingFlow: React.FC<ThinkingFlowProps> = ({ steps, currentStep }) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill className="flex items-center justify-center">
      <div className="flex gap-4">
        {steps.map((step, i) => {
          const isActive = i === currentStep;
          const opacity = interpolate(frame, [i * 15, i * 15 + 10], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });

          return (
            <div key={i} className="flex items-center">
              <div
                className={`px-4 py-2 rounded-lg ${
                  isActive ? 'bg-blue-500 text-white' : 'bg-gray-200'
                }`}
                style={{ opacity }}
              >
                {step}
              </div>
              {i < steps.length - 1 && (
                <div className="mx-2 text-gray-400">→</div>
              )}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
```

### 2. 对比卡片 (ContrastCard)

```tsx
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

interface ContrastCardProps {
  left: { title: string; content: string };
  right: { title: string; content: string };
}

export const ContrastCard: React.FC<ContrastCardProps> = ({ left, right }) => {
  const frame = useCurrentFrame();

  const leftX = interpolate(frame, [0, 20], [-200, 0], {
    extrapolateRight: 'clamp',
  });
  const rightX = interpolate(frame, [10, 30], [200, 0], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill className="flex items-center justify-center gap-8">
      <div
        className="w-80 p-6 bg-red-100 rounded-xl border-2 border-red-300"
        style={{ transform: `translateX(${leftX}px)` }}
      >
        <h3 className="text-red-600 font-bold mb-2">{left.title}</h3>
        <p className="text-gray-700">{left.content}</p>
      </div>

      <div className="text-4xl text-gray-400">VS</div>

      <div
        className="w-80 p-6 bg-green-100 rounded-xl border-2 border-green-300"
        style={{ transform: `translateX(${rightX}px)` }}
      >
        <h3 className="text-green-600 font-bold mb-2">{right.title}</h3>
        <p className="text-gray-700">{right.content}</p>
      </div>
    </AbsoluteFill>
  );
};
```

### 3. 数字滚动动画 (AnimatedNumber)

```tsx
import { useCurrentFrame, interpolate, useVideoConfig } from 'remotion';

interface AnimatedNumberProps {
  from: number;
  to: number;
  durationInFrames: number;
  prefix?: string;
  suffix?: string;
}

export const AnimatedNumber: React.FC<AnimatedNumberProps> = ({
  from,
  to,
  durationInFrames,
  prefix = '',
  suffix = '',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = interpolate(frame, [0, durationInFrames], [0, 1], {
    extrapolateRight: 'clamp',
  });

  // 使用 easeOutExpo 缓动
  const easedProgress = 1 - Math.pow(2, -10 * progress);
  const currentValue = Math.round(from + (to - from) * easedProgress);

  return (
    <div className="text-6xl font-bold text-blue-600">
      {prefix}
      {currentValue.toLocaleString()}
      {suffix}
    </div>
  );
};
```

### 4. 框架矩阵 (FrameworkMatrix)

```tsx
import { AbsoluteFill, Sequence, interpolate, useCurrentFrame } from 'remotion';

interface MatrixCell {
  row: string;
  col: string;
  content: string;
}

interface FrameworkMatrixProps {
  rows: string[];
  cols: string[];
  cells: MatrixCell[];
}

export const FrameworkMatrix: React.FC<FrameworkMatrixProps> = ({
  rows,
  cols,
  cells,
}) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill className="flex items-center justify-center p-8">
      <div className="grid gap-2" style={{
        gridTemplateColumns: `auto repeat(${cols.length}, 1fr)`
      }}>
        {/* 表头 */}
        <div />
        {cols.map((col, i) => {
          const opacity = interpolate(frame, [i * 10, i * 10 + 10], [0, 1], {
            extrapolateRight: 'clamp',
          });
          return (
            <div
              key={i}
              className="p-3 bg-blue-500 text-white text-center font-bold rounded"
              style={{ opacity }}
            >
              {col}
            </div>
          );
        })}

        {/* 行 */}
        {rows.map((row, rowIndex) => (
          <>
            <div
              key={`row-${rowIndex}`}
              className="p-3 bg-gray-200 font-bold rounded"
              style={{
                opacity: interpolate(
                  frame,
                  [(rowIndex + 1) * 10, (rowIndex + 1) * 10 + 10],
                  [0, 1],
                  { extrapolateRight: 'clamp' }
                ),
              }}
            >
              {row}
            </div>
            {cols.map((_, colIndex) => {
              const cell = cells.find(
                (c) => c.row === row && c.col === cols[colIndex]
              );
              const cellIndex = rowIndex * cols.length + colIndex;
              return (
                <div
                  key={`cell-${rowIndex}-${colIndex}`}
                  className="p-3 bg-white border rounded text-center"
                  style={{
                    opacity: interpolate(
                      frame,
                      [cellIndex * 5 + 20, cellIndex * 5 + 30],
                      [0, 1],
                      { extrapolateRight: 'clamp' }
                    ),
                  }}
                >
                  {cell?.content || '-'}
                </div>
              );
            })}
          </>
        ))}
      </div>
    </AbsoluteFill>
  );
};
```

### 5. 人物卡片 (PersonCard)

```tsx
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

interface PersonCardProps {
  name: string;
  title: string;
  quote: string;
  imageUrl?: string;
}

export const PersonCard: React.FC<PersonCardProps> = ({
  name,
  title,
  quote,
  imageUrl,
}) => {
  const frame = useCurrentFrame();

  const slideIn = interpolate(frame, [0, 20], [-100, 0], {
    extrapolateRight: 'clamp',
  });
  const quoteOpacity = interpolate(frame, [20, 35], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill className="flex items-center justify-center p-12">
      <div
        className="flex gap-6 items-center max-w-4xl"
        style={{ transform: `translateX(${slideIn}px)` }}
      >
        {/* 头像 */}
        <div className="w-32 h-32 rounded-full bg-gray-300 overflow-hidden flex-shrink-0">
          {imageUrl && (
            <img src={imageUrl} alt={name} className="w-full h-full object-cover" />
          )}
        </div>

        {/* 信息 */}
        <div>
          <h3 className="text-2xl font-bold text-gray-800">{name}</h3>
          <p className="text-gray-500 mb-4">{title}</p>
          <blockquote
            className="text-xl text-gray-700 italic border-l-4 border-blue-500 pl-4"
            style={{ opacity: quoteOpacity }}
          >
            "{quote}"
          </blockquote>
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

---

## 动画节奏指南

| Step | 节奏 | 动画效果 | 时长分配 |
|------|------|---------|---------|
| Step 1 (场景入口) | 慢入 | 淡入 + 缩放 | 8-10秒 |
| Step 2 (原有认知) | 轻快 | 滑动出现 | 8-10秒 |
| Step 3 (认知冲突) | 突然！ | 弹出 + 震动 | 5-8秒 |
| Step 4 (新框架) | 逐步展开 | 逐个出现 | 20-25秒 |
| Step 5 (验证) | 落定 | 数字滚动 + 落定 | 10-12秒 |

---

## 质量检查清单

### HKRR 检查
- [ ] 开场钩子类型是5种之一？
- [ ] Step 2 戳中观众共鸣？
- [ ] Step 3 制造了认知冲突/悬念？
- [ ] Step 4 讲清楚了核心知识（K）？
- [ ] Step 5 回答了"所以呢"（R）？

### 拆解深度检查
- [ ] 每个知识点都有5个Step？
- [ ] Step 4（新框架）是最详细的？
- [ ] 有具体的类比让抽象概念变具体？
- [ ] 框架可以迁移到其他场景？
- [ ] 观众看完能复述这个思考框架？

### 节奏检查
- [ ] 总时长60秒分配合理？
- [ ] 每个Step约10秒？
- [ ] 没有废话/铺垫太长？

---

## 与其他规则文件的衔接

| 需求 | 引用文件 |
|------|---------|
| 文字动画 | [text-animations.md](text-animations.md) |
| 转场效果 | [transitions.md](transitions.md) |
| 时间控制 | [timing.md](timing.md) |
| 图表展示 | [charts.md](charts.md) |
| 配音生成 | [voiceover.md](voiceover.md) |
| 字幕添加 | [subtitles.md](subtitles.md) |
