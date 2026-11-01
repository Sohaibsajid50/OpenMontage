# Persona Avatar Production — recurring AI presenter for source commentary

## When To Use

Use this skill whenever a source-commentary or presenter-led video features a
**recurring synthetic persona** (e.g. Mason Vale for ClearTake) instead of a
real presenter plate. It defines the one-time persona pack and the per-video
render flow. Read it at the `idea` stage (to lock the avatar path) and again at
`assets`, `edit` and `compose`.

Proven on 2026-09-24 (projects `mason-ai-mindblown`, `mason-robot-bolt`).

## The Flow At A Glance

```text
ONE-TIME PERSONA PACK
  headshot (identity anchor) ──► look images per setting ──► voice design (ElevenLabs) ──► saved IDs
PER VIDEO
  source research/screen/beat map ──► beat-locked script ──► per-line TTS in persona voice
  ──► place lines on timeline ──► retime SOURCE cuts to the real voice
  ──► talking_head (Kling AI Avatar v2 Pro): look image + voice track ──► avatar video
  ──► (optional) local cut-out for green-screen layout ──► compose layout ──► QA
```

## 1. One-Time Persona Pack

Store everything under the persona's branding project (Mason:
`projects/clear-take-branding/`) and record IDs in project memory.

### 1a. Identity anchor (headshot)

A clean, front-facing portrait. Every later image references it for identity.

### 1b. Look images (one per setting)

Generate with GPT Image 2.5 **Sunburst**, quality `xhigh`, via Higgsfield
`generate_image` (~2.25 credits/image; generate 2 variants and pick). Always pass
the headshot (and the previous approved look) as `image_references`.

| Setting | Aspect | Use for | Prompt essentials |
|---|---|---|---|
| **Webcam at desk** (default) | 16:9 | split-screen bottom pane, cut-out corner | webcam clipped on monitor, slightly above eye level; over-ear headphones; calm, **mouth closed**; evening room, warm lamp + monitor glow |
| POV / selfie | 9:16 | energetic phone reactions | arm-length front-camera selfie, arm/shoulder visible |
| **Green screen** | 16:9 | cut-out layouts with the cleanest key | same framing as webcam, plain evenly lit chroma-green background, no green on clothing |
| Office / studio | 16:9 | presenter-led reviews | desk, shelf, soft key light |

