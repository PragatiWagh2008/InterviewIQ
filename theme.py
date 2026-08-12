"""
InterviewIQ — Centralized Theme Engine
Provides colors, hover helpers, card factories, focus glow, and font scaling.
Palette mirrors the "AI Interview Pro" reference design (ink / cream / teal / coral).
"""
import math
import tkinter as tk
import tkinter.font as tkfont


# ─────────────────────────────────────────────
# Color Palette
# ─────────────────────────────────────────────
COLORS = {
    # Ink / navy (primary CTAs, sidebar, selected states)
    "ink":              "#12213B",
    "ink_soft":         "#1C2E4E",
    "sidebar":          "#12213B",
    "sidebar_text":     "#C7CEDD",
    "sidebar_muted":    "#9AA5B8",

    # Surfaces
    "bg":               "#F7F5F1",
    "surface":          "#FFFFFF",
    "surface_alt":      "#EFEEE8",
    "surface_hover":    "#E7E4DD",

    # Borders
    "border":           "#E7E4DD",
    "border_light":     "#D8D4CB",
    "border_focus":     "#17A98C",

    # Primary accent — teal
    "primary":          "#17A98C",
    "primary_hover":    "#0E7A63",
    "primary_light":    "#E7F5F0",
    "primary_lighter":  "#D3EFE6",

    # Secondary accent — coral
    "coral":            "#FF6B4A",
    "coral_soft":       "#FFE3DA",
    "mint":             "#E7F5F0",

    # Text
    "text":             "#12213B",
    "text_secondary":   "#1C2E4E",
    "text_muted":       "#657289",
    "text_faint":       "#9AA5B8",

    # Accent — Success (teal family)
    "success":          "#17A98C",
    "success_bg":       "#E7F5F0",
    "success_border":   "#CDE8E0",
    "success_text":     "#0E7A63",
    "success_dark":     "#0E7A63",

    # Accent — Danger (coral family)
    "danger":           "#FF6B4A",
    "danger_bg":        "#FFE3DA",
    "danger_border":    "#FFD2C4",

    # Accent — Warning / Streak
    "streak_bg":        "#FFE3DA",
    "streak_border":    "#FFD2C4",
    "streak_text":      "#D14A2A",

    # Accent — Info
    "info_bg":          "#E7F5F0",
    "info_border":      "#CDE8E0",
    "info_text":        "#0E7A63",
    "info_dark":        "#0E7A63",
}


