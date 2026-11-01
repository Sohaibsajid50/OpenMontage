"""Shared fal.ai queue runner for hosted avatar tools (lip_sync, talking_head).

Submits one job, polls it, and downloads the resulting video. A queue record
file, when given, is written right after submission and blocks any later
resubmission, so a paid job is recovered instead of rerun.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

POLL_INTERVAL_SECONDS = 5
POLL_TIMEOUT_SECONDS = 1800
DOWNLOAD_TIMEOUT_SECONDS = 300


def get_fal_api_key() -> str | None:
    """Return the configured fal.ai key, if any."""
    return os.environ.get("FAL_KEY") or os.environ.get("FAL_AI_API_KEY")


def ensure_no_queue_record(record_path: str | None) -> None:
    """Raise when a previous submission was recorded, so it is recovered instead of rerun."""
    if record_path and Path(record_path).exists():
        raise RuntimeError(
            f"Queue record already exists at {record_path}; recover the recorded job instead of resubmitting"
        )


def run_fal_queue_job(
    endpoint: str, payload: dict[str, Any], output_path: Path, record_path: str | None = None
) -> dict[str, Any]:
    """Submit a fal queue job, wait for it, and write its `video` output to output_path."""
    import requests

    api_key = get_fal_api_key()
    if not api_key:
        raise RuntimeError("FAL_KEY or FAL_AI_API_KEY required for hosted fal models")
    ensure_no_queue_record(record_path)

    headers = {"Authorization": f"Key {api_key}", "Content-Type": "application/json"}
    submit_resp = requests.post(f"https://queue.fal.run/{endpoint}", headers=headers, json=payload, timeout=30)
    submit_resp.raise_for_status()
    queue_data = submit_resp.json()
    if record_path:
        record = Path(record_path)
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(json.dumps({"model": endpoint, **queue_data}, indent=2))

    deadline = time.time() + POLL_TIMEOUT_SECONDS
    while True:
        time.sleep(POLL_INTERVAL_SECONDS)
        status_resp = requests.get(queue_data["status_url"], headers=headers, timeout=15)
        status_resp.raise_for_status()
        status = status_resp.json().get("status", "UNKNOWN")
        if status == "COMPLETED":
            break
        if status in ("FAILED", "CANCELLED"):
            raise RuntimeError(f"fal job on {endpoint} {status.lower()}")
        if time.time() > deadline:
            raise RuntimeError(
                f"fal job still {status} after {POLL_TIMEOUT_SECONDS}s; recover request {queue_data.get('request_id')}"
            )

    result_resp = requests.get(queue_data["response_url"], headers=headers, timeout=30)
    try:
        result_resp.raise_for_status()
    except requests.HTTPError as error:
        raise RuntimeError(f"fal result fetch failed: {error}; body: {result_resp.text[:500]}") from error
    result_url = result_resp.json()["video"]["url"]

    video_resp = requests.get(result_url, timeout=DOWNLOAD_TIMEOUT_SECONDS)
    video_resp.raise_for_status()
    output_path.write_bytes(video_resp.content)

    return {"endpoint": endpoint, "request_id": queue_data.get("request_id"), "result_url": result_url}
