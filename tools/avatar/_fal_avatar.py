"""Hosted photo + audio -> talking-video models on fal.ai for the talking_head tool."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from tools.avatar._fal_queue import ensure_no_queue_record, get_fal_api_key, run_fal_queue_job

FAL_AVATAR_ENDPOINTS = {
    "kling_avatar_v2_pro": "fal-ai/kling-video/ai-avatar/v2/pro",
    "sync_3_image": "fal-ai/sync-lipsync/v3/image-to-video",
}

# Models whose endpoint accepts a motion/performance text prompt.
PROMPT_MODELS = {"kling_avatar_v2_pro"}

# Published fal rate, USD per second of output video.
FAL_AVATAR_USD_PER_SECOND = {
    "kling_avatar_v2_pro": 0.115,
    "sync_3_image": 0.1333,
}


def run_fal_avatar(model: str, image_path: Path, audio_path: Path, output_path: Path, inputs: dict[str, Any]) -> dict[str, Any]:
    """Animate a still photo with driving audio on fal and write the video to output_path."""
    from tools.video._shared import upload_file_fal

    endpoint = FAL_AVATAR_ENDPOINTS.get(model)
    if endpoint is None:
        raise RuntimeError(f"Model '{model}' has no hosted fal endpoint")
    if not get_fal_api_key():
        raise RuntimeError("FAL_KEY or FAL_AI_API_KEY required for hosted talking-head models")
    record_path = inputs.get("queue_record_path")
    ensure_no_queue_record(record_path)

    payload = {
        "image_url": upload_file_fal(str(image_path)),
        "audio_url": upload_file_fal(str(audio_path)),
    }
    if inputs.get("prompt") and model in PROMPT_MODELS:
        payload["prompt"] = inputs["prompt"]
    return run_fal_queue_job(endpoint, payload, output_path, record_path)
