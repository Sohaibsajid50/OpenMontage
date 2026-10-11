# Hook Engine

Use this skill when writing the first 1-3 seconds of short-form narration,
especially source-commentary videos. The hook is not a slogan. It is a
beat-locked promise: what to watch, why it matters, and what payoff the viewer
risks missing.

## Research Basis

This process is based on current platform guidance, video-analysis research,
and public short-form hook skill patterns.

- YouTube Help treats opening retention as a measurable quality signal:
  audience-retention reports identify first-30-second intro performance, top
  moments, spikes, and dips. Shorts analytics also keeps `engaged views`,
  meaning viewers who chose to continue watching.
  <https://support.google.com/youtube/answer/9314415>
  <https://support.google.com/youtube/answer/10059070>
- Zhang et al. (2026) explicitly define the first three seconds as the
  video-ad `hooking period` and argue it must be evaluated multimodally across
  visuals, audio, and text, not as copy alone.
  <https://arxiv.org/abs/2602.22299>
- Violot et al. (2024) show Shorts behave differently from regular YouTube
  videos and over-index toward entertainment categories, so the opening should
  be built for fast entertainment comprehension instead of long-form setup.
  <https://arxiv.org/abs/2403.00454>
- Berger and Milkman (2012) find virality is connected to emotional arousal,
  including awe, anger, and anxiety. For source commentary, this supports hooks
  that activate conflict, suspicion, awe, or social debate without fabricating
  claims.
  <https://doi.org/10.1509/jmr.10.0353>
- Curiosity research supports information-gap hooks: viewers stay when they
  know enough to care but not enough to resolve the question.
  <https://arxiv.org/abs/2204.01182>
- The public `tiktok-reel-hook-generator` skill is useful for visual hook
  categories: sensory trigger, disruption, transformation tease, human moment,
  motion hook, and scale reveal. For OpenMontage, those categories become
  evidence inputs rather than copy templates.
  <https://github.com/aicontentskills/tiktok-reel-hook-generator>

## Rule Zero

Do not default to:

- "Stop scrolling"
- "Wait for it"
- "You won't believe this"
- "This is crazy"
- "Watch until the end"
- "POV"

These are allowed only if the source makes the phrase unusually specific and it
scores higher than source-specific alternatives. Otherwise they read as template
language and waste the first beat.

## Inputs

Build hooks from the strongest available signals:

- first visible frame,
- first motion in frame,
- first surprising action,
- final payoff,
- comment-section argument,
- transcript conflict,
- object that appears later,
- player behavior,
- visual trick, rule, or controversy,
- money/prize/stakes,
- unanswered question viewers are likely to ask,
- creator/title promise,
- platform comments with repeated wording or accusations.

## Evidence Packet

Before generating hook options, record the evidence. If an item is unknown,
write `unknown` instead of inventing it.

```json
{
  "first_frame": "What is visible at 0.0s",
  "first_motion": "What moves first and when",
  "payoff_frame": "What happens near the climax/end and timestamp",
  "comment_themes": ["theme 1", "theme 2", "theme 3"],
  "controversy_or_question": "What viewers are likely debating",
  "visual_triggers": {
    "object_or_action": "timestamp_seconds"
  },
  "sound_constraint": "usable | muted | dialogue_heavy | unknown"
}
```

## Hook Lab Process

Generate at least 12 hook options before choosing one. Use different families
so the options are genuinely varied.

Required mix:

- at least 3 comment-intelligence hooks,
- at least 3 first-frame or first-motion hooks,
- at least 2 payoff/open-loop hooks,
- at least 2 conflict, suspicion, or challenge hooks,
- at least 2 curiosity-gap hooks.

For each hook, record:

- hook text,
- family,
- evidence used,
- spoken duration estimate,
- referenced visual and trigger time,
- score breakdown.

## Hook Families

