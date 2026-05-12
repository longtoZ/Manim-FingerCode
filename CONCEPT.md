The **FingerCode algorithm** is a local texture analysis technique used for fingerprint matching, and it is designed to summarize ridge patterns in a way that is robust to small distortions and image noise. Rather than relying exclusively on minutiae extraction, the method applies filtering and spatial tessellation so it can encode both the fine-grained ridge texture and the broader spatial arrangement of those textures around a stable reference point.

The algorithm operates through the following sequential steps, each building on the previous step so the representation becomes progressively more structured and comparable across images:

**Step 1: Locating the Reference Point**

- **Description:** The algorithm begins by analyzing the input fingerprint image to **locate a specific reference point**, which is typically the core point where ridge flow bends into a characteristic loop, because this point provides a stable anchor for the rest of the pipeline.
- **Visualization:** This step can be visualized by showing a raw grayscale fingerprint image and then animating a target or crosshair smoothly locking onto the central core of the ridge pattern, emphasizing that the rest of the processing will be measured relative to this location.

**Step 2: Tessellation (Dividing the Image into Sectors)**

- **Description:** With the reference point established, the fingerprint area of interest surrounding this core is **tessellated, meaning it is divided into a circular spatial grid** consisting of multiple rings and angular sectors so that each cell captures a specific radial distance and direction.
- **Visualization:** An animation of a spiderweb-like geometric grid (concentric circles intersected by radial lines) smoothly expanding outward from the core point can clearly illustrate how the fingerprint is partitioned into local neighborhoods that are aligned to the same central anchor.

**Step 3: Normalization**

- **Description:** The image region contained within each individual sector of the spatial grid is independently **normalized**, which standardizes pixel intensity and contrast so that local variations in illumination do not dominate the texture measurements.
- **Visualization:** The discrete sectors within the overlaid grid can flash or adjust their contrast one by one (or simultaneously), with the resulting view showing a more uniform grayscale balance across the entire circular region while preserving the ridge pattern itself.

**Step 4: Filtering**

- **Description:** The normalized image is passed through a bank of filters designed to **extract local texture information** by responding to specific ridge orientations and spatial frequencies, which helps separate directional patterns that are characteristic of fingerprint structure.
- **Visualization:** The single normalized grid can branch out into multiple identical grids, where each grid applies a different directional filter; these filtered grids would visually appear as alternating light and dark wavy ripples that emphasize ridges aligned with each filter orientation.

**Step 5: Feature Extraction (Computing the FingerCode)**

- **Description:** From the filtered sectors, specific statistical data is calculated, and the system computes the **Average Absolute Deviation (A.A.D.) feature** for each sector to summarize how strongly the ridge texture varies within that local region. The ordered enumeration of all these extracted A.A.D. features across the tessellation forms the final 1D or 2D feature vector, which is called the **FingerCode**, and it serves as the compact descriptor used for matching.
- **Visualization:** The rippling, filtered grids can smoothly morph into arrays of shaded geometric discs or an ordered grid of numerical values, illustrating the exact moment the spatial image data transforms into a purely mathematical feature vector that can be compared efficiently.

**Step 6: Matching**

- **Description:** To determine a match, the system compares the template FingerCode (enrolled in the database) against the newly generated input FingerCode, and this comparison is achieved by **computing the Euclidean distance between the two feature vectors** so that smaller distances indicate stronger similarity.
- **Visualization:** The template FingerCode and the input FingerCode vectors can be displayed side by side or stacked, with glowing lines connecting corresponding sectors to visually represent the mathematical comparison, culminating in a final similarity score and a clear "match" or "no match" decision.
- **Formula:** While the provided text states that Euclidean distance is used, it does not print the specific mathematical equation. Drawing on general mathematical knowledge outside of the provided sources, the standard formula for calculating the Euclidean distance $d$ between a template vector $T$ and an input vector $I$, both of length $n$, is:
  **$d(T, I) = \sqrt{\sum_{i=1}^{n} (T_i - I_i)^2}$**
