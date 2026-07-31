import os
import re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog

from database import (
    save_user, extract_resume_data, authenticate, update_password,
    save_remembered_email, load_remembered_email, clear_remembered_email, get_user
)
from theme import COLORS, get_font, add_hover, add_focus_glow, bind_mousewheel


def _responsive_card(parent, max_width, max_height):
    """Create a centered card that scales with the window but caps at a max size."""
    card = tk.Frame(parent, bg=COLORS["surface"],
                    highlightbackground=COLORS["border"], highlightthickness=1, bd=0)
    card.place(relx=0.5, rely=0.5, anchor="center", width=max_width, height=max_height)

    _resize_id = [None]

    def _resize(event):
        if _resize_id[0]:
            parent.after_cancel(_resize_id[0])

        def _apply():
            w = min(max_width, int(event.width * 0.85))
            h = min(max_height, int(event.height * 0.92))
            card.place_configure(width=w, height=h)

        _resize_id[0] = parent.after(30, _apply)

    parent.bind("<Configure>", _resize)
    return card


class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg"])

        card = _responsive_card(self, max_width=420, max_height=500)

        canvas = tk.Canvas(card, width=60, height=60, bg=COLORS["surface"], bd=0, highlightthickness=0)
        canvas.pack(pady=(40, 15))
        canvas.create_polygon(30, 10, 10, 50, 50, 50, fill=COLORS["primary"], outline="")
        canvas.create_polygon(30, 25, 20, 45, 40, 45, fill=COLORS["surface"], outline="")

        tk.Label(card, text="InterviewIQ", font=get_font("h1"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(pady=2)
        tk.Label(card, text="An AI-powered interview preparation platform",
                 font=get_font("body"), fg=COLORS["text_muted"], bg=COLORS["surface"]).pack(pady=(0, 30))

        btn_login = tk.Button(card, text="I have an account", font=get_font("btn"),
                              bg=COLORS["primary"], fg="white",
                              activebackground=COLORS["primary_hover"], activeforeground="white",
                              bd=0, cursor="hand2",
                              command=lambda: controller.show_screen("LoginScreen"))
        btn_login.pack(fill="x", padx=45, pady=10, ipady=10)
        add_hover(btn_login, enter_bg=COLORS["primary_hover"], leave_bg=COLORS["primary"])

        tk.Label(card, text="Login to continue", font=get_font("caption"),
                 fg=COLORS["text_faint"], bg=COLORS["surface"]).pack()

        btn_signup = tk.Button(card, text="I'm new here", font=get_font("btn"),
                               bg=COLORS["surface"], fg=COLORS["primary"],
                               highlightbackground=COLORS["border_light"], highlightthickness=1,
                               bd=0, activebackground=COLORS["surface_alt"], cursor="hand2",
                               command=lambda: controller.show_screen("SignupScreen"))
        btn_signup.pack(fill="x", padx=45, pady=(20, 5), ipady=10)
        add_hover(btn_signup, enter_bg=COLORS["primary_light"], leave_bg=COLORS["surface"])

        tk.Label(card, text="Create a new account", font=get_font("caption"),
                 fg=COLORS["text_faint"], bg=COLORS["surface"]).pack()


def _validate_email(value: str) -> bool:
    if not value:
        return False
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value.strip()))


def _validate_fullname(value: str) -> bool:
    if not value:
        return False
    trimmed = value.strip()
    return len(trimmed) >= 3 and bool(re.search(r"[A-Za-z]", trimmed))


def _validate_password(value: str) -> bool:
    return bool(value and len(value) >= 8)


