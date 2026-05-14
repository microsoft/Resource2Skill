### 1. High-level Skill Pattern Extraction

> **Skill Name**: Minimalist KPI Trend Card

* **Tier**: component
* **Core Mechanism**: Constructs a self-contained KPI card pairing a bold summary metric with a minimalist, sparkline-style trend chart. It transforms a standard line chart by systematically stripping all default elements (axes, gridlines, legends, borders) and applying a thickened, smoothed line to maximize the data-ink ratio in tight spaces.
* **Applicability**: Ideal for executive dashboards and reports where multiple high-level trends (e.g., Monthly Sales, Conversion Rates, Traffic Sources) must be displayed compactly alongside their total values, without the visual clutter of full axes.

### 2. Structural Breakdown

- **Data Layout**: A single column of chronological values hosted on a backing data worksheet.
- **Formula Logic**: None required; relies on direct chart references to the data column.
- **Visual Design**: Uses a typographic hierarchy: a subdued, smaller font for the category title and a large, high-contrast font for the current KPI value, directly above the chart.
- **Charts/Tables**: `LineChart` configured with `x_axis.delete = True`, `y_axis.delete = True`, and `legend = None`. The series is customized with `smooth = True` and a heavy stroke width.
- **Theme Hooks**: Consumes `text` (KPI value), `subtext` (title), and `accent` (trend line color).

### 3. Reproduction Code

