### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Sales Dashboard

*   **Tier**: sheet_shell
*   **Core Mechanism**: Constructs a visually coherent and interactive Excel dashboard within a single sheet. It leverages a structured layout using stylized merged cells, integrates common chart types (line, donut) with theme-aligned formatting, and displays key performance indicators (KPIs) linked to source data.
*   **Applicability**: Creating professional, interactive management dashboards for sales, marketing, operations, or any domain requiring a visual summary of performance metrics, trend analysis, and performance tracking against targets. Suitable for data analysis reports needing a clean, dynamic, and easy-to-read interface.

### 2. Structural Breakdown

-   **Data Layout**: Data is organized in a separate 'Inputs' sheet, with tables for KPIs (actual, target, % complete, remainder), monthly sales figures for multiple years, sales by country, and customer satisfaction scores. The dashboard sheet acts as a visual layer.
-   **Formula Logic**:
    -   **KPI Completion Percentages**: `Inputs!D7 = Inputs!D5/Inputs!D6` (for Sales), `Inputs!G7 = Inputs!G5/Inputs!G6` (for Profit), `Inputs!J7 = Inputs!J5/Inputs!J6` (for Customers). These drive the donut charts.
    -   **KPI Display Values**: Dashboard displays actual numerical values and associated donut charts for percentage completion. Numerical values for Sales, Profit, and #Customers are dynamically linked via cell references (e.g., `=Inputs!D5`) within text boxes (simulated by merged cells in this openpyxl example).
-   **Visual Design**:
    -   **Overall Background**: White.
    -   **Sidebar**: Column A is filled with `header_bg` color. Text placeholders for icons with `header_fg` color, hyperlinked for navigation.
    -   **Main Title Bar**: Large merged cell (B2:M4) formatted as a rounded rectangle. `primary_bg` fill, no border, mimicked shadow. Text in `text_color` font, bold, large size.
    -   **KPI Boxes**: Merged cells (e.g., B5:E8) formatted as rounded rectangles. `primary_bg` fill, no border, mimicked shadow. Titles in `text_color` font, bold.
    -   **Chart Boxes**: Merged cells (e.g., B10:H19 for sales trend) formatted as rounded rectangles. `primary_bg` fill, no border, mimicked shadow. Titles in `text_color` font, bold.
-   **Charts/Tables**:
    -   **Donut Charts**: Three charts (placed at D5, H5, L5) for Sales, Profit, and #Customers. Data from respective `% Complete` and `Remainder` cells. Doughnut hole size 65%. Segments colored with `accent1` (complete) and `secondary_bg` (remainder). No title, no legend. Percentage text dynamically shown via a merged cell placed within the donut.
    -   **Line Chart (Sales Trend)**: Placed at B12. Data from `Inputs!C21:D32` with categories from `B21:B32`. No title, legend at bottom. Y-axis min 180. Line 2021: `accent1`, circle markers (white fill, `accent1` border). Line 2022: `accent2`, circle markers (white fill, `accent2` border). No chart area fill or border.
    -   **Radar Chart & Map Chart**: Represented by merged cell placeholders due to `openpyxl`'s current limitations for direct creation and dynamic embedding of these specific chart types with all tutorial features.
-   **Theme Hooks**: `header_bg`, `header_fg`, `primary_bg`, `text_color`, `accent1`, `accent2`, `secondary_bg`, `transparent`.

### 3. Reproduction Code

