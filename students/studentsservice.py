students = []

def add_student():
    student_id = input("Enter Student ID: ")
    name = input("Enter Student Name: ")

    students.append({
        "id": student_id,
        "name": name
    })
    print("Student registered successfully.\n")

def list_students():
    if not students:
        print("No students registered.\n")
        return

    print("\nRegistered Students:")
    for s in students:
        print(f"ID: {s['id']} | Name: {s['name']}")
    print()

def find_student(student_id):
    for s in students:
        if s["id"] == student_id:
            return s
    return None
