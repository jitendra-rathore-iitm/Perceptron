import os
import sqlite3
from datetime import date, timedelta

DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "perceptron.db"
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    device_id TEXT PRIMARY KEY,
    total_honey INTEGER NOT NULL DEFAULT 0,
    today_date TEXT,
    honey_today INTEGER NOT NULL DEFAULT 0,
    level INTEGER,
    dyslexia INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS placement_answers (
    device_id TEXT NOT NULL,
    question_id TEXT NOT NULL,
    order_index INTEGER NOT NULL,
    outcome TEXT NOT NULL,
    PRIMARY KEY (device_id, question_id)
);
CREATE TABLE IF NOT EXISTS seen_questions (
    device_id TEXT NOT NULL,
    level INTEGER NOT NULL,
    question_id TEXT NOT NULL,
    PRIMARY KEY (device_id, question_id)
);
CREATE TABLE IF NOT EXISTS attempts (
    device_id TEXT NOT NULL,
    question_id TEXT NOT NULL,
    tries INTEGER NOT NULL DEFAULT 0,
    hint_step INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'open',
    PRIMARY KEY (device_id, question_id)
);
"""


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def get_student(device_id):
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM students WHERE device_id = ?", (device_id,)
        ).fetchone()
    return dict(row) if row else None


def create_student(device_id, today):
    with connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO students (device_id, today_date) VALUES (?, ?)",
            (device_id, today),
        )
    return get_student(device_id)


def valid_cap_date(client_today):
    if not isinstance(client_today, str) or len(client_today) != 10:
        return False
    try:
        claimed = date.fromisoformat(client_today)
    except ValueError:
        return False
    server = date.today()
    return server - timedelta(days=1) <= claimed <= server + timedelta(days=1)


def apply_daily_reset(student, client_today):
    stored = student["today_date"]
    if stored == client_today:
        return student
    if not valid_cap_date(client_today):
        return student
    with connect() as conn:
        conn.execute(
            "UPDATE students SET today_date = ?, honey_today = 0 WHERE device_id = ?",
            (client_today, student["device_id"]),
        )
    return get_student(student["device_id"])


def add_honey(device_id, awarded):
    with connect() as conn:
        conn.execute(
            "UPDATE students SET total_honey = total_honey + ?, honey_today = honey_today + ? WHERE device_id = ?",
            (awarded, awarded, device_id),
        )
    return get_student(device_id)


def set_level(device_id, level):
    with connect() as conn:
        conn.execute(
            "UPDATE students SET level = ? WHERE device_id = ?", (level, device_id)
        )


def set_dyslexia(device_id, value):
    with connect() as conn:
        conn.execute(
            "UPDATE students SET dyslexia = ? WHERE device_id = ?",
            (1 if value else 0, device_id),
        )


def reset_device(device_id):
    with connect() as conn:
        for table in ("students", "placement_answers", "seen_questions", "attempts"):
            conn.execute(f"DELETE FROM {table} WHERE device_id = ?", (device_id,))


def get_attempt(device_id, question_id):
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM attempts WHERE device_id = ? AND question_id = ?",
            (device_id, question_id),
        ).fetchone()
    return dict(row) if row else None


def ensure_attempt(device_id, question_id):
    with connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO attempts (device_id, question_id) VALUES (?, ?)",
            (device_id, question_id),
        )
    return get_attempt(device_id, question_id)


def update_attempt(device_id, question_id, tries, hint_step, status):
    with connect() as conn:
        conn.execute(
            "UPDATE attempts SET tries = ?, hint_step = ?, status = ? WHERE device_id = ? AND question_id = ?",
            (tries, hint_step, status, device_id, question_id),
        )


def clear_attempt(device_id, question_id):
    with connect() as conn:
        conn.execute(
            "DELETE FROM attempts WHERE device_id = ? AND question_id = ?",
            (device_id, question_id),
        )


def mark_seen(device_id, level, question_id):
    with connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO seen_questions (device_id, level, question_id) VALUES (?, ?, ?)",
            (device_id, level, question_id),
        )


def seen_ids(device_id, level):
    with connect() as conn:
        rows = conn.execute(
            "SELECT question_id FROM seen_questions WHERE device_id = ? AND level = ?",
            (device_id, level),
        ).fetchall()
    return {row["question_id"] for row in rows}


def clear_seen(device_id, level):
    with connect() as conn:
        conn.execute(
            "DELETE FROM seen_questions WHERE device_id = ? AND level = ?",
            (device_id, level),
        )


def save_placement_answer(device_id, question_id, order_index, outcome):
    with connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO placement_answers (device_id, question_id, order_index, outcome) VALUES (?, ?, ?, ?)",
            (device_id, question_id, order_index, outcome),
        )


def placement_rows(device_id):
    with connect() as conn:
        rows = conn.execute(
            "SELECT question_id, order_index, outcome FROM placement_answers WHERE device_id = ? ORDER BY order_index",
            (device_id,),
        ).fetchall()
    return [dict(row) for row in rows]


def clear_placement(device_id):
    with connect() as conn:
        conn.execute(
            "DELETE FROM placement_answers WHERE device_id = ?", (device_id,)
        )
