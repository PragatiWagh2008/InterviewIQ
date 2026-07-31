# InterviewIQ 🚀

InterviewIQ is an AI-powered desktop application designed to help tech professionals prepare for interviews. Built with Python and Tkinter, it provides a comprehensive suite of tools including AI-simulated mock interviews, resume parsing and insights, and MCQ practice tests tailored specifically for roles in Data Science, AI, and Software Engineering.

## ✨ Features

*   **User Authentication & Profiles:** Secure login and signup system with SQLite.
*   **Smart Resume Parsing:** Upload your PDF resume during registration. The app uses `pypdf` to extract your text, skills, and profile photo.
*   **AI Mock Interviews:** An interactive chat interface that simulates technical interviews. It asks role-specific questions (e.g., AI Engineer, NLP Researcher, Computer Vision Specialist) and evaluates your responses based on depth and keyword matching.
*   **Resume Insights:** Get a dynamic "Strength Score" dial, extracted core skills, and AI-generated optimization tips based on your uploaded resume.
*   **Performance Dashboard:** Track your daily streak, overall progress, strengths, weaknesses, and follow a recommended training roadmap.
*   **MCQ Practice:** Take technical multiple-choice quizzes to sharpen your fundamentals.

## 🛠️ Tech Stack

*   **Language:** Python 3.x
*   **GUI Framework:** Tkinter (Standard GUI library for Python)
*   **Database:** SQLite3
*   **PDF Parsing:** `pypdf`
*   **Image Processing:** `Pillow` (PIL)

## 📁 Project Structure

*   `main.py` - Application entry point and window manager.
*   `login.py` - Authentication screens (Welcome, Login, Signup) and resume upload logic.
*   `menu.py` - Base layout (Sidebar), Main Dashboard, and Resume Insights view.
*   `interview.py` - The core AI mock interview chat interface and evaluation logic.
*   `roadmap.py` - MCQ practice flow and performance tracking dashboard.
*   `database.py` - SQLite database initialization and CRUD operations.
*   `skills.json` - Data store for multiple-choice questions.

## 🚀 Installation & Setup

1. **Clone the repository** (or download the source code):
   ```bash
   git clone https://github.com/PragatiWagh2008/InterviewIQ.git
   cd InterviewIQ
   ```

2. **Create a virtual environment (Optional but recommended):**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```
   *(Note: The SQLite database `interview_iq.db` will be automatically initialized on the first run with a demo user).*
