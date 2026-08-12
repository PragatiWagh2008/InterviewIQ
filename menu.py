import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from theme import COLORS, get_font, add_hover, create_card, animate_arc, draw_logo
from database import (
    get_user, get_week_activity, update_user_preferences,
    improve_skill_extraction
)


# ─────────────────────────────────────────────
# Sidebar Base View (shared by all internal pages)
# ─────────────────────────────────────────────
class InternalBaseView(tk.Frame):
    def __init__(self, parent, controller, title_text):
        super().__init__(parent, bg=COLORS["bg"])
        self.controller = controller

        sidebar = tk.Frame(self, bg=COLORS["sidebar"], highlightbackground=COLORS["border"], highlightthickness=0)
        sidebar.pack(fill="y", side="left")
        sidebar.pack_propagate(False)

        def _resize_sidebar(event):
            # event.width is the width of self (InternalBaseView)
            # Sidebar should be ~22% of total width, clamped
            w = max(190, min(250, int(event.width * 0.22)))
            sidebar.config(width=w)
        
        # Bind to self's Configure event for sidebar resize
        self.bind("<Configure>", _resize_sidebar)
        sidebar.config(width=232)

        brand_f = tk.Frame(sidebar, bg=COLORS["sidebar"])
        brand_f.pack(fill="x", pady=(28, 34), padx=18)

        logo_c = tk.Canvas(brand_f, width=28, height=28, bg=COLORS["sidebar"], bd=0, highlightthickness=0)
        logo_c.pack(side="left")
        draw_logo(logo_c, 28)

        tk.Label(brand_f, text="Interview", font=get_font("brand"),
                 fg="#FFFFFF", bg=COLORS["sidebar"]).pack(side="left", padx=(9, 0))
        tk.Label(brand_f, text="IQ", font=get_font("brand"),
                 fg=COLORS["primary"], bg=COLORS["sidebar"]).pack(side="left")

        nav_routes = [
            ("👤  Profile",        "MainDashboard"),
            ("📄  Resume",         "ResumeView"),
            ("💬  Interview Chat", "MockInterviewView"),
            ("📝  MCQs",           "McqPracticeView"),
            ("📊  Progress",       "PerformanceView"),
            ("🚪  Logout",         "__logout__"),
        ]

        for label, view_target in nav_routes:
            plain_label = label.split("  ", 1)[1] if "  " in label else label
            is_active = (plain_label == title_text)
            is_logout = (view_target == "__logout__")

            fg_color = "#FFFFFF" if is_active else (COLORS["danger"] if is_logout else COLORS["sidebar_text"])
            bg_color = COLORS["primary"] if is_active else COLORS["sidebar"]
            font = get_font("nav_active") if is_active else get_font("nav")

            row_frame = tk.Frame(sidebar, bg=COLORS["sidebar"])
            row_frame.pack(fill="x", padx=(12, 12), pady=2)

            def _nav(target=view_target):
                if target == "__logout__":
                    controller.logout_user()
                else:
                    controller.show_screen(target)

            btn = tk.Button(row_frame, text=label, font=font, fg=fg_color, bg=bg_color,
                            bd=0, anchor="w", cursor="hand2",
                            activebackground=COLORS["primary_hover"] if is_active else COLORS["ink_soft"],
                            activeforeground="#FFFFFF", command=_nav)
            btn.pack(fill="x", side="left", expand=True, padx=(4, 2), ipady=9)

            if not is_active:
                add_hover(btn, enter_bg=COLORS["ink_soft"], leave_bg=bg_color)

        self.sidebar_foot = tk.Frame(sidebar, bg=COLORS["sidebar"])
        self.sidebar_foot.pack(side="bottom", fill="x", padx=18, pady=(0, 22))

        tk.Frame(self.sidebar_foot, bg="#2A3A5E", height=1).pack(fill="x", pady=(0, 12))

        tk.Label(self.sidebar_foot, text="Prepping for", font=get_font("caption"),
                 fg=COLORS["sidebar_muted"], bg=COLORS["sidebar"]).pack(anchor="w")
        self.lbl_foot_target = tk.Label(self.sidebar_foot, text="", font=get_font("caption_b"),
                                        fg="#FFFFFF", bg=COLORS["sidebar"])
        self.lbl_foot_target.pack(anchor="w")

        self.workspace = tk.Frame(self, bg=COLORS["bg"])
        self.workspace.pack(fill="both", expand=True, padx=35, pady=25)

        def _resize_workspace(event):
            # Use sidebar's actual width to calculate workspace padding
            sidebar_w = sidebar.winfo_width()
            available_w = event.width - sidebar_w
            if available_w < 100:
                return
            px = max(18, min(45, int(available_w * 0.05)))
            py = max(12, min(30, int(event.height * 0.03)))
            self.workspace.pack_configure(padx=px, pady=py)
        self.bind("<Configure>", _resize_workspace, add="+")

    def _update_sidebar_footer(self):
        email = self.controller.current_user_email
        company = getattr(self.controller, "target_company", "Google") or "Google"
        designation = "SDE"
        if email:
            user = get_user(email)
            if user:
                company = user.get("target_company") or company
                designation = user.get("designation") or designation
        self.lbl_foot_target.config(text=f"{company} · {designation}")


