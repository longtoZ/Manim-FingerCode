"""
scenes/s0_intro.py
------------------
Phase 1 — Scene 0: Introduction & Title Card

Animation flow
--------------
1. Deep-navy background fades in.
2. Fingerprint image fades in, slightly dimmed, as a backdrop.
3. A glowing horizontal divider line draws itself.
4. Main title ("FingerCode Algorithm") writes itself in from the left.
5. Subtitle ("A Texture-Based Fingerprint Recognition Method") fades up.
6. A small "step pipeline" counter bar fades in at the bottom, showing
   the six algorithm steps as labelled boxes — Step 1 highlighted.
7. Narration pause (2 s).
8. Everything fades out smoothly before the next scene.

Standalone render
-----------------
    manim -pql scenes/s0_intro.py IntroScene
"""

from __future__ import annotations

from manim import *
import sys
import os

# Allow imports from the project root when running the file directly.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import (
    FP_BG_COLOR,
    FP_ACCENT_GOLD,
    FP_ACCENT_TEAL,
    FP_TEXT_PRIMARY,
    FP_TEXT_DIM,
    ASSET_FP_QUERY,
)

# Resolve preferred font with a safe fallback
try:
    import manimpango
    _available_fonts = {f.lower() for f in manimpango.list_fonts()}
    FP_FONT = "Fira Sans" if "fira sans" in _available_fonts else ""
except Exception:
    FP_FONT = ""  # empty string → Manim uses its built-in default


# ---------------------------------------------------------------------------
# Helper: step-pipeline bar
# ---------------------------------------------------------------------------

STEP_LABELS = [
    "Reference\nPoint",
    "Tessellation",
    "Normalization",
    "Filtering",
    "Feature\nExtraction",
    "Matching",
]


def _build_pipeline_bar(active_index: int = -1) -> VGroup:
    """Return a compact horizontal pipeline bar showing all 6 algorithm steps.

    The box at *active_index* is highlighted in gold; all others are dim.
    Pass ``active_index=-1`` (default) to show all boxes with equal dimmed
    styling (used in the intro where no step is active yet).
    """
    boxes = VGroup()
    arrows = VGroup()

    box_w, box_h = 1.35, 0.65
    gap = 0.18

    for i, label in enumerate(STEP_LABELS):
        is_active = (i == active_index)

        box = RoundedRectangle(
            width=box_w,
            height=box_h,
            corner_radius=0.1,
            fill_color=FP_ACCENT_GOLD if is_active else "#1a1a2e",
            fill_opacity=0.85 if is_active else 0.6,
            stroke_color=FP_ACCENT_GOLD if is_active else "#3a3a5c",
            stroke_width=1.5,
        )
        step_num = Text(
            f"Step {i + 1}",
            font=FP_FONT,
            font_size=10,
            color="#0d0d1a" if is_active else FP_ACCENT_GOLD,
            weight=BOLD,
        ).move_to(box.get_top() + DOWN * 0.15)
        lbl = Text(
            label,
            font=FP_FONT,
            font_size=11,
            color="#0d0d1a" if is_active else FP_TEXT_DIM,
            line_spacing=0.5,
        ).move_to(box.get_center() + DOWN * 0.05)

        cell = VGroup(box, step_num, lbl)
        boxes.add(cell)

    boxes.arrange(RIGHT, buff=gap)

    # Connector arrows between boxes
    for i in range(len(STEP_LABELS) - 1):
        left_box  = boxes[i][0]
        right_box = boxes[i + 1][0]
        arr = Arrow(
            start=left_box.get_right(),
            end=right_box.get_left(),
            buff=0.04,
            max_tip_length_to_length_ratio=0.4,
            stroke_width=1.5,
            color="#3a3a5c",
        )
        arrows.add(arr)

    return VGroup(boxes, arrows)


# ---------------------------------------------------------------------------
# Main scene class
# ---------------------------------------------------------------------------

