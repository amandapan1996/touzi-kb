---
name: fast-render
description: Fast Remotion rendering using Node.js API with @remotion/bundler and @remotion/renderer, more reliable than CLI
metadata:
  tags: remotion, render, bundler, renderer, performance, production
---

# Fast Remotion Rendering via Node.js API

## When to use

Use this method instead of `npx remotion render` CLI when rendering Remotion videos. The Node.js API approach is **faster** and **more reliable** than the CLI, avoiding common issues like "peer closed connection" errors.

## The Render Script

Save this as `render.mjs` in your project root:

```javascript
import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";
import path from "path";

const COMPOSITION_ID = "PutStrategy"; // Change to your composition ID
const ENTRY_POINT = "./src/index.ts";
const OUTPUT = "out/video.mp4";

async function main() {
  console.log("⏳ Bundling...");
  const bundleLocation = await bundle({
    entryPoint: path.resolve(ENTRY_POINT),
  });
  console.log("✅ Bundle at:", bundleLocation);

  console.log("⏳ Getting composition...");
  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: COMPOSITION_ID,
  });
  console.log(
    "📐 Composition:",
    JSON.stringify({
      id: composition.id,
      duration: composition.durationInFrames,
      fps: composition.fps,
      width: composition.width,
      height: composition.height,
    })
  );

  console.log("🎬 Rendering...");
  await renderMedia({
    composition,
    serveUrl: bundleLocation,
    codec: "h264",
    outputLocation: OUTPUT,
    crf: 23,
    onProgress: ({ renderedFrames }) => {
      if (renderedFrames % 100 === 0) {
        console.log(`  Rendered ${renderedFrames} frames...`);
      }
    },
  });
  console.log("✅ Done!", OUTPUT);
}

main().catch((e) => {
  console.error("❌ Fatal error:", e.message);
  process.exit(1);
});
```

## Usage

```bash
node render.mjs
```

## Inline One-Liner (for quick renders)

```bash
node -e "
const {bundle} = require('@remotion/bundler');
const {renderMedia, selectComposition} = require('@remotion/renderer');
const path = require('path');
async function main() {
  console.log('Bundling...');
  const bundleLocation = await bundle({ entryPoint: path.resolve('./src/index.ts') });
  console.log('Bundle at:', bundleLocation);
  const composition = await selectComposition({ serveUrl: bundleLocation, id: 'PutStrategy' });
  console.log('Composition:', JSON.stringify({id: composition.id, duration: composition.durationInFrames, fps: composition.fps, width: composition.width, height: composition.height}));
  console.log('Rendering...');
  await renderMedia({ composition, serveUrl: bundleLocation, codec: 'h264', outputLocation: 'out/put-strategy.mp4', crf: 23, onProgress: ({renderedFrames}) => { if (renderedFrames % 100 === 0) console.log('Rendered', renderedFrames); } });
  console.log('Done!');
}
main().catch(e => { console.error('Fatal error:', e.message); process.exit(1); });
"
```

## Why this is better than `npx remotion render`

| Issue | CLI (`npx remotion render`) | Node.js API |
|-------|---------------------------|-------------|
| "peer closed connection" errors | ❌ Frequent | ✅ Rare |
| Render speed | 🐌 Slower | 🚀 Faster |
| Progress tracking | Basic | Customizable |
| Error handling | Limited | Full try/catch |
| Concurrency control | CLI flag | Programmatic |

## Key Options

- `codec`: `"h264"` (most compatible), `"h265"`, `"vp8"`, `"vp9"`, `"prores"`
- `crf`: Lower = better quality (18=high, 23=medium, 28=low)
- `outputLocation`: Output file path
- `onProgress`: Callback for progress tracking

## Prerequisites

```bash
npm install @remotion/bundler @remotion/renderer
```
