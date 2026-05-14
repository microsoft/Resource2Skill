### 1. High-level Skill Pattern Extraction

> **Skill Name**: Data Summary with Top KPIs and Sparklines

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a structured data table with frozen header panes, creates dynamic top-level KPI summary cards using `TEXT` formulas to format aggregated data, and adds bottom-row sparklines for inline trend visualization.
* **Applicability**: Excellent for "raw data" tabs that need to be readable and presentable, acting as a mini-dashboard or high-level summary before feeding into more complex visual layers.

### 2. Structural Breakdown

- **Data Layout**: KPIs sit in Rows 1-2, aligned above their corresponding data columns. Table headers start at Row 5, followed by data rows. Totals and Trends sit immediately below the data.
- **Formula Logic**: Uses `=TEXT(SUM(range), "format")` to generate formatted string summaries in single cells, preventing the need for complex custom cell formatting on the KPI cards.
- **Visual Design**: Gridlines disabled. KPI cells use a distinct background fill to act as "cards". Row heights and column widths are expanded for breathing room.
- **Charts/Tables**: Utilizes `SparklineGroup` to insert inline miniature trend charts at the base of each numeric column.
- **Theme Hooks**: Uses `header` for table headers and KPI values, `bg` for KPI card backgrounds, and `text` for header fonts.

### 3. Reproduction Code

