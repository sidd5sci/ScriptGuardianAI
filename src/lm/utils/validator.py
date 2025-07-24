import json
from typing import List, Dict, Any, Union


class ScriptFindingValidator:
    """
    • validate() - strict check, like before
    • realign_findings() - returns a *corrected* findings list
      (moves a finding up/down ±N lines until the statement matches).
    """

    MAX_SHIFT = 3              # try ±3 lines when realigning

    # ------------------------------------------------------------------ #
    # public helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def strip_markers(code: str) -> List[str]:
        out = []
        for line in code.splitlines():
            if "<#" in line and "#>" in line:
                try:
                    out.append(line.split("#>", 1)[1])
                except IndexError:
                    out.append(line)
            else:
                out.append(line)
        return out

    @classmethod
    def validate_from_strings(cls,
                              script_text: str,
                              llm_json: Union[str, Dict[str, Any]]
                              ) -> List[Dict[str, Any]]:
        """Strict mismatch list (same as before)."""
        script_lines = cls.strip_markers(script_text)
        data = llm_json if isinstance(llm_json, dict) else json.loads(llm_json)
        findings = data.get("findings", [])

        problems = []
        for f in findings:
            ok, msg = cls._compare_line(script_lines, f)
            if not ok:
                problems.append(msg)
        return problems

    @classmethod
    def realign_findings(cls,
                         script_text: str,
                         llm_json: Dict[str, Any]) -> Dict[str, Any]:
        """Adjust mis-numbered findings in-place; return the new JSON."""
        script_lines = cls.strip_markers(script_text)
        total = len(script_lines)

        for f in llm_json.get("findings", []):
            lineno = f.get("line", -1)
            stmt   = (f.get("statement") or "").strip()
            if not stmt:
                continue

            if 1 <= lineno <= total and script_lines[lineno - 1].strip() == stmt:
                continue  # already correct

            # search upward & downward
            for shift in range(1, cls.MAX_SHIFT + 1):
                up   = lineno - shift
                down = lineno + shift

                if 1 <= up <= total and script_lines[up - 1].strip() == stmt:
                    f["line"] = up
                    break

                if 1 <= down <= total and script_lines[down - 1].strip() == stmt:
                    f["line"] = down
                    break
        return llm_json

    # ------------------------------------------------------------------ #
    # internal
    # ------------------------------------------------------------------ #
    @staticmethod
    def _compare_line(src_lines: List[str], finding: Dict[str, Any]):
        lineno = finding.get("line")
        stmt   = (finding.get("statement") or "").strip()
        if not isinstance(lineno, int) or lineno < 1 or lineno > len(src_lines):
            return False, {"line": lineno, "error": "line out of range"}
        actual = src_lines[lineno - 1].strip()
        if actual != stmt:
            return False, {"line": lineno, "expected": actual, "found": stmt}
        return True, None
