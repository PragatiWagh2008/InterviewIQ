import tkinter as tk
from menu import InternalBaseView, _draw_bar_chart
from database import load_quiz_data

class McqPracticeView(InternalBaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "MCQs")

        tk.Label(self.workspace, text="MCQ Practice Flow", font=("Helvetica", 20, "bold"), fg="#0F172A", bg="#F8FAFC").pack(anchor="w", pady=(0, 15))

        card = tk.Frame(self.workspace, bg="white", highlightbackground="#E2E8F0", highlightthickness=1)
        card.pack(fill="both", expand=True)

        data = load_quiz_data()
        q = data["questions"][0]

        tk.Label(card, text=q["text"], font=("Helvetica", 14, "bold"), fg="#0F172A", bg="white").pack(anchor="w", padx=35, pady=(35, 20))

        for opt in q["options"]:
            is_correct = "Correct option" in opt
            bg_c = "#F0FDF4" if is_correct else "#F8FAFC"
            fg_c = "#166534" if is_correct else "#334155"
            border_c = "#BBF7D0" if is_correct else "#E2E8F0"

            f_opt = tk.Frame(card, bg=bg_c, highlightbackground=border_c, highlightthickness=1)
            f_opt.pack(fill="x", padx=35, pady=8, ipady=12)
            
            tk.Label(f_opt, text=opt, font=("Helvetica", 11, "bold" if is_correct else "normal"), fg=fg_c, bg=bg_c).pack(side="left", padx=20)


