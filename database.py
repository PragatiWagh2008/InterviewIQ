import hashlib
import hmac
import json
import os
import re
import secrets
import sqlite3
import zipfile
from datetime import date, datetime, timedelta
from xml.etree import ElementTree

DB_PATH = "interview_iq.db"
REMEMBER_PATH = ".interviewiq_remember.json"

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


def _conn():
    return sqlite3.connect(DB_PATH)


def hash_password(password):
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 120000)
    return f"pbkdf2${salt}${digest.hex()}"


def verify_password(password, stored):
    if not stored:
        return False
    if stored.startswith("pbkdf2$"):
        try:
            _, salt, digest = stored.split("$", 2)
        except ValueError:
            return False
        check = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 120000)
        return hmac.compare_digest(check.hex(), digest)
    # Legacy plaintext passwords
    return hmac.compare_digest(password, stored)


def init_db():
    conn = _conn()
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
            photo BLOB,
            target_company TEXT DEFAULT 'Google',
            difficulty TEXT DEFAULT 'Easy'
        )
    """)
    # Migrate older DBs missing newer columns
    cursor.execute("PRAGMA table_info(users)")
    cols = {row[1] for row in cursor.fetchall()}
    if "target_company" not in cols:
        cursor.execute("ALTER TABLE users ADD COLUMN target_company TEXT DEFAULT 'Google'")
    if "difficulty" not in cols:
        cursor.execute("ALTER TABLE users ADD COLUMN difficulty TEXT DEFAULT 'Easy'")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            designation TEXT,
            company TEXT,
            difficulty TEXT,
            avg_score INTEGER,
            avg_words INTEGER,
            answers_json TEXT,
            created_at TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mcq_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            score INTEGER,
            total INTEGER,
            difficulty TEXT,
            created_at TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            activity_date TEXT NOT NULL,
            activity_type TEXT NOT NULL,
            UNIQUE(email, activity_date, activity_type)
        )
    """)

    # Always ensure a demo user exists
    cursor.execute("SELECT id, password FROM users WHERE email = ?", ("demo@example.com",))
    demo = cursor.fetchone()
    if not demo:
        cursor.execute("""
            INSERT INTO users (fullname, email, password, branch, designation, resume_text, photo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "Alex Carter", "demo@example.com", hash_password("password123"),
            "Computer Science Engineering", "AI Engineer", MOCK_RESUME_TEMPLATE, None
        ))
    else:
        # Upgrade legacy plaintext demo password if needed
        if not str(demo[1]).startswith("pbkdf2$"):
            cursor.execute(
                "UPDATE users SET password = ? WHERE email = ?",
                (hash_password("password123"), "demo@example.com")
            )

    # Upgrade any remaining plaintext passwords for known users on next verify
    conn.commit()
    conn.close()


init_db()


def _row_to_user(row):
    if not row:
        return None
    return {
        "fullname": row[0],
        "email": row[1],
        "password": row[2],
        "branch": row[3],
        "designation": row[4],
        "resume_text": row[5],
        "photo": row[6],
        "target_company": row[7] if len(row) > 7 else "Google",
        "difficulty": row[8] if len(row) > 8 else "Easy",
    }


def get_user(email):
    conn = _conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT fullname, email, password, branch, designation, resume_text, photo,
               target_company, difficulty
        FROM users WHERE lower(email) = lower(?)
    """, (email,))
    user = _row_to_user(cursor.fetchone())
    conn.close()
    return user