| Family | Shape | Example |
| --- | --- | --- |
| Suspicion | Something is off with X. | "She knew that bottle way too fast." |
| Challenge | Ask viewers to judge. | "Tell me if this looks real or staged." |
| Comment-context | Surface the audience argument. | "The comments think she saw the answer." |
| Prediction | Promise a near-future reversal. | "The last bottle is where everyone loses it." |
| Visual command | Direct eyes to a visible detail. | "Watch her eyes before the yellow bottle lands." |
| Stakes | Name the cost of failure. | "One wrong bottle loses the whole round." |
| Contradiction | It looks like X, but Y. | "This looks like memory, but the room says cheating." |
| Character | Point to unusual behavior. | "She is calm. Everyone else is panicking." |
| Object mystery | One object changes the story. | "That blue bottle is not the suspicious part." |
| Rule reveal | Explain why the clip is hard. | "They have to match the hidden row without seeing it." |
| Payoff-first | Tease the end without spoiling. | "By the final red bottle, nobody believes her anymore." |
| Insider | Name what repeat viewers noticed. | "People rewatched this for the reflection." |
| Motion hook | Start from incomplete action. | "That second bounce is already a problem." |
| Human reaction | Start from face/body language. | "His face gives away the whole round." |
| Scale/reveal | Start small, imply bigger reveal. | "This tiny cup is about to decide the game." |
| Sensory/detail | Use tactile/visual vividness. | "That balloon stretch is the warning sign." |

## Scoring

Score each hook from 0-5. Use the weighted total to choose finalists, then run
the hard gates.

| Criterion | Weight | What 5 Means |
| --- | --- | --- |
| `first_frame_fit` | 2 | Works with what is visible in the opening frame. |
| `specificity` | 2 | Names a concrete person, action, object, or rule. |
| `curiosity_gap` | 1 | Opens a clear question without clickbait. |
| `emotional_arousal` | 1 | Creates suspicion, awe, tension, humor, or social debate. |
| `comment_alignment` | 1 | Uses repeated audience themes from real comments. |
| `payoff_honesty` | 1 | The video actually delivers what the hook promises. |
| `brevity_speakability` | 1 | Can be spoken in 1.5-3.0 seconds, or split cleanly. |
| `freshness` | 1 | Avoids obvious template language. |

Hard gates:

- `beat_lock`: pass/fail. A hook must not name a visible object or action before
  it appears unless it is phrased as foreshadowing.
- `evidence`: pass/fail. A hook must cite at least one evidence packet field.
- `payoff`: pass/fail. A hook must not promise a reveal the video lacks.
- `muted_safe`: pass/fail. If the source will be muted, the hook must work from
  visuals and commentary alone.

Choose the hook with the best weighted score that passes all hard gates. If the
highest-scoring hook fails beat-lock, rewrite it or choose the next finalist.

## Output Contract

Before the final script, include a hook lab:

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
      "referenced_visual": "girl reacting to bottle choice",
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
      "why": "Specific, visual, short, and tied to the main comment debate."
    }
  ],
  "selected_hook": {
    "text": "She knew that bottle way too fast.",
    "family": "suspicion",
    "reason": "Best blend of first-frame fit, comment alignment, brevity, and payoff honesty."
  }
}
```

## Examples For Source-Commentary Game Clips

For a bottle matching game:

- "She knew that bottle way too fast."
- "The comments think she saw the answer."
- "This looks like memory, but the room says cheating."
- "Watch her eyes before the yellow bottle lands."
- "By the final red bottle, nobody believes her anymore."
- "One wrong bottle loses the whole round."
- "The suspicious part is not the bottle. It is her timing."
- "Everyone is arguing about the reflection."
- "His reaction changes before the answer shows."
- "The first match looks easy. The last one does not."

For a balloon or popping challenge:

- "The slowest kid might be the smartest one here."
- "This race flips in the last ten seconds."
- "Watch the kid on the left. That is the whole video."
- "The comments missed the real strategy."
- "One pop changes who is actually winning."
- "That first balloon is already a trap."
- "He is not losing. He is setting up the finish."

For a bottle flip or trick-shot challenge:

- "That landing looks fake until you watch the shadow."
- "The second bounce is the giveaway."
- "Everyone celebrates too early here."
- "The trick is not the flip. It is the setup."
- "Watch the bottle cap, not the player."
- "The first miss makes the ending better."

## Anti-Patterns

- Generic command with no source detail: "Stop scrolling."
- Fake certainty: "This is 100% rigged" when evidence is unclear.
- Spoiling too early: naming a late object before it appears without
  foreshadowing.
- Comment bait without context: "People are mad" when comments are not about
  anger.
- Hooks that require sound if the first frame does not visually support them.
- Hooks that are true but not speakable in the first three seconds.
- Hooks that work as text but do not match the frame shown underneath.
