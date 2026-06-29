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
            ("Resume", "MainDashboard"),
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