def _pick_ui_font():
    """Prefer Inter (the reference body font); fall back to Segoe UI on Windows."""
    try:
        available = set(tkfont.families())
    except Exception:
        available = set()
    for name in ("Inter", "Segoe UI", "Ubuntu", "Noto Sans", "DejaVu Sans",
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
    "brand": (15, "bold"),
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
    
    Returns a stop function that can be called to cancel the animation.
    """
    arc_color = arc_color or COLORS["primary"]
    bg_ring_color = bg_ring_color or COLORS["surface_alt"]
    label_font = label_font or get_font("h2")

    x1, y1 = cx - r, cy - r
    x2, y2 = cx + r, cy + r
    target_pct = max(0, min(100, int(target_pct or 0)))

    _anim_state = {"after_id": None, "cancelled": False}

    def _draw(pct):
        if _anim_state["cancelled"]:
            return
        try:
            canvas.delete("all")
        except tk.TclError:
            return  # Canvas destroyed
        
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
            _anim_state["after_id"] = canvas.after(delay, lambda: _draw(next_pct))
        elif pct > target_pct:
            # Allow redrawing lower values without animation glitches
            canvas.create_text(cx, cy - 8, text=f"{target_pct}%", font=label_font, fill=COLORS["text"])

    def _cancel():
        _anim_state["cancelled"] = True
        if _anim_state["after_id"]:
            try:
                canvas.after_cancel(_anim_state["after_id"])
            except tk.TclError:
                pass
            _anim_state["after_id"] = None

    _draw(current_pct)
    return _cancel


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
        self._running = False

    def start(self):
        self._running = True
        self._animate()

    def _animate(self):
        if not self._running:
            return
        try:
            self._dot_count = (self._dot_count % 3) + 1
            dots = "●  " * self._dot_count
            self._dots_label.config(text=f"AI is typing {dots.strip()}")
            self._anim_id = self.after(400, self._animate)
        except tk.TclError:
            self._running = False

    def stop(self):
        self._running = False
        if self._anim_id:
            try:
                self.after_cancel(self._anim_id)
            except tk.TclError:
                pass
            self._anim_id = None


# ─────────────────────────────────────────────
# Pulse Animation (for streak flame etc.)
# ─────────────────────────────────────────────
def pulse_label(label, color_a, color_b, interval=800):
    """Toggle a label's fg between two colors to create a pulse effect.
    
    Returns a stop function that can be called to cancel the animation.
    """
    _current = {"c": color_a, "running": True}

    def _toggle():
        if not _current["running"]:
            return
        try:
            _current["c"] = color_b if _current["c"] == color_a else color_a
            label.config(fg=_current["c"])
            label.after(interval, _toggle)
        except tk.TclError:
            _current["running"] = False

    def _stop():
        _current["running"] = False

    _toggle()
    return _stop


def bind_mousewheel(widget, canvas):
    """Cross-platform mousewheel binding for scrollable canvases.
    
    Uses widget-specific bindings instead of bind_all to avoid conflicts
    between multiple scrollable areas.
    """
    def _on_mousewheel(event):
        if getattr(event, "num", None) == 4 or getattr(event, "delta", 0) > 0:
            canvas.yview_scroll(-1, "units")
        elif getattr(event, "num", None) == 5 or getattr(event, "delta", 0) < 0:
            canvas.yview_scroll(1, "units")

    def _bind(_event=None):
        widget.bind("<MouseWheel>", _on_mousewheel)
        widget.bind("<Button-4>", _on_mousewheel)
        widget.bind("<Button-5>", _on_mousewheel)
        # Also bind to canvas for when mouse is over scrollbar area
        canvas.bind("<MouseWheel>", _on_mousewheel)
        canvas.bind("<Button-4>", _on_mousewheel)
        canvas.bind("<Button-5>", _on_mousewheel)

    def _unbind(_event=None):
        widget.unbind("<MouseWheel>")
        widget.unbind("<Button-4>")
        widget.unbind("<Button-5>")
        canvas.unbind("<MouseWheel>")
        canvas.unbind("<Button-4>")
        canvas.unbind("<Button-5>")

    widget.bind("<Enter>", _bind)
    widget.bind("<Leave>", _unbind)
    # Also bind on canvas enter/leave
    canvas.bind("<Enter>", _bind)
    canvas.bind("<Leave>", _unbind)


# ─────────────────────────────────────────────
# Logo (coral + teal infinity mark from the reference design)
# ─────────────────────────────────────────────
def _svg_arc_points(x1, y1, x2, y2, rx, ry, phi, large_arc, sweep, steps=32):
    """Convert an SVG elliptical-arc command into a polyline of points."""
    if rx == 0 or ry == 0:
        return [(x1, y1), (x2, y2)]
    rx, ry = abs(rx), abs(ry)
    cphi, sphi = math.cos(phi), math.sin(phi)

    dx = (x1 - x2) / 2.0
    dy = (y1 - y2) / 2.0
    x1p = cphi * dx + sphi * dy
    y1p = -sphi * dx + cphi * dy

    lam = (x1p * x1p) / (rx * rx) + (y1p * y1p) / (ry * ry)
    if lam > 1:
        s = math.sqrt(lam)
        rx *= s
        ry *= s

    num = rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p
    den = rx * rx * y1p * y1p + ry * ry * x1p * x1p
    if den == 0:
        return [(x1, y1), (x2, y2)]
    coef = math.sqrt(max(num / den, 0.0))
    sign = -1 if large_arc == sweep else 1
    cxp = sign * coef * (rx * y1p / ry)
    cyp = sign * coef * (-ry * x1p / rx)

    cx = cphi * cxp - sphi * cyp + (x1 + x2) / 2.0
    cy = sphi * cxp + cphi * cyp + (y1 + y2) / 2.0

    def _angle(ux, uy, vx, vy):
        dot = ux * vx + uy * vy
        mag = math.hypot(ux, uy) * math.hypot(vx, vy)
        ang = math.acos(max(-1.0, min(1.0, dot / mag)))
        if ux * vy - uy * vx < 0:
            ang = -ang
        return ang

    theta1 = _angle(1, 0, (x1 - cx) / rx, (y1 - cy) / ry)
    theta2 = _angle((x1 - cx) / rx, (y1 - cy) / ry, (x2 - cx) / rx, (y2 - cy) / ry)
    delta = theta2
    if not sweep and delta > 0:
        delta -= 2 * math.pi
    elif sweep and delta < 0:
        delta += 2 * math.pi

    n = max(int(steps * abs(delta) / math.pi) + 2, 8)
    pts = []
    for i in range(n + 1):
        t = theta1 + delta * (i / n)
        pts.append((cx + rx * math.cos(t) * cphi - ry * math.sin(t) * sphi,
                    cy + rx * math.cos(t) * sphi + ry * math.sin(t) * cphi))
    return pts


def draw_logo(canvas, size=None):
    """Render the InterviewIQ infinity logo (coral + teal + white dot) on a canvas."""
    canvas.delete("all")
    cw = canvas.winfo_width() if canvas.winfo_width() > 1 else (size or 40)
    ch = canvas.winfo_height() if canvas.winfo_height() > 1 else (size or 40)
    scale = min(cw, ch) / 130.0
    ox, oy = cw / 2.0, ch / 2.0

    def P(x, y):
        return (ox + x * scale, oy + y * scale)

    def arc_pts(x1, y1, x2, y2, r, large, sweep):
        return [P(x, y) for x, y in _svg_arc_points(x1, y1, x2, y2, r, r, 0.0, large, sweep)]

    # Left coral crescent
    outer_l = arc_pts(-37, -11, 11, 37, 37, 1, 1)
    inner_l = arc_pts(-1, 37, -37, 1, 25, 0, 0)
    left_pts = outer_l + [P(-1, 37)] + inner_l + [P(-37, -11)]
    canvas.create_polygon(left_pts, fill=COLORS["coral"], outline="", smooth=True)

    # Right teal crescent
    outer_r = arc_pts(37, 11, -11, -37, 37, 1, 1)
    inner_r = arc_pts(1, -37, 37, -1, 25, 0, 0)
    right_pts = outer_r + [P(1, -37)] + inner_r + [P(37, 11)]
    canvas.create_polygon(right_pts, fill=COLORS["primary"], outline="", smooth=True)

    # Round end caps
    for pt, color in ((P(-37, 1), COLORS["coral"]), (P(37, -1), COLORS["primary"])):
        rd = 9 * scale
        canvas.create_oval(pt[0] - rd, pt[1] - rd, pt[0] + rd, pt[1] + rd, fill=color, outline="")

    # White center dot
    c = P(0, 0)
    cd = 8 * scale
    canvas.create_oval(c[0] - cd, c[1] - cd, c[0] + cd, c[1] + cd, fill="#FFFFFF", outline="")


# ─────────────────────────────────────────────
# Decorative wave (bottom of the welcome card)
# ─────────────────────────────────────────────
def draw_wave(canvas):
    """Draw the teal → ink dome from the welcome screen reference design."""
    canvas.delete("all")
    w = canvas.winfo_width() if canvas.winfo_width() > 1 else 300
    h = canvas.winfo_height() if canvas.winfo_height() > 1 else 90

    # Deep ink dome (peeks out beneath the teal for depth)
    canvas.create_oval(-w * 0.25, h * 0.55, w * 1.25, h * 2.6, fill=COLORS["ink"], outline="")
    # Teal dome
    canvas.create_oval(-w * 0.22, h * 0.35, w * 1.22, h * 2.4, fill=COLORS["primary"], outline="")
    # Coral accent sliver
    canvas.create_oval(w * 0.55, h * 0.5, w * 1.35, h * 2.55, fill=COLORS["coral"], outline="")
