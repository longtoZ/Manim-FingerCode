# SCRIPT.md — FingerCode Algorithm Narration Script

> **Video:** _FingerCode — A Texture-Based Fingerprint Recognition Method_
>
> **Total estimated runtime:** ~12–14 minutes
>
> **Voice style:** Calm, authoritative, educational — as if explaining to an advanced undergraduate class in biometrics or computer vision.
>
> **Conventions:** Each section corresponds to one Manim scene. Narration should be paced to the on-screen animations. Pauses (…) indicate moments where the animation should speak for itself before you continue.

---

## Section 0: Introduction & Title Card

**Scene file:** `scenes/s0_intro.py` — **`IntroScene`**
**Estimated duration:** ~55 seconds
**On-screen action:**

- Deep-navy background fades in.
- A fingerprint image fades in as a dim (12% opacity) backdrop.
- A glowing teal horizontal divider line draws across the middle.
- The main title **"FingerCode Algorithm"** appears above the divider, with "FingerCode" in gold and "Algorithm" in white.
- The subtitle **"A Texture-Based Fingerprint Recognition Method"** fades in below the divider.
- A six-step pipeline bar fades in at the bottom: _Reference Point → Tessellation → Normalization → Filtering → Feature Extraction → Matching_ (all dimmed, no step highlighted yet).
- Three captions appear sequentially near the bottom, followed by a definition card in the top-right corner: _"FingerCode = texture features from polar sectors"_.
- Everything fades out.

### Narration

**[0:00 — Background and fingerprint fade in]**

> Fingerprint recognition is one of the oldest and most reliable forms of biometric identification. But how does a computer turn a messy, noisy image of ridges and valleys into a compact code that can be matched against millions of stored records?

**[0:10 — Divider draws, title appears]**

> In this video, we will explore the **FingerCode algorithm** — a texture-based approach that analyzes ridge patterns locally and encodes them into a fixed-length descriptor. The method was introduced by Hong, Wan, and Jain in 1998, and it remains a foundational technique in fingerprint image analysis.

**[0:22 — Subtitle appears]**

> Unlike minutiae-based systems that look for specific ridge endings and bifurcations, FingerCode captures the _texture_ of the fingerprint using oriented filters — making it robust to small distortions and image noise.

**[0:32 — Pipeline bar fades in]**

> The algorithm proceeds through six sequential steps, which we will cover one by one in this video.

**[0:40 — Captions cycle]**

> The goal is simple: compress a fingerprint into a compact code…
>
> …Each step isolates stable ridge texture…
>
> …and we finish by comparing codes to decide a match.

**[0:52 — Definition card appears]**

> In essence, a FingerCode is a collection of texture features extracted from polar sectors centred on the fingerprint core. Let's see how it works.

**[1:00 — Fade out]**

---

## Section 1: Algorithm Overview

**Scene file:** `scenes/s0a_overview.py` — **`OverviewTextScene`**
**Estimated duration:** ~40 seconds
**On-screen action:**

- Title: **"How FingerCode Works"** (gold, top edge).
- Subtitle: _"Goal: compress a fingerprint into a stable, comparable code"_.
- Two body paragraphs animate in, describing the pipeline.

### Narration

**[0:00 — Title appears]**

> Here is a roadmap of what we are about to build.

**[0:07 — Subtitle appears]**

> We start with a single fingerprint image that may contain noise, contrast changes, or small distortions, and we aim to turn it into a compact code that is stable across different captures.

**[0:15 — First paragraph]**

> The pipeline first finds the core, tessellates the area of interest, and normalizes contrast. Then it filters oriented texture, extracts features, and compares the resulting FingerCode vectors.

**[0:27 — Second paragraph]**

> Each step transforms the data into a more structured and more comparable representation. By the end, a raw pixel image becomes a small numeric vector that can be stored and matched efficiently — even across millions of fingerprints.

**[0:38 — Fade out]**

---

## Section 2: Reference Point Detection

**Scene file:** `scenes/s1_reference_point.py` — **`ReferencePointScene`**
**Estimated duration:** ~75 seconds
**On-screen action:**

- Pipeline bar slides in with **Step 1 (Reference Point)** highlighted in gold.
- Step header fades in at top: _"Step 1 — Reference Point Detection"_.
- Full-opacity fingerprint image appears with a subtle teal border.
- A glowing teal horizontal scan line sweeps from top to bottom (simulating analysis).
- A crosshair + concentric target rings converge on the core point.
- A glowing gold dot appears at the core, followed by a pulsing ring animation.
- An arrow and label _"Core Point (Reference)"_ animate in.
- Three captions cycle near the pipeline bar, plus a definition card: _"Core point = reference for alignment"_.
- Hold for narration, then non-essential elements fade out (fingerprint + core dot left if handoff mode).

