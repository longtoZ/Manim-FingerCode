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
    method: str = "brightest_valley",
) -> tuple[float, float]:
    """Estimate the core point of a fingerprint and return it as a Manim
    (x, y) coordinate pair.

    The coordinate is computed relative to the image centre so that it can be
    used directly with a Manim scene whose display height was set to
    ``height`` (default 5.0 Manim units).

    Parameters
    ----------
    path:
        File-system path to the fingerprint image.
    method:
        ``"brightest_valley"`` — locate the core as the darkest region near
        the image centre (works well for black-ridge-on-white images).
        ``"centre"`` — simply return (0, 0), the canvas origin (safe fallback).

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
        # Graceful fallback: return the centre of the canvas
        return (0.0, 0.0)

    path = Path(path)
    if not path.exists():
        return (0.0, 0.0)

    img = Image.open(path).convert("L")  # grayscale
    arr = np.array(img, dtype=np.float32)

    # --- Crop to the central 40 % of the image to limit search area ---
    h, w = arr.shape
    r0, r1 = int(h * 0.30), int(h * 0.70)
    c0, c1 = int(w * 0.30), int(w * 0.70)
    patch = arr[r0:r1, c0:c1]

    # Invert: ridges are dark → we want their density peak
    inverted = 255.0 - patch

    # Smooth with a Gaussian to find the density centre
    from scipy.ndimage import gaussian_filter  # scipy is a Manim dep
    smoothed = gaussian_filter(inverted, sigma=min(h, w) * 0.05)
    local_row, local_col = np.unravel_index(np.argmax(smoothed), smoothed.shape)

    # Convert back to full image coordinates
    abs_row = r0 + local_row
    abs_col = c0 + local_col

    # Map pixel coords → Manim world coords
    # Manim places (0,0) at the image centre.
    # We assume the ImageMobject was set to height=5.0.
    display_height = 5.0
    display_width = display_height * (w / h)

    x = (abs_col / w - 0.5) * display_width
    y = -(abs_row / h - 0.5) * display_height  # y-axis is flipped

    return (float(x), float(y))
