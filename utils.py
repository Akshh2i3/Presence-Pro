import sqlite3
import pickle

def initialize_db():
    conn = sqlite3.connect("models/student_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT,
            batch TEXT,
            enrollment_number TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY,
            student_id INTEGER,
            subject TEXT,
            time_slot TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_face_encoding(student_id, encoding):
    try:
        with open("models/face_encodings.pkl", "rb") as f:
            data = pickle.load(f)
    except FileNotFoundError:
        data = {}

    data[student_id] = encoding
    with open("models/face_encodings.pkl", "wb") as f:
        pickle.dump(data, f)

def load_face_encodings():
    try:
        with open("models/face_encodings.pkl", "rb") as f:
            data = pickle.load(f)
    except FileNotFoundError:
        return [], []

    student_data = []
    known_encodings = []
    conn = sqlite3.connect("models/student_data.db")
    cursor = conn.cursor()
    for student_id, encoding in data.items():
        cursor.execute("SELECT id, name FROM students WHERE id = ?", (student_id,))
        result = cursor.fetchone()
        if result:
            student_data.append({"id": result[0], "name": result[1]})
            known_encodings.append(encoding)

    conn.close()
    return student_data, known_encodings

def mark_attendance(student_id, subject, time_slot):
    conn = sqlite3.connect("models/student_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (student_id, subject, time_slot) VALUES (?, ?, ?)",
                   (student_id, subject, time_slot))
    conn.commit()
    conn.close()
