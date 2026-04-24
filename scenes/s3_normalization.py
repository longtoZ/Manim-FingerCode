"""
scenes/s3_normalization.py
--------------------------
Phase 4 — Scene 3: Normalization

Animation flow
--------------
1.  Pipeline bar (Step 3 gold) + step header.
2.  Fingerprint (30 % opacity) + polar grid fades in.
3.  All 32 sector overlays appear with *random* fills, simulating the
    raw uneven local contrast across the AOI (before normalization).
4.  One sector is spotlit — a mini histogram panel on the right shows
    its skewed pixel-intensity distribution ("Before").
5.  Normalization wave: LaggedStart transforms every sector to a uniform
    teal fill; simultaneously the histogram morphs to a Gaussian shape.
6.  "After" label confirms the uniform state.
7.  Normalization formula rendered with MathTex (LaTeX required).
8.  Caption block.
9.  Narration hold (2.5 s).
10. Fade everything out.

Standalone render
-----------------
    manim -pql scenes/s3_normalization.py NormalizationScene
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
    FP_TEXT_PRIMARY,
    FP_TEXT_DIM,
    N_RINGS,
    N_SECTORS,
    INNER_RADIUS,
    ASSET_FP_QUERY,
)
from utils.fingerprint_utils import load_fingerprint, get_core_point
from utils.grid_utils import get_sector_region

# Resolve preferred font
try:
    import manimpango
    _available = {f.lower() for f in manimpango.list_fonts()}
    FP_FONT = "Fira Sans" if "fira sans" in _available else ""
except Exception:
    FP_FONT = ""

# ── shared palette ──────────────────────────────────────────────────────────
BEFORE_DARK   = "#1a1060"   # dark-blue end of the before-spectrum
BEFORE_BRIGHT = "#F5CBA7"   # warm-peach end of the before-spectrum
AFTER_COLOR   = "#00CED1"   # FP_ACCENT_TEAL — uniform post-normalization
HISTOGRAM_BEFORE_COLOR = "#E67E22"   # warm orange bars
HISTOGRAM_AFTER_COLOR  = "#00CED1"   # teal bars

# Pipeline bar helper (same as other scenes)
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


# ── grid helpers (same style as s2) ─────────────────────────────────────────

def _build_grid_vgroups(center, n_rings, n_sectors, inner_r, outer_r,
                        stroke_color, stroke_width=2.5):
    """Return (rings_vg, spokes_vg) separately for display (no animation)."""
    radii  = np.linspace(inner_r, outer_r, n_rings + 1)
    angles = np.linspace(0, TAU, n_sectors, endpoint=False)

    rings_vg = VGroup(*[
        Arc(radius=r, start_angle=0, angle=TAU,
            stroke_color=stroke_color, stroke_width=stroke_width,
            stroke_opacity=1.0).move_arc_center_to(center)
        for r in radii
    ])
    spokes_vg = VGroup(*[
        Line(start=center + inner_r * np.array([np.cos(a), np.sin(a), 0]),
             end  =center + outer_r * np.array([np.cos(a), np.sin(a), 0]),
             stroke_color=stroke_color, stroke_width=stroke_width,
             stroke_opacity=1.0)
        for a in angles
    ])
    return rings_vg, spokes_vg


# ── histogram helpers ────────────────────────────────────────────────────────

def _build_bar_chart(heights, color, bar_w=0.17, gap=0.04,
                     max_h=1.4) -> VGroup:
    """Bar chart as a VGroup of Rectangles, aligned bottom."""
    bars = VGroup()
    for h in heights:
        bar = Rectangle(
            width=bar_w,
            height=max(h * max_h, 0.04),
            fill_color=color,
            fill_opacity=0.85,
            stroke_color=WHITE,
            stroke_width=0.8,
        )
        bars.add(bar)
    bars.arrange(RIGHT, buff=gap, aligned_edge=DOWN)
    return bars


def _build_histogram_panel(title: str, heights, color,
                            panel_w=2.1, panel_h=1.8) -> VGroup:
    """A labelled histogram panel in a rounded box."""
    panel_bg = RoundedRectangle(
        width=panel_w, height=panel_h, corner_radius=0.12,
        fill_color="#12122a", fill_opacity=0.92,
        stroke_color=color, stroke_width=1.5,
    )
    title_txt = Text(title, font=FP_FONT, font_size=16,
                     color=color, weight=BOLD)
    title_txt.move_to(panel_bg.get_top() + DOWN * 0.22)

    bars = _build_bar_chart(heights, color, max_h=0.9)
    bars.move_to(panel_bg.get_center() + DOWN * 0.1)

    x_label = Text("Intensity →", font=FP_FONT, font_size=12,
                   color=FP_TEXT_DIM)
    x_label.next_to(bars, DOWN, buff=0.1)

    return VGroup(panel_bg, title_txt, bars, x_label)


# ── Main scene ───────────────────────────────────────────────────────────────

class NormalizationScene(Scene):
    """Phase 4 — Per-sector Normalization."""

    OUTER_RADIUS: float = 2.1

    # Seeded RNG for reproducible per-sector "before" colors
    _RNG = np.random.default_rng(7)

    def construct(self):
        self.camera.background_color = FP_BG_COLOR

        # ── Layout constants (identical to s1 / s2) ────────────────────── #
        FP_HEIGHT = 4.8
        FP_CENTER = UP * 0.2
        OUTER_R   = self.OUTER_RADIUS

        # Pre-compute core world position
        core_x, core_y = get_core_point(ASSET_FP_QUERY, display_height=FP_HEIGHT)
        core_world = np.array([core_x + FP_CENTER[0],
                                core_y + FP_CENTER[1], 0])

        # ── 1. Pipeline bar (Step 3) + header ─────────────────────────── #
        pipeline = _build_pipeline_bar(active_index=2)
        pipeline.scale(0.82).to_edge(DOWN, buff=0.38)
        self.play(FadeIn(pipeline, shift=UP * 0.1), run_time=0.6)

        step_tag   = Text("Step 3", font=FP_FONT, font_size=14,
                          color=FP_ACCENT_GOLD, weight=BOLD)
        step_title = Text("Normalization", font=FP_FONT, font_size=30,
                          color=FP_TEXT_PRIMARY, weight=BOLD)
        header = VGroup(step_tag, step_title).arrange(RIGHT, buff=0.25)
        header.to_edge(UP, buff=0.35)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.7)

        # ── 2. Fingerprint (dimmed) + grid ────────────────────────────── #
        fp_img = load_fingerprint(ASSET_FP_QUERY, height=FP_HEIGHT)
        fp_img.move_to(FP_CENTER)
        fp_img.set_opacity(0.3)          # pre-dimmed to match end of s2

        core_dot = Dot(point=core_world, radius=0.09,
                       color=FP_ACCENT_GOLD, fill_opacity=1.0)
        core_dot.set_stroke(color=FP_ACCENT_GOLD, width=3, opacity=0.6)

        rings_vg, spokes_vg = _build_grid_vgroups(
            core_world, N_RINGS, N_SECTORS, INNER_RADIUS, OUTER_R,
            stroke_color=FP_ACCENT_TEAL,
        )
        grid_vg = VGroup(rings_vg, spokes_vg)

        self.play(
            FadeIn(fp_img), FadeIn(core_dot), FadeIn(grid_vg),
            run_time=0.9,
        )
        self.wait(0.4)

        # ── 3. "Before" sector overlays — random fills ────────────────── #
        before_label = Text("Before Normalization", font=FP_FONT,
                            font_size=18, color=HISTOGRAM_BEFORE_COLOR,
                            weight=BOLD)
        before_label.to_corner(UR, buff=0.5).shift(DOWN * 0.5)
        self.play(FadeIn(before_label, shift=DOWN * 0.1), run_time=0.4)

        # Generate per-sector random intensities (seeded)
        rng = self.__class__._RNG
        intensities = rng.uniform(0, 1, N_RINGS * N_SECTORS)

        before_sectors = VGroup()
        for idx, (r, s) in enumerate(
            (r, s) for r in range(N_RINGS) for s in range(N_SECTORS)
        ):
            v = float(intensities[idx])
            fill_c = interpolate_color(
                ManimColor(BEFORE_DARK), ManimColor(BEFORE_BRIGHT), v
            )
            cell = get_sector_region(
                center=core_world, ring=r, sector=s,
                n_rings=N_RINGS, n_sectors=N_SECTORS,
                inner_radius=INNER_RADIUS, outer_radius=OUTER_R,
                fill_color=fill_c, fill_opacity=0.6,
                stroke_color=FP_ACCENT_TEAL, stroke_width=0.4,
            )
            before_sectors.add(cell)

        # Fan the sectors in with a short stagger
        self.play(
            LaggedStart(
                *[FadeIn(cell, scale=0.9) for cell in before_sectors],
                lag_ratio=0.04,
            ),
            run_time=1.5,
        )
        self.wait(0.5)

        # ── 4. Spotlit sector + "Before" histogram ────────────────────── #
        # Spotlight ring=1, sector=3 for visual clarity
        SPOT_RING, SPOT_SEC = 1, 3
        spot_outline = get_sector_region(
            center=core_world, ring=SPOT_RING, sector=SPOT_SEC,
            n_rings=N_RINGS, n_sectors=N_SECTORS,
            inner_radius=INNER_RADIUS, outer_radius=OUTER_R,
            fill_color=FP_ACCENT_GOLD, fill_opacity=0.0,
            stroke_color=FP_ACCENT_GOLD, stroke_width=3.0,
        )
        self.play(Create(spot_outline), run_time=0.5)

        # Before-histogram: skewed/bimodal distribution
        h_before = [0.85, 0.70, 0.45, 0.30, 0.20, 0.15, 0.10, 0.08]
        h_after  = [0.10, 0.28, 0.55, 0.80, 0.82, 0.58, 0.30, 0.12]

        hist_before_panel = _build_histogram_panel(
            "Before", h_before, HISTOGRAM_BEFORE_COLOR
        )
        hist_before_panel.to_edge(RIGHT, buff=0.32).shift(UP * 0.4)

        self.play(FadeIn(hist_before_panel, shift=LEFT * 0.15), run_time=0.7)
        self.wait(0.6)

        # ── 5. Normalization wave ─────────────────────────────────────── #
        # Transition the "before" panel to "after"
        hist_after_panel = _build_histogram_panel(
            "After", h_after, HISTOGRAM_AFTER_COLOR
        )
        hist_after_panel.move_to(hist_before_panel)

        after_label = Text("After Normalization", font=FP_FONT,
                           font_size=18, color=AFTER_COLOR, weight=BOLD)
        after_label.move_to(before_label)

        # All sectors → uniform teal fill (LaggedStart ring by ring)
        uniform_sectors = VGroup()
        for idx, (r, s) in enumerate(
            (r, s) for r in range(N_RINGS) for s in range(N_SECTORS)
        ):
            cell = get_sector_region(
                center=core_world, ring=r, sector=s,
                n_rings=N_RINGS, n_sectors=N_SECTORS,
                inner_radius=INNER_RADIUS, outer_radius=OUTER_R,
                fill_color=AFTER_COLOR, fill_opacity=0.45,
                stroke_color=FP_ACCENT_TEAL, stroke_width=0.4,
            )
            uniform_sectors.add(cell)

        self.play(
            LaggedStart(
                *[Transform(before_sectors[i], uniform_sectors[i])
                  for i in range(len(before_sectors))],
                lag_ratio=0.035,
            ),
            Transform(hist_before_panel, hist_after_panel),
            Transform(before_label, after_label),
            run_time=2.0,
        )
        self.wait(0.4)

        # Remove spotlight outline (normalization complete)
        self.play(FadeOut(spot_outline), run_time=0.3)

        # ── 6. Formula ───────────────────────────────────────────────── #
        formula_bg = RoundedRectangle(
            width=5.8, height=1.0, corner_radius=0.15,
            fill_color="#0d0d1a", fill_opacity=0.9,
            stroke_color=FP_ACCENT_TEAL, stroke_width=1.2,
        )

        try:
            formula_tex = MathTex(
                r"G(x,y) \;=\; \mu_0 + \sigma_0 \cdot"
                r"\frac{I(x,y) - \mu}{\sigma}",
                color=FP_TEXT_PRIMARY,
                font_size=36,
            )
        except Exception:
            # LaTeX not available — plain text fallback
            formula_tex = Text(
                "G(x,y) = μ₀ + σ₀ · (I(x,y) − μ) / σ",
                font=FP_FONT, font_size=24, color=FP_TEXT_PRIMARY,
            )

        formula_group = VGroup(formula_bg, formula_tex)
        formula_tex.move_to(formula_bg.get_center())

        # Position: above pipeline, below the grid
        formula_group.next_to(pipeline, UP, buff=0.25)

        # Nudge left so it doesn't overlap the histogram panel
        formula_group.shift(LEFT * 0.8)

        self.play(
            FadeIn(formula_bg),
            FadeIn(formula_tex, shift=UP * 0.1),
            run_time=0.8,
        )

        # ── 7. Caption ─────────────────────────────────────────────────── #
        caption = VGroup(
            Text("Each sector is independently normalized:",
                 font=FP_FONT, font_size=17, color=FP_TEXT_DIM),
            Text("μ₀, σ₀² → uniform mean & variance.",
                 font=FP_FONT, font_size=17, color=FP_TEXT_DIM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        caption.next_to(formula_group, UP, buff=0.2)

        self.play(FadeIn(caption, shift=UP * 0.1), run_time=0.6)

        # ── 8. Narration hold ──────────────────────────────────────────── #
        self.wait(2.5)

        # ── 9. Fade out ────────────────────────────────────────────────── #
        self.play(
            FadeOut(header), FadeOut(pipeline),
            FadeOut(fp_img), FadeOut(core_dot), FadeOut(grid_vg),
            FadeOut(before_sectors),
            FadeOut(hist_before_panel),
            FadeOut(before_label),
            FadeOut(formula_group), FadeOut(caption),
            run_time=1.0,
        )
        self.wait(0.3)
