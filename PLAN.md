# FingerCode Algorithm — Manim Educational Video: Execution Plan

> **Goal:** Produce a polished, educational Manim animation that walks viewers through every step of the FingerCode fingerprint recognition algorithm — from reference-point detection through final matching.

---

## Project Structure

```
FingerCode Manim/
├── CONCEPT.md
├── PLAN.md            ← this file
├── main.py            ← scene orchestration & final render entry-point
├── assets/
│   ├── fingerprint.png          ← sample grayscale fingerprint image
│   └── fingerprint_template.png ← template fingerprint for matching scene
├── scenes/
│   ├── s0_intro.py
│   ├── s1_reference_point.py
│   ├── s2_tessellation.py
│   ├── s3_normalization.py
│   ├── s4_filtering.py
│   ├── s5_feature_extraction.py
│   └── s6_matching.py
└── utils/
    ├── fingerprint_utils.py  ← image loading, preprocessing helpers
    └── grid_utils.py         ← polar-grid / sector geometry helpers
```

---

## Phase 0 — Project Setup & Asset Preparation

> Lay the groundwork before writing any animation code.

- [x] **0.1** Create the folder structure above (`scenes/`, `utils/`, `assets/`).
- [x] **0.2** Install / verify Manim Community Edition (`pip install manim`) and LaTeX dependencies. *(Manim 0.20.1 installed in `.venv`)*
- [x] **0.3** Source or generate a clean grayscale fingerprint image (`fingerprint.png`) suitable for `ImageMobject`.
- [x] **0.4** Source or generate a second fingerprint image (`fingerprint_template.png`) for the matching scene.
- [x] **0.5** Create `utils/fingerprint_utils.py` with helpers:
  - `load_fingerprint(path)` — returns a Manim `ImageMobject` ready for use.
  - `get_core_point(image)` — returns a `(row, col)` or Manim coordinate tuple for the core.
- [x] **0.6** Create `utils/grid_utils.py` with helpers:
  - `build_polar_grid(center, n_rings, n_sectors)` — returns a `VGroup` of arcs and radial lines.
  - `get_sector_region(ring, sector)` — returns a `Polygon`/`ArcPolygon` for a single cell.
  - `get_all_sectors(...)` — returns a `VGroup` of all cells for bulk styling.
- [x] **0.7** Create a minimal `main.py` that imports and composes all scenes in order.

---

## Phase 1 — Scene 0: Introduction & Title Card

> Establish context and set visual tone before the algorithm begins.

- [x] **1.1** Design a title card with the text `"FingerCode Algorithm"` — "FingerCode" in gold, "Algorithm" in white (`Text`, two-part `VGroup`).
- [x] **1.2** Add a brief subtitle: `"A Texture-Based Fingerprint Recognition Method"` in dim teal-grey.
- [x] **1.3** Fingerprint `ImageMobject` fades in at 12 % opacity as a backdrop; teal divider line drawn with `Create`.
- [x] **1.4** Narration pause of 2.5 s after pipeline bar appears.
- [x] **1.5** All elements `FadeOut` together in 1 s. *(Rendered → `media/videos/s0_intro/480p15/IntroScene.mp4`)*

---

## Phase 2 — Scene 1: Reference Point Detection

> Visualize Step 1 — Locating the core point.

- [x] **2.1** Fingerprint `ImageMobject` (height 4.8 u) centered with a subtle teal border rectangle.
- [x] **2.2** Dual-layer scan line (solid + wide glow) sweeps top → bottom with `linear` rate; `FadeOut` on arrival.
- [x] **2.3** Crosshair `VGroup` (4 arms + 3 concentric rings) `GrowFromPoint` at estimated core; gold `Dot` with `GrowFromCenter`; outer pulse ring expands & fades with `rush_into`.
- [x] **2.4** `"Core Point (Reference)"` label + gold `Arrow` animate in with `FadeIn` / `GrowArrow`.
- [x] **2.5** 3-line caption block fades in above the pipeline bar.
- [x] **2.6** Transient elements fade out in 0.9 s; `HANDOFF_MODE` flag keeps `fp_img` + `core_dot` alive for Scene 2. *(Rendered → `media/videos/s1_reference_point/480p15/ReferencePointScene.mp4`)*

---

