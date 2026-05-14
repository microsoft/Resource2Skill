### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Dashboard Shell Layout

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a multi-chart dashboard layout by disabling sheet gridlines, merging cells for a prominent themed header, rendering a left-hand control panel (mocking slicers/filters), and generating a grid of charts linked to a hidden, dedicated data worksheet.
* **Applicability**: Ideal for generating clean, read-only executive summary dashboards, or as a scaffold that users can later swap with interactive PivotCharts. 

### 2. Structural Breakdown

- **Data Layout**: Places raw/aggregated data on a secondary hidden sheet (`{sheet_name}_Data`) to keep the front-end dashboard canvas pristine.
- **Formula Logic**: Uses openpyxl's `Reference` objects to securely bind the dashboard charts to the hidden aggregated data arrays without cross-sheet formula string complexity.
- **Visual Design**: Disables standard gridlines (`showGridLines = False`). Uses bold, high-contrast block headers and subtle border lines for the control panel. 
- **Charts/Tables**: Arranges a `LineChart` and two `BarChart` objects in a distinct grid layout. 
- **Theme Hooks**: Consumes `primary` (header background), `secondary` (control panel header), and `text` (header font color) tokens from the theme dictionary.

### 3. Reproduction Code

