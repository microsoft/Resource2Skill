### 1. High-level Skill Pattern Extraction

> **Skill Name**: Sidebar KPI Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Sets up a modern dashboard layout by contrasting a dark-colored left sidebar for Key Performance Indicators (KPIs) against a light-colored main canvas for charts. It disables gridlines and relies on cell-fill blocks with distinct typography to create an application-like interface entirely within native Excel cells.
* **Applicability**: Ideal for executive summaries, reporting dashboards, or any scenario where 4-6 primary high-level metrics need to be consistently visible alongside detailed trend charts or data tables.

### 2. Structural Breakdown

- **Data Layout**: Columns A-C are reserved for the sidebar (Column B holds the KPI content, A and C act as padding margins). Columns D-Z provide the main reporting canvas. Chart data is placed off-screen (e.g., Column AA).
- **Formula Logic**: Purely layout and presentation-driven; expects pre-aggregated values or external formula links to be passed into the KPI slots.
- **Visual Design**: Removes sheet gridlines. The sidebar uses the theme's `primary` color with `text_light` typography. KPI values are heavily weighted (size 22, bold) to establish a clear visual hierarchy over the italicized labels.
- **Charts/Tables**: Includes a clean, borderless Bar Chart in the main canvas as a placeholder for visual reporting.
- **Theme Hooks**: Consumes `primary` (sidebar fill), `bg` (main canvas fill), `text_light` (sidebar typography), and `text` (main title typography).

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, Reference

def render_sheet(wb, sheet_name: str, *, title: str = "Executive Dashboard", kpis: list = None, theme: str = "corporate_blue", **kwargs) -> None:
    # Safely load theme palette
    try:
        from _helpers import get_theme
        palette = get_theme(theme)
    except ImportError:
        palette = {
            "primary": "1F4E5B",
            "bg": "F4F6F9",
            "text": "1A1A1A",
            "text_light": "FFFFFF",
            "accent": "E63946"
        }
        
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    if kpis is None:
        kpis = [
            {"label": "Total Sales", "value": "$649.0k"},
            {"label": "Orders", "value": "2,400"},
            {"label": "Avg Rating", "value": "4.0"},
            {"label": "Days to Ship", "value": "2.3"},
        ]
        
    # Strip any potential hex hashes for OpenPyXL compatibility
    dark_fill = PatternFill(start_color=palette.get("primary", "1F4E5B").replace("#", ""), fill_type="solid")
    light_fill = PatternFill(start_color=palette.get("bg", "F4F6F9").replace("#", ""), fill_type="solid")
    
    # Paint background regions (Rows 1-50 ensures full screen coverage for most monitors)
    # A1:C50 acts as the dark sidebar; D1:Z50 is the light main canvas
    for r in range(1, 51):
        for c in range(1, 4):
            ws.cell(row=r, column=c).fill = dark_fill
        for c in range(4, 27):
            ws.cell(row=r, column=c).fill = light_fill
            
    # Configure precise column widths to create margins
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 22
    ws.column_dimensions['C'].width = 3
    ws.column_dimensions['D'].width = 4
    
    # Render Main Dashboard Title
    title_cell = ws.cell(row=2, column=5, value=title)
    title_cell.font = Font(size=24, bold=True, color=palette.get("text", "1A1A1A").replace("#", ""))
    
    # Place KPI blocks in the Sidebar
    current_row = 5
    label_font = Font(size=11, color=palette.get("text_light", "FFFFFF").replace("#", ""), italic=True)
    value_font = Font(size=22, bold=True, color=palette.get("text_light", "FFFFFF").replace("#", ""))
    align_center = Alignment(horizontal="center", vertical="center")
    
    for kpi in kpis:
        # KPI Label
        lbl_cell = ws.cell(row=current_row, column=2, value=kpi["label"])
        lbl_cell.font = label_font
        lbl_cell.alignment = align_center
        
        # KPI Value
        val_cell = ws.cell(row=current_row + 1, column=2, value=kpi["value"])
        val_cell.font = value_font
        val_cell.alignment = align_center
        
        # Space out cards evenly
        current_row += 4
        
    # Inject off-canvas sample chart data
    chart_data = [
        ["Month", "Revenue"],
        ["Jan", 112000],
        ["Feb", 134000],
        ["Mar", 128000],
        ["Apr", 145000],
        ["May", 130000],
    ]
    
    for r_idx, row_data in enumerate(chart_data, start=1):
        for c_idx, val in enumerate(row_data, start=27): # Columns AA and AB
            ws.cell(row=r_idx, column=c_idx, value=val)
            
    # Render main visualization on the canvas
    chart = BarChart()
    chart.title = "Revenue by Month"
    data = Reference(ws, min_col=28, min_row=1, max_row=6)
    cats = Reference(ws, min_col=27, min_row=2, max_row=6)
    
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    
    # Clean chart design parameters
    chart.height = 11
    chart.width = 18
    chart.legend = None 
    
    ws.add_chart(chart, "E6")
```