class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg"])
        self.controller = controller
        self.show_pwd = False

        card = _responsive_card(self, max_width=420, max_height=560)

        btn_back = tk.Button(card, text="← Back", font=get_font("small_b"),
                             fg=COLORS["text_muted"], bg=COLORS["surface"], bd=0,
                             activebackground=COLORS["surface"], cursor="hand2",
                             command=lambda: controller.show_screen("WelcomeScreen"))
        btn_back.pack(anchor="w", padx=35, pady=(25, 10))
        add_hover(btn_back, enter_fg=COLORS["primary"], leave_fg=COLORS["text_muted"])

        tk.Label(card, text="Welcome Back", font=get_font("h1"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=35, pady=2)
        tk.Label(card, text="Login to your account", font=get_font("body"),
                 fg=COLORS["text_muted"], bg=COLORS["surface"]).pack(anchor="w", padx=35, pady=(0, 15))

        tk.Label(card, text="Email or Full Name", font=get_font("small_b"),
                 fg=COLORS["text_secondary"], bg=COLORS["surface"]).pack(anchor="w", padx=35, pady=(10, 4))
        self.ent_user = tk.Entry(card, font=get_font("btn"), bg=COLORS["bg"], fg=COLORS["text"],
                                 bd=1, relief="solid", highlightthickness=1,
                                 highlightbackground=COLORS["border"], highlightcolor=COLORS["border"])
        self.ent_user.pack(fill="x", padx=35, ipady=8)
        add_focus_glow(self.ent_user)

        tk.Label(card, text="Password", font=get_font("small_b"),
                 fg=COLORS["text_secondary"], bg=COLORS["surface"]).pack(anchor="w", padx=35, pady=(15, 4))
        self.ent_pass = tk.Entry(card, font=get_font("btn"), bg=COLORS["bg"], fg=COLORS["text"],
                                 bd=1, relief="solid", show="*", highlightthickness=1,
                                 highlightbackground=COLORS["border"], highlightcolor=COLORS["border"])
        self.ent_pass.pack(fill="x", padx=35, ipady=8)
        add_focus_glow(self.ent_pass)

        opt_frame = tk.Frame(card, bg=COLORS["surface"])
        opt_frame.pack(fill="x", padx=35, pady=12)

        self.rem_var = tk.BooleanVar()
        tk.Checkbutton(opt_frame, text="Remember me", variable=self.rem_var, font=get_font("small"),
                       bg=COLORS["surface"], fg=COLORS["text_secondary"], activebackground=COLORS["surface"],
                       bd=0).pack(side="left")

        btn_show = tk.Button(opt_frame, text="Show", font=get_font("caption_b"),
                             fg=COLORS["primary"], bg=COLORS["surface"], bd=0, cursor="hand2",
                             activebackground=COLORS["surface"], command=self.toggle_password)
        btn_show.pack(side="left", padx=10)
        add_hover(btn_show, enter_fg=COLORS["primary_hover"], leave_fg=COLORS["primary"])

        btn_forgot = tk.Button(opt_frame, text="Forgot Password?", font=get_font("small"),
                               fg=COLORS["primary"], bg=COLORS["surface"], bd=0, cursor="hand2",
                               activebackground=COLORS["surface"], command=self.forgot_password)
        btn_forgot.pack(side="right")
        add_hover(btn_forgot, enter_fg=COLORS["primary_hover"], leave_fg=COLORS["primary"])

        btn_submit = tk.Button(card, text="Login", font=get_font("btn"), bg=COLORS["primary"], fg="white",
                               activebackground=COLORS["primary_hover"], activeforeground="white",
                               bd=0, cursor="hand2", command=self.login)
        btn_submit.pack(fill="x", padx=35, pady=(20, 10), ipady=10)
        add_hover(btn_submit, enter_bg=COLORS["primary_hover"], leave_bg=COLORS["primary"])

        tk.Label(card, text="Demo: demo@example.com / password123", font=get_font("caption"),
                 fg=COLORS["text_faint"], bg=COLORS["surface"]).pack(pady=(0, 10))

    def on_show(self):
        remembered = load_remembered_email()
        if remembered and get_user(remembered):
            self.ent_user.delete(0, tk.END)
            self.ent_user.insert(0, remembered)
            self.rem_var.set(True)
            self.ent_pass.focus_set()
        else:
            if remembered:
                clear_remembered_email()
            self.ent_pass.focus_set() if self.ent_user.get() else self.ent_user.focus_set()

    def forgot_password(self):
        email = simpledialog.askstring("Reset Password", "Enter the email for your account:", parent=self)
        if not email:
            return
        user = get_user(email.strip())
        if not user:
            messagebox.showerror("Error", "No account found with that email.")
            return
        new_pass = simpledialog.askstring("Reset Password", "Enter a new password:", show="*", parent=self)
        if not new_pass:
            return
        if len(new_pass) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters.")
            return
        confirm = simpledialog.askstring("Reset Password", "Confirm new password:", show="*", parent=self)
        if new_pass != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        if update_password(user["email"], new_pass):
            messagebox.showinfo("Success", "Password updated. You can log in now.")
        else:
            messagebox.showerror("Error", "Could not update password.")

    def login(self):
        email = self.ent_user.get().strip()
        password = self.ent_pass.get()

        if not email or not password:
            messagebox.showerror("Error", "Please enter both email/name and password!")
            return

        if "@" in email and not _validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address!")
            return

        user = authenticate(email, password)
        if not user:
            messagebox.showerror("Error", "Invalid email/name or password!")
            return

        if self.rem_var.get():
            save_remembered_email(user["email"])
        else:
            clear_remembered_email()

        self.controller.login_user(user["email"])
        self.ent_pass.delete(0, tk.END)
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
        super().__init__(parent, bg=COLORS["bg"])
        self.controller = controller

        card = _responsive_card(self, max_width=460, max_height=720)

        canvas_scroll = tk.Canvas(card, bg=COLORS["surface"], bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(card, orient="vertical", command=canvas_scroll.yview)
        self.inner = tk.Frame(canvas_scroll, bg=COLORS["surface"])

        self.inner.bind("<Configure>", lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all")))
        canvas_scroll.create_window((0, 0), window=self.inner, anchor="nw")
        canvas_scroll.configure(yscrollcommand=scrollbar.set)

        canvas_scroll.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        bind_mousewheel(canvas_scroll, canvas_scroll)

        def _sync_width(event):
            canvas_scroll.itemconfig("all", width=event.width)
        canvas_scroll.bind("<Configure>", _sync_width)

        inner = self.inner

        btn_back = tk.Button(inner, text="← Back", font=get_font("small_b"),
                             fg=COLORS["text_muted"], bg=COLORS["surface"], bd=0,
                             activebackground=COLORS["surface"], cursor="hand2",
                             command=lambda: controller.show_screen("WelcomeScreen"))
        btn_back.pack(anchor="w", padx=40, pady=(15, 5))
        add_hover(btn_back, enter_fg=COLORS["primary"], leave_fg=COLORS["text_muted"])

        tk.Label(inner, text="Create Your Account", font=get_font("h1"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=40, pady=2)
        tk.Label(inner, text="Get started with InterviewIQ", font=get_font("body"),
                 fg=COLORS["text_muted"], bg=COLORS["surface"]).pack(anchor="w", padx=40, pady=(0, 10))

        # Pre-declare entry attributes so static analyzers (pylint) recognize them
        self.ent_fullname = None
        self.ent_email = None
        self.ent_pass = None
        self.ent_confirm_pass = None

        fields = [
            ("Full Name", "ent_fullname"),
            ("Email", "ent_email"),
            ("Password", "ent_pass"),
            ("Confirm Password", "ent_confirm_pass"),
        ]
        for label_text, attr_name in fields:
            tk.Label(inner, text=label_text, font=get_font("small_b"),
                     fg=COLORS["text_secondary"], bg=COLORS["surface"]).pack(anchor="w", padx=40, pady=(4, 1))
            is_pwd = "pass" in attr_name.lower()
            entry = tk.Entry(inner, font=get_font("body"), bg=COLORS["bg"], bd=1, relief="solid",
                             show="*" if is_pwd else "", highlightthickness=1,
                             highlightbackground=COLORS["border"], highlightcolor=COLORS["border"])
            entry.pack(fill="x", padx=40, ipady=4)
            add_focus_glow(entry)
            setattr(self, attr_name, entry)

        tk.Label(inner, text="Branch", font=get_font("small_b"),
                 fg=COLORS["text_secondary"], bg=COLORS["surface"]).pack(anchor="w", padx=40, pady=(4, 1))
        self.b_combo = ttk.Combobox(inner, values=[
            "Computer Science Engineering", "Artificial Intelligence & Data Science",
            "Information Technology", "Electronics & Communication"], font=get_font("body"), state="readonly")
        self.b_combo.set("Artificial Intelligence & Data Science")
        self.b_combo.pack(fill="x", padx=40, ipady=2)

        tk.Label(inner, text="Designation", font=get_font("small_b"),
                 fg=COLORS["text_secondary"], bg=COLORS["surface"]).pack(anchor="w", padx=40, pady=(4, 1))
        self.d_combo = ttk.Combobox(inner, values=[
            "AI Engineer", "Machine Learning Engineer", "Data Scientist",
            "NLP Researcher", "Computer Vision Specialist"], font=get_font("body"), state="readonly")
        self.d_combo.set("AI Engineer")
        self.d_combo.pack(fill="x", padx=40, ipady=2)

        self.resume_path = None
        self.btn_resume = tk.Button(inner, text="📎 Upload Resume (PDF / DOCX / TXT)", font=get_font("body"),
                                    bg=COLORS["primary_light"], fg=COLORS["primary"], bd=1, relief="groove",
                                    cursor="hand2", command=self.upload_resume)
        self.btn_resume.pack(fill="x", padx=40, pady=(12, 12), ipady=6)
        add_hover(self.btn_resume, enter_bg=COLORS["primary_lighter"], leave_bg=COLORS["primary_light"])

        btn_register = tk.Button(inner, text="Complete Profile", font=get_font("btn"),
                                 bg=COLORS["primary"], fg="white",
                                 activebackground=COLORS["primary_hover"], activeforeground="white",
                                 bd=0, cursor="hand2", command=self.register)
        btn_register.pack(fill="x", padx=40, ipady=8, pady=(0, 15))
        add_hover(btn_register, enter_bg=COLORS["primary_hover"], leave_bg=COLORS["primary"])

    def upload_resume(self):
        file_path = filedialog.askopenfilename(
            title="Select Resume",
            filetypes=[
                ("Supported resumes", "*.pdf *.docx *.txt"),
                ("PDF files", "*.pdf"),
                ("Word documents", "*.docx"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            ext = os.path.splitext(file_path)[1].lower()
            if ext == ".doc":
                messagebox.showerror("Unsupported", "Legacy .doc files are not supported. Use PDF, DOCX, or TXT.")
                return
            self.resume_path = file_path
            filename = os.path.basename(file_path)
            if len(filename) > 25:
                filename = filename[:22] + "..."
            self.btn_resume.config(text=f"✓ {filename}", fg=COLORS["success_dark"],
                                   bg=COLORS["success_bg"])

    def register(self):
        fullname = self.ent_fullname.get().strip()
        email = self.ent_email.get().strip()
        password = self.ent_pass.get()
        confirm_pass = self.ent_confirm_pass.get()

        if not fullname or not email or not password or not confirm_pass:
            messagebox.showerror("Error", "All fields are required!")
            return

        if not _validate_fullname(fullname):
            messagebox.showerror("Error", "Please provide a valid full name (at least 3 characters).")
            return

        if not _validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address!")
            return

        if not _validate_password(password):
            messagebox.showerror("Error", "Password must be at least 8 characters!")
            return

        if password != confirm_pass:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if not self.resume_path:
            messagebox.showerror("Error", "Please upload your resume!")
            return

        resume_text, photo_bytes, err = extract_resume_data(self.resume_path)
        if err:
            messagebox.showerror("Resume Error", err)
            return

        branch = self.b_combo.get()
        designation = self.d_combo.get()

        success = save_user(fullname, email, password, branch, designation, resume_text, photo_bytes)

        if not success:
            messagebox.showerror("Error", "Email is already registered!")
            return

        self.controller.login_user(email)
        messagebox.showinfo("Welcome", f"Account created for {fullname}. You're logged in!")
        self.controller.show_screen("MainDashboard")
