"""
InterviewIQ — Centralized Theme Engine
Provides colors, hover helpers, card factories, focus glow, and font scaling.
"""
import tkinter as tk
import tkinter.font as tkfont


# ─────────────────────────────────────────────
# Color Palette
# ─────────────────────────────────────────────
COLORS = {
    # Surfaces
    "bg":              "#F8FAFC",
    "surface":         "#FFFFFF",
    "surface_alt":     "#F1F5F9",
    "surface_hover":   "#E2E8F0",

    # Borders
    "border":          "#E2E8F0",
    "border_light":    "#CBD5E1",
    "border_focus":    "#2563EB",

    # Primary
    "primary":         "#2563EB",
    "primary_hover":   "#1D4ED8",
    "primary_light":   "#EFF6FF",
    "primary_lighter": "#DBEAFE",

    # Text
    "text":            "#0F172A",
    "text_secondary":  "#475569",
    "text_muted":      "#64748B",
    "text_faint":      "#94A3B8",

    # Accent — Success
    "success":         "#10B981",
    "success_bg":      "#ECFDF5",
    "success_border":  "#D1FAE5",
    "success_text":    "#059669",
    "success_dark":    "#166534",

    # Accent — Danger
    "danger":          "#EF4444",
    "danger_bg":       "#FEF2F2",
    "danger_border":   "#FEE2E2",

    # Accent — Warning / Streak
    "streak_bg":       "#FFF7ED",
    "streak_border":   "#FFEDD5",
    "streak_text":     "#C2410C",

    # Accent — Info
    "info_bg":         "#F0F9FF",
    "info_border":     "#E0F2FE",
    "info_text":       "#0369A1",
    "info_dark":       "#0E7490",
}


def _pick_ui_font():
    """Prefer Segoe UI; fall back to fonts commonly available on Linux/macOS."""
    try:
        available = set(tkfont.families())
    except Exception:
        available = set()
    for name in ("Segoe UI", "Inter", "Ubuntu", "Noto Sans", "DejaVu Sans",
                 "Helvetica Neue", "Arial", "sans-serif"):
        if not available or name in available or name == "sans-serif":
            return name
    return "TkDefaultFont"


_UI_FONT = None


def _font_family():
    global _UI_FONT
    if _UI_FONT is None:
        _UI_FONT = _pick_ui_font()
    return _UI_FONT


# ─────────────────────────────────────────────
# Font Scaling
# ─────────────────────────────────────────────
_FONT_ROLES = {
    "h1": (24, "bold"),
    "h2": (20, "bold"),
    "h3": (16, "bold"),
    "h4": (14, "bold"),
    "body": (11, "normal"),
    "body_b": (11, "bold"),
    "small": (10, "normal"),
    "small_b": (10, "bold"),
    "caption": (9, "normal"),
    "caption_b": (9, "bold"),
    "tiny": (8, "bold"),
    "btn": (12, "bold"),
    "btn_sm": (11, "bold"),
    "nav": (11, "normal"),
    "nav_active": (11, "bold"),
    "brand": (14, "bold"),
    "chat": (11, "normal"),
    "chat_hdr": (10, "bold"),
}


def get_font(role):
    """Return a font tuple for the given role string."""
    size, weight = _FONT_ROLES.get(role, _FONT_ROLES["body"])
    return (_font_family(), size, weight)


# ─────────────────────────────────────────────
# Hover Helper
# ─────────────────────────────────────────────
def add_hover(widget, enter_bg=None, leave_bg=None, enter_fg=None, leave_fg=None):
    """
    Bind <Enter>/<Leave> events for instant visual feedback.
    Only changes the attributes that are passed (non-None).
    """
    def on_enter(e):
        if enter_bg:
            widget.config(bg=enter_bg)
        if enter_fg:
            widget.config(fg=enter_fg)

    def on_leave(e):
        if leave_bg:
            widget.config(bg=leave_bg)
        if leave_fg:
            widget.config(fg=leave_fg)

    widget.bind("<Enter>", on_enter, add="+")
    widget.bind("<Leave>", on_leave, add="+")


# ─────────────────────────────────────────────
# Card Factory
# ─────────────────────────────────────────────
def create_card(parent, bg=None, border_color=None, hover=False, hover_border=None):
    """
    Create a card-style Frame with consistent border styling.
    If hover=True, the border color shifts on mouse enter/leave.
    """
    bg = bg or COLORS["surface"]
    border_color = border_color or COLORS["border"]
    card = tk.Frame(parent, bg=bg, highlightbackground=border_color, highlightthickness=1)

    if hover:
        hb = hover_border or COLORS["primary"]

        def _enter(e):
            card.config(highlightbackground=hb)

        def _leave(e):
            card.config(highlightbackground=border_color)

        card.bind("<Enter>", _enter)
        card.bind("<Leave>", _leave)
        # Also bind to children so hovering inner labels doesn't flicker

        def _bind_children(widget):
            for child in widget.winfo_children():
                child.bind("<Enter>", _enter, add="+")
                child.bind("<Leave>", _leave, add="+")
        card.after(100, lambda: _bind_children(card))

    return card