### Narration

**[0:00 — Pipeline bar and header appear]**

> Step one: we locate a stable reference point — the **core** of the fingerprint.

**[0:10 — Fingerprint appears with border]**

> This is a raw fingerprint image. The core is the point where the innermost ridge curves around on itself, forming a loop. It is the most stable and recognizable landmark in the print.

**[0:20 — Scan line sweeps]**

> The algorithm scans the image to analyze ridge orientation at each pixel. It looks for the region where ridge flow changes direction most abruptly — that is where the core lies.

**[0:30 — Crosshair locks on]**

> Once detected, a crosshair locks onto the core coordinates.

**[0:38 — Gold core dot appears with pulse]**

> This golden dot marks the core point. It becomes the anchor for every geometric measurement that follows.

**[0:46 — Arrow and label appear]**

> The core point is our reference. All sectors, all filters, all feature measurements — everything will be aligned relative to this single location. This is what makes the FingerCode robust to fingerprint translation: if the finger is placed slightly differently on the sensor, the core still anchors the analysis in the same way.

**[0:58 — Captions cycle]**

> Find the core where ridge flow turns inward…
>
> …This point stabilizes rotation and alignment…
>
> …All sectors are measured relative to this anchor.

**[1:10 — Definition card]**

> The core point serves as the spatial origin for the entire pipeline.

**[1:15 — Fade out (transient elements)]**

---

## Section 3: Tessellation

**Scene file:** `scenes/s2_tessellation.py` — **`TessellationScene`**
**Estimated duration:** ~70 seconds
**On-screen action:**

- Pipeline bar with **Step 2 (Tessellation)** highlighted in gold.
- Step header: _"Step 2 — Tessellation"_.
- Fingerprint image + gold core dot re-appear.
- Innermost concentric ring grows from the core outward.
- Successive rings expand with a staggered delay (LaggedStart).
- Radial spokes draw outward from the inner ring, fanning like a spinning web.
- (Optional) Ring-index labels (r0, r1, r2, r3, r4) and sector-index labels (s0–s7) appear.
- One example sector flashes with a gold fill pulse.
- Caption: _"AOI divided into R rings × S sectors = R×S cells."_
- Narration hold, then fade out.

### Narration

**[0:00 — Pipeline, header, fingerprint + core appear]**

> Step two: we divide the area around the core into a structured polar grid — a process called **tessellation**.

**[0:12 — First ring grows]**

> The algorithm defines concentric rings radiating outward from the core. The innermost ring starts just a small distance away — the inner radius — and each successive ring expands outward.

**[0:22 — All rings expand]**

> Here we see all four rings coming into view. The number of rings is a parameter of the algorithm; in our case, we use four.

**[0:30 — Spokes fan out]**

> Next, radial spokes divide each ring into angular sectors. These spokes emanate from the core like the rays of a spiderweb.

**[0:40 — Labels appear]**

> With **four rings** and **eight sectors**, the area of interest is partitioned into **32 cells** — each one a local neighbourhood at a specific distance and direction from the core.

**[0:50 — One sector flashes]**

> Each sector captures ridge information from a unique zone. Rings capture _distance_ from the core, while sectors capture _direction_. This means that rotation of the finger shifts values between sectors — but keeps the ring ordering intact — which becomes important for matching.

**[1:00 — Caption]**

> The area of interest is divided into 4 rings times 8 sectors, giving us 32 local cells that can be analysed uniformly.

**[1:08 — Hold for narration]**

> Why a polar grid? Because fingerprint ridges naturally radiate outward from the core in curved patterns. A rectangular grid would not align with this geometry — a polar grid follows the natural structure of the fingerprint.

**[1:18 — Fade out]**

---

## Section 4: Why a Polar Grid? (Text Interlude)

**Scene file:** `scenes/s2a_polar_grid_text.py` — **`PolarGridTextScene`**
**Estimated duration:** ~35 seconds
**On-screen action:**

- Title: **"Why a Polar Grid?"** (gold).
- Two explanatory paragraphs.
- Teal tag: _"AOI = the area of interest we analyze around the core"_.

### Narration

**[0:00 — Title appears]**

> You might wonder — why a polar grid? Why not use a simple Cartesian grid like most image-processing operations?

