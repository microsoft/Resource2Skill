### 1. High-level Skill Pattern Extraction

> **Skill Name**: Clean Interactive Dashboard Archetype

* **Tier**: archetype
* **Core Mechanism**: Builds a multi-sheet workbook separating data from presentation. The presentation sheet ("Dashboard") strips away gridlines, establishes a strong branded title banner, and arranges charts and slicer placeholder regions into a clean, grid-based layout. The data sheet is hidden, acting as a calculation/cache layer.
* **Applicability**: Ideal for executive summaries, financial reports, or high-level project dashboards. Use this archetype when you need to present aggregated KPIs and trends in a clean, presentation-ready layout without the visual clutter of gridlines or raw data tables.

### 2. Structural Breakdown

- **Data Layout**: Places raw data in a secondary, hidden `ChartData` worksheet to act as the chart/pivot cache, keeping the main dashboard pristine.
- **Formula Logic**: Uses openpyxl `Reference` objects to tie the presentation layer charts back to the hidden data sheet.
- **Visual Design**: Disables worksheet gridlines via `ws.sheet_view.showGridLines = False`. Constructs a large merged header (`A1:T4`) acting as the dashboard banner, colored heavily with the primary brand color. Sets up a visual "left rail" column for interactive controls (Slicers/Timelines).
- **Charts/Tables**: Deploys a main Stacked Column chart for categorical breakdown, and two vertically stacked Line charts for time-series trends. Removes gridlines and redundant legends on charts for a cleaner UI.
- **Theme Hooks**: Consumes `primary` for the top banner background, `text` for the banner title, and `slicer_bg` / `border` for the interactive control placeholders on the left rail.

### 3. Reproduction Code

```python
def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

    # Standard theme palette fallback
    colors = {
        "corporate_blue": {"primary": "1F4E78", "text": "FFFFFF", "border": "CCCCCC", "slicer_bg": "F2F2F2"},
        "midnight": {"primary": "203764", "text": "FFFFFF", "border": "595959", "slicer_bg": "D9D9D9"}
    }
    palette = colors.get(theme, colors["corporate_blue"])

    # 1. Setup Data Sheet (Hidden Cache)
    ws_data = wb.active
    ws_data.title = "ChartData"
    ws_data.sheet_state = 'hidden'
    
    # Table 1: Stacked Column Data (Profit by Market & Product)
    data1 = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin"],
        ["India", 62000, 4800, 21000],
        ["United States", 36000, 6300, 22000],
        ["United Kingdom", 46000, 5200, 11000],
        ["Philippines", 54000, 7000, 22000],
    ]
    for r in data1:
        ws_data.append(r)
        
    # Table 2: Line 1 Data (Units)
    ws_data.append([]) # spacer row 7
    data2 = [
        ["Month", "Units Sold"],
        ["Sep", 50000],
        ["Oct", 95000],
        ["Nov", 65000],
        ["Dec", 52000],
    ]
    for r in data2:
        ws_data.append(r)
        
    # Table 3: Line 2 Data (Profit)
    ws_data.append([]) # spacer row 14
    data3 = [
        ["Month", "Profit"],
        ["Sep", 124000],
        ["Oct", 228000],
        ["Nov", 160000],
        ["Dec", 136000],
    ]
    for r in data3:
        ws_data.append(r)

    # 2. Setup Dashboard Sheet (Presentation Layer)
    ws_dash = wb.create_sheet("Dashboard")
    ws_dash.sheet_view.showGridLines = False

    # Title Banner
    ws_dash.merge_cells("A1:T4")
    title_cell = ws_dash["A1"]
    title_cell.value = title
    
    banner_fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    banner_font = Font(color=palette["text"], size=24, bold=True)
    banner_align = Alignment(horizontal="center", vertical="center")
    
    for row in ws_dash.iter_rows(min_row=1, max_row=4, min_col=1, max_col=20):
        for cell in row:
            cell.fill = banner_fill
            
    title_cell.font = banner_font
    title_cell.alignment = banner_align

    # 3. Create Slicer Placeholders (Left Rail)
    thin_border = Border(left=Side(style='thin', color=palette["border"]),
                         right=Side(style='thin', color=palette["border"]),
                         top=Side(style='thin', color=palette["border"]),
                         bottom=Side(style='thin', color=palette["border"]))
    slicer_fill = PatternFill(start_color=palette["slicer_bg"], end_color=palette["slicer_bg"], fill_type="solid")
    
    def make_slicer_placeholder(ws, range_str, text):
        ws.merge_cells(range_str)
        cell = ws[range_str.split(":")[0]]
        cell.value = text
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.font = Font(color="555555", italic=True)
        for r in ws[range_str]:
            for c in r:
                c.fill = slicer_fill
                c.border = thin_border

    make_slicer_placeholder(ws_dash, "A6:C10", "Date Timeline Slicer")
    make_slicer_placeholder(ws_dash, "A12:C16", "Country Slicer")
    make_slicer_placeholder(ws_dash, "A18:C22", "Product Slicer")

    # 4. Create Charts
    # Chart 1: Main Stacked Bar (Center Grid)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    
    data_ref1 = Reference(ws_data, min_col=2, min_row=1, max_col=4, max_row=5)
    cats_ref1 = Reference(ws_data, min_col=1, min_row=2, max_row=5)
    chart1.add_data(data_ref1, titles_from_data=True)
    chart1.set_categories(cats_ref1)
    chart1.width = 15
    chart1.height = 10
    chart1.y_axis.majorGridlines = None
    ws_dash.add_chart(chart1, "E6")

    # Chart 2: Top Line Chart (Right Grid)
    chart2 = LineChart()
    chart2.title = "Units sold each month"
    chart2.legend = None
    data_ref2 = Reference(ws_data, min_col=2, min_row=8, max_col=2, max_row=12)
    cats_ref2 = Reference(ws_data, min_col=1, min_row=9, max_row=12)
    chart2.add_data(data_ref2, titles_from_data=True)
    chart2.set_categories(cats_ref2)
    chart2.width = 12
    chart2.height = 5
    chart2.y_axis.majorGridlines = None
    ws_dash.add_chart(chart2, "N6")

    # Chart 3: Bottom Line Chart (Right Grid)
    chart3 = LineChart()
    chart3.title = "Profit by month"
    chart3.legend = None
    data_ref3 = Reference(ws_data, min_col=2, min_row=15, max_col=2, max_row=19)
    cats_ref3 = Reference(ws_data, min_col=1, min_row=16, max_row=19)
    chart3.add_data(data_ref3, titles_from_data=True)
    chart3.set_categories(cats_ref3)
    chart3.width = 12
    chart3.height = 5
    chart3.y_axis.majorGridlines = None
    ws_dash.add_chart(chart3, "N13")
```