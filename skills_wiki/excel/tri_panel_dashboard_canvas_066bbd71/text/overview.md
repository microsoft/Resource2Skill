### 1. High-level Skill Pattern Extraction

> **Skill Name**: Tri-Panel Dashboard Canvas

* **Tier**: sheet_shell
* **Core Mechanism**: Generates a clean, interactive-style dashboard canvas by disabling gridlines, adding a unified theme banner, and strictly positioning pre-aggregated data into a tri-panel chart grid. A separate, hidden "Data" worksheet is automatically generated to isolate raw chart data from the visual dashboard.
* **Applicability**: Best used for executive summaries or performance overviews where a primary metric (stacked column) must be compared against secondary time-series metrics (line charts) on a single screen. 

### 2. Structural Breakdown

- **Data Layout**: A hidden worksheet (`{sheet_name}_Data`) is created to cleanly host the series data for the charts, avoiding clutter on the main dashboard surface. 
- **Formula Logic**: N/A (Relies on data supplied directly to the shell's panel dictionaries).
- **Visual Design**: Gridlines are hidden (`ws.sheet_view.showGridLines = False`). A continuous, solid-colored banner spanning columns A through R establishes the visual hierarchy, styled using the theme's primary color and contrasting text.
- **Charts/Tables**: 
  - Main Panel: Stacked Bar Chart (`grouping="stacked"`, `overlap=100`), anchored at `B5` (width 18cm, height 12cm).
  - Secondary Panels: Two Line Charts, stacked vertically, anchored at `L5` and `L12` (width 12cm, height 5.5cm).
- **Theme Hooks**: Consumes `primary` for the banner background and `text_on_primary` for the header text font.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart, Reference

def _get_theme(theme_name: str) -> dict:
    """Standard theme palette fallback."""
    themes = {
        "corporate_blue": {"primary": "2F5597", "secondary": "D9E1F2", "text_on_primary": "FFFFFF"},
        "midnight": {"primary": "203764", "secondary": "8FAADC", "text_on_primary": "FFFFFF"},
        "emerald": {"primary": "385723", "secondary": "E2EFDA", "text_on_primary": "FFFFFF"}
    }
    return themes.get(theme_name, themes["corporate_blue"])

def render_sheet(wb, sheet_name: str, *, 
                 title: str, 
                 main_panel: dict, 
                 top_right_panel: dict, 
                 bottom_right_panel: dict, 
                 theme: str = "corporate_blue", 
                 **kwargs) -> None:
    """
    Renders a 3-panel dashboard using pre-aggregated data.
    
    Expected panel structure:
    {
        "title": "Profit by Market & Cookie Type",
        "categories": ["India", "Philippines", "UK", "USA"],
        "series": {
            "Chocolate Chip": [62349, 54618, 46530, 36657],
            "Sugar": [18560, 14947, 19446, 9186]
        }
    }
    """
    # 1. Setup Dashboard Sheet
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    palette = _get_theme(theme)
    
    # 2. Header Banner
    ws.merge_cells("A1:R3")
    title_cell = ws["A1"]
    title_cell.value = title
    title_cell.font = Font(size=24, bold=True, color=palette["text_on_primary"])
    title_cell.fill = PatternFill(start_color=palette["primary"], fill_type="solid")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # 3. Setup Hidden Data Sheet
    data_sheet_name = f"{sheet_name}_Data"
    if data_sheet_name in wb.sheetnames:
        del wb[data_sheet_name]
    ws_data = wb.create_sheet(data_sheet_name)
    ws_data.sheet_state = "hidden"
    
    current_row = 1
    
    def build_chart(chart_type: str, panel: dict, start_row: int):
        """Helper to write data to the hidden sheet and configure a chart."""
        # Write Headers
        ws_data.cell(row=start_row, column=1, value="Category")
        series_names = list(panel["series"].keys())
        for col_idx, s_name in enumerate(series_names, start=2):
            ws_data.cell(row=start_row, column=col_idx, value=s_name)
            
        # Write Values
        categories = panel["categories"]
        for row_idx, cat in enumerate(categories, start=start_row + 1):
            ws_data.cell(row=row_idx, column=1, value=cat)
            for col_idx, s_name in enumerate(series_names, start=2):
                val = panel["series"][s_name][row_idx - start_row - 1]
                ws_data.cell(row=row_idx, column=col_idx, value=val)
                
        # Configure Chart
        if chart_type == "stacked_column":
            chart = BarChart()
            chart.type = "col"
            chart.grouping = "stacked"
            chart.overlap = 100
        else:
            chart = LineChart()
            
        chart.title = panel.get("title", "")
        
        # Link Data
        data_ref = Reference(ws_data, min_col=2, min_row=start_row, 
                             max_col=1 + len(series_names), max_row=start_row + len(categories))
        cats_ref = Reference(ws_data, min_col=1, min_row=start_row + 1, 
                             max_row=start_row + len(categories))
        
        chart.add_data(data_ref, titles_from_data=True)
        chart.set_categories(cats_ref)
        chart.style = 13  # Clean built-in Excel chart style
        
        return chart, start_row + len(categories) + 2

    # 4. Construct and Position Main Chart
    main_chart, current_row = build_chart("stacked_column", main_panel, current_row)
    main_chart.width = 18
    main_chart.height = 12
    ws.add_chart(main_chart, "B5")
    
    # 5. Construct and Position Top-Right Chart
    tr_chart, current_row = build_chart("line", top_right_panel, current_row)
    tr_chart.width = 12
    tr_chart.height = 5.5
    ws.add_chart(tr_chart, "L5")
    
    # 6. Construct and Position Bottom-Right Chart
    br_chart, current_row = build_chart("line", bottom_right_panel, current_row)
    br_chart.width = 12
    br_chart.height = 5.5
    ws.add_chart(br_chart, "L12")
```