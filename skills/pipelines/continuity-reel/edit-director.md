# Edit Director — Continuity Reel Pipeline

## When to Use

You decide the timing and edit structure of the reel before the compose stage
renders it. You turn the continuous narration + the per-beat clips into a precise
edit decision list: which clip plays when, how long, how it's fitted, and how
captions are chunked. You make decisions; the compose-director executes the render.

Read [Audio Direction](audio-direction.md) before making voice, music, or timing decisions.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/edit_decisions.schema.json` | Output artifact |
| Prior | `script`, `asset_manifest`, `visual_memory` | Beats, clips, narration timing |

## Process

### 1. Derive scene windows from the narration word-timestamps
The narration is one continuous take with per-word timestamps. For each beat:
- `window_start` = first word's timestamp.
- `window_end` = next beat's first word timestamp (last beat → narration end + ~0.6s tail).
- `window_dur` = window_end − window_start.
Map each window to its beat's clip (`scene-NN.mp4`).
For a replacement voice, invalidate previous timestamps and recalculate every window
and caption. Align the new take against the unchanged script; document transcript
corrections without inventing timings. Preserve prior versions before updating artifacts.

### 2. Decide the clip fit per beat
- `window_dur <= clip_len` → **trim** the clip to the window.
- `window_dur > clip_len` → **stretch** (slow) the clip to fill the window. Flag
  `fit: "stretch"` with `speed_factor = clip_len/window_dur`. NEVER freeze-frame.
Record the chosen `fit` per beat so compose renders it correctly.

### 3. Specify caption chunks
For each beat, choose readable phrase chunks from the approved reference or
hook treatment. Record maximum words, lines, font size, and safe-area position in
the edit metadata. For reference-free work, start with rolling single-line chunks:
- **≤3 words and ≤16 characters** per chunk.
- Keep numbers + units together where possible ("120 KG", not "120" / "KG").
- Each chunk: `text`, `start` (its first word's timestamp), `end` (next chunk's
  start, or beat end for the last).
These are replacement phrases, not a cumulative sentence. A reference may use
longer phrases or two short lines; preserve that grammar when legible without
covering the behavior. Do not force every reel into the same three-word template.

Select caption behavior from the hook mode:
- `spectacle_montage` may use selective 1–2-word kinetic emphasis on high-value
  claim or consequence words.
- `impossible_tableau` should prefer restrained phrase captions that leave the
  behavior unobstructed.

Do not animate every word. Record the chosen `caption_mode` and any
`hook_keywords` in the subtitle plan.

### 4. Set transitions and pacing
- Execute the selected hook mode instead of one universal transition recipe.
  `spectacle_montage` normally uses clean impact cuts; `impossible_tableau` may
  hold one coherent proof shot. Do not dissolve an impact or cut merely to reset
  attention.
- After the hook, use hard cuts for causal/energy changes and short dissolves
  (~0.2–0.3s) only for a motivated continuity or mood transition. Pad dissolves
  so the net timeline still equals the sum of windows.
- Assess breaths against the intended performance, without a fixed pause duration. If the narration
  has long pauses caused by bad TTS pacing, send back to the asset stage to regenerate.
  If the pauses are natural performance breaths, plan a subtle ambience/noise-floor
  layer so the reel does not feel empty.

### 4b. Plan the audio bed, not just music

Edit decisions should specify:
- narration at full clarity,
- music bed under the voice with useful energy from frame one,
- synchronized SFX when visible impact or transformation requires it,
- optional ambience/noise floor for the environment,
- source levels, normalization, gain, ducking parameters, fades, and loop joins
  under `metadata.audio_mix`,
- listening criteria for speech clarity and musical emotion, with silence detection
  used to flag unexplained gaps rather than prove engagement.

Emit an explicit `hook_treatment` with `mode`, proof timing, narration-entry mode,
caption mode, transition strategy, music attack, and SFX plan. A visual cold open,
rapid cuts, kinetic captions, and narration pauses are choices—not defaults.

If music stays at a fixed low volume, describe it as fixed-volume. Set `ducking`
only when the compose path applies voice-responsive gain reduction.

Ambience is not a replacement for music. It is a quiet environmental layer that keeps
energy through narration breaths: underwater rumble, wind tone, room tone, cave air,
city bed, etc. If it is generated or sourced as an asset, reference it in
`audio.sfx`; if compose will synthesize it locally, note that in `metadata`.

### 5. Emit edit_decisions
Produce a schema-valid `edit_decisions` artifact: ordered beats with clip path,
window times, `fit` (trim/stretch + factor), caption chunks, and transition spec.
Also note the music track, ambience strategy, and whether actual ducking is planned
(compose executes the documented mix).

## Common Pitfalls

- **Freeze to fill** — never. Stretch long beats.
- **Cumulative captions** — use replacement phrases within the approved line limit.
- **Ignoring dead air** — fix bad narration pacing at the source; use subtle ambience
  for natural performance breaths.
- **Window math off by the crossfade** — pad segments so dissolves don't shorten beats.
- **One edit grammar for every hook** — select montage or tableau from the actual proof.
- **False ducking metadata** — fixed music volume is not voice-responsive ducking.

## Current engine runtime contract

Preserve the proposal’s approved `render_runtime`, `renderer_family`, and `composition_mode` in edit decisions. Validate against this checkout’s schemas and use its current tool registry and checkpoint APIs. Do not assume older examples override current required fields.
