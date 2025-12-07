"""
GPA Calculator System - Professional Core Edition
Focused on Students, Courses, Results, and Grade Reports
"""

import os
import time
from datetime import datetime
import sys

# Import your existing modules
from students.studentsservice import add_student, list_students, find_student
from courses.coursesservice import add_course, list_courses, find_course
from result.resultsservice import add_result, list_results, results as results_data
from gradesreport.gradereport import calculate_gpa

# ==================== UI CONFIGURATION ====================
class UIConfig:
    """UI Configuration and styling"""
    
    # ANSI Color Codes (works on most terminals)
    class Colors:
        RESET = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        DIM = '\033[2m'  # Added DIM attribute
        
        # Regular colors
        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        WHITE = '\033[37m'
        GRAY = '\033[90m'  # Added GRAY attribute
        
        # Bright colors
        BRIGHT_RED = '\033[91m'
        BRIGHT_GREEN = '\033[92m'
        BRIGHT_YELLOW = '\033[93m'
        BRIGHT_BLUE = '\033[94m'
        BRIGHT_MAGENTA = '\033[95m'
        BRIGHT_CYAN = '\033[96m'
        BRIGHT_WHITE = '\033[97m'
        
        # Backgrounds
        BG_BLUE = '\033[44m'
        BG_GREEN = '\033[42m'
        BG_YELLOW = '\033[43m'
        BG_RED = '\033[41m'
        BG_GRAY = '\033[100m'
    
    # Icons for visual appeal
    class Icons:
        STUDENT = "👨‍🎓"
        COURSE = "📚"
        RESULT = "📊"
        REPORT = "📈"
        EXIT = "🚪"
        BACK = "⬅️"
        ADD = "➕"
        LIST = "📋"
        SEARCH = "🔍"
        CALCULATE = "🧮"
        SUCCESS = "✅"
        ERROR = "❌"
        WARNING = "⚠️"
        INFO = "ℹ️"
        LOADING = "⏳"
        CHECK = "✓"
        STAR = "⭐"
        TROPHY = "🏆"
        BOOK = "📖"
        GRADUATE = "🎓"

