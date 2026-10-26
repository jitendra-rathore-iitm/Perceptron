import json
import os

from config import HONEY_AFTER_HINT, HONEY_FIRST_TRY, daily_cap

BANK_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "fractions.json")

with open(BANK_PATH, encoding="utf-8") as f:
    bank = json.load(f)

practice_by_level = {int(k): v for k, v in bank["levels"].items()}
all_practice = {q["id"]: q for level in practice_by_level.values() for q in level if q}

HINT_KINDS = ["nudge", "steps", "worked"]

honey_by_device = {}
cycles_by_device = {}
attempts = {}


def attempt_status(device_id, question_id):
    attempt = attempts.get((device_id, question_id))
    if attempt is None:
        return "none"
    return attempt["status"]


def next_question(device_id):
    level = 1
    pool = practice_by_level.get(level, [])
    if not pool:
        return None
    cycle = cycles_by_device.setdefault(device_id, {"index": 0})
    question = pool[cycle["index"] % len(pool)]
    cycle["index"] += 1
    attempts.pop((device_id, question["id"]), None)
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


def fresh_attempt(device_id, question_id):
    return attempts.setdefault(
        (device_id, question_id),
        {"status": "open", "tries": 0, "hint_step": 0, "honey": 0},
    )


def totals_for(device_id):
    return honey_by_device.setdefault(device_id, {"total": 0, "today": 0})


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
    attempt = fresh_attempt(device_id, question_id)
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
        totals["total"] += awarded
        totals["today"] += awarded
        attempt["status"] = "solved"
        attempt["honey"] = awarded
        return {
            "correct": True,
            "honeyAdded": awarded,
            "capped": capped,
            "honeyToday": totals["today"],
            "totalHoney": totals["total"],
        }
    attempt["tries"] += 1
    if attempt["hint_step"] >= 3:
        attempt["status"] = "revealed"
        return reveal_payload(device_id, question_id)
    attempt["hint_step"] += 1
    step_index = attempt["hint_step"] - 1
    return {
        "correct": False,
        "hintStep": attempt["hint_step"],
        "hint": {"kind": HINT_KINDS[step_index], "text": question["hints"][step_index]},
    }


def hint_step(device_id, question_id):
    attempt = fresh_attempt(device_id, question_id)
    if attempt["status"] == "revealed":
        return {"hintStep": 4, "hint": None}
    if attempt["hint_step"] >= 3:
        return {"hintStep": attempt["hint_step"], "hint": None}
    attempt["hint_step"] += 1
    step_index = attempt["hint_step"] - 1
    question = all_practice[question_id]
    return {
        "hintStep": attempt["hint_step"],
        "hint": {"kind": HINT_KINDS[step_index], "text": question["hints"][step_index]},
    }
