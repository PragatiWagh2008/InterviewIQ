import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import save_user, extract_pdf_data, get_user


def _responsive_card(parent, max_width, max_height):
    """Create a centered card that scales with the window but caps at a max size."""
    card = tk.Frame(parent, bg="white", highlightbackground="#E2E8F0", highlightthickness=1, bd=0)
    card.place(relx=0.5, rely=0.5, anchor="center", width=max_width, height=max_height)

    def _resize(event):
        w = min(max_width, int(event.width * 0.85))
        h = min(max_height, int(event.height * 0.92))
        card.place_configure(width=w, height=h)

    parent.bind("<Configure>", _resize)
    return card


class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F8FAFC")
        
        card = _responsive_card(self, max_width=420, max_height=500)

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
        self.controller = controller
        self.show_pwd = False
        
        card = _responsive_card(self, max_width=420, max_height=560)

        tk.Button(card, text="← Back", font=("Helvetica", 10, "bold"), fg="#64748B", bg="white", bd=0, activebackground="white", cursor="hand2", command=lambda: controller.show_screen("WelcomeScreen")).pack(anchor="w", padx=35, pady=(25, 10))
        
        tk.Label(card, text="Welcome Back", font=("Helvetica", 22, "bold"), fg="#0F172A", bg="white").pack(anchor="w", padx=35, pady=2)
        tk.Label(card, text="Login to your account", font=("Helvetica", 11), fg="#64748B", bg="white").pack(anchor="w", padx=35, pady=(0, 15))

        tk.Label(card, text="Username or Email", font=("Helvetica", 10, "bold"), fg="#475569", bg="white").pack(anchor="w", padx=35, pady=(10, 4))
        self.ent_user = tk.Entry(card, font=("Helvetica", 12), bg="#F8FAFC", fg="#0F172A", bd=1, relief="solid")
        self.ent_user.pack(fill="x", padx=35, ipady=8)

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

        tk.Button(card, text="Login", font=("Helvetica", 12, "bold"), bg="#2563EB", fg="white", activebackground="#1D4ED8", activeforeground="white", bd=0, cursor="hand2", command=self.login).pack(fill="x", padx=35, pady=(20, 10), ipady=10)

    def login(self):
        email = self.ent_user.get().strip()
        password = self.ent_pass.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password!")
            return
            
        user = get_user(email)
        if not user or user["password"] != password:
            messagebox.showerror("Error", "Invalid email or password!")
            return
            
        self.controller.current_user_email = email
        self.controller.show_screen("MainDashboard")

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
        self.controller = controller
        
        card = _responsive_card(self, max_width=460, max_height=720)

        # Scrollable interior so content doesn't clip on shorter windows
        canvas_scroll = tk.Canvas(card, bg="white", bd=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(card, orient="vertical", command=canvas_scroll.yview)
        self.inner = tk.Frame(canvas_scroll, bg="white")

        self.inner.bind("<Configure>", lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all")))
        canvas_scroll.create_window((0, 0), window=self.inner, anchor="nw")
        canvas_scroll.configure(yscrollcommand=scrollbar.set)

        canvas_scroll.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel for scroll
        def _on_mousewheel(event):
            canvas_scroll.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas_scroll.bind_all("<MouseWheel>", _on_mousewheel)

        # Sync inner frame width with canvas width
        def _sync_width(event):
            canvas_scroll.itemconfig("all", width=event.width)
        canvas_scroll.bind("<Configure>", _sync_width)

        # --- Form content inside self.inner ---
        inner = self.inner

        tk.Button(inner, text="← Back", font=("Helvetica", 10, "bold"), fg="#64748B", bg="white", bd=0, activebackground="white", cursor="hand2", command=lambda: controller.show_screen("WelcomeScreen")).pack(anchor="w", padx=40, pady=(15, 5))
        
        tk.Label(inner, text="Create Your Account", font=("Helvetica", 22, "bold"), fg="#0F172A", bg="white").pack(anchor="w", padx=40, pady=2)
        tk.Label(inner, text="Get started with InterviewIQ", font=("Helvetica", 11), fg="#64748B", bg="white").pack(anchor="w", padx=40, pady=(0, 10))

        tk.Label(inner, text="Full Name", font=("Helvetica", 10, "bold"), fg="#475569", bg="white").pack(anchor="w", padx=40, pady=(4, 1))
        self.ent_fullname = tk.Entry(inner, font=("Helvetica", 11), bg="#F8FAFC", bd=1, relief="solid")
        self.ent_fullname.pack(fill="x", padx=40, ipady=4)

        tk.Label(inner, text="Email", font=("Helvetica", 10, "bold"), fg="#475569", bg="white").pack(anchor="w", padx=40, pady=(4, 1))
        self.ent_email = tk.Entry(inner, font=("Helvetica", 11), bg="#F8FAFC", bd=1, relief="solid")
        self.ent_email.pack(fill="x", padx=40, ipady=4)

        tk.Label(inner, text="Password", font=("Helvetica", 10, "bold"), fg="#475569", bg="white").pack(anchor="w", padx=40, pady=(4, 1))
        self.ent_pass = tk.Entry(inner, font=("Helvetica", 11), bg="#F8FAFC", bd=1, relief="solid", show="*")
        self.ent_pass.pack(fill="x", padx=40, ipady=4)

        tk.Label(inner, text="Confirm Password", font=("Helvetica", 10, "bold"), fg="#475569", bg="white").pack(anchor="w", padx=40, pady=(4, 1))
        self.ent_confirm_pass = tk.Entry(inner, font=("Helvetica", 11), bg="#F8FAFC", bd=1, relief="solid", show="*")
        self.ent_confirm_pass.pack(fill="x", padx=40, ipady=4)

        # AI/Tech Targeted Dropdown Menus
        tk.Label(inner, text="Branch", font=("Helvetica", 10, "bold"), fg="#475569", bg="white").pack(anchor="w", padx=40, pady=(4, 1))
        self.b_combo = ttk.Combobox(inner, values=["Computer Science Engineering", "Artificial Intelligence & Data Science", "Information Technology", "Electronics & Communication"], font=("Helvetica", 11), state="readonly")
        self.b_combo.set("Artificial Intelligence & Data Science")
        self.b_combo.pack(fill="x", padx=40, ipady=2)

        tk.Label(inner, text="Designation", font=("Helvetica", 10, "bold"), fg="#475569", bg="white").pack(anchor="w", padx=40, pady=(4, 1))
        self.d_combo = ttk.Combobox(inner, values=["AI Engineer", "Machine Learning Engineer", "Data Scientist", "NLP Researcher", "Computer Vision Specialist"], font=("Helvetica", 11), state="readonly")
        self.d_combo.set("AI Engineer")
        self.d_combo.pack(fill="x", padx=40, ipady=2)

        self.resume_path = None
        self.btn_resume = tk.Button(inner, text="Upload Resume", font=("Helvetica", 11), bg="#EFF6FF", fg="#2563EB", bd=1, relief="groove", cursor="hand2", command=self.upload_resume)
        self.btn_resume.pack(fill="x", padx=40, pady=(12, 12), ipady=6)
        tk.Button(inner, text="Complete Profile", font=("Helvetica", 12, "bold"), bg="#2563EB", fg="white", activebackground="#1D4ED8", activeforeground="white", bd=0, cursor="hand2", command=self.register).pack(fill="x", padx=40, ipady=8, pady=(0, 15))

    def upload_resume(self):
        import os
        file_path = filedialog.askopenfilename(
            title="Select Resume",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("Word documents", "*.docx;*.doc"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.resume_path = file_path
            filename = os.path.basename(file_path)
            if len(filename) > 25:
                filename = filename[:22] + "..."
            self.btn_resume.config(text=f"✓ {filename}", fg="#16A34A", bg="#F0FDF4")

    def register(self):
        fullname = self.ent_fullname.get().strip()
        email = self.ent_email.get().strip()
        password = self.ent_pass.get()
        confirm_pass = self.ent_confirm_pass.get()

        if not fullname or not email or not password or not confirm_pass:
            messagebox.showerror("Error", "All fields are required!")
            return

        if "@" not in email:
            messagebox.showerror("Error", "Please enter a valid email address!")
            return

        if password != confirm_pass:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if not self.resume_path:
            messagebox.showerror("Error", "Please upload your resume!")
            return

        # Extract text and photo from the PDF
        resume_text, photo_bytes = extract_pdf_data(self.resume_path)
        
        # Save to database
        branch = self.b_combo.get()
        designation = self.d_combo.get()
        
        success = save_user(fullname, email, password, branch, designation, resume_text, photo_bytes)
        
        if not success:
            messagebox.showerror("Error", "Email is already registered!")
            return

        # Navigate to Dashboard on successful registration
        self.controller.show_screen("MainDashboard")