# ==================== UI UTILITIES ====================
class UIUtils:
    """Utility functions for user interface"""
    
    @staticmethod
    def clear_screen():
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_center(text, width=60, color=UIConfig.Colors.CYAN):
        """Print centered text"""
        centered = text.center(width)
        print(f"{color}{centered}{UIConfig.Colors.RESET}")
    
    @staticmethod
    def print_header(title, width=60):
        """Print a beautiful header"""
        border = "═" * width
        print(f"\n{UIConfig.Colors.BRIGHT_CYAN}{border}")
        print(f"║{UIConfig.Colors.BRIGHT_WHITE}{title.center(width-2)}{UIConfig.Colors.BRIGHT_CYAN}║")
        print(f"{border}{UIConfig.Colors.RESET}\n")
    
    @staticmethod
    def print_section(title, width=50):
        """Print a section title"""
        print(f"\n{UIConfig.Colors.BRIGHT_BLUE}{'─' * width}")
        print(f" {UIConfig.Icons.INFO} {title}")
        print(f"{'─' * width}{UIConfig.Colors.RESET}")
    
    @staticmethod
    def print_success(message):
        """Print success message"""
        print(f"\n{UIConfig.Colors.GREEN}{UIConfig.Icons.SUCCESS} {message}{UIConfig.Colors.RESET}")
    
    @staticmethod
    def print_error(message):
        """Print error message"""
        print(f"\n{UIConfig.Colors.RED}{UIConfig.Icons.ERROR} {message}{UIConfig.Colors.RESET}")
    
    @staticmethod
    def print_warning(message):
        """Print warning message"""
        print(f"\n{UIConfig.Colors.YELLOW}{UIConfig.Icons.WARNING} {message}{UIConfig.Colors.RESET}")
    
    @staticmethod
    def print_info(message):
        """Print info message"""
        print(f"\n{UIConfig.Colors.CYAN}{UIConfig.Icons.INFO} {message}{UIConfig.Colors.RESET}")
    
    @staticmethod
    def loading_animation(text="Processing", duration=1.5):
        """Show loading animation"""
        print(f"\n{UIConfig.Colors.YELLOW}{UIConfig.Icons.LOADING} {text}", end="", flush=True)
        
        frames = [".  ", ".. ", "...", "   "]
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for frame in frames:
                print(f"\r{UIConfig.Colors.YELLOW}{UIConfig.Icons.LOADING} {text}{frame}", end="", flush=True)
                time.sleep(0.2)
        
        print(f"\r{UIConfig.Colors.GREEN}{UIConfig.Icons.CHECK} {text} complete!{' ' * 20}{UIConfig.Colors.RESET}")
    
    @staticmethod
    def get_input(prompt, required=True):
        """Get user input with validation"""
        while True:
            try:
                value = input(f"\n{UIConfig.Colors.BRIGHT_YELLOW}↳ {prompt}: {UIConfig.Colors.WHITE}").strip()
                
                if required and not value:
                    UIUtils.print_error("This field is required!")
                    continue
                
                return value
            except KeyboardInterrupt:
                print(f"\n{UIConfig.Colors.YELLOW}Operation cancelled.{UIConfig.Colors.RESET}")
                return None
    
    @staticmethod
    def confirm_action(message):
        """Ask for confirmation"""
        response = input(f"\n{UIConfig.Colors.YELLOW}{UIConfig.Icons.WARNING} {message} (y/N): {UIConfig.Colors.WHITE}").strip().lower()
        return response in ['y', 'yes']
    
    @staticmethod
    def press_enter():
        """Wait for Enter key"""
        input(f"\n{UIConfig.Colors.GRAY}Press Enter to continue...{UIConfig.Colors.RESET}")
    
    @staticmethod
    def format_gpa(gpa):
        """Format GPA with color coding"""
        if gpa >= 3.7:
            color = UIConfig.Colors.BRIGHT_GREEN
            icon = UIConfig.Icons.TROPHY
            grade = "A"
        elif gpa >= 3.3:
            color = UIConfig.Colors.GREEN
            icon = UIConfig.Icons.STAR
            grade = "B+"
        elif gpa >= 3.0:
            color = UIConfig.Colors.YELLOW
            icon = "✨"
            grade = "B"
        elif gpa >= 2.7:
            color = UIConfig.Colors.BRIGHT_YELLOW
            icon = "👍"
            grade = "C+"
        elif gpa >= 2.3:
            color = UIConfig.Colors.MAGENTA
            icon = "📝"
            grade = "C"
        elif gpa >= 2.0:
            color = UIConfig.Colors.RED
            icon = "⚠️"
            grade = "D"
        else:
            color = UIConfig.Colors.BRIGHT_RED
            icon = "❌"
            grade = "F"
        
        return f"{color}{icon} {gpa:.2f} ({grade}){UIConfig.Colors.RESET}"

