"""
fingerprint_utils.py
--------------------
Helper functions for loading and pre-processing fingerprint images inside
Manim scenes.

Usage example (inside a Scene):
    from utils.fingerprint_utils import load_fingerprint, get_core_point

    fp = load_fingerprint("assets/fingerprint.png")
    core_xy = get_core_point("assets/fingerprint.png")
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from manim import ImageMobject, ORIGIN


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def load_fingerprint(path: str | Path, height: float = 5.0) -> ImageMobject:
    """Return a Manim ``ImageMobject`` of the fingerprint ready to place on
    the canvas.

    Parameters
    ----------
    path:
        File-system path to a PNG/JPG fingerprint image.
    height:
        Desired display height in Manim units (default 5.0).

    Returns
    -------
    ImageMobject
        Centered at ORIGIN, scaled to *height* Manim units tall.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Fingerprint image not found: {path.resolve()}")

    mob = ImageMobject(str(path))
    mob.set_height(height)
    mob.move_to(ORIGIN)
    return mob


def get_core_point(
    path: str | Path,
    *,
    method: str = "ridge_centroid",
    display_height: float = 5.0,
) -> tuple[float, float]:
    """Estimate the core point of a fingerprint and return it as a Manim
    (x, y) coordinate pair.

    The coordinate is computed relative to the image centre so that it can be
    used directly with a Manim scene whose display height was set to
    ``display_height``.

    Parameters
    ----------
    path:
        File-system path to the fingerprint image.
    method:
        ``"ridge_centroid"`` *(default)* — compute the weighted centroid of the
        darkest ridge pixels within the central region of the image.  Works well
        for AI-generated and real scanned fingerprints with dark ridges on a
        light background.
        ``"centre"`` — simply return (0, 0), the canvas origin (safe fallback).
    display_height:
        The height in Manim units that the ``ImageMobject`` was given
        (passed to ``set_height()``).  Must match the value used in the scene
        to get pixel-accurate placement.

    Returns
    -------
    tuple[float, float]
        (x, y) in Manim world coordinates.
    """
    if method == "centre":
        return (0.0, 0.0)

    try:
        from PIL import Image  # Pillow is a Manim dependency
    except ImportError:
        return (0.0, 0.0)

    path = Path(path)
    if not path.exists():
        return (0.0, 0.0)

    img = Image.open(path).convert("L")  # grayscale
    arr = np.array(img, dtype=np.float32)
    h, w = arr.shape

    # --- Search within the central 50 % of the image ---
    r0, r1 = int(h * 0.25), int(h * 0.75)
    c0, c1 = int(w * 0.25), int(w * 0.75)
    patch = arr[r0:r1, c0:c1]

    # Ridge pixels are dark (low intensity on a white background).
    # Threshold at the 30th percentile to isolate the darkest ridge pixels.
    thresh = float(np.percentile(patch, 30))
    ridge_rows, ridge_cols = np.where(patch < thresh)

    if len(ridge_rows) == 0:
        # No ridges found — fall back to image centre
        return (0.0, 0.0)

    # Weighted centroid: pixels closer to black get higher weight
    weights = thresh - patch[ridge_rows, ridge_cols]
    abs_row = r0 + float(np.average(ridge_rows, weights=weights))
    abs_col = c0 + float(np.average(ridge_cols, weights=weights))

    # --- Map pixel coords → Manim world coords ---
    # Manim's (0, 0) is the image centre; y-axis points up.
    display_width = display_height * (w / h)
    x = (abs_col / w - 0.5) * display_width
    y = -(abs_row / h - 0.5) * display_height   # pixel y points down

    return (float(x), float(y))