Realism block to append to every look prompt (this is what removed the "AI
render" look): *genuine unretouched webcam/iPhone frame; visible pores, natural
skin texture, slight shine, stray hairs; real teeth; fabric wrinkles; mild
sensor noise; no beauty filter, no smoothing, no HDR, no studio lighting; no
text, logos or watermark.*

Rules:
- Start frames for talking video: **neutral or calm expression, mouth closed**.
  A wide-open grin as frame 0 fights the lip-sync.
- Plain clothing (solid tee). Graphic tees, chains, earbuds read as "costume".
- Ordinary, lived-in rooms. Neon/RGB setups read as AI.

### 1c. Voice (ElevenLabs Voice Design)

1. `POST /v1/text-to-voice/design` with `model_id: eleven_ttv_v3`, a
   descriptive `voice_description` (age, accent, warmth, rasp, "talks like a
   friend on a call, not an announcer"), and a 100–1000 char preview line in the
   persona's real speaking style. Returns 3 previews.
2. User listens and picks one. Previews expire (~24h).
3. `POST /v1/text-to-voice` with `voice_name`, `voice_description`,
   `generated_voice_id` → permanent `voice_id`.

Mason: voice "Mason Vale", `voice_id Oy57qqMfM8XpFLTVO6aV`
(`projects/clear-take-branding/assets/voice/voice_design_auditions.json`).

## 2. Per-Video Voice Track

1. Split the approved script into its timed lines.
2. Generate **each line separately** with `elevenlabs_tts` (`model_id eleven_v3`,
   stability 0.5, similarity 0.85, style 0.35, `mp3_44100_128`).
   - `mp3_44100_192` is Creator-tier only → 403 on lower plans.
   - Spell numbers for speech ("nine point five eight"), show digits in captions.
   - Do not use "..." for pauses; use separate lines.
3. Trim leading/trailing silence, then place each line at
   `max(planned_start, previous_end + 0.25s)`; adjust starts so every line still
   lands at/after its `visual_trigger_time`.
4. Mix to one mono 48 kHz track exactly the video length. Record
   `artifacts/voice_lines.json` (id, text, start, end).
5. User listens before any avatar spend.

**Retime the source, not the voice.** Source cuts are free; voice/avatar
regenerations cost money. After real line timings exist, move/extend source
segments so each visual lands under its line.

## 3. Avatar Render (talking_head)

Default: `talking_head` with `model: kling_avatar_v2_pro` (fal, ~$0.115/s,
~15–20 min for 30s). Inputs: look image + voice track + a short `prompt`:
*regular guy at his desk wearing headphones, relaxed webcam review, natural small
head movements and nods, natural blinking, occasional glance at monitor, subtle
hand gestures, small genuine smiles on funny lines, headphones stay on, static
webcam, calm, not exaggerated.* Always pass `queue_record_path`.

Tested alternatives (same photo + audio, 2026-09-24):

| Model | Result | Use? |
|---|---|---|
| **Kling AI Avatar v2 Pro** (`kling_avatar_v2_pro`) | natural lips/teeth, head tilts, blinks, hand gestures | **Default** |
| sync-3 image-to-video (`sync_3_image`, $0.1333/s) | **bright pink/magenta lips every frame**, static head | No (re-test if sync ships a fix) |
| Seedance 2.5 via Higgsfield (native voice) | great performance, but voice changes every video; 7 credits/s | Only when no fixed voice is needed |
| sync-3 / lipsync-2 video-to-video (`lip_sync`) | re-syncs an existing moving video | Fix-up pass only |
| fal Seedance / OmniHuman (ByteDance) | likely blocked: fal Seedance rejected Mason as "real person likeness" | Avoid |

Speed: long renders are normal. If turnaround matters, split the voice into
~10s chunks and render in parallel (watch for seams).

## 4. Layouts

| Layout | Build | When |
|---|---|---|
| `source_top_avatar_bottom` | source crop 1080×960 top, avatar cover-crop 1080×960 bottom, 4px white divider | default; avatar always visible |
| `source_full_avatar_cutout` | source large (1350×1200 crop to 1080 wide) over blurred full-bleed fill; **cut-out persona bottom-left**, overlapping; captions above his head | "green-screen streamer" look |
| `source_full_avatar_overlay` | circle bubble facecam bottom-left with white ring | compact alternative |
| `voiceover_only` | no avatar | action needs the whole frame |

### Local cut-out (no model generation)

`scripts/avatar_commentary/person_mask.swift` uses Apple Vision
`VNGeneratePersonSegmentationRequest` (built into macOS, free, no download).
Extract frames at half size → run the binary → `alphamerge` masks in ffmpeg.
872 frames ≈ 47s. Clean on hair and headphones; hands at the frame edge fade.
Hosted alternatives are limited: fal BiRefNet video caps at **512 frames**.
If the user wants the cleanest key, render the avatar from the green-screen
look image instead.

## 5. Source Gotchas

- **Pre-split sources:** many viral explainers are already split (B-roll top,
  creator bottom, captions in between). Detect the split row (row-mean luminance
  jump; e.g. y=592 of 1080) and crop only the B-roll. Mark full-frame creator
  shots as unusable ranges.
- Narration-heavy sources (81+ words): mute the source entirely; the persona
  carries the explanation.
- Verify the headline claim before scripting (e.g. "robot beat Usain Bolt":
  Tiangong Ultra 8.84s at 2026 World Humanoid Robot Games). Never point at an
  unidentified robot/person and name it.
- Comments: SocialKit needs a browser User-Agent and credits; free fallback is
  yt-dlp (`source-screen-director.md`).

## 6. Cost & Time Reference (30s video)

| Step | Cost | Time |
|---|---|---|
| Look image (2 variants) | ~4.5 Higgsfield credits | ~1 min |
| Per-line TTS | cents | <1 min |
| Kling AI Avatar v2 Pro | ~$3.45 | 15–20 min |
| Local cut-out + compose | free | ~2 min |

Always announce tool, provider, model, and cost before each paid call.
