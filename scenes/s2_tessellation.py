"""
scenes/s2_tessellation.py
--------------------------
Phase 3 — Scene 2: Tessellation

Animation flow
--------------
1.  Pipeline bar slides in (Step 2 highlighted gold).
2.  Step header fades in.
3.  Fingerprint image + core dot re-appear (transitioning from Scene 1).
4.  Brief pause — the grid is about to expand.
5.  Innermost ring grows from the core outward (GrowFromCenter).
6.  Each successive ring grows with a short stagger (LaggedStart).
7.  Radial spokes draw outward from inner_radius → outer_radius, fanning
    around with lag_ratio to simulate a spinning-web reveal.
8.  (Optional, SHOW_LABELS=True) Small ring-index and sector-index labels
    fade in around the grid.
9.  One example sector flashes with a gold fill pulse (Indicate-like).
10. Caption block: "AOI divided into R rings × S sectors = R×S cells."
11. Narration hold (2.5 s).
12. All elements fade out.

Standalone render
-----------------
    manim -pql scenes/s2_tessellation.py TessellationScene
"""

from __future__ import annotations

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from main import (
    FP_BG_COLOR,
    FP_ACCENT_GOLD,
    FP_ACCENT_TEAL,
    FP_ACCENT_PURPLE,
    FP_TEXT_PRIMARY,
    FP_TEXT_DIM,
    N_RINGS,
    N_SECTORS,
    INNER_RADIUS,
    ASSET_FP_QUERY,
)
from utils.fingerprint_utils import load_fingerprint, get_core_point
from utils.grid_utils import get_sector_region

# Resolve preferred font with a safe fallback
try:
    import manimpango
    _available = {f.lower() for f in manimpango.list_fonts()}
    FP_FONT = "Fira Sans" if "fira sans" in _available else ""
except Exception:
    FP_FONT = ""

# Pipeline bar helper (kept local — same as other scenes)
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
            start=boxes[i][0].get_right(), end=boxes[i + 1][0].get_left(),
            buff=0.04, max_tip_length_to_length_ratio=0.4,
            stroke_width=1.5, color="#3a3a5c",
        ))
    return VGroup(boxes, arrows)


# ---------------------------------------------------------------------------
# Grid-building helpers (keep rings + spokes as separate VGroups for
# fine-grained animation control)
# ---------------------------------------------------------------------------

def _build_rings(
    center: np.ndarray,
    n_rings: int,
    inner_radius: float,
    outer_radius: float,
    stroke_color,
    stroke_width: float = 2.5,
) -> VGroup:
    """Return a VGroup of Arc objects (one per ring boundary)."""
    radii = np.linspace(inner_radius, outer_radius, n_rings + 1)
    rings = VGroup()
    for r in radii:
        arc = Arc(
            radius=r, start_angle=0, angle=TAU,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            stroke_opacity=1.0,
        )
        arc.move_arc_center_to(center)
        rings.add(arc)
    return rings


def _build_spokes(
    center: np.ndarray,
    n_sectors: int,
    inner_radius: float,
    outer_radius: float,
    stroke_color,
    stroke_width: float = 2.5,
) -> VGroup:
    """Return a VGroup of Line objects (one radial spoke per sector boundary).
    Each Line runs from inner_radius to outer_radius so Create() draws
    outward from the core region.
    """
    angles = np.linspace(0, TAU, n_sectors, endpoint=False)
    spokes = VGroup()
    for angle in angles:
        direction = np.array([np.cos(angle), np.sin(angle), 0])
        spoke = Line(
            start=center + inner_radius * direction,
            end=center   + outer_radius * direction,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            stroke_opacity=1.0,
        )
        spokes.add(spoke)
    return spokes


def _build_ring_labels(
    center: np.ndarray,
    n_rings: int,
    inner_radius: float,
    outer_radius: float,
    font: str = "",
) -> VGroup:
    """Small ring-index labels placed to the right of each ring arc."""
    radii = np.linspace(inner_radius, outer_radius, n_rings + 1)
    labels = VGroup()
    for i, r in enumerate(radii):
        lbl = Text(f"r{i}", font=font, font_size=13, color=WHITE, weight=BOLD)
        lbl.move_to(center + RIGHT * (r + 0.18))
        labels.add(lbl)
    return labels


def _build_sector_labels(
    center: np.ndarray,
    n_sectors: int,
    outer_radius: float,
    font: str = "",
) -> VGroup:
    """Small sector-index labels just outside the outermost ring."""
    angles = np.linspace(0, TAU, n_sectors, endpoint=False)
    labels = VGroup()
    for i, angle in enumerate(angles):
        mid_angle = angle + (TAU / n_sectors) / 2
        direction = np.array([np.cos(mid_angle), np.sin(mid_angle), 0])
        lbl = Text(f"s{i}", font=font, font_size=13, color=FP_ACCENT_TEAL, weight=BOLD)
        lbl.move_to(center + (outer_radius + 0.22) * direction)
        labels.add(lbl)
    return labels


