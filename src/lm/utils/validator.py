import json
from typing import Union

class ScriptFindingValidator():  
    @staticmethod
    def validate_from_strings(script_text: str, 
                          llm_json: Union[str, dict]) -> list[dict]:
        """
        Parameters
        ----------
        script_text : str
            Full original script (may include <#N#> markers).
        llm_json_text : str
            JSON string returned by the LLM (single-object spec).

        Returns
        -------
        List[dict]
            Same mismatch dicts as .validate() – empty list ⇒ all good.
        """
        def strip_markers(code: str) -> list[str]:
            lines = []
            for line in code.splitlines():
                if "<#" in line and "#>" in line:
                    try:
                        lines.append(line.split("#>", 1)[1])
                    except IndexError:
                        lines.append(line)
                else:
                    lines.append(line)
            return lines

        script_lines = strip_markers(script_text)
        total_lines  = len(script_lines)

        if isinstance(llm_json, dict):
            data = llm_json
        else:
            try:
                data = json.loads(llm_json)
            except json.JSONDecodeError as exc:
                raise ValueError("Invalid LLM JSON text") from exc

        findings = data.get("findings", [])
        mismatches: list[dict] = []
        for f in findings:
            lineno = f.get("line")
            stmt   = (f.get("statement") or "").strip()

            if not isinstance(lineno, int) or lineno < 1 or lineno > total_lines:
                mismatches.append({"line": lineno, "error": "line out of range"})
                continue

            actual = script_lines[lineno - 1].strip()
            if actual != stmt:
                mismatches.append(
                    {"line": lineno, "expected": actual, "found": stmt}
                )

        return mismatches

# Uses
# from validator import ScriptFindingValidator as VF

# script = """<#1#> $pass='secret'
# <#2#> Write-Host $pass
# """

# llm_resp = """
# {
#   "script":"vulnerable",
#   "score":9,
#   "findings":[
#      {"line":2,
#       "severity":"Error",
#       "statement":"Write-Host $pass",
#       "reason":"Sensitive var leaked",
#       "recommendation":"Remove",
#       "code_suggestion":"Write-Host 'done'"}
#   ]
# }
# """

# diffs = VF.validate_from_strings(script, llm_resp)
# print("mismatches:", diffs)