# Asset Director - Avatar Spokesperson Pipeline

## When To Use

This stage prepares the actual spokesperson ingredients: narration, avatar or lip-sync footage, subtitle assets, branded backgrounds, and the minimal support graphics needed to complete the cut.

In `source_commentary` mode, this stage also measures narration against the
source video duration, fits the audio, generates subtitle/caption assets, and
only then creates the avatar performance from the final fitted narration.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["scene_plan"]["scene_plan"]`, `state.artifacts["script"]["script"]`, `state.artifacts["idea"]["brief"]` | Presenter plan and narration needs |
| Tools | `talking_head`, `lip_sync`, `tts_selector`, `subtitle_gen`, `image_selector`, `audio_enhance` — selectors auto-discover all available providers from the registry | Avatar, narration, and support asset options |
| Playbook | Active style playbook | Background, type, and subtitle rules |

## Process

### 1. Lock The Avatar Generation Path

Use one primary path and record it clearly:

- `talking_head` from still image plus audio,
- `lip_sync` from existing presenter plate plus new audio,
- externally supplied avatar render if created outside the current runtime.

Do not hide a blocked avatar path. Record it.

**Recurring persona (e.g. Mason Vale):** follow
`skills/pipelines/avatar-spokesperson/persona-avatar-production.md`. Default path:
per-line ElevenLabs TTS in the persona's saved voice → timeline placement →
`talking_head` with `model: kling_avatar_v2_pro` (hosted on fal; needs only
`FAL_KEY`) using the persona's look image for the chosen layout. Both
`talking_head` and `lip_sync` now have hosted fal backends, so "no GPU" no
longer forces the no-avatar pivot. Always set `queue_record_path` on paid calls.

### 1b. Sample Preview (Prevents Wasted Spend)

Before batch-generating assets, produce one sample of each expensive type and show the user:

1. **TTS sample** (if generating narration): Generate one section. Confirm voice, pace, and persona before batching the rest.
2. **Avatar sample** (if using `talking_head`): Generate a short test clip. Confirm the avatar quality is acceptable before committing to full generation.

If rejected, adjust parameters and retry (max 3 iterations). Do not batch until approved.

### 2. Resolve Narration Before Support Graphics

Spokesperson videos depend on speech. Determine whether narration is:

- supplied,
- TTS-generated,
- already embedded in a presenter plate.

If narration is missing and no TTS tool is available, mark the project blocked instead of pretending the stage succeeded.

### 2b. Fit Narration To Source Timing

For source-commentary work, generate the strongest approved narration first,
then measure its actual duration before rendering the avatar.

Compute:

```text
speed_factor = narration_duration / target_video_duration
```

Use this policy:

| Speed Factor | Action |
| --- | --- |
| 0.95-1.10 | Fit directly with small trim, silence, or speed change |
| 1.10-1.25 | Usually acceptable for high-energy shorts if speech remains clear |
| 1.25-1.35 | Review manually; often rewrite or split into segments |
| >1.35 | Rewrite before forcing audio |
| <0.90 | Add copy, pauses, or original sound moments |

For larger-scale narration, a controlled speed-up is acceptable when it improves
energy and still matches the beat map. But global speed-up cannot fix a line
attached to the wrong frame. If a visual object appears at 36 seconds, the line
that names it must still land at or after that visual trigger after fitting.

Preferred order:

1. final beat-locked script,
2. TTS narration,
3. duration measurement,
4. speed/segment fit,
5. subtitle/caption timing,
6. avatar render from the final narration audio.

Prefer **per-line TTS** over one long take: generate each script line
separately, trim silence, and place each at `max(planned_start,
previous_end + 0.25s)`. Record `artifacts/voice_lines.json`. When lines run
long, **retime the source segments** (free) instead of speeding up the voice
or regenerating the avatar (paid).

### 3. Build The Minimal Support Kit

Prepare only what the scene plan actually needs:

- subtitle files,
- burned-in caption image or subtitle assets for platforms that need hard captions,
- one lower-third system,
- CTA card,
- background or plate assets,
- optional still or product support images.

### 4. Use Metadata For Capability Truth

Recommended metadata keys:

- `avatar_generation_path`
- `narration_assets`
- `narration_fit_report`
- `subtitle_assets`
- `caption_style`
- `caption_safe_zone_notes`
- `background_assets`
- `scene_asset_index`
- `blocked_assets`

### 5. Quality Gate

- the avatar path is explicit,
- narration and avatar assets align,
- support graphics stay minimal,
- every referenced file exists.
- source-commentary mode records target duration, narration duration,
  speed_factor, fit method, and subtitle/caption source.

## No-Avatar Path

When the EP has triggered a narration-over-graphics pivot (neither `talking_head` nor `lip_sync` available), skip avatar generation entirely and produce a graphics-driven asset kit instead:

### What to produce:
1. **Narration audio** — via `tts_selector` (mandatory; block the project if no TTS is available either).
2. **Scene visuals** — via `image_selector` or `video_selector`. One primary visual per scene that reinforces the spoken point (diagram, illustration, product shot, or stock footage).
3. **Subtitle files** — same as standard path.
4. **Text cards** — key-point overlays, stat cards, CTA end card.
5. **Backgrounds** — consistent family matching the playbook.

### What to skip:
- No `talking_head` or `lip_sync` calls.
- No presenter framing metadata.
- `avatar_generation_path` should be set to `"none — narration-over-graphics pivot"`.

### Metadata for this path:
- `avatar_generation_path`: `"narration_over_graphics"`
- `pivot_reason`: why the no-avatar path was chosen
- All other metadata keys remain the same.

### Mid-Production Fact Verification

If you encounter uncertainty during asset generation:
- Use `web_search` to verify visual accuracy of subjects (e.g. what does this building actually look like?)
- Use `web_search` to find reference images before generating illustrations
- Log verification in the decision log: `category="visual_accuracy_check"`

Visual accuracy matters. If the script mentions a specific place, person, or object,
verify what it actually looks like before generating images. Don't rely on
the AI model's training data — it may be wrong or outdated.

## Common Pitfalls

- Building decorative assets before the narration path is solved.
- Mixing multiple avatar-generation strategies in one simple spokesperson video.
- Marking the stage complete when the core presenter asset is still hypothetical.
- (No-avatar path) Generating filler visuals with no connection to the narration — every image must reinforce the spoken point.


## When You Do Not Know How

If you encounter a generation technique, provider behavior, or prompting pattern you are unsure about:

1. **Search the web** for current best practices — models and APIs change frequently, and the agent's training data may be stale
2. **Check `.agents/skills/`** for existing Layer 3 knowledge (provider-specific prompting guides, API patterns)
3. **If neither helps**, write a project-scoped skill at `projects/<project-name>/skills/<name>.md` documenting what you learned
4. **Reference source URLs** in the skill so the knowledge is traceable
5. **Log it** in the decision log: `category: "capability_extension"`, `subject: "learned technique: <name>"`

This is especially important for:
- **Video generation prompting** — models respond to specific vocabularies that change with each version
- **Image model parameters** — optimal settings for FLUX, GPT Image, Imagen differ and evolve
- **Audio provider quirks** — voice cloning, music generation, and TTS each have model-specific best practices
- **Remotion component patterns** — new composition techniques emerge as the framework evolves

Do not rely on stale knowledge. When in doubt, search first.

---

## Gate Reminder (Binding)

This stage gates on human approval (`human_approval_default: true`). After review passes:
checkpoint with `status="awaiting_human"`, present the summary (the Backlot board renders
the artifact), and **END YOUR TURN**. Do not start the next stage in the same response.
Approval is per-gate — an earlier "go ahead" does not cover this gate.

## HeyGen Avatar V

Use `heygen_avatar` for explicitly approved HeyGen digital twins. Inspect the look before rendering: Avatar V requires `digital_twin` and `avatar_v` in `supported_api_engines`. Pass script plus voice_id, or one supplied audio source. Keep the returned resume_job/job_path if polling times out; resume the job instead of submitting again. An ineligible look is a blocker, never permission to switch to Avatar IV. Read the provider-model-refresh skill.
