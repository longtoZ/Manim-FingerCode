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

        bullets = [
            "- The grid is centered on the core point to anchor all measurements",
            "- Rings capture distance from the core so radial structure is preserved",
            "- Sectors capture ridge flow direction so orientation is measured explicitly",
            "- Rotation shifts angles but preserves ring order, which keeps the layout stable",
            f"- {N_RINGS} rings x {N_SECTORS} sectors = {N_RINGS * N_SECTORS} local cells",
        ]
        bullet_text = VGroup(*[
            Text(line, font=FP_FONT, font_size=20, color=FP_TEXT_PRIMARY)
            for line in bullets
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        bullet_text.next_to(title, DOWN, buff=0.4)

        tag = Text(
            "AOI = the area of interest we analyze around the core",
            font=FP_FONT, font_size=18, color=FP_ACCENT_TEAL,
        )
        tag.next_to(bullet_text, DOWN, buff=0.35)

        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.7)
        for line in bullet_text:
            self.play(FadeIn(line, shift=UP * 0.08), run_time=0.45)
        self.play(FadeIn(tag, shift=UP * 0.08), run_time=0.5)

        self.wait(2.2)

        self.play(
            FadeOut(title), FadeOut(bullet_text), FadeOut(tag),
            run_time=0.8,
        )
        self.wait(0.3)
