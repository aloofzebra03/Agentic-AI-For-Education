"""Small in-memory search over existing lessons. No LLM, sessions or database."""

import json
import logging
import random
import re
import unicodedata
from difflib import SequenceMatcher
from functools import lru_cache
from pathlib import Path

from api_servers.schemas import SearchAction, SearchResponse, SearchResult
from utils.problem_catalog import load_problem_records

LOGGER = logging.getLogger(__name__)


def normalize(text):
    return " ".join(re.findall(r"\w+", unicodedata.normalize("NFKC", str(text)).casefold()))


def preview(text):
    # Catalog snippets only: never index or return final answers/solution steps.
    return " ".join(str(text or "").split())[:260]


@lru_cache(maxsize=1)
def search_index():
    rows = {}
    root = Path(__file__).resolve().parents[1]
    for path in sorted((root / "science_jsons").glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            for item in data.get("concepts", []):
                title = item.get("concept", item.get("Concept", "")).strip()
                if not title:
                    continue
                key = "science:" + normalize(title)
                chapter = re.search(r"\d+", path.stem)
                result = SearchResult(
                    id=key, subject="science", title=title,
                    description=preview(item.get("description", "")), content_type="topic",
                    chapter=int(chapter[0]) if chapter else None,
                    actions=[SearchAction(type="tutor", concept_title=title), SearchAction(type="doubt")],
                )
                rows[key] = (result, normalize(" ".join(map(str, item.get("key_topics", [])))))
        except (ValueError, TypeError, AttributeError) as error:
            LOGGER.warning("Search skipped science file %s: %s", path.name, type(error).__name__)

    source_problems = {}
    for item, filename in load_problem_records():
        problem_id = item["problem_id"].strip()
        key = "math:" + problem_id.casefold()
        source_problems.setdefault(problem_id.casefold(), item)
        if key in rows or not isinstance(item.get("question"), str) or not item["question"].strip():
            continue
        chapter = re.match(r"p([12])_ch(\d+)_", filename)
        rows[key] = (SearchResult(
            id=key, subject="math", title=item["topic"].strip(),
            description=preview(item["question"]), content_type="problem",
            book_part=int(chapter[1]) if chapter else None,
            chapter=int(chapter[2]) if chapter else None,
            actions=[SearchAction(type="tutor", problem_id=problem_id), SearchAction(type="doubt")],
        ), normalize(item["question"] + " " + " ".join(item.get("required_concepts", []))))

    # This is the same SVG-backed catalog used by the whiteboard API.
    from whiteboard_tutor.catalog import load_whiteboard_concepts
    for record in load_whiteboard_concepts():
        action = SearchAction(type="whiteboard", concept_id=record.concept_id)
        source = record.data.get("source_snapshot", {}).get("problem", {})
        key = ("science:" + normalize(record.title) if record.subject == "science"
               else "math:" + str(record.data.get("source_problem_id", "")).casefold())
        if key in rows:
            result, keywords = rows[key]
            # Maths scenes must match the exact source question AND solution record,
            # not merely a similar title or reused problem ID.
            if record.subject == "math":
                original = source_problems.get(key[5:])
                if original != source:
                    LOGGER.warning("Search omitted mismatched whiteboard action: %s", record.concept_id)
                    continue
            result.actions.insert(-1, action)
        else:
            # Unmapped maths scenes remain standalone lessons (not maths-agent problems).
            key = "whiteboard:" + record.concept_id
            rows[key] = (SearchResult(
                id=key, subject=record.subject, title=record.title,
                description=preview(record.data.get("description", "")),
                content_type="whiteboard_lesson", chapter=record.chapter,
                book_part=record.data.get("source_snapshot", {}).get("book_part"),
                actions=[action, SearchAction(type="doubt")],
            ), normalize(" ".join(record.data.get("key_topics", []))))
    return tuple(rows.values())


def interpret_query(query, subject=None, mode=None, randomize=False):
    text = " ".join(query.casefold().split())
    inferred_mode = "all"
    suffix = re.search(r"\b(whiteboard|manual|tutor|help|doubt)\s*$", text)
    if suffix:
        inferred_mode = {"manual": "tutor", "help": "doubt"}.get(suffix[1], suffix[1])
        text = text[:suffix.start()].strip()
    found = re.search(r"\b(science|maths|mathematics|math)\b", text)
    inferred_subject = "all"
    if found:
        inferred_subject = "science" if found[1] == "science" else "math"
        text = (text[:found.start()] + " " + text[found.end():]).strip()
    if re.search(r"\brandom\b", text):
        randomize = True
        text = re.sub(r"^(?:(?:give|show)\s+)?(?:me\s+)?(?:five\s+|5\s+)?random\s*", "", text)
        text = re.sub(r"\btopics?\s*$", "", text).strip()
    text = normalize(text)
    return text, subject or inferred_subject, mode or inferred_mode, randomize or not text


def match_score(query, result, keywords):
    title = normalize(result.title)
    tokens = query.split()
    if query == title:
        return 1000
    if query in title:
        return 800
    if all(any(word.startswith(token) for word in title.split()) for token in tokens):
        return 700
    searchable = title + " " + keywords + " " + normalize(result.description)
    if all(token in searchable for token in tokens):
        return 500
    # Spelling fallback requires every query word to resemble a title word.
    similarity = min(max((SequenceMatcher(None, token, word).ratio()
                          for word in title.split()), default=0) for token in tokens)
    return int(similarity * 100) if similarity >= .8 else 0


def search_topics(query="", subject=None, mode=None, limit=5, randomize=False):
    query, subject, mode, randomize = interpret_query(query, subject, mode, randomize)
    candidates = []
    spelling_matches = []
    for result, keywords in search_index():
        if subject != "all" and result.subject != subject:
            continue
        if mode != "all" and not any(action.type == mode for action in result.actions):
            continue
        score = match_score(query, result, keywords) if query else 1
        if score:
            target = spelling_matches if query and score < 500 else candidates
            target.append((score, result))
    # Do not pad real matches with approximate, potentially unrelated titles.
    candidates = candidates or spelling_matches
    if randomize:
        selected = random.sample(candidates, min(limit, len(candidates)))
    else:
        selected = sorted(candidates, key=lambda pair: (-pair[0], normalize(pair[1].title), pair[1].id))[:limit]
    return SearchResponse(query=query, subject=subject, mode=mode,
                          selection="random" if randomize else "ranked",
                          total_matches=len(candidates), results=[item for _, item in selected])
