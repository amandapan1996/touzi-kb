---
name: voiceover
description: Adding AI-generated voiceover to Remotion compositions using TTS (ElevenLabs or MiniMax)
metadata:
  tags: voiceover, audio, elevenlabs, minimax, tts, speech, calculateMetadata, dynamic duration
---

# Adding AI voiceover to a Remotion composition

Use TTS (Text-to-Speech) to generate speech audio per scene, then use [`calculateMetadata`](./calculate-metadata) to dynamically size the composition to match the audio.

## Supported Providers

| Provider | Best For | Features |
|----------|----------|----------|
| **ElevenLabs** | High-quality multilingual voices | Natural prosody, voice cloning, emotion control |
| **MiniMax** | Chinese content, cost-effective | Native Chinese voices, emotion tags, speed/pitch control |

Choose the provider based on content language and requirements.

---

# ElevenLabs TTS

## Prerequisites

### ⚠️ API Key Handling (CRITICAL)

**If the user has NOT provided an ElevenLabs API key, you MUST use `ask_human` to ask for it before proceeding:**

```
ask_human(
  message="我需要 ElevenLabs API Key 来生成配音。请在下方输入你的 API Key：",
  fields=[{
    "name": "api_key",
    "label": "ElevenLabs API Key",
    "type": "text",
    "placeholder": "sk_xxxxxxxxxxxxxxxx",
    "required": True
  }]
)
```

Only proceed with voiceover generation after receiving the key. Never hardcode or guess API keys.

If the user provides the key directly in their message, use it directly without asking again.

Ensure the API key is available when running the generation script:

```bash
ELEVENLABS_API_KEY="sk_xxx" node generate-voiceover.mjs
```

## Voice Selection by Language (CRITICAL)

**You MUST select the appropriate voice based on the content language.** Different languages require different voice IDs for natural-sounding output.

### Voice ID Reference Table

| Language | Voice ID | Voice Name | Notes |
|----------|----------|------------|-------|
| **Chinese (Mandarin)** | `pNInz6obpgDQGcFmaJgB` | Guy | Natural Chinese male voice |
| **Chinese (Mandarin)** | `jBpfuIE2acO8f2sHfD7P` | Lily | Natural Chinese female voice |
| **Chinese (Mandarin)** | `iPQj9Uip4w4gNGyH9kRS` | Evelyn | Warm Chinese female voice |
| **English (US)** | `21m00Tcm4TlvDq8ikWAM` | Rachel | Professional English female |
| **English (US)** | `AZnzlk1XvdvUeBnXmlld` | Drew | Natural English male |
| **English (US)** | `pNInz6obpgDQGcFmaJgB` | Guy | Multi-purpose male |
| **English (UK)** | `jBpfuIE2acO8f2sHfD7P` | Lily | British English female |
| **Japanese** | `iPQj9Uip4w4gNGyH9kRS` | Evelyn | Japanese female |
| **Korean** | `pNInz6obpgDQGcFmaJgB` | Guy | Korean male |
| **Spanish** | `jBpfuIE2acO8f2sHfD7P` | Lily | Spanish female |
| **French** | `iPQj9Uip4w4gNGyH9kRS` | Evelyn | French female |
| **German** | `pNInz6obpgDQGcFmaJgB` | Guy | German male |

### How to Select the Right Voice

1. **Detect the language** from the user's script/content text
2. **Match the tone** — for educational/informal content (like Xiaohongshu style), prefer warmer, more expressive voices
3. **Consider gender** — if the user doesn't specify, default to male for business/finance topics, female for lifestyle/beauty
4. **Always use `eleven_multilingual_v2` model** for non-English content — it handles multilingual synthesis much better

### Voice Settings by Content Style

