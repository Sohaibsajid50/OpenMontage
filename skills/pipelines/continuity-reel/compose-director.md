# Compose Director — Continuity Reel Pipeline

## When to Use

You assemble the final reel from the generated assets: the image-to-video clips,
the continuous narration, the background music, and word-by-word captions. This
stage is where most "it feels broken" problems are made or fixed. The rules below
are hard-won — follow them exactly.

Read [Audio Direction](audio-direction.md) before making voice, music, or timing decisions.

Read [Visual Production and Review](visual-production-review.md) for reference mapping,
failed-take review, and evidence required before batching.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | Output artifact |
| Prior | `asset_manifest`, `edit_decisions`, `script`, `visual_memory` | Clips, narration, music, timing |
| Tools | `video_compose`, `audio_mixer`, ffmpeg | Render |

## The Assembly Contract (do all of these)

### 1. ONE continuous narration drives everything
The narration is a single ElevenLabs take (not per-line). Its word-timestamps
define **scene windows** and **caption timing**. One master audio track carries
flow across every cut. Never stitch per-line audio clips — that produces the
disjointed "cold start" sound.

### 2. Scene windows = beat start → next beat start
Each beat's on-screen time = its first word's timestamp → the next beat's first
word timestamp (last beat → narration end + small tail). The clip for that beat
fills exactly that window.

### 3. Motion-fill by STRETCH, never freeze
If a beat's narration window is **longer** than its 5s clip, **slow the clip**
(`setpts={window/clip}*PTS`, then resample to fps) so motion continues for the
whole window. **Never** `tpad`/freeze-frame the last frame — a frozen frame while
the voice keeps talking reads as the video "pausing/breaking" (a real bug we hit).
If the window is shorter than the clip, trim.

`setpts` takes a **duration multiplier**, not playback speed: use
`window_seconds / source_seconds`, applied to `(PTS-STARTPTS)`, then resample
to the output frame rate. A 5-second clip filling 7 seconds needs `setpts=1.4*(PTS-STARTPTS)`.
Using `5/7` here speeds up the clip and leaves the timeline short.

Probe each rendered clip's **video stream duration** before assembling it. Reject
clips more than two output frames away from their intended window. After each
transition, verify the cumulative picture duration before scheduling the next
transition; never place an xfade beyond the end of the available picture track.

### 4. Caption phrases follow the approved edit plan
Captions show a **short phrase at a time** and swap as the speaker advances —
never the whole sentence stacked into 2-3 lines covering the screen.
- Use the edit plan's word/line limits and safe-area position. For reference-free
  work, default to **≤3 words / ≤16 characters**, one line. Reference-driven work
  may specify longer phrases or two short lines; check them against the actual frame.
- Show each chunk from its first word's start until the next chunk's start
  (last chunk holds to beat end).
- Render via **image (PNG) overlays** composited with ffmpeg `overlay` +
  `enable='between(t,start,end)'`. Do NOT rely on ffmpeg `drawtext` — many builds
  (e.g. Homebrew) ship without it. Use a bold font, white text + dark shadow, a
  translucent band, positioned in the lower third (around y≈H-240).
- Try to keep multi-word numbers/units intact when chunking (e.g. "120 KG"
  together rather than splitting awkwardly).

### 5. Breaths must be carried by the screen
Do not apply one universal inter-beat pause. A short breath often keeps a
spectacle montage moving; an impossible-tableau hook may hold longer while the
behavior remains active and legible. Any narration gap must be carried by
meaningful motion, music, captions, or the payoff itself. A silent held frame is
still a failure.

### 6. Execute the selected hook grammar
Read `edit_decisions.hook_treatment` before assembling the opening:
- `spectacle_montage`: use impact-motivated cuts between distinct phases of the
  behavior. Do not cut merely to reset attention.
- `impossible_tableau`: preserve the coherent proof shot long enough to read.
  A dissolve or cut is allowed only when the causal beat changes.

After the hook, choose hard cuts, dissolves, or another restrained transition by
editorial intent. When using `xfade`, pad segments so the dissolve does not steal
screen time and round offsets to 3 decimals.

