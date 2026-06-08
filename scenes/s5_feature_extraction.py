"""
scenes/s5_feature_extraction.py
--------------------------------
Phase 6 — Scene 5: Feature Extraction (FingerCode)

Animation flow
--------------
1.  Pipeline bar (Step 5) + header.
2.  Polar grid over the fingerprint (30 % opacity); sectors colored by seeded
    A.A.D. values (cool-to-warm). LaggedStart reveal.
3.  A.A.D. formula panel (MathTex) fades in top-right.
4.  Sectors collapse → small discs at each sector centroid (Transform).
5.  Fingerprint + grid rings/spokes fade out.
6.  Discs fly from polar positions → 1-D horizontal bar (Transform to rects).
7.  "FingerCode Vector" label + sub-label (F × R × S = 128 features).
8.  Caption.
9.  Hold 2.5 s → fade out.

Standalone render
-----------------
    manim -pql scenes/s5_feature_extraction.py FeatureExtractionScene
"""

from __future__ import annotations
import sys, os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import (
    FP_BG_COLOR, FP_ACCENT_GOLD, FP_ACCENT_TEAL,
    FP_TEXT_PRIMARY, FP_TEXT_DIM,
    N_RINGS, N_SECTORS, INNER_RADIUS, ASSET_FP_QUERY,
)
from utils.fingerprint_utils import load_fingerprint, get_core_point
from utils.grid_utils import get_sector_region

try:
    import manimpango
    _av = {f.lower() for f in manimpango.list_fonts()}
    FP_FONT = "Fira Sans" if "fira sans" in _av else ""
except Exception:
    FP_FONT = ""

# ── Pipeline bar ──────────────────────────────────────────────────────────────
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


# ── Colour helpers ────────────────────────────────────────────────────────────
COOL = "#1a4a7a"   # low A.A.D. → cool blue
WARM = "#E67E22"   # high A.A.D. → warm orange

def _aad_color(v: float):
    return interpolate_color(ManimColor(COOL), ManimColor(WARM), float(v))