```javascript
// For casual/humorous content (Xiaohongshu, TikTok style)
const voiceSettings = {
  stability: 0.6,
  similarity_boost: 0.75,
  style: 0.4,  // Higher style for more expressiveness
};

// For professional/educational content
const voiceSettings = {
  stability: 0.7,
  similarity_boost: 0.8,
  style: 0.2,  // Lower style for more consistency
};

// For dramatic/storytelling content
const voiceSettings = {
  stability: 0.4,
  similarity_boost: 0.7,
  style: 0.6,  // High style for dramatic effect
};
```

## Generating audio with ElevenLabs

Create a script that reads the config, calls the ElevenLabs API for each scene, and writes MP3 files to the `public/` directory so Remotion can access them via `staticFile()`.

The core API call for a single scene:

```ts title="generate-voiceover.mjs"
import { writeFileSync, mkdirSync, existsSync } from "fs";

const API_KEY = process.env.ELEVENLABS_API_KEY;
const VOICE_ID = "pNInz6obpgDQGcFmaJgB"; // Choose based on language!
const OUTPUT_DIR = "public/voiceover/my-comp";

const scenes = [
  { id: "scene-01-intro", text: "Welcome to the show." },
  { id: "scene-02-main", text: "Let's dive into the details." },
  { id: "scene-03-outro", text: "Thanks for watching!" },
];

async function generateVoiceover() {
  if (!existsSync(OUTPUT_DIR)) mkdirSync(OUTPUT_DIR, { recursive: true });

  for (const scene of scenes) {
    const path = `${OUTPUT_DIR}/${scene.id}.mp3`;
    if (existsSync(path)) {
      console.log("Skipping (exists):", scene.id);
      continue;
    }

    console.log("Generating:", scene.id);
    const response = await fetch(
      `https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}`,
      {
        method: "POST",
        headers: {
          "xi-api-key": API_KEY,
          "Content-Type": "application/json",
          Accept: "audio/mpeg",
        },
        body: JSON.stringify({
          text: scene.text,
          model_id: "eleven_multilingual_v2",
          voice_settings: {
            stability: 0.6,
            similarity_boost: 0.75,
            style: 0.4,
          },
        }),
      }
    );

    if (!response.ok) {
      console.error(`ERROR ${response.status}: ${await response.text()}`);
      continue;
    }

    const audioBuffer = Buffer.from(await response.arrayBuffer());
    writeFileSync(path, audioBuffer);
    console.log(`  Saved: ${audioBuffer.length} bytes`);
  }
  console.log("All voiceovers generated!");
}

generateVoiceover().catch(console.error);
```

Run it:

```bash
ELEVENLABS_API_KEY="sk_xxx" node generate-voiceover.mjs
```

---

# MiniMax TTS

MiniMax offers high-quality Chinese TTS with native emotion support and competitive pricing.

## Prerequisites

### ⚠️ API Key Handling (CRITICAL)

**If the user has NOT provided a MiniMax API key, you MUST use `ask_human` to ask for it before proceeding:**

```
ask_human(
  message="我需要 MiniMax API Key 来生成配音。请在下方输入你的 API Key：",
  fields=[{
    "name": "api_key",
    "label": "MiniMax API Key",
    "type": "text",
    "placeholder": "xxxxxxxxxxxxxxxx",
    "required": True
  }]
)
```

Only proceed with voiceover generation after receiving the key. Never hardcode or guess API keys.

If the user provides the key directly in their message, use it directly without asking again.

Ensure the API key is available when running the generation script:

```bash
MINIMAX_API_KEY="xxx" node generate-voiceover-minimax.mjs
```

## Voice Selection by Language (CRITICAL)

**You MUST select the appropriate voice based on the content language.**

### Voice ID Reference Table

