# Publish Director - Avatar Spokesperson Pipeline

## When To Use

Package the finished spokesperson outputs for delivery. This stage should make it obvious which file is the hero cut, which are derivatives, and what message or audience each version serves.

For source-commentary shorts, package the final render with the source research,
comment themes, beat map, timing audit, narration fit report, and caption file so
future videos can repeat the same workflow.

## Process

### 1. Label Deliverables Clearly

Distinguish:

- hero cut,
- vertical cutdown,
- square cutdown,
- language variants,
- watermark or review versions.

### 2. Keep Metadata Message-Led

Recommended metadata keys:

- `audience_segment`
- `cta_copy`
- `offer_name`
- `locale`
- `thumbnail_concept`
- `source_url`
- `avatar_layout_mode`
- `narration_fit_report`

### 3. Package Review Notes

If the avatar path has limitations such as visible lip-sync risk, retain that note in the package instead of hiding it.

### 4. Quality Gate

- exports are clearly named,
- metadata matches the intended message,
- poster frame or thumbnail concept features the presenter cleanly,
- review notes stay attached to the package.
- source-commentary packages include source notes, timing audit, captions, and
  final render paths.

## Common Pitfalls

- Mixing hero and derivative exports without clear naming.
- Reusing generic metadata that ignores the spokesperson offer.
- Dropping risk notes that matter for downstream publishing teams.

---

## Gate Reminder (Binding)

This stage gates on human approval (`human_approval_default: true`). After review passes:
checkpoint with `status="awaiting_human"`, present the summary (the Backlot board renders
the artifact), and **END YOUR TURN**. Do not start the next stage in the same response.
Approval is per-gate — an earlier "go ahead" does not cover this gate.