**[0:08 — First paragraph]**

> The grid is centred on the core to anchor all measurements. Rings capture radial distance, while sectors capture ridge direction. If the fingerprint is rotated, the same ridge texture simply shifts to a neighbouring sector — but the ring sequence stays consistent.

**[0:18 — Second paragraph]**

> With four rings and eight sectors, the area of interest becomes exactly 32 local cells — each small enough to capture local texture, yet large enough to be robust to noise. Every cell can be analysed using identical statistical measurements, making the comparison fair and uniform.

**[0:28 — Tag line]**

> The AOI — area of interest — is the circular region we analyse around the core. Everything that follows happens inside this polar grid.

**[0:35 — Fade out]**

---

## Section 5: Normalization

**Scene file:** `scenes/s3_normalization.py` — **`NormalizationScene`**
**Estimated duration:** ~85 seconds
**On-screen action:**

- Pipeline bar with **Step 3 (Normalization)** highlighted in gold.
- Step header: _"Step 3 — Normalization"_.
- Fingerprint (30% opacity) + polar grid + core dot fade in.
- "Before Normalization" label appears top-right.
- All 32 sectors fill with random dark-to-warm colours simulating uneven local contrast (LaggedStart fan-in).
- One sector (ring 1, sector 3) is spotlit with a gold outline.
- A histogram panel labelled "Before" appears on the right showing a skewed distribution.
- Normalization wave: all sectors transform to a uniform teal fill, and the histogram morphs to a Gaussian-like shape.
- Label changes to "After Normalization".
- The normalization formula appears: _G(x,y) = μ₀ + σ₀ · (I(x,y) − μ) / σ_.
- Three captions cycle, then fade out.

### Narration

**[0:00 — Pipeline, header, fingerprint + grid appear]**

> Step three: normalization. Even after tessellation, the raw pixel intensities across different sectors can vary dramatically.

**[0:12 — "Before" sectors fill in]**

> Here we see the 32 sectors coloured according to their raw intensity distributions. Some sectors may be bright, others dark — this is due to uneven pressure, moisture, or lighting during fingerprint capture.

**[0:22 — Spotlight on one sector + histogram]**

> Let us look closely at one sector. Its intensity histogram is skewed and irregular. If we tried to compare texture features across sectors directly, these lighting artefacts would dominate the measurement, drowning out the actual ridge information.

**[0:35 — Normalization wave begins]**

> The solution is to normalize each sector independently. We re-centre the pixel intensities to a target mean and rescale them to a target variance. This is the normalization equation:

**[0:45 — Formula appears]**

> G of x, y equals μ₀ plus σ₀ times the quantity I of x, y minus μ, all divided by σ. Here, μ and σ are the mean and standard deviation of the current sector, while μ₀ and σ₀ are the desired target values. Every sector goes through this transformation independently.

**[0:58 — All sectors become uniform teal]**

> After normalization, all sectors have the same average intensity and the same contrast range. The ridge pattern itself is preserved — only the lighting bias has been removed.

**[1:08 — Histogram morphs to Gaussian]**

> Notice that the histogram has shifted from a skewed distribution to a more balanced, centred one. This ensures that the same filter response has a consistent meaning regardless of which sector it comes from.

**[1:15 — Captions cycle]**

> Local contrast can vary widely from sector to sector, so raw intensities are not directly comparable across the image…
>
> …We normalize each sector to a common mean and variance, removing lighting bias while preserving ridge texture…
>
> …After normalization, the same filter response has a consistent meaning across different fingerprints.

**[1:28 — Fade out]**

---

## Section 6: Normalization Formula (Text Interlude)

**Scene file:** `scenes/s3a_normalization_formula.py` — **`NormalizationFormulaScene`**
**Estimated duration:** ~35 seconds
**On-screen action:**

- Title: **"Normalization Equation"** (gold).
- Formula in a rounded box with teal border.
- Two explanatory paragraphs.

### Narration

**[0:00 — Title appears]**

> Let us take a closer look at the normalization equation.

**[0:07 — Formula appears]**

> G of x, y equals μ₀ plus σ₀ times I of x, y minus μ, all over σ.

**[0:15 — First paragraph]**

> Here, μ and σ are the mean and standard deviation computed from a single local sector. μ₀ and σ₀ are the target values — the desired mean and variance we want every sector to share.

**[0:25 — Second paragraph]**

> By re-centering and re-scaling each sector independently, we effectively remove any lighting bias that is specific to that region of the fingerprint. This makes the subsequent texture responses comparable not just across sectors in the same image, but across images captured under different conditions.

