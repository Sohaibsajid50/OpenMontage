"""Contracts for behavior-first hooks in the continuity-reel pipeline."""

from pathlib import Path
import sys

import jsonschema
import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from lib.pipeline_loader import load_pipeline
from schemas.artifacts import validate_artifact


def _continuity_script(first_role: str = "hook") -> dict:
    return {
        "version": "1.0",
        "title": "Behavior First",
        "total_duration_seconds": 24,
        "sections": [
            {
                "id": "beat-01",
                "text": "This animal lands two hits with one punch.",
                "start_seconds": 0,
                "end_seconds": 4.8,
                "beat_role": first_role,
            },
            {
                "id": "beat-02",
                "text": "Meet the peacock mantis shrimp.",
                "start_seconds": 4.8,
                "end_seconds": 8.5,
                "beat_role": "stakes",
            },
            {
                "id": "beat-03",
                "text": "Its collapsing bubble becomes the second impact.",
                "start_seconds": 8.5,
                "end_seconds": 12,
                "beat_role": "re_hook",
            },
        ],
        "metadata": {
            "pipeline": "continuity-reel",
            "hook_mode": "spectacle_montage",
            "selected_hook_visual": "club strike followed by cavitation collapse",
            "identity_reveal_at_seconds": 4.8,
        },
    }


def test_continuity_script_requires_hook_first_but_allows_held_hook() -> None:
    validate_artifact("script", _continuity_script())

    with pytest.raises(jsonschema.ValidationError):
        validate_artifact("script", _continuity_script(first_role="stakes"))


def test_scene_plan_accepts_video_hook_role() -> None:
    validate_artifact(
        "scene_plan",
        {
            "version": "1.0",
            "scenes": [
                {
                    "id": "scene-01",
                    "type": "video",
                    "description": "The club strikes and the cavitation bubble collapses.",
                    "start_seconds": 0,
                    "end_seconds": 4.8,
                    "narrative_role": "hook",
                }
            ],
            "metadata": {"hook_mode": "spectacle_montage"},
        },
    )


@pytest.mark.parametrize(
    ("mode", "caption_mode", "transition_strategy"),
    [
        ("spectacle_montage", "kinetic_keywords", "impact_cuts"),
        ("impossible_tableau", "phrase", "held_proof_shot"),
    ],
)
def test_edit_decisions_encode_hook_treatment(
    mode: str, caption_mode: str, transition_strategy: str
) -> None:
    validate_artifact(
        "edit_decisions",
        {
            "version": "1.0",
            "render_runtime": "ffmpeg",
            "cuts": [
                {
                    "id": "cut-01",
                    "source": "strike.mp4",
                    "in_seconds": 0,
                    "out_seconds": 4.8,
                    "fit": "stretch",
                    "speed_factor": 0.9,
                    "beat_role": "hook",
                }
            ],
            "hook_treatment": {
                "mode": mode,
                "proof_visible_at_seconds": 0,
                "narration_entry": "immediate",
                "caption_mode": caption_mode,
                "transition_strategy": transition_strategy,
                "music_entry": "immediate_active",
                "sfx_strategy": "impact_synchronized",
            },
            "subtitles": {
                "enabled": True,
                "caption_mode": caption_mode,
                "hook_keywords": ["TWO HITS", "ONE PUNCH"],
            },
        },
    )


def test_pipeline_manifest_and_directors_share_the_contract() -> None:
    manifest = load_pipeline("continuity-reel")
    script_stage = next(stage for stage in manifest["stages"] if stage["name"] == "script")
    joined = " ".join(script_stage["review_focus"] + script_stage["success_criteria"])
    assert "spectacle_montage" in joined
    assert "impossible_tableau" in joined
    assert "before biography" in joined

    hook_engine = (PROJECT_ROOT / "skills/creative/narrative-hook-engine.md").read_text()
    scene_director = (PROJECT_ROOT / "skills/pipelines/continuity-reel/scene-director.md").read_text()
    edit_director = (PROJECT_ROOT / "skills/pipelines/continuity-reel/edit-director.md").read_text()
    compose_director = (PROJECT_ROOT / "skills/pipelines/continuity-reel/compose-director.md").read_text()

    for document in (hook_engine, scene_director, edit_director, compose_director):
        assert "spectacle_montage" in document
        assert "impossible_tableau" in document

    assert "Plan deliberate ~1.5–2.0s pauses" not in scene_director
    assert "fixed mix" in compose_director
    assert "not voice-responsive ducking" in edit_director
