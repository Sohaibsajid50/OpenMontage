# Script Director - Avatar Spokesperson Pipeline

## When To Use

Turn the approved brief into scene-safe spoken copy for an avatar presenter. The quality bar is not literary flourish. It is spoken clarity, believable pacing, and one clean point per scene.

In `source_commentary` mode, this stage writes beat-locked commentary over
source footage. The script must follow the frame evidence and beat map, not just
the general story of the clip.

## Reference Inputs

- `docs/avatar-spokesperson-best-practices.md`
- `skills/creative/storytelling.md`
- `skills/creative/hook-engine.md`

## Process

### 1. Write For Speech, Not For Slides

Prefer:

- short sentences,
- direct verbs,
- one idea per beat,
- explicit transitions,
- conversational emphasis.

If the copy sounds like a brochure when read aloud, rewrite it.

### 2. Break Into Scene-Safe Chunks

Avatar scenes are easier to manage when each section is compact. A useful starting point is:

- hook,
- value statement,
- proof or feature beat,
- CTA.

### 3. Keep On-Screen Text Light

The presenter is already carrying attention. Use on-screen text only for:

- product names,
- short proof points,
- CTA copy,
- legal or compliance text that must appear.

### 4. Use Metadata For Delivery Notes

Recommended metadata keys:

- `scene_copy_map`
- `cta_language`
- `pronunciation_notes`
- `supplied_script_source`
- `legal_text_requirements`

### 5. Quality Gate

- the copy sounds spoken,
- scene lengths are realistic,
- CTA placement is clear,
- text overlays are restrained.

## Hook Lab

Before writing the full script, generate a hook lab. Do this for every
source-commentary script and for any short-form spokesperson video where the
first three seconds matter.

Do not default to "Stop scrolling." Treat it as a rejected generic opener unless
there is a specific reason it fits the source better than the alternatives.

### Required Hook Process

1. Read `skills/creative/hook-engine.md`.
2. Build a hook evidence packet from:
   - first frame,
   - first motion,
   - visual beat map,
   - final payoff,
   - transcript conflict,
   - 50-100 comment themes,
   - visible object/action that creates curiosity.
3. Generate at least 12 hook options across different hook families.
4. Include the required mix from the hook engine:
   - at least 3 comment-intelligence hooks,
   - at least 3 first-frame or first-motion hooks,
   - at least 2 payoff/open-loop hooks,
   - at least 2 conflict, suspicion, or challenge hooks,
   - at least 2 curiosity-gap hooks.
5. Score each hook with the hook-engine weighted rubric:
   - first-frame fit,
   - specificity,
   - curiosity gap,
   - emotional arousal,
   - comment alignment,
   - payoff honesty,
   - brevity/speakability,
   - freshness.
6. Run hard gates for beat-lock, evidence, payoff honesty, and muted safety.
7. Select the best passing hook and record why it won.
8. Use the selected hook in the first line of the script.

### Hook Families To Vary

- suspicion,
- challenge,
- comment-context,
- prediction,
- visual command,
- stakes,
- contradiction,
- character,
- object mystery,
- rule reveal,
- payoff-first,
- insider,
- motion hook,
- human reaction,
- scale/reveal,
- sensory/detail.

### Hook Examples

For bottle/color matching clips:

- "She knew that bottle way too fast."
- "The comments think she saw the answer."
- "This looks like memory, but the room says cheating."
- "Watch her face before the yellow bottle lands."
- "By the final red bottle, nobody believes her anymore."
- "One wrong bottle loses the money."
- "The suspicious part is not the bottle. It is her timing."
- "Everyone is arguing about the reflection."

For fast challenge clips:

- "The slowest player might be the smartest one here."
- "This race flips in the last ten seconds."
- "Watch the kid on the left. That is the whole video."
- "The comments missed the real strategy."
- "One move changes who is actually winning."

For trick-shot or bottle-flip clips:

