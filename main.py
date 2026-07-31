import tkinter as tk
from tkinter import ttk
import sys
import os

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


class InterviewIQApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("InterviewIQ")
        self.geometry("1100x780")
        self.minsize(800, 600)
        self.configure(bg=COLORS["bg"])

        # ── Global ttk styles ────────────────────────────────────
        style = ttk.Style(self)
        style.theme_use("clam")

        # Combobox styling
        style.configure("TCombobox",
                         fieldbackground=COLORS["bg"],
                         background=COLORS["surface"],
                         foreground=COLORS["text"],
                         bordercolor=COLORS["border"],
                         arrowcolor=COLORS["primary"],
                         selectbackground=COLORS["primary_light"],
                         selectforeground=COLORS["text"])
        style.map("TCombobox",
                   bordercolor=[("focus", COLORS["primary"])],
                   lightcolor=[("focus", COLORS["primary"])])

        # Scrollbar styling
        style.configure("Vertical.TScrollbar",
                         background=COLORS["surface_alt"],
                         troughcolor=COLORS["surface"],
                         bordercolor=COLORS["border"],
                         arrowcolor=COLORS["text_muted"],
                         gripcount=0)
        style.map("Vertical.TScrollbar",
                   background=[("active", COLORS["border_light"])])

        # Global Session variables
        self.current_user_email = "demo@example.com"

        self.container = tk.Frame(self, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True)

        self.screens = {}

        for ScreenClass in (WelcomeScreen, LoginScreen, SignupScreen, MainDashboard,
                             ResumeView, MockInterviewView, McqPracticeView, PerformanceView):
            screen_name = ScreenClass.__name__
            frame = ScreenClass(parent=self.container, controller=self)
            self.screens[screen_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.show_screen("WelcomeScreen")

    def show_screen(self, screen_name):
        frame = self.screens[screen_name]
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()

if __name__ == "__main__":
    app = InterviewIQApp()
    app.mainloop()