### 7. Background music + ambience, immediately intentional
Mix the music bed (`assets/music/background.mp3`) UNDER the narration:
- Follow `audio-direction.md`: measure both sources, normalize narration when needed,
  then choose music gain and ducking for audible emotion and clear speech. Fixed
  percentages are not a quality target. Execute `edit_decisions.metadata.audio_mix`.
- The opening must have useful audio energy from frame one unless
  `hook_treatment.music_entry` explicitly selects designed silence. A long
  automatic fade-in is not a default.
- Fade music out near the end when that supports the landing.
- Call the music **ducked** only when a real sidechain or volume-envelope process
  reduces it in response to narration. A fixed low music level is a fixed mix,
  not ducking.
- Add a subtle ambience/noise-floor layer when natural narration breaths produce dead
  air or when the environment should feel alive. Examples: underwater rumble, cave air,
  wind tone, room tone.
- If ambience is generated in ffmpeg (`anoisesrc`, filtered noise, etc.), keep it very
  low and shape it with highpass/lowpass filters so it feels environmental, not like hiss.
- When using `amix`, beware normalization lowering all inputs. If you add a quiet
  ambience layer, use `normalize=0` and a limiter when needed so the noise floor remains
  present without clipping.

The narration must always sit clearly on top. Ambience is a floor, not a featured sound.

### 8. Output & verify
Render H.264 yuv420p + AAC, 9:16, the project's resolution. Then verify:
- `ffprobe` confirms the file exists and duration ≈ narration length.
- Probe video and audio stream durations separately. Both must cover the intended
  timeline within two output frames (allow documented audio encoder padding).
  Container duration alone is insufficient: the August 2026 octopus render had
  45.09 seconds of audio but only 21.93 seconds of video.
- Decode frames near the actual ending as well as the opening and hero beat.
  A failed late-frame extraction is a failed render check, not a reason to sample
  only earlier frames. Do not count a player holding its last frame as coverage.
- Use `silencedetect` to flag unexplained gaps over ~0.7s; record designed silence.
  A non-silent waveform does not prove a good mix.
- Review the actual mix for narrator fit, intelligibility, musical energy, pumping,
  and loop joins. Record measured levels separately from listening observations;
  if listening is unavailable, mark it unassessed instead of claiming a pass.
- Spot-check a long-beat timestamp shows moving frames (proves no freeze).
- Captions follow the approved line count, stay inside safe areas, and remain legible.
Write schema-valid `render_report` and `final_review` artifacts. Link the reviewed
output and preserve its version. Record user feedback with reviewer and scope;
a preferred mix is not evidence of audience retention or publication readiness.

## Common Pitfalls (all observed in real builds)

- **Freeze-frame fill** → looks like the video paused. Stretch instead.
- **Cumulative captions** → text covers half the screen. Use approved phrase limits.
- **Per-line TTS** → disjointed narration. One continuous take.
- **Uncarried inter-beat pauses** → "in steps" feel. Let active motion, sound, or
  payoff justify every longer gap.
- **One transition grammar for every hook** → montage and tableau hooks lose the
  property that made them work.
- **No opening audio energy / music too loud** → the hook feels inert, or the bed
  fights the voice.
- **Calling a fixed-volume mix ducking** → the artifact no longer describes the
  render truthfully.
- **No ambience through natural breaths** → the reel feels empty even with visuals. Add a
  subtle environmental floor and verify with `silencedetect`.
- **`amix` normalizes ambience away** → use `normalize=0` plus a limiter when mixing
  narration, music, and ambience.
- **Trimming clips to narration length** → throws away motion, feels cut short.
- **Relying on ffmpeg drawtext** → fails on builds without it. Use PNG overlays.

## Current engine runtime contract

Preserve the proposal’s approved `render_runtime`, `renderer_family`, and `composition_mode` in edit decisions. Validate against this checkout’s schemas and use its current tool registry and checkpoint APIs. Do not assume older examples override current required fields.
