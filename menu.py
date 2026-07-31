import tkinter as tk
from tkinter import ttk
from theme import COLORS, get_font, add_hover, create_card, animate_arc, pulse_label


# ─────────────────────────────────────────────
# Sidebar Base View (shared by all internal pages)
# ─────────────────────────────────────────────
class InternalBaseView(tk.Frame):
    def __init__(self, parent, controller, title_text):
        super().__init__(parent, bg=COLORS["bg"])
        self.controller = controller

        # ── Sidebar ──────────────────────────────────────────────
        sidebar = tk.Frame(self, bg=COLORS["surface"], highlightbackground=COLORS["border"], highlightthickness=1)
        sidebar.pack(fill="y", side="left")
        sidebar.pack_propagate(False)

        # Responsive sidebar width
        def _resize_sidebar(event):
            w = max(200, min(260, int(event.width * 0.22)))
            sidebar.config(width=w)
        self.bind("<Configure>", _resize_sidebar)
        sidebar.config(width=240)

        # Brand header
        brand_f = tk.Frame(sidebar, bg=COLORS["surface"])
        brand_f.pack(fill="x", pady=(30, 35), padx=20)

        logo_c = tk.Canvas(brand_f, width=28, height=28, bg=COLORS["surface"], bd=0, highlightthickness=0)
        logo_c.pack(side="left")
        logo_c.create_polygon(14, 2, 2, 26, 26, 26, fill=COLORS["primary"])
        logo_c.create_polygon(14, 9, 8, 22, 20, 22, fill=COLORS["surface"])

        tk.Label(brand_f, text="InterviewIQ", font=get_font("brand"),
                 fg=COLORS["primary"], bg=COLORS["surface"]).pack(side="left", padx=10)

        # Navigation items with icons
        nav_routes = [
            ("👤  Profile",        "MainDashboard"),
            ("📄  Resume",         "ResumeView"),
            ("💬  Interview Chat", "MockInterviewView"),
            ("📝  MCQs",           "McqPracticeView"),
            ("📊  Progress",       "PerformanceView"),
            ("🚪  Logout",         "WelcomeScreen"),
        ]

        for label, view_target in nav_routes:
            # Determine if this is the active page
            plain_label = label.split("  ", 1)[1] if "  " in label else label
            is_active = (plain_label == title_text)
            is_logout = ("Logout" in label)

            fg_color = COLORS["danger"] if is_logout else (COLORS["primary"] if is_active else COLORS["text_secondary"])
            bg_color = COLORS["primary_light"] if is_active else COLORS["surface"]
            font = get_font("nav_active") if is_active else get_font("nav")

            # Wrapper frame for left-border accent indicator
            row_frame = tk.Frame(sidebar, bg=COLORS["surface"])
            row_frame.pack(fill="x", padx=(0, 12), pady=3)

            # Active indicator bar
            accent_bar = tk.Frame(row_frame, bg=COLORS["primary"] if is_active else COLORS["surface"], width=4)
            accent_bar.pack(side="left", fill="y")

            btn = tk.Button(row_frame, text=label, font=font, fg=fg_color, bg=bg_color,
                            bd=0, anchor="w", cursor="hand2", activebackground=COLORS["surface_hover"],
                            command=lambda target=view_target: controller.show_screen(target))
            btn.pack(fill="x", side="left", expand=True, padx=(8, 4), ipady=9)

            # Hover effects (skip active page — it already looks highlighted)
            if not is_active:
                hover_bg = COLORS["danger_bg"] if is_logout else COLORS["surface_alt"]
                add_hover(btn, enter_bg=hover_bg, leave_bg=bg_color)

        # ── Workspace ────────────────────────────────────────────
        self.workspace = tk.Frame(self, bg=COLORS["bg"])
        self.workspace.pack(fill="both", expand=True, padx=35, pady=25)

        # Responsive workspace padding
        def _resize_workspace(event):
            px = max(18, min(45, int(event.width * 0.04)))
            py = max(12, min(30, int(event.height * 0.03)))
            self.workspace.pack_configure(padx=px, pady=py)
        self.bind("<Configure>", _resize_workspace, add="+")


