"""
scenes/s6a_matching_text.py
---------------------------
Text Interlude C — Matching Logic

Standalone render
-----------------
    manim -pql scenes/s6a_matching_text.py MatchingTextScene
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import (
    FP_BG_COLOR,
    FP_ACCENT_GOLD,
    FP_TEXT_PRIMARY,
    FP_TEXT_DIM,
)

try:
    import manimpango
    _available = {f.lower() for f in manimpango.list_fonts()}
    FP_FONT = "Fira Sans" if "fira sans" in _available else ""
except Exception:
    FP_FONT = ""


class MatchingTextScene(Scene):
    """Text-only explanation of matching logic."""

    def construct(self):
        self.camera.background_color = FP_BG_COLOR

        title = Text(
            "Matching Logic",
            font=FP_FONT, font_size=38,
            color=FP_ACCENT_GOLD, weight=BOLD,
        )
        title.to_edge(UP, buff=0.6)

        para_1 = Text(
            "We compare the 128-D FingerCode from the template with the 128-D\n"
            "FingerCode from the input, and we summarize all local differences\n"
            "into a single distance score d(T, I).",
            font=FP_FONT, font_size=20, color=FP_TEXT_PRIMARY,
        )
        para_2 = Text(
            "A smaller distance indicates stronger similarity across ridge\n"
            "texture, and the threshold is tuned to balance false matches\n"
            "against false misses in the final decision.",
            font=FP_FONT, font_size=18, color=FP_TEXT_DIM,
        )
        paragraph_text = VGroup(para_1, para_2).arrange(
            DOWN, aligned_edge=LEFT, buff=0.24
        )
        paragraph_text.next_to(title, DOWN, buff=0.4)

        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(paragraph_text, shift=UP * 0.08), run_time=0.9)

        self.wait(2.2)

        self.play(
            FadeOut(title), FadeOut(paragraph_text),
            run_time=0.8,
        )
        self.wait(0.3)
