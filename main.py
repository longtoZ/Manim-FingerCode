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

# ---------------------------------------------------------------------------
# Global design constants — import these in every scene file for consistency
# ---------------------------------------------------------------------------

# --- Color palette ----------------------------------------------------------
FP_BG_COLOR      = "#0d0d1a"   # deep navy background
FP_ACCENT_GOLD   = "#FFD700"   # core-point highlight
FP_ACCENT_TEAL   = "#00CED1"   # grid / sector highlights
FP_ACCENT_PURPLE = "#9B59B6"   # filter channel tint
FP_TEXT_PRIMARY  = "#F0F0F0"   # main labels
FP_TEXT_DIM      = "#8899AA"   # secondary / caption text
FP_MATCH_GREEN   = "#2ECC71"   # match outcome
FP_NOMATCH_RED   = "#E74C3C"   # no-match outcome

# --- Typography -------------------------------------------------------------
FP_FONT          = "Fira Sans"   # falls back to default if not installed
FP_FONT_MONO     = "Fira Code"

# --- Grid parameters (used by tessellation, normalization, filtering) -------
N_RINGS   = 4
N_SECTORS = 8
INNER_RADIUS = 0.3
OUTER_RADIUS = 2.5

# --- Asset paths ------------------------------------------------------------
ASSET_FP_QUERY    = "assets/fingerprint.png"
ASSET_FP_TEMPLATE = "assets/fingerprint_template.png"


# ---------------------------------------------------------------------------
# Scene imports  (uncomment each scene as it is implemented)
# ---------------------------------------------------------------------------
from scenes.s0_intro            import IntroScene
from scenes.s1_reference_point  import ReferencePointScene
from scenes.s2_tessellation     import TessellationScene
from scenes.s3_normalization    import NormalizationScene
from scenes.s4_filtering        import FilteringScene
# from scenes.s5_feature_extraction import FeatureExtractionScene
# from scenes.s6_matching         import MatchingScene


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
        self._play_subscene(ReferencePointScene)
        self._play_subscene(TessellationScene)
        self._play_subscene(NormalizationScene)
        self._play_subscene(FilteringScene)
        # self._play_subscene(FeatureExtractionScene)
        # self._play_subscene(MatchingScene)

    # ---------------------------------------------------------------------- #
    # Helper                                                                   #
    # ---------------------------------------------------------------------- #
    def _play_subscene(self, scene_class):
        """Instantiate a subscene class and run its construct() in this
        scene's context so all objects share the same renderer / camera."""
        subscene = scene_class()
        subscene.renderer = self.renderer
        subscene.camera   = self.camera
        subscene.construct()
        # Clear remaining mobjects before next scene
        self.clear()
        self.wait(0.5)
