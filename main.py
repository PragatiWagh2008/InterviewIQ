import tkinter as tk
from login import WelcomeScreen, LoginScreen, SignupScreen
from menu import MainDashboard
from interview import MockInterviewView
from roadmap import McqPracticeView, PerformanceView

class InterviewIQApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("InterviewIQ")
        self.geometry("1100x780")
        self.configure(bg="#F8FAFC")

        self.container = tk.Frame(self, bg="#F8FAFC")
        self.container.pack(fill="both", expand=True)

        self.screens = {}

        for ScreenClass in (WelcomeScreen, LoginScreen, SignupScreen, MainDashboard, 
                             MockInterviewView, McqPracticeView, PerformanceView):
            screen_name = ScreenClass.__name__
            frame = ScreenClass(parent=self.container, controller=self)
            self.screens[screen_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.show_screen("WelcomeScreen")

    def show_screen(self, screen_name):
        frame = self.screens[screen_name]
        frame.tkraise()

if __name__ == "__main__":
    app = InterviewIQApp()
    app.mainloop()