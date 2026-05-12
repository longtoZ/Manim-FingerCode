"""
scenes/s6_matching.py
---------------------
Phase 7 — Scene 6: Matching

Animation flow
--------------
1.  Pipeline bar (Step 6 gold) + header.
2.  Two 32-cell FingerCode vectors appear stacked:
      Template T  (top, gold border)
      Input I     (bottom, teal border)
3.  LaggedStart glowing connector lines link corresponding tiles.
4.  Euclidean-distance formula (MathTex) fades in.
5.  Distance meter (progress bar) fills to the computed value.
6.  Decision: d < threshold → green "MATCH ✓" (GrowFromCenter).
7.  Hold 2.5 s → fade out.

Standalone render
-----------------
    manim -pql scenes/s6_matching.py MatchingScene
"""

from __future__ import annotations
import sys, os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import (
    FP_BG_COLOR, FP_ACCENT_GOLD, FP_ACCENT_TEAL,
    FP_TEXT_PRIMARY, FP_TEXT_DIM,
    N_RINGS, N_SECTORS, ASSET_FP_QUERY,
)

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


# ── Colour helper (same cool-to-warm as Phase 6) ─────────────────────────────
def _vec_color(v: float):
    return interpolate_color(ManimColor("#1a4a7a"), ManimColor("#E67E22"), float(v))


# ── Build a 1-D vector bar ────────────────────────────────────────────────────
def _build_vector_bar(
    values,
    bar_y: float,
    cell_w: float = 0.20,
    cell_h: float = 0.60,
    cell_gap: float = 0.025,
) -> VGroup:
    n = len(values)
    total_w = n * cell_w + (n - 1) * cell_gap
    rects = VGroup()
    for i, v in enumerate(values):
        x = -total_w / 2 + cell_w / 2 + i * (cell_w + cell_gap)
        rects.add(
            Rectangle(
                width=cell_w, height=cell_h,
                fill_color=_vec_color(v), fill_opacity=0.92,
                stroke_width=0,
            ).move_to([x, bar_y, 0])
        )
    return rects


