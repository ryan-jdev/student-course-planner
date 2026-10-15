# Student Course Planner (Flask + SQLite)

A full-stack web application that helps students plan their weekly schedule by adding courses and automatically detecting time conflicts.

## Features
- Add and delete courses
- Server-side validation for time format
- Conflict detection (prevents overlapping courses on the same day)
- Clean UI with flash messages (success/error)

## Tech Stack
- Python
- Flask
- SQLite
- HTML/CSS

## Time Format
Supports 24-hour format (recommended): `HH:MM-HH:MM`  
Example: `16:00-18:00`

## Run Locally
```bash
pip install -r requirements.txt
python app.py