**[0:35 — Fade out]**

---

## Section 7: Gabor Filter Bank

**Scene file:** `scenes/s4_filtering.py` — **`FilteringScene`**
**Estimated duration:** ~85 seconds
**On-screen action:**

- Pipeline bar with **Step 4 (Filtering)** highlighted in gold.
- Step header: _"Step 4 — Gabor Filter Bank"_.
- Normalised fingerprint (30% opacity) + uniform teal polar grid fade in.
- Context caption: _"The normalized image is passed through a bank of directional filters…"_.
- Grid clones into **4 smaller copies** arranged in a 2×2 layout.
- Each copy has a unique hue tint and a sinusoidal wave overlay at its filter orientation (0°, 45°, 90°, 135°).
- Orientation angle labels appear below each card.
- A Gabor kernel heatmap inset appears top-right with a sliding arrow illustrating the convolution metaphor.
- Three captions cycle, including the feature count: _"4 filters × 32 sectors → 128 features per image"_.
- Hold, then fade out.

### Narration

**[0:00 — Pipeline, header, fingerprint + grid appear]**

> Step four: filtering. Fingerprint ridges are strongly oriented structures, so we need filters that respond selectively to specific directions.

**[0:12 — Context caption]**

> The normalized image is passed through a bank of directional filters so we can measure texture along multiple ridge orientations.

**[0:20 — Grid splits into 4 filter channels]**

> The algorithm applies a bank of **Gabor filters** — these are band-pass filters tuned to specific orientations and spatial frequencies. Here we use four orientations: 0, 45, 90, and 135 degrees.

**[0:32 — Each card shows wave overlay]**

> Each filtered copy reveals the ridge texture that aligns with its orientation. The 0° channel captures horizontal ridge segments; the 90° channel captures vertical ones; and the diagonal channels capture the curved transitions in between.

**[0:44 — Gabor kernel heatmap appears]**

> This is what a Gabor kernel looks like — a sinusoidal wave modulated by a Gaussian envelope. The kernel slides across the image in a convolution operation, and at each position it produces a strong response when the local ridge orientation matches the filter angle.

**[0:58 — Sliding arrow animates]**

> The convolution metaphor: the kernel is scanned across every sector, and the response at each location tells us how strongly the local texture aligns with that orientation.

**[1:06 — Captions cycle]**

> Ridge texture is strongly oriented, so we analyze it with filters that are selective to direction and spatial frequency…
>
> …Each Gabor filter responds to one dominant orientation band, isolating the ridge flow that aligns with that direction…
>
> …Stacking four orientations across 32 cells yields a 128-value texture signature that is compact but still descriptive.

**[1:20 — Hold]**

> Four filters times 32 sectors gives us 128 features per image. This is the raw data from which the final FingerCode will be built.

**[1:28 — Fade out]**

---

## Section 8: Feature Extraction — Computing the FingerCode

**Scene file:** `scenes/s5_feature_extraction.py` — **`FeatureExtractionScene`**
**Estimated duration:** ~85 seconds
**On-screen action:**

- Pipeline bar with **Step 5 (Feature Extraction)** highlighted in gold.
- Step header: _"Step 5 — Feature Extraction"_.
- Fingerprint (30% opacity) + grid appear with sectors coloured by seeded A.A.D. values (cool-to-warm gradient via LaggedStart).
- A.A.D. formula panel fades in top-right.
- All 32 coloured sectors collapse (Transform) into small discs at each sector's centroid.
- Fingerprint + grid rings/spokes fade out.
- The discs fly from their polar positions into a horizontal 1-D bar of rectangles (a vector visualization).
- _"FingerCode Vector"_ label appears, with sub-label: _"(F=4 filters × 4 rings × 8 sectors = 128 features)"_.
- A brace under the bar: _"32 A.A.D. values (1 filter)"_.
- A callout: _"128-D"_ with arrow.
- Three captions cycle, then fade out.

### Narration

**[0:00 — Pipeline, header appear]**

> Step five: feature extraction. This is where the spatial image data transforms into a mathematical vector.

**[0:10 — Fingerprint + coloured sectors appear]**

> The filtered sectors are colour-coded by their texture energy — cool blue for low activity, warm orange for high activity. We need to summarize each sector with a single, meaningful number.

**[0:22 — A.A.D. formula appears]**

