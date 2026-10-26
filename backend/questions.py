import json
import os
import random

import state
from config import HONEY_AFTER_HINT, HONEY_FIRST_TRY, daily_cap

BANK_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "fractions.json")


def valid_question(q):
    return (
        isinstance(q, dict)
        and isinstance(q.get("id"), str)
        and bool(q["id"].strip())
        and isinstance(q.get("level"), int)
        and isinstance(q.get("text"), str)
        and bool(q["text"].strip())
        and isinstance(q.get("options"), list)
        and len(q["options"]) == 4
        and all(isinstance(o, str) and o.strip() for o in q["options"])
        and isinstance(q.get("correct"), int)
        and 0 <= q["correct"] < 4
        and isinstance(q.get("hints"), list)
        and len(q["hints"]) == 3
        and all(isinstance(h, str) and h.strip() for h in q["hints"])
        and isinstance(q.get("explanation"), str)
        and bool(q["explanation"].strip())
    )


def load_bank(path):
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    placement = [
        q
        for q in raw.get("placement", [])
        if valid_question(q) and isinstance(q.get("order"), int)
    ]
    levels = {}
    for key, items in raw.get("levels", {}).items():
        levels[int(key)] = [q for q in items if valid_question(q)]
    return placement, levels


placement_list_raw, practice_by_level = load_bank(BANK_PATH)
placement_by_id = {}
for q in placement_list_raw:
    placement_by_id.setdefault(q["id"], q)
all_practice = {}
for level in practice_by_level.values():
    for q in level:
        all_practice.setdefault(q["id"], q)

HINT_KINDS = ["nudge", "steps", "worked"]


def bank_counts():
    return {
        "placement": len(placement_list_raw),
        "practice": len(all_practice),
        "levels": {k: len(v) for k, v in practice_by_level.items()},
        "skipped": 0,
    }


def placement_list():
    ordered = sorted(placement_list_raw, key=lambda q: q["order"])
    return [
        {
            "id": q["id"],
            "level": q["level"],
            "text": q["text"],
            "options": q["options"],
            "order": q["order"],
        }
        for q in ordered
    ]


def placement_outcome(question_id, selected):
    if selected is None:
        return "skipped"
    return "correct" if selected == placement_by_id[question_id]["correct"] else "wrong"


def placed_level(rows):
    wins = set()
    for row in rows:
        if row["outcome"] == "correct":
            wins.add(placement_by_id[row["question_id"]]["level"])
    for level in (3, 2, 1):
        if level in wins:
            return level
    return 1


def attempt_status(device_id, question_id):
    attempt = state.get_attempt(device_id, question_id)
    if attempt is None:
        return "none"
    return attempt["status"]


def next_question(device_id, level):
    pool = practice_by_level.get(level, [])
    if not pool:
        return None
    seen = state.seen_ids(device_id, level)
    unseen = [q for q in pool if q["id"] not in seen]
    if not unseen:
        state.clear_seen(device_id, level)
        unseen = pool
    question = random.choice(unseen)
    state.mark_seen(device_id, level, question["id"])
    state.clear_attempt(device_id, question["id"])
    return {
        "id": question["id"],
        "level": question["level"],
        "text": question["text"],
        "options": question["options"],
        "hintStep": 0,
    }


def option_count(question_id):
    question = all_practice[question_id]
    return len(question["options"])


def totals_for(device_id):
    student = state.get_student(device_id)
    if student is None:
        return {"total": 0, "today": 0}
    return {"total": student["total_honey"], "today": student["honey_today"]}


def reveal_payload(device_id, question_id):
    question = all_practice[question_id]
    totals = totals_for(device_id)
    return {
        "correct": False,
        "revealed": True,
        "correctOption": question["options"][question["correct"]],
        "explanation": question["explanation"],
        "honeyAdded": 0,
        "honeyToday": totals["today"],
        "totalHoney": totals["total"],
    }


def grade(device_id, question_id, selected):
    question = all_practice[question_id]
    attempt = state.ensure_attempt(device_id, question_id)
    totals = totals_for(device_id)
    if selected == question["correct"]:
        awarded = HONEY_FIRST_TRY if attempt["tries"] == 0 else HONEY_AFTER_HINT
        capped = False
        remaining = daily_cap() - totals["today"]
        if remaining <= 0:
            awarded = 0
            capped = True
        elif awarded > remaining:
            awarded = remaining
            capped = True
        if awarded:
            student = state.add_honey(device_id, awarded)
            totals = {"total": student["total_honey"], "today": student["honey_today"]}
        state.update_attempt(
            device_id, question_id, attempt["tries"], attempt["hint_step"], "solved"
        )
        return {
            "correct": True,
            "honeyAdded": awarded,
            "capped": capped,
            "honeyToday": totals["today"],
            "totalHoney": totals["total"],
        }
    tries = attempt["tries"] + 1
    if attempt["hint_step"] >= 3:
        state.update_attempt(device_id, question_id, tries, attempt["hint_step"], "revealed")
        return reveal_payload(device_id, question_id)
    hint_step = attempt["hint_step"] + 1
    state.update_attempt(device_id, question_id, tries, hint_step, "open")
    step_index = hint_step - 1
    return {
        "correct": False,
        "hintStep": hint_step,
        "hint": {"kind": HINT_KINDS[step_index], "text": question["hints"][step_index]},
    }


def hint_step(device_id, question_id):
    attempt = state.ensure_attempt(device_id, question_id)
    if attempt["status"] == "revealed":
        return {"hintStep": 4, "hint": None}
    if attempt["hint_step"] >= 3:
        return {"hintStep": attempt["hint_step"], "hint": None}
    hint_step = attempt["hint_step"] + 1
    state.update_attempt(
        device_id, question_id, attempt["tries"], hint_step, attempt["status"]
    )
    step_index = hint_step - 1
    question = all_practice[question_id]
    return {
        "hintStep": hint_step,
        "hint": {"kind": HINT_KINDS[step_index], "text": question["hints"][step_index]},
    }
