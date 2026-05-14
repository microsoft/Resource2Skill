### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed KPI Doughnut Card

* **Tier**: component
* **Core Mechanism**: Builds a modular KPI card containing a title, raw metric, and a minimalist doughnut chart showing percentage completion. Uses `openpyxl.chart.marker.DataPoint` to explicitly color individual "actual" and "remaining" chart slices, removes standard chart furniture (legends/titles), and sets `holeSize` to 65% for a modern dashboard aesthetic.
* **Applicability**: Ideal for high-level executive dashboards to show metrics against targets (e.g., Sales vs Target, Budget Utilized, Quota Attainment). Fits well in a grid layout across the top of a report.

### 2. Structural Breakdown

- **Data Layout**: Places the visible Title and Value at the anchor cell, and writes the background percentage calculations (`actual/target` and `1 - actual/target`) far off-screen (e.g., 20 columns to the right) to keep the dashboard sheet clean.
- **Formula Logic**: Calculates `pct_complete` and `pct_remain` in Python before injecting them into the hidden data columns. 
- **Visual Design**: Uses a distinct theme color for the title, value, and the "actual" chart slice, while using a muted gray for the "remaining" slice to draw the eye to the completion rate.
- **Charts/Tables**: `DoughnutChart` sized down to 4.5x4.5 cm with `holeSize=65`, `legend=None`, and `title=None`.
- **Theme Hooks**: Consumes `primary_color` (for the metric and filled slice), `muted_color` (for the empty slice), and `text_color` (for the label).

### 3. Reproduction Code