# ── Main scene ────────────────────────────────────────────────────────────────
class MatchingScene(Scene):

    THRESHOLD: float = 0.55   # Euclidean distance threshold for MATCH

    def construct(self):
        self.camera.background_color = FP_BG_COLOR

        # Generate template and input vectors
        rng_T = np.random.default_rng(99)
        rng_I = np.random.default_rng(99)    # same seed
        n_feat = N_RINGS * N_SECTORS          # 32
        vals_T = rng_T.uniform(0.05, 0.95, n_feat)
        # Input = Template + small noise → guaranteed MATCH
        noise  = np.random.default_rng(7).uniform(-0.12, 0.12, n_feat)
        vals_I = np.clip(vals_T + noise, 0.0, 1.0)
        dist   = float(np.sqrt(np.sum((vals_T - vals_I) ** 2)))

        # ── 1. Pipeline + header ──────────────────────────────────────── #
        pipeline = _build_pipeline_bar(active_index=5)
        pipeline.scale(0.82).to_edge(DOWN, buff=0.38)
        self.play(FadeIn(pipeline, shift=UP * 0.1), run_time=0.6)

        step_tag   = Text("Step 6", font=FP_FONT, font_size=14,
                          color=FP_ACCENT_GOLD, weight=BOLD)
        step_title = Text("Matching", font=FP_FONT, font_size=30,
                          color=FP_TEXT_PRIMARY, weight=BOLD)
        header = VGroup(step_tag, step_title).arrange(RIGHT, buff=0.25)
        header.to_edge(UP, buff=0.35)
        self.play(FadeIn(header, shift=DOWN * 0.1), run_time=0.7)

        # ── 2. Two FingerCode vector bars ─────────────────────────────── #
        BAR_Y_T = 1.15    # Template (top)
        BAR_Y_I = -0.05   # Input   (bottom)

        bar_T = _build_vector_bar(vals_T, BAR_Y_T)
        bar_I = _build_vector_bar(vals_I, BAR_Y_I)

        # Outer box for each bar
        cell_w, cell_gap = 0.20, 0.025
        total_w = n_feat * cell_w + (n_feat - 1) * cell_gap
        cell_h  = 0.60

        def _bar_box(bar_y, color, label_str):
            box = RoundedRectangle(
                width=total_w + 0.20, height=cell_h + 0.24,
                corner_radius=0.1,
                fill_color="#0d0d1a", fill_opacity=0.0,
                stroke_color=color, stroke_width=1.5,
            ).move_to([0, bar_y, 0])
            lbl = Text(label_str, font=FP_FONT, font_size=16,
                       color=color, weight=BOLD)
            lbl.next_to(box, LEFT, buff=0.2)
            return VGroup(box, lbl)

        box_T = _bar_box(BAR_Y_T, FP_ACCENT_GOLD, "Template  T")
        box_I = _bar_box(BAR_Y_I, FP_ACCENT_TEAL,  "Input     I")

        self.play(
            FadeIn(box_T, shift=RIGHT * 0.1),
            FadeIn(bar_T, shift=RIGHT * 0.1),
            run_time=0.7,
        )
        self.play(
            FadeIn(box_I, shift=RIGHT * 0.1),
            FadeIn(bar_I, shift=RIGHT * 0.1),
            run_time=0.7,
        )
        self.wait(0.3)

        # ── 3. Connector lines (sample 8 evenly spaced tiles) ─────────── #
        sample_indices = list(range(0, n_feat, 4))   # every 4th cell → 8 lines
        connector_lines = VGroup()
        for i in sample_indices:
            top_pt    = bar_T[i].get_bottom()
            bottom_pt = bar_I[i].get_top()
            line = Line(
                start=top_pt, end=bottom_pt,
                stroke_color=FP_ACCENT_GOLD,
                stroke_width=1.8, stroke_opacity=0.7,
            )
            connector_lines.add(line)

        self.play(
            LaggedStart(*[Create(l) for l in connector_lines], lag_ratio=0.12),
            run_time=0.9,
        )
        self.wait(0.2)

        # ── 4. Distance formula ───────────────────────────────────────── #
        try:
            formula_tex = MathTex(
                r"d(T,I) = \sqrt{\,\sum_{i=1}^{n}(T_i - I_i)^2\,}",
                color=FP_TEXT_PRIMARY, font_size=32,
            )
        except Exception:
            formula_tex = Text("d(T,I) = sqrt( Σ (Tᵢ − Iᵢ)² )",
                               font=FP_FONT, font_size=22, color=FP_TEXT_PRIMARY)

        formula_bg = RoundedRectangle(
            width=formula_tex.width + 0.5,
            height=formula_tex.height + 0.4,
            corner_radius=0.12,
            fill_color="#0d0d1a", fill_opacity=0.92,
            stroke_color=FP_ACCENT_GOLD, stroke_width=1.2,
        )
        formula_tex.move_to(formula_bg)
        formula_panel = VGroup(formula_bg, formula_tex)
        formula_panel.next_to(bar_I, DOWN, buff=0.45)
        formula_panel.shift(LEFT * 1.5)

        self.play(FadeIn(formula_panel, shift=UP * 0.1), run_time=0.6)

        # ── 5. Distance meter ─────────────────────────────────────────── #
        meter_w, meter_h = 3.5, 0.30
        max_dist = 1.5    # normalise display; any d > max_dist → full bar

        meter_bg = RoundedRectangle(
            width=meter_w, height=meter_h, corner_radius=0.06,
            fill_color="#1a1a2e", fill_opacity=1.0,
            stroke_color="#3a3a5c", stroke_width=1.0,
        )
        fill_ratio = min(dist / max_dist, 1.0)
        fill_color = (interpolate_color(ManimColor("#2ECC71"), ManimColor("#E74C3C"),
                                        fill_ratio))

        meter_fill = Rectangle(
            width=0.001, height=meter_h - 0.06,
            fill_color=fill_color, fill_opacity=0.95,
            stroke_width=0,
        )
        meter_fill.align_to(meter_bg, LEFT).shift(RIGHT * 0.03)

        meter_lbl = Text("Distance:", font=FP_FONT, font_size=14,
                         color=FP_TEXT_DIM)
        meter_val = Text(f"d = {dist:.3f}", font=FP_FONT, font_size=14,
                         color=fill_color, weight=BOLD)
        thr_lbl   = Text(f"threshold = {self.THRESHOLD:.2f}",
                         font=FP_FONT, font_size=12, color=FP_TEXT_DIM)

        meter_group = VGroup(meter_bg, meter_fill)
        meter_group.next_to(formula_panel, RIGHT, buff=0.45)
        meter_lbl.next_to(meter_group, UP, buff=0.1)
        meter_val.next_to(meter_group, DOWN, buff=0.08)
        thr_lbl.next_to(meter_val, RIGHT, buff=0.25)

        self.play(FadeIn(meter_group), FadeIn(meter_lbl), run_time=0.5)
        # Animate fill expanding via Transform to a pre-built target shape
        target_w = max((meter_w - 0.06) * fill_ratio, 0.04)
        meter_fill_target = Rectangle(
            width=target_w, height=meter_h - 0.06,
            fill_color=fill_color, fill_opacity=0.95,
            stroke_width=0,
        ).align_to(meter_bg, LEFT).shift(RIGHT * 0.03)
        meter_fill_target.move_to(
            [meter_bg.get_left()[0] + target_w / 2 + 0.03,
             meter_bg.get_center()[1], 0]
        )
        self.play(Transform(meter_fill, meter_fill_target),
                  run_time=1.0, rate_func=smooth)
        self.play(FadeIn(meter_val), FadeIn(thr_lbl), run_time=0.4)
        self.wait(0.3)

        # ── 6. Decision ───────────────────────────────────────────────── #
        is_match = dist < self.THRESHOLD

        if is_match:
            decision_color = "#2ECC71"
            decision_text  = "MATCH  ✓"
        else:
            decision_color = "#E74C3C"
            decision_text  = "NO MATCH  ✗"

        decision_bg = RoundedRectangle(
            width=4.0, height=1.0, corner_radius=0.18,
            fill_color=decision_color, fill_opacity=0.15,
            stroke_color=decision_color, stroke_width=2.5,
        )
        decision_lbl = Text(decision_text, font=FP_FONT, font_size=36,
                            color=decision_color, weight=BOLD)
        decision_lbl.move_to(decision_bg)
        decision_panel = VGroup(decision_bg, decision_lbl)
        decision_panel.to_corner(UR, buff=0.4).shift(DOWN * 0.4)

        self.play(GrowFromCenter(decision_panel), run_time=0.7)
        self.wait(0.3)

        # Pulsing glow effect on decision
        self.play(
            decision_bg.animate.set_fill(decision_color, opacity=0.35),
            run_time=0.4, rate_func=there_and_back,
        )

        # ── 7. Caption ────────────────────────────────────────────────── #
        caption = VGroup(
            Text("Euclidean distance between the two 128-D FingerCode vectors.",
                 font=FP_FONT, font_size=16, color=FP_TEXT_DIM),
            Text(f"d < {self.THRESHOLD} → fingerprints match; d ≥ {self.THRESHOLD} → reject.",
                 font=FP_FONT, font_size=16, color=FP_TEXT_DIM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        caption.next_to(pipeline, UP, buff=0.22)
        self.play(FadeIn(caption, shift=UP * 0.1), run_time=0.6)

        # ── 8. Hold ───────────────────────────────────────────────────── #
        self.wait(2.5)

        # ── 9. Fade out ────────────────────────────────────────────────── #
        self.play(
            FadeOut(header), FadeOut(pipeline), FadeOut(caption),
            FadeOut(bar_T), FadeOut(bar_I), FadeOut(box_T), FadeOut(box_I),
            FadeOut(connector_lines), FadeOut(formula_panel),
            FadeOut(meter_group), FadeOut(meter_lbl),
            FadeOut(meter_val), FadeOut(thr_lbl),
            FadeOut(decision_panel),
            run_time=1.0,
        )
        self.wait(0.3)
