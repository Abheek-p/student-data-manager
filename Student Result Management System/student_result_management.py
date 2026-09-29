"""
Student Result Management System
A beginner-friendly CLI project using JSON file storage.
"""

import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "students.json"

SUBJECTS = ["Python", "Mathematics", "Physics", "English", "Computer Fundamentals"]


def load_students():
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_students(students):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)


def calculate_result(marks):
    total = sum(marks.values())
    percentage = total / len(SUBJECTS)

    if any(mark < 35 for mark in marks.values()):
        status = "FAIL"
    elif percentage >= 90:
        status = "A+"
    elif percentage >= 80:
        status = "A"
    elif percentage >= 70:
        status = "B+"
    elif percentage >= 60:
        status = "B"
    elif percentage >= 50:
        status = "C"
    elif percentage >= 35:
        status = "D"
    else:
        status = "FAIL"

    return total, round(percentage, 2), status


def find_student(students, roll_no):
    return next(
        (student for student in students if student["roll_no"].lower() == roll_no.lower()),
        None,
    )


def read_mark(subject):
    while True:
        try:
            mark = float(input(f"Enter marks for {subject} (0-100): "))
            if 0 <= mark <= 100:
                return mark
            print("Marks must be between 0 and 100.")
        except ValueError:
            print("Please enter a valid number.")


def add_student(students):
    print("\n--- Add Student ---")
    roll_no = input("Roll number: ").strip()

    if not roll_no:
        print("Roll number cannot be empty.")
        return

    if find_student(students, roll_no):
        print("A student with this roll number already exists.")
        return

    name = input("Student name: ").strip()
    course = input("Course/Class: ").strip()

    if not name or not course:
        print("Name and course cannot be empty.")
        return

    marks = {subject: read_mark(subject) for subject in SUBJECTS}
    total, percentage, grade = calculate_result(marks)

    students.append({
        "roll_no": roll_no,
        "name": name,
        "course": course,
        "marks": marks,
        "total": total,
        "percentage": percentage,
        "grade": grade,
    })
    save_students(students)
    print("Student result added successfully.")


def display_student(student):
    print("\n" + "=" * 55)
    print(f"Roll No   : {student['roll_no']}")
    print(f"Name      : {student['name']}")
    print(f"Course    : {student['course']}")
    print("-" * 55)

    for subject, mark in student["marks"].items():
        print(f"{subject:<25}: {mark:>6.2f}")

    print("-" * 55)
    print(f"Total     : {student['total']:.2f} / {len(SUBJECTS) * 100}")
    print(f"Percentage: {student['percentage']:.2f}%")
    print(f"Grade     : {student['grade']}")
    print("=" * 55)


def view_all_students(students):
    print("\n--- All Student Results ---")

    if not students:
        print("No student records found.")
        return

    print(f"{'Roll No':<12}{'Name':<22}{'Percentage':<14}{'Grade':<8}")
    print("-" * 56)
    for student in students:
        print(
            f"{student['roll_no']:<12}"
            f"{student['name'][:20]:<22}"
            f"{student['percentage']:<14.2f}"
            f"{student['grade']:<8}"
        )


def search_student(students):
    roll_no = input("Enter roll number to search: ").strip()
    student = find_student(students, roll_no)

    if student:
        display_student(student)
    else:
        print("Student not found.")


def update_student(students):
    roll_no = input("Enter roll number to update: ").strip()
    student = find_student(students, roll_no)

    if not student:
        print("Student not found.")
        return

    print("Press ENTER to keep the existing value.")
    name = input(f"Name [{student['name']}]: ").strip()
    course = input(f"Course/Class [{student['course']}]: ").strip()

    if name:
        student["name"] = name
    if course:
        student["course"] = course

    change_marks = input("Update marks? (y/n): ").strip().lower()
    if change_marks == "y":
        student["marks"] = {subject: read_mark(subject) for subject in SUBJECTS}

    total, percentage, grade = calculate_result(student["marks"])
    student["total"] = total
    student["percentage"] = percentage
    student["grade"] = grade

    save_students(students)
    print("Student record updated successfully.")


def delete_student(students):
    roll_no = input("Enter roll number to delete: ").strip()
    student = find_student(students, roll_no)

    if not student:
        print("Student not found.")
        return

    confirm = input(f"Delete {student['name']}? (y/n): ").strip().lower()
    if confirm == "y":
        students.remove(student)
        save_students(students)
        print("Student deleted successfully.")
    else:
        print("Delete cancelled.")


def show_statistics(students):
    if not students:
        print("No records available.")
        return

    average = sum(s["percentage"] for s in students) / len(students)
    highest = max(students, key=lambda s: s["percentage"])
    passed = sum(s["grade"] != "FAIL" for s in students)

    print("\n--- Result Statistics ---")
    print(f"Total students : {len(students)}")
    print(f"Passed         : {passed}")
    print(f"Failed         : {len(students) - passed}")
    print(f"Class average  : {average:.2f}%")
    print(f"Highest scorer : {highest['name']} ({highest['percentage']:.2f}%)")


def main():
    students = load_students()

    while True:
        print("\n" + "=" * 55)
        print(" STUDENT RESULT MANAGEMENT SYSTEM")
        print("=" * 55)
        print("1. Add Student Result")
        print("2. View All Results")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Show Statistics")
        print("7. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_all_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            show_statistics(students)
        elif choice == "7":
            print("Thank you for using the system.")
            break
        else:
            print("Invalid choice. Please select 1-7.")


if __name__ == "__main__":
    main()
