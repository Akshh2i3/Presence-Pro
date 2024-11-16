import cv2
import face_recognition
from utils import load_face_encodings, mark_attendance

def capture_live_photo():
    """
    Captures a live photo using the default camera.
    Press 's' to capture the image and 'q' to quit without capturing.
    """
    # Open the default camera (camera index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return None

    print("Press 's' to take a snapshot or 'q' to quit.")

    captured_image = None
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Display the camera feed
        cv2.imshow('Live Camera Feed', frame)

        # Wait for user input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):  # Capture the image when 's' is pressed
            print("Image captured!")
            captured_image = frame
            break
        elif key == ord('q'):  # Quit without capturing
            print("Camera feed closed without capturing.")
            break

    # Release the camera and close any open windows
    cap.release()
    cv2.destroyAllWindows()

    return captured_image

def mark_attendance_from_live(subject, time_slot):
    """
    Captures a live photo, detects and identifies faces, and marks attendance.
    If a face is recognized from the registered encodings, attendance is marked.
    """
    captured_image = capture_live_photo()
    if captured_image is None:
        print("No image captured. Attendance not marked.")
        return

    # Convert the image to RGB format for face recognition
    rgb_image = cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB)

    # Detect face locations and encodings in the captured image
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    # Load known face encodings and corresponding student data
    student_data, known_encodings = load_face_encodings()

    if not face_encodings:
        print("No faces detected in the image.")
        return

    for face_encoding in face_encodings:
        # Compare the detected face encoding with known encodings
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
        if True in matches:
            matched_idx = matches.index(True)
            student_id = student_data[matched_idx]["id"]
            mark_attendance(student_id, subject, time_slot)
            print(f"Attendance marked for student ID: {student_id}")
        else:
            print("Face detected but not recognized as a registered student.")

    print("Attendance marking process completed.")
