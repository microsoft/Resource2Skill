### 1. High-level Skill Pattern Extraction

> **Skill Name**: Modern Trend Line Chart

* **Tier**: component
* **Core Mechanism**: Creates a polished Line Chart comparing two series (e.g., current vs previous year) across categories. It programmatically adjusts the Y-axis minimum bound to highlight variance, and styles the lines with "hollow" markers (white fill with a colored border matching the line), replicating modern interactive dashboard aesthetics.
* **Applicability**: Best for time-series comparisons where highlighting the delta between two periods is more important than showing the absolute scale starting from zero.

### 2. Structural Breakdown

- **Data Layout**: Categories (e.g., Months) in the first column, Series 1 (Previous Year) in the second, Series 2 (Current Year) in the third.
- **Formula Logic**: None required; relies on static or pre-calculated trend data.
- **Visual Design**: Hides major gridlines for a clean look and positions the legend at the top to save horizontal space.
- **Charts/Tables**: `LineChart` with custom marker styling (`Marker(symbol="circle")`, inner fill white, border matches line color, border width increased). Y-axis minimum is explicitly set to bound the data tightly.
- **Theme Hooks**: Uses the primary accent color (`theme.accent1` or dark blue) for the current year, and a secondary or warning color (`theme.accent2` or red) for the comparison year.

### 3. Reproduction Code

