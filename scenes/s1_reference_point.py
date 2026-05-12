"""
scenes/s1_reference_point.py
-----------------------------
Phase 2 — Scene 1: Reference Point Detection

Animation flow
--------------
1. Pipeline bar slides in at the bottom (Step 1 highlighted gold).
2. Step header fades in at the top.
3. Fingerprint image fades in at full opacity, centred.
4. A teal horizontal scan line sweeps top-to-bottom suggesting analysis.
5. The scan line dissipates; a crosshair + target rings converge on the core.
6. The core is revealed as a glowing gold Dot with a pulsing ring.
7. An Arrow + label "Core Point (Reference)" animate in.
8. A caption text block explains the step.
9. 2 s narration hold.
10. Non-essential elements (scan artefacts, label, caption) fade out;
    fingerprint image and core dot are left for Scene 2 to pick up.

Standalone render
-----------------
    manim -pql scenes/s1_reference_point.py ReferencePointScene
"""

from __future__ import annotations

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import (
    FP_BG_COLOR,
    FP_ACCENT_GOLD,
    FP_ACCENT_TEAL,
    FP_TEXT_PRIMARY,
    FP_TEXT_DIM,
    FP_NOMATCH_RED,
    ASSET_FP_QUERY,
)
from utils.fingerprint_utils import load_fingerprint, get_core_point

# Resolve preferred font with a safe fallback
try:
    import manimpango
    _available = {f.lower() for f in manimpango.list_fonts()}
    FP_FONT = "Fira Sans" if "fira sans" in _available else ""
except Exception:
    FP_FONT = ""

# Pipeline bar (reused from s0_intro, kept local to avoid cross-import)
STEP_LABELS = [
    "Reference\nPoint", "Tessellation", "Normalization",
    "Filtering", "Feature\nExtraction", "Matching",
]

def _build_pipeline_bar(active_index: int = -1) -> VGroup:
    boxes, arrows = VGroup(), VGroup()
    box_w, box_h, gap = 1.35, 0.65, 0.18
    for i, label in enumerate(STEP_LABELS):
        active = (i == active_index)
        box = RoundedRectangle(
            width=box_w, height=box_h, corner_radius=0.1,
            fill_color=FP_ACCENT_GOLD if active else "#1a1a2e",
            fill_opacity=0.85 if active else 0.6,
            stroke_color=FP_ACCENT_GOLD if active else "#3a3a5c",
            stroke_width=1.5,
        )
        step_num = Text(f"Step {i+1}", font=FP_FONT, font_size=10,
                        color="#0d0d1a" if active else FP_ACCENT_GOLD,
                        weight=BOLD).move_to(box.get_top() + DOWN * 0.15)
        lbl = Text(label, font=FP_FONT, font_size=11,
                   color="#0d0d1a" if active else FP_TEXT_DIM,
                   line_spacing=0.5).move_to(box.get_center() + DOWN * 0.05)
        boxes.add(VGroup(box, step_num, lbl))
    boxes.arrange(RIGHT, buff=gap)
    for i in range(len(STEP_LABELS) - 1):
        arrows.add(Arrow(
            start=boxes[i][0].get_right(), end=boxes[i+1][0].get_left(),
            buff=0.04, max_tip_length_to_length_ratio=0.4,
            stroke_width=1.5, color="#3a3a5c",
        ))
    return VGroup(boxes, arrows)


# ---------------------------------------------------------------------------
# Helper: crosshair + target-ring VGroup
# ---------------------------------------------------------------------------

def _build_crosshair(center: np.ndarray, radii=(0.18, 0.32, 0.48),
                     arm_len: float = 0.55) -> VGroup:
    """Return a VGroup of crosshair lines + concentric target rings centred at
    *center* in Manim world coordinates."""
    group = VGroup()

    # Crosshair arms
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        arm = Line(
            start=center + np.array([dx, dy, 0]) * 0.08,
            end=center   + np.array([dx, dy, 0]) * arm_len,
            stroke_color=FP_ACCENT_GOLD,
            stroke_width=1.8,
            stroke_opacity=0.9,
        )
        group.add(arm)

    # Concentric rings
    for r in radii:
        ring = Circle(
            radius=r,
            stroke_color=FP_ACCENT_GOLD,
            stroke_width=1.5,
            stroke_opacity=0.75,
        ).move_to(center)
        group.add(ring)

    return group


