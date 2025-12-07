from students.studentsservice import add_student, list_students, find_student
from courses.coursesservice import add_course, list_courses, find_course
from result.resultsservice import add_result, list_results, results as results_data
from gradesreport.gradereport import calculate_gpa

def menu():
    print("\n===== GPA CALCULATOR SYSTEM =====")
    print("1. Students")
    print("2. Courses")
    print("3. Results")
    print("4. Grade Report")
    print("5. Exit")

while True:
    menu()
    choice = input("Enter choice: ")
    if choice == "1":
        print("\n1. List Students")
        print("2. Add Student")
        sub = input("Enter: ")

        if sub == "1":
            list_students()

        elif sub == "2":
            add_student()

    elif choice == "2":
        print("\n1. List Courses")
        print("2. Add Course")
        sub = input("Enter: ")

        if sub == "1":
            list_courses()

        elif sub == "2":
            add_course()
    elif choice == "3":
        print("\n1. List Results")
        print("2. Add Result")
        sub = input("Enter: ")

        if sub == "1":
            list_results()

        elif sub == "2":
            add_result(find_student, find_course)


    elif choice == "4":
        student_id = input("Enter Student ID: ")
        gpa = calculate_gpa(student_id, results_data, find_course)
        if gpa == 0:
            print("No graded courses found for this student or student not found.")
        else:
            print(f"GPA for student {student_id}: {gpa}")

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid choice!")
         