class PerformanceView(InternalBaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Progress")

        # 1. Top Navigation Title Bar
        header_frame = tk.Frame(self.workspace, bg="#F8FAFC")
        header_frame.pack(fill="x", pady=(0, 15))
        
        tk.Button(header_frame, text="←  Performance Dashboard", font=("Helvetica", 16, "bold"), 
                  fg="#0F172A", bg="#F8FAFC", bd=0, activebackground="#F8FAFC", 
                  cursor="hand2", command=lambda: controller.show_screen("MainDashboard")).pack(side="left")

        # 2. Balanced 2x2 Grid Workspace layout area
        grid_matrix = tk.Frame(self.workspace, bg="#F8FAFC")
        grid_matrix.pack(fill="both", expand=True)
        
        # Configure weight ratios to keep columns strictly balanced without text cuts
        grid_matrix.columnconfigure(0, weight=4, uniform="group1")
        grid_matrix.columnconfigure(1, weight=3, uniform="group1")
        grid_matrix.rowconfigure(0, weight=1, uniform="group2")
        grid_matrix.rowconfigure(1, weight=1, uniform="group2")

        # -------------------------------------------------------------
        # CARD 1: Overall Progress [Top Left Box]
        # -------------------------------------------------------------
        progress_card = tk.Frame(grid_matrix, bg="white", highlightbackground="#E2E8F0", highlightthickness=1)
        progress_card.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="nsew")
        
        tk.Label(progress_card, text="Overall Progress", font=("Helvetica", 12, "bold"), fg="#0F172A", bg="white").pack(anchor="w", padx=20, pady=(15, 10))
        
        p_body = tk.Frame(progress_card, bg="white")
        p_body.pack(fill="both", expand=True, padx=20)
        
        arc_canvas = tk.Canvas(p_body, width=85, height=85, bg="white", bd=0, highlightthickness=0)
        arc_canvas.pack(side="left")
        arc_canvas.create_oval(5, 5, 80, 80, outline="#E2E8F0", width=8)
        arc_canvas.create_arc(5, 5, 80, 80, start=90, extent=-324, outline="#10B981", width=8, style="arc")
        arc_canvas.create_text(42, 38, text="90%", font=("Helvetica", 13, "bold"), fill="#0F172A")
        arc_canvas.create_text(42, 54, text="Completed", font=("Helvetica", 8, "bold"), fill="#64748B")

        tk.Label(p_body, text="Great job! You have completed most of\nyour interview preparation modules.\nKeep practicing!", 
                 font=("Helvetica", 10), fg="#475569", bg="white", justify="left").pack(side="left", padx=15)

        # -------------------------------------------------------------
        # CARD 2: Daily Streak Tracker [Top Right Box] - Fixed spacing layout
        # -------------------------------------------------------------
        streak_card = tk.Frame(grid_matrix, bg="white", highlightbackground="#E2E8F0", highlightthickness=1)
        streak_card.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="nsew")
        
        tk.Label(streak_card, text="Daily Streak Tracker", font=("Helvetica", 12, "bold"), fg="#0F172A", bg="white").pack(anchor="w", padx=20, pady=(15, 10))
        
        streak_bar = tk.Frame(streak_card, bg="white")
        streak_bar.pack(fill="x", padx=15, pady=10)
        
        days_tracker = [("M", True), ("T", True), ("W", True), ("T", True), ("F", True), ("S", False), ("S", False)]
        for day, achieved in days_tracker:
            bg_circle = "#10B981" if achieved else "#F1F5F9"
            fg_circle = "white" if achieved else "#64748B"
            
            # Using custom tight dimension bounds to avoid frame cuts completely
            f_circle = tk.Frame(streak_bar, bg=bg_circle, width=28, height=28)
            f_circle.pack_propagate(False)
            f_circle.pack(side="left", padx=3, expand=True)
            tk.Label(f_circle, text=day, font=("Helvetica", 9, "bold"), fg=fg_circle, bg=bg_circle).pack(expand=True)

        # -------------------------------------------------------------
        # CARD 3: Strengths & Weaknesses [Bottom Left Box]
        # -------------------------------------------------------------
        sw_card = tk.Frame(grid_matrix, bg="white", highlightbackground="#E2E8F0", highlightthickness=1)
        sw_card.grid(row=1, column=0, padx=(0, 10), pady=(10, 0), sticky="nsew")
        
        tk.Label(sw_card, text="Strengths & Weaknesses", font=("Helvetica", 12, "bold"), fg="#0F172A", bg="white").pack(anchor="w", padx=20, pady=10)

        sw_split = tk.Frame(sw_card, bg="white")
        sw_split.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        str_box = tk.Frame(sw_split, bg="#F0FDF4", highlightbackground="#DCFCE7", highlightthickness=1)
        str_box.pack(side="left", fill="both", expand=True, padx=(0, 5))
        tk.Label(str_box, text="🟢 Strengths", font=("Helvetica", 10, "bold"), fg="#166534", bg="#F0FDF4").pack(anchor="w", padx=10, pady=4)
        tk.Label(str_box, text="• ML Fundamentals\n• Core Architecture", font=("Helvetica", 9), fg="#334155", bg="#F0FDF4", justify="left").pack(anchor="w", padx=10)

        weak_box = tk.Frame(sw_split, bg="#FEF2F2", highlightbackground="#FEE2E2", highlightthickness=1)
        weak_box.pack(side="left", fill="both", expand=True, padx=(5, 0))
        tk.Label(weak_box, text="🔴 Weaknesses", font=("Helvetica", 10, "bold"), fg="#991B1B", bg="#FEF2F2").pack(anchor="w", padx=10, pady=4)
        weak_box_lbl = tk.Label(weak_box, text="• System Scaling\n• NLP Fine-Tuning", font=("Helvetica", 9), fg="#334155", bg="#FEF2F2", justify="left")
        weak_box_lbl.pack(anchor="w", padx=10)

        # -------------------------------------------------------------
        # CARD 4: Daily Progress Bar Graph [Bottom Right Box]
        # -------------------------------------------------------------
        prog_card = tk.Frame(grid_matrix, bg="white", highlightbackground="#E2E8F0", highlightthickness=1)
        prog_card.grid(row=1, column=1, padx=(10, 0), pady=(10, 0), sticky="nsew")
        
        tk.Label(prog_card, text="Daily Progress", font=("Helvetica", 12, "bold"), fg="#0F172A", bg="white").pack(anchor="w", padx=20, pady=10)

        # Dynamic bar chart canvas — redraws on resize
        self.perf_graph_canvas = tk.Canvas(prog_card, bg="white", bd=0, highlightthickness=0)
        self.perf_graph_canvas.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        self._perf_days = ["M", "T", "W", "T", "F", "S", "S"]
        self._perf_heights = [25, 50, 40, 45, 65, 50, 35]
        self._perf_colors = ["#A7F3D0", "#A7F3D0", "#A7F3D0", "#A7F3D0", "#2563EB", "#A7F3D0", "#A7F3D0"]

        def _draw_perf_chart(event):
            self.perf_graph_canvas.delete("all")
            w = self.perf_graph_canvas.winfo_width()
            h = self.perf_graph_canvas.winfo_height()
            if w < 10 or h < 10:
                return

            n = len(self._perf_days)
            margin_left = 10
            margin_right = 10
            margin_top = 5
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
                self.perf_graph_canvas.create_text(x0 + bar_width / 2, y1 + 10, text=d_name, font=("Helvetica", 8, "bold"), fill="#64748B")

        self.perf_graph_canvas.bind("<Configure>", _draw_perf_chart)

        # -------------------------------------------------------------
        # FOOTER ROW: Recommended Training Roadmap (Full Width Strip)
        # -------------------------------------------------------------
        col2 = tk.Frame(self.workspace, bg="white", highlightbackground="#E2E8F0", highlightthickness=1)
        col2.pack(fill="x", pady=(15, 0))

        tk.Label(col2, text="Recommended Training Roadmap", font=("Helvetica", 12, "bold"), fg="#0F172A", bg="white").pack(anchor="w", padx=20, pady=10)

        roadmaps = [
            ("📝", "Data Structures"),
            ("🤖", "System Design"),
            ("👥", "Behavioral Skills"),
            ("📄", "Resume Building"),
            ("🗣️", "Communication")
        ]

        r_strip = tk.Frame(col2, bg="white")
        r_strip.pack(fill="x", padx=15, pady=(0, 15))

        for icon, topic in roadmaps:
            row_item = tk.Frame(r_strip, bg="#F8FAFC", highlightbackground="#E2E8F0", highlightthickness=1)
            row_item.pack(side="left", fill="x", expand=True, padx=4, ipady=8)
            tk.Label(row_item, text=f"{icon} {topic}", font=("Helvetica", 9, "bold"), fg="#334155", bg="#F8FAFC").pack(expand=True, padx=2)