def find_user(login_id):
    """Find user by email or full name (case-insensitive)."""
    login_id = (login_id or "").strip()
    if not login_id:
        return None
    conn = _conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT fullname, email, password, branch, designation, resume_text, photo,
               target_company, difficulty
        FROM users
        WHERE lower(email) = lower(?) OR lower(fullname) = lower(?)
        LIMIT 1
    """, (login_id, login_id))
    user = _row_to_user(cursor.fetchone())
    conn.close()
    return user


def authenticate(login_id, password):
    user = find_user(login_id)
    if not user or not verify_password(password, user["password"]):
        return None
    # Upgrade plaintext password hashes after successful login
    if not user["password"].startswith("pbkdf2$"):
        update_password(user["email"], password)
        user["password"] = hash_password(password)
    return user


def save_user(fullname, email, password, branch, designation, resume_text, photo_bytes):
    conn = _conn()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (fullname, email, password, branch, designation, resume_text, photo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (fullname, email, hash_password(password), branch, designation, resume_text, photo_bytes))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def update_password(email, new_password):
    conn = _conn()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password = ? WHERE lower(email) = lower(?)",
        (hash_password(new_password), email)
    )
    changed = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return changed


def update_user_preferences(email, company=None, difficulty=None):
    conn = _conn()
    cursor = conn.cursor()
    if company is not None:
        cursor.execute(
            "UPDATE users SET target_company = ? WHERE lower(email) = lower(?)",
            (company, email)
        )
    if difficulty is not None:
        cursor.execute(
            "UPDATE users SET difficulty = ? WHERE lower(email) = lower(?)",
            (difficulty, email)
        )
    conn.commit()
    conn.close()


def _extract_docx_text(path):
    """Extract plain text from a .docx using the stdlib (no python-docx required)."""
    texts = []
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml")
    root = ElementTree.fromstring(xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    for node in root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"):
        if node.text:
            texts.append(node.text)
    return " ".join(texts).strip()


def _extract_pdf_data(pdf_path):
    resume_text = ""
    photo_bytes = None
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text + "\n"
        for page in reader.pages:
            try:
                for image_file in page.images:
                    photo_bytes = image_file.data
                    break
            except Exception:
                continue
            if photo_bytes:
                break
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
    return resume_text.strip(), photo_bytes


def extract_resume_data(file_path):
    """
    Extract resume text (and optional photo) from PDF, DOCX, DOC, or TXT.
    Returns (resume_text, photo_bytes, error_message).
    """
    if not file_path or not os.path.exists(file_path):
        return "", None, "File not found."

    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == ".pdf":
            text, photo = _extract_pdf_data(file_path)
            if not text:
                return "", photo, "Could not extract text from this PDF. Try a text-based PDF."
            return text, photo, None
        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read().strip()
            if not text:
                return "", None, "The text file is empty."
            return text, None, None
        if ext == ".docx":
            text = _extract_docx_text(file_path)
            if not text:
                return "", None, "Could not extract text from this DOCX."
            return text, None, None
        if ext == ".doc":
            return "", None, "Legacy .doc is not supported. Please convert to PDF, DOCX, or TXT."
        return "", None, f"Unsupported file type: {ext or '(none)'}. Use PDF, DOCX, or TXT."
    except Exception as e:
        return "", None, f"Failed to read resume: {e}"


# Backward-compatible alias
def extract_pdf_data(pdf_path):
    text, photo, _err = extract_resume_data(pdf_path)
    return text, photo


def log_activity(email, activity_type):
    today = date.today().isoformat()
    conn = _conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO activity_log (email, activity_date, activity_type)
        VALUES (?, ?, ?)
    """, (email, today, activity_type))
    conn.commit()
    conn.close()


def save_interview_session(email, designation, company, difficulty, avg_score, avg_words, answers):
    conn = _conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO interview_sessions
        (email, designation, company, difficulty, avg_score, avg_words, answers_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        email, designation, company, difficulty, avg_score, avg_words,
        json.dumps(answers), datetime.now().isoformat(timespec="seconds")
    ))
    conn.commit()
    conn.close()
    log_activity(email, "interview")


def save_mcq_session(email, score, total, difficulty):
    conn = _conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO mcq_sessions (email, score, total, difficulty, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (email, score, total, difficulty, datetime.now().isoformat(timespec="seconds")))
    conn.commit()
    conn.close()
    log_activity(email, "mcq")


def get_streak(email):
    """Return current consecutive-day streak ending today or yesterday."""
    conn = _conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT activity_date FROM activity_log
        WHERE lower(email) = lower(?)
        ORDER BY activity_date DESC
    """, (email,))
    days = {row[0] for row in cursor.fetchall()}
    conn.close()
    if not days:
        return 0
    streak = 0
    d = date.today()
    # Allow streak to continue if last activity was yesterday
    if d.isoformat() not in days:
        d = d - timedelta(days=1)
        if d.isoformat() not in days:
            return 0
    while d.isoformat() in days:
        streak += 1
        d -= timedelta(days=1)
    return streak


def get_week_activity(email):
    """Return Mon-Sun activity counts for the current week (ints)."""
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    week_dates = [(monday + timedelta(days=i)).isoformat() for i in range(7)]
    conn = _conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT activity_date, COUNT(*) FROM activity_log
        WHERE lower(email) = lower(?) AND activity_date >= ? AND activity_date <= ?
        GROUP BY activity_date
    """, (email, week_dates[0], week_dates[6]))
    counts = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return [counts.get(d, 0) for d in week_dates]


def get_week_streak_flags(email):
    """Return list of (day_letter, achieved) for current week Mon-Sun."""
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    letters = ["M", "T", "W", "T", "F", "S", "S"]
    flags = []
    conn = _conn()
    cursor = conn.cursor()
    for i, letter in enumerate(letters):
        d = (monday + timedelta(days=i)).isoformat()
        cursor.execute("""
            SELECT 1 FROM activity_log
            WHERE lower(email) = lower(?) AND activity_date = ?
            LIMIT 1
        """, (email, d))
        flags.append((letter, cursor.fetchone() is not None))
    conn.close()
    return flags


