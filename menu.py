import tkinter as tk
from tkinter import ttk

class InternalBaseView(tk.Frame):
    def __init__(self, parent, controller, title_text):
        super().__init__(parent, bg="#F8FAFC")
        self.controller = controller

        sidebar = tk.Frame(self, bg="white", width=240, highlightbackground="#E2E8F0", highlightthickness=1)
        sidebar.pack(fill="y", side="left")
        sidebar.pack_propagate(False)

        brand_f = tk.Frame(sidebar, bg="white")
        brand_f.pack(fill="x", pady=(30, 40), padx=20)
        
        logo_c = tk.Canvas(brand_f, width=24, height=24, bg="white", bd=0, highlightthickness=0)
        logo_c.pack(side="left")
        logo_c.create_polygon(12, 2, 2, 22, 22, 22, fill="#2563EB")
        logo_c.create_polygon(12, 8, 7, 19, 17, 19, fill="white")

        tk.Label(brand_f, text="InterviewIQ", font=("Helvetica", 14, "bold"), fg="#2563EB", bg="white").pack(side="left", padx=10)

        # Updated Left Sidebar items from Persona request
        nav_routes = [
            ("Profile", "MainDashboard"),
            ("Resume", "ResumeView"),
            ("Interview Chat", "MockInterviewView"),
            ("MCQs", "McqPracticeView"),
            ("Progress", "PerformanceView"),
            ("Logout", "WelcomeScreen")
        ]

        for label, view_target in nav_routes:
            color = "#EF4444" if label == "Logout" else "#475569"
            font_weight = "bold" if label == title_text else "normal"
            bg_select = "#F1F5F9" if label == title_text else "white"
            
            btn = tk.Button(sidebar, text=f"  {label}", font=("Helvetica", 11, font_weight), fg=color, bg=bg_select, 
                            bd=0, anchor="w", cursor="hand2", activebackground="#F1F5F9",
                            command=lambda target=view_target: controller.show_screen(target))
            btn.pack(fill="x", padx=15, pady=6, ipady=8)

        self.workspace = tk.Frame(self, bg="#F8FAFC")
        self.workspace.pack(fill="both", expand=True, padx=40, pady=30)


