### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive-Style Sales Dashboard

* **Tier**: archetype
* **Core Mechanism**: Constructs a multi-sheet workbook mimicking a modern, interactive web dashboard. It hides the raw calculation data on a backend sheet while using border/fill stylized cell blocks on a light gray grid to simulate floating shape "cards". It integrates Doughnut charts for KPIs, Line charts for trends, and Radar charts for categorical scores.
* **Applicability**: Best for executive summaries and high-level metric reporting where you want a clean, "UI-like" presentation format without dealing with finicky drawing shapes that can distort when rows/columns are adjusted.

### 2. Structural Breakdown

- **Data Layout**: An `Inputs` sheet structures data vertically. KPI targets are mapped into `Complete` vs `Remainder` rows (perfect for Doughnut charting). Trend lines use contiguous matrices, and satisfaction scores map category-to-float.
- **Formula Logic**: Standard percentage scaling for the KPI rings (`=Actual/Target` and `=1-Complete`).
- **Visual Design**: Uses a solid `1E3A8A` (Dark Blue) simulated side-nav bar. The worksheet background uses `F3F4F6` (Light Gray) to push white "Card" regions forward. Cards are bounded by thin `D1D5DB` borders.
- **Charts/Tables**: 
  - `DoughnutChart`: Sized down heavily with `holeSize=65` and `legend=None` to act as pure KPI micro-visuals.
  - `LineChart`: Employs a fixed y-axis scaling (min=180) to exaggerate trend movements.
  - `RadarChart`: Uses `type="filled"` to visually anchor the multiple dimensions of customer satisfaction.
- **Theme Hooks**: Background colors act as the main driver, leveraging corporate dark blue accents (`1E3A8A`) and crisp UI grays (`F3F4F6`, `6B7280`).

### 3. Reproduction Code

