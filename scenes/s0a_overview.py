"""
scenes/s0a_overview.py
----------------------
Text Interlude A — Algorithm Overview

A text-only scene to clarify goals and extend runtime.

Standalone render
-----------------
    manim -pql scenes/s0a_overview.py OverviewTextScene
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


class OverviewTextScene(Scene):
    """Text-only overview of the FingerCode pipeline."""

    def construct(self):
        self.camera.background_color = FP_BG_COLOR

        title = Text(
            "How FingerCode Works",
            font=FP_FONT, font_size=40,
            color=FP_ACCENT_GOLD, weight=BOLD,
        )
        subtitle = Text(
            "Goal: compress a fingerprint into a stable, comparable code",
            font=FP_FONT, font_size=20,
            color=FP_TEXT_DIM,
        )
        title.to_edge(UP, buff=0.6)
        subtitle.next_to(title, DOWN, buff=0.2)

        para_1 = Text(
            "We start with a single fingerprint image that may contain noise,\n"
            "contrast changes, or small distortions, and we aim to turn it\n"
            "into a compact code that is stable across different captures.",
            font=FP_FONT, font_size=20, color=FP_TEXT_PRIMARY,
        )
        para_2 = Text(
            "The pipeline first finds the core, tessellates the AOI, and\n"
            "normalizes contrast, then it filters oriented texture, extracts\n"
            "features, and compares the resulting FingerCode vectors.",
            font=FP_FONT, font_size=20, color=FP_TEXT_PRIMARY,
        )
        paragraph_text = VGroup(para_1, para_2).arrange(
            DOWN, aligned_edge=LEFT, buff=0.24
        )
        paragraph_text.next_to(subtitle, DOWN, buff=0.45)

        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(subtitle, shift=UP * 0.1), run_time=0.6)

        self.play(FadeIn(paragraph_text, shift=UP * 0.08), run_time=0.8)

        self.wait(2.0)

        self.play(
            FadeOut(title), FadeOut(subtitle), FadeOut(paragraph_text),
            run_time=0.8,
        )
        self.wait(0.3)