class MainDashboard(InternalBaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Profile")

        # Top Section Layout Splitting
        header_f = tk.Frame(self.workspace, bg="#F8FAFC")
        header_f.pack(fill="x", pady=(0, 10))
        tk.Label(header_f, text="Welcome Dashboard", font=("Helvetica", 22, "bold"), fg="#0F172A", bg="#F8FAFC").pack(side="left")

        # Daily Streak Tracker Widget Block
        streak_frame = tk.Frame(header_f, bg="#FFF7ED", highlightbackground="#FFEDD5", highlightthickness=1)
        streak_frame.pack(side="right", padx=5)
        tk.Label(streak_frame, text="🔥 5 Day Streak!", font=("Helvetica", 11, "bold"), fg="#C2410C", bg="#FFF7ED", padx=10, pady=5).pack()

        # Target Navigation Work Cards Grid Layout
        cards_f = tk.Frame(self.workspace, bg="#F8FAFC")
        cards_f.pack(fill="x", pady=10)

        flows = [
            ("Prepare with\nMock Interview", "MockInterviewView", "📝"),
            ("Take\nMCQ Quizzes", "McqPracticeView", "📋"),
            ("View\nProgress", "PerformanceView", "📊")
        ]

        for title, route, icon in flows:
            card = tk.Frame(cards_f, bg="white", highlightbackground="#E2E8F0", highlightthickness=1, width=220, height=120)
            card.pack_propagate(False)
            card.pack(side="left", padx=(0, 20))
            
            tk.Label(card, text=icon, font=("Helvetica", 18), bg="white").pack(anchor="w", padx=20, pady=(12, 2))
            lbl_text = tk.Label(card, text=title, font=("Helvetica", 12, "bold"), bg="white", fg="#0F172A", justify="left")
            lbl_text.pack(anchor="w", padx=20)

            for widget in (card, lbl_text):
                widget.bind("<Button-1>", lambda e, r=route: self.controller.show_screen(r))
                widget.config(cursor="hand2")

        # Configurations Filter Panel
        config_f = tk.Frame(self.workspace, bg="white", highlightbackground="#E2E8F0", highlightthickness=1)
        config_f.pack(fill="x", pady=20, ipady=15, padx=2)

        row1 = tk.Frame(config_f, bg="white")
        row1.pack(fill="x", padx=25, pady=(15, 8))
        tk.Label(row1, text="Choose Company Target", font=("Helvetica", 11, "bold"), fg="#475569", bg="white", width=22, anchor="w").pack(side="left")
        
        # Broad Software Giants Target Dropdown Row
        c_combo = ttk.Combobox(row1, values=["Google", "Microsoft", "Amazon", "Meta", "NVIDIA", "OpenAI", "Apple"], font=("Helvetica", 11), state="readonly", width=25)
        c_combo.set("Google")
        c_combo.pack(side="left", padx=10)

        row2 = tk.Frame(config_f, bg="white")
        row2.pack(fill="x", padx=25, pady=8)
        tk.Label(row2, text="Select Difficulty Level", font=("Helvetica", 11, "bold"), fg="#475569", bg="white", width=22, anchor="w").pack(side="left")
        d_combo = ttk.Combobox(row2, values=["Easy", "Moderate", "Hard"], font=("Helvetica", 11), state="readonly", width=25)
        d_combo.set("Easy")
        d_combo.pack(side="left", padx=10)

        # Graphical Progress Tracker Analytics section
        graph_f = tk.Frame(self.workspace, bg="white", highlightbackground="#E2E8F0", highlightthickness=1)
        graph_f.pack(fill="both", expand=True, pady=(10, 0))
        tk.Label(graph_f, text="Daily Progress Activity", font=("Helvetica", 12, "bold"), fg="#0F172A", bg="white").pack(anchor="w", padx=20, pady=10)

        # Custom Bar Graph Canvas Draw Rendering Block
        graph_canvas = tk.Canvas(graph_f, bg="white", bd=0, highlightthickness=0)
        graph_canvas.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Drawing Mock Activity bar charts metrics dynamically
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        heights = [40, 60, 35, 90, 50, 75, 95]
        for i, (day, h) in enumerate(zip(days, heights)):
            x0 = 40 + (i * 75)
            y0 = 150 - h
            x1 = x0 + 35
            y1 = 150
            graph_canvas.create_rectangle(x0, y0, x1, y1, fill="#2563EB", outline="")
            graph_canvas.create_text(x0+17, 162, text=day, font=("Helvetica", 10), fill="#64748B")


class ResumeView(InternalBaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Resume")
        
        # Header
        header_f = tk.Frame(self.workspace, bg="#F8FAFC")
        header_f.pack(fill="x", pady=(0, 15))
        tk.Label(header_f, text="Your Uploaded Resume", font=("Helvetica", 22, "bold"), fg="#0F172A", bg="#F8FAFC").pack(side="left")

        # Two-panel layout: Left for Profile & Photo, Right for Resume Content
        self.panel_frame = tk.Frame(self.workspace, bg="#F8FAFC")
        self.panel_frame.pack(fill="both", expand=True)
        
        # -------------------------------------------------------------
        # Left Panel (Profile info card)
        # -------------------------------------------------------------
        self.left_card = tk.Frame(self.panel_frame, bg="white", highlightbackground="#E2E8F0", highlightthickness=1, width=320)
        self.left_card.pack(side="left", fill="both", padx=(0, 20), pady=5)
        self.left_card.pack_propagate(False)
        
        # Avatar / Photo Canvas Unit
        self.photo_canvas = tk.Canvas(self.left_card, width=120, height=120, bg="#F1F5F9", highlightthickness=0)
        self.photo_canvas.pack(pady=20)
        
        # Labels for user profile info
        self.lbl_name = tk.Label(self.left_card, text="Full Name", font=("Helvetica", 14, "bold"), fg="#0F172A", bg="white", wraplength=280)
        self.lbl_name.pack(pady=(10, 2))
        
        self.lbl_email = tk.Label(self.left_card, text="email@example.com", font=("Helvetica", 10), fg="#64748B", bg="white", wraplength=280)
        self.lbl_email.pack(pady=(0, 15))
        
        # Divider line
        div = tk.Frame(self.left_card, bg="#E2E8F0", height=1)
        div.pack(fill="x", padx=30, pady=10)
        
        # Branch & Designation Labels styled as capsule badges
        tk.Label(self.left_card, text="BRANCH", font=("Helvetica", 9, "bold"), fg="#94A3B8", bg="white").pack(anchor="w", padx=30, pady=(10, 2))
        self.branch_badge = tk.Frame(self.left_card, bg="#F1F5F9", highlightbackground="#E2E8F0", highlightthickness=1)
        self.branch_badge.pack(anchor="w", padx=30, pady=2)
        self.lbl_branch = tk.Label(self.branch_badge, text="Branch Info", font=("Helvetica", 9, "bold"), fg="#475569", bg="#F1F5F9", padx=8, pady=3, wraplength=220, justify="left")
        self.lbl_branch.pack()
        
        tk.Label(self.left_card, text="DESIGNATION", font=("Helvetica", 9, "bold"), fg="#94A3B8", bg="white").pack(anchor="w", padx=30, pady=(12, 2))
        self.desig_badge = tk.Frame(self.left_card, bg="#EFF6FF", highlightbackground="#DBEAFE", highlightthickness=1)
        self.desig_badge.pack(anchor="w", padx=30, pady=2)
        self.lbl_desig = tk.Label(self.desig_badge, text="Designation Info", font=("Helvetica", 9, "bold"), fg="#2563EB", bg="#EFF6FF", padx=8, pady=3, wraplength=220, justify="left")
        self.lbl_desig.pack()

        # -------------------------------------------------------------
        # Right Panel (Tabbed Content Area)
        # -------------------------------------------------------------
        self.right_container = tk.Frame(self.panel_frame, bg="#F8FAFC")
        self.right_container.pack(side="left", fill="both", expand=True, pady=5)
        
        # Tab bar layout
        self.tab_bar = tk.Frame(self.right_container, bg="#F8FAFC")
        self.tab_bar.pack(fill="x", pady=(0, 10))
        
        self.btn_insights_tab = tk.Button(self.tab_bar, text="📊 AI Resume Insights", font=("Helvetica", 11, "bold"), bg="white", fg="#2563EB", bd=1, highlightbackground="#E2E8F0", highlightthickness=1, cursor="hand2", command=lambda: self.switch_tab("insights"))
        self.btn_insights_tab.pack(side="left", padx=(0, 10), ipady=6, ipadx=12)
        
        self.btn_text_tab = tk.Button(self.tab_bar, text="📄 Extracted Resume Text", font=("Helvetica", 11), bg="#F1F5F9", fg="#64748B", bd=0, cursor="hand2", command=lambda: self.switch_tab("text"))
        self.btn_text_tab.pack(side="left", ipady=6, ipadx=12)
        
        # Card Background Frame for tab views
        self.content_card = tk.Frame(self.right_container, bg="white", highlightbackground="#E2E8F0", highlightthickness=1)
        self.content_card.pack(fill="both", expand=True)

        # ------------------- Tab 1: AI Insights Frame -------------------
        self.insights_frame = tk.Frame(self.content_card, bg="white")
        self.insights_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Split into upper section (Radial Dial and Tech Skills side-by-side)
        upper_frame = tk.Frame(self.insights_frame, bg="white")
        upper_frame.pack(fill="x", pady=(0, 20))
        
        # Score Dial Card
        score_card = tk.Frame(upper_frame, bg="white", highlightbackground="#F1F5F9", highlightthickness=1)
        score_card.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=5)
        
        tk.Label(score_card, text="Resume Strength Indicator", font=("Helvetica", 11, "bold"), fg="#0F172A", bg="white").pack(anchor="w", padx=15, pady=(15, 10))
        self.score_canvas = tk.Canvas(score_card, width=140, height=140, bg="white", highlightthickness=0)
        self.score_canvas.pack(pady=(0, 15))
        
        # Skills Card
        skills_card = tk.Frame(upper_frame, bg="white", highlightbackground="#F1F5F9", highlightthickness=1)
        skills_card.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=5)
        
        tk.Label(skills_card, text="Detected Core Skills", font=("Helvetica", 11, "bold"), fg="#0F172A", bg="white").pack(anchor="w", padx=20, pady=(15, 10))
        self.skills_container = tk.Frame(skills_card, bg="white")
        self.skills_container.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Bottom Section: Tips alert card
        self.tips_card = tk.Frame(self.insights_frame, bg="#F0F9FF", highlightbackground="#E0F2FE", highlightthickness=1)
        self.tips_card.pack(fill="x", pady=(10, 0), ipady=15)
        
        tk.Label(self.tips_card, text="💡 AI Optimization Suggestions", font=("Helvetica", 12, "bold"), fg="#0369A1", bg="#F0F9FF").pack(anchor="w", padx=20, pady=(12, 8))
        self.lbl_tips = tk.Label(self.tips_card, text="", font=("Helvetica", 10), fg="#0E7490", bg="#F0F9FF", justify="left", anchor="w")
        self.lbl_tips.pack(anchor="w", padx=20)

        # ------------------- Tab 2: Full Extracted Text Frame -------------------
        self.text_frame = tk.Frame(self.content_card, bg="white")
        
        tk.Label(self.text_frame, text="Raw Resume Content", font=("Helvetica", 12, "bold"), fg="#0F172A", bg="white").pack(anchor="w", padx=25, pady=15)
        
        text_scroll_container = tk.Frame(self.text_frame, bg="white")
        text_scroll_container.pack(fill="both", expand=True, padx=25, pady=(0, 20))
        
        self.scroll_y = tk.Scrollbar(text_scroll_container)
        self.scroll_y.pack(side="right", fill="y")
        
        self.txt_resume = tk.Text(text_scroll_container, font=("Helvetica", 10), bg="#F8FAFC", fg="#334155", bd=1, relief="solid", yscrollcommand=self.scroll_y.set, wrap="word")
        self.txt_resume.pack(fill="both", expand=True, side="left")
        self.scroll_y.config(command=self.txt_resume.yview)

    def switch_tab(self, tab_name):
        if tab_name == "insights":
            self.text_frame.pack_forget()
            self.insights_frame.pack(fill="both", expand=True, padx=25, pady=20)
            
            # Update tab buttons styling
            self.btn_insights_tab.config(bg="white", fg="#2563EB", bd=1, highlightthickness=1)
            self.btn_text_tab.config(bg="#F1F5F9", fg="#64748B", bd=0, highlightthickness=0)
        else:
            self.insights_frame.pack_forget()
            self.text_frame.pack(fill="both", expand=True)
            
            # Update tab buttons styling
            self.btn_text_tab.config(bg="white", fg="#2563EB", bd=1, highlightthickness=1)
            self.btn_insights_tab.config(bg="#F1F5F9", fg="#64748B", bd=0, highlightthickness=0)

    def draw_score_gauge(self, score):
        self.score_canvas.delete("all")
        # Draw background ring (gray)
        self.score_canvas.create_oval(15, 15, 125, 125, outline="#F1F5F9", width=10)
        # Draw progress arc (blue)
        extent = -(score / 100.0) * 360
        self.score_canvas.create_arc(15, 15, 125, 125, start=90, extent=extent, outline="#2563EB", width=10, style="arc")
        # Draw text inside
        self.score_canvas.create_text(70, 62, text=f"{score}%", font=("Helvetica", 20, "bold"), fill="#0F172A")
        self.score_canvas.create_text(70, 84, text="Strength Score", font=("Helvetica", 8, "bold"), fill="#64748B")

    def extract_skills(self, text):
        if not text:
            return []
        common_skills = [
            "Python", "PyTorch", "TensorFlow", "Machine Learning", "Deep Learning",
            "NLP", "Natural Language Processing", "Computer Vision", "SQL", "Git",
            "C++", "Java", "HTML", "CSS", "JavaScript", "React", "Docker", "AWS",
            "System Design", "Kubernetes", "Linux", "R", "Go", "Rust", "Spark"
        ]
        text_lower = text.lower()
        found = []
        for skill in common_skills:
            if skill.lower() in text_lower:
                found.append(skill)
        return found

    def on_show(self):
        from database import get_user
        import io
        
        try:
            from PIL import Image, ImageTk
            pillow_available = True
        except ImportError:
            pillow_available = False

        email = getattr(self.controller, "current_user_email", "demo@example.com")
        user = get_user(email)
        
        if user:
            # Update left card user info
            self.lbl_name.config(text=user["fullname"])
            self.lbl_email.config(text=user["email"])
            self.lbl_branch.config(text=user["branch"] or "N/A")
            self.lbl_desig.config(text=user["designation"] or "N/A")
            
            # Update raw resume text tab content
            self.txt_resume.config(state="normal")
            self.txt_resume.delete("1.0", tk.END)
            resume_text = user["resume_text"] or ""
            self.txt_resume.insert(tk.END, resume_text or "No resume text extracted.")
            self.txt_resume.config(state="disabled")
            
            # Dynamic skill badge extraction
            skills = self.extract_skills(resume_text)
            
            # Clear previous skills inside container
            for widget in self.skills_container.winfo_children():
                widget.destroy()
                
            if skills:
                # Render skills in row-based tags layout
                row_frame = None
                for i, skill in enumerate(skills[:8]): # limit to top 8 skills to look neat
                    if i % 3 == 0:
                        row_frame = tk.Frame(self.skills_container, bg="white")
                        row_frame.pack(fill="x", pady=4, anchor="w")
                    
                    badge = tk.Frame(row_frame, bg="#EFF6FF", highlightbackground="#DBEAFE", highlightthickness=1)
                    badge.pack(side="left", padx=4)
                    tk.Label(badge, text=skill, font=("Helvetica", 8, "bold"), fg="#2563EB", bg="#EFF6FF", padx=6, pady=2).pack()
            else:
                tk.Label(self.skills_container, text="No tech skills identified.", font=("Helvetica", 10, "italic"), fg="#94A3B8", bg="white").pack(anchor="w", pady=10)

            # Draw resume strength score dial
            score = min(65 + len(skills) * 5, 98) if skills else 50
            self.draw_score_gauge(score)
            
            # Set feedback tips
            tips = (
                "• Strong keyword alignment with Designation target: " + (user["designation"] or "AI Engineer") + ".\n"
                "• Quantitative metric recommendations: Add impact stats (e.g. 'Increased accuracy by 15%').\n"
                "• Structuring recommendation: Ensure key professional experience matches tech branch profile."
            )
            self.lbl_tips.config(text=tips)

            # Display photo or standard avatar representation
            self.photo_canvas.delete("all")
            photo_bytes = user["photo"]
            if photo_bytes and pillow_available:
                try:
                    image = Image.open(io.BytesIO(photo_bytes))
                    image = image.resize((120, 120), Image.Resampling.LANCZOS)
                    self.photo_image = ImageTk.PhotoImage(image)
                    self.photo_canvas.create_image(0, 0, anchor="nw", image=self.photo_image)
                    return
                except Exception as e:
                    print(f"Error loading profile image: {e}")
                    
            # Draw professional vector avatar fallback on Canvas
            self.photo_canvas.create_oval(30, 20, 90, 80, fill="#CBD5E1", outline="")
            self.photo_canvas.create_oval(15, 90, 105, 150, fill="#94A3B8", outline="")