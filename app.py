"""
Student Course Planner

A Python application for managing course schedules.

Features:
- Add, view, and delete courses
- Display courses using numbered lists
- Store course start and end times
- Check for scheduling conflicts
- Validate course deletion input
"""

# Array that will store all courses currently loaded into program
courses = []

# Saves all courses to a text file called courses.txt so they can be loaded next time
def save_courses():
    file = open("courses.txt", "w")

    # Write each courses information on a seperate line
    for course in courses:
        file.write(course["name"] + "," + course["day"] + "," + course["startTime"] + "," + course["endTime"] + "\n")

    file.close()

# Check whether a time follows the valid HH:MM format (Error handling)
def valid_time(time):
    parts = time.split(":")

    # A valid time must contain exactly two parts
    if len(parts) != 2:
        return False

    if not parts[0].isdigit() or not parts[1].isdigit():
        return False

    # Convert the hours and minutes from strings to integers
    hours = int(parts[0])
    minutes = int(parts[1])

    # Check that the hours are between 0 and 23
    if hours < 0 or hours > 23:
        return False

    # Check that the minutes are between 0 and 59
    if minutes < 0 or minutes > 59:
        return False

    return True

# Loads previously saved courses when the program starts
def load_courses():
    try:
        file = open("courses.txt", "r")

        # Read the file one course at a time
        for line in file:
            parts = line.strip().split(",")

            # Rebuild the course dictionary
            course = {
                "name": parts[0],
                "day": parts[1],
                "startTime": parts[2],
                "endTime": parts[3]
            }

            courses.append(course)

        file.close()

    # If no saved file exists, start with an empty course list
    except FileNotFoundError:
        pass

# Load saved courses before displaying the menu
load_courses()

# Keep displaying the menu until the user chooses to exit
while True:
    print("\nStudent Course Planner")
    print("1. Add Course")
    print("2. View Courses")
    print("3. Delete Courses")
    print("4. Exit")

    choice = input("Choose an option: ")

    # Option 1: Add a new course
    if choice == "1":
        name = input("Course name: ")
        day = input("Day of the week: ")
        time = input("Start Time (24 Hour Clock): ")
        endTime = input("End time (24 Hour Clock): ")

        # Prevent courses from having an empty name or day
        if name.strip() == "" or day.strip() == "":
            print("Course name and day cannot be empty.")
            continue

        if not valid_time(time) or not valid_time(endTime):
            print("Invalid time. Please use HH:MM format.")
            continue

        conflict = False

        # Convert the start and end times into minutes after 12 am
        start_parts = time.split(":")
        end_parts = endTime.split(":")

        start_minutes = int(start_parts[0]) * 60 + int(start_parts[1])
        end_minutes = int(end_parts[0]) * 60 + int(end_parts[1])

        # Ensure the end time is later than the start time
        if end_minutes <= start_minutes:
            print("End time must be later than start time.")
            continue

        # Boolean to track whether the new course overlaps another course
        conflict = False

        # Compare the new course with existing courses on the same day
        for course in courses:
            if course["day"] == day:
                # Convert the existing course's times into minutes
                existing_start_parts = course["startTime"].split(":")
                existing_end_parts = course["endTime"].split(":")

                existing_start_minutes = int(existing_start_parts[0]) * 60 + int(existing_start_parts[1])
                existing_end_minutes = int(existing_end_parts[0]) * 60 + int(existing_end_parts[1])

                if start_minutes < existing_end_minutes and end_minutes > existing_start_minutes:
                    conflict = True
                    print("Scheduling conflict with", course["name"])

        # Only save the course if no scheduling conflict was found
        if conflict == False:
            course = {
                "name": name,
                "day": day,
                "startTime": time,
                "endTime": endTime
            }

            courses.append(course)
            save_courses()
            print("Course added successfully.")

    # Option 2: Display all saved courses
    elif choice == "2":
        if len(courses) == 0:
            print("\nThere are no courses to display.")
        else:
            # Display each course with a numbered position
            for i in range(len(courses)):
                course = courses[i]
                print(i + 1, "-", course["name"], "-", course["day"], "-", course["startTime"], "-", course["endTime"])

    # Option 3: Delete a course
    elif choice == "3":
        if len(courses) == 0:
            print("There are no courses available to delete.")

        else:
            # Display course names so the user can choose one
            for i in range (len(courses)):
                print(i + 1, "-", courses[i]["name"])

            delete = input("Choose which course to delete: ")

            # Ensuring the selection contains only digits (Error handling)
            if delete.isdigit():
                delete = int(delete)

                if delete >= 1 and delete <= len(courses):
                    courses.pop(delete - 1)
                    # Save the updated list after deletion
                    save_courses()
                    print("Course deleted.")

                else:
                    print("Invalid course number.")

            else:
                print("Please enter a number.")

    # Option 4: Exit the program
    elif choice == "4":
        print("Thank you for using the student course planner!")
        break

    # Handle menu selections that are not 1, 2, 3, or 4 (Error handling)
    else:
        print("Invalid choice, please pick (1-4).")