> The chosen statistic is the **Average Absolute Deviation**, or A.A.D. For each sector k, we compute the average absolute difference between every pixel intensity and the sector mean. This tells us how much the ridge texture varies within that local region — a high A.A.D. means strong, well-defined ridges; a low A.A.D. means a smooth or low-contrast area.

**[0:38 — Sectors collapse into discs]**

> Each sector is now represented by a single disc at its centroid, coloured by its A.A.D. value. The spatial layout is still preserved — we can see which regions are texturally active.

**[0:48 — Fingerprint fades out]**

> Now we strip away the fingerprint image and the grid. We no longer need them — we have moved from pixels to pure data.

**[0:55 — Discs fly into a 1-D bar]**

> The discs rearrange into a horizontal bar. Each tile in this bar represents one sector's A.A.D. value. The order follows a fixed convention — ring by ring, sector by sector — so that every FingerCode has the same layout.

**[1:08 — Labels appear]**

> This is the **FingerCode vector** — 32 values for one filter orientation. But remember, we have four filter orientations. When we concatenate all four channels, we get a full 128-dimensional descriptor.

**[1:18 — Dimension callout]**

> 128 dimensions — compact enough for fast comparison, yet rich enough to distinguish between different fingers.

**[1:25 — Captions cycle]**

> Within each sector we summarize texture energy as a single A.A.D. value, capturing how much the ridges deviate locally…
>
> …We collect these values in a fixed order across rings and sectors so the vector has a consistent, comparable layout…
>
> …Concatenating all filter channels produces the full 128-D FingerCode descriptor used for matching.

**[1:40 — Fade out]**

---

## Section 9: Matching Logic (Text Interlude)

**Scene file:** `scenes/s6a_matching_text.py` — **`MatchingTextScene`**
**Estimated duration:** ~35 seconds
**On-screen action:**

- Title: **"Matching Logic"** (gold).
- Two explanatory paragraphs describing how FingerCodes are compared.

### Narration

**[0:00 — Title appears]**

> Now we come to the final step: matching. We have a template FingerCode stored in the database, and a new input FingerCode just computed from the incoming image.

**[0:10 — First paragraph]**

> We compare the 128-dimensional FingerCode from the template with the 128-dimensional FingerCode from the input, and we summarize all local differences into a single distance score, d of T comma I.

**[0:20 — Second paragraph]**

> A smaller distance indicates stronger similarity across ridge texture. A threshold is tuned during enrolment to balance false matches against false misses. If the distance falls below the threshold, we declare a match — the two fingerprints are from the same finger.

**[0:35 — Fade out]**

---

## Section 10: Distance Equation (Text Interlude)

**Scene file:** `scenes/s6b_distance_formula.py` — **`DistanceFormulaScene`**
**Estimated duration:** ~30 seconds
**On-screen action:**

- Title: **"Distance Equation"** (gold).
- Euclidean distance formula in a rounded box.
- Two explanatory paragraphs.

### Narration

**[0:00 — Title appears]**

> This is the equation that quantifies the comparison.

**[0:07 — Formula appears]**

> d of T comma I equals the square root of the sum from i equals 1 to n of T sub i minus I sub i squared.

**[0:15 — First paragraph]**

> We take the difference at every corresponding index between the template and the input vector, square it so that positive and negative deviations both contribute, and sum the results. The square root gives us back a distance in the original units.

**[0:25 — Second paragraph]**

> A single scalar distance makes it easy to compare against a threshold and decide whether the two fingerprints belong to the same finger. The lower the distance, the more similar the texture profiles — and the more confident we can be of a match.

**[0:32 — Fade out]**

---

## Section 11: Matching — Visual Comparison & Decision

**Scene file:** `scenes/s6_matching.py` — **`MatchingScene`**
**Estimated duration:** ~70 seconds
**On-screen action:**

- Pipeline bar with **Step 6 (Matching)** highlighted in gold.
- Step header: _"Step 6 — Matching"_.
- Two 32-cell FingerCode vectors appear stacked: **Template T** (top, gold border) and **Input I** (bottom, teal border).
- LaggedStart glowing connector lines link corresponding tiles between the two vectors.
- Euclidean distance formula panel fades in below the input vector.
- A distance meter (progress bar) fills to the computed value, with a numerical label and threshold marker.
- Decision: distance < threshold → green **"MATCH ✓"** grows from centre with a pulsing glow.
- Hold, then fade out.

### Narration

**[0:00 — Pipeline, header appear]**

> Step six: the final comparison — matching.

**[0:10 — Two vector bars appear]**

