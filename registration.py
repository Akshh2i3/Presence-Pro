import cv2
import face_recognition
import sqlite3
from utils import initialize_db, save_face_encoding

def capture_live_photo():
    # Open the camera (default camera 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    print("Press 's' to take a snapshot and 'q' to quit.")
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Display the resulting frame
        cv2.imshow('Live Camera Feed', frame)

        # Wait for user input
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):  # Press 's' to capture the image
            print("Image captured!")
            captured_image = frame
            break
        elif key == ord('q'):  # Press 'q' to quit without capturing
            print("Camera feed closed.")
            captured_image = None
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

    return captured_image

def register_student(name, batch, enrollment_number):
    # Capture live photo from the camera
    initialize_db()
    image = capture_live_photo()
    
    if image is None:
        print("No image captured. Registration failed.")
        return False

    # Convert the captured image to RGB format
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

# if __name__ == "__main__":
#     initialize_db()
#     # Test registration
#     register_student("John Doe", "CS2024", "12345")
