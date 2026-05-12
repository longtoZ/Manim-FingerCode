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
- [x] **0.2** Install / verify Manim Community Edition (`pip install manim`) and LaTeX dependencies. _(Manim 0.20.1 installed in `.venv`)_
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
- [x] **1.5** All elements `FadeOut` together in 1 s. _(Rendered → `media/videos/s0_intro/480p15/IntroScene.mp4`)_
- [ ] **1.6** Add staged intro captions (2-3 short lines) to introduce the pipeline goals.
- [ ] **1.7** Add a brief definition card: "FingerCode = texture features from polar sectors".

---

## Phase 2 — Scene 1: Reference Point Detection

> Visualize Step 1 — Locating the core point.

- [x] **2.1** Fingerprint `ImageMobject` (height 4.8 u) centered with a subtle teal border rectangle.
- [x] **2.2** Dual-layer scan line (solid + wide glow) sweeps top → bottom with `linear` rate; `FadeOut` on arrival.
- [x] **2.3** Crosshair `VGroup` (4 arms + 3 concentric rings) `GrowFromPoint` at estimated core; gold `Dot` with `GrowFromCenter`; outer pulse ring expands & fades with `rush_into`.
- [x] **2.4** `"Core Point (Reference)"` label + gold `Arrow` animate in with `FadeIn` / `GrowArrow`.
- [x] **2.5** 3-line caption block fades in above the pipeline bar.
- [x] **2.6** Transient elements fade out in 0.9 s; `HANDOFF_MODE` flag keeps `fp_img` + `core_dot` alive for Scene 2. _(Rendered → `media/videos/s1_reference_point/480p15/ReferencePointScene.mp4`)_
- [ ] **2.7** Split the caption into 2-3 sequential beats to extend explanation (fade between lines).
- [ ] **2.8** Add a short definition card: "Core point anchors rotation and alignment".

---

## Phase 3 — Scene 2: Tessellation

> Visualize Step 2 — Polar-grid overlay expanding from the core.

- [x] **3.1** Fingerprint + core dot re-created at identical layout constants (FP_HEIGHT=4.8, FP_CENTER=UP×0.2) matching Scene 1.
- [x] **3.2** `_build_rings()` and `_build_spokes()` helpers wrap `Arc`/`Line` geometry; `get_sector_region()` from `grid_utils` used for the highlight cell. `OUTER_RADIUS=2.1` to fit within the image.
- [x] **3.3** Rings grow one-by-one with `LaggedStart(GrowFromCenter, lag_ratio=0.25)`; spokes fan out with `LaggedStart(Create, lag_ratio=0.09)`.
- [x] **3.4** Ring labels (`r0`–`r4`) and sector labels (`s0`–`s7`) rendered via `_build_ring_labels()` / `_build_sector_labels()`; controlled by `SHOW_LABELS` class attribute.
- [x] **3.5** Caption: _"The AOI is divided into 4 rings × 8 sectors = 32 cells, each capturing local ridge texture."_
- [x] **3.6** Ring 1 / Sector 2 highlighted with gold fill pulse + callout arrow; fill fades back out.
- [x] **3.7** 2.5 s narration hold; all elements fade out in 1.0 s. _(Rendered → `media/videos/s2_tessellation/480p15/TessellationScene.mp4`)_
- [ ] **3.8** Add multi-beat captions: (1) why polar grid, (2) AOI partitioning, (3) cell summary.
- [ ] **3.9** Add a small "AOI" label near the grid edge during the highlight.

---

## Phase 4 — Scene 3: Normalization

> Visualize Step 3 — Per-sector intensity normalization.

- [x] **4.1** Fingerprint (pre-dimmed to 30 %) + polar grid re-established at same FP_HEIGHT/FP_CENTER; `LaggedStart(FadeIn, lag_ratio=0.04)` fans 32 sector overlays in.
- [x] **4.2** 32 `AnnularSector` overlays with seeded-random fills (`BEFORE_DARK` → `BEFORE_BRIGHT` via `interpolate_color`) simulate uneven local contrast; `LaggedStart(Transform, lag_ratio=0.035)` normalisation wave turns all to uniform teal.
- [x] **4.3** Right-side histogram panel: `_build_bar_chart()` + `_build_histogram_panel()`; skewed "Before" bars `Transform` to Gaussian "After" bars simultaneously with the sector sweep.
- [x] **4.4** Caption: _"Each sector is independently normalized: μ₀, σ₀² → uniform mean & variance."_
- [x] **4.5** `MathTex(r"G(x,y) = \mu_0 + \sigma_0 \cdot \frac{I(x,y)-\mu}{\sigma}")` in a dark `RoundedRectangle` panel; plain-text `Text` fallback if LaTeX unavailable. _(LaTeX compiled successfully.)_
- [x] **4.6** 2.5 s narration hold; all elements fade in 1.0 s. _(Rendered → `media/videos/s3_normalization/480p15/NormalizationScene.mp4`)_
- [ ] **4.7** Add staged captions: (1) local contrast varies, (2) normalize per sector, (3) improves comparability.
- [ ] **4.8** Add "Before" and "After" labels for the sector colors and histogram.

---

## Phase 5 — Scene 4: Gabor Filter Bank

> Visualize Step 4 — Multi-directional filtering of the normalized image.