# ---------------------------------------------------------------------------
# Main scene
# ---------------------------------------------------------------------------

class ReferencePointScene(Scene):
    """Phase 2 — Reference Point Detection."""

    # Set to True to leave fp_img + core_dot on screen for Scene 2 handoff
    HANDOFF_MODE: bool = False

    def construct(self):
        self.camera.background_color = FP_BG_COLOR

        # ---------------------------------------------------------- #
        # 0. Layout constants                                          #
        # ---------------------------------------------------------- #
        FP_HEIGHT    = 4.8          # fingerprint display height (Manim units)
        FP_CENTER    = UP * 0.2     # slightly above canvas centre

        # ---------------------------------------------------------- #
        # 1. Pipeline bar (Step 1 highlighted)                         #
        # ---------------------------------------------------------- #
        pipeline = _build_pipeline_bar(active_index=0)
        pipeline.scale(0.82).to_edge(DOWN, buff=0.38)

        self.play(FadeIn(pipeline, shift=UP * 0.1), run_time=0.6)

        # ---------------------------------------------------------- #
        # 2. Step header                                               #
        # ---------------------------------------------------------- #
        step_tag = Text("Step 1", font=FP_FONT, font_size=14,
                        color=FP_ACCENT_GOLD, weight=BOLD)
        step_title = Text("Reference Point Detection", font=FP_FONT,
                          font_size=30, color=FP_TEXT_PRIMARY, weight=BOLD)
        header = VGroup(step_tag, step_title).arrange(RIGHT, buff=0.25)
        header.to_edge(UP, buff=0.35)

        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.7)

        # ---------------------------------------------------------- #
        # 3. Fingerprint image                                         #
        # ---------------------------------------------------------- #
        fp_img = load_fingerprint(ASSET_FP_QUERY, height=FP_HEIGHT)
        fp_img.move_to(FP_CENTER)

        # Subtle border rectangle around the fingerprint
        border = SurroundingRectangle(
            fp_img, buff=0.05,
            stroke_color=FP_ACCENT_TEAL,
            stroke_width=1.0,
            stroke_opacity=0.4,
            fill_opacity=0,
        )

        self.play(FadeIn(fp_img), Create(border), run_time=1.0)
        self.wait(0.4)

        # ---------------------------------------------------------- #
        # 4. Scan line sweeping top → bottom                           #
        # ---------------------------------------------------------- #
        img_top    = fp_img.get_top()[1]
        img_bottom = fp_img.get_bottom()[1]
        img_left   = fp_img.get_left()[0]
        img_right  = fp_img.get_right()[0]

        scan_line = Line(
            start=[img_left  - 0.1, img_top, 0],
            end  =[img_right + 0.1, img_top, 0],
            stroke_color=FP_ACCENT_TEAL,
            stroke_width=2.5,
            stroke_opacity=0.85,
        )
        # Glow duplicate (wider, more transparent)
        scan_glow = Line(
            start=[img_left  - 0.1, img_top, 0],
            end  =[img_right + 0.1, img_top, 0],
            stroke_color=FP_ACCENT_TEAL,
            stroke_width=8,
            stroke_opacity=0.2,
        )
        scan_group = VGroup(scan_glow, scan_line)

        # Animate scan sweep
        scan_target = scan_group.copy().shift(DOWN * (img_top - img_bottom))
        self.play(FadeIn(scan_group), run_time=0.2)
        self.play(
            Transform(scan_group, scan_target),
            run_time=1.6,
            rate_func=linear,
        )
        self.play(FadeOut(scan_group), run_time=0.3)

        # ---------------------------------------------------------- #
        # 5. Crosshair lock-on at the estimated core point             #
        # ---------------------------------------------------------- #
        core_x, core_y = get_core_point(ASSET_FP_QUERY, display_height=FP_HEIGHT)
        # Shift by the scene's FP_CENTER offset so the dot lands on the
        # fingerprint image which itself was moved to FP_CENTER
        core_world = np.array([core_x + FP_CENTER[0], core_y + FP_CENTER[1], 0])

        crosshair = _build_crosshair(core_world)
        crosshair.set_opacity(0)

        # Grow crosshair from the centre of the image outward
        self.play(
            crosshair.animate.set_opacity(1),
            GrowFromPoint(crosshair, point=core_world),
            run_time=0.7,
        )

        # ---------------------------------------------------------- #
        # 6. Glowing core dot                                          #
        # ---------------------------------------------------------- #
        core_dot = Dot(point=core_world, radius=0.09,
                       color=FP_ACCENT_GOLD, fill_opacity=1.0)
        core_dot.set_stroke(color=FP_ACCENT_GOLD, width=3, opacity=0.6)

        # Outer pulse ring — animated with UpdateFromAlphaFunc
        pulse_ring = Circle(radius=0.09, stroke_color=FP_ACCENT_GOLD,
                            stroke_width=2, stroke_opacity=0.8).move_to(core_world)

        self.play(GrowFromCenter(core_dot), run_time=0.5)

        # Pulse animation: ring expands and fades
        self.play(
            pulse_ring.animate.scale(3.5).set_stroke(opacity=0),
            run_time=0.8,
            rate_func=rush_into,
        )
        self.remove(pulse_ring)

        # ---------------------------------------------------------- #
        # 7. Arrow + label                                             #
        # ---------------------------------------------------------- #
        label_text = Text("Core Point  (Reference)",
                          font=FP_FONT, font_size=22,
                          color=FP_ACCENT_GOLD)

        # Place label to the right if space allows, else to the left
        label_side = RIGHT if core_x < 0.5 else LEFT
        label_dir  = RIGHT if core_x < 0.5 else LEFT
        label_text.next_to(core_world, label_side * 3.5 + UP * 0.5, buff=0)

        arrow = Arrow(
            start=label_text.get_left() if core_x < 0.5 else label_text.get_right(),
            end=core_world + RIGHT * 0.12,
            buff=0.05,
            stroke_color=FP_ACCENT_GOLD,
            stroke_width=2.0,
            max_tip_length_to_length_ratio=0.25,
            color=FP_ACCENT_GOLD,
        )

        self.play(
            FadeIn(label_text, shift=UP * 0.1),
            GrowArrow(arrow),
            run_time=0.8,
        )

        # ---------------------------------------------------------- #
        # 8. Caption block                                             #
        # ---------------------------------------------------------- #
        caption_lines = VGroup(
            Text("The algorithm first locates the fingerprint",
                 font=FP_FONT, font_size=18, color=FP_TEXT_DIM),
            Text("core point — the innermost tip of the ridge",
                 font=FP_FONT, font_size=18, color=FP_TEXT_DIM),
            Text("curvature — which anchors all subsequent steps.",
                 font=FP_FONT, font_size=18, color=FP_TEXT_DIM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        caption_lines.next_to(pipeline, UP, buff=0.28)

        self.play(FadeIn(caption_lines, shift=UP * 0.1), run_time=0.7)

        # ---------------------------------------------------------- #
        # 9. Narration hold                                            #
        # ---------------------------------------------------------- #
        self.wait(2.5)

        # ---------------------------------------------------------- #
        # 10. Fade out transient elements; keep fp_img + core_dot      #
        # ---------------------------------------------------------- #
        self.play(
            FadeOut(header),
            FadeOut(pipeline),
            FadeOut(caption_lines),
            FadeOut(label_text),
            FadeOut(arrow),
            FadeOut(crosshair),
            FadeOut(border),
            run_time=0.9,
        )

        if not self.HANDOFF_MODE:
            # Standalone: fade everything out cleanly
            self.play(FadeOut(fp_img), FadeOut(core_dot), run_time=0.6)

        self.wait(0.3)
