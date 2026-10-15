
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

courses = []

def save_courses():
    file = open("courses.txt", "w")

    for course in courses:
        file.write(course["name"] + "," + course["day"] + "," + course["startTime"] + "," + course["endTime"] + "\n")

    file.close()

def valid_time(time):
    parts = time.split(":")

    if len(parts) != 2:
        return False

    if not parts[0].isdigit() or not parts[1].isdigit():
        return False

    hours = int(parts[0])
    minutes = int(parts[1])

    if hours < 0 or hours > 23:
        return False

    if minutes < 0 or minutes > 59:
        return False

    return True

def load_courses():
    try:
        file = open("courses.txt", "r")

        for line in file:
            parts = line.strip().split(",")

            course = {
                "name": parts[0],
                "day": parts[1],
                "startTime": parts[2],
                "endTime": parts[3]
            }

            courses.append(course)

        file.close()

    except FileNotFoundError:
        pass

# Load saved courses when program starts
load_courses()

while True:
    print("\nStudent Course Planner")
    print("1. Add Course")
    print("2. View Courses")
    print("3. Delete Courses")
    print("4. Exit")

    choice = input("Choose an option: ")


    if choice == "1":
        name = input("Course name: ")
        day = input("Day of the week: ")
        time = input("Start Time (24 Hour Clock): ")
        endTime = input("End time (24 Hour Clock): ")

        if name.strip() == "" or day.strip() == "":
            print("Course name and day cannot be empty.")
            continue

        if not valid_time(time) or not valid_time(endTime):
            print("Invalid time. Please use HH:MM format.")
            continue

        conflict = False

        start_parts = time.split(":")
        end_parts = endTime.split(":")

        start_minutes = int(start_parts[0]) * 60 + int(start_parts[1])
        end_minutes = int(end_parts[0]) * 60 + int(end_parts[1])

        if end_minutes <= start_minutes:
            print("End time must be later than start time.")
            continue

        conflict = False

        for course in courses:
            if course["day"] == day:
                existing_start_parts = course["startTime"].split(":")
                existing_end_parts = course["endTime"].split(":")

                existing_start_minutes = int(existing_start_parts[0]) * 60 + int(existing_start_parts[1])
                existing_end_minutes = int(existing_end_parts[0]) * 60 + int(existing_end_parts[1])

                if start_minutes < existing_end_minutes and end_minutes > existing_start_minutes:
                    conflict = True
                    print("Scheduling conflict with", course["name"])


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

    elif choice == "2":
        if len(courses) == 0:
            print("\nThere are no courses to display.")
        else:
            for i in range(len(courses)):
                course = courses[i]
                print(i + 1, "-", course["name"], "-", course["day"], "-", course["startTime"], "-", course["endTime"])

    elif choice == "3":
        if len(courses) == 0:
            print("There are no courses available to delete.")

        else:
            for i in range (len(courses)):
                print(i + 1, "-", courses[i]["name"])

            delete = input("Choose which course to delete: ")

            if delete.isdigit():
                delete = int(delete)

                if delete >= 1 and delete <= len(courses):
                    courses.pop(delete - 1)
                    save_courses()
                    print("Course deleted.")

                else:
                    print("Invalid course number.")

            else:
                print("Please enter a number.")


    elif choice == "4":
        print("Thank you for using the student course planner!")
        break

    else:
        print("Invalid choice, please pick (1-4).")