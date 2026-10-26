from datetime import date

from flask import Flask, jsonify, request

import os

import questions
import state

app = Flask(__name__)


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
    return jsonify(
        {
            "isNew": is_new,
            "totalHoney": student["total_honey"],
            "honeyToday": student["honey_today"],
            "level": student["level"],
            "dyslexia": bool(student["dyslexia"]),
            "placement": [],
        }
    )


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
