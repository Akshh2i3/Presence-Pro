from registration import register_student
from attedance import mark_attendance_from_live

if __name__ == "__main__":
    print("Welcome to the Attendance Management System")
    print("Please choose an option:")
    print("1. Register a new student")
    print("2. Mark attendance")

    choice = input("Enter 1 or 2: ")

    if choice == "1":
        # Get input from the user for registering a student
        name = input("Enter the student's name: ")
        batch= input("Enter the student's batch: ")
        student_id = input("Enter the student's ID: ")
        register_student(name, batch, student_id)
        print("Student registered successfully!")

    elif choice == "2":
        # Get input from the user for marking attendance
        subject = input("Enter the subject: ")
        time = input("Enter the time (e.g., 11:00 AM): ")
        mark_attendance_from_live(subject, time)
        print("Attendance marked successfully!")

    else:
        print("Invalid choice. Please enter 1 or 2.")