# ── Main scene ────────────────────────────────────────────────────────────────
class FeatureExtractionScene(Scene):
    OUTER_RADIUS: float = 2.1

    def construct(self):
        self.camera.background_color = FP_BG_COLOR

        FP_HEIGHT = 4.8
        FP_CENTER = UP * 0.2
        OUTER_R   = self.OUTER_RADIUS

        core_x, core_y = get_core_point(ASSET_FP_QUERY, display_height=FP_HEIGHT)
        core_world = np.array([core_x + FP_CENTER[0],
                                core_y + FP_CENTER[1], 0])

        # Seeded A.A.D. values (one per sector, reproducible)
        rng = np.random.default_rng(99)
        aad_vals = rng.uniform(0.05, 0.95, N_RINGS * N_SECTORS)

        # ── 1. Pipeline + header ──────────────────────────────────────── #
        pipeline = _build_pipeline_bar(active_index=4)
        pipeline.scale(0.82).to_edge(DOWN, buff=0.38)
        self.play(FadeIn(pipeline, shift=UP * 0.1), run_time=0.6)

        step_tag   = Text("Step 5", font=FP_FONT, font_size=14,
                          color=FP_ACCENT_GOLD, weight=BOLD)
        step_title = Text("Feature Extraction", font=FP_FONT, font_size=30,
                          color=FP_TEXT_PRIMARY, weight=BOLD)
        header = VGroup(step_tag, step_title).arrange(RIGHT, buff=0.25)
        header.to_edge(UP, buff=0.35)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.7)

        # ── 2. Fingerprint + grid + colored sectors ───────────────────── #
        fp_img = load_fingerprint(ASSET_FP_QUERY, height=FP_HEIGHT)
        fp_img.move_to(FP_CENTER).set_opacity(0.3)

        radii_arr  = np.linspace(INNER_RADIUS, OUTER_R, N_RINGS + 1)
        angles_arr = np.linspace(0, TAU, N_SECTORS, endpoint=False)

        rings_vg = VGroup(*[
            Arc(radius=r, start_angle=0, angle=TAU,
                stroke_color=FP_ACCENT_TEAL, stroke_width=2.0,
                stroke_opacity=0.8).move_arc_center_to(core_world)
            for r in radii_arr
        ])
        spokes_vg = VGroup(*[
            Line(
                start=core_world + INNER_RADIUS * np.array([np.cos(a), np.sin(a), 0]),
                end  =core_world + OUTER_R      * np.array([np.cos(a), np.sin(a), 0]),
                stroke_color=FP_ACCENT_TEAL, stroke_width=2.0, stroke_opacity=0.8,
            ) for a in angles_arr
        ])

        self.play(FadeIn(fp_img), FadeIn(rings_vg), FadeIn(spokes_vg), run_time=0.8)
        self.wait(0.2)

        # Build 32 colored sectors (A.A.D. magnitude → cool-to-warm)
        colored_sectors = []
        centroids       = []
        sector_angle    = TAU / N_SECTORS
        idx = 0
        for r_i in range(N_RINGS):
            r_mid = (radii_arr[r_i] + radii_arr[r_i + 1]) / 2
            for s_i in range(N_SECTORS):
                a_mid = angles_arr[s_i] + sector_angle / 2
                color = _aad_color(aad_vals[idx])
                sec = get_sector_region(
                    center=core_world, ring=r_i, sector=s_i,
                    n_rings=N_RINGS, n_sectors=N_SECTORS,
                    inner_radius=INNER_RADIUS, outer_radius=OUTER_R,
                    fill_color=color, fill_opacity=0.75,
                    stroke_color=color, stroke_width=0.3,
                )
                colored_sectors.append(sec)
                cent = core_world + r_mid * np.array([np.cos(a_mid), np.sin(a_mid), 0])
                centroids.append(cent)
                idx += 1

        self.play(
            LaggedStart(*[FadeIn(s, scale=0.9) for s in colored_sectors],
                        lag_ratio=0.04),
            run_time=1.4,
        )
        self.wait(0.3)

        # ── 3. A.A.D. formula panel (smaller, positioned in top-left) ── #
        try:
            formula_tex = MathTex(
                r"\text{A.A.D.}_k = \frac{1}{A}"
                r"\sum_{x,y \in S_k} |I_k(x,y) - \mu_k|",
                color=FP_TEXT_PRIMARY, font_size=24,
            )
        except Exception:
            formula_tex = Text("A.A.D.k = (1/A) Σ |I(x,y) − μk|",
                               font=FP_FONT, font_size=18, color=FP_TEXT_PRIMARY)

        formula_bg = RoundedRectangle(
            width=formula_tex.width + 0.4,
            height=formula_tex.height + 0.3,
            corner_radius=0.12,
            fill_color="#0d0d1a", fill_opacity=0.92,
            stroke_color=FP_ACCENT_GOLD, stroke_width=1.0,
        )
        formula_lbl = Text("A.A.D. per sector:", font=FP_FONT,
                           font_size=12, color=FP_ACCENT_GOLD, weight=BOLD)
        formula_panel = VGroup(formula_bg, formula_tex)
        formula_tex.move_to(formula_bg)
        formula_panel = VGroup(formula_lbl, formula_panel).arrange(DOWN, buff=0.08)
        formula_panel.to_corner(UL, buff=0.5).shift(DOWN * 0.2)

        self.play(FadeIn(formula_panel, shift=LEFT * 0.1), run_time=0.7)
        self.wait(0.5)

        # ── 4. Sectors → discs at centroids ──────────────────────────── #
        disc_targets = [
            Circle(radius=0.14, fill_color=_aad_color(aad_vals[i]),
                   fill_opacity=0.95, stroke_width=0).move_to(centroids[i])
            for i in range(len(colored_sectors))
        ]

        self.play(
            LaggedStart(
                *[Transform(sec, disc)
                  for sec, disc in zip(colored_sectors, disc_targets)],
                lag_ratio=0.03,
            ),
            run_time=1.2,
        )
        self.wait(0.2)

        # ── 5. Fade out fingerprint + grid ────────────────────────────── #
        self.play(
            FadeOut(fp_img), FadeOut(rings_vg), FadeOut(spokes_vg),
            FadeOut(formula_panel),
            run_time=0.6,
        )

        # ── 6. Discs fly → 1-D bar ───────────────────────────────────── #
        n_cells  = N_RINGS * N_SECTORS   # 32
        cell_w   = 0.24
        cell_h   = 0.70
        cell_gap = 0.03
        total_w  = n_cells * cell_w + (n_cells - 1) * cell_gap
        bar_y    = 0.0

        bar_targets = []
        for i in range(n_cells):
            x = -total_w / 2 + cell_w / 2 + i * (cell_w + cell_gap)
            rect = Rectangle(
                width=cell_w, height=cell_h,
                fill_color=_aad_color(aad_vals[i]),
                fill_opacity=0.92, stroke_width=0,
            ).move_to([x, bar_y, 0])
            bar_targets.append(rect)

        self.play(
            LaggedStart(
                *[Transform(sec, rect)
                  for sec, rect in zip(colored_sectors, bar_targets)],
                lag_ratio=0.03,
            ),
            run_time=1.5,
        )
        self.wait(0.2)

        # ── 7. Vector labels ──────────────────────────────────────────── #
        vec_label = Text("FingerCode Vector", font=FP_FONT, font_size=22,
                         color=FP_TEXT_PRIMARY, weight=BOLD)
        vec_label.next_to(VGroup(*bar_targets), UP, buff=0.28)

        sub_label = Text(
            f"(F={4} filters × {N_RINGS} rings × {N_SECTORS} sectors"
            f" = {4 * N_RINGS * N_SECTORS} features)",
            font=FP_FONT, font_size=14, color=FP_TEXT_DIM,
        )
        sub_label.next_to(vec_label, DOWN, buff=0.1)

        # Bracket under the bar
        brace = Brace(VGroup(*bar_targets), DOWN, buff=0.1,
                      color=FP_ACCENT_TEAL)
        brace_lbl = Text(f"{n_cells} A.A.D. values  (1 filter)",
                         font=FP_FONT, font_size=13, color=FP_ACCENT_TEAL)
        brace_lbl.next_to(brace, DOWN, buff=0.1)

        self.play(
            FadeIn(vec_label, shift=DOWN * 0.1),
            FadeIn(sub_label, shift=DOWN * 0.1),
            GrowFromCenter(brace),
            FadeIn(brace_lbl),
            run_time=0.8,
        )

        dim_callout = Text("128-D", font=FP_FONT, font_size=14,
                           color=FP_ACCENT_GOLD, weight=BOLD)
        dim_callout.next_to(VGroup(*bar_targets), RIGHT, buff=0.25)
        dim_arrow = Arrow(
            start=dim_callout.get_left(),
            end=VGroup(*bar_targets).get_right(),
            buff=0.08,
            stroke_color=FP_ACCENT_GOLD,
            stroke_width=1.6,
            max_tip_length_to_length_ratio=0.25,
        )
        self.play(FadeIn(dim_callout), GrowArrow(dim_arrow), run_time=0.6)

        # ── 8. Staged captions ────────────────────────────────────────── #
        cap_1 = Text(
            "Within each sector we summarize texture energy as a single A.A.D.\n"
            "value, which captures how much the ridges deviate locally.",
            font=FP_FONT, font_size=17, color=FP_TEXT_DIM,
        )
        cap_2 = Text(
            "We collect these values in a fixed order across rings and sectors\n"
            "so the vector has a consistent, comparable layout.",
            font=FP_FONT, font_size=17, color=FP_TEXT_DIM,
        )
        cap_3 = Text(
            "Concatenating all filter channels produces the full 128-D FingerCode\n"
            "descriptor used for matching.",
            font=FP_FONT, font_size=17, color=FP_TEXT_DIM,
        )
        cap_1.next_to(pipeline, UP, buff=0.25)
        cap_2.move_to(cap_1)
        cap_3.move_to(cap_1)
        self.play(FadeIn(cap_1, shift=UP * 0.1), run_time=0.6)
        self.wait(0.6)
        self.play(Transform(cap_1, cap_2), run_time=0.5)
        self.wait(0.6)
        self.play(Transform(cap_1, cap_3), run_time=0.5)

        # ── 9. Hold ───────────────────────────────────────────────────── #
        self.wait(2.5)

        # ── 10. Fade out ──────────────────────────────────────────────── #
        self.play(
            *[FadeOut(sec) for sec in colored_sectors],
            FadeOut(header), FadeOut(pipeline), FadeOut(cap_1),
            FadeOut(vec_label), FadeOut(sub_label),
            FadeOut(brace), FadeOut(brace_lbl),
            FadeOut(dim_callout), FadeOut(dim_arrow),
            run_time=1.0,
        )
        self.wait(0.3)