def get_performance_summary(email):
    """Aggregate interview/MCQ stats for the progress dashboard."""
    conn = _conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT AVG(avg_score), COUNT(*) FROM interview_sessions
        WHERE lower(email) = lower(?)
    """, (email,))
    irow = cursor.fetchone()
    interview_avg = int(irow[0] or 0)
    interview_count = irow[1] or 0

    cursor.execute("""
        SELECT AVG(CASE WHEN total > 0 THEN 100.0 * score / total ELSE 0 END), COUNT(*)
        FROM mcq_sessions WHERE lower(email) = lower(?)
    """, (email,))
    mrow = cursor.fetchone()
    mcq_avg = int(mrow[0] or 0)
    mcq_count = mrow[1] or 0

    cursor.execute("""
        SELECT avg_score, designation FROM interview_sessions
        WHERE lower(email) = lower(?)
        ORDER BY id DESC LIMIT 5
    """, (email,))
    recent = cursor.fetchall()
    conn.close()

    total_sessions = interview_count + mcq_count
    if total_sessions == 0:
        overall = 0
    else:
        parts = []
        if interview_count:
            parts.append(interview_avg)
        if mcq_count:
            parts.append(mcq_avg)
        overall = int(sum(parts) / len(parts))

    # Derive simple strengths/weaknesses from recent interview scores
    strengths = []
    weaknesses = []
    if interview_avg >= 75:
        strengths.append("Technical interview responses")
    if mcq_avg >= 70:
        strengths.append("MCQ fundamentals")
    if interview_count >= 2:
        strengths.append("Consistent practice")
    if interview_avg and interview_avg < 65:
        weaknesses.append("Interview depth & keywords")
    if mcq_avg and mcq_avg < 60:
        weaknesses.append("MCQ accuracy")
    if total_sessions < 2:
        weaknesses.append("Need more practice sessions")
    if not strengths:
        strengths.append("Getting started")
    if not weaknesses:
        weaknesses.append("Keep refining project metrics")

    return {
        "overall": overall,
        "interview_avg": interview_avg,
        "interview_count": interview_count,
        "mcq_avg": mcq_avg,
        "mcq_count": mcq_count,
        "streak": get_streak(email),
        "week_activity": get_week_activity(email),
        "week_flags": get_week_streak_flags(email),
        "strengths": strengths[:3],
        "weaknesses": weaknesses[:3],
        "recent_interviews": recent,
    }


def load_quiz_data(difficulty="Easy"):
    file_path = "skills.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    else:
        data = {"questions": []}

    questions = data.get("questions", [])
    # Filter by difficulty when tagged; otherwise include all
    filtered = [q for q in questions if q.get("difficulty", "Easy") == difficulty]
    if not filtered:
        filtered = questions
    return {"questions": filtered}


def save_remembered_email(email):
    try:
        with open(REMEMBER_PATH, "w", encoding="utf-8") as f:
            json.dump({"email": email}, f)
    except OSError:
        pass


def load_remembered_email():
    try:
        if os.path.exists(REMEMBER_PATH):
            with open(REMEMBER_PATH, "r", encoding="utf-8") as f:
                return json.load(f).get("email")
    except (OSError, json.JSONDecodeError):
        pass
    return None


def clear_remembered_email():
    try:
        if os.path.exists(REMEMBER_PATH):
            os.remove(REMEMBER_PATH)
    except OSError:
        pass


def improve_skill_extraction(text):
    """Shared skill extraction used by resume insights."""
    if not text:
        return []

    skills_match = re.search(r"SKILLS\s*\n(.*?)(?:\n\s*\n[A-Z][A-Z &/]+|\Z)", text, re.DOTALL | re.IGNORECASE)
    if skills_match:
        skills_block = skills_match.group(1)
        extracted = []
        for line in skills_block.split("\n"):
            line = line.strip().lstrip("-•*").strip()
            if not line:
                continue
            if ":" in line:
                line = line.split(":", 1)[1].strip()
            for skill in re.split(r"[,;/|]", line):
                skill = skill.strip()
                if skill and len(skill) < 40 and skill not in extracted:
                    extracted.append(skill)
        if extracted:
            return extracted

    common_skills = [
        "Python", "PyTorch", "TensorFlow", "Machine Learning", "Deep Learning",
        "NLP", "Natural Language Processing", "Computer Vision", "SQL", "Git",
        "C++", "C/C++", "Java", "HTML", "CSS", "JavaScript", "React", "Docker", "AWS",
        "System Design", "Kubernetes", "Linux", "R", "Go", "Rust", "Spark",
        "Pandas", "NumPy", "Scikit-learn", "Hugging Face", "OpenCV", "Flask", "Django"
    ]
    text_lower = text.lower()
    found = []
    for skill in common_skills:
        if skill.lower() in text_lower:
            found.append(skill)
    return found
