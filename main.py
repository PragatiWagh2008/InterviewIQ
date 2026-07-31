import tkinter as tk
from tkinter import ttk
import sys

# ── DPI Awareness (Windows) ──────────────────────────────────────
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

from login import WelcomeScreen, LoginScreen, SignupScreen
from menu import MainDashboard, ResumeView
from interview import MockInterviewView
from roadmap import McqPracticeView, PerformanceView
from theme import COLORS
from database import get_user, load_remembered_email


class InterviewIQApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("InterviewIQ")
        self.geometry("1100x780")
        self.minsize(800, 600)
        self.configure(bg=COLORS["bg"])

        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "TCombobox",
            fieldbackground=COLORS["bg"],
            background=COLORS["surface"],
            foreground=COLORS["text"],
            bordercolor=COLORS["border"],
            arrowcolor=COLORS["primary"],
            selectbackground=COLORS["primary_light"],
            selectforeground=COLORS["text"],
        )
        style.map(
            "TCombobox",
            bordercolor=[("focus", COLORS["primary"])],
            lightcolor=[("focus", COLORS["primary"])],
        )

        style.configure(
            "Vertical.TScrollbar",
            background=COLORS["surface_alt"],
            troughcolor=COLORS["surface"],
            bordercolor=COLORS["border"],
            arrowcolor=COLORS["text_muted"],
            gripcount=0,
        )
        style.map(
            "Vertical.TScrollbar",
            background=[("active", COLORS["border_light"])],
        )

        self.current_user_email = None
        self.target_company = "Google"
        self.difficulty = "Easy"

        self.container = tk.Frame(self, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True)

        self.screens = {}
        for ScreenClass in (
            WelcomeScreen,
            LoginScreen,
            SignupScreen,
            MainDashboard,
            ResumeView,
            MockInterviewView,
            McqPracticeView,
            PerformanceView,
        ):
            screen_name = ScreenClass.__name__
            frame = ScreenClass(parent=self.container, controller=self)
            self.screens[screen_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.show_screen("WelcomeScreen")

    def login_user(self, email):
        self.current_user_email = email
        user = get_user(email)
        if user:
            self.target_company = user.get("target_company") or "Google"
            self.difficulty = user.get("difficulty") or "Easy"

    def logout_user(self):
        self.current_user_email = None
        self.target_company = "Google"
        self.difficulty = "Easy"
        # Reset interview session so next login starts fresh
        interview = self.screens.get("MockInterviewView")
        if interview is not None:
            interview.session_active = False
        self.show_screen("WelcomeScreen")

    def show_screen(self, screen_name):
        protected = {
            "MainDashboard", "ResumeView", "MockInterviewView",
            "McqPracticeView", "PerformanceView"
        }
        if screen_name in protected and not self.current_user_email:
            remembered = load_remembered_email()
            if remembered and get_user(remembered):
                self.login_user(remembered)
            else:
                screen_name = "LoginScreen"

        frame = self.screens[screen_name]
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()


if __name__ == "__main__":
    app = InterviewIQApp()
    app.mainloop()