# ---------------------------------------------------------------------------
# Main scene
# ---------------------------------------------------------------------------

class TessellationScene(Scene):
    """Phase 3 — Tessellation: polar grid expanding from the core."""

    # Toggle sector/ring index labels around the grid
    SHOW_LABELS: bool = True

    # Grid geometry (overrides global constants for this scene)
    OUTER_RADIUS: float = 2.1     # slightly inside the fingerprint boundary

    def construct(self):
        self.camera.background_color = FP_BG_COLOR

        # ------------------------------------------------------------------ #
        # 0. Layout constants (must match s1_reference_point.py)              #
        # ------------------------------------------------------------------ #
        FP_HEIGHT  = 4.8
        FP_CENTER  = UP * 0.2
        GRID_COLOR = FP_ACCENT_TEAL

        # ------------------------------------------------------------------ #
        # 1. Pipeline bar — Step 2 highlighted                                #
        # ------------------------------------------------------------------ #
        pipeline = _build_pipeline_bar(active_index=1)
        pipeline.scale(0.82).to_edge(DOWN, buff=0.38)
        self.play(FadeIn(pipeline, shift=UP * 0.1), run_time=0.6)

        # ------------------------------------------------------------------ #
        # 2. Step header                                                       #
        # ------------------------------------------------------------------ #
        step_tag   = Text("Step 2", font=FP_FONT, font_size=14,
                          color=FP_ACCENT_GOLD, weight=BOLD)
        step_title = Text("Tessellation", font=FP_FONT, font_size=30,
                          color=FP_TEXT_PRIMARY, weight=BOLD)
        header = VGroup(step_tag, step_title).arrange(RIGHT, buff=0.25)
        header.to_edge(UP, buff=0.35)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.7)

        # ------------------------------------------------------------------ #
        # 3. Fingerprint image + core dot (re-establish from Scene 1)         #
        # ------------------------------------------------------------------ #
        fp_img = load_fingerprint(ASSET_FP_QUERY, height=FP_HEIGHT)
        fp_img.move_to(FP_CENTER)

        core_x, core_y = get_core_point(ASSET_FP_QUERY, display_height=FP_HEIGHT)
        core_world = np.array([core_x + FP_CENTER[0],
                                core_y + FP_CENTER[1], 0])

        core_dot = Dot(point=core_world, radius=0.09,
                       color=FP_ACCENT_GOLD, fill_opacity=1.0)
        core_dot.set_stroke(color=FP_ACCENT_GOLD, width=3, opacity=0.6)

        self.play(FadeIn(fp_img), FadeIn(core_dot), run_time=0.8)
        self.wait(0.3)

        # Dim the fingerprint so teal grid lines and labels are legible
        # against the white background
        self.play(fp_img.animate.set_opacity(0.3), run_time=0.6)
        self.wait(0.1)

        # ------------------------------------------------------------------ #
        # 4. Build rings + spokes as separate VGroups                         #
        # ------------------------------------------------------------------ #
        rings_vg = _build_rings(
            center=core_world, n_rings=N_RINGS,
            inner_radius=INNER_RADIUS, outer_radius=self.OUTER_RADIUS,
            stroke_color=GRID_COLOR,
        )
        spokes_vg = _build_spokes(
            center=core_world, n_sectors=N_SECTORS,
            inner_radius=INNER_RADIUS, outer_radius=self.OUTER_RADIUS,
            stroke_color=GRID_COLOR,
        )

        # ------------------------------------------------------------------ #
        # 5. Animate rings expanding outward from the core                    #
        # ------------------------------------------------------------------ #
        # Flash a small "about to expand" indicator on the core dot
        flash_ring = Circle(
            radius=0.12,
            stroke_color=FP_ACCENT_GOLD,
            stroke_width=2,
            stroke_opacity=0.9,
        ).move_to(core_world)
        self.play(
            flash_ring.animate.scale(5).set_stroke(opacity=0),
            run_time=0.5,
            rate_func=rush_into,
        )
        self.remove(flash_ring)

        # Rings grow one-by-one from innermost to outermost
        self.play(
            LaggedStart(
                *[GrowFromCenter(ring) for ring in rings_vg],
                lag_ratio=0.25,
            ),
            run_time=1.4,
        )

        # ------------------------------------------------------------------ #
        # 6. Animate spokes fanning out (drawn outward from inner_radius)     #
        # ------------------------------------------------------------------ #
        self.play(
            LaggedStart(
                *[Create(spoke) for spoke in spokes_vg],
                lag_ratio=0.09,
            ),
            run_time=1.2,
        )
        self.wait(0.3)

        # ------------------------------------------------------------------ #
        # 7. Optional index labels                                             #
        # ------------------------------------------------------------------ #
        labels_vg = VGroup()
        if self.SHOW_LABELS:
            ring_labels   = _build_ring_labels(
                core_world, N_RINGS, INNER_RADIUS, self.OUTER_RADIUS, FP_FONT)
            sector_labels = _build_sector_labels(
                core_world, N_SECTORS, self.OUTER_RADIUS, FP_FONT)
            labels_vg = VGroup(ring_labels, sector_labels)
            self.play(FadeIn(labels_vg), run_time=0.6)

        # ------------------------------------------------------------------ #
        # 8. Highlight one example sector                                     #
        # ------------------------------------------------------------------ #
        # Pick ring 1 (second band), sector 2 (roughly upper-right area)
        highlight_sector = get_sector_region(
            center=core_world,
            ring=1,
            sector=2,
            n_rings=N_RINGS,
            n_sectors=N_SECTORS,
            inner_radius=INNER_RADIUS,
            outer_radius=self.OUTER_RADIUS,
            fill_color=FP_ACCENT_GOLD,
            fill_opacity=0.0,
            stroke_color=FP_ACCENT_GOLD,
            stroke_width=2.0,
        )

        # Sector flash: fade in fill → hold → fade out fill
        self.play(
            highlight_sector.animate.set_fill(FP_ACCENT_GOLD, opacity=0.45),
            run_time=0.4,
        )
        # Sector label callout
        sector_callout = Text(
            "One sector (ring 1, sector 2)",
            font=FP_FONT, font_size=17, color=FP_ACCENT_GOLD,
        )
        sector_mid_angle = 2 * (TAU / N_SECTORS) + (TAU / N_SECTORS) / 2
        radii_arr = np.linspace(INNER_RADIUS, self.OUTER_RADIUS, N_RINGS + 1)
        mid_r = (radii_arr[1] + radii_arr[2]) / 2
        direction = np.array([np.cos(sector_mid_angle), np.sin(sector_mid_angle), 0])
        label_pos = core_world + (mid_r + 0.9) * direction

        # Keep label within canvas bounds by clamping x
        label_pos[0] = np.clip(label_pos[0], -5.5, 5.5)
        label_pos[1] = np.clip(label_pos[1], -3.2, 3.2)

        callout_arrow = Arrow(
            start=label_pos,
            end=core_world + mid_r * direction,
            buff=0.12,
            stroke_color=FP_ACCENT_GOLD,
            stroke_width=1.8,
            max_tip_length_to_length_ratio=0.25,
            color=FP_ACCENT_GOLD,
        )
        sector_callout.next_to(label_pos, UP, buff=0.08)

        self.play(
            FadeIn(sector_callout),
            GrowArrow(callout_arrow),
            run_time=0.6,
        )
        self.wait(0.8)
        self.play(
            FadeOut(sector_callout),
            FadeOut(callout_arrow),
            highlight_sector.animate.set_fill(opacity=0.0),
            run_time=0.5,
        )

        # ------------------------------------------------------------------ #
        # 9. Caption block                                                     #
        # ------------------------------------------------------------------ #
        r_val = N_RINGS
        s_val = N_SECTORS
        total = r_val * s_val

        caption = VGroup(
            Text(
                f"The AOI is divided into {r_val} rings × {s_val} sectors",
                font=FP_FONT, font_size=19, color=FP_TEXT_DIM,
            ),
            Text(
                f"= {total} cells, each capturing local ridge texture.",
                font=FP_FONT, font_size=19, color=FP_TEXT_DIM,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        caption.next_to(pipeline, UP, buff=0.28)

        self.play(FadeIn(caption, shift=UP * 0.1), run_time=0.7)

        # ------------------------------------------------------------------ #
        # 10. Narration hold                                                   #
        # ------------------------------------------------------------------ #
        self.wait(2.5)

        # ------------------------------------------------------------------ #
        # 11. Fade everything out                                              #
        # ------------------------------------------------------------------ #
        fade_targets = [
            header, pipeline, caption,
            rings_vg, spokes_vg,
            highlight_sector, fp_img, core_dot,
        ]
        if self.SHOW_LABELS:
            fade_targets.append(labels_vg)

        self.play(
            *[FadeOut(mob) for mob in fade_targets],
            run_time=1.0,
        )
        self.wait(0.3)
