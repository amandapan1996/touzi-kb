---
name: xiaohongshu-style
description: Xiaohongshu (小红书) style video design system for Remotion - warm colors, playful animations, emoji-rich UI
metadata:
  tags: xiaohongshu, style, design, theme, colors, components, chinese, social-media
---

# Xiaohongshu (小红书) Style Video Design System

A complete design system for creating Xiaohongshu-style educational videos in Remotion. This style features warm colors, playful animations, emoji-rich UI, and a casual humorous tone.

## When to use

Use this style when the user asks for:
- 小红书 (Xiaohongshu / RED) style videos
- Social media educational content for Chinese audience
- Casual, humorous tutorial videos
- Short-form explainer videos with personality

## Color Palette (NO blue/purple!)

Xiaohongshu style uses **warm, inviting colors**. **NEVER use blue or purple** as primary colors.

### 莫兰迪暖调色系 (Morandi Warm)

高级灰调暖色，温柔内敛，适合知识类/生活方式内容。

```typescript
export const COLORS = {
  // Primary - 莫兰迪暖棕
  primary: "#C9A87C",      // 核心暖棕 - 标题/重点
  primaryLight: "#D4B896", // 浅暖棕
  primaryDark: "#A68B5B",  // 深暖棕

  // Accent - 莫兰迪橙粉
  accent: "#D4A574",       // 杏仁橙 - 强调/按钮
  accentLight: "#E8C4A0",  // 奶油杏
  accentDark: "#B8956A",   // 深杏仁

  // Secondary - 莫兰迪灰粉
  secondary: "#C9B8A8",    // 暖灰米 - 次要元素
  secondaryLight: "#D9CDBF",
  secondaryDark: "#A89888",

  // Neutrals - 中性色
  dark: "#3D3D3D",         // 深炭灰 - 正文
  darkSoft: "#6B6B6B",     // 软灰 - 次要文字
  muted: "#9A9A9A",        // 浅灰 - 辅助文字
  white: "#FFFFFF",
  cream: "#FDF8F3",        // 奶油白
  warmGray: "#F5F0EB",     // 暖灰背景

  // Functional - 功能色 (保持莫兰迪调性)
  success: "#9DB5A0",      // 莫兰迪绿
  successLight: "#B8CCBA",
  warning: "#D4A574",      // 同 accent
  error: "#C9A0A0",        // 莫兰迪红
  errorLight: "#D9B8B8",

  // Backgrounds
  bgGradient1: "#FDF8F3",  // 奶油白
  bgGradient2: "#F0E6DB",  // 浅驼色
  bgGradient3: "#E8DDD0",  // 暖米色
  bgDark: "#2D2D2D",       // 深色模式背景

  // Decorative - 装饰色
  gold: "#C9A86C",         // 莫兰迪金
  rose: "#D4B8B8",         // 莫兰迪玫瑰
  sage: "#A8B5A0",         // 莫兰迪鼠尾草
  terracotta: "#C17F59",   // 陶土色
};
```

### 配色方案选择

根据内容风格选择合适的配色：

| 配色方案 | 风格特点 | 适用场景 |
|---------|---------|---------|
| **莫兰迪暖调** | 温柔内敛，高级灰调 | 知识类、生活方式、情感治愈 |
| **香槟金** | 轻奢质感，金属光泽 | 时尚、美妆、高端产品 |
| **大地陶土** | 自然质朴，有机感 | 美食、旅行、家居、手作 |
| **复古电影** | 胶片质感，故事感 | 文艺、情感故事、怀旧内容 |

---

### 香槟金色系 (Champagne Gold)

轻奢质感，适合时尚/美妆/高端产品内容。