- "That landing looks fake until you watch the shadow."
- "The second bounce is the giveaway."
- "Everyone celebrates too early here."
- "The trick is not the flip. It is the setup."
- "Watch the bottle cap, not the player."

### Hook Output Contract

Store hook options in script metadata or in a `hook_lab` section:

```json
{
  "evidence_packet": {
    "first_frame": "Girl and bottles already visible at the table",
    "first_motion": "Host starts moving the first bottle at 0.7s",
    "payoff_frame": "Final red match at 52.0s",
    "comment_themes": ["cheating", "reflection", "too calm"],
    "controversy_or_question": "Did she see the answer?",
    "visual_triggers": {
      "yellow_bottle": 6.0,
      "green_bottle": 28.0,
      "red_bottle": 48.0
    },
    "sound_constraint": "muted"
  },
  "hook_options": [
    {
      "text": "She knew that bottle way too fast.",
      "family": "suspicion",
      "evidence": ["comment_themes.cheating", "first_frame"],
      "spoken_seconds_estimate": 1.8,
      "visual_trigger_time": 0.0,
      "scores": {
        "first_frame_fit": 5,
        "specificity": 5,
        "curiosity_gap": 4,
        "emotional_arousal": 4,
        "comment_alignment": 5,
        "payoff_honesty": 5,
        "brevity_speakability": 5,
        "freshness": 4
      },
      "hard_gates": {
        "beat_lock": "pass",
        "evidence": "pass",
        "payoff": "pass",
        "muted_safe": "pass"
      },
      "weighted_score": 51,
      "why": "Specific, short, visual, and tied to cheating comments."
    }
  ],
  "selected_hook": {
    "text": "She knew that bottle way too fast.",
    "family": "suspicion",
    "reason": "Best blend of visual specificity and comment alignment."
  }
}
```

## Source-Commentary Timing

When `source_screen`, `source_media_review`, or `beat_map` exists, add a timing
audit before approving the script.

### Beat-Lock Rules

- The first 3 seconds must use the selected hook from the hook lab.
- Explain the game or stakes quickly, then build toward the climax.
- Use comment themes as audience context, not copied comments.
- Any line naming a visible object, player action, rule moment, or controversy
  must start at or after `visual_trigger_time`.
- Foreshadowing is allowed only when the line is phrased as foreshadowing, for
  example: "one mystery bottle is about to make everyone suspicious."

### Word Budget

Start with:

```text
target_words = source_duration_seconds * target_words_per_second
```

For high-energy commentary, use `2.6-3.1` words per second. If the user wants a
larger-scale, denser narration, use the upper end of that range, then rely on
the asset stage to measure and fit actual TTS duration.

### Timing Audit Contract

Record:

- line text,
- planned start/end,
- referenced visual,
- required `visual_trigger_time`,
- status: `ok`, `foreshadowing`, or `too_early`.

Any `too_early` line must be moved or rewritten before TTS/avatar generation.

### Mid-Production Fact Verification

If you encounter uncertainty during script writing:
- Use `web_search` to verify factual claims before committing them to the script
- Use `web_search` to find reference images for visual accuracy
- Log verification in the decision log: `category="visual_accuracy_check"`

Every factual claim in the script should be traceable to the `research_brief`.
If you make a claim that isn't in the research, do additional research and
add the source. Do not invent statistics, dates, or attributions.

## Common Pitfalls

- Overstuffing one scene because the script reads well on paper.
- Duplicating the same sentence in speech and large text overlays.
- Writing humor or improvisational beats the avatar path cannot sell.
- Reusing "Stop scrolling" or "Wait for it" when the source has stronger
  built-in curiosity.
- Source commentary: naming a bottle, player, prize, score, or trick before it
  is visible in the sampled frames.

---

## Gate Reminder (Binding)

This stage gates on human approval (`human_approval_default: true`). After review passes:
checkpoint with `status="awaiting_human"`, present the summary (the Backlot board renders
the artifact), and **END YOUR TURN**. Do not start the next stage in the same response.
Approval is per-gate — an earlier "go ahead" does not cover this gate.
