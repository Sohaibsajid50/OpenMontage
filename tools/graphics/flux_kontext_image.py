"""FLUX Kontext image-to-image generation via fal.ai API."""

from __future__ import annotations

import base64
import mimetypes
import os
import time
from pathlib import Path
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)


def _file_to_data_uri(path: str) -> str:
    file_path = Path(path)
    mime_type = mimetypes.guess_type(file_path.name)[0] or "image/png"
    encoded = base64.b64encode(file_path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


class FluxKontextImage(BaseTool):
    name = "flux_kontext_image"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "image_generation"
    provider = "flux_kontext"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.SEEDED
    runtime = ToolRuntime.API

    dependencies = []
    install_instructions = (
        "Set FAL_KEY to your fal.ai API key.\n"
        "  Get one at https://fal.ai/dashboard/keys"
    )
    agent_skills = ["flux-best-practices", "bfl-api"]

    capabilities = ["generate_image", "edit_image", "image_to_image", "reference_image"]
    supports = {
        "reference_image": True,
        "image_edit": True,
        "seed": True,
        "aspect_ratio": True,
    }
    best_for = [
        "FLUX image editing with a reference image via fal.ai",
        "character or subject continuity from a prior generated frame",
        "targeted global edits while preserving image context",
    ]
    not_good_for = ["offline generation", "precise inpainting masks"]

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "model_variant": {"type": "string", "enum": ["kontext", "flux-2-pro"], "default": "kontext"},
            "image_paths": {"type": "array", "items": {"type": "string"}, "maxItems": 9},
            "image_size": {"type": "object", "properties": {"width": {"type": "integer"}, "height": {"type": "integer"}}, "required": ["width", "height"]},
            "prompt": {"type": "string"},
            "image_url": {"type": "string", "description": "Source image URL for reference/edit mode"},
            "image_path": {"type": "string", "description": "Local source image path for reference/edit mode"},
            "aspect_ratio": {
                "type": "string",
                "enum": ["21:9", "16:9", "4:3", "3:2", "1:1", "2:3", "3:4", "9:16", "9:21"],
                "default": "9:16",
            },
            "seed": {"type": "integer"},
            "guidance_scale": {"type": "number", "default": 3.5},
            "num_images": {"type": "integer", "default": 1},
            "output_format": {
                "type": "string",
                "enum": ["jpeg", "png"],
                "default": "jpeg",
            },
            "safety_tolerance": {
                "type": "string",
                "enum": ["1", "2", "3", "4", "5", "6"],
                "default": "2",
            },
            "output_path": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=1, ram_mb=512, vram_mb=0, disk_mb=100, network_required=True
    )
    retry_policy = RetryPolicy(max_retries=2, retryable_errors=["rate_limit", "timeout"])
    idempotency_key_fields = ["prompt", "image_url", "image_path", "image_paths", "model_variant", "image_size", "seed", "aspect_ratio"]
    side_effects = ["writes image file to output_path", "calls fal.ai API"]
    user_visible_verification = ["Inspect edited image for identity continuity and quality"]

    def _get_api_key(self) -> str | None:
        return os.environ.get("FAL_KEY") or os.environ.get("FAL_AI_API_KEY")

    def get_status(self) -> ToolStatus:
        if self._get_api_key():
            return ToolStatus.AVAILABLE
        return ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        if inputs.get("model_variant") == "flux-2-pro":
            import math
            from PIL import Image
            size = inputs.get("image_size", {"width": 1024, "height": 1024})
            # Conservative per-image rounding; provider billing remains authoritative.
            output_mp = math.ceil(size["width"] * size["height"] / 1_000_000)
            input_mp = 0
            for path in inputs.get("image_paths", []):
                with Image.open(path) as im:
                    input_mp += math.ceil(im.width * im.height / 1_000_000)
            return round(0.03 + 0.015 * (max(0, output_mp - 1) + input_mp), 4)
        return 0.04

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        api_key = self._get_api_key()
        if not api_key:
            return ToolResult(
                success=False,
                error="No fal.ai API key found. " + self.install_instructions,
            )

        variant = inputs.get("model_variant", "kontext")
        if variant not in ("kontext", "flux-2-pro"):
            return ToolResult(success=False, error="Unsupported FLUX model_variant")
        if variant == "flux-2-pro" and not inputs.get("image_paths"):
            return ToolResult(success=False, error="FLUX.2 Pro requires local image_paths")
        image_ref = inputs.get("image_url")
        if not image_ref and inputs.get("image_path"):
            image_path = Path(inputs["image_path"])
            if not image_path.is_file():
                return ToolResult(success=False, error=f"Image not found: {image_path}")
            image_ref = _file_to_data_uri(str(image_path))
        if not image_ref and variant == "kontext":
            return ToolResult(
                success=False,
                error="FLUX Kontext requires image_url or image_path for reference/edit mode.",
            )

        import requests

        start = time.time()
        prompt = inputs["prompt"]
        payload: dict[str, Any] = {
            "prompt": prompt,
            "image_url": image_ref,
            "aspect_ratio": inputs.get("aspect_ratio", "9:16"),
            "num_images": inputs.get("num_images", 1),
            "output_format": inputs.get("output_format", "jpeg"),
            "safety_tolerance": inputs.get("safety_tolerance", "2"),
        }
        if inputs.get("seed") is not None:
            payload["seed"] = inputs["seed"]
        if inputs.get("guidance_scale") is not None:
            payload["guidance_scale"] = inputs["guidance_scale"]

        model = "fal-ai/flux-pro/kontext"
        if variant == "flux-2-pro":
            paths = inputs["image_paths"]
            if len(paths) > 9 or any(not Path(p).is_file() for p in paths):
                return ToolResult(success=False, error="FLUX.2 Pro needs 1-9 existing reference files")
            model = "fal-ai/flux-2-pro/edit"
            payload = {
                "prompt": prompt,
                "image_urls": [_file_to_data_uri(p) for p in paths],
                "image_size": inputs.get("image_size", {"width": 1024, "height": 1024}),
                "output_format": inputs.get("output_format", "jpeg"),
                "safety_tolerance": inputs.get("safety_tolerance", "2"),
            }
            if inputs.get("seed") is not None:
                payload["seed"] = inputs["seed"]

        try:
            response = requests.post(
                f"https://fal.run/{model}",
                headers={
                    "Authorization": f"Key {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=180,
            )
            response.raise_for_status()
            data = response.json()

            image_url = data["images"][0]["url"]
            image_response = requests.get(image_url, timeout=90)
            image_response.raise_for_status()

            output_path = Path(inputs.get("output_path", "flux_kontext_image.jpg"))
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(image_response.content)

        except Exception as e:
            detail = ""
            if isinstance(e, requests.HTTPError) and e.response is not None:
                try:
                    body = e.response.json()
                    errors = body.get("detail", [])
                    if isinstance(errors, list):
                        detail = str([{k: item[k] for k in ("loc", "msg", "type") if k in item}
                                      for item in errors if isinstance(item, dict)])[:1000]
                    elif isinstance(errors, str):
                        detail = errors[:500]
                except (ValueError, AttributeError):
                    pass
            return ToolResult(success=False, error=f"FLUX generation failed: {e}; {detail}")

        return ToolResult(
            success=True,
            data={
                "provider": "flux_kontext",
                "model": model,
                "image_paths": inputs.get("image_paths"),
                "prompt": prompt,
                "image_path": inputs.get("image_path"),
                "image_url": inputs.get("image_url"),
                "output": str(output_path),
                "seed": data.get("seed"),
                "source_endpoint": f"https://fal.run/{model}",
            },
            artifacts=[str(output_path)],
            cost_usd=self.estimate_cost(inputs),
            duration_seconds=round(time.time() - start, 2),
            seed=data.get("seed"),
            model=model,
        )