```typescript
export const COLORS_CHAMPAGNE = {
  // Primary - 香槟金
  primary: "#C9A86C",
  primaryLight: "#DBC08A",
  primaryDark: "#A68B4C",

  // Accent - 玫瑰金
  accent: "#B76E79",
  accentLight: "#D4919A",
  accentDark: "#8B5A5A",

  // Secondary - 奶油米
  secondary: "#E8D5B5",
  secondaryLight: "#F0E4D0",
  secondaryDark: "#C9B896",

  // Neutrals
  dark: "#2C2C2C",
  darkSoft: "#5A5A5A",
  muted: "#8A8A8A",
  white: "#FFFFFF",
  cream: "#FDF8F0",
  warmGray: "#F8F2E8",

  // Functional
  success: "#8BA888",
  warning: "#C9A86C",
  error: "#C98989",

  // Backgrounds
  bgGradient1: "#FDF8F0",
  bgGradient2: "#F5EBD9",
  bgGradient3: "#E8D5B5",
  bgDark: "#1E1E1E",

  // Decorative
  gold: "#D4AF37",
  bronze: "#CD7F32",
  copper: "#B87333",
  pearl: "#F5E6D3",
};
```

---

### 大地陶土色系 (Terracotta Earth)

自然质朴，适合美食/旅行/家居/手作内容。

```typescript
export const COLORS_TERRACOTTA = {
  // Primary - 赤陶色
  primary: "#C17F59",
  primaryLight: "#D4A07A",
  primaryDark: "#A66542",

  // Accent - 橄榄绿
  accent: "#8B7355",
  accentLight: "#A69076",
  accentDark: "#6B5A44",

  // Secondary - 沙色
  secondary: "#D4C4A8",
  secondaryLight: "#E5D9C4",
  secondaryDark: "#B5A589",

  // Neutrals
  dark: "#3A3028",
  darkSoft: "#6B6055",
  muted: "#9A9085",
  white: "#FFFFFF",
  cream: "#FAF6F0",
  warmGray: "#F2EBE0",

  // Functional
  success: "#7A9A6D",
  warning: "#C17F59",
  error: "#B87070",

  // Backgrounds
  bgGradient1: "#FAF6F0",
  bgGradient2: "#EBE0D0",
  bgGradient3: "#D4C4A8",
  bgDark: "#2A2520",

  // Decorative
  rust: "#A65D3F",
  moss: "#7A8B6E",
  sand: "#D4B896",
  clay: "#B5A088",
};
```

---

### 复古电影色系 (Vintage Film)

胶片质感，适合文艺/情感故事/怀旧内容。

```typescript
export const COLORS_VINTAGE = {
  // Primary - 焦糖棕
  primary: "#B5651D",
  primaryLight: "#CD853F",
  primaryDark: "#8B4513",

  // Accent - 奶油黄
  accent: "#E6C35C",
  accentLight: "#F0D87A",
  accentDark: "#C9A83C",

  // Secondary - 深红褐
  secondary: "#8B4513",
  secondaryLight: "#A65D3F",
  secondaryDark: "#6B3410",

  // Neutrals
  dark: "#2D2620",
  darkSoft: "#5A5045",
  muted: "#8A8075",
  white: "#FFF8F0",
  cream: "#F5E6D3",
  warmGray: "#E8DED0",

  // Functional
  success: "#7A8B6E",
  warning: "#D4A03A",
  error: "#A65D5D",

  // Backgrounds
  bgGradient1: "#FFF8F0",
  bgGradient2: "#F0E0C8",
  bgGradient3: "#E6D0B0",
  bgDark: "#1E1A15",

  // Decorative
  sepia: "#A08060",
  amber: "#FFBF00",
  mahogany: "#C04000",
  honey: "#EB9605",
};
```

---

### 配色使用原则

1. **主色层次**: 用 `primary` 系列创建视觉焦点
2. **强调克制**: `accent` 只用于按钮、高亮等关键交互
3. **背景柔和**: 渐变背景用 `bgGradient1 → bgGradient2`
4. **文字层次**: `dark` → `darkSoft` → `muted` 三级灰度
5. **功能色统一**: 保持与主色调和谐

## Typography

Use Google Fonts loaded via `@remotion/google-fonts`:

