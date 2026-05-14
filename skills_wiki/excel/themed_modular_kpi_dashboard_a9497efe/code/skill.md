### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Modular KPI Dashboard

* **Tier**: sheet_shell
* **Core Mechanism**: Renders a modular grid of 4x3 KPI cards with dynamic conditional formatting rules pointing to an inline target cell. The shell configures column widths, removes gridlines, and establishes a visual hierarchy with bold, solid-fill section headers above isolated data blocks.
* **Applicability**: When building executive summaries, balanced scorecards, or top-level dashboards where stakeholders need to see absolute figures immediately alongside performance status (green/red background) and context (target/prior period).

### 2. Structural Breakdown

- **Data Layout**: Each KPI card occupies a 3-row by 4-column block. Row 1 is the merged header; Row 2 is the merged oversized value; Row 3 holds the comparison metrics ("Vs Target" and "Vs Prior").
- **Formula Logic**: Uses standard openpyxl `CellIsRule` with absolute cell references to drive the background color of the main value cell based on the neighboring target value.
- **Visual Design**: Gridlines are hidden for a clean dashboard look. Section headers span the dashboard width. Cards use large fonts (size 24) for the focal metric. Good/Bad statuses use standard Excel green (`C6EFCE`) and red (`FFC7CE`) fills.
- **Charts/Tables**: Dropdown implemented via `DataValidation` to simulate a dynamic period selector.
- **Theme Hooks**: Utilizes `primary` for section headers and the dashboard title, and `text` for the large KPI figures.

### 3. Reproduction Code

