### 1. High-level Skill Pattern Extraction

> **Skill Name**: Two-Panel Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a modern, software-like dashboard layout by disabling gridlines, establishing a dark thematic left sidebar for KPIs, and leaving a spacious, subtly-tinted main area for charts. While the tutorial uses floating shapes for backgrounds, this pattern adapts the concept natively to Excel cell fills and column width adjustments, providing a far more robust grid for `openpyxl` generation without floating object alignment issues.
* **Applicability**: Best for executive summaries and overview dashboards where high-level metrics (KPIs) need to be anchored visibly and consistently alongside a main grid of deeper visual analysis.

### 2. Structural Breakdown

- **Data Layout**: 
  - Column A: Sidebar Left Margin (width: 3)
  - Column B: Sidebar Content (width: 28, holds Titles and KPIs)
  - Column C: Sidebar Right Margin (width: 3)
  - Column D: Main Content Margin (width: 4)
  - Columns E+: Main Charting Area
- **Formula Logic**: Static layout scaffolding. Designed to accept injected string values or external formula references via the `kpis` list.
- **Visual Design**: Gridlines disabled. The sidebar uses a deep primary theme color with bright white text to force high contrast. KPI values are scaled up to size 24 and bolded to create a strict visual hierarchy against the size 11 labels.
- **Charts/Tables**: Establishes the spatial grid where subsequent charts should be anchored (e.g., top-left chart at E5).
- **Theme Hooks**: 
  - `primary`: Drives the dark sidebar background.
  - `text_light`: Drives the high-contrast text and divider lines on the sidebar.
  - `background`: Drives the subtle canvas color for the main charting area.

### 3. Reproduction Code

