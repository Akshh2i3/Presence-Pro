import cv2
import face_recognition
import sqlite3
from utils import initialize_db, save_face_encoding

def capture_live_photo():
    """
    Captures a live photo from the webcam and returns it.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    print("Press 's' to take a snapshot and 'q' to quit.")
    captured_image = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Display the frame
        cv2.imshow('Live Camera Feed', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            print("Image captured successfully!")
            captured_image = frame
            break
        elif key == ord('q'):
            print("Camera feed closed.")
            break

    cap.release()
    cv2.destroyAllWindows()
    return captured_image

def register_student(name, batch, enrollment_number):
    """
    Registers a new student by capturing a photo, encoding their face,
    and storing their details and encoding in the database.
    """
    # Initialize the database if needed
    initialize_db()

    # Capture a live photo
    image = capture_live_photo()
    if image is None:
        print("No image captured. Registration cancelled.")
        return False

    # Convert image to RGB for face recognition processing
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect face and create encoding
    face_locations = face_recognition.face_locations(rgb_image)
    if len(face_locations) != 1:
        print("Error: The image must contain exactly one face.")
        return False

    face_encoding = face_recognition.face_encodings(rgb_image, face_locations)[0]

    try:
        # Save student data to the database
        conn = sqlite3.connect("models/student_data.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, batch, enrollment_number) VALUES (?, ?, ?)",
                       (name, batch, enrollment_number))
        student_id = cursor.lastrowid
        conn.commit()

        # Save face encoding using utility function
        save_face_encoding(student_id, face_encoding)
        print(f"Student '{name}' registered successfully!")

        return True

    except sqlite3.Error as db_error:
        print(f"Database error: {db_error}")
        return False

    except Exception as error:
        print(f"Unexpected error: {error}")
        return False

    finally:
        if conn:
            conn.close()

# Uncomment the lines below to test the script independently
# if __name__ == "__main__":
#     initialize_db()
#     register_student("John Doe", "CS2024", "12345")
