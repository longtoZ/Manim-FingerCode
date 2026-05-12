"""
config.py
---------
Shared design constants for all scenes and the main entry point.
"""

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
