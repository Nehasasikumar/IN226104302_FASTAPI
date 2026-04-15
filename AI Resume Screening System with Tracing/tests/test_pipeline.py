import json
from pathlib import Path

from run_local import run_all


def test_run_local_creates_results(tmp_path):
    # run pipeline which writes results.json in project directory
    base = Path(__file__).resolve().parents[1]
    run_all()
    out = base / "results.json"
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "strong" in data and "average" in data and "weak" in data
