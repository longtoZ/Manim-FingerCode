"""
scenes/s6b_distance_formula.py
------------------------------
Text Interlude E — Distance Formula

Standalone render
-----------------
    manim -pql scenes/s6b_distance_formula.py DistanceFormulaScene
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


class DistanceFormulaScene(Scene):
    """Text-only explanation of the distance equation."""

    def construct(self):
        self.camera.background_color = FP_BG_COLOR

        title = Text(
            "Distance Equation",
            font=FP_FONT, font_size=36,
            color=FP_ACCENT_GOLD, weight=BOLD,
        )
        title.to_edge(UP, buff=0.6)

        formula_bg = RoundedRectangle(
            width=6.2, height=1.1, corner_radius=0.15,
            fill_color="#0d0d1a", fill_opacity=0.92,
            stroke_color=FP_ACCENT_GOLD, stroke_width=1.2,
        )
        try:
            formula_tex = MathTex(
                r"d(T,I) = \sqrt{\sum_{i=1}^{n}(T_i - I_i)^2}",
                color=FP_TEXT_PRIMARY, font_size=36,
            )
        except Exception:
            formula_tex = Text(
                "d(T,I) = sqrt( Σ (Tᵢ − Iᵢ)² )",
                font=FP_FONT, font_size=24, color=FP_TEXT_PRIMARY,
            )
        formula_group = VGroup(formula_bg, formula_tex)
        formula_tex.move_to(formula_bg)
        formula_group.next_to(title, DOWN, buff=0.35)

        para_1 = Text(
            "We take the difference at every index, square it, and sum the results\n"
            "so the distance reflects total mismatch across all sectors.",
            font=FP_FONT, font_size=19, color=FP_TEXT_DIM,
        )
        para_2 = Text(
            "A single scalar distance makes it easy to compare against a threshold\n"
            "and decide whether the two fingerprints belong to the same finger.",
            font=FP_FONT, font_size=19, color=FP_TEXT_DIM,
        )
        para_group = VGroup(para_1, para_2).arrange(
            DOWN, aligned_edge=LEFT, buff=0.24
        )
        para_group.next_to(formula_group, DOWN, buff=0.4)

        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(formula_group, shift=UP * 0.1), run_time=0.7)
        self.play(FadeIn(para_group, shift=UP * 0.08), run_time=0.9)
        self.wait(2.2)

        self.play(
            FadeOut(title), FadeOut(formula_group), FadeOut(para_group),
            run_time=0.8,
        )
        self.wait(0.3)
