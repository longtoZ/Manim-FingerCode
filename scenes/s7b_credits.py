"""
scenes/s7b_credits.py
---------------------
Phase 8b — Credits / References

Standalone render
-----------------
    manim -pql scenes/s7b_credits.py CreditsScene
"""

from __future__ import annotations
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import (
    FP_BG_COLOR, FP_ACCENT_GOLD, FP_ACCENT_TEAL,
    FP_TEXT_PRIMARY, FP_TEXT_DIM,
)

try:
    import manimpango
    _av = {f.lower() for f in manimpango.list_fonts()}
    FP_FONT = "Fira Sans" if "fira sans" in _av else ""
except Exception:
    FP_FONT = ""


class CreditsScene(Scene):
    """Credits and reference information."""

    def construct(self):
        self.camera.background_color = FP_BG_COLOR

        # ── Title ──────────────────────────────────────────────────────── #
        title = Text(
            "References & Credits",
            font=FP_FONT, font_size=38,
            color=FP_ACCENT_GOLD, weight=BOLD,
        )
        title.to_edge(UP, buff=0.8)

        # ── Paper reference ───────────────────────────────────────────── #
        ref_header = Text(
            "Original Paper",
            font=FP_FONT, font_size=22,
            color=FP_ACCENT_TEAL, weight=BOLD,
        )
        ref_lines = VGroup(
            Text("Hong, L., Wan, Y., & Jain, A. (1998).",
                 font=FP_FONT, font_size=18, color=FP_TEXT_PRIMARY),
            Text("Fingerprint Image Enhancement: Algorithm and",
                 font=FP_FONT, font_size=18, color=FP_TEXT_PRIMARY),
            Text("Performance Evaluation.",
                 font=FP_FONT, font_size=18, color=FP_TEXT_PRIMARY),
            Text("IEEE Transactions on Pattern Analysis and",
                 font=FP_FONT, font_size=18, color=FP_TEXT_PRIMARY),
            Text("Machine Intelligence, 20(8), 777–789.",
                 font=FP_FONT, font_size=18, color=FP_TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        ref_group = VGroup(ref_header, ref_lines).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2
        )
        ref_group.shift(UP * 0.3)

        # ── Divider ───────────────────────────────────────────────────── #
        divider = Line(
            LEFT * 3.5, RIGHT * 3.5,
            stroke_color="#3a3a5c", stroke_width=1.0, stroke_opacity=0.5,
        )
        divider.next_to(ref_group, DOWN, buff=0.4)

        # ── Production credit ─────────────────────────────────────────── #
        prod_text = Text(
            "Animated with Manim",
            font=FP_FONT, font_size=20,
            color=FP_TEXT_DIM,
        )
        prod_text.next_to(divider, DOWN, buff=0.35)

        # ── Narration hold ────────────────────────────────────────────── #
        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(ref_group, shift=UP * 0.1), run_time=0.8)
        self.play(Create(divider), run_time=0.5)
        self.play(FadeIn(prod_text, shift=UP * 0.1), run_time=0.6)

        self.wait(3.0)

        # ── Fade out ──────────────────────────────────────────────────── #
        self.play(
            FadeOut(title), FadeOut(ref_group),
            FadeOut(divider), FadeOut(prod_text),
            run_time=1.2,
        )
        self.wait(0.5)