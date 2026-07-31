import tkinter as tk
from tkinter import ttk, messagebox
from menu import InternalBaseView
from database import get_user
from theme import COLORS, get_font, add_hover, TypingIndicator
import random

# Question banks tailored by designation / general tech
QUESTION_BANKS = {
    "AI Engineer": [
        "Welcome! To start off, please introduce yourself and outline your background in AI & key projects.",
        "How do you decide between fine-tuning a pre-trained Transformer (e.g. Llama/BERT) vs building a model from scratch?",
        "Can you explain how Retrieval-Augmented Generation (RAG) works and how you evaluate retrieval accuracy?",
        "How do you mitigate data bias, handle edge cases, and optimize latency in real-time AI inference pipelines?",
        "Describe a complex AI project you built. What specific challenges did you face and how did you measure success?"
    ],
    "Machine Learning Engineer": [
        "Welcome! Could you introduce yourself and highlight your experience with end-to-end ML model development?",
        "What concrete techniques do you use to detect and combat overfitting or high variance in deep models?",
        "How do you monitor concept/data drift in production systems and establish automated retraining triggers?",
        "Explain the trade-offs between precision, recall, and F1-score. When would you optimize for high recall?",
        "Walk me through how you optimize feature engineering and handling of imbalanced datasets."
    ],
    "Data Scientist": [
        "Welcome! Please introduce yourself and your statistical analysis & machine learning experience.",
        "How do you handle missing data, extreme outliers, and class imbalance during data preprocessing?",
        "Can you explain A/B testing methodology, confidence intervals, and how to determine statistical significance?",
        "Which evaluation metrics (e.g., ROC-AUC, Log-Loss, MAE/RMSE) do you choose for different problem types?",
        "Tell me about a time your quantitative data analysis directly drove a business or product decision."
    ],
    "NLP Researcher": [
        "Welcome! Tell me about your background and research interests in Natural Language Processing.",
        "Explain how scaled dot-product self-attention works in Transformer architectures.",
        "What strategies do you use for domain adaptation and low-resource language fine-tuning?",
        "How do you address hallucinations, alignment, and factual consistency in Large Language Models?",
        "Walk me through a recent NLP paper, architecture, or decoding technique that impressed you."
    ],
    "Computer Vision Specialist": [
        "Welcome! Please introduce your technical background and experience in Computer Vision.",
        "Compare object detection (e.g., YOLO, Faster R-CNN) with semantic vs instance segmentation.",
        "How do data augmentation methods and transfer learning improve CNN generalization?",
        "How do you optimize vision models for low-latency edge deployment (e.g. TensorRT, ONNX)?",
        "Describe a computer vision pipeline you built—what architecture did you select and what were the performance results?"
    ],
    "Default": [
        "Welcome to your mock interview! Please tell me about yourself and your tech background.",
        "What are your core technical strengths, and how do you approach learning new frameworks?",
        "Describe a challenging bug or architecture issue you encountered and how you solved it.",
        "How do you ensure code quality, test coverage, and smooth deployment in a software project?",
        "Where do you see your technical career evolving over the next two years?"
    ]
}

DESIGNATION_KEYWORDS = {
    "AI Engineer": ["model", "transformer", "rag", "fine-tune", "pipeline", "bias", "latency", "data", "accuracy", "inference", "gpu", "llm", "neural", "train", "eval"],
    "Machine Learning Engineer": ["overfitting", "variance", "cross-validation", "precision", "recall", "f1", "drift", "retrain", "feature", "imbalanced", "hyperparameter", "dataset"],
    "Data Scientist": ["outlier", "imbalanced", "statistical", "a/b", "p-value", "significance", "roc", "auc", "metric", "regression", "hypothesis", "insights", "analysis"],
    "NLP Researcher": ["attention", "transformer", "llm", "hallucination", "alignment", "embedding", "token", "bert", "gpt", "fine-tuning", "sequence", "language"],
    "Computer Vision Specialist": ["yolo", "segmentation", "detection", "cnn", "augmentation", "edge", "tensorrt", "onnx", "opencv", "resnet", "feature", "image"],
    "Default": ["project", "code", "architecture", "system", "performance", "test", "design", "team", "scale", "solution", "framework"]
}


