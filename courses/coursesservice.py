courses = []

def add_course():
    course_id = input("Enter Course ID: ")
    title = input("Enter Course Title: ")
    credit = float(input("Enter Credit Hour: "))

    courses.append({
        "id": course_id,
        "title": title,
        "credit": credit
    })
    print("Course added successfully.\n")

def list_courses():
    if not courses:
        print("No courses registered.\n")
        return

    print("\nAvailable Courses:")
    for c in courses:
        print(f"ID: {c['id']} | Title: {c['title']} | Credit: {c['credit']}")
    print()

def find_course(course_id):
    for c in courses:
        if c["id"] == course_id:
            return c
    return None
