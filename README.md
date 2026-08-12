# InterviewIQ 🚀

InterviewIQ is an AI-powered desktop application that helps tech professionals prepare for technical interviews. Built with Python and Tkinter, it combines a clean, modern UI (dark-ink sidebar, cream canvas, teal & coral accents) with a full interview-prep workflow: AI-simulated mock interviews, resume parsing with insights, MCQ quizzes, and a performance dashboard.

## ✨ Features

*   **User Authentication & Profiles:** Secure login/signup backed by SQLite (hashed passwords with `pbkdf2`), plus a "remember me" option.
*   **Smart Resume Parsing:** Upload a PDF, DOCX, or TXT resume during registration. The app extracts text, skills, and profile photo (via `pypdf`).
*   **AI Mock Interviews:** Interactive chat simulating technical interviews with role-specific question banks (AI Engineer, ML Engineer, Data Scientist, NLP Researcher, Computer Vision Specialist), difficulty scaling, keyword-based scoring, and a final performance report.
*   **Resume Insights:** A "Strength Score" dial, detected core skills, and actionable optimization tips based on your resume.
*   **MCQ Practice:** Company-aware multiple-choice quizzes that build fundamentals and feed your daily streak.
*   **Performance Dashboard:** Track overall progress ring, daily streak, weekly activity, strengths & weaknesses, and a recommended training roadmap.
*   **Optional AI Provider & Speech:** Plug in a real LLM for generated questions/evaluation, and real microphone input when the optional packages are installed.

## 🛠️ Tech Stack

*   **Language:** Python 3.x
*   **GUI Framework:** Tkinter (standard library)
*   **Database:** SQLite3
*   **PDF Parsing:** `pypdf`
*   **Image Processing:** `Pillow` (PIL)
*   **Config:** `python-dotenv` (optional `.env` for AI provider)

## 📁 Project Structure

*   `main.py` — Application entry point and screen/window manager.
*   `theme.py` — Central design system (colors, fonts, hover/focus helpers, card factory, logo & wave drawing).
*   `login.py` — Welcome, Login, and Signup screens plus resume upload logic.
*   `menu.py` — Base sidebar layout, Main Dashboard, and Resume Insights view.
*   `interview.py` — The AI mock interview chat interface and evaluation logic.
*   `roadmap.py` — MCQ practice flow and performance tracking dashboard.
*   `database.py` — SQLite initialization and CRUD operations.
*   `config.py` — Reads optional AI settings from `.env`.
*   `services/ai_service.py` — AI provider shim (falls back to local heuristics when no provider is configured).
*   `skills.json` — Data store for multiple-choice questions.

## 🚀 Installation & Setup

1. **Get the code:**
   ```bash
   git clone https://github.com/PragatiWagh2008/InterviewIQ.git
   cd InterviewIQ
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
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
   *Note: the SQLite database `interview_iq.db` is initialized automatically on first run with a demo user.*

### 🔑 Demo account

```
Email:    demo@example.com
Password: password123
```

### 🤖 Enabling a real AI provider (optional)

1. Copy `.env.example` to `.env`.
2. Fill in your provider details:
   ```env
   AI_API_KEY=your-api-key
   AI_MODEL=gpt-3.5-turbo
   AI_PROVIDER=openai
   ```
3. Install the provider client, e.g. `pip install openai`.

When configured, the mock interview uses provider-generated questions and AI answer evaluation. Without a provider, the app falls back to built-in question banks and heuristic scoring.

### 🎙️ Enabling speech input (optional)

Uncomment `speechrecognition` and `PyAudio` in `requirements.txt` and install them. The mock interview's "Speech Assist" button will then capture real microphone input; otherwise it inserts a practice prompt instead.

> **Note:** PyAudio requires an extra step on Windows (`pip install pipwin && pipwin install pyaudio`) or a prebuilt wheel — see the [PyAudio documentation](https://people.csail.mit.edu/hubert/pyaudio/).