# ==================== MAIN MENU ====================
class MainMenu:
    """Main menu system"""
    
    @staticmethod
    def display():
        """Display main menu"""
        UIUtils.clear_screen()
        
        # Print beautiful header
        print(f"{UIConfig.Colors.BRIGHT_CYAN}")
        print("╔═══════════════════════════════════════════════════╗")
        print("║                                                   ║")
        print("║   ██████╗ ██████╗  █████╗     ██████╗ █████╗      ║")
        print("║  ██╔════╝ ██╔══██╗██╔══██╗   ██╔════╝██╔══██╗     ║")
        print("║  ██║  ███╗██████╔╝███████║   ██║     ███████║     ║")
        print("║  ██║   ██║██╔═══╝ ██╔══██║   ██║     ██╔══██║     ║")
        print("║  ╚██████╔╝██║     ██║  ██║   ╚██████╗██║  ██║     ║")
        print("║   ╚═════╝ ╚═╝     ╚═╝  ╚═╝    ╚═════╝╚═╝  ╚═╝     ║")
        print("║                                                   ║")
        print("║         GPA CALCULATOR SYSTEM                     ║")
        print("║                                                   ║")
        print("╚═══════════════════════════════════════════════════╝")
        print(f"{UIConfig.Colors.RESET}")
        
        # Print current date and time
        current_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        print(f"{UIConfig.Colors.GRAY}{' '*15}📅 {current_time}{' '*15}{UIConfig.Colors.RESET}")
        print()
        
        # Menu options with icons
        options = [
            (f"{UIConfig.Icons.STUDENT}  Students Management", "Manage student records"),
            (f"{UIConfig.Icons.COURSE}  Courses Management", "Manage course information"),
            (f"{UIConfig.Icons.RESULT}  Results Management", "Manage examination results"),
            (f"{UIConfig.Icons.REPORT}  Grade Report", "Calculate and view GPA"),
            (f"{UIConfig.Icons.EXIT}  Exit System", "Close the application")
        ]
        
        # Display menu in a box
        print(f"{UIConfig.Colors.BRIGHT_BLUE}┌{'─'*58}┐{UIConfig.Colors.RESET}")
        print(f"{UIConfig.Colors.BRIGHT_BLUE}│{UIConfig.Colors.BRIGHT_WHITE}{'MAIN MENU'.center(58)}{UIConfig.Colors.BRIGHT_BLUE}│{UIConfig.Colors.RESET}")
        print(f"{UIConfig.Colors.BRIGHT_BLUE}├{'─'*58}┤{UIConfig.Colors.RESET}")
        
        for i, (title, description) in enumerate(options, 1):
            print(f"{UIConfig.Colors.BRIGHT_BLUE}│ {UIConfig.Colors.GREEN}[{i}] {UIConfig.Colors.BRIGHT_WHITE}{title:<25} "
                  f"{UIConfig.Colors.GRAY}{description:<30}{UIConfig.Colors.BRIGHT_BLUE}│{UIConfig.Colors.RESET}")
        
        print(f"{UIConfig.Colors.BRIGHT_BLUE}└{'─'*58}┘{UIConfig.Colors.RESET}")
        print()
        
        return UIUtils.get_input("Select option (1-5)", required=True)

# ==================== STUDENTS MODULE ====================
class StudentsModule:
    """Students management module"""
    
    @staticmethod
    def show():
        """Show students menu"""
        while True:
            UIUtils.clear_screen()
            UIUtils.print_header(f"{UIConfig.Icons.STUDENT} STUDENTS MANAGEMENT")
            
            # Students menu options
            print(f"{UIConfig.Colors.BRIGHT_WHITE}Please select an option:{UIConfig.Colors.RESET}\n")
            print(f"  {UIConfig.Colors.GREEN}[1]{UIConfig.Colors.RESET} {UIConfig.Icons.LIST}  View All Students")
            print(f"  {UIConfig.Colors.GREEN}[2]{UIConfig.Colors.RESET} {UIConfig.Icons.ADD}  Add New Student")
            print(f"  {UIConfig.Colors.GREEN}[3]{UIConfig.Colors.RESET} {UIConfig.Icons.SEARCH}  Find Student")
            print(f"  {UIConfig.Colors.GREEN}[0]{UIConfig.Colors.RESET} {UIConfig.Icons.BACK}  Return to Main Menu")
            print()
            
            choice = UIUtils.get_input("Enter your choice", required=True)
            
            if choice == "0":
                break
            elif choice == "1":
                StudentsModule.list_all()
            elif choice == "2":
                StudentsModule.add_new()
            elif choice == "3":
                StudentsModule.find()
            else:
                UIUtils.print_error("Invalid choice! Please try again.")
                time.sleep(1)
    
    @staticmethod
    def list_all():
        """List all students"""
        UIUtils.clear_screen()
        UIUtils.print_header(f"{UIConfig.Icons.LIST} ALL STUDENTS")
        UIUtils.loading_animation("Loading student records")
        print()
        
        list_students()
        UIUtils.press_enter()
    
    @staticmethod
    def add_new():
        """Add new student"""
        UIUtils.clear_screen()
        UIUtils.print_header(f"{UIConfig.Icons.ADD} ADD NEW STUDENT")
        
        print(f"{UIConfig.Colors.CYAN}Please fill in the student details:{UIConfig.Colors.RESET}\n")
        print(f"{UIConfig.Colors.GRAY}{'─'*50}{UIConfig.Colors.RESET}")
        
        add_student()
        
        UIUtils.print_success("Student added successfully!")
        time.sleep(1)
    
    @staticmethod
    def find():
        """Find a student"""
        UIUtils.clear_screen()
        UIUtils.print_header(f"{UIConfig.Icons.SEARCH} FIND STUDENT")
        
        student_id = UIUtils.get_input("Enter Student ID to search")
        if student_id:
            UIUtils.loading_animation("Searching for student")
            print()
            
            student = find_student(student_id)
            if student:
                UIUtils.print_success("Student Found!")
                print(f"\n{UIConfig.Colors.BRIGHT_WHITE}{'─'*40}")
                print(f"{UIConfig.Colors.CYAN}ID:{UIConfig.Colors.RESET} {student.get('id', 'N/A')}")
                print(f"{UIConfig.Colors.CYAN}Name:{UIConfig.Colors.RESET} {student.get('name', 'N/A')}")
                print(f"{UIConfig.Colors.CYAN}Email:{UIConfig.Colors.RESET} {student.get('email', 'N/A')}")
                print(f"{UIConfig.Colors.BRIGHT_WHITE}{'─'*40}{UIConfig.Colors.RESET}")
            else:
                UIUtils.print_error(f"No student found with ID: {student_id}")
            
            UIUtils.press_enter()

