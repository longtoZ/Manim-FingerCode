"""
main.py
-------
FingerCode Algorithm — Manim Educational Video
==============================================

Entry point that composes all scenes into a single, continuous animation.

Render commands
---------------
Low-quality preview (fast):
    manim -pql main.py FingerCodeVideo

High-quality final render:
    manim -pqh main.py FingerCodeVideo

Render a single scene for development (example):
    manim -pql scenes/s1_reference_point.py ReferencePointScene
"""

from manim import *

from config import (
    FP_BG_COLOR,
    FP_ACCENT_GOLD,
    FP_ACCENT_TEAL,
    FP_ACCENT_PURPLE,
    FP_TEXT_PRIMARY,
    FP_TEXT_DIM,
    FP_MATCH_GREEN,
    FP_NOMATCH_RED,
    FP_FONT,
    FP_FONT_MONO,
    N_RINGS,
    N_SECTORS,
    INNER_RADIUS,
    OUTER_RADIUS,
    ASSET_FP_QUERY,
    ASSET_FP_TEMPLATE,
)

# ---------------------------------------------------------------------------
# Global design constants — import these in every scene file for consistency
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# Scene imports  (uncomment each scene as it is implemented)
# ---------------------------------------------------------------------------
from scenes.s0_intro              import IntroScene
from scenes.s0a_overview           import OverviewTextScene
from scenes.s1_reference_point     import ReferencePointScene
from scenes.s2_tessellation        import TessellationScene
from scenes.s2a_polar_grid_text    import PolarGridTextScene
from scenes.s3_normalization       import NormalizationScene
from scenes.s3a_normalization_formula import NormalizationFormulaScene
from scenes.s4_filtering           import FilteringScene
from scenes.s5_feature_extraction  import FeatureExtractionScene
from scenes.s6a_matching_text      import MatchingTextScene
from scenes.s6b_distance_formula   import DistanceFormulaScene
from scenes.s6_matching            import MatchingScene
from scenes.s7_outro               import OutroScene


# ---------------------------------------------------------------------------
# Composite scene — plays all subscenes back-to-back
# ---------------------------------------------------------------------------

class FingerCodeVideo(Scene):
    """Full FingerCode educational video.

    Each subscene is instantiated and its ``construct`` method is called
    within *this* scene's renderer so all frames are written to a single
    output file.

    Development note
    ----------------
    While individual scenes are under development, comment out the lines
    below for scenes that are not yet implemented.  Render the full video
    only in Phase 9.
    """

    def construct(self):
        # Set background colour for the whole video
        self.camera.background_color = FP_BG_COLOR

        # ------------------------------------------------------------------ #
        # Scenes — uncomment each line as the scene is implemented            #
        # ------------------------------------------------------------------ #
        self._play_subscene(IntroScene)
        self._play_subscene(OverviewTextScene)
        self._play_subscene(ReferencePointScene)
        self._play_subscene(TessellationScene)
        self._play_subscene(PolarGridTextScene)
        self._play_subscene(NormalizationScene)
        self._play_subscene(NormalizationFormulaScene)
        self._play_subscene(FilteringScene)
        self._play_subscene(FeatureExtractionScene)
        self._play_subscene(MatchingTextScene)
        self._play_subscene(DistanceFormulaScene)
        self._play_subscene(MatchingScene)
        self._play_subscene(OutroScene)

    # ---------------------------------------------------------------------- #
    # Helper                                                                   #
    # ---------------------------------------------------------------------- #
    def _play_subscene(self, scene_class):
        """Instantiate a subscene class and run its construct() in this
        scene's context so all objects share the same renderer / camera."""
        subscene = scene_class()
        subscene.renderer = self.renderer
        subscene.construct()
        # Clear remaining mobjects before next scene
        self.clear()
        self.wait(0.5)
