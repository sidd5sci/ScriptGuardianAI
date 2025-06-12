from pathlib import Path
from subprocess import run, PIPE

def test_cli_smoke(tmp_path: Path):
    src = Path(__file__).parents[1] / "examples"
    out = tmp_path / "scan.sarif.json"
    cp = run(
        ["llm-secscan", str(src), "--sarif", str(out)],
        stdout=PIPE, stderr=PIPE, text=True,
    )
    assert cp.returncode == 0, cp.stderr
    assert out.exists() and out.stat().st_size > 50
