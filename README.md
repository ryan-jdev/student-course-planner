# Student Course Planner

A Python command-line application that helps students organize their course schedules and avoid scheduling conflicts.

## Features

- **Add Courses:** Enter a course name, day, start time, and end time.
- **View Courses:** Display saved courses in a numbered list.
- **Delete Courses:** Remove courses from the schedule.
- **Time Validation:** Validate time inputs using the 24-hour `HH:MM` format.
- **Conflict Detection:** Check for overlapping courses scheduled on the same day.
- **Data Persistence:** Save courses to a text file so they remain available after restarting the program.
- **Input Validation:** Prevent empty course details, invalid times, and invalid course selections.

## Technologies Used

- Python
- File Handling
- Lists and Dictionaries
- Functions
- Input Validation
- Basic Scheduling Logic

## Requirements

- Python 3 installed on your computer.

No external libraries are required.

## How to Run

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Run the following command:

   ```bash
   python app.py
   ```

4. Follow the on-screen menu to add, view, or delete courses.

## Data Storage

Course information is stored locally in a file named `courses.txt`. The program loads previously saved courses when it starts and updates the file when courses are added or deleted.

## What I Learned

Through this project, I practiced organizing a Python program into functions, working with lists and dictionaries, validating user input, comparing time intervals, detecting scheduling conflicts, and saving data using file handling.
