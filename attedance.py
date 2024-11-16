import cv2
import face_recognition
from utils import load_face_encodings, mark_attendance

def mark_attendance_from_image(image_path, subject, time_slot):
    # Load the group photo
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

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

    print("Attendance marked successfully!")

if __name__ == "__main__":
    # Test attendance marking
    mark_attendance_from_image("path/to/group_photo.jpg", "Mathematics", "10:00 AM")
