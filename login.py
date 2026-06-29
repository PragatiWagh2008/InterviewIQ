import tkinter as tk
from tkinter import ttk

class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F8FAFC")
        
        card = tk.Frame(self, bg="white", highlightbackground="#E2E8F0", highlightthickness=1, bd=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=500)

        canvas = tk.Canvas(card, width=60, height=60, bg="white", bd=0, highlightthickness=0)
        canvas.pack(pady=(40, 15))
        canvas.create_polygon(30, 10, 10, 50, 50, 50, fill="#2563EB", outline="")
        canvas.create_polygon(30, 25, 20, 45, 40, 45, fill="white", outline="")

        tk.Label(card, text="InterviewIQ", font=("Helvetica", 24, "bold"), fg="#0F172A", bg="white").pack(pady=2)
        tk.Label(card, text="An AI-powered interview preparation platform", font=("Helvetica", 11), fg="#64748B", bg="white").pack(pady=(0, 30))

        btn_login = tk.Button(card, text="I have an account", font=("Helvetica", 12, "bold"), bg="#2563EB", fg="white", 
                              activebackground="#1D4ED8", activeforeground="white", bd=0, cursor="hand2", command=lambda: controller.show_screen("LoginScreen"))
        btn_login.pack(fill="x", padx=45, pady=10, ipady=10)
        tk.Label(card, text="Login to continue", font=("Helvetica", 9), fg="#94A3B8", bg="white").pack()

        btn_signup = tk.Button(card, text="I'm new here", font=("Helvetica", 12, "bold"), bg="#FFFFFF", fg="#2563EB", 
                               highlightbackground="#CBD5E1", highlightthickness=1, bd=0, activebackground="#F1F5F9", cursor="hand2", command=lambda: controller.show_screen("SignupScreen"))
        btn_signup.pack(fill="x", padx=45, pady=(20, 5), ipady=10)
        tk.Label(card, text="Create a new account", font=("Helvetica", 9), fg="#94A3B8", bg="white").pack()


class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F8FAFC")
        self.show_pwd = False
        
        card = tk.Frame(self, bg="white", highlightbackground="#E2E8F0", highlightthickness=1, bd=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=560)

        tk.Button(card, text="← Back", font=("Helvetica", 10, "bold"), fg="#64748B", bg="white", bd=0, activebackground="white", cursor="hand2", command=lambda: controller.show_screen("WelcomeScreen")).pack(anchor="w", padx=35, pady=(25, 10))
        
        tk.Label(card, text="Welcome Back", font=("Helvetica", 22, "bold"), fg="#0F172A", bg="white").pack(anchor="w", padx=35, pady=2)
        tk.Label(card, text="Login to your account", font=("Helvetica", 11), fg="#64748B", bg="white").pack(anchor="w", padx=35, pady=(0, 15))

        tk.Label(card, text="Username or Email", font=("Helvetica", 10, "bold"), fg="#475569", bg="white").pack(anchor="w", padx=35, pady=(10, 4))
        ent_user = tk.Entry(card, font=("Helvetica", 12), bg="#F8FAFC", fg="#0F172A", bd=1, relief="solid")
        ent_user.pack(fill="x", padx=35, ipady=8)

        tk.Label(card, text="Password", font=("Helvetica", 10, "bold"), fg="#475569", bg="white").pack(anchor="w", padx=35, pady=(15, 4))
        self.ent_pass = tk.Entry(card, font=("Helvetica", 12), bg="#F8FAFC", fg="#0F172A", bd=1, relief="solid", show="*")
        self.ent_pass.pack(fill="x", padx=35, ipady=8)

        # Options Row: Show Password, Remember Me & Forgot Password
        opt_frame = tk.Frame(card, bg="white")
        opt_frame.pack(fill="x", padx=35, pady=12)

        self.rem_var = tk.BooleanVar()
        tk.Checkbutton(opt_frame, text="Remember me", variable=self.rem_var, font=("Helvetica", 10), bg="white", fg="#475569", activebackground="white", bd=0).pack(side="left")
        
        btn_show = tk.Button(opt_frame, text="👁 Show", font=("Helvetica", 9, "bold"), fg="#2563EB", bg="white", bd=0, cursor="hand2", activebackground="white", command=self.toggle_password)
        btn_show.pack(side="left", padx=10)

        tk.Button(opt_frame, text="Forgot Password?", font=("Helvetica", 10), fg="#2563EB", bg="white", bd=0, cursor="hand2", activebackground="white").pack(side="right")

        tk.Button(card, text="Login", font=("Helvetica", 12, "bold"), bg="#2563EB", fg="white", activebackground="#1D4ED8", activeforeground="white", bd=0, cursor="hand2", command=lambda: controller.show_screen("MainDashboard")).pack(fill="x", padx=35, pady=(20, 10), ipady=10)

    def toggle_password(self):
        if self.show_pwd:
            self.ent_pass.config(show="*")
            self.show_pwd = False
        else:
            self.ent_pass.config(show="")
            self.show_pwd = True


class SignupScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F8FAFC")
        
        card = tk.Frame(self, bg="white", highlightbackground="#E2E8F0", highlightthickness=1, bd=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=460, height=660)

        tk.Button(card, text="← Back", font=("Helvetica", 10, "bold"), fg="#64748B", bg="white", bd=0, activebackground="white", cursor="hand2", command=lambda: controller.show_screen("WelcomeScreen")).pack(anchor="w", padx=40, pady=(20, 5))
        
        tk.Label(card, text="Create Your Account", font=("Helvetica", 22, "bold"), fg="#0F172A", bg="white").pack(anchor="w", padx=40, pady=2)
        tk.Label(card, text="Get started with InterviewIQ", font=("Helvetica", 11), fg="#64748B", bg="white").pack(anchor="w", padx=40, pady=(0, 15))

        tk.Label(card, text="Full Name", font=("Helvetica", 10, "bold"), fg="#475569", bg="white").pack(anchor="w", padx=40, pady=(5, 2))
        tk.Entry(card, font=("Helvetica", 11), bg="#F8FAFC", bd=1, relief="solid").pack(fill="x", padx=40, ipady=6)

        tk.Label(card, text="Email", font=("Helvetica", 10, "bold"), fg="#475569", bg="white").pack(anchor="w", padx=40, pady=(5, 2))
        tk.Entry(card, font=("Helvetica", 11), bg="#F8FAFC", bd=1, relief="solid").pack(fill="x", padx=40, ipady=6)

        # AI/Tech Targeted Dropdown Menus
        tk.Label(card, text="Branch", font=("Helvetica", 10, "bold"), fg="#475569", bg="white").pack(anchor="w", padx=40, pady=(5, 2))
        b_combo = ttk.Combobox(card, values=["Computer Science Engineering", "Artificial Intelligence & Data Science", "Information Technology", "Electronics & Communication"], font=("Helvetica", 11), state="readonly")
        b_combo.set("Artificial Intelligence & Data Science")
        b_combo.pack(fill="x", padx=40, ipady=4)

        tk.Label(card, text="Designation", font=("Helvetica", 10, "bold"), fg="#475569", bg="white").pack(anchor="w", padx=40, pady=(5, 2))
        d_combo = ttk.Combobox(card, values=["AI Engineer", "Machine Learning Engineer", "Data Scientist", "NLP Researcher", "Computer Vision Specialist"], font=("Helvetica", 11), state="readonly")
        d_combo.set("AI Engineer")
        d_combo.pack(fill="x", padx=40, ipady=4)

        tk.Button(card, text="Upload Resume", font=("Helvetica", 11), bg="#EFF6FF", fg="#2563EB", bd=1, relief="groove", cursor="hand2").pack(fill="x", padx=40, pady=15, ipady=8)
        tk.Button(card, text="Complete Profile", font=("Helvetica", 12, "bold"), bg="#2563EB", fg="white", activebackground="#1D4ED8", activeforeground="white", bd=0, cursor="hand2", command=lambda: controller.show_screen("MainDashboard")).pack(fill="x", padx=40, ipady=10)