from registration import register_student
from attedance import mark_attendance_from_live

def main():
    print("Welcome to the Attendance Management System")
    print("Please choose an option:")
    print("1. Register a new student")
    print("2. Mark attendance")
    print("3. Exit")
    choice = input("Enter 1, 2, or 3: ")

    if choice == "1":
        # Register a new student
        name = input("Enter the student's name: ")
        batch = input("Enter the student's batch: ")
        enrollment_number = input("Enter the student's enrollment number: ")
        if register_student(name, batch, enrollment_number):
            print(f"Student '{name}' registered successfully!")

    elif choice == "2":
        # Mark attendance
        subject = input("Enter the subject: ")
        time = input("Enter the time (e.g., 11:00 AM): ")
        mark_attendance_from_live(subject, time)
        print("Attendance marked successfully!")

    elif choice == "3":
        print("Exiting the system. Goodbye!")
        exit()

    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
