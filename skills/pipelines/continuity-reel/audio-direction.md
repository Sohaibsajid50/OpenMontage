# Audio Direction — Continuity Reel

Read during script, assets, edit, and compose. Voice performance and audible musical
emotion are creative requirements. A valid audio file and a non-silent waveform do
not establish either one.

## Choose the performance before locking timing

- Use the user's selected voice when provided. Otherwise use an approved channel
  preference, or shortlist available voices by authority, warmth, texture, accent,
  pace, and emotional fit. A generic provider default is not a creative choice.
- For a new voice without an existing approval, preview the actual hook and a
  representative body sentence. Include music when assessing the pairing. Explicit
  user selection or authorization to generate the full take satisfies this gate;
  do not ask again or create unsolicited comparison samples.
- Record provider, voice name/ID, model, supported settings, selection reason, and
  approval source in `asset_manifest.metadata.audio_direction`. Keep channel
  preferences distinct from universal defaults.
- A missing personal-library lookup does not prove a shared voice is unusable.
  Resolve the exact ID in the shared library. A denied library-add operation is a
  different permission from speech generation; a supported direct TTS request may
  work without adding it. Never change permissions or substitute a voice silently.

Generate one continuous take. Start from natural punctuation; choose pacing for the
story. Settings such as stability 0.55, similarity 0.85, style 0.0 are a documented
starting point, not a requirement for every voice. Use only parameters supported by
the selected tool/model. Do not spend on additional takes solely to satisfy a preview
step the user already waived.

## Direct music as part of the story

Choose or prompt a score with a specific role at the hook, build, reveal, and landing.
Describe emotional movement, rhythmic pulse, instrumentation, density, and space for
speech. For example: “Instrumental wildlife suspense: immediate low-string pulse,
growing tension into the feeding reveal, a restrained release at the final insight;
clear midrange space for an older narrator, no vocals.” Adapt this to the actual arc.

Reuse an approved track when the problem is its mix. Check source level and the
interesting section before buying another generation. “Quiet background music” can
produce a bed too weak to carry emotion. Sparse instrumentation can still have energy.
Record track provenance, mood/arc, chosen offset, and any loop/extension in metadata.

## Mix from measured sources, then listen

1. Measure narration and music separately. A different voice can arrive much quieter
   even with identical TTS settings. Loudness-match candidate voices for fair review.
2. Normalize narration when necessary, preserve a raw take, and record the process.
   An example normalization target is FFmpeg `loudnorm=I=-17:TP=-2:LRA=9`.
   These are targets, not measured output claims or universal delivery standards.
3. Set music gain from the actual source and the intended emotional effect. Do not
   hardcode 14%, 16%, 32%, or 65% as a quality rule. Gain is an amplitude multiplier,
   not perceived loudness or a measured voice-to-music ratio.
4. Use only enough ducking to keep words clear. Inspect threshold, ratio, attack,
   release, and any pre-attenuation together. Strong attenuation followed by strong
   ducking can erase the score throughout a continuous narration.
5. Shape entry, transitions, and ending intentionally. Verify loop joins if a new
   narration outlasts the score. Ambience serves the environment; never add noise
   solely to defeat a silence detector.
6. Check the actual exported mix at the opening, dense speech, reveal, and ending.
   Listen for clear consonants, audible musical emotion, pumping, abrupt joins,
   and a coherent landing. Check phone-like playback when possible. If listening
   is unavailable, record it as unassessed; measurements cannot stand in for ears.

Store exact normalization, gain, ducking, fades, and loop decisions under
`edit_decisions.metadata.audio_mix`; record measurements, listening method, reviewer,
and feedback under `final_review.metadata.audio_review`. Omit subjective pass claims
when no listening review occurred. User listening feedback can supply this evidence.

## Revise without wasting accepted work

For a voice/music revision, keep the approved script and footage unless the user
requests otherwise. Generate the replacement narration, realign words against the
script, rebuild scene windows and captions, and re-render from the original clips.
Do not reuse the old captions' timing or freeze footage to fill a longer performance.
Honor a hard duration limit if one exists; do not truncate the ending to fit it.
Archive prior artifacts/output, update canonical checkpoints and cumulative costs,
and deliver the version the user requested. Compare versions only when requested.

