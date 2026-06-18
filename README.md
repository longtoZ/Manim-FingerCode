# FingerCode Algorithm -- Manim Educational Video

An animated walkthrough of the FingerCode fingerprint recognition algorithm, rendered with the [Manim Community Edition](https://docs.manim.community) mathematics animation library. The video illustrates the six-stage pipeline that transforms a raw fingerprint image into a compact 128-dimensional feature vector and performs matching using Euclidean distance.

---

## Algorithm Overview

The FingerCode algorithm, introduced by Hong, Wan, and Jain (1998), is a texture-based fingerprint recognition method. Instead of relying exclusively on minutiae points (ridge endings and bifurcations), it analyses local ridge patterns through oriented Gabor filters and encodes the resulting texture information into a fixed-length descriptor that is robust to small distortions and image noise.

```mermaid
flowchart LR
    A["Step 1<br/>Reference Point"] --> B["Step 2<br/>Tessellation"]
    B --> C["Step 3<br/>Normalization"]
    C --> D["Step 4<br/>Gabor Filtering"]
    D --> E["Step 5<br/>Feature Extraction"]
    E --> F["Step 6<br/>Matching"]
```

| Step | Stage                     | Description                                                                                                                |
| ---- | ------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| 1    | Reference Point Detection | Locate the core point where ridge flow curves into a loop, providing a stable spatial anchor.                              |
| 2    | Tessellation              | Partition the area of interest into a polar grid of 4 concentric rings and 8 angular sectors, yielding 32 local cells.     |
| 3    | Normalization             | Standardise pixel intensities within each sector to a common mean and variance, removing lighting bias.                    |
| 4    | Gabor Filtering           | Apply a bank of 4 directional Gabor filters (0, 45, 90, 135 degrees) to measure ridge texture along each orientation.      |
| 5    | Feature Extraction        | Compute the Average Absolute Deviation (A.A.D.) per sector per filter, producing a 128-dimensional FingerCode vector.      |
| 6    | Matching                  | Compare input and template FingerCode vectors using Euclidean distance; a value below a tuned threshold indicates a match. |

The Euclidean distance between a template vector T and an input vector I, each of length n, is defined as:

$$d(T, I) = \sqrt{\sum_{i=1}^{n} (T_i - I_i)^2}$$

---

## Project Structure

```
FingerCode Manim/
├── README.md
├── main.py                     # Entry point; orchestrates all scenes
├── config.py                   # Shared colour palette, fonts, grid constants
├── assets/
├── scenes/
│   ├── s0_intro.py             # Title card and introduction
│   ├── s0a_overview.py         # Text interlude: algorithm overview
│   ├── s1_reference_point.py   # Reference point detection
│   ├── s2_tessellation.py      # Polar grid tessellation
│   ├── s2a_polar_grid_text.py  # Text interlude: polar grid intuition
│   ├── s3_normalization.py     # Per-sector intensity normalisation
│   ├── s3a_normalization_formula.py # Text interlude: normalisation formula
│   ├── s4_filtering.py         # Gabor filter bank
│   ├── s5_feature_extraction.py# Feature extraction and FingerCode assembly
│   ├── s6a_matching_text.py    # Text interlude: matching logic
│   ├── s6b_distance_formula.py # Text interlude: distance equation
│   ├── s6_matching.py          # Visual comparison and match decision
│   ├── s7_outro.py             # Pipeline recap and closing title
│   └── s7b_credits.py          # References and credits
├── utils/
│   ├── fingerprint_utils.py    # Image loading and core-point helpers
│   └── grid_utils.py           # Polar grid and sector geometry
└── media/                      # Output directory (auto-generated)
```

---

## Getting Started

### Prerequisites

- Python 3.10 or later
- [Manim Community Edition](https://docs.manim.community) v0.20 or later
- LaTeX distribution (for mathematical formula rendering; optional but recommended)
- The Fira Sans font (optional; falls back to the system default if absent)

### Installation

```bash
pip install manim
```

### Usage

Render the full video in low quality for preview:

```bash
manim -pql main.py FingerCodeVideo
```

Render the full video in high quality for final output:

```bash
manim -pqh main.py FingerCodeVideo
```

Render a single scene independently (useful during development):

```bash
manim -pql scenes/s0_intro.py IntroScene
```

Replace the filename and class name with the scene of interest.

### Render Quality Flags

| Flag   | Resolution | Frame Rate | Use Case                         |
| ------ | ---------- | ---------- | -------------------------------- |
| `-pql` | 480p       | 15 fps     | Rapid preview during development |
| `-pqh` | 1080p      | 60 fps     | Final production-quality output  |
| `-ql`  | 480p       | 15 fps     | No auto-preview, low quality     |
| `-qh`  | 1080p      | 60 fps     | No auto-preview, high quality    |

---

## Scene Pipeline

Each scene in the `scenes/` directory is a self-contained Manim class that can be rendered independently. All scenes share a common design system defined in `config.py`, including a deep-navy background, a gold accent for highlights, teal for grid elements, and a consistent typographic palette.

The `main.py` entry point composes every sub-scene into a single continuous animation by calling each scene's `construct()` method within a shared renderer.

---

## Customisation

Design constants (colours, grid parameters, font preferences) are centralised in `config.py`:

| Constant         | Default   | Purpose                                      |
| ---------------- | --------- | -------------------------------------------- |
| `N_RINGS`        | 4         | Number of concentric rings in the polar grid |
| `N_SECTORS`      | 8         | Number of angular sectors per ring           |
| `INNER_RADIUS`   | 0.3       | Inner radius of the polar grid (Manim units) |
| `OUTER_RADIUS`   | 2.5       | Outer radius of the polar grid (Manim units) |
| `FP_BG_COLOR`    | `#0d0d1a` | Scene background colour                      |
| `FP_ACCENT_GOLD` | `#FFD700` | Highlight colour for active elements         |
| `FP_ACCENT_TEAL` | `#00CED1` | Grid and sector colour                       |

---

## Attribution

The FingerCode algorithm was introduced in:

> Hong, L., Wan, Y., and Jain, A. (1998). Fingerprint Image Enhancement: Algorithm and Performance Evaluation. _IEEE Transactions on Pattern Analysis and Machine Intelligence_, 20(8), 777--789.

This project is an independent educational visualisation and is not affiliated with the original authors.