class IntroScene(Scene):
    """Phase 1 — Introduction & Title Card."""

    def construct(self):
        self.camera.background_color = FP_BG_COLOR

        # ------------------------------------------------------------------ #
        # 1. Fingerprint backdrop                                              #
        # ------------------------------------------------------------------ #
        fp_img = ImageMobject(ASSET_FP_QUERY)
        fp_img.set_height(6.5)
        fp_img.set_opacity(0.12)          # very subtle — texture, not focus
        fp_img.move_to(ORIGIN)

        self.play(FadeIn(fp_img, run_time=1.2))

        # ------------------------------------------------------------------ #
        # 2. Glowing horizontal divider                                        #
        # ------------------------------------------------------------------ #
        divider = Line(
            LEFT * 4.5, RIGHT * 4.5,
            stroke_color=FP_ACCENT_TEAL,
            stroke_width=1.5,
            stroke_opacity=0.6,
        ).move_to(UP * 0.55)

        self.play(Create(divider), run_time=0.7)

        # ------------------------------------------------------------------ #
        # 3. Main title                                                        #
        # ------------------------------------------------------------------ #
        title = Text(
            "FingerCode Algorithm",
            font=FP_FONT,
            color=FP_TEXT_PRIMARY,
            font_size=58,
            weight=BOLD,
        ).next_to(divider, UP, buff=0.35)

        # Accent: colour "FingerCode" in gold, "Algorithm" stays white
        title_fc = Text(
            "FingerCode",
            font=FP_FONT,
            color=FP_ACCENT_GOLD,
            font_size=58,
            weight=BOLD,
        )
        title_algo = Text(
            " Algorithm",
            font=FP_FONT,
            color=FP_TEXT_PRIMARY,
            font_size=58,
            weight=BOLD,
        )
        title_group = VGroup(title_fc, title_algo).arrange(RIGHT, buff=0).next_to(
            divider, UP, buff=0.35
        )

        self.play(
            FadeIn(title_group, shift=UP * 0.25),
            run_time=1.0,
        )

        # ------------------------------------------------------------------ #
        # 4. Subtitle                                                          #
        # ------------------------------------------------------------------ #
        subtitle = Text(
            "A Texture-Based Fingerprint Recognition Method",
            font=FP_FONT,
            color=FP_TEXT_DIM,
            font_size=26,
        ).next_to(divider, DOWN, buff=0.35)

        self.play(FadeIn(subtitle, shift=UP * 0.15), run_time=0.8)

        # ------------------------------------------------------------------ #
        # 5. Step pipeline bar (all boxes dim — intro, no active step)         #
        # ------------------------------------------------------------------ #
        pipeline = _build_pipeline_bar(active_index=-1)
        pipeline.scale(0.82)
        pipeline.to_edge(DOWN, buff=0.45)

        pipeline_label = Text(
            "Algorithm Pipeline",
            font=FP_FONT,
            font_size=14,
            color=FP_TEXT_DIM,
        ).next_to(pipeline, UP, buff=0.18)

        self.play(
            FadeIn(pipeline_label),
            LaggedStart(
                *[FadeIn(cell, shift=UP * 0.1) for cell in pipeline[0]],
                lag_ratio=0.12,
            ),
            FadeIn(pipeline[1]),   # arrows
            run_time=1.2,
        )

        # ------------------------------------------------------------------ #
        # 6. Narration pause                                                   #
        # ------------------------------------------------------------------ #
        self.wait(2.5)

        # ------------------------------------------------------------------ #
        # 7. Fade out everything                                               #
        # ------------------------------------------------------------------ #
        self.play(
            FadeOut(title_group),
            FadeOut(subtitle),
            FadeOut(divider),
            FadeOut(pipeline),
            FadeOut(pipeline_label),
            FadeOut(fp_img),
            run_time=1.0,
        )
        self.wait(0.3)
