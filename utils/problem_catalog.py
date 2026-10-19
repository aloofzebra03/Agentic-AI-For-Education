"""Shared, read-only maths catalog parsing; preserves the API's legacy parser."""

import json
from pathlib import Path


def iter_json_objects(raw_text):
    decoder = json.JSONDecoder()
    index = 0
    while index < len(raw_text):
        if raw_text[index].isspace():
            index += 1
            continue
        try:
            value, index = decoder.raw_decode(raw_text, index)
            yield value
        except json.JSONDecodeError:
            index += 1


def load_problem_records():
    """Return full records and source filenames, in the existing catalog order."""
    root = Path(__file__).resolve().parents[1]
    directory = root / "math_problems_jsons"
    if not directory.exists():
        directory = root / "problems_json"
    records = []
    for path in sorted(directory.glob("*.json")):
        try:
            for value in iter_json_objects(path.read_text(encoding="utf-8")):
                for item in value if isinstance(value, list) else [value]:
                    if not isinstance(item, dict):
                        continue
                    if all(isinstance(item.get(key), str) and item[key].strip()
                           for key in ("problem_id", "topic")):
                        records.append((item, path.name))
        except Exception as error:
            print(f"[WARN] Failed loading problem catalog from {path.name}: {error}")
    return records


def load_problem_catalog():
    return [dict(problem_id=item["problem_id"].strip(), topic=item["topic"].strip(),
                 difficulty=item.get("difficulty")) for item, _ in load_problem_records()]