def _draw_bar_chart(canvas, days, heights, bar_color=None, show_values=True):
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
    max_h = max(max(heights), 1)

    for frac in (0.25, 0.5, 0.75):
        gy = margin_top + usable_h * (1 - frac)
        canvas.create_line(margin_left, gy, w - margin_right, gy, fill=COLORS["surface_alt"], dash=(3, 3))

    for i, (day, val) in enumerate(zip(days, heights)):
        bar_h = (val / max_h) * usable_h if max_h else 0
        x0 = margin_left + i * bar_spacing + (bar_spacing - bar_width) / 2
        y0 = margin_top + usable_h - bar_h
        x1 = x0 + bar_width
        y1 = margin_top + usable_h

        canvas.create_rectangle(x0, y0, x1, y1, fill=bar_color, outline="")
        canvas.create_text(x0 + bar_width / 2, y1 + 12, text=day, font=get_font("caption"), fill=COLORS["text_muted"])

        if show_values:
            canvas.create_text(x0 + bar_width / 2, y0 - 10, text=str(val), font=get_font("caption_b"), fill=COLORS["text_secondary"])


class PillRow(tk.Frame):
    """Wrap-row of selectable pill buttons (company / difficulty chooser).

    Rows re-wrap automatically to fit the widget's current width, so pills
    never overflow the card when the window is resized.
    """

    def __init__(self, parent, options, initial, on_change, specials=None, max_width=860):
        super().__init__(parent, bg=COLORS["surface"])
        self.on_change = on_change
        self.value = initial
        self.buttons = {}
        self.specials = specials or {}
        self.options = list(options)
        self.max_width = max_width
        self._last_width = -1

        f = tkfont.Font(font=get_font("small_b"))
        self._font = f
        self._widths = {opt: f.measure(opt) + 48 for opt in self.options}

        # Re-wrap when the available width actually changes (window resize).
        self.bind("<Configure>", self._on_resize)

        # Seed an initial layout using the caller's width hint; the first
        # <Configure> with a real size will rebuild rows to fit exactly.
        self._rebuild(max_width)

    def _on_resize(self, event):
        w = event.width
        if w < 10 or abs(w - self._last_width) <= 4:
            return
        self._rebuild(w)

    def _rebuild(self, avail_width):
        self._last_width = avail_width
        for child in self.winfo_children():
            child.destroy()
        if avail_width < 10:
            return

        row = tk.Frame(self, bg=COLORS["surface"])
        row.pack(fill="x", anchor="w")
        row_w = 0
        for opt in self.options:
            w = self._widths[opt]
            if row_w > 0 and row_w + w > avail_width:
                row = tk.Frame(self, bg=COLORS["surface"])
                row.pack(fill="x", anchor="w", pady=(8, 0))
                row_w = 0
            btn = self._make(row, opt)
            btn.pack(side="left", padx=(0, 8))
            row_w += w + 8
            self.buttons[opt] = btn
        self._apply_styles(self.value)

    def _make(self, parent, text):
        return tk.Button(parent, text=text, font=get_font("small_b"), bd=0, relief="flat",
                         cursor="hand2", padx=15, pady=6, command=lambda t=text: self._select(t))

    def _select(self, text):
        self.value = text
        self._apply_styles(text)
        if self.on_change:
            self.on_change(text)

    def set_value(self, text):
        self.value = text
        self._apply_styles(text)

    def _apply_styles(self, selected):
        for opt, btn in self.buttons.items():
            if self.specials.get(opt) == "teal":
                if opt == selected:
                    btn.config(fg="#FFFFFF", bg=COLORS["primary"],
                               highlightbackground=COLORS["primary"], highlightthickness=1,
                               activebackground=COLORS["primary_hover"], activeforeground="#FFFFFF")
                else:
                    btn.config(fg=COLORS["primary_hover"], bg=COLORS["primary_light"],
                               highlightbackground=COLORS["primary"], highlightthickness=1,
                               activebackground=COLORS["primary_light"],
                               activeforeground=COLORS["primary_hover"])
            else:
                if opt == selected:
                    btn.config(fg="#FFFFFF", bg=COLORS["ink"],
                               highlightbackground=COLORS["ink"], highlightthickness=1,
                               activebackground=COLORS["ink_soft"], activeforeground="#FFFFFF")
                else:
                    btn.config(fg=COLORS["text_muted"], bg=COLORS["surface"],
                               highlightbackground=COLORS["border"], highlightthickness=1,
                               activebackground=COLORS["primary_light"],
                               activeforeground=COLORS["text_muted"])


