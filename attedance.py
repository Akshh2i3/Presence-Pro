import cv2
import face_recognition
from utils import load_face_encodings, mark_attendance

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


def mark_attendance_from_live(subject, time_slot):
    # Capture live photo
    captured_image = capture_live_photo()
    
    if captured_image is None:
        print("No image captured, attendance not marked.")
        return

    # Convert the captured image to RGB format
    rgb_image = cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB)

    # Detect faces in the image
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    # Load registered face encodings
    student_data, known_encodings = load_face_encodings()

    for face_encoding in face_encodings:
        # Compare with known encodings
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
        if True in matches:
            matched_idx = matches.index(True)
            student_id = student_data[matched_idx]["id"]
            mark_attendance(student_id, subject, time_slot)
        else: 
            print('Student Identified is not Registered')



# if __name__ == "__main__":
#     # Test attendance marking from live image capture
#     mark_attendance_from_live("Mathematics", "10:00 AM")
