from flask import Flask, jsonify, request

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
    if questions.is_solved(device_id, question_id):
        totals = questions.honey_by_device.get(device_id, {"total": 0, "today": 0})
        return jsonify(
            {
                "correct": True,
                "duplicate": True,
                "honeyAdded": 0,
                "honeyToday": totals["today"],
                "totalHoney": totals["total"],
            }
        )
    return jsonify(questions.grade(device_id, question_id, selected))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
