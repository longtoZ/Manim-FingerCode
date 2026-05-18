"""
scenes/s2a_polar_grid_text.py
----------------------------
Text Interlude B — Polar Grid Intuition

Standalone render
-----------------
    manim -pql scenes/s2a_polar_grid_text.py PolarGridTextScene
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import (
    FP_BG_COLOR,
    FP_ACCENT_GOLD,
    FP_ACCENT_TEAL,
    FP_TEXT_PRIMARY,
    FP_TEXT_DIM,
    N_RINGS,
    N_SECTORS,
)

try:
    import manimpango
    _available = {f.lower() for f in manimpango.list_fonts()}
    FP_FONT = "Fira Sans" if "fira sans" in _available else ""
except Exception:
    FP_FONT = ""


class PolarGridTextScene(Scene):
    """Text-only explanation of polar tessellation."""

    def construct(self):
        self.camera.background_color = FP_BG_COLOR

        title = Text(
            "Why a Polar Grid?",
            font=FP_FONT, font_size=38,
            color=FP_ACCENT_GOLD, weight=BOLD,
        )
        title.to_edge(UP, buff=0.6)

        para_1 = Text(
            "The grid is centered on the core to anchor all measurements,\n"
            "so rings capture distance while sectors capture ridge direction,\n"
            "and rotation shifts angles but keeps ring order consistent.",
            font=FP_FONT, font_size=20, color=FP_TEXT_PRIMARY,
        )
        para_2 = Text(
            f"With {N_RINGS} rings and {N_SECTORS} sectors, the AOI becomes\n"
            f"{N_RINGS * N_SECTORS} local cells that can be measured uniformly.",
            font=FP_FONT, font_size=20, color=FP_TEXT_PRIMARY,
        )
        tag = Text(
            "AOI = the area of interest we analyze around the core",
            font=FP_FONT, font_size=18, color=FP_ACCENT_TEAL,
        )
        paragraph_text = VGroup(para_1, para_2, tag).arrange(
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