# ─────────────────────────────────────────────
# Entry Focus Glow
# ─────────────────────────────────────────────
def add_focus_glow(entry, focus_color=None, blur_color=None):
    """
    Change the entry's highlight/border color on focus and blur.
    """
    fc = focus_color or COLORS["primary"]
    bc = blur_color or COLORS["border"]

    def on_focus(e):
        entry.config(highlightbackground=fc, highlightcolor=fc, highlightthickness=2)

    def on_blur(e):
        entry.config(highlightbackground=bc, highlightcolor=bc, highlightthickness=1)

    entry.bind("<FocusIn>", on_focus, add="+")
    entry.bind("<FocusOut>", on_blur, add="+")


# ─────────────────────────────────────────────
# Animated Arc Draw
# ─────────────────────────────────────────────
def animate_arc(canvas, cx, cy, r, target_pct, current_pct=0, arc_color=None,
                bg_ring_color=None, label_font=None, sub_label="", step=2, delay=12):
    """
    Smoothly draw a progress arc from current_pct → target_pct on a canvas.
    """
    arc_color = arc_color or COLORS["primary"]
    bg_ring_color = bg_ring_color or COLORS["surface_alt"]
    label_font = label_font or get_font("h2")

    x1, y1 = cx - r, cy - r
    x2, y2 = cx + r, cy + r
    target_pct = max(0, min(100, int(target_pct or 0)))

    def _draw(pct):
        canvas.delete("all")
        # Background ring
        canvas.create_oval(x1, y1, x2, y2, outline=bg_ring_color, width=10)
        # Progress arc
        extent = -(pct / 100.0) * 360
        canvas.create_arc(x1, y1, x2, y2, start=90, extent=extent, outline=arc_color, width=10, style="arc")
        # Center text
        canvas.create_text(cx, cy - 8, text=f"{int(pct)}%", font=label_font, fill=COLORS["text"])
        if sub_label:
            canvas.create_text(cx, cy + 14, text=sub_label, font=get_font("tiny"), fill=COLORS["text_muted"])

        if pct < target_pct:
            next_pct = min(pct + step, target_pct)
            canvas.after(delay, lambda: _draw(next_pct))
        elif pct > target_pct:
            # Allow redrawing lower values without animation glitches
            canvas.create_text(cx, cy - 8, text=f"{target_pct}%", font=label_font, fill=COLORS["text"])

    _draw(current_pct)


# ─────────────────────────────────────────────
# Typing Indicator Animation
# ─────────────────────────────────────────────
class TypingIndicator(tk.Frame):
    """Animated '...' dots to show the AI is composing a response."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS["surface"], **kwargs)
        self._dots_label = tk.Label(self, text="AI is typing", font=get_font("small"),
                                    fg=COLORS["text_muted"], bg=COLORS["surface"])
        self._dots_label.pack(anchor="w", padx=25, pady=8)
        self._dot_count = 0
        self._anim_id = None

    def start(self):
        self._animate()

    def _animate(self):
        self._dot_count = (self._dot_count % 3) + 1
        dots = "●  " * self._dot_count
        self._dots_label.config(text=f"AI is typing {dots.strip()}")
        self._anim_id = self.after(400, self._animate)

    def stop(self):
        if self._anim_id:
            self.after_cancel(self._anim_id)
            self._anim_id = None


# ─────────────────────────────────────────────
# Pulse Animation (for streak flame etc.)
# ─────────────────────────────────────────────
def pulse_label(label, color_a, color_b, interval=800):
    """Toggle a label's fg between two colors to create a pulse effect."""
    _current = {"c": color_a}

    def _toggle():
        _current["c"] = color_b if _current["c"] == color_a else color_a
        try:
            label.config(fg=_current["c"])
        except tk.TclError:
            return  # widget was destroyed
        label.after(interval, _toggle)

    _toggle()


def bind_mousewheel(widget, canvas):
    """Cross-platform mousewheel binding for scrollable canvases."""
    def _on_mousewheel(event):
        if getattr(event, "num", None) == 4 or getattr(event, "delta", 0) > 0:
            canvas.yview_scroll(-1, "units")
        elif getattr(event, "num", None) == 5 or getattr(event, "delta", 0) < 0:
            canvas.yview_scroll(1, "units")

    def _bind(_event=None):
        widget.bind_all("<MouseWheel>", _on_mousewheel)
        widget.bind_all("<Button-4>", _on_mousewheel)
        widget.bind_all("<Button-5>", _on_mousewheel)

    def _unbind(_event=None):
        widget.unbind_all("<MouseWheel>")
        widget.unbind_all("<Button-4>")
        widget.unbind_all("<Button-5>")

    widget.bind("<Enter>", _bind)
    widget.bind("<Leave>", _unbind)