## Phase 3 — Scene 2: Tessellation

> Visualize Step 2 — Polar-grid overlay expanding from the core.

- [x] **3.1** Fingerprint + core dot re-created at identical layout constants (FP_HEIGHT=4.8, FP_CENTER=UP×0.2) matching Scene 1.
- [x] **3.2** `_build_rings()` and `_build_spokes()` helpers wrap `Arc`/`Line` geometry; `get_sector_region()` from `grid_utils` used for the highlight cell. `OUTER_RADIUS=2.1` to fit within the image.
- [x] **3.3** Rings grow one-by-one with `LaggedStart(GrowFromCenter, lag_ratio=0.25)`; spokes fan out with `LaggedStart(Create, lag_ratio=0.09)`.
- [x] **3.4** Ring labels (`r0`–`r4`) and sector labels (`s0`–`s7`) rendered via `_build_ring_labels()` / `_build_sector_labels()`; controlled by `SHOW_LABELS` class attribute.
- [x] **3.5** Caption: *"The AOI is divided into 4 rings × 8 sectors = 32 cells, each capturing local ridge texture."*
- [x] **3.6** Ring 1 / Sector 2 highlighted with gold fill pulse + callout arrow; fill fades back out.
- [x] **3.7** 2.5 s narration hold; all elements fade out in 1.0 s. *(Rendered → `media/videos/s2_tessellation/480p15/TessellationScene.mp4`)*

---

## Phase 4 — Scene 3: Normalization

> Visualize Step 3 — Per-sector intensity normalization.

- [ ] **4.1** Retain the tessellated fingerprint image from Scene 2.
- [ ] **4.2** Sequentially (or in groups) highlight each sector using a color-wash overlay (`Rectangle` / `ArcPolygon` with fill opacity animation):
  - Before: random-contrast shading (light/dark variation).
  - After: uniform, standardized shading.
- [ ] **4.3** Show a side-by-side mini histogram or grayscale bar (using `Rectangle` bars as a simple bar chart) for one sector:
  - Left: skewed distribution → Right: normalized distribution.
  - Use `Transform` to morph the bars into the normalized state.
- [ ] **4.4** Add caption: *"Each sector is normalized: μ₀, σ₀² → uniform mean & variance."*
- [ ] **4.5** Display the normalization formula using `MathTex`:
  ```
  G(x, y) = \mu_0 + \sigma_0 \cdot \frac{I(x,y) - \mu}{\sigma}
  ```
- [ ] **4.6** Hold frame, then transition.

---

## Phase 5 — Scene 4: Gabor Filter Bank

> Visualize Step 4 — Multi-directional filtering of the normalized image.

- [ ] **5.1** Show the single normalized polar-grid as the starting state.
- [ ] **5.2** Animate the single grid **cloning** itself into multiple copies (one per filter channel) arranged in a row or 2×N grid layout using `VGroup` + `arrange`.
- [ ] **5.3** Apply distinct visual textures to each copy to represent different filter orientations:
  - Diagonal hatching patterns or wavy sinusoidal overlays drawn with `ParametricFunction`.
  - Vary hue slightly per filter (e.g., blues, purples, teals) to distinguish channels.
- [ ] **5.4** Show a Gabor kernel visualized as a 2D heatmap (optional, small inset):
  - Use a grid of `Square` cells colored by intensity.
  - Animate an `Arrow` sliding the kernel across the image (convolution metaphor).
- [ ] **5.5** Label each filtered grid with its orientation angle (e.g., 0°, 45°, 90°, 135°).
- [ ] **5.6** Add caption: *"A bank of F Gabor filters extracts ridge texture at F orientations."*
- [ ] **5.7** Hold frame, then transition.

---

## Phase 6 — Scene 5: Feature Extraction (FingerCode)

> Visualize Step 5 — Computing A.A.D. and assembling the feature vector.

- [ ] **6.1** Zoom into a single filtered grid to focus on individual sectors.
- [ ] **6.2** Animate each sector morphing / collapsing into a single numerical disc or colored tile:
  - Use `Transform` from `ArcPolygon` → `Circle` (disc) with a number label inside.
  - Discs colored by value magnitude (cool-to-warm colormap using `interpolate_color`).