def _create_rounded_rect(canvas, x1, y1, x2, y2, radius=10, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)


class ChatBubble(tk.Canvas):
    """Custom visually appealing chat bubble using Canvas drawing"""
    def __init__(self, parent, text, sender="bot", sender_name="AI", **kwargs):
        super().__init__(parent, bg=COLORS["surface"], bd=0, highlightthickness=0, **kwargs)
        self.text = text
        self.sender = sender
        self.sender_name = sender_name
        self.bind("<Configure>", self.draw)

    def draw(self, event=None):
        self.delete("all")
        w = self.winfo_width()

        bg_color = COLORS["surface_alt"] if self.sender == "bot" else COLORS["primary"]
        fg_color = COLORS["text"] if self.sender == "bot" else "white"
        header_color = COLORS["primary"] if self.sender == "bot" else COLORS["primary_lighter"]

        max_bubble_width = max(200, w - 100)

        temp_text = self.create_text(0, 0, text=self.text, font=get_font("chat"), width=max_bubble_width-40, anchor="nw")
        bounds = self.bbox(temp_text)
        text_w = bounds[2] - bounds[0]
        text_h = bounds[3] - bounds[1]
        self.delete(temp_text)

        bubble_w = text_w + 40
        bubble_h = text_h + 50

        self.config(height=bubble_h + 10)

        if self.sender == "bot":
            x1, y1 = 20, 5
            x2, y2 = 20 + bubble_w, 5 + bubble_h
            _create_rounded_rect(self, x1, y1, x2, y2, radius=16, fill=bg_color)
            self.create_text(x1 + 20, y1 + 18, text=f"🤖 {self.sender_name}", font=get_font("chat_hdr"), fill=header_color, anchor="w")
            self.create_text(x1 + 20, y1 + 35, text=self.text, font=get_font("chat"), fill=fg_color, width=max_bubble_width-40, anchor="nw")
        else:
            x1, y1 = w - bubble_w - 20, 5
            x2, y2 = w - 20, 5 + bubble_h
            _create_rounded_rect(self, x1, y1, x2, y2, radius=16, fill=bg_color)
            self.create_text(x2 - 20, y1 + 18, text=f"{self.sender_name} 👤", font=get_font("chat_hdr"), fill=header_color, anchor="e")
            self.create_text(x1 + 20, y1 + 35, text=self.text, font=get_font("chat"), fill=fg_color, width=max_bubble_width-40, anchor="nw")


