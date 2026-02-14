"""
Student Course Planner
A Flask-based web application that allows users to add, view,
and delete courses stored in an SQLite database.

Technologies:
- Python
- Flask
- SQLite
"""

from flask import Flask, render_template, request, redirect, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "dev"

# Determine absolute path to database file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Hompage route: displays all saved courses
@app.route("/")
def index():
    conn = get_db_connection()
    courses = conn.execute("SELECT * FROM courses").fetchall()
    print("COURSES COUNT:", len(courses))
    conn.close()
    return render_template("index.html", courses=courses)

def parse_time_range(time_str: str):
    """
    Expects 'HH:MM-HH:MM' (24-hour). Returns (start_minutes, end_minutes).
    Raises ValueError if invalid.
    """
    time_str = time_str.strip()
    if "-" not in time_str:
        raise ValueError("Time must be in format HH:MM-HH:MM")

    start_s, end_s = [p.strip() for p in time_str.split("-", 1)]

    def to_minutes(hhmm: str) -> int:
        hh, mm = hhmm.split(":")
        h = int(hh)
        m = int(mm)
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError("Invalid time value")
        return h * 60 + m

    start = to_minutes(start_s)
    end = to_minutes(end_s)
    if end <= start:
        raise ValueError("End time must be after start time")
    return start, end


def overlaps(a_start, a_end, b_start, b_end) -> bool:
    # True if time ranges overlap (not counting touching endpoints as overlap)
    return a_start < b_end and b_start < a_end


@app.route("/add", methods=["POST"])
def add_course():
    name = request.form["name"].strip()
    day = request.form["day"].strip()
    time = request.form["time"].strip()

    # Validate time format
    try:
        new_start, new_end = parse_time_range(time)
    except ValueError as e:
        flash(f"Invalid time: {e}", "error")
        return redirect("/")

    conn = get_db_connection()

    # Fetch existing courses on the same day
    existing = conn.execute(
        "SELECT name, time FROM courses WHERE day = ?",
        (day,),
    ).fetchall()

    # Check for overlaps
    for row in existing:
        try:
            old_start, old_end = parse_time_range(row["time"])
        except Exception:
            continue

        if overlaps(new_start, new_end, old_start, old_end):
            conn.close()
            flash(f"Conflict: overlaps with {row['name']} ({day} {row['time']})", "error")
            return redirect("/")

    # No conflict: insert
    conn.execute(
        "INSERT INTO courses (name, day, time) VALUES (?, ?, ?)",
        (name, day, time),
    )
    conn.commit()
    conn.close()

    flash("Course added!", "success")
    return redirect("/")

# Deletes a course by their ID
@app.route('/delete/<int:id>')
def delete_course(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM courses WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            day TEXT,
            time TEXT
        )
    ''')
    conn.close()
    app.run(debug=True)