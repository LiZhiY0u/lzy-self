"""Read-only structural checks. Does not execute behavioral test prompts."""
import json
import re
from pathlib import Path

project = Path(__file__).resolve().parent.parent
suite = json.loads((project / "skill-tests/cases.json").read_text(encoding="utf-8"))
skill_root = project / "lzy-self"
skill = (skill_root / "SKILL.md").read_text(encoding="utf-8")
match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", skill, re.S)
assert match, "Missing frontmatter"
fields = dict(line.split(": ", 1) for line in match.group(1).splitlines())
assert set(fields) == {"name", "description"}, "Unexpected frontmatter"
assert fields["name"] == suite["skill_name"] == skill_root.name
assert re.fullmatch(r"[a-z0-9-]{1,64}", fields["name"])
assert 0 < len(fields["description"]) < 1024
for link in re.findall(r"\]\((references/[^)]+)\)", skill):
    assert (skill_root / link).is_file(), f"Missing reference: {link}"
expected = {f"R{i:02}" for i in range(1, 13)} | {f"H{i:02}" for i in range(1, 4)} | {f"S{i:02}" for i in range(1, 4)}
assert set(suite["rules"]) == expected, "Unexpected rule registry"
ids, covered = set(), set()
for case in suite["cases"]:
    assert case["id"] not in ids, "Duplicate ID"
    ids.add(case["id"])
    assert case["prompt"] and case["must"] and case["must_not"]
    assert isinstance(case["critical"], bool)
    assert case["rules"] and set(case["rules"]) <= expected
    covered.update(case["rules"])
    assert case["status"] == "not_run", "This draft expects unexecuted cases"
    assert all(case[field] is None for field in ("actual_output", "evidence", "judgment"))
assert expected == covered, f"Missing coverage: {expected - covered}"
record = (project / "skill-tests/results.md").read_text(encoding="utf-8")
assert all(f"| {case_id} |" in record for case_id in ids), "Missing result row"
print(f"STRUCTURE PASS: {len(ids)} cases cover {len(covered)}/{len(expected)} registered rule groups.")
print(f"Critical cases: {sum(case['critical'] for case in suite['cases'])}")
print("STRUCTURE ONLY: behavioral evidence is recorded separately in results.md and run reports.")
