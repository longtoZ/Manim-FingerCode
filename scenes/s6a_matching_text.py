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

        bullets = [
            "- Compare two 128-D FingerCode vectors from the template and input",
            "- Compute a distance d(T, I) that summarizes all local differences",
            "- Lower distance indicates stronger similarity across ridge texture",
            "- If d is below a threshold, we accept a match as the same finger",
        ]
        bullet_text = VGroup(*[
            Text(line, font=FP_FONT, font_size=20, color=FP_TEXT_PRIMARY)
            for line in bullets
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        bullet_text.next_to(title, DOWN, buff=0.4)

        note = Text(
            "The threshold is tuned to balance false matches against false misses",
            font=FP_FONT, font_size=18, color=FP_TEXT_DIM,
        )
        note.next_to(bullet_text, DOWN, buff=0.35)

        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.7)
        for line in bullet_text:
            self.play(FadeIn(line, shift=UP * 0.08), run_time=0.45)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.6)

        self.wait(2.2)

        self.play(
            FadeOut(title), FadeOut(bullet_text), FadeOut(note),
            run_time=0.8,
        )
        self.wait(0.3)
