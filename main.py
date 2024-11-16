from registration import register_student
from attendance import mark_attendance_from_image

if __name__ == "__main__":
    print("Welcome to the Attendance Management System")
    # Example: register a student
    register_student("Alice", "ECE2024", "98765", "path/to/image.jpg")

    # Example: mark attendance
    mark_attendance_from_image("path/to/group_photo.jpg", "Physics", "11:00 AM")
