import tkinter as tk
import random
from menu import InternalBaseView, _draw_bar_chart
from database import load_quiz_data, save_mcq_session, get_performance_summary
from theme import COLORS, get_font, add_hover, create_card, animate_arc


class McqPracticeView(InternalBaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "MCQs")

        header = tk.Frame(self.workspace, bg=COLORS["bg"])
        header.pack(fill="x", pady=(0, 10))
        tk.Label(header, text="MCQ Practice Flow", font=get_font("h2"),
                 fg=COLORS["text"], bg=COLORS["bg"]).pack(side="left")

        self.lbl_meta = tk.Label(header, text="", font=get_font("small"),
                                 fg=COLORS["text_muted"], bg=COLORS["bg"])
        self.lbl_meta.pack(side="right")

        self.card = create_card(self.workspace)
        self.card.pack(fill="both", expand=True)

        self.question_body = tk.Frame(self.card, bg=COLORS["surface"])
        self.question_body.pack(fill="both", expand=True)

        self.questions = []
        self.q_index = 0
        self.score = 0
        self.answered = False
        self.option_frames = []
        self.selected_option = tk.StringVar(value="")
        self.difficulty = "Easy"

        self.lbl_progress = tk.Label(self.question_body, text="", font=get_font("caption_b"),
                                     fg=COLORS["text_muted"], bg=COLORS["surface"])
        self.lbl_progress.pack(anchor="w", padx=35, pady=(25, 0))

        self.lbl_question = tk.Label(self.question_body, text="", font=get_font("h4"),
                                     fg=COLORS["text"], bg=COLORS["surface"], wraplength=700, justify="left")
        self.lbl_question.pack(anchor="w", padx=35, pady=(10, 20))

        self.options_box = tk.Frame(self.question_body, bg=COLORS["surface"])
        self.options_box.pack(fill="x")

        self.footer = tk.Frame(self.card, bg=COLORS["surface"])
        self.footer.pack(fill="x", side="bottom", padx=35, pady=20)

        self.lbl_feedback = tk.Label(self.footer, text="", font=get_font("small"),
                                     fg=COLORS["text_secondary"], bg=COLORS["surface"])
        self.lbl_feedback.pack(side="left")

        self.btn_next = tk.Button(self.footer, text="Next →", font=get_font("btn_sm"),
                                  bg=COLORS["primary"], fg="white", bd=0, cursor="hand2",
                                  activebackground=COLORS["primary_hover"],
                                  command=self.next_question, state="disabled")
        self.btn_next.pack(side="right", ipadx=14, ipady=6)
        add_hover(self.btn_next, enter_bg=COLORS["primary_hover"], leave_bg=COLORS["primary"])

        self.btn_restart = tk.Button(self.footer, text="Restart Quiz", font=get_font("small_b"),
                                     bg=COLORS["surface_alt"], fg=COLORS["text_secondary"], bd=0,
                                     cursor="hand2", command=self.start_quiz)
        self.btn_restart.pack(side="right", padx=10, ipadx=10, ipady=6)
        add_hover(self.btn_restart, enter_bg=COLORS["surface_hover"], leave_bg=COLORS["surface_alt"])

    def on_show(self):
        self.difficulty = getattr(self.controller, "difficulty", "Easy") or "Easy"
        self.lbl_meta.config(text=f"Difficulty: {self.difficulty}")
        if not self.questions or self.q_index == 0 and not self.answered:
            self.start_quiz()

    def start_quiz(self):
        # Load questions using centralized helper (resolves project paths)
        data = load_quiz_data(self.difficulty)
        raw = data.get("questions", [])

        preferred = [q for q in raw if q.get("difficulty") == self.difficulty]
        others = [q for q in raw if q.get("difficulty") != self.difficulty]
        # Prefer matching difficulty; randomize order for fresh restart behavior.
        random.shuffle(preferred)
        random.shuffle(others)
        combined = preferred + others
        self.questions = combined[:5] if combined else []

        self.q_index = 0
        self.score = 0
        self.answered = False
        self.btn_next.config(text="Next →", state="disabled")
        if not self.questions:
            self.lbl_question.config(text="No questions available in skills.json.")
            return
        self._render_question()

    def _clear_options(self):
        for child in self.options_box.winfo_children():
            child.destroy()
        self.option_frames = []

    def _render_question(self):
        self._clear_options()
        self.answered = False
        self.selected_option.set("")
        self.lbl_feedback.config(text="")
        self.btn_next.config(state="disabled", text="Next →")

        q = self.questions[self.q_index]
        total = len(self.questions)
        topic = q.get("topic", "")
        self.lbl_progress.config(text=f"Question {self.q_index + 1} of {total}" + (f"  ·  {topic}" if topic else ""))
        self.lbl_question.config(text=q.get("text", ""))

        correct = q.get("correct", "")
        for opt in q.get("options", []):
            f_opt = tk.Frame(self.options_box, bg=COLORS["bg"],
                             highlightbackground=COLORS["border"], highlightthickness=1)
            f_opt.pack(fill="x", padx=35, pady=8, ipady=12)

            indicator = tk.Label(f_opt, text="○", font=get_font("body_b"), fg=COLORS["text_muted"],
                                 bg=COLORS["bg"], width=3)
            indicator.pack(side="left", padx=(15, 0))

            lbl = tk.Label(f_opt, text=opt, font=get_font("body"),
                           fg=COLORS["text_secondary"], bg=COLORS["bg"], wraplength=620, justify="left")
            lbl.pack(side="left", padx=10)

            item = {
                "frame": f_opt,
                "label": lbl,
                "indicator": indicator,
                "option": opt,
                "is_correct": opt == correct
            }
            self.option_frames.append(item)

            def _select(event, opt_text=opt):
                if not self.answered:
                    self._handle_option_select(opt_text)

            for widget in (f_opt, lbl, indicator):
                widget.bind("<Button-1>", _select)
                widget.config(cursor="hand2")

            add_hover(f_opt, enter_bg=COLORS["surface_alt"], leave_bg=COLORS["bg"])
            add_hover(lbl, enter_bg=COLORS["surface_alt"], leave_bg=COLORS["bg"])
            add_hover(indicator, enter_bg=COLORS["surface_alt"], leave_bg=COLORS["bg"])

    def _handle_option_select(self, selected_text):
        self.answered = True
        self.selected_option.set(selected_text)

        chosen_correct = False
        for item in self.option_frames:
            f = item["frame"]
            lbl = item["label"]
            ind = item["indicator"]
            is_this = item["option"] == selected_text
            is_correct = item["is_correct"]

            if is_correct:
                f.config(bg=COLORS["success_bg"], highlightbackground=COLORS["success_border"])
                lbl.config(bg=COLORS["success_bg"], fg=COLORS["success_dark"], font=get_font("body_b"))
                ind.config(bg=COLORS["success_bg"], text="✓", fg=COLORS["success_dark"])
                if is_this:
                    chosen_correct = True
            elif is_this and not is_correct:
                f.config(bg=COLORS["danger_bg"], highlightbackground=COLORS["danger_border"])
                lbl.config(bg=COLORS["danger_bg"], fg=COLORS["danger"], font=get_font("body_b"))
                ind.config(bg=COLORS["danger_bg"], text="✗", fg=COLORS["danger"])
            else:
                f.config(bg=COLORS["bg"], highlightbackground=COLORS["border"])
                lbl.config(bg=COLORS["bg"], fg=COLORS["text_faint"], font=get_font("body"))
                ind.config(bg=COLORS["bg"], text="○", fg=COLORS["text_faint"])

            for w in (f, lbl, ind):
                w.unbind("<Button-1>")
                w.unbind("<Enter>")
                w.unbind("<Leave>")
                w.config(cursor="")

        if chosen_correct:
            self.score += 1
            self.lbl_feedback.config(text="Correct!", fg=COLORS["success_dark"])
        else:
            self.lbl_feedback.config(text="Incorrect — correct answer highlighted.", fg=COLORS["danger"])

        if self.q_index + 1 >= len(self.questions):
            self.btn_next.config(text="Finish", state="normal")
        else:
            self.btn_next.config(text="Next →", state="normal")

    def next_question(self):
        if not self.answered:
            return
        if self.q_index + 1 >= len(self.questions):
            self._finish_quiz()
            return
        self.q_index += 1
        self._render_question()

    def _finish_quiz(self):
        total = len(self.questions)
        email = self.controller.current_user_email
        if email:
            save_mcq_session(email, self.score, total, self.difficulty)

        pct = int(100 * self.score / total) if total else 0
        self._clear_options()
        self.lbl_progress.config(text="Quiz complete")
        self.lbl_question.config(
            text=f"Score: {self.score}/{total} ({pct}%)\n\nResults saved to your Progress tab."
        )
        self.lbl_feedback.config(text="Great work — keep practicing daily to build your streak.", fg=COLORS["text_secondary"])
        self.btn_next.config(state="disabled")
        self.answered = False
        self.questions = []  # allow restart fresh on next on_show if desired


