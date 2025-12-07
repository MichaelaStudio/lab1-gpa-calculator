GRADE_POINTS = {
    "A": 4.0,
    "B+": 3.5,
    "B": 3.0,
    "C+": 2.5,
    "C": 2.0,
    "D": 1.0,
    "F": 0.0
}

def calculate_gpa(student_id, results_list, course_finder):
    total_points = 0
    total_credits = 0

    for r in results_list:
        if r["student_id"] == student_id:
            course = course_finder(r["course_id"])
            if course:
                credit = course["credit"]
                grade_value = GRADE_POINTS.get(r["grade"], 0)

                total_credits += credit
                total_points += (grade_value * credit)

    if total_credits == 0:
        return 0

    return round(total_points / total_credits, 2)
