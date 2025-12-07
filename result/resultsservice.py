results = []

def add_result(students_list, courses_list):
    student_id = input("Enter Student ID: ")
    course_id = input("Enter Course ID: ")
    grade = input("Enter Letter Grade (A, B+, B, C+, C, D, F): ").upper()

    student = students_list(student_id)
    if student is None:
        print("Student not found.\n")
        return

    course = courses_list(course_id)
    if course is None:
        print("Course not found.\n")
        return

    results.append({
        "student_id": student_id,
        "course_id": course_id,
        "grade": grade
    })
    print("Result added successfully.\n")

def list_results():
    if not results:
        print("No results found.\n")
        return

    print("\nAll Results:")
    for r in results:
        print(f"Student ID: {r['student_id']} | Course ID: {r['course_id']} | Grade: {r['grade']}")
    print()