| Language | Voice ID | Voice Name | Notes |
|----------|----------|------------|-------|
| **Chinese (Mandarin)** | `moss_audio_ce44fc67-7ce3-11f0-8de5-96e35d26fb85` | Moss Audio | High-quality Chinese male |
| **Chinese (Mandarin)** | `moss_audio_aaa1346a-7ce7-11f0-8e61-2e6e3c7ee85d` | Moss Audio 2 | Natural Chinese voice |
| **Chinese (Mandarin)** | `Chinese (Mandarin)_Lyrical_Voice` | Lyrical Voice | Expressive Chinese female |
| **Chinese (Mandarin)** | `Chinese (Mandarin)_HK_Flight_Attendant` | HK Flight Attendant | Professional Chinese female |
| **English (US)** | `English_Graceful_Lady` | Graceful Lady | Professional English female |
| **English (US)** | `English_Insightful_Speaker` | Insightful Speaker | Natural English male |
| **English (US)** | `English_radiant_girl` | Radiant Girl | Young English female |
| **English (US)** | `English_Lucky_Robot` | Lucky Robot | AI/robotic style |
| **Japanese** | `Japanese_Whisper_Belle` | Whisper Belle | Japanese female |
| **Japanese** | `moss_audio_24875c4a-7be4-11f0-9359-4e72c55db738` | Moss JP | Natural Japanese |

### Emotion Control (speech-2.8-hd/turbo only)

MiniMax supports emotion tags in text for `speech-2.8-hd` and `speech-2.8-turbo` models:

| Tag | Effect |
|-----|--------|
| `(laughs)` | 笑声 |
| `(chuckle)` | 轻笑 |
| `(coughs)` | 咳嗽 |
| `(sighs)` | 叹气 |
| `(breath)` | 正常换气 |
| `(gasps)` | 倒吸气 |
| `(emm)` | 嗯 |
| `(sneezes)` | 喷嚏 |

Example usage: `"今天是不是很开心呀(laughs)，当然了！"`

### Audio Settings

```javascript
const audioSettings = {
  sample_rate: 32000,    // 8000, 16000, 22050, 24000, 32000, 44100
  bitrate: 128000,       // 32000, 64000, 128000, 256000 (mp3 only)
  format: "mp3",         // mp3, pcm, flac, wav (wav non-streaming only)
  channel: 1,            // 1=mono, 2=stereo
};
```

### Voice Settings by Content Style

```javascript
// For casual/humorous content (Xiaohongshu, TikTok style)
const voiceSettings = {
  speed: 1.0,           // Range: 0.5-2.0
  vol: 1.0,             // Range: 0-10
  pitch: 0,             // Range: -12 to 12
  emotion: "happy",     // happy, sad, angry, fearful, disgusted, surprised, calm, fluent
};

// For professional/educational content
const voiceSettings = {
  speed: 0.9,
  vol: 1.0,
  pitch: 0,
  emotion: "calm",
};

// For dramatic/storytelling content
const voiceSettings = {
  speed: 1.1,
  vol: 1.2,
  pitch: 2,
  emotion: "fluent",
};
```

## Generating audio with MiniMax

Create a script that reads the config, calls the MiniMax API for each scene, and writes audio files to the `public/` directory.

