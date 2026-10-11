# Continuity Reel fork

This fork adds `continuity-reel` to upstream OpenMontage. It includes the pipeline manifest, all seven continuity direction/review guides, visual-memory schema, hook and scene contracts, reference-conditioned FLUX image generation, and Kling first/last-frame and economical i2v support.

## First use on a new laptop

Read the repository README for dependencies, then AGENT_GUIDE.md and pipeline_defs/continuity-reel.yaml. Use the live tool registry to check provider availability and supported inputs. Configure credentials locally; none are included. Prices in tools are estimates: confirm current endpoint costs and a per-run cap before generation.

Give your agent: "Read AGENT_GUIDE.md and use the continuity-reel pipeline for this video. Load each stage director and its provider guidance before executing. Use my channel DNA and budget."

## Default continuity approval policy

For continuity-reel, research and inspect real subject references automatically. Select the strongest hook internally and present its opening visual, narration and payoff together with the full script and proposal decisions for approval. Preserve the native proposal and script artifacts; record the user's actual approval for both only when both were presented.

Next present the full scene plan and budget for approval before generation. Generate the subject reference and hardest essential action as samples; wait for sample approval before remaining assets. Complete the approved batch, narration, music, captions and edit automatically within that plan. After an initial essential-shot attempt and two failed repairs, stop and show observed failures, costs and alternatives. Material changes need affected approval again. Publication requires separate approval of the actual final video, accounts, captions and time.

This policy applies ahead of generic concept-shortlisting/review defaults for this pipeline. Record sample approval and retry outcomes in project artifacts/decision_log before continuing assets. These instructions do not constitute an isolated spending service or automatic visual-quality judge. Content OS-managed runs must additionally use its approvals and ledger.

## Updating

`origin` is this fork. Add `upstream` pointing to https://github.com/calesthio/OpenMontage.git to review future upstream changes. Merge updates deliberately and run contract tests; do not overwrite the custom pipeline with a fresh upstream directory copy.

Channel DNA, private voice preferences, credentials, generated projects and the original laptop's checkpoint history are not part of this change. Existing channels must point their engine_root at this checkout to use it. Provider generation and final video quality still require validation on the target laptop.
