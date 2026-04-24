The **FingerCode algorithm** is a local texture analysis technique used for fingerprint matching. Instead of relying solely on extracting minutiae points, this approach uses filtering and spatial tessellation to capture both the local texture information of the ridges and the global spatial relationship among these local contributions. 

The algorithm operates through the following sequential steps:

**Step 1: Locating the Reference Point**
*   **Description:** The algorithm begins by analyzing the input fingerprint image to **locate a specific reference point**, which is the core point of the fingerprint. 
*   **Visualization:** This step can be elegantly visualized by showing a raw, grayscale fingerprint image, followed by a target or crosshair smoothly locking onto the central core of the fingerprint's ridge pattern.

**Step 2: Tessellation (Dividing the Image into Sectors)**
*   **Description:** With the reference point established, the fingerprint area of interest surrounding this core is **tessellated, meaning it is divided into a circular spatial grid** consisting of multiple sectors.
*   **Visualization:** An animation of a spiderweb-like geometric grid (concentric circles intersected by radial lines) smoothly expanding outward from the core point, perfectly overlaying the fingerprint image.

**Step 3: Normalization**
*   **Description:** The image region contained within each individual sector of the spatial grid is independently **normalized**. This step standardizes the pixel intensity and contrast to prepare the texture for accurate filtering.
*   **Visualization:** The discrete sectors within the overlaid grid flashing or adjusting their contrast one by one (or simultaneously), resulting in a uniform, standardized grayscale balance across the entire circular region.

**Step 4: Filtering**
*   **Description:** The normalized image is passed through a bank of filters designed to **extract local texture information** by analyzing the ridge orientations and frequencies. 
*   **Visualization:** The single normalized grid branching out into multiple identical grids, where each grid applies a different directional filter. These filtered grids would visually appear as alternating light and dark wavy ripples, highlighting ridges that flow in specific directions.

**Step 5: Feature Extraction (Computing the FingerCode)**
*   **Description:** From the filtered sectors, specific statistical data is calculated—specifically, the system computes the **Average Absolute Deviation (A.A.D.) feature** for each sector. The ordered enumeration of all these extracted A.A.D. features across the tessellation forms the final 1D or 2D feature vector, which is called the **FingerCode**.
*   **Visualization:** The rippling, filtered grids smoothly morphing into arrays of shaded geometric discs or an ordered grid of numerical values, illustrating the exact moment the spatial image data transforms into a purely mathematical feature vector.

**Step 6: Matching**
*   **Description:** To determine a match, the system compares the template FingerCode (enrolled in the database) against the newly generated input FingerCode. This comparison is achieved simply by **computing the Euclidean distance between the two feature vectors**. 
*   **Visualization:** The template FingerCode and the input FingerCode vectors displayed side-by-side or stacked. Glowing lines could connect their corresponding sectors to visually represent the mathematical comparison, culminating in a final similarity score and a "match" or "no match" decision.
*   **Formula:** While the provided text states that Euclidean distance is used, it does not print the specific mathematical equation. Drawing on general mathematical knowledge outside of the provided sources, the standard formula for calculating the Euclidean distance $d$ between a template vector $T$ and an input vector $I$, both of length $n$, is: 
    **$d(T, I) = \sqrt{\sum_{i=1}^{n} (T_i - I_i)^2}$**