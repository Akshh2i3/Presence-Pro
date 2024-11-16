import cv2
import face_recognition
import sqlite3
from utils import initialize_db, save_face_encoding

def register_student(name, batch, enrollment_number, image_path):
    # Load the image
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect face and encode it
    face_locations = face_recognition.face_locations(rgb_image)
    if len(face_locations) != 1:
        print("Error: Image must contain exactly one face.")
        return False

    face_encoding = face_recognition.face_encodings(rgb_image, face_locations)[0]

    # Save data to database
    conn = sqlite3.connect("models/student_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, batch, enrollment_number) VALUES (?, ?, ?)",
                   (name, batch, enrollment_number))
    student_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Save face encoding
    save_face_encoding(student_id, face_encoding)
    print(f"Student {name} registered successfully!")
    return True

if __name__ == "__main__":
    initialize_db()
    # Test registration
    register_student("John Doe", "CS2024", "12345", "path/to/image.jpg")
