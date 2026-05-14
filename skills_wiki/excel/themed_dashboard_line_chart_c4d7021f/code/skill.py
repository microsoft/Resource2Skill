### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Dashboard Line Chart

* **Tier**: component
* **Core Mechanism**: Constructs a highly stylized line chart optimized for custom dashboards. It strips away default backgrounds, borders, and gridlines to blend seamlessly with the underlying sheet. Data markers are styled with a fill matching the line color and a border matching the dashboard background, creating a professional "cutout" effect. Y-axis numbers are formatted to show "K" for thousands.
* **Applicability**: Use when integrating trend lines into a custom-designed dashboard where standard Excel chart containers look out of place. Perfect for monthly performance metrics like sales, visitors, or customer rates.

### 2. Structural Breakdown

- **Data Layout**: Time-series data in adjacent columns (e.g., Month, Value), typically placed on a hidden calculation sheet or drawn directly from a PivotTable.
- **Formula Logic**: N/A (Chart rendering relies on openpyxl `Reference` objects pointing to the data).
- **Visual Design**: Transparent chart and plot areas to allow the dashboard background to show through. Smooth lines with elevated thickness for modern aesthetics.
- **Charts/Tables**: `LineChart` with custom markers (`circle` symbol, color-matched fill, background-matched border). Removed legend, title, and gridlines.
- **Theme Hooks**: Consumes a background color (`bg_hex`) for the marker borders (to simulate transparency) and an accent color (`accent_hex`) for the primary line and marker fill.

### 3. Reproduction Code

