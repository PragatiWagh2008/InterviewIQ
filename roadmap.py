import tkinter as tk
from menu import InternalBaseView, _draw_bar_chart
from database import load_quiz_data
from theme import COLORS, get_font, add_hover, create_card, animate_arc


class McqPracticeView(InternalBaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "MCQs")

        tk.Label(self.workspace, text="MCQ Practice Flow", font=get_font("h2"),
                 fg=COLORS["text"], bg=COLORS["bg"]).pack(anchor="w", pady=(0, 15))

        card = create_card(self.workspace)
        card.pack(fill="both", expand=True)

        data = load_quiz_data()
        q = data["questions"][0]

        tk.Label(card, text=q["text"], font=get_font("h4"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=35, pady=(35, 20))

        self.selected_option = tk.StringVar(value="")
        self.option_frames = []

        for opt in q["options"]:
            is_correct = "Correct option" in opt

            f_opt = tk.Frame(card, bg=COLORS["bg"],
                             highlightbackground=COLORS["border"], highlightthickness=1)
            f_opt.pack(fill="x", padx=35, pady=8, ipady=12)

            # Radio indicator
            indicator = tk.Label(f_opt, text="○", font=get_font("body_b"), fg=COLORS["text_muted"],
                                 bg=COLORS["bg"], width=3)
            indicator.pack(side="left", padx=(15, 0))

            lbl = tk.Label(f_opt, text=opt, font=get_font("body"),
                           fg=COLORS["text_secondary"], bg=COLORS["bg"])
            lbl.pack(side="left", padx=10)

            self.option_frames.append({
                "frame": f_opt,
                "label": lbl,
                "indicator": indicator,
                "option": opt,
                "is_correct": is_correct
            })

            # Click handler
            def _select(event, opt_text=opt):
                self._handle_option_select(opt_text)

            for widget in (f_opt, lbl, indicator):
                widget.bind("<Button-1>", _select)
                widget.config(cursor="hand2")

            # Hover effect
            add_hover(f_opt, enter_bg=COLORS["surface_alt"], leave_bg=COLORS["bg"])
            add_hover(lbl, enter_bg=COLORS["surface_alt"], leave_bg=COLORS["bg"])
            add_hover(indicator, enter_bg=COLORS["surface_alt"], leave_bg=COLORS["bg"])

    def _handle_option_select(self, selected_text):
        """Highlight the selected option and reveal correct/incorrect."""
        self.selected_option.set(selected_text)

        for item in self.option_frames:
            f = item["frame"]
            lbl = item["label"]
            ind = item["indicator"]
            is_this = (item["option"] == selected_text)
            is_correct = item["is_correct"]

            if is_correct:
                # Always highlight correct answer in green
                f.config(bg=COLORS["success_bg"], highlightbackground=COLORS["success_border"])
                lbl.config(bg=COLORS["success_bg"], fg=COLORS["success_dark"], font=get_font("body_b"))
                ind.config(bg=COLORS["success_bg"], text="✓", fg=COLORS["success_dark"])
            elif is_this and not is_correct:
                # Highlight wrong selection in red
                f.config(bg=COLORS["danger_bg"], highlightbackground=COLORS["danger_border"])
                lbl.config(bg=COLORS["danger_bg"], fg=COLORS["danger"], font=get_font("body_b"))
                ind.config(bg=COLORS["danger_bg"], text="✗", fg=COLORS["danger"])
            else:
                # Dim unselected wrong options
                f.config(bg=COLORS["bg"], highlightbackground=COLORS["border"])
                lbl.config(bg=COLORS["bg"], fg=COLORS["text_faint"], font=get_font("body"))
                ind.config(bg=COLORS["bg"], text="○", fg=COLORS["text_faint"])

            # Remove hover and click after selection
            for w in (f, lbl, ind):
                w.unbind("<Button-1>")
                w.unbind("<Enter>")
                w.unbind("<Leave>")
                w.config(cursor="")


class PerformanceView(InternalBaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Progress")

        # ── Top Header ───────────────────────────────────────────
        header_frame = tk.Frame(self.workspace, bg=COLORS["bg"])
        header_frame.pack(fill="x", pady=(0, 15))

        btn_back = tk.Button(header_frame, text="←  Performance Dashboard", font=get_font("h3"),
                             fg=COLORS["text"], bg=COLORS["bg"], bd=0, activebackground=COLORS["bg"],
                             cursor="hand2", command=lambda: controller.show_screen("MainDashboard"))
        btn_back.pack(side="left")
        add_hover(btn_back, enter_fg=COLORS["primary"], leave_fg=COLORS["text"])

        # ── 2×2 Grid ─────────────────────────────────────────────
        grid_matrix = tk.Frame(self.workspace, bg=COLORS["bg"])
        grid_matrix.pack(fill="both", expand=True)

        grid_matrix.columnconfigure(0, weight=4, uniform="group1")
        grid_matrix.columnconfigure(1, weight=3, uniform="group1")
        grid_matrix.rowconfigure(0, weight=1, uniform="group2")
        grid_matrix.rowconfigure(1, weight=1, uniform="group2")

        # ── CARD 1: Overall Progress (Top Left) ─────────────────
        progress_card = create_card(grid_matrix, hover=True, hover_border=COLORS["success"])
        progress_card.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="nsew")

        tk.Label(progress_card, text="Overall Progress", font=get_font("h4"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=20, pady=(15, 10))

        p_body = tk.Frame(progress_card, bg=COLORS["surface"])
        p_body.pack(fill="both", expand=True, padx=20)

        self.progress_canvas = tk.Canvas(p_body, width=85, height=85, bg=COLORS["surface"], bd=0, highlightthickness=0)
        self.progress_canvas.pack(side="left")

        tk.Label(p_body, text="Great job! You have completed most of\nyour interview preparation modules.\nKeep practicing!",
                 font=get_font("small"), fg=COLORS["text_secondary"], bg=COLORS["surface"],
                 justify="left").pack(side="left", padx=15)

        # ── CARD 2: Daily Streak (Top Right) ─────────────────────
        streak_card = create_card(grid_matrix, hover=True, hover_border=COLORS["success"])
        streak_card.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="nsew")

        tk.Label(streak_card, text="Daily Streak Tracker", font=get_font("h4"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=20, pady=(15, 10))

        streak_bar = tk.Frame(streak_card, bg=COLORS["surface"])
        streak_bar.pack(fill="x", padx=15, pady=10)

        days_tracker = [("M", True), ("T", True), ("W", True), ("T", True), ("F", True), ("S", False), ("S", False)]
        for day, achieved in days_tracker:
            bg_circle = COLORS["success"] if achieved else COLORS["surface_alt"]
            fg_circle = "white" if achieved else COLORS["text_muted"]

            f_circle = tk.Frame(streak_bar, bg=bg_circle, width=28, height=28)
            f_circle.pack_propagate(False)
            f_circle.pack(side="left", padx=3, expand=True)
            tk.Label(f_circle, text=day, font=get_font("caption_b"),
                     fg=fg_circle, bg=bg_circle).pack(expand=True)

        # ── CARD 3: Strengths & Weaknesses (Bottom Left) ────────
        sw_card = create_card(grid_matrix, hover=True)
        sw_card.grid(row=1, column=0, padx=(0, 10), pady=(10, 0), sticky="nsew")

        tk.Label(sw_card, text="Strengths & Weaknesses", font=get_font("h4"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=20, pady=10)

        sw_split = tk.Frame(sw_card, bg=COLORS["surface"])
        sw_split.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        str_box = tk.Frame(sw_split, bg=COLORS["success_bg"],
                           highlightbackground=COLORS["success_border"], highlightthickness=1)
        str_box.pack(side="left", fill="both", expand=True, padx=(0, 5))
        tk.Label(str_box, text="🟢 Strengths", font=get_font("small_b"),
                 fg=COLORS["success_dark"], bg=COLORS["success_bg"]).pack(anchor="w", padx=10, pady=4)
        tk.Label(str_box, text="• ML Fundamentals\n• Core Architecture", font=get_font("caption"),
                 fg=COLORS["text_secondary"], bg=COLORS["success_bg"], justify="left").pack(anchor="w", padx=10)

        weak_box = tk.Frame(sw_split, bg=COLORS["danger_bg"],
                            highlightbackground=COLORS["danger_border"], highlightthickness=1)
        weak_box.pack(side="left", fill="both", expand=True, padx=(5, 0))
        tk.Label(weak_box, text="🔴 Weaknesses", font=get_font("small_b"),
                 fg=COLORS["danger"], bg=COLORS["danger_bg"]).pack(anchor="w", padx=10, pady=4)
        tk.Label(weak_box, text="• System Scaling\n• NLP Fine-Tuning", font=get_font("caption"),
                 fg=COLORS["text_secondary"], bg=COLORS["danger_bg"], justify="left").pack(anchor="w", padx=10)

        # ── CARD 4: Daily Progress Bar Graph (Bottom Right) ──────
        prog_card = create_card(grid_matrix, hover=True)
        prog_card.grid(row=1, column=1, padx=(10, 0), pady=(10, 0), sticky="nsew")

        tk.Label(prog_card, text="Daily Progress", font=get_font("h4"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=20, pady=10)

        self.perf_graph_canvas = tk.Canvas(prog_card, bg=COLORS["surface"], bd=0, highlightthickness=0)
        self.perf_graph_canvas.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        self._perf_days = ["M", "T", "W", "T", "F", "S", "S"]
        self._perf_heights = [25, 50, 40, 45, 65, 50, 35]
        self._perf_colors = ["#A7F3D0", "#A7F3D0", "#A7F3D0", "#A7F3D0", COLORS["primary"], "#A7F3D0", "#A7F3D0"]

        def _draw_perf_chart(event):
            self.perf_graph_canvas.delete("all")
            w = self.perf_graph_canvas.winfo_width()
            h = self.perf_graph_canvas.winfo_height()
            if w < 10 or h < 10:
                return

            n = len(self._perf_days)
            margin_left = 10
            margin_right = 10
            margin_top = 18
            margin_bottom = 20
            usable_w = w - margin_left - margin_right
            usable_h = h - margin_top - margin_bottom

            bar_spacing = usable_w / n
            bar_width = max(8, bar_spacing * 0.5)
            max_h = max(self._perf_heights)

            for idx, (d_name, height, color) in enumerate(zip(self._perf_days, self._perf_heights, self._perf_colors)):
                bar_h = (height / max_h) * usable_h
                x0 = margin_left + idx * bar_spacing + (bar_spacing - bar_width) / 2
                y0 = margin_top + usable_h - bar_h
                x1 = x0 + bar_width
                y1 = margin_top + usable_h

                self.perf_graph_canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
                self.perf_graph_canvas.create_text(x0 + bar_width / 2, y1 + 10, text=d_name,
                                                   font=get_font("tiny"), fill=COLORS["text_muted"])
                # Value labels above bars
                self.perf_graph_canvas.create_text(x0 + bar_width / 2, y0 - 8, text=str(height),
                                                   font=get_font("tiny"), fill=COLORS["text_secondary"])

        self.perf_graph_canvas.bind("<Configure>", _draw_perf_chart)

        # ── Footer: Recommended Training Roadmap ─────────────────
        col2 = create_card(self.workspace)
        col2.pack(fill="x", pady=(15, 0))

        tk.Label(col2, text="Recommended Training Roadmap", font=get_font("h4"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=20, pady=10)

        roadmaps = [
            ("📝", "Data Structures"),
            ("🤖", "System Design"),
            ("👥", "Behavioral Skills"),
            ("📄", "Resume Building"),
            ("🗣️", "Communication"),
        ]

        r_strip = tk.Frame(col2, bg=COLORS["surface"])
        r_strip.pack(fill="x", padx=15, pady=(0, 15))

        for icon, topic in roadmaps:
            row_item = tk.Frame(r_strip, bg=COLORS["bg"],
                                highlightbackground=COLORS["border"], highlightthickness=1)
            row_item.pack(side="left", fill="x", expand=True, padx=4, ipady=8)
            lbl = tk.Label(row_item, text=f"{icon} {topic}", font=get_font("caption_b"),
                           fg=COLORS["text_secondary"], bg=COLORS["bg"], cursor="hand2")
            lbl.pack(expand=True, padx=2)

            # Hover effect on roadmap items
            add_hover(row_item, enter_bg=COLORS["primary_light"], leave_bg=COLORS["bg"])
            add_hover(lbl, enter_bg=COLORS["primary_light"], leave_bg=COLORS["bg"],
                      enter_fg=COLORS["primary"], leave_fg=COLORS["text_secondary"])

    def on_show(self):
        """Animate the progress arc when the view becomes visible."""
        animate_arc(self.progress_canvas, 42, 42, 37, target_pct=90,
                    arc_color=COLORS["success"], sub_label="Completed")