# ==================== COURSES MODULE ====================
class CoursesModule:
    """Courses management module"""
    
    @staticmethod
    def show():
        """Show courses menu"""
        while True:
            UIUtils.clear_screen()
            UIUtils.print_header(f"{UIConfig.Icons.COURSE} COURSES MANAGEMENT")
            
            # Courses menu options
            print(f"{UIConfig.Colors.BRIGHT_WHITE}Please select an option:{UIConfig.Colors.RESET}\n")
            print(f"  {UIConfig.Colors.GREEN}[1]{UIConfig.Colors.RESET} {UIConfig.Icons.LIST}  View All Courses")
            print(f"  {UIConfig.Colors.GREEN}[2]{UIConfig.Colors.RESET} {UIConfig.Icons.ADD}  Add New Course")
            print(f"  {UIConfig.Colors.GREEN}[3]{UIConfig.Colors.RESET} {UIConfig.Icons.SEARCH}  Find Course")
            print(f"  {UIConfig.Colors.GREEN}[0]{UIConfig.Colors.RESET} {UIConfig.Icons.BACK}  Return to Main Menu")
            print()
            
            choice = UIUtils.get_input("Enter your choice", required=True)
            
            if choice == "0":
                break
            elif choice == "1":
                CoursesModule.list_all()
            elif choice == "2":
                CoursesModule.add_new()
            elif choice == "3":
                CoursesModule.find()
            else:
                UIUtils.print_error("Invalid choice! Please try again.")
                time.sleep(1)
    
    @staticmethod
    def list_all():
        """List all courses"""
        UIUtils.clear_screen()
        UIUtils.print_header(f"{UIConfig.Icons.LIST} ALL COURSES")
        UIUtils.loading_animation("Loading course catalog")
        print()
        
        list_courses()
        UIUtils.press_enter()
    
    @staticmethod
    def add_new():
        """Add new course"""
        UIUtils.clear_screen()
        UIUtils.print_header(f"{UIConfig.Icons.ADD} ADD NEW COURSE")
        
        print(f"{UIConfig.Colors.CYAN}Please fill in the course details:{UIConfig.Colors.RESET}\n")
        print(f"{UIConfig.Colors.GRAY}{'─'*50}{UIConfig.Colors.RESET}")
        
        add_course()
        
        UIUtils.print_success("Course added successfully!")
        time.sleep(1)
    
    @staticmethod
    def find():
        """Find a course"""
        UIUtils.clear_screen()
        UIUtils.print_header(f"{UIConfig.Icons.SEARCH} FIND COURSE")
        
        course_code = UIUtils.get_input("Enter Course Code to search")
        if course_code:
            UIUtils.loading_animation("Searching for course")
            print()
            
            course = find_course(course_code)
            if course:
                UIUtils.print_success("Course Found!")
                print(f"\n{UIConfig.Colors.BRIGHT_WHITE}{'─'*40}")
                print(f"{UIConfig.Colors.CYAN}Code:{UIConfig.Colors.RESET} {course.get('code', 'N/A')}")
                print(f"{UIConfig.Colors.CYAN}Name:{UIConfig.Colors.RESET} {course.get('name', 'N/A')}")
                print(f"{UIConfig.Colors.CYAN}Credits:{UIConfig.Colors.RESET} {course.get('credits', 'N/A')}")
                print(f"{UIConfig.Colors.BRIGHT_WHITE}{'─'*40}{UIConfig.Colors.RESET}")
            else:
                UIUtils.print_error(f"No course found with code: {course_code}")
            
            UIUtils.press_enter()

