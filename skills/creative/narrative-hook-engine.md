# Narrative Hook Engine — Topic-Driven Short-Form Scripts

Use this skill to write the **script and opening hook** for a fully-generated
short-form narrated video about ANY subject — an animal, a person, a place, an
event, a discovery, an object, a concept. Unlike source-commentary hooks (which
react to existing footage and comments), this engine builds the hook and the
whole retention arc from the **subject's own strongest facts**, because every
visual is generated from the script.

This is the script brain for the `continuity-reel` pipeline, but it is
subject-agnostic and reusable.

## Core Premise

The first **1.5–3 seconds** decide whether the video is watched. The hook is not
a slogan — it is a **beat-locked promise**: it opens a question the viewer needs
resolved, and the rest of the script delivers the answer while opening the next
question. In a generated reel the hook is **two things at once**:

1. a **spoken line** (the narration's first beat), and
2. a **visual** (the opening generated shot).

Both must land together. A great line over a weak opening frame fails; a stunning
frame with a generic line fails. Design them as a pair.

## Rule One — Behavior Before Biography

Show the subject's most unusual behavior, consequence, anomaly, or transformation
before habitat, taxonomy, biography, or a neutral identity shot. The opening claim
must describe what is visible **now**, not footage that appears later. Name the
subject only after the hook has earned the viewer's attention.

Default information order:

`BEHAVIOR/CONSEQUENCE -> CONTRAST OR OPEN MECHANISM -> IDENTITY -> EXPLANATION -> PAYOFF`

This is not a command to reveal the complete answer. Show enough proof to make the
question concrete, then preserve the surprising mechanism or second consequence.

## Select the Hook Mode

Choose the mode from the available footage and subject behavior. Record it in the
hook lab as `hook_mode`.

### `spectacle_montage`

Use when several impacts, reactions, transformations, or escalating consequences
are individually legible. A visual cold open, faster cuts, layered reaction, impact
SFX, and selective kinetic keywords may help. Keep extending the montage only while
the action escalates.

### `impossible_tableau`

Use when one strange behavior is visually clear enough to hold attention by itself.
Begin the contrast line immediately and hold the proof shot long enough to inspect.
Prefer restrained phrase captions and meaningful subject motion over decorative
cutting.

Do not score one mode as inherently more engaging. The wrong fast montage can make
proof harder to understand; the wrong long take can become an empty establishing
shot.

## Research Basis (why these rules)

- **First 3 seconds = the hooking period**, evaluated multimodally across visual,
  audio, and text — not copy alone. (Zhang et al. 2026, arXiv:2602.22299)
- **Shorts over-index on fast entertainment comprehension** — open for immediate
  payoff, not long-form setup. (Violot et al. 2024, arXiv:2403.00454)
- **Virality tracks emotional arousal** — awe, anxiety, anger, suspense. Build
  hooks that activate one of these from a TRUE fact, never a fabricated claim.
  (Berger & Milkman 2012, jmr.10.0353)
- **Curiosity is an information gap** — the viewer must know *enough to care* but
  *not enough to resolve*. Too little context = no curiosity; full answer = no
  reason to stay. (curiosity / information-gap research, arXiv:2204.01182)
- **Opening retention is a measured signal** (YouTube audience-retention, Shorts
  engaged views). The opening frame must also work as a **still/thumbnail**.
- **Visual hook patterns** (sensory, disruption, transformation, human-moment,
  motion, scale-reveal) adapted from the public `tiktok-reel-hook-generator`
  skill — used here as opening-shot strategies, not copy templates.

## Rule Zero — Banned Openers

Do NOT default to template clickbait:

- "Stop scrolling" / "Wait for it" / "You won't believe this" / "This is crazy"
- "Watch until the end" / "POV" / "Here's why" / "Let me tell you about…"
- Encyclopedia openers: "The [X] is a species of…" / "[Name] was born in…"

These waste the most valuable beat. They are allowed ONLY if the subject makes the
phrase unusually specific and it out-scores every subject-specific alternative.

## Step 1 — Build the Subject Evidence Packet

Before writing any hook, mine the subject for the raw material a hook is made of.
Research the subject (web search if needed — do not invent facts). If a field is
unknown, write `unknown`; never fabricate.

Do not treat a worked example as a factual evidence packet. Record `subject`,
`one_line`, `surprising_fact`, `conflict_or_stakes`, `open_question`, and `payoff`
with claim-level source references and uncertainty. Optional superlatives and
precise numbers stay `unknown` until sourced. In particular, reconstructions of
extinct animals must not turn uncertain anatomy or inferred behavior into a
confident narrated fact.

For other subject types, the same fields apply:
- **Biography:** superlative = their defining achievement; conflict = what they
  overcame; open_question = the improbable turn; payoff = how it resolved.
- **History/event:** stakes = what was at risk; surprising_fact = the detail
  textbooks skip; payoff = the consequence that still matters.
- **Science/concept:** counterintuitive = the part that breaks intuition;
  open_question = "how is that possible?"; payoff = the mechanism.

## Step 2 — Hook Lab (explore, test the promise, select)

For open concepts, explore genuinely different hook/visual pairs (around ten
can help when the direction is unclear). Do not require a quota for a hook the
user already approved; audit that pair and retain their direction. Each hook = a spoken line + the
opening shot it implies.

Hook-family examples below illustrate rhetoric only; they are not verified facts
or reusable evidence. Research the actual subject before using any such claim.

### Hook Families (subject-agnostic)

| Family | Shape | Example (varied subjects) |
| --- | --- | --- |
| **Superlative** | Name an extreme, concretely. | "This is the largest rhino that ever walked the Earth." |
| **Information gap** | Open a question, withhold the answer. | "Even apex predators refused to hunt this animal. Here's why." |
| **Counterintuitive** | Set up an expectation, break it. | "They called it a unicorn. It was a five-ton tank." |
| **Stakes / threat** | Name the danger or cost. | "Getting this wrong meant a six-foot horn through your ribs." |
| **Scale reveal** | Start small/tight, imply huge. | "That horn alone was taller than you are." |
| **In-progress / motion** | Drop into action already happening. | "It's already charging — and nothing on the steppe can stop it." |
| **Time collision** | Connect past to the viewer's now. | "Your ancestors actually saw this thing alive." |
| **Mystery / open loop** | Tease a reveal the body pays off. | "Its horn had a third purpose nobody expected." |
| **Contradiction** | "It looks like X, but Y." | "It looks like a myth. Every bone of it was real." |
| **Human stakes (bio/history)** | Put a person at a decision point. | "At 23, she'd been told no by every lab in the country." |
| **Awe / sensory** | Lead with a vivid, tactile image. | "Five tons of muscle moving through a frozen white silence." |

### For each hook option, record:

- `text` (the spoken line, 1.5–3.0s when read aloud)
- `hook_mode` (`spectacle_montage` or `impossible_tableau`)
- `family`
- `evidence_used` (which evidence-packet field — must cite at least one)
- `opening_shot` (the generated visual that plays under it; name the visual hook
  pattern: sensory / disruption / transformation / human-moment / motion / scale-reveal)
- `spoken_seconds_estimate`
- `scores` (below)

### Scoring (0–5 each, weighted)

| Criterion | Weight | What 5 means |
| --- | --- | --- |
| `curiosity_gap` | 2 | Opens a clear question; viewer must stay to resolve it. |
| `specificity` | 2 | Names a concrete fact/number/image, not a vague claim. |
| `emotional_arousal` | 1 | Triggers awe, tension, suspicion, or surprise. |
| `visual_pairing` | 1 | The opening shot is strong as a still AND matches the line. |
| `truth` | 1 | Grounded in a real fact from the evidence packet. |
| `brevity_speakability` | 1 | Reads in 1.5–3.0s; flows when spoken aloud. |
| `freshness` | 1 | Avoids template/clickbait language. |
| `payoff_setup` | 1 | The body of the script can actually deliver what it promises. |

### Hard Gates (pass/fail — a hook must pass ALL)

- `truth`: cites a real evidence-packet fact; invents nothing.
- `payoff`: the script delivers the reveal/answer the hook promises.
- `gap`: leaves a question open — does not state the full answer in the hook.
- `visual_still`: the opening shot works as a frozen thumbnail.
- `speakable`: can be spoken cleanly in ≤3s.
- `behavior_first`: proof or consequence appears before contextual orientation.
- `synchronized`: the spoken claim and visible evidence refer to the same thing.
- `mode_fit`: shot duration, cut density, captions, and narration entry match the
  selected hook mode rather than a universal template.

Scores are editorial judgments, not measured retention or evidence that an asset
will work. First reject pairs with unsupported claims or an essential visual
that lacks a credible production plan. Record the hardest shot and its failure
condition; actual generated footage still needs inspection.

Pick the strongest supported pair that passes every gate. If the top hook fails a
gate, rewrite it or take the next finalist.

## Step 3 — Structure the Whole Script (retention arc)

A great hook with a flat body still loses viewers. Build the full narration as a
**chain of open and closed loops** — every beat answers the previous question and
advances the main question. A clear answer can hold attention without another
cliffhanger. Target documentary pacing: **2.0–2.5 words/second**, with short
breaths between beats (not long dead-air pauses).

Recommended arc for a 30–60s reel:

1. **Hook (0–3s)** — the selected hook. Open the primary loop.
2. **Stakes / scale (next 1–2 beats)** — make the subject matter: how big, how
   rare, how dangerous, how improbable. Deepen the awe or tension.
3. **Escalation (middle)** — 2–4 beats of evidence, each raising a new micro-question.
   This is where most facts live. Keep each beat one idea; never stack three facts
   into one breath.
4. **Turn / reveal (the payoff loop)** — the surprising answer the hook promised
   (the "third purpose", the improbable victory, the twist). This is the emotional
   peak — pair it with the `hero_moment` shot.
5. **Landing (final beat)** — a resonant close that re-frames the subject or leaves
   a lingering thought. Avoid a hard "the end"; let it echo.

For a reel longer than 20 seconds, introduce at least one fresh `re_hook` around
8–12 seconds: a contradiction, new consequence, or incomplete mechanism. Do not
repeat the opening claim in different words.

**Loop discipline:** before writing each beat, ask "what question is the viewer
holding right now?" The beat should partly answer it and open the next. If a beat
answers nothing and asks nothing, cut it.

## Step 4 — Output Contract

Produce a hook lab + the final script. The script feeds the scene-director as
ordered narration beats. A beat may span multiple shots linked by
`script_section_id`; shot count follows the explanation, not sentence count.

```json
{
  "evidence_packet": { "...": "see Step 1" },
  "hook_lab": {
    "options": [ { "text": "...", "family": "...", "opening_shot": "...", "scores": {}, "weighted_score": 0, "gates": {} } ],
    "selected_hook": { "text": "...", "family": "...", "opening_shot": "...", "reason": "..." }
  },
  "script": {
    "title": "...",
    "arc": ["hook","stakes","escalation","turn","landing"],
    "sections": [
      { "id": "vo-01", "text": "<the selected hook line>", "beat_role": "hook" },
      { "id": "vo-02", "text": "...", "beat_role": "stakes" }
    ]
  }
}
```

## Anti-Patterns

- **Encyclopedia opener** — "The X is a species of…" / "X was born in Y." Lead with
  the most arresting true fact instead.
- **Fact dump** — stacking multiple facts into one beat. One idea per beat.
- **Answer in the hook** — stating the full payoff up front kills the gap.
- **Vague awe** — "This animal is amazing." Replace with the concrete reason.
- **Verbal/visual mismatch** — a line about the horn over a wide empty-steppe frame.
- **Context before proof** — habitat, taxonomy, or identity appears before the
  behavior that makes the subject worth knowing.
- **Cut-density cargo cult** — adding cuts because another viral Reel cut quickly.
  Cut only when the next image advances proof, scale, mechanism, or consequence.
- **Caption-style cargo cult** — kinetic keywords and restrained phrases are both
  valid; choose according to hook mode and visual complexity.
- **Fabrication for drama** — inventing a stat or threat. Truth gate fails it.
- **Dead-air pacing** — long pauses between beats read as "broken / in steps." Keep
  breaths short; let the voice carry continuously.
- **No landing** — trailing off, or a flat "and that's the story of X."
