from flask import Flask, jsonify, request

import os

import questions

app = Flask(__name__)


def error(code, description, status):
    return jsonify({"error": {"code": code, "description": description}}), status


@app.get("/api/practice/question")
def practice_question():
    device_id = request.args.get("deviceId", "").strip()
    if not device_id:
        return error("bad_request", "Missing deviceId.", 400)
    question = questions.next_question(device_id)
    if question is None:
        return error("unknown_question", "No questions are available right now.", 404)
    return jsonify(question)


@app.post("/api/check")
def check():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return error("bad_request", "Send JSON like {deviceId, questionId, selected}.", 400)
    device_id = body.get("deviceId", "")
    question_id = body.get("questionId", "")
    selected = body.get("selected")
    if not isinstance(device_id, str) or not device_id.strip():
        return error("bad_request", "Missing deviceId.", 400)
    if not isinstance(question_id, str) or not question_id.strip():
        return error("bad_request", "Missing questionId.", 400)
    try:
        count = questions.option_count(question_id)
    except KeyError:
        return error("unknown_question", "That question does not exist.", 404)
    selection_ok = isinstance(selected, int) and not isinstance(selected, bool) and 0 <= selected < int(count)
    if not selection_ok:
        return error("invalid_selection", "Pick one of the four answers before checking.", 400)
    device_id = device_id.strip()
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
    device_id = (body.get("deviceId") or "").strip()
    question_id = (body.get("questionId") or "").strip()
    if not device_id:
        return error("bad_request", "Missing deviceId.", 400)
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

