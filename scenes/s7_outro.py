"""
scenes/s7_outro.py
------------------
Phase 8 — Scene 7: Summary / Outro

Animation flow
--------------
1.  A horizontal pipeline flowchart (6 RoundedRectangle nodes + Arrow
    connectors) fades in at the centre of a dark canvas.
2.  Each node pulses gold in sequence (LaggedStart), replaying its role
    in a small icon label beneath.
3.  The closing title "FingerCode — Texture Meets Topology" rises in.
4.  Sub-title and credits text appear.
5.  A final FadeOut darkens everything to the background colour.

Standalone render
-----------------
    manim -pql scenes/s7_outro.py OutroScene
"""

from __future__ import annotations
import sys, os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import (
    FP_BG_COLOR, FP_ACCENT_GOLD, FP_ACCENT_TEAL,
    FP_TEXT_PRIMARY, FP_TEXT_DIM,
)

try:
    import manimpango
    _av = {f.lower() for f in manimpango.list_fonts()}
    FP_FONT = "Fira Sans" if "fira sans" in _av else ""
except Exception:
    FP_FONT = ""

# ── Step metadata ─────────────────────────────────────────────────────────────
STEPS = [
    {"num": 1, "title": "Reference\nPoint",   "icon": "⊕"},
    {"num": 2, "title": "Tessellation",        "icon": "⬡"},
    {"num": 3, "title": "Normalization",       "icon": "≋"},
    {"num": 4, "title": "Gabor\nFiltering",    "icon": "≈"},
    {"num": 5, "title": "Feature\nExtraction", "icon": "▦"},
    {"num": 6, "title": "Matching",            "icon": "✓"},
]

# ── Helper: build one pipeline node ──────────────────────────────────────────
def _make_node(step: dict, active: bool = False, node_w=1.55, node_h=0.85) -> VGroup:
    box = RoundedRectangle(
        width=node_w, height=node_h, corner_radius=0.12,
        fill_color=FP_ACCENT_GOLD if active else "#1a1a2e",
        fill_opacity=0.85 if active else 0.55,
        stroke_color=FP_ACCENT_GOLD if active else "#3a3a5c",
        stroke_width=2.0 if active else 1.2,
    )
    num_txt = Text(f"Step {step['num']}", font=FP_FONT, font_size=10,
                   color="#0d0d1a" if active else FP_ACCENT_GOLD,
                   weight=BOLD).move_to(box.get_top() + DOWN * 0.14)
    title_txt = Text(step["title"], font=FP_FONT, font_size=12,
                     color="#0d0d1a" if active else FP_TEXT_DIM,
                     line_spacing=0.45).move_to(box.get_center() + DOWN * 0.06)
    return VGroup(box, num_txt, title_txt)


# ── Main scene ────────────────────────────────────────────────────────────────
class OutroScene(Scene):

    def construct(self):
        self.camera.background_color = FP_BG_COLOR

        # ── 1. Build pipeline flowchart ───────────────────────────────── #
        NODE_W, NODE_H, GAP = 1.55, 0.85, 0.22

        nodes_vg   = VGroup()
        arrows_vg  = VGroup()

        for step in STEPS:
            nodes_vg.add(_make_node(step, active=False))

        nodes_vg.arrange(RIGHT, buff=GAP)
        nodes_vg.move_to(UP * 0.5)   # centre-upper area

        for i in range(len(STEPS) - 1):
            arrows_vg.add(Arrow(
                start=nodes_vg[i][0].get_right(),
                end  =nodes_vg[i + 1][0].get_left(),
                buff=0.04, max_tip_length_to_length_ratio=0.35,
                stroke_width=1.8, color="#4a4a7a",
            ))

        self.play(
            LaggedStart(
                *[FadeIn(n, shift=UP * 0.12) for n in nodes_vg],
                lag_ratio=0.12,
            ),
            run_time=1.4,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows_vg], lag_ratio=0.12),
            run_time=0.9,
        )
        self.wait(0.3)

        # ── 2. Pulse each node gold in sequence ───────────────────────── #
        recap_lines = [
            "1. Find the core reference point.",
            "2. Partition into polar sectors.",
            "3. Normalize local contrast.",
            "4. Filter oriented ridge texture.",
            "5. Assemble the FingerCode vector.",
            "6. Compare vectors to decide a match.",
        ]
        recap_text = Text(recap_lines[0], font=FP_FONT,
                          font_size=16, color=FP_TEXT_DIM)
        recap_text.to_edge(DOWN, buff=0.55)
        self.play(FadeIn(recap_text, shift=UP * 0.1), run_time=0.5)

        for i, (step, node) in enumerate(zip(STEPS, nodes_vg)):
            active_node = _make_node(step, active=True)
            active_node.move_to(node.get_center())
            self.play(Transform(node, active_node), run_time=0.25)
            if i < len(recap_lines) - 1:
                next_text = Text(recap_lines[i + 1], font=FP_FONT,
                                 font_size=16, color=FP_TEXT_DIM)
                next_text.move_to(recap_text)
                self.play(Transform(recap_text, next_text), run_time=0.35)
            self.wait(0.2)

        self.wait(0.4)

        # ── 3. Closing title ──────────────────────────────────────────── #
        title_line1 = Text(
            "FingerCode",
            font=FP_FONT, font_size=52,
            color=FP_ACCENT_GOLD, weight=BOLD,
        )
        title_line2 = Text(
            "Texture Meets Topology",
            font=FP_FONT, font_size=26,
            color=FP_ACCENT_TEAL,
        )
        separator = Line(
            start=LEFT * 2.8, end=RIGHT * 2.8,
            stroke_color=FP_ACCENT_GOLD, stroke_width=1.2, stroke_opacity=0.5,
        )
        title_block = VGroup(title_line1, separator, title_line2).arrange(
            DOWN, buff=0.22, aligned_edge=ORIGIN
        )
        title_block.move_to(DOWN * 0.85)

        self.play(
            FadeIn(title_line1, shift=UP * 0.2),
            run_time=0.9,
        )
        self.play(
            GrowFromCenter(separator),
            FadeIn(title_line2, shift=UP * 0.15),
            run_time=0.7,
        )
        self.wait(0.4)

        # ── 4. Sub-title + credits ────────────────────────────────────── #
        sub = Text(
            "A Manim-animated walkthrough of Hong, Wan & Jain (1998)",
            font=FP_FONT, font_size=15, color=FP_TEXT_DIM,
        )
        credit_lines = VGroup(
            Text("Reference: Hong, L., Wan, Y., & Jain, A. (1998).",
                 font=FP_FONT, font_size=12, color=FP_TEXT_DIM),
            Text("Fingerprint Image Enhancement: Algorithm and Performance Evaluation.",
                 font=FP_FONT, font_size=12, color=FP_TEXT_DIM),
            Text("IEEE Trans. PAMI, 20(8), 777–789.",
                 font=FP_FONT, font_size=12, color=FP_TEXT_DIM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.06)

        sub.next_to(title_block, DOWN, buff=0.35)
        credit_lines.to_edge(DOWN, buff=0.32)

        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(credit_lines, shift=UP * 0.1), run_time=0.6)

        # ── 5. Narration hold ─────────────────────────────────────────── #
        self.wait(3.0)

        # ── 6. Final fade to black ────────────────────────────────────── #
        self.play(
            FadeOut(nodes_vg), FadeOut(arrows_vg),
            FadeOut(title_block), FadeOut(sub), FadeOut(credit_lines),
            FadeOut(recap_text),
            run_time=1.5,
        )
        self.wait(0.5)
