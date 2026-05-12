"""
scenes/s4_filtering.py
-----------------------
Phase 5 — Scene 4: Gabor Filter Bank

Animation flow
--------------
1.  Pipeline bar (Step 4 gold) + step header.
2.  The single normalised fingerprint + polar grid fades in (end state of s3).
3.  Caption: "We apply a bank of F directional filters to extract texture."
4.  The grid clones itself into 4 smaller copies arranged in a 2×2 layout;
    each copy represents one Gabor filter orientation channel.
5.  Each copy fades in with a unique hue tint AND a sinusoidal wave overlay
    (ParametricFunction) drawn at its filter angle, simulating the filter response.
6.  Orientation angle label (0°, 45°, 90°, 135°) fades in below each copy.
7.  Small Gabor-kernel heatmap inset appears in the top-right corner with a
    sliding-Arrow to illustrate the convolution metaphor.
8.  Caption formula: "F = 4 filters × 32 sectors → 128 features per image"
9.  Narration hold (2.5 s).
10. All elements fade out.

Standalone render
-----------------
    manim -pql scenes/s4_filtering.py FilteringScene
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
    FP_ACCENT_PURPLE,
    FP_TEXT_PRIMARY,
    FP_TEXT_DIM,
    N_RINGS,
    N_SECTORS,
    INNER_RADIUS,
    ASSET_FP_QUERY,
)
from utils.fingerprint_utils import load_fingerprint, get_core_point
from utils.grid_utils import get_all_sectors

# ── Font ────────────────────────────────────────────────────────────────────
try:
    import manimpango
    _available = {f.lower() for f in manimpango.list_fonts()}
    FP_FONT = "Fira Sans" if "fira sans" in _available else ""
except Exception:
    FP_FONT = ""

# ── Pipeline bar ─────────────────────────────────────────────────────────────
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


# ── Filter channel definitions ────────────────────────────────────────────────
# 4 orientation channels with distinct hues and angles
FILTER_CHANNELS = [
    {"angle_deg": 0,   "color": "#00CED1", "label": "0°"},    # teal
    {"angle_deg": 45,  "color": "#9B59B6", "label": "45°"},   # purple
    {"angle_deg": 90,  "color": "#E67E22", "label": "90°"},   # orange
    {"angle_deg": 135, "color": "#2ECC71", "label": "135°"},  # green
]


# ── Helper: mini polar grid card ─────────────────────────────────────────────
def _build_grid_card(
    color: str,
    card_size: float = 2.4,
    angle_deg: float = 0,
    n_rings: int = N_RINGS,
    n_sectors: int = N_SECTORS,
    inner_r: float = INNER_RADIUS,
    bg_color: str = "#0d0d1a",
) -> VGroup:
    """A polar-grid card with wave overlay, BG-colored edge masks, and border.

    Z-order inside the VGroup:
      1. bg_fill      — dark card background (no stroke)
      2. rings/spokes — grid lines (may extend past card edge)
      3. wave         — sinusoidal direction overlay
      4. mask strips  — 4 BG-coloured rectangles covering protrusions
      5. bg_border    — coloured outline on top so it remains visible
    """
    hw = card_size / 2
    outer_r = hw - 0.02          # nearly fills the card
    centre  = ORIGIN

    # ── 1. Background fill (no stroke — border is drawn last) ─────────── #
    bg_fill = RoundedRectangle(
        width=card_size, height=card_size, corner_radius=0.18,
        fill_color=bg_color, fill_opacity=0.92,
        stroke_width=0,
    ).move_to(centre)

    # ── 2. Grid lines ─────────────────────────────────────────────────── #
    radii = np.linspace(inner_r * (outer_r / 2.5), outer_r, n_rings + 1)
    rings = VGroup(*[
        Arc(radius=r, start_angle=0, angle=TAU,
            stroke_color=color, stroke_width=1.2,
            stroke_opacity=0.85).move_arc_center_to(centre)
        for r in radii
    ])

    # Radial spokes
    angles_arr = np.linspace(0, TAU, n_sectors, endpoint=False)
    spokes = VGroup(*[
        Line(
            start=centre + radii[0]  * np.array([np.cos(a), np.sin(a), 0]),
            end  =centre + outer_r   * np.array([np.cos(a), np.sin(a), 0]),
            stroke_color=color, stroke_width=1.2, stroke_opacity=0.85,
        )
        for a in angles_arr
    ])

    # ── 3. Wave overlay ───────────────────────────────────────────────── #
    wave = _build_wave_overlay(angle_deg, color, card_size)

    # ── 4. Mask strips — BG-colored, cover protrusions outside hw ─────── #
    # Keep mask_ext small (just enough to hide grid/wave protrusions);
    # a large value bleeds into neighbouring cards and covers text.
    mask_ext = 0.30
    masks = VGroup(
        # top
        Rectangle(width=card_size + 2 * mask_ext, height=mask_ext,
                  fill_color=bg_color, fill_opacity=1.0,
                  stroke_width=0).move_to(UP   * (hw + mask_ext / 2)),
        # bottom
        Rectangle(width=card_size + 2 * mask_ext, height=mask_ext,
                  fill_color=bg_color, fill_opacity=1.0,
                  stroke_width=0).move_to(DOWN  * (hw + mask_ext / 2)),
        # left
        Rectangle(width=mask_ext, height=card_size + 2 * mask_ext,
                  fill_color=bg_color, fill_opacity=1.0,
                  stroke_width=0).move_to(LEFT  * (hw + mask_ext / 2)),
        # right
        Rectangle(width=mask_ext, height=card_size + 2 * mask_ext,
                  fill_color=bg_color, fill_opacity=1.0,
                  stroke_width=0).move_to(RIGHT * (hw + mask_ext / 2)),
    )

    # ── 5. Border — stroke only, on top of masks ──────────────────────── #
    bg_border = RoundedRectangle(
        width=card_size, height=card_size, corner_radius=0.18,
        fill_opacity=0,
        stroke_color=color, stroke_width=2.0,
    ).move_to(centre)

    return VGroup(bg_fill, rings, spokes, wave, masks, bg_border)


# ── Helper: sinusoidal wave overlay ──────────────────────────────────────────
def _build_wave_overlay(
    angle_deg: float,
    color: str,
    card_size: float = 2.4,
    n_waves: int = 4,
) -> VGroup:
    """Sinusoidal stripes at a given angle, strictly clipped to card_size.

    Only strips whose perp-axis centre lies within ±half of the card are
    rendered — this prevents lines from bleeding into neighbouring cards.
    """
    angle_rad  = np.deg2rad(angle_deg)
    perp_angle = angle_rad + np.pi / 2

    wave_dir = np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
    perp_dir = np.array([np.cos(perp_angle), np.sin(perp_angle), 0])

    # half matches the grid's outer_r so waves also fill edge-to-edge
    half       = card_size / 2 - 0.05
    wavelength = (half * 2) / n_waves      # even spacing across the card
    curves     = VGroup()

    for k in range(-n_waves, n_waves + 1):
        offset = k * wavelength * 0.5      # centre of this strip
        # Skip any strip whose centre falls outside the card boundary
        if abs(offset) > half * 0.98:
            continue

        def make_curve(off=offset):
            def path(t):
                s = t * half
                amp = np.sin(2 * np.pi * off / (wavelength + 1e-8)) * 0.04
                return wave_dir * s + perp_dir * (off + amp)
            return path

        curve = ParametricFunction(
            make_curve(),
            t_range=[-1, 1, 0.05],
            stroke_color=color,
            stroke_width=1.8,
            stroke_opacity=0.50,
        )
        curves.add(curve)

    return curves


# ── Helper: Gabor kernel heatmap ─────────────────────────────────────────────
def _build_gabor_heatmap(
    angle_deg: float = 0,
    size: int = 7,
    sigma: float = 1.2,
    lam: float = 2.5,
    cell_size: float = 0.2,
) -> VGroup:
    """A discrete 2D Gabor kernel rendered as a grid of colored squares."""
    half = size // 2
    cells = VGroup()
    kernel = np.zeros((size, size))

    # Gabor formula (real part)
    for iy in range(size):
        for ix in range(size):
            x = ix - half
            y = iy - half
            a = np.deg2rad(angle_deg)
            xp =  x * np.cos(a) + y * np.sin(a)
            yp = -x * np.sin(a) + y * np.cos(a)
            gauss = np.exp(-(xp**2 + yp**2) / (2 * sigma**2))
            sinusoid = np.cos(2 * np.pi * xp / lam)
            kernel[iy, ix] = gauss * sinusoid

    # Normalize to [-1, 1]
    mx = np.abs(kernel).max() + 1e-8
    kernel /= mx

    for iy in range(size):
        for ix in range(size):
            v = kernel[iy, ix]
            if v >= 0:
                c = interpolate_color(ManimColor("#0d0d1a"), ManimColor("#00CED1"), v)
            else:
                c = interpolate_color(ManimColor("#0d0d1a"), ManimColor("#9B59B6"), -v)
            sq = Square(
                side_length=cell_size,
                fill_color=c, fill_opacity=0.9,
                stroke_color="#333355", stroke_width=0.5,
            )
            sq.move_to(RIGHT * (ix - half) * cell_size
                      + DOWN  * (iy - half) * cell_size)
            cells.add(sq)

    return cells


# ── Main scene ────────────────────────────────────────────────────────────────
class FilteringScene(Scene):
    """Phase 5 — Gabor Filter Bank."""

    OUTER_RADIUS: float = 2.1

    def construct(self):
        self.camera.background_color = FP_BG_COLOR

        FP_HEIGHT = 4.8
        FP_CENTER = UP * 0.2
        OUTER_R   = self.OUTER_RADIUS

        core_x, core_y = get_core_point(ASSET_FP_QUERY, display_height=FP_HEIGHT)
        core_world = np.array([core_x + FP_CENTER[0],
                                core_y + FP_CENTER[1], 0])

        # ── 1. Pipeline + header ───────────────────────────────────────── #
        pipeline = _build_pipeline_bar(active_index=3)
        pipeline.scale(0.82).to_edge(DOWN, buff=0.38)
        self.play(FadeIn(pipeline, shift=UP * 0.1), run_time=0.6)

        step_tag   = Text("Step 4", font=FP_FONT, font_size=14,
                          color=FP_ACCENT_GOLD, weight=BOLD)
        step_title = Text("Gabor Filter Bank", font=FP_FONT, font_size=30,
                          color=FP_TEXT_PRIMARY, weight=BOLD)
        header = VGroup(step_tag, step_title).arrange(RIGHT, buff=0.25)
        header.to_edge(UP, buff=0.35)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.7)

        # ── 2. Normalised fingerprint + grid ───────────────────────────── #
        fp_img = load_fingerprint(ASSET_FP_QUERY, height=FP_HEIGHT)
        fp_img.move_to(FP_CENTER).set_opacity(0.3)

        # Grid (rings + spokes) at teal — same as end of s3
        radii_arr  = np.linspace(INNER_RADIUS, OUTER_R, N_RINGS + 1)
        angles_arr = np.linspace(0, TAU, N_SECTORS, endpoint=False)
        rings_vg = VGroup(*[
            Arc(radius=r, start_angle=0, angle=TAU,
                stroke_color=FP_ACCENT_TEAL, stroke_width=2.5,
                stroke_opacity=1.0).move_arc_center_to(core_world)
            for r in radii_arr
        ])
        spokes_vg = VGroup(*[
            Line(
                start=core_world + INNER_RADIUS * np.array([np.cos(a), np.sin(a), 0]),
                end  =core_world + OUTER_R      * np.array([np.cos(a), np.sin(a), 0]),
                stroke_color=FP_ACCENT_TEAL, stroke_width=2.5, stroke_opacity=1.0,
            )
            for a in angles_arr
        ])
        # Uniform-teal sector overlays (normalised state from s3)
        norm_sectors = get_all_sectors(
            center=core_world, n_rings=N_RINGS, n_sectors=N_SECTORS,
            inner_radius=INNER_RADIUS, outer_radius=OUTER_R,
            fill_color=FP_ACCENT_TEAL, fill_opacity=0.25,
            stroke_color=FP_ACCENT_TEAL, stroke_width=0.4,
        )

        # ImageMobject is not a VMobject → use Group (not VGroup)
        intro_group = Group(fp_img, rings_vg, spokes_vg, norm_sectors)
        self.play(FadeIn(intro_group), run_time=0.9)
        self.wait(0.3)

        # ── 3. Context caption ─────────────────────────────────────────── #
        ctx_caption = Text(
            "The normalized image is passed through a bank of directional filters\n"
            "so we can measure texture along multiple ridge orientations.",
            font=FP_FONT, font_size=17, color=FP_TEXT_DIM,
        )
        ctx_caption.next_to(pipeline, UP, buff=0.25)
        self.play(FadeIn(ctx_caption, shift=UP * 0.1), run_time=0.6)
        self.wait(0.6)

        # ── 4. Clone the grid into 4 filter-channel cards ─────────────── #
        # Slide the original grid to the LEFT to make room for the layout
        self.play(
            FadeOut(ctx_caption),
            FadeOut(intro_group),
            run_time=0.5,
        )

        # Build 4 cards in a 2×2 grid — wave + mask + border all inside each card
        # Card size and buff kept small so the 2×2 block stays compact and
        # doesn't push into the header above or the pipeline bar below.
        CARD_SIZE = 1.55
        cards_vg     = VGroup()
        angle_labels = VGroup()

        for ch in FILTER_CHANNELS:
            card = _build_grid_card(
                ch["color"], card_size=CARD_SIZE,
                angle_deg=ch["angle_deg"],
                n_rings=3, n_sectors=6,
                bg_color=FP_BG_COLOR,
            )
            cards_vg.add(card)

            lbl = Text(ch["label"], font=FP_FONT, font_size=16,
                       color=ch["color"], weight=BOLD)
            angle_labels.add(lbl)

        # Arrange in a tight 2×2 grid; small buff keeps cards close together
        cards_vg.arrange_in_grid(rows=2, cols=2, buff=0.18)
        cards_vg.move_to(ORIGIN + UP * 0.1)

        # Angle labels below each card
        for card, lbl in zip(cards_vg, angle_labels):
            lbl.next_to(card, DOWN, buff=0.15)

        # ── 5. Animate cards in with LaggedStart ───────────────────────── #
        self.play(
            LaggedStart(
                *[FadeIn(card, shift=UP * 0.1) for card in cards_vg],
                lag_ratio=0.3,
            ),
            run_time=2.0,
        )

        # ── 6. Orientation angle labels ────────────────────────────────── #
        self.play(
            LaggedStart(
                *[FadeIn(lbl, shift=UP * 0.08) for lbl in angle_labels],
                lag_ratio=0.2,
            ),
            run_time=0.8,
        )
        self.wait(0.4)

        # ── 7. Gabor kernel heatmap inset ──────────────────────────────── #
        kernel_cells = _build_gabor_heatmap(angle_deg=0, cell_size=0.22)
        kernel_bg = RoundedRectangle(
            width=1.9, height=2.1, corner_radius=0.12,
            fill_color="#0d0d1a", fill_opacity=0.92,
            stroke_color=FP_ACCENT_GOLD, stroke_width=1.5,
        )
        kernel_title = Text("Gabor Kernel", font=FP_FONT, font_size=13,
                            color=FP_ACCENT_GOLD, weight=BOLD)

        kernel_group = VGroup(kernel_bg, kernel_cells)
        kernel_cells.move_to(kernel_bg.get_center())

        kernel_panel = VGroup(kernel_group, kernel_title)
        kernel_title.next_to(kernel_group, UP, buff=0.12)
        kernel_panel.to_corner(UR, buff=0.35).shift(DOWN * 0.6)

        self.play(FadeIn(kernel_panel, shift=LEFT * 0.15), run_time=0.6)

        # Sliding arrow — convolution metaphor
        arrow_start = kernel_panel.get_left() + LEFT * 0.1
        arrow_end   = kernel_panel.get_left() + LEFT * 1.3
        conv_arrow  = Arrow(
            start=arrow_end, end=arrow_start,
            stroke_color=FP_ACCENT_GOLD, stroke_width=2,
            max_tip_length_to_length_ratio=0.25,
            color=FP_ACCENT_GOLD,
        )
        conv_label = Text("Convolution →", font=FP_FONT, font_size=13,
                          color=FP_TEXT_DIM)
        conv_label.next_to(conv_arrow, DOWN, buff=0.1)

        self.play(GrowArrow(conv_arrow), FadeIn(conv_label), run_time=0.5)
        # Slide the arrow left→right to imply kernel sliding across the image
        self.play(
            conv_arrow.animate.shift(RIGHT * 1.2),
            conv_label.animate.shift(RIGHT * 1.2),
            run_time=0.9, rate_func=there_and_back,
        )
        self.wait(0.2)

        # ── 8. Staged captions + definition card ───────────────────────── #
        cap_1 = Text(
            "Ridge texture is strongly oriented, so we analyze it with filters\n"
            "that are selective to direction and spatial frequency.",
            font=FP_FONT, font_size=17, color=FP_TEXT_DIM,
        )
        cap_2 = Text(
            "Each Gabor filter responds to one dominant orientation band, which\n"
            "isolates the ridge flow that aligns with that direction.",
            font=FP_FONT, font_size=17, color=FP_TEXT_DIM,
        )
        cap_3 = Text(
            "Stacking 4 orientations across 32 cells yields a 128-value texture\n"
            "signature that is compact but still descriptive.",
            font=FP_FONT, font_size=17, color=FP_TEXT_DIM,
        )
        cap_1.next_to(pipeline, UP, buff=0.25)
        cap_2.move_to(cap_1)
        cap_3.move_to(cap_1)

        def_text = Text(
            "Gabor filter = an oriented band-pass texture probe",
            font=FP_FONT, font_size=15, color=FP_TEXT_PRIMARY,
        )
        def_bg = RoundedRectangle(
            width=def_text.width + 0.45,
            height=def_text.height + 0.3,
            corner_radius=0.12,
            fill_color="#0d0d1a", fill_opacity=0.92,
            stroke_color=FP_ACCENT_GOLD, stroke_width=1.2,
        )
        def_card = VGroup(def_bg, def_text)
        def_text.move_to(def_bg)
        def_card.to_corner(UR, buff=0.35).shift(DOWN * 0.2)

        self.play(FadeIn(cap_1, shift=UP * 0.1), run_time=0.6)
        self.wait(0.6)
        self.play(Transform(cap_1, cap_2), run_time=0.5)
        self.wait(0.6)
        self.play(Transform(cap_1, cap_3), run_time=0.5)
        self.play(FadeIn(def_card, shift=LEFT * 0.1), run_time=0.6)

        # ── 9. Narration hold ──────────────────────────────────────────── #
        self.wait(2.5)

        # ── 10. Fade out ───────────────────────────────────────────────── #
        self.play(
            FadeOut(header), FadeOut(pipeline), FadeOut(cap_1),
            FadeOut(cards_vg), FadeOut(angle_labels),
            FadeOut(kernel_panel), FadeOut(conv_arrow), FadeOut(conv_label),
            FadeOut(def_card),
            run_time=1.0,
        )
        self.wait(0.3)
