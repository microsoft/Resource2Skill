### 1. High-level Skill Pattern Extraction

> **Skill Name**: Clean Marker Line Chart

* **Tier**: component
* **Core Mechanism**: Constructs a minimalist, dashboard-friendly line chart by stripping away backgrounds, borders, and gridlines. Applies a thickened series line with prominent circular markers, removes the legend, and formats the value axis using a compact thousands ("K") suffix to reduce visual clutter.
* **Applicability**: Best used on themed dashboards to show time-series trends (like monthly sales or active users) where a clean, non-distracting visual is needed to blend seamlessly with the underlying sheet background.

### 2. Structural Breakdown

- **Data Layout**: Expects a two-column dataset (e.g., Category/Month and Value) ideally driven by a PivotTable or aggregate formulas.
- **Formula Logic**: None required; operates on provided cell ranges.
- **Visual Design**: Transparent chart area and plot area fills so the dashboard background shows through. Gridlines and legend are deleted to maximize the data-to-ink ratio. 
- **Charts/Tables**: LineChart with custom `GraphicalProperties` for background removal, a custom `#,##0,"K"` number format on the Y-axis, and custom `Marker` properties for the series.
- **Theme Hooks**: Backgrounds are set to transparent to inherit the global sheet theme (e.g., `bg_base`). The line and markers naturally inherit the active workbook's `accent1` palette color.

### 3. Reproduction Code

