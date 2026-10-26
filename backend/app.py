from datetime import date

from flask import Flask, jsonify, request

import os

import questions
import state

app = Flask(__name__)

_counts = questions.bank_counts()
print(
    f"Fraction bank: {_counts['placement']} placement + {_counts['practice']} practice questions "
    f"(L1: {_counts['levels'].get(1, 0)}, L2: {_counts['levels'].get(2, 0)}, L3: {_counts['levels'].get(3, 0)})",
    flush=True,
)
if _counts["placement"] < 6 or any(_counts["levels"].get(level, 0) < 8 for level in (1, 2, 3)):
    print("WARNING: question bank is below the planned 6 + 8-per-level minimum.")


def error(code, description, status):
    return jsonify({"error": {"code": code, "description": description}}), status


def require_student(body_device_id):
    if not isinstance(body_device_id, str) or not body_device_id.strip():
        return None, error("bad_request", "Missing deviceId.", 400)
    device_id = body_device_id.strip()
    student = state.get_student(device_id)
    if student is None:
        return None, error("unknown_device", "We don't know this device. Refresh to start fresh.", 404)
    return (device_id, student), None


@app.errorhandler(Exception)
def server_error(exc):
    return error("server_error", "Something went wrong on our side. Try again.", 500)


@app.post("/api/session")
def session():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return error("bad_request", "Send JSON like {deviceId, today}.", 400)
    device_id = body.get("deviceId", "")
    if not isinstance(device_id, str) or not device_id.strip():
        return error("bad_request", "Missing deviceId.", 400)
    device_id = device_id.strip()
    claimed = body.get("today")
    today_valid = state.valid_cap_date(claimed)
    existing = state.get_student(device_id)
    is_new = existing is None
    if is_new:
        start_date = claimed if today_valid else date.today().isoformat()
        student = state.create_student(device_id, start_date)
    else:
        student = existing
        if today_valid:
            student = state.apply_daily_reset(student, claimed)
    rows = state.placement_rows(device_id)
    finished = student["level"] is not None
    placement = [] if finished else [
        {
            "questionId": row["question_id"],
            "order": row["order_index"],
            "outcome": row["outcome"],
        }
        for row in rows
    ]
    return jsonify(
        {
            "isNew": is_new,
            "totalHoney": student["total_honey"],
            "honeyToday": student["honey_today"],
            "level": student["level"],
            "dyslexia": bool(student["dyslexia"]),
            "placement": placement,
        }
    )


@app.get("/api/placement/questions")
def placement_questions():
    device_id = request.args.get("deviceId", "").strip()
    found, err = require_student(device_id)
    if err:
        return err
    return jsonify({"questions": questions.placement_list()})


@app.post("/api/placement/answer")
def placement_answer():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return error("bad_request", "Send JSON like {deviceId, questionId, selected}.", 400)
    found, err = require_student(body.get("deviceId"))
    if err:
        return err
    device_id = found[0]
    question_id = body.get("questionId", "")
    selected = body.get("selected")
    if not isinstance(question_id, str) or not question_id.strip():
        return error("bad_request", "Missing questionId.", 400)
    question_id = question_id.strip()
    if question_id not in questions.placement_by_id:
        return error("unknown_question", "That placement question does not exist.", 404)
    if selected is not None:
        count = len(questions.placement_by_id[question_id]["options"])
        ok = isinstance(selected, int) and not isinstance(selected, bool) and 0 <= selected < count
        if not ok:
            return error("invalid_selection", "Pick one of the four answers or skip.", 400)
    rows = state.placement_rows(device_id)
    already = {row["question_id"] for row in rows}
    if question_id not in already:
        outcome = questions.placement_outcome(question_id, selected)
        state.save_placement_answer(device_id, question_id, questions.placement_by_id[question_id]["order"], outcome)
        rows = state.placement_rows(device_id)
    if len(rows) < 6:
        return jsonify({"done": False})
    placed = questions.placed_level(rows)
    state.set_level(device_id, placed)
    return jsonify({"done": True, "placedLevel": placed})


@app.post("/api/reset")
def reset():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return error("bad_request", "Send JSON like {deviceId}.", 400)
    device_id = body.get("deviceId", "")
    if not isinstance(device_id, str) or not device_id.strip():
        return error("bad_request", "Missing deviceId.", 400)
    state.reset_device(device_id.strip())
    return jsonify({"isNew": True})


@app.get("/api/practice/question")
def practice_question():
    device_id = request.args.get("deviceId", "").strip()
    found, err = require_student(device_id)
    if err:
        return err
    student = state.get_student(device_id)
    question = questions.next_question(device_id, student["level"] or 1)
    if question is None:
        return error("unknown_question", "No questions are available right now.", 404)
    return jsonify(question)


@app.post("/api/check")
def check():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return error("bad_request", "Send JSON like {deviceId, questionId, selected}.", 400)
    found, err = require_student(body.get("deviceId"))
    if err:
        return err
    device_id = found[0]
    question_id = body.get("questionId", "")
    selected = body.get("selected")
    if not isinstance(question_id, str) or not question_id.strip():
        return error("bad_request", "Missing questionId.", 400)
    try:
        count = questions.option_count(question_id)
    except KeyError:
        return error("unknown_question", "That question does not exist.", 404)
    selection_ok = isinstance(selected, int) and not isinstance(selected, bool) and 0 <= selected < int(count)
    if not selection_ok:
        return error("invalid_selection", "Pick one of the four answers before checking.", 400)
    question_id = question_id.strip()
    status = questions.attempt_status(device_id, question_id)
    if status == "solved":
        totals = questions.totals_for(device_id)
        return jsonify(
            {
                "correct": True,
                "duplicate": True,
                "honeyAdded": 0,
                "honeyToday": totals["today"],
                "totalHoney": totals["total"],
            }
        )
    if status == "revealed":
        return jsonify(questions.reveal_payload(device_id, question_id))
    return jsonify(questions.grade(device_id, question_id, selected))


@app.post("/api/hint")
def hint():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return error("bad_request", "Send JSON like {deviceId, questionId}.", 400)
    found, err = require_student(body.get("deviceId"))
    if err:
        return err
    device_id = found[0]
    question_id = (body.get("questionId") or "").strip()
    if not question_id:
        return error("bad_request", "Missing questionId.", 400)
    try:
        questions.option_count(question_id)
    except KeyError:
        return error("unknown_question", "That question does not exist.", 404)
    return jsonify(questions.hint_step(device_id, question_id))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