- [ ] **6.3** Show the A.A.D. formula using `MathTex`:
  ```
  A.A.D._k = \frac{1}{A} \sum_{x,y \in S_k} |I_k(x,y) - \mu_k|
  ```
  where *k* is the sector index.
- [ ] **6.4** Animate all disc tiles assembling into a 1D feature vector bar (flattened into a horizontal sequence of colored rectangles).
- [ ] **6.5** Label the assembled vector `"FingerCode Vector (F × R × S features)"`.
- [ ] **6.6** Add caption contrasting the input (image) with the output (compact vector).
- [ ] **6.7** Hold frame, then transition.

---

## Phase 7 — Scene 6: Matching

> Visualize Step 6 — Euclidean distance comparison and decision.

- [ ] **7.1** Display two FingerCode vectors side-by-side (or stacked):
  - **Top:** Template vector (from database) — labeled `"Template T"`.
  - **Bottom:** Input vector (from query image) — labeled `"Input I"`.
  - Each vector rendered as a row of colored `Rectangle` tiles (reuse Phase 6 style).
- [ ] **7.2** Animate glowing connector lines between corresponding tiles of the two vectors using `Line` + a glow effect (`set_stroke(color=YELLOW, width=…)`).
- [ ] **7.3** Show component differences animating into squared values, then summed (brief schematic).
- [ ] **7.4** Display the Euclidean distance formula using `MathTex`:
  ```
  d(T, I) = \sqrt{\sum_{i=1}^{n} (T_i - I_i)^2}
  ```
- [ ] **7.5** Animate a distance meter / progress bar filling up to the computed value.
- [ ] **7.6** Branch into two outcomes:
  - If `d < threshold` → green checkmark + `"MATCH ✓"` text (use `GrowFromCenter`).
  - If `d ≥ threshold` → red X + `"NO MATCH ✗"` text.
- [ ] **7.7** Hold on the final decision frame, then fade to the outro.

---

## Phase 8 — Scene 7: Summary / Outro

> Recap the full pipeline and close the video.

- [ ] **8.1** Display a pipeline flowchart using `Arrow`-connected `RoundedRectangle` nodes, each labeled with a step name (Steps 1–6).
- [ ] **8.2** Animate each node lighting up in sequence, replaying the key visual from its scene as a small thumbnail insert (optional, advanced).
- [ ] **8.3** Display closing text: `"FingerCode — Texture Meets Topology"` with a subtle fade-in.
- [ ] **8.4** Add credits / source references using small `Text` at the bottom.
- [ ] **8.5** Final `FadeOut` of all elements to black.

---

## Phase 9 — Integration, Polish & Render

> Wire everything together, refine timing, and produce the final output.

- [ ] **9.1** Assemble all scenes in `main.py` using a top-level `Scene` class that calls each subscene in order (or use `play_scene()` helper).
- [ ] **9.2** Add narration-friendly timing pauses (`self.wait()`) at each key moment.
- [ ] **9.3** Apply a consistent color palette and font across all scenes (define global constants at top of `main.py`).
- [ ] **9.4** Add background music placeholder comment (post-production step).
- [ ] **9.5** Perform a **low-quality preview render** of each scene individually:
  ```bash
  manim -pql scenes/s1_reference_point.py ReferencePointScene
  ```
- [ ] **9.6** Review each scene for timing, label readability, and animation smoothness.
- [ ] **9.7** Perform a **full high-quality render** of the complete video:
  ```bash
  manim -pqh main.py FingerCodeVideo
  ```
- [ ] **9.8** Export subtitles / narration script aligned to scene timestamps (optional).
- [ ] **9.9** Final review: check transitions, mathematical formula rendering, and overall pacing.

---

## Notes & Tips

| Concern | Recommendation |
|---|---|
| Fingerprint image rights | Use a synthetic or open-license fingerprint (e.g., FVC2002 sample or generated with `scipy`) |
| Gabor filter visualization | Pre-compute filter response images with `numpy`/`scipy` and load as `ImageMobject` |
| MathTex compilation | Test all `MathTex` strings independently early to catch LaTeX errors |
| Performance | Render each scene file separately (`-pql`) iteratively; only do full render at the end |
| Code reuse | Keep all shared geometry (polar grid, color palette) in `utils/` to avoid duplication |