# ==================== RESULTS MODULE ====================
class ResultsModule:
    """Results management module"""
    
    @staticmethod
    def show():
        """Show results menu"""
        while True:
            UIUtils.clear_screen()
            UIUtils.print_header(f"{UIConfig.Icons.RESULT} RESULTS MANAGEMENT")
            
            # Results menu options
            print(f"{UIConfig.Colors.BRIGHT_WHITE}Please select an option:{UIConfig.Colors.RESET}\n")
            print(f"  {UIConfig.Colors.GREEN}[1]{UIConfig.Colors.RESET} {UIConfig.Icons.LIST}  View All Results")
            print(f"  {UIConfig.Colors.GREEN}[2]{UIConfig.Colors.RESET} {UIConfig.Icons.ADD}  Add New Result")
            print(f"  {UIConfig.Colors.GREEN}[0]{UIConfig.Colors.RESET} {UIConfig.Icons.BACK}  Return to Main Menu")
            print()
            
            choice = UIUtils.get_input("Enter your choice", required=True)
            
            if choice == "0":
                break
            elif choice == "1":
                ResultsModule.list_all()
            elif choice == "2":
                ResultsModule.add_new()
            else:
                UIUtils.print_error("Invalid choice! Please try again.")
                time.sleep(1)
    
    @staticmethod
    def list_all():
        """List all results"""
        UIUtils.clear_screen()
        UIUtils.print_header(f"{UIConfig.Icons.LIST} ALL RESULTS")
        UIUtils.loading_animation("Loading examination results")
        print()
        
        list_results()
        UIUtils.press_enter()
    
    @staticmethod
    def add_new():
        """Add new result"""
        UIUtils.clear_screen()
        UIUtils.print_header(f"{UIConfig.Icons.ADD} ADD NEW RESULT")
        
        print(f"{UIConfig.Colors.CYAN}Please fill in the result details:{UIConfig.Colors.RESET}\n")
        print(f"{UIConfig.Colors.GRAY}{'─'*50}{UIConfig.Colors.RESET}")
        
        add_result(find_student, find_course)
        
        UIUtils.print_success("Result added successfully!")
        time.sleep(1)

