import json
import os

from config import HONEY_FIRST_TRY, daily_cap

BANK_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "fractions.json")

with open(BANK_PATH, encoding="utf-8") as f:
    bank = json.load(f)

practice_by_level = {int(k): v for k, v in bank["levels"].items()}
all_practice = {q["id"]: q for level in practice_by_level.values() for q in level if q}

honey_by_device = {}
cycles_by_device = {}
solved_by_device = {}


def next_question(device_id):
    level = 1
    pool = practice_by_level.get(level, [])
    if not pool:
        return None
    cycle = cycles_by_device.setdefault(device_id, {"index": 0})
    question = pool[cycle["index"] % len(pool)]
    cycle["index"] += 1
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


def is_solved(device_id, question_id):
    return (device_id, question_id) in solved_by_device


def grade(device_id, question_id, selected):
    question = all_practice[question_id]
    totals = honey_by_device.setdefault(device_id, {"total": 0, "today": 0})
    if selected == question["correct"]:
        awarded = HONEY_FIRST_TRY
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
        solved_by_device[(device_id, question_id)] = awarded
        return {
            "correct": True,
            "honeyAdded": awarded,
            "capped": capped,
            "honeyToday": totals["today"],
            "totalHoney": totals["total"],
        }
    return {"correct": False, "hintStep": 0}
