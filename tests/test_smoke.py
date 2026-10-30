"""Smoke tests for CognitiveGrid. They don't need a GEMINI_API_KEY."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.pop("GEMINI_API_KEY", None)  # force zero-config / simulator path


def test_index_html_exists_and_has_title():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "<html" in html.lower()
    assert "<title" in html.lower()


def test_agents_module_imports():
    import agents  # noqa: F401


def test_server_imports_and_has_orchestrate_route():
    from server import app

    paths = {getattr(r, "path", None) for r in app.routes}
    assert "/api/orchestrate" in paths


def test_server_serves_ui():
    from fastapi.testclient import TestClient
    from server import app

    client = TestClient(app)
    res = client.get("/")
    assert res.status_code == 200
    assert "html" in res.text.lower()