```typescript
import { loadFont } from "@remotion/google-fonts/ZCOOLKuaiLe";
import { loadFont as loadNotoSans } from "@remotion/google-fonts/NotoSansSC";

// Load in Root.tsx (top level)
loadFont();      // ZCOOL KuaiLe - for titles/headings
loadNotoSans();  // Noto Sans SC - for body text

export const FONT_DISPLAY = "ZCOOL KuaiLe";  // Fun, rounded display font
export const FONT_MAIN = "Noto Sans SC";      // Clean, readable body font
```

**Font usage rules:**
- **Titles/Headings**: `ZCOOL KuaiLe` — playful, rounded, eye-catching
- **Body/Content**: `Noto Sans SC` — clean, professional, readable
- **Numbers/Data**: `ZCOOL KuaiLe` — makes numbers pop
- **Font weights**: 700-900 for titles, 400-600 for body

## Reusable Components

### AnimatedTitle
Slides up with spring animation, used for scene titles.

```tsx
export const AnimatedTitle: React.FC<{
  text: string;
  delay?: number;
  fontSize?: number;
  color?: string;
}> = ({ text, delay = 0, fontSize = 72, color = "#2D3436" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({ frame: frame - delay, fps, config: { damping: 15, stiffness: 120 } });
  const translateY = interpolate(progress, [0, 1], [60, 0]);
  const opacity = interpolate(progress, [0, 1], [0, 1]);

  return (
    <div style={{
      fontSize, fontWeight: 700, color,
      transform: `translateY(${translateY}px)`,
      opacity: Math.max(0, opacity),
      fontFamily: '"ZCOOL KuaiLe", "Noto Sans SC", sans-serif',
      textAlign: "center", lineHeight: 1.3,
    }}>
      {text}
    </div>
  );
};
```

### Card
Content card with colored left border, scales in with spring.

```tsx
export const Card: React.FC<{
  children: React.ReactNode;
  delay?: number;
  backgroundColor?: string;
  borderColor?: string;
}> = ({ children, delay = 0, backgroundColor = "#FFFFFF", borderColor = "#D4A574" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({ frame: frame - delay, fps, config: { damping: 15, stiffness: 100 } });
  const scale = interpolate(progress, [0, 1], [0.8, 1]);

  return (
    <div style={{
      backgroundColor, borderRadius: 24, padding: "40px 50px",
      borderLeft: `6px solid ${borderColor}`,
      boxShadow: "0 10px 40px rgba(0,0,0,0.08)",
      transform: `scale(${scale})`,
      opacity: Math.max(0, progress),
    }}>
      {children}
    </div>
  );
};
```

### Badge / Tag
Rounded pill badge, pops in with spring.

```tsx
export const Badge: React.FC<{
  text: string;
  color?: string;
  textColor?: string;
  delay?: number;
}> = ({ text, color = "#C9A87C", textColor = "#FFFFFF", delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({ frame: frame - delay, fps, config: { damping: 12 } });

  return (
    <div style={{
      backgroundColor: color, color: textColor,
      padding: "8px 24px", borderRadius: 50,
      fontSize: 28, fontWeight: 700,
      fontFamily: '"Noto Sans SC", sans-serif',
      transform: `scale(${progress})`,
      opacity: Math.max(0, progress),
      display: "inline-block",
    }}>
      {text}
    </div>
  );
};
```

### EmojiPop
Emoji that bounces in with rotation.

```tsx
export const EmojiPop: React.FC<{
  emoji: string;
  delay?: number;
  size?: number;
}> = ({ emoji, delay = 0, size = 80 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({ frame: frame - delay, fps, config: { damping: 8, stiffness: 200 } });
  const scale = interpolate(progress, [0, 1], [0, 1.2]);
  const rotation = interpolate(progress, [0, 1], [-20, 5]);

  return (
    <div style={{
      fontSize: size,
      transform: `scale(${scale}) rotate(${rotation}deg)`,
      opacity: Math.max(0, progress),
      display: "inline-block",
    }}>
      {emoji}
    </div>
  );
};
```

### ProgressBar
Animated progress bar that fills from left to right.