# ─────────────────────────────────────────────
# Bar Chart Drawing Utility
# ─────────────────────────────────────────────
def _draw_bar_chart(canvas, days, heights, bar_color=None, show_values=True):
    """Redraw a bar chart proportionally to the current canvas size, with optional value labels."""
    bar_color = bar_color or COLORS["primary"]
    canvas.delete("all")
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    if w < 10 or h < 10:
        return

    n = len(days)
    margin_left = 20
    margin_right = 20
    margin_top = 22 if show_values else 10
    margin_bottom = 25
    usable_w = w - margin_left - margin_right
    usable_h = h - margin_top - margin_bottom

    bar_spacing = usable_w / n
    bar_width = max(8, bar_spacing * 0.55)
    max_h = max(heights) if heights else 1

    # Subtle horizontal gridlines
    for frac in (0.25, 0.5, 0.75):
        gy = margin_top + usable_h * (1 - frac)
        canvas.create_line(margin_left, gy, w - margin_right, gy, fill=COLORS["surface_alt"], dash=(3, 3))

    for i, (day, val) in enumerate(zip(days, heights)):
        bar_h = (val / max_h) * usable_h
        x0 = margin_left + i * bar_spacing + (bar_spacing - bar_width) / 2
        y0 = margin_top + usable_h - bar_h
        x1 = x0 + bar_width
        y1 = margin_top + usable_h

        canvas.create_rectangle(x0, y0, x1, y1, fill=bar_color, outline="")
        canvas.create_text(x0 + bar_width / 2, y1 + 12, text=day, font=get_font("caption"), fill=COLORS["text_muted"])

        if show_values:
            canvas.create_text(x0 + bar_width / 2, y0 - 10, text=str(val), font=get_font("caption_b"), fill=COLORS["text_secondary"])


