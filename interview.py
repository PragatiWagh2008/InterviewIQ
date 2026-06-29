import tkinter as tk
from menu import InternalBaseView

class MockInterviewView(InternalBaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Interview Chat")

        tk.Label(self.workspace, text="Mock Interview Flow", font=("Helvetica", 20, "bold"), fg="#0F172A", bg="#F8FAFC").pack(anchor="w")

        room = tk.Frame(self.workspace, bg="white", highlightbackground="#E2E8F0", highlightthickness=1)
        room.pack(fill="both", expand=True, pady=15)

        # Vector Rendering High Fidelity Professional Robot Canvas Avatar Graphics Unit
        bot_canvas = tk.Canvas(room, width=200, height=180, bg="white", bd=0, highlightthickness=0)
        bot_canvas.pack(pady=(35, 5))

        bot_canvas.create_oval(60, 45, 140, 115, fill="#F1F5F9", outline="#CBD5E1", width=2) 
        bot_canvas.create_rectangle(75, 65, 125, 95, fill="#0F172A", outline="") 
        bot_canvas.create_oval(85, 74, 97, 86, fill="#2563EB", outline="") 
        bot_canvas.create_oval(103, 74, 115, 86, fill="#2563EB", outline="") 
        bot_canvas.create_rectangle(92, 115, 108, 135, fill="#CBD5E1", outline="") 
        bot_canvas.create_oval(50, 130, 150, 175, fill="#2563EB", outline="") 

        tk.Label(room, text="AI Recruiter Professional Room", font=("Helvetica", 15, "bold"), fg="#0F172A", bg="white").pack()
        tk.Label(room, text="AI will speak to you, ask follow-up questions, and analyze performance.", font=("Helvetica", 11), fg="#64748B", bg="white").pack(pady=10)

        footer = tk.Frame(room, bg="#F8FAFC", height=65, highlightbackground="#E2E8F0", highlightthickness=1)
        footer.pack(fill="x", side="bottom", padx=25, pady=25)
        footer.pack_propagate(False)

        ent_msg = tk.Entry(footer, font=("Helvetica", 11), bg="white", fg="#0F172A", bd=1, relief="solid")
        ent_msg.pack(side="left", fill="both", expand=True, padx=(15, 10), pady=12)
        ent_msg.insert(0, "Type your response or speak...")

        tk.Label(footer, text="🎙️", font=("Helvetica", 14), bg="#F8FAFC", fg="#2563EB", cursor="hand2").pack(side="right", padx=15)