class MainDashboard(InternalBaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Profile")

        header_f = tk.Frame(self.workspace, bg=COLORS["bg"])
        header_f.pack(fill="x", pady=(0, 12))

        title_stack = tk.Frame(header_f, bg=COLORS["bg"])
        title_stack.pack(side="left")

        tk.Label(title_stack, text="DASHBOARD", font=get_font("caption_b"),
                 fg=COLORS["primary_hover"], bg=COLORS["bg"]).pack(anchor="w")
        self.lbl_greeting = tk.Label(title_stack, text="Good morning", font=get_font("h2"),
                                     fg=COLORS["text"], bg=COLORS["bg"])
        self.lbl_greeting.pack(anchor="w")

        self.user_chip = tk.Frame(header_f, bg=COLORS["surface"],
                                  highlightbackground=COLORS["border"], highlightthickness=1)
        self.user_chip.pack(side="right", anchor="e")

        self.avatar_canvas = tk.Canvas(self.user_chip, width=27, height=27,
                                       bg=COLORS["surface"], bd=0, highlightthickness=0)
        self.avatar_canvas.pack(side="left", padx=(4, 8), pady=4)

        self.lbl_user = tk.Label(self.user_chip, text="", font=get_font("body_b"),
                                 fg=COLORS["text"], bg=COLORS["surface"])
        self.lbl_user.pack(side="left", padx=(0, 14))
        self._draw_avatar()

        cards_f = tk.Frame(self.workspace, bg=COLORS["bg"])
        cards_f.pack(fill="x", pady=8)

        card_meta = [
            ("Prepare with mock interview", "Talk it through with your AI interviewer", "💬", "a", "MockInterviewView"),
            ("Take MCQ quizzes",            "Sharpen concepts, company-wise",            "📝", "b", "McqPracticeView"),
            ("View progress",               "See how far you've come",                   "📊", "c", "PerformanceView"),
        ]
        icon_bg = {"a": COLORS["mint"], "b": COLORS["coral_soft"], "c": "#EAEBFB"}
        icon_fg = {"a": COLORS["primary_hover"], "b": COLORS["coral"], "c": "#5B5FE0"}

        for i, (title, sub, icon, tag, route) in enumerate(card_meta):
            cards_f.columnconfigure(i, weight=1, uniform="nav_cards")

            card = create_card(cards_f, hover=True, hover_border=COLORS["primary"])
            card.grid(row=0, column=i, padx=(0 if i == 0 else 10, 0), sticky="nsew", ipady=14)

            icon_box = tk.Frame(card, bg=icon_bg[tag], width=34, height=34)
            icon_box.pack(anchor="w", padx=18, pady=(14, 10))
            icon_box.pack_propagate(False)
            tk.Label(icon_box, text=icon, font=(get_font("body")[0], 12),
                     bg=icon_bg[tag], fg=icon_fg[tag]).pack(expand=True)

            lbl_title = tk.Label(card, text=title, font=get_font("h4"),
                                 bg=COLORS["surface"], fg=COLORS["text"], justify="left")
            lbl_title.pack(anchor="w", padx=18)
            lbl_sub = tk.Label(card, text=sub, font=get_font("small"),
                               bg=COLORS["surface"], fg=COLORS["text_muted"], justify="left")
            lbl_sub.pack(anchor="w", padx=18, pady=(2, 14))

            for widget in (card, lbl_title, lbl_sub):
                widget.bind("<Button-1>", lambda e, r=route: self.controller.show_screen(r))
                widget.config(cursor="hand2")

        config_f = create_card(self.workspace)
        config_f.pack(fill="x", pady=16, ipady=6, padx=2)

        tk.Label(config_f, text="Choose company", font=get_font("h4"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=24, pady=(14, 10))
        self.company_pills = PillRow(
            config_f, ["Google", "Microsoft", "Amazon", "Meta", "NVIDIA", "OpenAI", "Apple"],
            "Google", self._save_company)
        self.company_pills.pack(anchor="w", padx=24)

        tk.Label(config_f, text="Select difficulty", font=get_font("h4"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=24, pady=(16, 10))
        self.difficulty_pills = PillRow(
            config_f, ["Easy", "Moderate", "Hard"], "Easy",
            self._save_difficulty, specials={"Easy": "teal"})
        self.difficulty_pills.pack(anchor="w", padx=24, pady=(0, 14))

        tk.Label(config_f, text="These settings customize interview questions and MCQ difficulty.",
                 font=get_font("caption"), fg=COLORS["text_faint"],
                 bg=COLORS["surface"]).pack(anchor="w", padx=24, pady=(0, 8))

        graph_f = create_card(self.workspace)
        graph_f.pack(fill="both", expand=True, pady=(10, 0))
        tk.Label(graph_f, text="Daily Progress Activity (this week)", font=get_font("h4"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=20, pady=10)

        self.graph_canvas = tk.Canvas(graph_f, bg=COLORS["surface"], bd=0, highlightthickness=0)
        self.graph_canvas.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self._dash_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self._dash_heights = [0, 0, 0, 0, 0, 0, 0]
        self.graph_canvas.bind("<Configure>", lambda e: _draw_bar_chart(
            self.graph_canvas, self._dash_days, self._dash_heights))

    def _draw_avatar(self):
        self.avatar_canvas.delete("all")
        self.avatar_canvas.create_oval(1, 1, 26, 26, fill=COLORS["coral"], outline="")
        self.avatar_canvas.create_arc(1, 1, 26, 26, start=0, extent=180,
                                      fill=COLORS["primary"], outline="")

    def _save_company(self, company):
        email = self.controller.current_user_email
        self.controller.target_company = company
        if email:
            update_user_preferences(email, company=company)

    def _save_difficulty(self, difficulty):
        email = self.controller.current_user_email
        self.controller.difficulty = difficulty
        if email:
            update_user_preferences(email, difficulty=difficulty)

    def on_show(self):
        email = self.controller.current_user_email
        user = get_user(email) if email else None
        if user:
            first = (user["fullname"] or "there").split()[0]
            self.lbl_greeting.config(text=f"Good morning, {first}")
            self.lbl_user.config(text=user["fullname"])
            company = user.get("target_company") or self.controller.target_company or "Google"
            difficulty = user.get("difficulty") or self.controller.difficulty or "Easy"
            self.company_pills.set_value(company)
            self.difficulty_pills.set_value(difficulty)
            self.controller.target_company = company
            self.controller.difficulty = difficulty

        self._update_sidebar_footer()
        self._dash_heights = get_week_activity(email) if email else [0, 0, 0, 0, 0, 0, 0]
        _draw_bar_chart(self.graph_canvas, self._dash_days, self._dash_heights)


class ResumeView(InternalBaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Resume")

        header_f = tk.Frame(self.workspace, bg=COLORS["bg"])
        header_f.pack(fill="x", pady=(0, 15))
        tk.Label(header_f, text="Your Uploaded Resume", font=get_font("h1"),
                 fg=COLORS["text"], bg=COLORS["bg"]).pack(side="left")

        self.panel_frame = tk.Frame(self.workspace, bg=COLORS["bg"])
        self.panel_frame.pack(fill="both", expand=True)
        self.panel_frame.columnconfigure(0, weight=1, minsize=220)
        self.panel_frame.columnconfigure(1, weight=3)
        self.panel_frame.rowconfigure(0, weight=1)

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

        self.right_container = tk.Frame(self.panel_frame, bg=COLORS["bg"])
        self.right_container.grid(row=0, column=1, pady=5, sticky="nsew")

        self.tab_bar = tk.Frame(self.right_container, bg=COLORS["bg"])
        self.tab_bar.pack(fill="x", pady=(0, 0))

        self.btn_insights_tab = tk.Button(self.tab_bar, text="📊 Resume Insights", font=get_font("body_b"),
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

        self.tab_underline_frame = tk.Frame(self.right_container, bg=COLORS["border"], height=2)
        self.tab_underline_frame.pack(fill="x")
        self.active_underline = tk.Frame(self.tab_underline_frame, bg=COLORS["primary"], height=3, width=180)
        self.active_underline.place(x=0, y=0)

        self.content_card = create_card(self.right_container)
        self.content_card.pack(fill="both", expand=True, pady=(0, 0))

        self.insights_frame = tk.Frame(self.content_card, bg=COLORS["surface"])
        self.insights_frame.pack(fill="both", expand=True, padx=25, pady=20)

        upper_frame = tk.Frame(self.insights_frame, bg=COLORS["surface"])
        upper_frame.pack(fill="both", expand=True, pady=(0, 20))

        score_card = tk.Frame(upper_frame, bg=COLORS["surface"],
                              highlightbackground=COLORS["surface_alt"], highlightthickness=1)
        score_card.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=5)
        tk.Label(score_card, text="Resume Strength Indicator", font=get_font("body_b"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=15, pady=(15, 10))
        self.score_canvas = tk.Canvas(score_card, width=140, height=140,
                                      bg=COLORS["surface"], highlightthickness=0)
        self.score_canvas.pack(pady=(0, 15))

        skills_card = tk.Frame(upper_frame, bg=COLORS["surface"],
                               highlightbackground=COLORS["surface_alt"], highlightthickness=1)
        skills_card.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=5)
        tk.Label(skills_card, text="Detected Core Skills", font=get_font("body_b"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=20, pady=(15, 10))
        self.skills_container = tk.Frame(skills_card, bg=COLORS["surface"])
        self.skills_container.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        self.tips_card = tk.Frame(self.insights_frame, bg=COLORS["info_bg"],
                                  highlightbackground=COLORS["info_border"], highlightthickness=1)
        self.tips_card.pack(fill="x", pady=(10, 0), ipady=15)
        tk.Label(self.tips_card, text="💡 Optimization Suggestions", font=get_font("h4"),
                 fg=COLORS["info_text"], bg=COLORS["info_bg"]).pack(anchor="w", padx=20, pady=(12, 8))
        self.lbl_tips = tk.Label(self.tips_card, text="", font=get_font("small"),
                                 fg=COLORS["info_dark"], bg=COLORS["info_bg"], justify="left", anchor="w")
        self.lbl_tips.pack(anchor="w", padx=20)

        self.text_frame = tk.Frame(self.content_card, bg=COLORS["surface"])

        header_row = tk.Frame(self.text_frame, bg=COLORS["surface"])
        header_row.pack(fill="x", padx=25, pady=(15, 10))
        tk.Label(header_row, text="Raw Resume Content", font=get_font("h4"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(side="left")

        self.btn_copy = tk.Button(header_row, text="📋 Copy", font=get_font("caption_b"),
                                  bg=COLORS["surface_alt"], fg=COLORS["text_secondary"], bd=0,
                                  cursor="hand2", activebackground=COLORS["surface_hover"],
                                  command=self._copy_resume_text)
        self.btn_copy.pack(side="right")
        add_hover(self.btn_copy, enter_bg=COLORS["surface_hover"], leave_bg=COLORS["surface_alt"])

        text_scroll_container = tk.Frame(self.text_frame, bg=COLORS["surface_alt"],
                                         highlightbackground=COLORS["border"], highlightthickness=1)
        text_scroll_container.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        self.scroll_y = ttk.Scrollbar(text_scroll_container, orient="vertical")
        self.scroll_y.pack(side="right", fill="y")

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

            email = self.controller.current_user_email
            user = get_user(email) if email else None
            if user:
                skills = improve_skill_extraction(user.get("resume_text") or "")
                score = self._compute_resume_score(user.get("resume_text") or "", skills)
                self.draw_score_gauge(score)
        else:
            self.insights_frame.pack_forget()
            self.text_frame.pack(fill="both", expand=True)
            self.btn_text_tab.config(bg=COLORS["surface"], fg=COLORS["primary"], font=get_font("body_b"))
            self.btn_insights_tab.config(bg=COLORS["bg"], fg=COLORS["text_muted"], font=get_font("body"))
            self.active_underline.place(x=self.btn_insights_tab.winfo_width() + 10, y=0)

    def draw_score_gauge(self, score):
        # Store reference to allow cancellation of previous animation
        if hasattr(self, "_score_anim_cancel"):
            try:
                self._score_anim_cancel()
            except Exception:
                pass
        self._score_anim_cancel = animate_arc(self.score_canvas, 70, 70, 55, score, sub_label="Strength Score")

    def _compute_resume_score(self, text, skills):
        score = 40
        score += min(len(skills) * 4, 28)
        lower = text.lower()
        for keyword, pts in (
            ("experience", 6), ("project", 6), ("education", 4),
            ("certif", 4), ("github", 3), ("%", 5),
        ):
            if keyword in lower:
                score += pts
        return max(35, min(98, score))

    def _build_tips(self, user, skills, text):
        tips = []
        designation = user.get("designation") or "AI Engineer"
        tips.append(f"• Align bullets with your target role: {designation}.")
        if not any(ch.isdigit() for ch in text):
            tips.append("• Add measurable impact (e.g. 'Improved accuracy by 12%').")
        else:
            tips.append("• Keep quantifying outcomes; interviewers notice metrics.")
        if len(skills) < 4:
            tips.append("• Expand a clear SKILLS section with tools and frameworks.")
        else:
            tips.append(f"• Strong skill coverage detected ({len(skills)} items). Prioritize top 6–8.")
        if "project" not in text.lower():
            tips.append("• Add 1–2 project write-ups with stack + outcome.")
        return "\n".join(tips[:4])

    def on_show(self):
        import io

        self._update_sidebar_footer()

        try:
            from PIL import Image, ImageTk
            pillow_available = True
        except ImportError:
            pillow_available = False

        email = self.controller.current_user_email
        user = get_user(email) if email else None

        if not user:
            self.lbl_name.config(text="No user loaded")
            return

        self.lbl_name.config(text=user["fullname"])
        self.lbl_email.config(text=user["email"])
        self.lbl_branch.config(text=user["branch"] or "N/A")
        self.lbl_desig.config(text=user["designation"] or "N/A")

        self.txt_resume.config(state="normal")
        self.txt_resume.delete("1.0", tk.END)
        resume_text = user["resume_text"] or ""
        self.txt_resume.insert(tk.END, resume_text or "No resume text extracted.")
        self.txt_resume.config(state="disabled")

        skills = improve_skill_extraction(resume_text)
        for widget in self.skills_container.winfo_children():
            widget.destroy()

        if skills:
            row_frame = None
            for i, skill in enumerate(skills[:12]):
                if i % 3 == 0:
                    row_frame = tk.Frame(self.skills_container, bg=COLORS["surface"])
                    row_frame.pack(fill="x", pady=4, anchor="w")

                badge = tk.Frame(row_frame, bg=COLORS["primary_light"],
                                 highlightbackground=COLORS["primary_lighter"], highlightthickness=1)
                badge.pack(side="left", padx=4)
                lbl = tk.Label(badge, text=skill, font=get_font("tiny"),
                               fg=COLORS["primary"], bg=COLORS["primary_light"], padx=6, pady=2)
                lbl.pack()
                add_hover(lbl, enter_bg=COLORS["primary"], leave_bg=COLORS["primary_light"],
                          enter_fg=COLORS["surface"], leave_fg=COLORS["primary"])
                add_hover(badge, enter_bg=COLORS["primary"], leave_bg=COLORS["primary_light"])
        else:
            tk.Label(self.skills_container, text="No tech skills identified.",
                     font=(get_font("body")[0], 10, "italic"), fg=COLORS["text_faint"],
                     bg=COLORS["surface"]).pack(anchor="w", pady=10)

        score = self._compute_resume_score(resume_text, skills)
        self.draw_score_gauge(score)
        self.lbl_tips.config(text=self._build_tips(user, skills, resume_text))

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

        self.photo_canvas.create_oval(30, 20, 90, 80, fill=COLORS["border_light"], outline="")
        self.photo_canvas.create_oval(15, 90, 105, 150, fill=COLORS["text_faint"], outline="")