# ─────────────────────────────────────────────
# Main Dashboard
# ─────────────────────────────────────────────
class MainDashboard(InternalBaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Profile")

        # Top header
        header_f = tk.Frame(self.workspace, bg=COLORS["bg"])
        header_f.pack(fill="x", pady=(0, 10))
        tk.Label(header_f, text="Welcome Dashboard", font=get_font("h1"),
                 fg=COLORS["text"], bg=COLORS["bg"]).pack(side="left")

        # Streak badge with pulse
        streak_frame = tk.Frame(header_f, bg=COLORS["streak_bg"],
                                highlightbackground=COLORS["streak_border"], highlightthickness=1)
        streak_frame.pack(side="right", padx=5)
        streak_lbl = tk.Label(streak_frame, text="🔥 5 Day Streak!", font=get_font("body_b"),
                              fg=COLORS["streak_text"], bg=COLORS["streak_bg"], padx=12, pady=6)
        streak_lbl.pack()
        pulse_label(streak_lbl, COLORS["streak_text"], "#EA580C", interval=900)

        # ── Navigation Flow Cards ────────────────────────────────
        cards_f = tk.Frame(self.workspace, bg=COLORS["bg"])
        cards_f.pack(fill="x", pady=10)

        flows = [
            ("Prepare with\nMock Interview", "MockInterviewView", "📝"),
            ("Take\nMCQ Quizzes",            "McqPracticeView",   "📋"),
            ("View\nProgress",               "PerformanceView",   "📊"),
        ]

        for i, (title, route, icon) in enumerate(flows):
            cards_f.columnconfigure(i, weight=1, uniform="nav_cards")

            card = create_card(cards_f, hover=True, hover_border=COLORS["primary"])
            card.grid(row=0, column=i, padx=(0 if i == 0 else 10, 0), sticky="nsew", ipady=15)

            tk.Label(card, text=icon, font=("Segoe UI", 20), bg=COLORS["surface"]).pack(anchor="w", padx=20, pady=(12, 2))
            lbl_text = tk.Label(card, text=title, font=get_font("h4"),
                                bg=COLORS["surface"], fg=COLORS["text"], justify="left")
            lbl_text.pack(anchor="w", padx=20)

            for widget in (card, lbl_text):
                widget.bind("<Button-1>", lambda e, r=route: self.controller.show_screen(r))
                widget.config(cursor="hand2")

        # ── Configuration Panel ──────────────────────────────────
        config_f = create_card(self.workspace)
        config_f.pack(fill="x", pady=20, ipady=15, padx=2)

        row1 = tk.Frame(config_f, bg=COLORS["surface"])
        row1.pack(fill="x", padx=25, pady=(15, 8))
        tk.Label(row1, text="Choose Company Target", font=get_font("body_b"),
                 fg=COLORS["text_secondary"], bg=COLORS["surface"], width=22, anchor="w").pack(side="left")
        c_combo = ttk.Combobox(row1, values=["Google", "Microsoft", "Amazon", "Meta", "NVIDIA", "OpenAI", "Apple"],
                               font=get_font("body"), state="readonly", width=25)
        c_combo.set("Google")
        c_combo.pack(side="left", padx=10)

        row2 = tk.Frame(config_f, bg=COLORS["surface"])
        row2.pack(fill="x", padx=25, pady=8)
        tk.Label(row2, text="Select Difficulty Level", font=get_font("body_b"),
                 fg=COLORS["text_secondary"], bg=COLORS["surface"], width=22, anchor="w").pack(side="left")
        d_combo = ttk.Combobox(row2, values=["Easy", "Moderate", "Hard"],
                               font=get_font("body"), state="readonly", width=25)
        d_combo.set("Easy")
        d_combo.pack(side="left", padx=10)

        # ── Daily Progress Graph ─────────────────────────────────
        graph_f = create_card(self.workspace)
        graph_f.pack(fill="both", expand=True, pady=(10, 0))
        tk.Label(graph_f, text="Daily Progress Activity", font=get_font("h4"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=20, pady=10)

        self.graph_canvas = tk.Canvas(graph_f, bg=COLORS["surface"], bd=0, highlightthickness=0)
        self.graph_canvas.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self._dash_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self._dash_heights = [40, 60, 35, 90, 50, 75, 95]
        self.graph_canvas.bind("<Configure>", lambda e: _draw_bar_chart(
            self.graph_canvas, self._dash_days, self._dash_heights))


# ─────────────────────────────────────────────
# Resume View
# ─────────────────────────────────────────────
class ResumeView(InternalBaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Resume")

        # Header
        header_f = tk.Frame(self.workspace, bg=COLORS["bg"])
        header_f.pack(fill="x", pady=(0, 15))
        tk.Label(header_f, text="Your Uploaded Resume", font=get_font("h1"),
                 fg=COLORS["text"], bg=COLORS["bg"]).pack(side="left")

        # Two-panel responsive grid
        self.panel_frame = tk.Frame(self.workspace, bg=COLORS["bg"])
        self.panel_frame.pack(fill="both", expand=True)
        self.panel_frame.columnconfigure(0, weight=1, minsize=220)
        self.panel_frame.columnconfigure(1, weight=3)
        self.panel_frame.rowconfigure(0, weight=1)

        # ── Left Panel (Profile Card) ────────────────────────────
        self.left_card = create_card(self.panel_frame)
        self.left_card.grid(row=0, column=0, padx=(0, 20), pady=5, sticky="nsew")

        self.photo_canvas = tk.Canvas(self.left_card, width=120, height=120,
                                      bg=COLORS["surface_alt"], highlightthickness=0)
        self.photo_canvas.pack(pady=20)

        self.lbl_name = tk.Label(self.left_card, text="Full Name", font=get_font("h4"),
                                 fg=COLORS["text"], bg=COLORS["surface"], wraplength=280)
        self.lbl_name.pack(pady=(10, 2))

        self.lbl_email = tk.Label(self.left_card, text="email@example.com", font=get_font("small"),
                                  fg=COLORS["text_muted"], bg=COLORS["surface"], wraplength=280)
        self.lbl_email.pack(pady=(0, 15))

        tk.Frame(self.left_card, bg=COLORS["border"], height=1).pack(fill="x", padx=30, pady=10)

        tk.Label(self.left_card, text="BRANCH", font=get_font("caption_b"),
                 fg=COLORS["text_faint"], bg=COLORS["surface"]).pack(anchor="w", padx=30, pady=(10, 2))
        self.branch_badge = tk.Frame(self.left_card, bg=COLORS["surface_alt"],
                                     highlightbackground=COLORS["border"], highlightthickness=1)
        self.branch_badge.pack(anchor="w", padx=30, pady=2)
        self.lbl_branch = tk.Label(self.branch_badge, text="Branch Info", font=get_font("caption_b"),
                                   fg=COLORS["text_secondary"], bg=COLORS["surface_alt"], padx=8, pady=3,
                                   wraplength=220, justify="left")
        self.lbl_branch.pack()

        tk.Label(self.left_card, text="DESIGNATION", font=get_font("caption_b"),
                 fg=COLORS["text_faint"], bg=COLORS["surface"]).pack(anchor="w", padx=30, pady=(12, 2))
        self.desig_badge = tk.Frame(self.left_card, bg=COLORS["primary_light"],
                                    highlightbackground=COLORS["primary_lighter"], highlightthickness=1)
        self.desig_badge.pack(anchor="w", padx=30, pady=2)
        self.lbl_desig = tk.Label(self.desig_badge, text="Designation Info", font=get_font("caption_b"),
                                  fg=COLORS["primary"], bg=COLORS["primary_light"], padx=8, pady=3,
                                  wraplength=220, justify="left")
        self.lbl_desig.pack()

        # ── Right Panel (Tabbed Content) ─────────────────────────
        self.right_container = tk.Frame(self.panel_frame, bg=COLORS["bg"])
        self.right_container.grid(row=0, column=1, pady=5, sticky="nsew")

        # Tab bar with underline indicator
        self.tab_bar = tk.Frame(self.right_container, bg=COLORS["bg"])
        self.tab_bar.pack(fill="x", pady=(0, 0))

        self.btn_insights_tab = tk.Button(self.tab_bar, text="📊 AI Resume Insights", font=get_font("body_b"),
                                          bg=COLORS["surface"], fg=COLORS["primary"], bd=0, cursor="hand2",
                                          activebackground=COLORS["surface"],
                                          command=lambda: self.switch_tab("insights"))
        self.btn_insights_tab.pack(side="left", padx=(0, 5), ipady=8, ipadx=14)

        self.btn_text_tab = tk.Button(self.tab_bar, text="📄 Extracted Resume Text", font=get_font("body"),
                                      bg=COLORS["bg"], fg=COLORS["text_muted"], bd=0, cursor="hand2",
                                      activebackground=COLORS["bg"],
                                      command=lambda: self.switch_tab("text"))
        self.btn_text_tab.pack(side="left", ipady=8, ipadx=14)

        add_hover(self.btn_text_tab, enter_fg=COLORS["primary"], leave_fg=COLORS["text_muted"])

        # Tab underline indicators
        self.tab_underline_frame = tk.Frame(self.right_container, bg=COLORS["border"], height=2)
        self.tab_underline_frame.pack(fill="x")
        self.active_underline = tk.Frame(self.tab_underline_frame, bg=COLORS["primary"], height=3, width=180)
        self.active_underline.place(x=0, y=0)

        # Content card
        self.content_card = create_card(self.right_container)
        self.content_card.pack(fill="both", expand=True, pady=(0, 0))

        # ─── Tab 1: AI Insights ──────────────────────────────────
        self.insights_frame = tk.Frame(self.content_card, bg=COLORS["surface"])
        self.insights_frame.pack(fill="both", expand=True, padx=25, pady=20)

        upper_frame = tk.Frame(self.insights_frame, bg=COLORS["surface"])
        upper_frame.pack(fill="both", expand=True, pady=(0, 20))

        # Score dial card
        score_card = tk.Frame(upper_frame, bg=COLORS["surface"],
                              highlightbackground=COLORS["surface_alt"], highlightthickness=1)
        score_card.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=5)
        tk.Label(score_card, text="Resume Strength Indicator", font=get_font("body_b"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=15, pady=(15, 10))
        self.score_canvas = tk.Canvas(score_card, width=140, height=140,
                                      bg=COLORS["surface"], highlightthickness=0)
        self.score_canvas.pack(pady=(0, 15))

        # Skills card
        skills_card = tk.Frame(upper_frame, bg=COLORS["surface"],
                               highlightbackground=COLORS["surface_alt"], highlightthickness=1)
        skills_card.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=5)
        tk.Label(skills_card, text="Detected Core Skills", font=get_font("body_b"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=20, pady=(15, 10))
        self.skills_container = tk.Frame(skills_card, bg=COLORS["surface"])
        self.skills_container.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        # Tips card
        self.tips_card = tk.Frame(self.insights_frame, bg=COLORS["info_bg"],
                                  highlightbackground=COLORS["info_border"], highlightthickness=1)
        self.tips_card.pack(fill="x", pady=(10, 0), ipady=15)
        tk.Label(self.tips_card, text="💡 AI Optimization Suggestions", font=get_font("h4"),
                 fg=COLORS["info_text"], bg=COLORS["info_bg"]).pack(anchor="w", padx=20, pady=(12, 8))
        self.lbl_tips = tk.Label(self.tips_card, text="", font=get_font("small"),
                                 fg=COLORS["info_dark"], bg=COLORS["info_bg"], justify="left", anchor="w")
        self.lbl_tips.pack(anchor="w", padx=20)

        # ─── Tab 2: Raw Resume Text ─────────────────────────────
        self.text_frame = tk.Frame(self.content_card, bg=COLORS["surface"])

        header_row = tk.Frame(self.text_frame, bg=COLORS["surface"])
        header_row.pack(fill="x", padx=25, pady=(15, 10))
        tk.Label(header_row, text="Raw Resume Content", font=get_font("h4"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(side="left")

        # Added Copy button
        self.btn_copy = tk.Button(header_row, text="📋 Copy", font=get_font("caption_b"),
                                  bg=COLORS["surface_alt"], fg=COLORS["text_secondary"], bd=0,
                                  cursor="hand2", activebackground=COLORS["surface_hover"],
                                  command=self._copy_resume_text)
        self.btn_copy.pack(side="right")
        add_hover(self.btn_copy, enter_bg=COLORS["surface_hover"], leave_bg=COLORS["surface_alt"])

        # Styled container
        text_scroll_container = tk.Frame(self.text_frame, bg=COLORS["surface_alt"],
                                         highlightbackground=COLORS["border"], highlightthickness=1)
        text_scroll_container.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        self.scroll_y = ttk.Scrollbar(text_scroll_container, orient="vertical")
        self.scroll_y.pack(side="right", fill="y")

        # Styled Text widget with padding and line spacing
        self.txt_resume = tk.Text(text_scroll_container, font=get_font("small"), bg=COLORS["surface_alt"],
                                  fg=COLORS["text_secondary"], bd=0, highlightthickness=0,
                                  padx=15, pady=15, spacing1=4, spacing2=2, spacing3=4,
                                  yscrollcommand=self.scroll_y.set, wrap="word")
        self.txt_resume.pack(fill="both", expand=True, side="left")
        self.scroll_y.config(command=self.txt_resume.yview)

    def _copy_resume_text(self):
        text = self.txt_resume.get("1.0", tk.END).strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.update()
            self.btn_copy.config(text="✓ Copied", fg=COLORS["success_text"], bg=COLORS["success_bg"])
            self.after(2000, lambda: self.btn_copy.config(text="📋 Copy", fg=COLORS["text_secondary"], bg=COLORS["surface_alt"]))

    def switch_tab(self, tab_name):
        if tab_name == "insights":
            self.text_frame.pack_forget()
            self.insights_frame.pack(fill="both", expand=True, padx=25, pady=20)
            self.btn_insights_tab.config(bg=COLORS["surface"], fg=COLORS["primary"], font=get_font("body_b"))
            self.btn_text_tab.config(bg=COLORS["bg"], fg=COLORS["text_muted"], font=get_font("body"))
            self.active_underline.place(x=0, y=0)
            
            # Re-animate the strength indicator
            email = getattr(self.controller, "current_user_email", "demo@example.com")
            from database import get_user
            user = get_user(email)
            if user:
                skills = self.extract_skills(user.get("resume_text") or "")
                score = min(65 + len(skills) * 5, 98) if skills else 50
                self.draw_score_gauge(score)
        else:
            self.insights_frame.pack_forget()
            self.text_frame.pack(fill="both", expand=True)
            self.btn_text_tab.config(bg=COLORS["surface"], fg=COLORS["primary"], font=get_font("body_b"))
            self.btn_insights_tab.config(bg=COLORS["bg"], fg=COLORS["text_muted"], font=get_font("body"))
            # Move underline to second tab
            self.active_underline.place(x=self.btn_insights_tab.winfo_width() + 10, y=0)

    def draw_score_gauge(self, score):
        """Animated score gauge using the theme helper."""
        animate_arc(self.score_canvas, 70, 70, 55, score, sub_label="Strength Score")

    def extract_skills(self, text):
        if not text:
            return []
            
        # 1. Try to dynamically parse the formatted SKILLS section
        import re
        skills_match = re.search(r'SKILLS\n(.*?)(?:\n\n[A-Z]+|$)', text, re.DOTALL)
        if skills_match:
            skills_block = skills_match.group(1)
            extracted = []
            for line in skills_block.split('\n'):
                line = line.strip()
                if line.startswith('-'):
                    # Remove the bullet
                    content = line[1:].strip()
                    # If there's a category like "Languages: ", strip it
                    if ':' in content:
                        content = content.split(':', 1)[1].strip()
                    
                    # Split by commas
                    for skill in content.split(','):
                        skill = skill.strip()
                        if skill and skill not in extracted:
                            extracted.append(skill)
            if extracted:
                return extracted
                
        # 2. Fallback to hardcoded search if no formatted SKILLS section is found
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
            self.lbl_name.config(text=user["fullname"])
            self.lbl_email.config(text=user["email"])
            self.lbl_branch.config(text=user["branch"] or "N/A")
            self.lbl_desig.config(text=user["designation"] or "N/A")

            self.txt_resume.config(state="normal")
            self.txt_resume.delete("1.0", tk.END)
            resume_text = user["resume_text"] or ""
            self.txt_resume.insert(tk.END, resume_text or "No resume text extracted.")
            self.txt_resume.config(state="disabled")

            # Skill badge extraction with hover effects
            skills = self.extract_skills(resume_text)
            for widget in self.skills_container.winfo_children():
                widget.destroy()

            if skills:
                row_frame = None
                for i, skill in enumerate(skills[:8]):
                    if i % 3 == 0:
                        row_frame = tk.Frame(self.skills_container, bg=COLORS["surface"])
                        row_frame.pack(fill="x", pady=4, anchor="w")

                    badge = tk.Frame(row_frame, bg=COLORS["primary_light"],
                                     highlightbackground=COLORS["primary_lighter"], highlightthickness=1)
                    badge.pack(side="left", padx=4)
                    lbl = tk.Label(badge, text=skill, font=get_font("tiny"),
                                   fg=COLORS["primary"], bg=COLORS["primary_light"], padx=6, pady=2)
                    lbl.pack()
                    # Hover inversion on skill badges
                    add_hover(lbl, enter_bg=COLORS["primary"], leave_bg=COLORS["primary_light"],
                              enter_fg=COLORS["surface"], leave_fg=COLORS["primary"])
                    add_hover(badge, enter_bg=COLORS["primary"], leave_bg=COLORS["primary_light"])
            else:
                tk.Label(self.skills_container, text="No tech skills identified.",
                         font=("Segoe UI", 10, "italic"), fg=COLORS["text_faint"],
                         bg=COLORS["surface"]).pack(anchor="w", pady=10)

            # Animated score gauge
            score = min(65 + len(skills) * 5, 98) if skills else 50
            self.draw_score_gauge(score)

            # Tips
            tips = (
                "• Strong keyword alignment with Designation target: " + (user["designation"] or "AI Engineer") + ".\n"
                "• Quantitative metric recommendations: Add impact stats (e.g. 'Increased accuracy by 15%').\n"
                "• Structuring recommendation: Ensure key professional experience matches tech branch profile."
            )
            self.lbl_tips.config(text=tips)

            # Photo / Avatar
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

            # Vector avatar fallback
            self.photo_canvas.create_oval(30, 20, 90, 80, fill=COLORS["border_light"], outline="")
            self.photo_canvas.create_oval(15, 90, 105, 150, fill=COLORS["text_faint"], outline="")