```tsx
export const ProgressBar: React.FC<{
  progress: number; // 0 to 1
  color?: string;
  height?: number;
  delay?: number;
}> = ({ progress: targetProgress, color = "#C9A87C", height = 12, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const animatedProgress = interpolate(
    frame, [delay, delay + 1 * fps], [0, targetProgress],
    { extrapolateRight: "clamp" }
  );

  return (
    <div style={{ width: "100%", height, backgroundColor: "#F5F0EB", borderRadius: height, overflow: "hidden" }}>
      <div style={{
        width: `${animatedProgress * 100}%`, height: "100%",
        backgroundColor: color, borderRadius: height,
      }} />
    </div>
  );
};
```

### NumberCounter
Counts up from 0 to target value.

```tsx
export const NumberCounter: React.FC<{
  value: number;
  suffix?: string;
  prefix?: string;
  delay?: number;
  duration?: number;
  fontSize?: number;
  color?: string;
}> = ({ value, suffix = "", prefix = "", delay = 0, duration = 1, fontSize = 80, color = "#C9A87C" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = interpolate(
    frame, [delay, delay + duration * fps], [0, value],
    { extrapolateRight: "clamp" }
  );

  return (
    <div style={{
      fontSize, fontWeight: 900, color,
      fontFamily: '"ZCOOL KuaiLe", "Noto Sans SC", sans-serif',
    }}>
      {prefix}{Math.round(progress)}{suffix}
    </div>
  );
};
```

### HighlightBox
Text with animated highlight underline.

```tsx
export const HighlightBox: React.FC<{
  children: React.ReactNode;
  delay?: number;
  highlightColor?: string;
}> = ({ children, delay = 0, highlightColor = "#E8C4A0" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({ frame: frame - delay, fps, config: { damping: 15 } });
  const width = interpolate(progress, [0, 1], [0, 100]);

  return (
    <div style={{ position: "relative", display: "inline-block" }}>
      <div style={{
        position: "absolute", bottom: 0, left: 0,
        width: `${width}%`, height: "40%",
        backgroundColor: highlightColor, opacity: 0.5, zIndex: 0,
      }} />
      <div style={{ position: "relative", zIndex: 1 }}>{children}</div>
    </div>
  );
};
```

## Scene Layout Patterns

### Pattern 1: Title + Cards (for comparisons, lists)
```
┌─────────────────────────────────┐
│         [Badge]                 │
│    Main Title (ZCOOL KuaiLe)    │
│                                 │
│  ┌──────────┐ ┌──────────┐     │
│  │  Card 1  │ │  Card 2  │     │
│  │  emoji   │ │  emoji   │     │
│  │  text    │ │  text    │     │
│  └──────────┘ └──────────┘     │
│                                 │
│      [Bottom tag / emoji]       │
└─────────────────────────────────┘
```

### Pattern 2: Title + Progress Bars (for data/stats)
```
┌─────────────────────────────────┐
│         [Badge]                 │
│    Main Title                   │
│    [Threshold bar]              │
│                                 │
│  Label1 ████████░░░ 18%        │
│  Label2 ████████████ 30%       │
│  Label3 ██████░░░░░ 14%        │
│                                 │
│      [Bottom quote]             │
└─────────────────────────────────┘
```

### Pattern 3: Title + Grid (for multiple items)
```
┌─────────────────────────────────┐
│         [Badge]                 │
│    Main Title                   │
│    [Quote / rule]               │
│                                 │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐  │
│  │ 🍎 │ │ 🛒 │ │ ⚡ │ │ 🏭 │  │
│  │AAPL│ │BABA│ │NVDA│ │TSM │  │
│  └────┘ └────┘ └────┘ └────┘  │
│                                 │
│      [Bottom text]              │
└─────────────────────────────────┘
```

### Pattern 4: Hook / Outro (full-screen centered)
```
┌─────────────────────────────────┐
│    ○ decorative circle          │
│                                 │
│         [Badge]                 │
│                                 │
│    ✨ Main Title ✨             │
│    Subtitle / tagline           │
│                                 │
│    🤯  📈  (emoji row)         │
│                                 │
│    ○ decorative circle          │
└─────────────────────────────────┘
```

## Animation Principles