# ==================== GRADE REPORT MODULE ====================
class GradeReportModule:
    """Grade report and GPA calculation module"""
    
    @staticmethod
    def show():
        """Show grade report menu"""
        while True:
            UIUtils.clear_screen()
            UIUtils.print_header(f"{UIConfig.Icons.REPORT} GRADE REPORT")
            
            # Grade report options
            print(f"{UIConfig.Colors.BRIGHT_WHITE}Please select an option:{UIConfig.Colors.RESET}\n")
            print(f"  {UIConfig.Colors.GREEN}[1]{UIConfig.Colors.RESET} {UIConfig.Icons.CALCULATE}  Calculate GPA")
            print(f"  {UIConfig.Colors.GREEN}[2]{UIConfig.Colors.RESET} {UIConfig.Icons.GRADUATE}  View Academic Standing")
            print(f"  {UIConfig.Colors.GREEN}[0]{UIConfig.Colors.RESET} {UIConfig.Icons.BACK}  Return to Main Menu")
            print()
            
            choice = UIUtils.get_input("Enter your choice", required=True)
            
            if choice == "0":
                break
            elif choice == "1":
                GradeReportModule.calculate_gpa()
            elif choice == "2":
                GradeReportModule.academic_standing()
            else:
                UIUtils.print_error("Invalid choice! Please try again.")
                time.sleep(1)
    
    @staticmethod
    def calculate_gpa():
        """Calculate GPA for a student"""
        UIUtils.clear_screen()
        UIUtils.print_header(f"{UIConfig.Icons.CALCULATE} GPA CALCULATOR")
        
        print(f"{UIConfig.Colors.CYAN}Enter the student ID to calculate GPA:{UIConfig.Colors.RESET}\n")
        
        student_id = UIUtils.get_input("Student ID")
        if not student_id:
            return
        
        UIUtils.loading_animation(f"Calculating GPA for {student_id}")
        print()
        
        gpa = calculate_gpa(student_id, results_data, find_course)
        
        # Display results
        print(f"{UIConfig.Colors.BRIGHT_CYAN}{'='*55}")
        print(f" GPA CALCULATION RESULT ".center(55, '='))
        print(f"{'='*55}{UIConfig.Colors.RESET}\n")
        
        if gpa == 0:
            UIUtils.print_error(f"No graded courses found for Student ID: {student_id}")
            print(f"\n{UIConfig.Colors.GRAY}Possible reasons:")
            print(f"• Student doesn't exist in the system")
            print(f"• No results have been recorded yet")
            print(f"• All courses are ungraded{UIConfig.Colors.RESET}")
        else:
            # Display GPA with color coding
            print(f"{UIConfig.Colors.BRIGHT_WHITE}Student ID: {UIConfig.Colors.CYAN}{student_id}")
            print(f"{UIConfig.Colors.BRIGHT_WHITE}GPA Score: {UIUtils.format_gpa(gpa)}")
            print()
            
            # Display academic standing
            GradeReportModule.display_academic_info(gpa)
        
        print(f"\n{UIConfig.Colors.GRAY}{'─'*55}{UIConfig.Colors.RESET}")
        UIUtils.press_enter()
    
    @staticmethod
    def academic_standing():
        """Show academic standing information"""
        UIUtils.clear_screen()
        UIUtils.print_header(f"{UIConfig.Icons.GRADUATE} ACADEMIC STANDING")
        
        print(f"{UIConfig.Colors.CYAN}Academic Grading Scale:{UIConfig.Colors.RESET}\n")
        
        # Academic scale table
        scale = [
            (4.00, 3.70, "A", "First Class Honors", UIConfig.Colors.BRIGHT_GREEN, UIConfig.Icons.TROPHY),
            (3.69, 3.30, "B+", "Upper Second Class", UIConfig.Colors.GREEN, UIConfig.Icons.STAR),
            (3.29, 3.00, "B", "Lower Second Class", UIConfig.Colors.YELLOW, "✨"),
            (2.99, 2.70, "C+", "Third Class", UIConfig.Colors.BRIGHT_YELLOW, "👍"),
            (2.69, 2.30, "C", "Pass", UIConfig.Colors.MAGENTA, "📝"),
            (2.29, 2.00, "D", "Conditional Pass", UIConfig.Colors.RED, "⚠️"),
            (1.99, 0.00, "F", "Fail", UIConfig.Colors.BRIGHT_RED, "❌"),
        ]
        
        print(f"{UIConfig.Colors.BRIGHT_WHITE}{'GPA Range':^12} {'Grade':^8} {'Standing':^20} {'Status':^15}{UIConfig.Colors.RESET}")
        print(f"{UIConfig.Colors.GRAY}{'─'*55}{UIConfig.Colors.RESET}")
        
        for high, low, grade, standing, color, icon in scale:
            range_str = f"{low:.2f} - {high:.2f}" if low > 0 else f"0.00 - {high:.2f}"
            print(f"{color}{range_str:^12} {grade:^8} {standing:^20} {icon:^15}{UIConfig.Colors.RESET}")
        
        print(f"\n{UIConfig.Colors.GRAY}{'─'*55}{UIConfig.Colors.RESET}")
        print(f"\n{UIConfig.Colors.CYAN}Note:{UIConfig.Colors.RESET} Minimum passing GPA is usually 2.00")
        print(f"{UIConfig.Colors.GRAY}GPA is calculated based on weighted average of grades.{UIConfig.Colors.RESET}")
        
        UIUtils.press_enter()
    
    @staticmethod
    def display_academic_info(gpa):
        """Display academic information based on GPA"""
        print(f"{UIConfig.Colors.BRIGHT_WHITE}Academic Standing:{UIConfig.Colors.RESET}")
        
        if gpa >= 3.7:
            print(f"{UIConfig.Colors.BRIGHT_GREEN}🏆 Excellent - First Class Honors!")
            print("Outstanding academic performance. Eligible for honors programs.")
        elif gpa >= 3.3:
            print(f"{UIConfig.Colors.GREEN}⭐ Very Good - Upper Second Class")
            print("Strong academic record. Consider research opportunities.")
        elif gpa >= 3.0:
            print(f"{UIConfig.Colors.YELLOW}✨ Good - Lower Second Class")
            print("Solid performance. Maintain current study habits.")
        elif gpa >= 2.7:
            print(f"{UIConfig.Colors.BRIGHT_YELLOW}👍 Satisfactory - Third Class")
            print("Meeting requirements. Room for improvement in some areas.")
        elif gpa >= 2.0:
            print(f"{UIConfig.Colors.RED}⚠️  Conditional - Minimum Passing")
            print("Academic probation risk. Consider academic counseling.")
        else:
            print(f"{UIConfig.Colors.BRIGHT_RED}❌ Below Standard")
            print("Immediate academic intervention required.")
        
        # Study recommendations
        print(f"\n{UIConfig.Colors.CYAN}Recommendations:{UIConfig.Colors.RESET}")
        if gpa < 2.5:
            print("• Schedule meeting with academic advisor")
            print("• Utilize tutoring services")
            print("• Improve time management skills")
        elif gpa < 3.0:
            print("• Join study groups")
            print("• Focus on weaker subjects")
            print("• Regular review of materials")
        else:
            print("• Consider honors courses")
            print("• Explore research opportunities")
            print("• Mentor fellow students")