- [x] **5.1** Normalised fingerprint + full polar grid + uniform-teal sectors re-established (pre-dimmed 30%) as starting state.
- [x] **5.2** FadeOut then 4 grid-card objects in arrange_in_grid(rows=2, cols=2); each is a mini polar grid in its channel colour.
- [x] **5.3** Sinusoidal ParametricFunction stripes at each filter angle; hues: teal 0deg, purple 45deg, orange 90deg, green 135deg. LaggedStart lag_ratio=0.3.
- [x] **5.4** Gabor kernel heatmap (NxN Square cells by signed value); sliding Arrow+label for convolution metaphor.
- [x] **5.5** Orientation labels (0deg, 45deg, 90deg, 135deg) in matching hue below each card.
- [x] **5.6** Caption: A bank of F=4 Gabor filters, 4 orientations, 4x32=128 filtered values.
- [x] **5.7** 2.5s hold; fade out 1.0s. _(Rendered to media/videos/s4_filtering/480p15/FilteringScene.mp4)_
- [ ] **5.8** Add staged captions: (1) texture = oriented ridges, (2) Gabor responds to direction, (3) stack 4 channels.
- [ ] **5.9** Add a short definition card: "Gabor filter = oriented band-pass".

---

## Phase 6 — Scene 5: Feature Extraction (FingerCode)

> Visualize Step 5 — Computing A.A.D. and assembling the feature vector.

- [x] **6.1** FP at 30%% + polar grid fades in at core_world.
- [x] **6.2** 32 AnnularSectors colored by seeded AAD values cool-blue to warm-orange; LaggedStart sectors to discs.
- [x] **6.3** MathTex AAD formula in gold-bordered panel top-right.
- [x] **6.4** FP+grid fade out; LaggedStart discs to bar rectangles at y=0.
- [x] **6.5** Label FingerCode Vector + sub-label 128 features; Brace under bar.
- [x] **6.6** Caption about 128-D descriptor.
- [x] **6.7** 2.5s hold; fade out. Rendered to media/videos/s5_feature_extraction/480p15/FeatureExtractionScene.mp4
- [ ] **6.8** Add staged captions: (1) summarize sector energy, (2) AAD measures deviation, (3) vector assembly.
- [ ] **6.9** Add a small "128-D" callout near the final vector.

---

## Phase 7 — Scene 6: Matching

> Visualize Step 6 — Euclidean distance comparison and decision.

- [x] **7.1** Display two FingerCode vectors side-by-side (or stacked):
    - **Top:** Template vector (from database) — labeled `"Template T"`.
    - **Bottom:** Input vector (from query image) — labeled `"Input I"`.
    - Each vector rendered as a row of colored `Rectangle` tiles (reuse Phase 6 style).
- [x] **7.2** Animate glowing connector lines between corresponding tiles of the two vectors using `Line` + a glow effect (`set_stroke(color=YELLOW, width=…)`).
- [x] **7.3** Show component differences animating into squared values, then summed (brief schematic).
- [x] **7.4** Display the Euclidean distance formula using `MathTex`:
    ```
    d(T, I) = \sqrt{\sum_{i=1}^{n} (T_i - I_i)^2}
    ```
- [x] **7.5** Animate a distance meter / progress bar filling up to the computed value.
- [x] **7.6** Branch into two outcomes:
    - If `d < threshold` → green checkmark + `"MATCH ✓"` text (use `GrowFromCenter`).
    - If `d ≥ threshold` → red X + `"NO MATCH ✗"` text.
- [x] **7.7** Hold on the final decision frame, then fade to the outro.
- [ ] **7.8** Add staged captions: (1) compare vectors, (2) compute distance, (3) threshold decision.
- [ ] **7.9** Add a brief label on the meter: "Distance".

---

## Phase 8 — Scene 7: Summary / Outro

> Recap the full pipeline and close the video.

- [ ] **8.1** Display a pipeline flowchart using `Arrow`-connected `RoundedRectangle` nodes, each labeled with a step name (Steps 1–6).
- [ ] **8.2** Animate each node lighting up in sequence, replaying the key visual from its scene as a small thumbnail insert (optional, advanced).
- [ ] **8.3** Display closing text: `"FingerCode — Texture Meets Topology"` with a subtle fade-in.
- [ ] **8.4** Add credits / source references using small `Text` at the bottom.
- [ ] **8.5** Final `FadeOut` of all elements to black.
- [ ] **8.6** Add a recap caption line for each step as the node pulses.

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
- [ ] **9.10** Target runtime ~5:00 by adding 20-30 s of staged text per scene.

---

## Notes & Tips

| Concern                    | Recommendation                                                                               |
| -------------------------- | -------------------------------------------------------------------------------------------- |
| Fingerprint image rights   | Use a synthetic or open-license fingerprint (e.g., FVC2002 sample or generated with `scipy`) |
| Gabor filter visualization | Pre-compute filter response images with `numpy`/`scipy` and load as `ImageMobject`           |
| MathTex compilation        | Test all `MathTex` strings independently early to catch LaTeX errors                         |
| Performance                | Render each scene file separately (`-pql`) iteratively; only do full render at the end       |
| Code reuse                 | Keep all shared geometry (polar grid, color palette) in `utils/` to avoid duplication        |
