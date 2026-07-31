import json
import os
import sqlite3

DB_PATH = "interview_iq.db"

MOCK_RESUME_TEMPLATE = """ARYAN DEKONDWAR
Chh. Sambhajinagar | +91-8446819553 | aryandekondwar6@gmail.com

TARGET ROLE
Artificial Intelligence and Machine Learning Intern

SUMMARY
- Dedicated undergraduate student with a keen interest in technology, problem-solving, and continuous learning.
- Seeking an internship opportunity to enhance technical and professional skills while contributing to projects through creativity, teamwork, and analytical thinking.

SKILLS
- Languages: C/C++, Python, Java, HTML/CSS
- Concepts: Problem Solving, Artificial Intelligence, Machine Learning

EDUCATION
Diploma in Artificial Intelligence and Machine Learning
Pursuing

Little Flower High School
SSC Percentage: 83%

CERTIFICATIONS
- C/C++
- MSCIT"""

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            branch TEXT,
            designation TEXT,
            resume_text TEXT,
            photo BLOB
        )
    """)
    # Insert a mock demo user if the database is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO users (fullname, email, password, branch, designation, resume_text, photo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('Alex Carter', 'demo@example.com', 'password123', 
              'Computer Science Engineering', 'Software Developer', MOCK_RESUME_TEMPLATE, None))
    conn.commit()
    conn.close()

# Auto-initialize on module import
init_db()

def get_user(email):
    """
    Retrieves user profile details by email.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT fullname, email, password, branch, designation, resume_text, photo
        FROM users WHERE email = ?
    """, (email,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "fullname": row[0],
            "email": row[1],
            "password": row[2],
            "branch": row[3],
            "designation": row[4],
            "resume_text": row[5],
            "photo": row[6]
        }
    return None

def extract_pdf_data(pdf_path):
    """
    Extracts text and the first photo/image from a PDF file.
    Returns a tuple: (resume_text, photo_bytes).
    """
    resume_text = ""
    photo_bytes = None
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        
        # Extract text page by page
        for page in reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text + "\n"
                
        # Extract first image/photo (if any)
        for page in reader.pages:
            for image_file in page.images:
                photo_bytes = image_file.data
                break
            if photo_bytes:
                break
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        
    return resume_text.strip(), photo_bytes

def save_user(fullname, email, password, branch, designation, resume_text, photo_bytes):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (fullname, email, password, branch, designation, resume_text, photo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (fullname, email, password, branch, designation, resume_text, photo_bytes))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def load_quiz_data():
    file_path = "skills.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return {
        "questions": [
            {
                "id": 1,
                "text": "Q1: A primary goal of Artificial Intelligence is...",
                "options": [
                    "A. Making artificial ideas",
                    "B. Mimicking human intelligence",
                    "C. Correct option",
                    "D. Creating network protocols"
                ],
                "correct": "C. Correct option"
            }
        ]
    }