1. **Stagger entrances**: Each element delays 10-15 frames after the previous
2. **Use spring animations**: `damping: 12-15` for most elements, `damping: 8` for playful emoji pops
3. **Never use CSS animations**: All animations MUST use `useCurrentFrame()` + `interpolate()` / `spring()`
4. **Subtle floating**: Decorative elements can use `Math.sin(frame / fps * 2) * 8` for gentle bobbing
5. **Scale from 0.8 to 1**: Cards and containers should scale in, not just fade

## Script Writing Style (小红书文案风格)

When writing voiceover scripts for Xiaohongshu style:

1. **Hook opening**: Start with a provocative question or surprising fact
2. **Use emojis liberally** in visual text (not in voiceover)
3. **Casual tone**: 朋友们！/ 你猜怎么着？/ 这波啊，这波叫XX！
4. **Humor**: 轻松幽默，适当用梗 (稳如老狗, 主打一个XX, 香不香)
5. **Repetition for emphasis**: 重要的事情说三遍
6. **CTA ending**: 点赞收藏，下期再见！
7. **Keep each scene under 25 seconds** for optimal engagement

## Background Gradients

根据选择的配色方案，使用对应的背景渐变：

```typescript
// 莫兰迪暖调
const morandiBackgrounds = [
  `linear-gradient(135deg, ${COLORS.bgGradient1} 0%, ${COLORS.bgGradient2} 100%)`,
  `linear-gradient(180deg, ${COLORS.cream} 0%, ${COLORS.warmGray} 100%)`,
  `linear-gradient(135deg, ${COLORS.white} 0%, ${COLORS.cream} 100%)`,
  `linear-gradient(135deg, ${COLORS.bgGradient1} 0%, ${COLORS.bgGradient3} 100%)`,
];

// 香槟金
const champagneBackgrounds = [
  `linear-gradient(135deg, ${COLORS_CHAMPAGNE.cream} 0%, ${COLORS_CHAMPAGNE.bgGradient2} 100%)`,
  `linear-gradient(180deg, ${COLORS_CHAMPAGNE.warmGray} 0%, ${COLORS_CHAMPAGNE.secondary} 100%)`,
  `linear-gradient(135deg, ${COLORS_CHAMPAGNE.white} 0%, ${COLORS_CHAMPAGNE.pearl} 100%)`,
  `linear-gradient(135deg, ${COLORS_CHAMPAGNE.cream} 0%, ${COLORS_CHAMPAGNE.secondaryLight} 100%)`,
];

// 大地陶土
const terracottaBackgrounds = [
  `linear-gradient(135deg, ${COLORS_TERRACOTTA.bgGradient1} 0%, ${COLORS_TERRACOTTA.bgGradient2} 100%)`,
  `linear-gradient(180deg, ${COLORS_TERRACOTTA.cream} 0%, ${COLORS_TERRACOTTA.warmGray} 100%)`,
  `linear-gradient(135deg, ${COLORS_TERRACOTTA.white} 0%, ${COLORS_TERRACOTTA.sand} 100%)`,
  `linear-gradient(135deg, ${COLORS_TERRACOTTA.cream} 0%, ${COLORS_TERRACOTTA.secondary} 100%)`,
];

// 复古电影
const vintageBackgrounds = [
  `linear-gradient(135deg, ${COLORS_VINTAGE.bgGradient1} 0%, ${COLORS_VINTAGE.bgGradient2} 100%)`,
  `linear-gradient(180deg, ${COLORS_VINTAGE.cream} 0%, ${COLORS_VINTAGE.warmGray} 100%)`,
  `linear-gradient(135deg, ${COLORS_VINTAGE.white} 0%, ${COLORS_VINTAGE.cream} 100%)`,
  `linear-gradient(135deg, ${COLORS_VINTAGE.bgGradient1} 0%, ${COLORS_VINTAGE.bgGradient3} 100%)`,
];
```

在不同场景间轮换渐变背景，增加视觉层次感。

## AI Image Generation (MiniMax API)

When the video needs custom illustrations or images, use MiniMax Image Generation API.

### API Endpoint

