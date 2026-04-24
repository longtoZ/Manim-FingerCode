"""
grid_utils.py
-------------
Helper functions for constructing the polar (spiderweb) tessellation grid
used throughout the FingerCode animation scenes.

Usage example (inside a Scene):
    from utils.grid_utils import build_polar_grid, get_sector_region

    grid = build_polar_grid(center=ORIGIN, n_rings=4, n_sectors=8)
    self.play(Create(grid))

    sector = get_sector_region(
        center=ORIGIN, ring=1, sector=2,
        n_rings=4, n_sectors=8,
        inner_radius=0.3, outer_radius=2.5,
    )
    self.play(FadeIn(sector))
"""

from __future__ import annotations

import numpy as np
from manim import (
    VGroup,
    Arc,
    Line,
    AnnularSector,
    ORIGIN,
    TAU,
    WHITE,
    np as mnp,
)


# ---------------------------------------------------------------------------
# Constants (override at call-site as needed)
# ---------------------------------------------------------------------------

DEFAULT_INNER_RADIUS: float = 0.3   # radius of the innermost ring (Manim units)
DEFAULT_OUTER_RADIUS: float = 2.5   # radius of the outermost ring
DEFAULT_STROKE_COLOR = WHITE
DEFAULT_STROKE_WIDTH: float = 1.5


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_polar_grid(
    center: np.ndarray = ORIGIN,
    n_rings: int = 4,
    n_sectors: int = 8,
    inner_radius: float = DEFAULT_INNER_RADIUS,
    outer_radius: float = DEFAULT_OUTER_RADIUS,
    stroke_color=DEFAULT_STROKE_COLOR,
    stroke_width: float = DEFAULT_STROKE_WIDTH,
    stroke_opacity: float = 0.85,
) -> VGroup:
    """Build a polar tessellation grid (concentric rings + radial lines).

    Parameters
    ----------
    center:
        Centre of the grid in Manim world coordinates.
    n_rings:
        Number of concentric rings (annuli).
    n_sectors:
        Number of angular sectors per ring.
    inner_radius / outer_radius:
        Inner and outer radii of the full grid (Manim units).
    stroke_color / stroke_width / stroke_opacity:
        Visual styling for all grid lines.

    Returns
    -------
    VGroup
        A flat ``VGroup`` containing all ``Arc`` (rings) and ``Line``
        (radial spokes) objects, ready to animate with ``Create``.
    """
    grid = VGroup()

    # --- Concentric rings ---------------------------------------------------
    radii = np.linspace(inner_radius, outer_radius, n_rings + 1)
    for r in radii:
        ring = Arc(
            radius=r,
            start_angle=0,
            angle=TAU,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            stroke_opacity=stroke_opacity,
        )
        ring.move_arc_center_to(center)
        grid.add(ring)

    # --- Radial spokes ------------------------------------------------------
    angles = np.linspace(0, TAU, n_sectors, endpoint=False)
    for angle in angles:
        start = center + inner_radius * np.array([np.cos(angle), np.sin(angle), 0])
        end   = center + outer_radius * np.array([np.cos(angle), np.sin(angle), 0])
        spoke = Line(
            start=start,
            end=end,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            stroke_opacity=stroke_opacity,
        )
        grid.add(spoke)

    return grid


def get_sector_region(
    center: np.ndarray = ORIGIN,
    ring: int = 0,
    sector: int = 0,
    n_rings: int = 4,
    n_sectors: int = 8,
    inner_radius: float = DEFAULT_INNER_RADIUS,
    outer_radius: float = DEFAULT_OUTER_RADIUS,
    fill_color=None,
    fill_opacity: float = 0.4,
    stroke_color=DEFAULT_STROKE_COLOR,
    stroke_width: float = 1.0,
) -> AnnularSector:
    """Return an ``AnnularSector`` representing a single polar-grid cell.

    Parameters
    ----------
    center:
        Centre of the overall grid (Manim world coordinates).
    ring:
        Zero-based ring index (0 = innermost band).
    sector:
        Zero-based sector index (counted counter-clockwise from the positive
        x-axis).
    n_rings / n_sectors:
        Must match the values used in :func:`build_polar_grid`.
    inner_radius / outer_radius:
        Same radii as the parent grid.
    fill_color / fill_opacity / stroke_color / stroke_width:
        Visual styling for the highlight shape.

    Returns
    -------
    AnnularSector
        A single wedge-ring cell of the polar grid.
    """
    radii = np.linspace(inner_radius, outer_radius, n_rings + 1)
    r_inner = radii[ring]
    r_outer = radii[ring + 1]

    sector_angle = TAU / n_sectors
    start_angle  = sector * sector_angle

    cell = AnnularSector(
        inner_radius=r_inner,
        outer_radius=r_outer,
        angle=sector_angle,
        start_angle=start_angle,
        fill_color=fill_color,
        fill_opacity=fill_opacity,
        stroke_color=stroke_color,
        stroke_width=stroke_width,
    )
    cell.move_arc_center_to(center)
    return cell


def get_all_sectors(
    center: np.ndarray = ORIGIN,
    n_rings: int = 4,
    n_sectors: int = 8,
    inner_radius: float = DEFAULT_INNER_RADIUS,
    outer_radius: float = DEFAULT_OUTER_RADIUS,
    **kwargs,
) -> VGroup:
    """Return a ``VGroup`` of *all* sector cells for convenient bulk styling.

    Sectors are ordered row-major: ring 0 sector 0, ring 0 sector 1, …,
    ring (n_rings-1) sector (n_sectors-1).
    """
    cells = VGroup()
    for r in range(n_rings):
        for s in range(n_sectors):
            cells.add(
                get_sector_region(
                    center=center,
                    ring=r,
                    sector=s,
                    n_rings=n_rings,
                    n_sectors=n_sectors,
                    inner_radius=inner_radius,
                    outer_radius=outer_radius,
                    **kwargs,
                )
            )
    return cells