# ==================== APPLICATION MAIN CLASS ====================
class GPACalculatorApp:
    """Main application class"""
    
    def __init__(self):
        self.running = True
        self.session_start = datetime.now()
    
    def run(self):
        """Main application loop"""
        try:
            while self.running:
                try:
                    choice = MainMenu.display()
                    
                    if choice == "1":
                        StudentsModule.show()
                    elif choice == "2":
                        CoursesModule.show()
                    elif choice == "3":
                        ResultsModule.show()
                    elif choice == "4":
                        GradeReportModule.show()
                    elif choice == "5":
                        self.exit_app()
                    else:
                        UIUtils.print_error("Invalid choice! Please select 1-5.")
                        time.sleep(1)
                        
                except KeyboardInterrupt:
                    print(f"\n{UIConfig.Colors.YELLOW}Operation interrupted.{UIConfig.Colors.RESET}")
                    if UIUtils.confirm_action("Exit the application?"):
                        self.exit_app()
                        
                except Exception as e:
                    UIUtils.print_error(f"An error occurred: {str(e)}")
                    print(f"{UIConfig.Colors.GRAY}The application will continue...{UIConfig.Colors.RESET}")
                    time.sleep(2)
                    
        except Exception as e:
            UIUtils.print_error(f"Fatal error: {str(e)}")
            input("Press Enter to exit...")
    
    def exit_app(self):
        """Exit the application gracefully"""
        UIUtils.clear_screen()
        
        # Calculate session duration
        session_duration = datetime.now() - self.session_start
        hours, remainder = divmod(session_duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Farewell message
        print(f"{UIConfig.Colors.BRIGHT_CYAN}")
        print("╔═══════════════════════════════════════════════════╗")
        print("║                                                   ║")
        print("║          Thank you for using                      ║")
        print("║          GPA Calculator System!                   ║")
        print("║                                                   ║")
        print("╚═══════════════════════════════════════════════════╝")
        print(f"{UIConfig.Colors.RESET}")
        
        print(f"\n{UIConfig.Colors.CYAN}Session Summary:{UIConfig.Colors.RESET}")
        print(f"{UIConfig.Colors.GRAY}{'─'*30}{UIConfig.Colors.RESET}")
        print(f"{UIConfig.Colors.WHITE}Duration: {hours:02d}:{minutes:02d}:{seconds:02d}")
        print(f"Session ended: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}{UIConfig.Colors.RESET}")
        print()
        print(f"{UIConfig.Colors.GREEN}{UIConfig.Icons.CHECK} All data saved successfully!")
        print(f"{UIConfig.Colors.BRIGHT_WHITE}Goodbye! 👋{UIConfig.Colors.RESET}")
        print()
        
        self.running = False
        time.sleep(2)

# ==================== APPLICATION ENTRY POINT ====================
if __name__ == "__main__":
    # Create and run the application
    app = GPACalculatorApp()
    app.run()