```
POST https://api.minimaxi.com/v1/image_generation
Authorization: Bearer {API_KEY}
Content-Type: application/json
```

### Text-to-Image (文生图)

Generate images from text descriptions.

```typescript
interface TextToImageRequest {
  model: "image-01" | "image-01-live";
  prompt: string;           // 图像描述，最长 1500 字符
  aspect_ratio?: "1:1" | "16:9" | "4:3" | "3:2" | "2:3" | "3:4" | "9:16" | "21:9";
  width?: number;           // 仅 image-01，范围 [512, 2048]，8 的倍数
  height?: number;          // 仅 image-01，范围 [512, 2048]，8 的倍数
  response_format?: "url" | "base64";  // 默认 url，有效期 24 小时
  n?: number;               // 生成数量 [1, 9]，默认 1
  seed?: number;            // 随机种子，用于复现结果
  prompt_optimizer?: boolean;  // 是否开启 prompt 优化，默认 false
  aigc_watermark?: boolean;    // 是否添加水印，默认 false
  style?: {                  // 仅 image-01-live 生效
    style_type: "漫画" | "元气" | "中世纪" | "水彩";
    style_weight?: number;   // (0, 1]，默认 0.8
  };
}
```

**Example:**
```typescript
const response = await fetch("https://api.minimaxi.com/v1/image_generation", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${MINIMAX_API_KEY}`,
  },
  body: JSON.stringify({
    model: "image-01",
    prompt: "A warm cozy cafe interior with soft morning light, Morandi color palette, aesthetic lifestyle photography",
    aspect_ratio: "16:9",
    n: 1,
    prompt_optimizer: true,
  }),
});

const result = await response.json();
const imageUrl = result.data.image_urls[0];
```

### Image-to-Image (图生图)

Generate images based on a reference image (e.g., character consistency).

```typescript
interface ImageToImageRequest extends TextToImageRequest {
  subject_reference?: {
    type: "character";      // 当前仅支持 character (人像)
    image_file: string;     // 公网 URL 或 Base64 Data URL
  }[];
}
```

**Example:**
```typescript
const response = await fetch("https://api.minimaxi.com/v1/image_generation", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${MINIMAX_API_KEY}`,
  },
  body: JSON.stringify({
    model: "image-01",
    prompt: "A girl looking into the distance from a library window, warm lighting",
    aspect_ratio: "16:9",
    subject_reference: [
      {
        type: "character",
        image_file: "https://example.com/reference-photo.jpg",
      },
    ],
    n: 2,
  }),
});
```

### 推荐的 Aspect Ratio 选择

| 视频场景 | Aspect Ratio | 尺寸 |
|---------|-------------|------|
| 竖版全屏 (抖音/小红书) | `9:16` | 720x1280 |
| 横版视频内嵌图片 | `16:9` | 1280x720 |
| 方形卡片/头像 | `1:1` | 1024x1024 |
| 宽幅插画 | `21:9` | 1344x576 |

### Prompt 写作建议 (小红书风格)

为保持视觉一致性，prompt 应遵循小红书美学：

```
风格关键词: warm tones, Morandi colors, soft lighting, cozy atmosphere,
           lifestyle photography, aesthetic, minimalist, clean composition

避免: blue, purple, cold tones, harsh lighting, cluttered background
```

**Example Prompts:**
```typescript
// 插画风格
"a cute illustration of a girl studying at a desk, warm Morandi colors,
soft pastel tones, minimalist style, cozy room, natural light"

// 生活方式
"aesthetic morning coffee setup on wooden table, golden hour lighting,
warm earth tones, lifestyle photography, shallow depth of field"

// 知识卡片背景
"abstract soft gradient background, warm cream and beige tones,
minimalist, clean, subtle texture, elegant"
```

### Error Codes

| Code | 含义 |
|------|------|
| 0 | 请求成功 |
| 1002 | 触发限流 |
| 1004 | 账号鉴权失败 |
| 1008 | 账号余额不足 |
| 1026 | 图片描述涉及敏感内容 |
| 2013 | 参数异常 |
| 2049 | 无效的 API Key |
