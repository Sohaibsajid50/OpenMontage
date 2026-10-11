"""Offline regression checks for the continuity fork on current upstream."""
from pathlib import Path
from unittest.mock import patch

import pytest
from lib.pipeline_loader import load_pipeline
from schemas.artifacts import load_schema
from tools.graphics.flux_kontext_image import FluxKontextImage
from tools.video.kling_video import KlingVideo

ROOT = Path(__file__).resolve().parents[2]


def test_every_required_director_is_shipped():
    manifest = load_pipeline('continuity-reel')
    for name in manifest['required_skills']:
        assert (ROOT / 'skills' / (name + '.md')).is_file(), name
    assert (ROOT / 'skills/creative/narrative-hook-engine.md').is_file()
    assert (ROOT / 'schemas/artifacts/visual_memory.schema.json').is_file()


def test_upstream_schema_capabilities_are_preserved():
    script = load_schema('script')['properties']
    assert 'voice_performance' in script
    assert 'delivery_cues' in script['sections']['items']['properties']
    edit = load_schema('edit_decisions')
    assert 'render_runtime' in edit['required']
    assert 'bespoke' in edit['properties']
    scene = load_schema('scene_plan')['properties']['scenes']['items']['properties']
    assert 'character_scene' in scene['type']['enum']
    assert 'character_actions' in scene
    assert 'visual_entity_id' in scene


@pytest.mark.parametrize('extra', [
    {'operation': 'text_to_video'},
    {'operation': 'image_to_video', 'generate_audio': True},
    {'operation': 'image_to_video', 'end_image_url': 'https://example.test/end.png'},
])
def test_turbo_rejects_unsupported_requests_before_spending(monkeypatch, extra):
    monkeypatch.setenv('FAL_KEY', 'synthetic-test-only')
    with patch('requests.post') as post:
        result = KlingVideo().execute({'prompt': 'synthetic', 'model_variant': 'v2.5-turbo/standard', **extra})
    assert not result.success
    post.assert_not_called()


def test_reference_editor_blocks_missing_reference_before_spending(monkeypatch):
    monkeypatch.setenv('FAL_KEY', 'synthetic-test-only')
    with patch('requests.post') as post:
        result = FluxKontextImage().execute({'prompt':'synthetic'})
    assert not result.success
    post.assert_not_called()