class MockInterviewView(InternalBaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Interview Chat")

        self.session_active = False
        self.current_q_index = 0
        self.user_answers = []
        self.questions = []
        self.user_name = "Candidate"
        self.designation = "AI Engineer"
        self._typing_indicator = None

        # ── Top Header ───────────────────────────────────────────
        header = tk.Frame(self.workspace, bg=COLORS["bg"])
        header.pack(fill="x", pady=(0, 15))

        title_frame = tk.Frame(header, bg=COLORS["bg"])
        title_frame.pack(side="left")

        tk.Label(title_frame, text="AI Mock Interview", font=get_font("h1"),
                 fg=COLORS["text"], bg=COLORS["bg"]).pack(anchor="w")
        self.lbl_subtitle = tk.Label(title_frame, text="Real-time technical interview session",
                                     font=get_font("body"), fg=COLORS["text_muted"], bg=COLORS["bg"])
        self.lbl_subtitle.pack(anchor="w")

        # Controls
        controls_f = tk.Frame(header, bg=COLORS["bg"])
        controls_f.pack(side="right", anchor="e")

        # Live status pill
        status_pill = tk.Frame(controls_f, bg=COLORS["success_bg"],
                               highlightbackground=COLORS["success_border"], highlightthickness=1)
        status_pill.pack(side="left", padx=10)
        self.lbl_status = tk.Label(status_pill, text="● Live Interview (1/5)", font=get_font("small_b"),
                                   fg=COLORS["success_text"], bg=COLORS["success_bg"], padx=12, pady=6)
        self.lbl_status.pack()

        self.btn_reset = tk.Button(controls_f, text="↺ Restart Session", font=get_font("small_b"),
                                   bg=COLORS["surface_alt"], fg=COLORS["text_secondary"], bd=0,
                                   padx=15, pady=8, cursor="hand2", activebackground=COLORS["surface_hover"],
                                   command=self.reset_interview)
        self.btn_reset.pack(side="left")
        add_hover(self.btn_reset, enter_bg=COLORS["surface_hover"], leave_bg=COLORS["surface_alt"])

        # ── Chat Area ────────────────────────────────────────────
        self.chat_card = tk.Frame(self.workspace, bg=COLORS["surface"],
                                  highlightbackground=COLORS["border_light"], highlightthickness=1)
        self.chat_card.pack(fill="both", expand=True, pady=(0, 10))

        self.chat_canvas = tk.Canvas(self.chat_card, bg=COLORS["surface"], bd=0, highlightthickness=0)
        self.chat_scrollbar = ttk.Scrollbar(self.chat_card, orient="vertical", command=self.chat_canvas.yview)

        self.chat_scroll_frame = tk.Frame(self.chat_canvas, bg=COLORS["surface"])
        self.chat_scroll_frame.bind("<Configure>", lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))

        self.canvas_window = self.chat_canvas.create_window((0, 0), window=self.chat_scroll_frame, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)

        self.chat_canvas.pack(side="left", fill="both", expand=True)
        self.chat_scrollbar.pack(side="right", fill="y")

        self.chat_canvas.bind("<Configure>", self._on_canvas_configure)

        # ── Footer Input Area ────────────────────────────────────
        footer = tk.Frame(self.chat_card, bg=COLORS["surface"])
        footer.pack(fill="x", side="bottom")

        tk.Frame(footer, bg=COLORS["border"], height=1).pack(fill="x")

        input_container = tk.Frame(footer, bg=COLORS["surface"], pady=15, padx=20)
        input_container.pack(fill="x")

        txt_outer = tk.Frame(input_container, bg=COLORS["surface_alt"],
                             highlightbackground=COLORS["border"], highlightthickness=1)
        txt_outer.pack(side="left", fill="both", expand=True, padx=(0, 15))

        self.txt_msg = tk.Text(txt_outer, font=get_font("body"), bg=COLORS["surface_alt"],
                               fg=COLORS["text"], bd=0, wrap="word", height=2,
                               insertbackground=COLORS["primary"])
        self.txt_msg.pack(fill="both", expand=True, padx=12, pady=10)
        self.txt_msg.bind("<Return>", self._on_enter_pressed)

        # Focus glow on the outer frame
        def _focus_in(e):
            txt_outer.config(highlightbackground=COLORS["primary"])
        def _focus_out(e):
            txt_outer.config(highlightbackground=COLORS["border"])
        self.txt_msg.bind("<FocusIn>", _focus_in, add="+")
        self.txt_msg.bind("<FocusOut>", _focus_out, add="+")

        # Action buttons
        btn_panel = tk.Frame(input_container, bg=COLORS["surface"])
        btn_panel.pack(side="right")

        self.btn_send = tk.Button(btn_panel, text="Send ➔", font=get_font("btn_sm"),
                                  bg=COLORS["primary"], fg="white", bd=0, cursor="hand2",
                                  activebackground=COLORS["primary_hover"], command=self.send_message)
        self.btn_send.pack(fill="x", ipady=4, pady=(0, 6))
        add_hover(self.btn_send, enter_bg=COLORS["primary_hover"], leave_bg=COLORS["primary"])

        self.btn_mic = tk.Button(btn_panel, text="🎙️ Speech Assist", font=get_font("caption"),
                                 bg=COLORS["bg"], fg=COLORS["text_secondary"], bd=0,
                                 highlightbackground=COLORS["border"], highlightthickness=1,
                                 cursor="hand2", activebackground=COLORS["surface_alt"],
                                 command=self.simulated_mic)
        self.btn_mic.pack(fill="x", ipady=2)
        add_hover(self.btn_mic, enter_bg=COLORS["surface_alt"], leave_bg=COLORS["bg"])

    def _on_canvas_configure(self, event):
        self.chat_canvas.itemconfig(self.canvas_window, width=event.width)
        for child in self.chat_scroll_frame.winfo_children():
            if isinstance(child, ChatBubble):
                child.draw()

    def _on_enter_pressed(self, event):
        if event.state & 0x0001:  # Shift pressed
            return
        self.send_message()
        return "break"

    def on_show(self):
        email = getattr(self.controller, "current_user_email", "demo@example.com")
        user = get_user(email)
        if user:
            self.user_name = user.get("fullname", "Candidate")
            self.designation = user.get("designation") or "AI Engineer"

        self.lbl_subtitle.config(text=f"Target Role: {self.designation}   |   Candidate: {self.user_name}")

        if not self.session_active:
            self.start_interview()
        else:
            self.txt_msg.focus_set()

    def start_interview(self):
        self.session_active = True
        self.current_q_index = 0
        self.user_answers = []

        bank = QUESTION_BANKS.get(self.designation, QUESTION_BANKS["Default"])
        self.questions = list(bank)

        self.lbl_status.config(text="● Live Interview (1/5)", fg=COLORS["success_text"])
        self.lbl_status.master.config(bg=COLORS["success_bg"], highlightbackground=COLORS["success_border"])

        for widget in self.chat_scroll_frame.winfo_children():
            widget.destroy()

        self.add_message("bot", f"🎯 Welcome {self.user_name}!\nLet's begin your technical interview for {self.designation}.\n\nQuestion 1 of 5:\n{self.questions[0]}")
        self.txt_msg.focus_set()

    def reset_interview(self):
        self.session_active = False
        self.start_interview()

    def add_message(self, sender, text):
        sender_name = "AI Recruiter" if sender == "bot" else self.user_name
        bubble = ChatBubble(self.chat_scroll_frame, text=text, sender=sender, sender_name=sender_name)
        bubble.pack(fill="x", expand=True)

        self.chat_canvas.update_idletasks()
        bubble.draw()

        self.chat_canvas.yview_moveto(1.0)

    def _show_typing_then_reply(self, reply_text):
        """Show typing indicator, then replace with the actual reply."""
        indicator = TypingIndicator(self.chat_scroll_frame)
        indicator.pack(fill="x", padx=10, pady=4)
        indicator.start()
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)

        def _deliver():
            indicator.stop()
            indicator.destroy()
            self.add_message("bot", reply_text)

        # Show typing for 600–1000ms
        delay = random.randint(600, 1000)
        self.after(delay, _deliver)

    def evaluate_user_answer(self, user_text):
        words = user_text.lower().split()
        word_count = len(words)

        keywords = DESIGNATION_KEYWORDS.get(self.designation, DESIGNATION_KEYWORDS["Default"])
        matched_keywords = [kw for kw in keywords if kw in user_text.lower()]

        if word_count < 6:
            feedback = "⚠️ Note: Your answer was quite brief. In technical interviews, try adding specific technical context or examples."
            quality_score = 45
        elif word_count < 15:
            feedback = "👍 Good point! Adding more technical depth or framework details will strengthen your response."
            quality_score = 68
        else:
            if matched_keywords:
                kw_str = ", ".join(set(matched_keywords[:3]))
                feedback = f"✨ Great answer! You covered key technical concepts ({kw_str}) clearly."
                quality_score = min(95, 75 + len(matched_keywords) * 5)
            else:
                feedback = "💡 Well-structured explanation! Be sure to highlight core domain terminology and metrics."
                quality_score = 82

        return feedback, quality_score

    def send_message(self):
        text = self.txt_msg.get("1.0", "end-1c").strip()
        if not text:
            return

        if not self.session_active:
            self.start_interview()

        self.add_message("user", text)

        feedback, quality_score = self.evaluate_user_answer(text)
        self.user_answers.append({
            "text": text,
            "word_count": len(text.split()),
            "score": quality_score
        })

        self.txt_msg.delete("1.0", tk.END)
        self.txt_msg.focus_set()

        # Brief "sent" flash on send button
        self.btn_send.config(bg=COLORS["success"], text="✓ Sent")
        self.after(400, lambda: self.btn_send.config(bg=COLORS["primary"], text="Send ➔"))

        self.current_q_index += 1

        if self.current_q_index < len(self.questions):
            next_q = self.questions[self.current_q_index]
            q_num = self.current_q_index + 1

            self.lbl_status.config(text=f"● Live Interview ({q_num}/5)")
            bot_reply = f"{feedback}\n\nQuestion {q_num} of 5:\n{next_q}"
            self.after(300, lambda: self._show_typing_then_reply(bot_reply))
        else:
            self.session_active = False
            self.lbl_status.config(text="✓ Completed", fg=COLORS["text"])
            self.lbl_status.master.config(bg=COLORS["surface_alt"], highlightbackground=COLORS["border"])

            summary = self._generate_summary_report()
            self.after(400, lambda: self._show_typing_then_reply(summary))

    def simulated_mic(self):
        sample_responses = [
            "In my previous projects, I implemented fine-tuning for Transformer models using PyTorch and Hugging Face, optimizing memory footprint with 8-bit quantization and LoRA adapters.",
            "To prevent overfitting, I rely on regularized validation splits, dropout layers, data augmentation techniques, and early stopping criteria based on validation loss.",
            "For RAG pipelines, we construct dense vector embeddings with FAISS, retrieve relevant chunks, and pass them to the LLM context window while checking BLEU and ROUGE metrics.",
            "I manage inference latency by batching requests, deploying models with TensorRT/ONNX Runtime, and caching frequent query embeddings."
        ]
        simulated_text = random.choice(sample_responses)

        # Pulse mic button while "recording"
        self.btn_mic.config(bg=COLORS["danger_bg"], fg=COLORS["danger"], text="🎙️ Recording...")
        self.after(800, lambda: (
            self.btn_mic.config(bg=COLORS["bg"], fg=COLORS["text_secondary"], text="🎙️ Speech Assist"),
            self.txt_msg.delete("1.0", tk.END),
            self.txt_msg.insert("1.0", simulated_text),
            self.txt_msg.focus_set()
        ))

    def _generate_summary_report(self):
        if self.user_answers:
            avg_score = sum(ans["score"] for ans in self.user_answers) // len(self.user_answers)
            avg_words = sum(ans["word_count"] for ans in self.user_answers) // len(self.user_answers)
        else:
            avg_score = 85
            avg_words = 20

        depth_eval = "Detailed" if avg_words > 18 else "Concise"

        report = (
            f"🎉 Interview Completed!\n\n"
            f"📊 Performance Evaluation:\n"
            f"• Target Role: {self.designation}\n"
            f"• Overall Candidate Score: {avg_score}% / 100 ⭐\n"
            f"• Average Response Depth: {avg_words} words / answer ({depth_eval})\n\n"
            f"💡 Recommendations:\n"
            f"1. Excellent engagement across technical concepts.\n"
            f"2. Keep refining your specific project metrics.\n\n"
            f"Status: Ready for live tech round! Check your Progress tab."
        )
        return report