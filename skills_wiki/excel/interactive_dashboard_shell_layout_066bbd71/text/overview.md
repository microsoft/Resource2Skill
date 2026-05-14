### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive Dashboard Shell Layout

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a professional presentation layer by disabling gridlines, adding a prominent themed header banner, establishing a dedicated sidebar for filters/slicers, and arranging multiple charts (e.g., Stacked Column, Line) cleanly in the central view.
* **Applicability**: Use when aggregating multiple KPIs, PivotCharts, or summary tables into a single high-level dashboard sheet. Though `openpyxl` does not natively generate interactive Slicers, this shell provides the exact layout structure required so users can drop in Slicers and align them later.

### 2. Structural Breakdown

- **Data Layout**: Pre-aggregates plotting data into a separate, hidden `[SheetName]_Data` worksheet to keep the presentation layer completely clean.
- **Formula Logic**: N/A (Data is consumed directly by chart objects).
- **Visual Design**: Turns off native gridlines (`showGridLines = False`). Merges a large header row with bold contrasting text. Formats a left-side panel with neutral fill to visually demarcate the "control" pane from the "viewing" pane.
- **Charts/Tables**: Implements a Stacked Column chart (using `grouping="stacked"` and `overlap=100`) to show composition, alongside Line charts to show trends over time. Legends are selectively hidden on line charts to mimic the video's clean aesthetics.
- **Theme Hooks**: Consumes `header_bg` (main brand color), `header_fg` (text contrast), and `sidebar_bg` (subtle neutral).

### 3. Reproduction Code

```python
def render_sheet(wb, sheet_name: str, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import PatternFill, Font, Alignment
    from openpyxl.chart import BarChart, LineChart, Reference
    
    # 1. Theme Configuration
    themes = {
        "corporate_blue": {"header_bg": "203764", "header_fg": "FFFFFF", "sidebar_bg": "F2F2F2"},
        "dark_mode": {"header_bg": "000000", "header_fg": "FFFFFF", "sidebar_bg": "333333"},
        "emerald": {"header_bg": "0F52BA", "header_fg": "FFFFFF", "sidebar_bg": "E8F4F8"}
    }
    palette = themes.get(theme, themes["corporate_blue"])
    
    # 2. Setup Hidden Data Sheet for Charts
    data_sheet_name = f"{sheet_name}_Data"
    data_ws = wb.create_sheet(data_sheet_name)
    data_ws.sheet_state = 'hidden'
    
    # Chart 1 Data (Rows 1-5, Cols 1-4)
    chart1_data = [
        ["Market", "Chocolate Chip", "Sugar", "Fortune Cookie"],
        ["India", 62000, 23000, 4800],
        ["Philippines", 54000, 24000, 7000],
        ["United Kingdom", 46000, 26000, 7000],
        ["United States", 36000, 32000, 5500]
    ]
    for row in chart1_data:
        data_ws.append(row)
        
    # Chart 2 Data (Rows 1-5, Cols 6-7)
    chart2_data = [
        ["Month", "Units Sold"],
        ["Sep", 50601],
        ["Oct", 95622],
        ["Nov", 65481],
        ["Dec", 52970]
    ]
    for i, row in enumerate(chart2_data, 1):
        data_ws.cell(row=i, column=6, value=row[0])
        data_ws.cell(row=i, column=7, value=row[1])
        
    # Chart 3 Data (Rows 1-5, Cols 8-9)
    chart3_data = [
        ["Month", "Profit"],
        ["Sep", 124812],
        ["Oct", 228275],
        ["Nov", 160228],
        ["Dec", 136337]
    ]
    for i, row in enumerate(chart3_data, 1):
        data_ws.cell(row=i, column=8, value=row[0])
        data_ws.cell(row=i, column=9, value=row[1])
        
    # 3. Setup Presentation Dashboard Sheet
    ws = wb[sheet_name] if sheet_name in wb.sheetnames else wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    # Layout adjustments
    ws.row_dimensions[1].height = 10
    ws.row_dimensions[2].height = 30
    ws.row_dimensions[3].height = 10
    ws.column_dimensions['A'].width = 12
    ws.column_dimensions['B'].width = 12
    
    # Header Banner Setup
    ws.merge_cells("A1:Q3")
    header_cell = ws["A1"]
    header_cell.value = title
    header_cell.font = Font(size=22, bold=True, color=palette["header_fg"])
    header_cell.fill = PatternFill("solid", fgColor=palette["header_bg"])
    header_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # Sidebar Pane Setup
    sidebar_fill = PatternFill("solid", fgColor=palette["sidebar_bg"])
    sidebar_font = Font(bold=True, color="595959")
    ws.merge_cells("A4:B4")
    sidebar_title = ws["A4"]
    sidebar_title.value = "Filters & Controls"
    sidebar_title.font = sidebar_font
    sidebar_title.alignment = Alignment(horizontal="center", vertical="center")
    
    for row in range(4, 30):
        for col in range(1, 3):
            ws.cell(row=row, column=col).fill = sidebar_fill
            
    ws.merge_cells("A6:B6")
    placeholder = ws["A6"]
    placeholder.value = "[ Insert Slicers Here ]"
    placeholder.font = Font(italic=True, color="A6A6A6")
    placeholder.alignment = Alignment(horizontal="center")
    
    # 4. Initialize and Place Charts
    # Chart 1: Stacked Column (Profit by Market)
    c1 = BarChart()
    c1.type = "col"
    c1.style = 10
    c1.grouping = "stacked"
    c1.overlap = 100
    c1.title = "Profit by Market & Cookie Type"
    data1 = Reference(data_ws, min_col=2, min_row=1, max_row=5, max_col=4)
    cats1 = Reference(data_ws, min_col=1, min_row=2, max_row=5)
    c1.add_data(data1, titles_from_data=True)
    c1.set_categories(cats1)
    c1.height = 13
    c1.width = 16
    ws.add_chart(c1, "D5")
    
    # Chart 2: Line (Units Sold)
    c2 = LineChart()
    c2.title = "Units sold each month"
    c2.style = 13
    data2 = Reference(data_ws, min_col=7, min_row=1, max_row=5)
    cats2 = Reference(data_ws, min_col=6, min_row=2, max_row=5)
    c2.add_data(data2, titles_from_data=True)
    c2.set_categories(cats2)
    c2.height = 8.5
    c2.width = 12
    c2.legend = None
    ws.add_chart(c2, "K5")
    
    # Chart 3: Line (Profit Trend)
    c3 = LineChart()
    c3.title = "Profit by month"
    c3.style = 13
    data3 = Reference(data_ws, min_col=9, min_row=1, max_row=5)
    cats3 = Reference(data_ws, min_col=8, min_row=2, max_row=5)
    c3.add_data(data3, titles_from_data=True)
    c3.set_categories(cats3)
    c3.height = 8.5
    c3.width = 12
    c3.legend = None
    ws.add_chart(c3, "K15")
```