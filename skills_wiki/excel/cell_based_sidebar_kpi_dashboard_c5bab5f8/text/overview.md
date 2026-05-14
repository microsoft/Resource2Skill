### 1. High-level Skill Pattern Extraction

> **Skill Name**: Cell-based Sidebar KPI Dashboard

* **Tier**: sheet_shell
* **Core Mechanism**: Emulates a modern "sidebar" UI layout purely through Excel grid mechanics. It dedicates the leftmost columns as a dark-themed summary panel for large KPI figures, leaving the rightward columns as a light-themed canvas for data and charts. This approach completely avoids the fragility and positioning issues of floating shapes and text boxes.
* **Applicability**: Perfect for executive summaries and high-level dashboards where 3-5 key metrics need to be permanently visible alongside supporting trend charts.

### 2. Structural Breakdown

- **Data Layout**: Columns A-B act as the sidebar (A is a visual margin, B holds text content). Columns C-Z act as the main analytical canvas. KPIs are stacked vertically in column B.
- **Formula Logic**: Static injection for the presentation layer; formatting relies heavily on explicit cell `.number_format` strings (e.g., `#,##0` or `$#,##0`).
- **Visual Design**: Disables worksheet gridlines. Uses highly contrasting `PatternFill` backgrounds to split the screen visually. KPIs utilize large, bold fonts to stand out against the dark sidebar background.
- **Charts/Tables**: Includes a dynamic LineChart anchored in the main canvas, referencing a structured data table placed adjacent to it. 
- **Theme Hooks**: Consumes `sidebar_bg`, `sidebar_fg`, `main_bg`, `accent`, and `text` to ensure the layout has high contrast and matches corporate branding.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import LineChart, Reference

def render_sheet(
    wb, 
    sheet_name: str, 
    *, 
    title: str = "Sales Dashboard", 
    kpis: list = None, 
    trend_data: list = None, 
    theme: str = "corporate_blue", 
    **kwargs
) -> None:
    """
    Renders a complete dashboard sheet featuring a prominent left sidebar for KPIs 
    and a main canvas area for charts and supporting data.
    """
    # 1. Provide realistic default data if none is supplied
    if kpis is None:
        kpis = [
            {"label": "🛒 Total Orders", "value": 2400, "fmt": "#,##0"},
            {"label": "💰 Gross Revenue", "value": 649000, "fmt": "$#,##0"},
            {"label": "⭐ Avg Rating", "value": 4.2, "fmt": "0.0"}
        ]
    if trend_data is None:
        trend_data = [
            ("Month", "Revenue"),
            ("Jan", 150000),
            ("Feb", 220000),
            ("Mar", 279000),
            ("Apr", 310000)
        ]

    # 2. Setup Worksheet & Theme
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)
        
    ws.sheet_view.showGridLines = False
        
    themes = {
        "corporate_blue": {"sidebar_bg": "1E3A8A", "sidebar_fg": "FFFFFF", "main_bg": "F8FAFC", "accent": "3B82F6", "text": "1F2937"},
        "viva_green": {"sidebar_bg": "14532D", "sidebar_fg": "F0FDF4", "main_bg": "ECFDF5", "accent": "10B981", "text": "064E3B"}
    }
    palette = themes.get(theme, themes["corporate_blue"])
    
    side_fill = PatternFill("solid", fgColor=palette["sidebar_bg"])
    main_fill = PatternFill("solid", fgColor=palette["main_bg"])
    
    # 3. Grid Structure
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 25
    ws.column_dimensions['C'].width = 3
    ws.column_dimensions['D'].width = 15
    ws.column_dimensions['E'].width = 15
    
    # Paint the background canvas
    for row in range(1, 45):
        for col in range(1, 20):
            cell = ws.cell(row=row, column=col)
            cell.fill = side_fill if col <= 2 else main_fill
            
    # 4. Inject Sidebar Content
    title_cell = ws['B2']
    title_cell.value = title
    title_cell.font = Font(name="Arial", size=22, bold=True, color=palette["sidebar_fg"])
    
    start_row = 6
    for kpi in kpis:
        val_cell = ws.cell(row=start_row, column=2)
        val_cell.value = kpi["value"]
        val_cell.number_format = kpi.get("fmt", "#,##0")
        val_cell.font = Font(name="Arial", size=18, bold=True, color=palette["sidebar_fg"])
        
        lbl_cell = ws.cell(row=start_row+1, column=2)
        lbl_cell.value = kpi["label"]
        lbl_cell.font = Font(name="Arial", size=11, color=palette["sidebar_fg"])
        
        start_row += 4
        
    # 5. Inject Main Canvas Data Table
    ws['D3'].value = "Underlying Data"
    ws['D3'].font = Font(size=14, bold=True, color=palette["text"])
    
    for r_idx, row_data in enumerate(trend_data, start=5):
        for c_idx, val in enumerate(row_data, start=4):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(color=palette["text"])
            
            # Style header row
            if r_idx == 5: 
                cell.font = Font(bold=True, color=palette["sidebar_fg"])
                cell.fill = PatternFill("solid", fgColor=palette["accent"])
                
    # 6. Inject Main Canvas Chart
    chart = LineChart()
    chart.title = "Revenue Trend Analysis"
    chart.style = 13
    chart.height = 10
    chart.width = 16
    
    data_ref = Reference(ws, min_col=5, min_row=5, max_row=4 + len(trend_data))
    cats_ref = Reference(ws, min_col=4, min_row=6, max_row=4 + len(trend_data))
    
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    
    # Format the chart series to match the theme accent
    series = chart.series[0]
    series.graphicalProperties.line.solidFill = palette["accent"]
    series.graphicalProperties.line.width = 30000  # 3pt width
    chart.legend = None
    
    ws.add_chart(chart, "G5")
```