import json
from pathlib import Path
import argparse


def load_script_lines(script_text: str) -> list[str]:
    """Strip markers like <#N#> and return plain lines."""
    lines = []
    for line in script_text.splitlines():
        if "<#" in line and "#>" in line:
            try:
                clean = line.split("#>", 1)[1].strip()
                lines.append(clean)
            except IndexError:
                lines.append(line.strip())
        else:
            lines.append(line.strip())
    return lines


def validate_findings(script_text: str, findings: list[dict]) -> list[dict]:
    """Return a list of mismatches between finding.statement and actual line content."""
    mismatches = []
    script_lines = load_script_lines(script_text)

    for f in findings:
        lineno = f.get("line")
        expected = f.get("statement", "").strip()
        if not isinstance(lineno, int) or lineno < 1 or lineno > len(script_lines):
            mismatches.append({
                "line": lineno,
                "error": "Invalid or out-of-range line number"
            })
            continue

        actual = script_lines[lineno - 1].strip()
        if actual != expected:
            mismatches.append({
                "line": lineno,
                "expected": actual,
                "found": expected
            })

    return mismatches


def main():
    parser = argparse.ArgumentParser(description="Validate LLM findings against script lines")
    parser.add_argument("--script", required=True, help="Script file with <#N#> markers")
    parser.add_argument("--json", required=True, help="LLM output JSON file")

    args = parser.parse_args()

    script_text = Path(args.script).read_text(encoding="utf-8")
    findings_json = json.loads(Path(args.json).read_text(encoding="utf-8"))

    findings = findings_json.get("findings", [])
    mismatches = validate_findings(script_text, findings)

    if not mismatches:
        print("✅ All findings match the script line numbers.")
    else:
        print(f"❌ Found {len(mismatches)} mismatches:")
        for m in mismatches:
            if "error" in m:
                print(f"  Line {m['line']}: {m['error']}")
            else:
                print(f"  Line {m['line']}:\n    expected: {m['expected']}\n    found:    {m['found']}")


if __name__ == "__main__":
    main()
