### 1. High-level Skill Pattern Extraction

> **Skill Name**: Minimalist Area Trend Chart

* **Tier**: component
* **Core Mechanism**: Generates an Area chart and systematically strips away all default "chrome" (axes, gridlines, legend, background fills, and borders). This leaves a clean, floating data shape that blends seamlessly into a custom dashboard background, mimicking a modern UI sparkline.
* **Applicability**: Best used underneath or alongside prominent KPI numbers (like a conversion rate or returning customer percentage) to provide historical context without cluttering the layout with full chart axes.

### 2. Structural Breakdown

- **Data Layout**: Two columns (Categories for time periods, Values for the metric).
- **Formula Logic**: None required for the component execution.
- **Visual Design**: The chart area is explicitly set to transparent (`noFill=True`) with no bounding line.
- **Charts/Tables**: `AreaChart`, sized down (e.g., 6x3) to fit inside a dashboard card.
- **Theme Hooks**: Consumes a primary accent color for the area series fill.

### 3. Reproduction Code