class PerformanceView(InternalBaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Progress")

        header_frame = tk.Frame(self.workspace, bg=COLORS["bg"])
        header_frame.pack(fill="x", pady=(0, 15))

        btn_back = tk.Button(header_frame, text="←  Performance Dashboard", font=get_font("h3"),
                             fg=COLORS["text"], bg=COLORS["bg"], bd=0, activebackground=COLORS["bg"],
                             cursor="hand2", command=lambda: controller.show_screen("MainDashboard"))
        btn_back.pack(side="left")
        add_hover(btn_back, enter_fg=COLORS["primary"], leave_fg=COLORS["text"])

        grid_matrix = tk.Frame(self.workspace, bg=COLORS["bg"])
        grid_matrix.pack(fill="both", expand=True)

        grid_matrix.columnconfigure(0, weight=4, uniform="group1")
        grid_matrix.columnconfigure(1, weight=3, uniform="group1")
        grid_matrix.rowconfigure(0, weight=1, uniform="group2")
        grid_matrix.rowconfigure(1, weight=1, uniform="group2")

        progress_card = create_card(grid_matrix, hover=True, hover_border=COLORS["success"])
        progress_card.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="nsew")

        tk.Label(progress_card, text="Overall Progress", font=get_font("h4"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=20, pady=(15, 10))

        p_body = tk.Frame(progress_card, bg=COLORS["surface"])
        p_body.pack(fill="both", expand=True, padx=20)

        self.progress_canvas = tk.Canvas(p_body, width=85, height=85, bg=COLORS["surface"], bd=0, highlightthickness=0)
        self.progress_canvas.pack(side="left")

        self.lbl_progress_msg = tk.Label(
            p_body, text="Complete interviews and MCQs to build progress.",
            font=get_font("small"), fg=COLORS["text_secondary"], bg=COLORS["surface"], justify="left"
        )
        self.lbl_progress_msg.pack(side="left", padx=15)

        streak_card = create_card(grid_matrix, hover=True, hover_border=COLORS["success"])
        streak_card.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="nsew")

        tk.Label(streak_card, text="Daily Streak Tracker", font=get_font("h4"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=20, pady=(15, 10))

        self.streak_bar = tk.Frame(streak_card, bg=COLORS["surface"])
        self.streak_bar.pack(fill="x", padx=15, pady=10)
        self.streak_day_widgets = []

        for _ in range(7):
            f_circle = tk.Frame(self.streak_bar, bg=COLORS["surface_alt"], width=28, height=28)
            f_circle.pack_propagate(False)
            f_circle.pack(side="left", padx=3, expand=True)
            lbl = tk.Label(f_circle, text="", font=get_font("caption_b"),
                           fg=COLORS["text_muted"], bg=COLORS["surface_alt"])
            lbl.pack(expand=True)
            self.streak_day_widgets.append((f_circle, lbl))

        self.lbl_streak_count = tk.Label(streak_card, text="", font=get_font("small"),
                                         fg=COLORS["text_secondary"], bg=COLORS["surface"])
        self.lbl_streak_count.pack(anchor="w", padx=20, pady=(0, 10))

        sw_card = create_card(grid_matrix, hover=True)
        sw_card.grid(row=1, column=0, padx=(0, 10), pady=(10, 0), sticky="nsew")

        tk.Label(sw_card, text="Strengths & Weaknesses", font=get_font("h4"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=20, pady=10)

        sw_split = tk.Frame(sw_card, bg=COLORS["surface"])
        sw_split.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        str_box = tk.Frame(sw_split, bg=COLORS["success_bg"],
                           highlightbackground=COLORS["success_border"], highlightthickness=1)
        str_box.pack(side="left", fill="both", expand=True, padx=(0, 5))
        tk.Label(str_box, text="Strengths", font=get_font("small_b"),
                 fg=COLORS["success_dark"], bg=COLORS["success_bg"]).pack(anchor="w", padx=10, pady=4)
        self.lbl_strengths = tk.Label(str_box, text="", font=get_font("caption"),
                                      fg=COLORS["text_secondary"], bg=COLORS["success_bg"], justify="left")
        self.lbl_strengths.pack(anchor="w", padx=10)

        weak_box = tk.Frame(sw_split, bg=COLORS["danger_bg"],
                            highlightbackground=COLORS["danger_border"], highlightthickness=1)
        weak_box.pack(side="left", fill="both", expand=True, padx=(5, 0))
        tk.Label(weak_box, text="Weaknesses", font=get_font("small_b"),
                 fg=COLORS["danger"], bg=COLORS["danger_bg"]).pack(anchor="w", padx=10, pady=4)
        self.lbl_weaknesses = tk.Label(weak_box, text="", font=get_font("caption"),
                                       fg=COLORS["text_secondary"], bg=COLORS["danger_bg"], justify="left")
        self.lbl_weaknesses.pack(anchor="w", padx=10)

        prog_card = create_card(grid_matrix, hover=True)
        prog_card.grid(row=1, column=1, padx=(10, 0), pady=(10, 0), sticky="nsew")

        tk.Label(prog_card, text="Daily Progress", font=get_font("h4"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=20, pady=10)

        self.perf_graph_canvas = tk.Canvas(prog_card, bg=COLORS["surface"], bd=0, highlightthickness=0)
        self.perf_graph_canvas.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        self._perf_days = ["M", "T", "W", "T", "F", "S", "S"]
        self._perf_heights = [0, 0, 0, 0, 0, 0, 0]
        self.perf_graph_canvas.bind("<Configure>", lambda e: _draw_bar_chart(
            self.perf_graph_canvas, self._perf_days, self._perf_heights, bar_color=COLORS["primary"]))

        col2 = create_card(self.workspace)
        col2.pack(fill="x", pady=(15, 0))

        tk.Label(col2, text="Recommended Training Roadmap", font=get_font("h4"),
                 fg=COLORS["text"], bg=COLORS["surface"]).pack(anchor="w", padx=20, pady=10)

        roadmaps = [
            ("📝", "Data Structures", "McqPracticeView"),
            ("🤖", "System Design", "MockInterviewView"),
            ("👥", "Behavioral Skills", "MockInterviewView"),
            ("📄", "Resume Building", "ResumeView"),
            ("🗣️", "Communication", "MockInterviewView"),
        ]

        r_strip = tk.Frame(col2, bg=COLORS["surface"])
        r_strip.pack(fill="x", padx=15, pady=(0, 15))

        for icon, topic, route in roadmaps:
            row_item = tk.Frame(r_strip, bg=COLORS["bg"],
                                highlightbackground=COLORS["border"], highlightthickness=1)
            row_item.pack(side="left", fill="x", expand=True, padx=4, ipady=8)
            lbl = tk.Label(row_item, text=f"{icon} {topic}", font=get_font("caption_b"),
                           fg=COLORS["text_secondary"], bg=COLORS["bg"], cursor="hand2")
            lbl.pack(expand=True, padx=2)

            def _go(event=None, r=route):
                controller.show_screen(r)

            for w in (row_item, lbl):
                w.bind("<Button-1>", _go)
                w.config(cursor="hand2")

            add_hover(row_item, enter_bg=COLORS["primary_light"], leave_bg=COLORS["bg"])
            add_hover(lbl, enter_bg=COLORS["primary_light"], leave_bg=COLORS["bg"],
                      enter_fg=COLORS["primary"], leave_fg=COLORS["text_secondary"])

        self._overall_pct = 0

    def on_show(self):
        email = self.controller.current_user_email
        if not email:
            return
        summary = get_performance_summary(email)
        self._overall_pct = summary["overall"]
        animate_arc(self.progress_canvas, 42, 42, 37, target_pct=self._overall_pct,
                    arc_color=COLORS["success"], sub_label="Score")

        msg = (
            f"Interviews: {summary['interview_count']} (avg {summary['interview_avg']}%)\n"
            f"MCQs: {summary['mcq_count']} (avg {summary['mcq_avg']}%)\n"
            f"Keep practicing to raise your overall score."
        )
        self.lbl_progress_msg.config(text=msg)

        flags = summary["week_flags"]
        for (f_circle, lbl), (day, achieved) in zip(self.streak_day_widgets, flags):
            bg_circle = COLORS["success"] if achieved else COLORS["surface_alt"]
            fg_circle = "white" if achieved else COLORS["text_muted"]
            f_circle.config(bg=bg_circle)
            lbl.config(text=day, fg=fg_circle, bg=bg_circle)

        streak = summary["streak"]
        self.lbl_streak_count.config(text=f"Current streak: {streak} day(s)")

        self.lbl_strengths.config(text="\n".join(f"• {s}" for s in summary["strengths"]))
        self.lbl_weaknesses.config(text="\n".join(f"• {w}" for w in summary["weaknesses"]))

        self._perf_heights = summary["week_activity"]
        _draw_bar_chart(self.perf_graph_canvas, self._perf_days, self._perf_heights, bar_color=COLORS["primary"])
