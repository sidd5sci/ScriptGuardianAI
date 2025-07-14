import re
SINK_RE = re.compile(
    r"\b(Write-Host|Write-Output|Set-Content|Out-File|"
    r"Invoke-RestMethod|Invoke-WebRequest)\b", re.I)

# same regex you provided
SENSITIVE_PLACEHOLDER_RE = re.compile(
    r"^((snmp|([0-9]+\.)?snmptrap)\.(community|privtoken|authtoken))$"
    r"|.*credential$|.*password$|(\S+((\.pass)|(\.auth)|(\.key)))$"
    r"|(aws\.accesskey)$|(azure\.secretkey)$|(saas\.(privatekey|secretkey))$"
    r"|(gcp\.serviceaccountkey)$|(collector\.sqs\.(awsaccesskey|awssecretkey))$"
    r"|(gcccli.accesskey)$", re.I)

def quick_flow_scan(code: str):
    """Return {'sens_vars': set[str], 'sus_lines': list[(lineno,str)]}."""
    sens_vars = set()
    lines = code.splitlines()
    for idx, line in enumerate(lines, 1):
        # detect hard-coded sensitive placeholders
        if m := re.search(r"\$(\w+)\s*=\s*['\"]##([^#]+)##['\"]", line):
            var, placeholder = "$" + m.group(1), m.group(2)
            if SENSITIVE_PLACEHOLDER_RE.match(placeholder):
                sens_vars.add(var)

        # copy propagation  e.g. $b = $a
        if m := re.search(r"\$(\w+)\s*=\s*\$(\w+)", line):
            tgt, src = "$"+m.group(1), "$"+m.group(2)
            if src in sens_vars:
                sens_vars.add(tgt)

    # leak sinks
    sus_lines = []
    for idx, line in enumerate(lines, 1):
        if not SINK_RE.search(line):
            continue
        for v in sens_vars:
            if v in line:
                sus_lines.append((idx, line.strip()))
                break

    return {"sens_vars": sens_vars, "sus_lines": sus_lines}