> Here we have two FingerCode vectors. On top, the **template** vector — the code stored in the database when the finger was enrolled. Below, the **input** vector — the code computed from the fingerprint we just captured. The tiles are colour-coded by A.A.D. value, cool to warm.

**[0:25 — Connector lines draw]**

> Glowing lines connect corresponding positions in the two vectors. Each line represents the difference at one index. The longer the line, the larger the deviation between the two values.

**[0:38 — Formula appears]**

> We compute the Euclidean distance using the formula we just discussed — the square root of the sum of squared differences.

**[0:46 — Distance meter fills]**

> Here is our distance meter. The bar fills from left to right, and the numeric value updates. The threshold is marked — this is the maximum allowed distance for a match.

**[0:56 — Decision appears]**

> In this case, the distance falls below the threshold. The system declares a **MATCH** — the two fingerprints belong to the same finger.

**[1:05 — Pulsing glow]**

> The decision panel pulses green, confirming the successful verification. If the distance had exceeded the threshold, the panel would have turned red with a "NO MATCH" message.

**[1:12 — Hold]**

> And that is the complete FingerCode pipeline — from a raw pixel image to a binary match decision, all driven by texture analysis.

**[1:20 — Fade out]**

---

## Section 12: Summary & Outro

**Scene file:** `scenes/s7_outro.py` — **`OutroScene`**
**Estimated duration:** ~50 seconds
**On-screen action:**

- All six pipeline nodes fade in as a horizontal flowchart at centre, with arrow connectors.
- Each node pulses gold in sequence (LaggedStart) as a recap text line updates below.
- Closing title rises: **"FingerCode — Texture Meets Topology"** (gold + teal).
- Sub-title: _"A Manim-animated walkthrough of Hong, Wan & Jain (1998)"_.
- Credit lines with the full IEEE reference.
- Final fadeout to background colour.

### Narration

**[0:00 — Pipeline nodes appear]**

> Let us recap the complete FingerCode pipeline.

**[0:10 — Nodes pulse in sequence as recap lines update]**

> Step one: find the core reference point.
>
> Step two: partition the area of interest into polar sectors.
>
> Step three: normalize local contrast in each sector.
>
> Step four: filter oriented ridge texture using a Gabor filter bank.
>
> Step five: assemble the FingerCode vector from sector A.A.D. values.
>
> Step six: compare vectors to decide a match.

**[0:30 — Closing title rises]**

> FingerCode — where texture meets topology. By encoding ridge patterns through a structured spatial grid and oriented filters, the algorithm transforms a biometric image into a compact, comparable mathematical code.

**[0:42 — Subtitle and credits appear]**

> This video was inspired by the seminal 1998 paper by Hong, Wan, and Jain, published in IEEE Transactions on Pattern Analysis and Machine Intelligence. Their work demonstrated that texture-based fingerprint analysis could achieve high accuracy while remaining computationally efficient.

**[0:52 — Final hold]**

> Thank you for watching. I hope this walkthrough has given you a clear understanding of how the FingerCode algorithm works, step by step.

**[1:00 — Fade to black]**

---

## Appendix: Scene Timing Summary

| #   | Scene                           | File                           | Est. Duration    |
| --- | ------------------------------- | ------------------------------ | ---------------- |
| 0   | Intro & Title Card              | `s0_intro.py`                  | ~55 s            |
| 1   | Algorithm Overview              | `s0a_overview.py`              | ~40 s            |
| 2   | Reference Point Detection       | `s1_reference_point.py`        | ~75 s            |
| 3   | Tessellation                    | `s2_tessellation.py`           | ~70 s            |
| 4   | Why a Polar Grid?               | `s2a_polar_grid_text.py`       | ~35 s            |
| 5   | Normalization                   | `s3_normalization.py`          | ~85 s            |
| 6   | Normalization Formula           | `s3a_normalization_formula.py` | ~35 s            |
| 7   | Gabor Filter Bank               | `s4_filtering.py`              | ~85 s            |
| 8   | Feature Extraction (FingerCode) | `s5_feature_extraction.py`     | ~85 s            |
| 9   | Matching Logic                  | `s6a_matching_text.py`         | ~35 s            |
| 10  | Distance Equation               | `s6b_distance_formula.py`      | ~30 s            |
| 11  | Matching — Visual Comparison    | `s6_matching.py`               | ~70 s            |
| 12  | Summary & Outro                 | `s7_outro.py`                  | ~50 s            |
|     | **Total**                       |                                | **~11 min 35 s** |
