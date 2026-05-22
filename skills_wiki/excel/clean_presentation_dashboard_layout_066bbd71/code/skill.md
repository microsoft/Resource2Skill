### 1. High-level Skill Pattern Extraction

> **Skill Name**: Clean Presentation Dashboard Layout

* **Tier**: sheet_shell
* **Core Mechanism**: Sets up an interactive-style dashboard canvas by hiding standard Excel gridlines and row/column headers. Creates a clean, aligned visual grid by anchoring a primary chart and stacked secondary charts to specific cell coordinates. Leverages a hidden companion sheet to host the aggregate data safely out of view.
* **Applicability**: Best used when delivering aggregate KPIs, trends, and summary reports to management or clients. It elevates a standard spreadsheet into a presentation-ready application interface. 

### 2. Structural Breakdown

- **Data Layout**: A dedicated, hidden worksheet acts as the data source for the charts, separating the backend data layer from the frontend presentation layer.
- **Formula Logic**: Uses standard static values in the data sheet (would typically be populated by pivot aggregates or `SUMIFS` in a dynamic scenario).
- **Visual Design**: Turns off `showGridLines` and `showRowColHeaders` on the worksheet view. Uses a prominent, themed title spanning the top of the canvas to establish visual hierarchy. 
- **Charts/Tables**: Uses a primary Stacked Bar chart for multi-dimensional data (e.g., Profit by Market & Product) and two smaller Line charts (e.g., Trends over time) arranged vertically to balance the layout. Legends are removed on single-series line charts to reduce clutter.
- **Theme Hooks**: Consumes primary text colors (or falls back to `"003366"`) for the dashboard title to match the corporate palette. Relies on built-in Excel chart styles (`style=10`, `style=13`) for immediate, clean color assignment.

### 3. Reproduction Code