```ts title="generate-voiceover-minimax.mjs"
import { writeFileSync, mkdirSync, existsSync } from "fs";

const API_KEY = process.env.MINIMAX_API_KEY;
const OUTPUT_DIR = "public/voiceover/my-comp";

const scenes = [
  { id: "scene-01-intro", text: "欢迎来到今天的节目。" },
  { id: "scene-02-main", text: "让我们深入了解一下细节。" },
  { id: "scene-03-outro", text: "感谢观看！" },
];

async function generateVoiceover() {
  if (!existsSync(OUTPUT_DIR)) mkdirSync(OUTPUT_DIR, { recursive: true });

  for (const scene of scenes) {
    const path = `${OUTPUT_DIR}/${scene.id}.mp3`;
    if (existsSync(path)) {
      console.log("Skipping (exists):", scene.id);
      continue;
    }

    console.log("Generating:", scene.id);
    const response = await fetch(
      "https://api.minimaxi.com/v1/t2a_v2",
      {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${API_KEY}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: "speech-2.8-hd",
          text: scene.text,
          stream: false,
          voice_setting: {
            voice_id: "moss_audio_ce44fc67-7ce3-11f0-8de5-96e35d26fb85",
            speed: 1.0,
            vol: 1.0,
            pitch: 0,
            emotion: "calm",
          },
          audio_setting: {
            sample_rate: 32000,
            bitrate: 128000,
            format: "mp3",
            channel: 1,
          },
          subtitle_enable: false,
        }),
      }
    );

    if (!response.ok) {
      console.error(`ERROR ${response.status}: ${await response.text()}`);
      continue;
    }

    const result = await response.json();

    if (result.base_resp?.status_code !== 0) {
      console.error(`API ERROR: ${result.base_resp?.status_msg}`);
      continue;
    }

    // Audio is returned as hex-encoded string
    const audioBuffer = Buffer.from(result.data.audio, "hex");
    writeFileSync(path, audioBuffer);
    console.log(`  Saved: ${audioBuffer.length} bytes`);
    console.log(`  Duration: ${result.extra_info?.audio_length}ms`);
  }
  console.log("All voiceovers generated!");
}

generateVoiceover().catch(console.error);
```

Run it:

```bash
MINIMAX_API_KEY="xxx" node generate-voiceover-minimax.mjs
```

### Streaming Mode (for long text)

For texts longer than 3000 characters, use streaming mode:

```javascript
const response = await fetch(
  "https://api.minimaxi.com/v1/t2a_v2",
  {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "speech-2.8-hd",
      text: longText,
      stream: true,  // Enable streaming
      voice_setting: { /* ... */ },
      audio_setting: { /* ... */ },
    }),
  }
);

// Handle streaming response
const reader = response.body.getReader();
let chunks = [];

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  chunks.push(value);
}

// Combine chunks and parse
```

### Custom Pause Control

Use `<#x#>` tags to add custom pauses (x = seconds, range: 0.01-99.99):

```javascript
const text = "大家好<#0.5#>欢迎来到今天的节目<#1#>让我们开始吧";
```

---

## Getting accurate audio durations with ffprobe

After generating audio files, use `ffprobe` to get precise durations for the composition:

```bash
for f in public/voiceover/my-comp/*.mp3; do
  dur=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$f")
  echo "$(basename $f): ${dur}s"
done
```

Use these durations in `Root.tsx` to set `sceneDurations` and `durationInFrames`.

## Dynamic composition duration with calculateMetadata

Use [`calculateMetadata`](./calculate-metadata.md) to measure the [audio durations](./get-audio-duration.md) and set the composition length accordingly.

```tsx
import { CalculateMetadataFunction, staticFile } from "remotion";
import { getAudioDuration } from "./get-audio-duration";

const FPS = 30;

const SCENE_AUDIO_FILES = [
  "voiceover/my-comp/scene-01-intro.mp3",
  "voiceover/my-comp/scene-02-main.mp3",
  "voiceover/my-comp/scene-03-outro.mp3",
];

export const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  const durations = await Promise.all(
    SCENE_AUDIO_FILES.map((file) => getAudioDuration(staticFile(file))),
  );

  const sceneDurations = durations.map((durationInSeconds) => {
    return durationInSeconds * FPS;
  });

  return {
    durationInFrames: Math.ceil(sceneDurations.reduce((sum, d) => sum + d, 0)),
  };
};
```

The computed `sceneDurations` are passed into the component via a `voiceover` prop so the component knows how long each scene should be.

If the composition uses [`<TransitionSeries>`](./transitions.md), subtract the overlap from total duration: [./transitions.md#calculating-total-composition-duration](./transitions.md#calculating-total-composition-duration)

## Rendering audio in the component

See [audio.md](./audio.md) for more information on how to render audio in the component.

## Delaying audio start

See [audio.md#delaying](./audio.md#delaying) for more information on how to delay the audio start.
