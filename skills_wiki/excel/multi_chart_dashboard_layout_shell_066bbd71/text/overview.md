### 1. High-level Skill Pattern Extraction

> **Skill Name**: Multi-Chart Dashboard Layout Shell

* **Tier**: archetype
* **Core Mechanism**: Constructs a clean, professional dashboard view by hiding gridlines, establishing a themed top header, reserving a side column for parameter controls/slicers, and positioning multiple generated charts (Stacked Bar and Line) into a structured visual grid.
* **Applicability**: Ideal for executive KPI dashboards, operational performance summaries, or any multi-chart reporting view where a polished, centralized interface is needed instead of bare data sheets.

### 2. Structural Breakdown

- **Data Layout**: Pre-aggregates metrics into a hidden "Report Data" sheet to keep the presentation layer clean.
- **Formula Logic**: Relies on openpyxl `Reference` objects linking the presentation charts directly to the hidden data blocks.
- **Visual Design**: Disables gridlines, applies a solid brand color to the top two rows (`A1:O2`) for a strong header, and adds a light gray background to Column A to denote a filter/control zone.
- **Charts/Tables**: Generates a Stacked Column chart (`BarChart(type="col", grouping="stacked")`) and two trend lines (`LineChart()`), anchoring them cleanly to exact cells (`C4`, `I4`, `I15`) with precise width and height dimensions to form a rigid layout grid.
- **Theme Hooks**: Consumes `primary` for the header banner, `text` for the dashboard title font, and `panel` for the side control panel background.

### 3. Reproduction Code

```python
def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.utils import get_column_letter

    # Simple theme fallback
    themes = {
        "corporate_blue": {"primary": "203764", "text": "FFFFFF", "panel": "F2F2F2"},
        "modern_dark": {"primary": "262626", "text": "FFFFFF", "panel": "404040"},
        "forest_green": {"primary": "2E5339", "text": "FFFFFF", "panel": "EAF0EC"}
    }
    palette = themes.get(theme, themes["corporate_blue"])

    # 1. Setup Hidden Data Sheet
    ws_data = wb.active
    ws_data.title = "Report Data"

    # Block 1: Monthly Trend (For Line Charts)
    ws_data.append(["Month", "Units Sold", "Profit"])
    monthly_data = [
        ["Jan", 500, 15000],
        ["Feb", 600, 18000],
        ["Mar", 750, 22000],
        ["Apr", 700, 21000],
        ["May", 850, 25000],
        ["Jun", 900, 28000],
    ]
    for row in monthly_data:
        ws_data.append(row)
        
    ws_data.append([]) # Spacer

    # Block 2: Market x Category (For Stacked Bar)
    row_offset = 10
    ws_data.cell(row=row_offset, column=1, value="Market")
    ws_data.cell(row=row_offset, column=2, value="Chocolate Chip")
    ws_data.cell(row=row_offset, column=3, value="Oatmeal Raisin")
    ws_data.cell(row=row_offset, column=4, value="Sugar")
    
    market_data = [
        ["India", 45000, 20000, 15000],
        ["Philippines", 30000, 18000, 12000],
        ["UK", 25000, 15000, 10000],
        ["USA", 55000, 25000, 20000],
    ]
    for i, row in enumerate(market_data, start=row_offset + 1):
        for j, val in enumerate(row, start=1):
            ws_data.cell(row=i, column=j, value=val)

    # 2. Setup Dashboard Sheet
    ws_dash = wb.create_sheet("Dashboard")
    ws_dash.sheet_view.showGridLines = False

    # Establish Layout Sizing
    ws_dash.column_dimensions['A'].width = 25  # Side panel (Slicers/Filters)
    ws_dash.column_dimensions['B'].width = 3   # Spacer column
    for col in range(3, 16):
        ws_dash.column_dimensions[get_column_letter(col)].width = 12

    # Top Header Banner
    ws_dash.merge_cells('A1:O2')
    title_cell = ws_dash['A1']
    title_cell.value = title
    title_cell.font = Font(size=24, bold=True, color=palette["text"])
    title_cell.alignment = Alignment(horizontal="left", vertical="center")
    
    header_fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    for row in ws_dash['A1:O2']:
        for cell in row:
            cell.fill = header_fill

    # Side Control Panel
    panel_fill = PatternFill(start_color=palette["panel"], end_color=palette["panel"], fill_type="solid")
    for row in range(3, 30):
        ws_dash[f'A{row}'].fill = panel_fill
        
    ws_dash['A4'].value = "Filters & Controls"
    ws_dash['A4'].font = Font(bold=True, size=12, color=palette["primary"])
    ws_dash['A4'].alignment = Alignment(horizontal="center")
    
    ws_dash['A6'].value = "[ Slicer Placeholder ]"
    ws_dash['A6'].font = Font(italic=True, color="888888")
    ws_dash['A6'].alignment = Alignment(horizontal="center")

    # 3. Create Presentation Charts
    
    # Chart A: Stacked Bar (Market x Cookie Type)
    chart_bar = BarChart()
    chart_bar.type = "col"
    chart_bar.grouping = "stacked"
    chart_bar.overlap = 100
    chart_bar.title = "Profit by Market & Product Line"
    chart_bar.y_axis.title = "Profit ($)"
    
    data_bar = Reference(ws_data, min_col=2, min_row=row_offset, max_col=4, max_row=row_offset+4)
    cats_bar = Reference(ws_data, min_col=1, min_row=row_offset+1, max_row=row_offset+4)
    chart_bar.add_data(data_bar, titles_from_data=True)
    chart_bar.set_categories(cats_bar)
    
    # Chart B: Units Sold (Line Trend)
    chart_line1 = LineChart()
    chart_line1.title = "Units Sold Each Month"
    chart_line1.style = 13
    data_line1 = Reference(ws_data, min_col=2, min_row=1, max_row=7)
    cats_line = Reference(ws_data, min_col=1, min_row=2, max_row=7)
    chart_line1.add_data(data_line1, titles_from_data=True)
    chart_line1.set_categories(cats_line)
    chart_line1.legend = None

    # Chart C: Monthly Profit (Line Trend)
    chart_line2 = LineChart()
    chart_line2.title = "Profit By Month"
    chart_line2.style = 13
    data_line2 = Reference(ws_data, min_col=3, min_row=1, max_row=7)
    chart_line2.add_data(data_line2, titles_from_data=True)
    chart_line2.set_categories(cats_line)
    chart_line2.legend = None

    # 4. Position Charts on the Dashboard Grid
    # Main visual on the left
    chart_bar.height = 14
    chart_bar.width = 18
    ws_dash.add_chart(chart_bar, "C4")
    
    # Top right secondary visual
    chart_line1.height = 7
    chart_line1.width = 14
    ws_dash.add_chart(chart_line1, "I4")
    
    # Bottom right secondary visual
    chart_line2.height = 7
    chart_line2.width = 14
    ws_dash.add_chart(chart_line2, "I15")
    
    # Present the dashboard by default, keeping raw data isolated
    ws_data.sheet_state = 'hidden'
    wb.active = ws_dash
```