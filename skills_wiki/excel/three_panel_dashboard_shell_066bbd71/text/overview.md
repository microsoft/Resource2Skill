### 1. High-level Skill Pattern Extraction

> **Skill Name**: Three-Panel Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a presentation-layer worksheet with a clean, grid-less layout. It embeds a hidden data sheet, generates a primary stacked column chart, and two secondary trend line charts, arranging them into a standard executive dashboard grid. It also reserves a dedicated left-hand column for interactive filters or slicers.
* **Applicability**: Best used when generating high-level summary reports that require comparing categorical performance (e.g., market by product) alongside temporal trends (e.g., monthly volume and profit). 

### 2. Structural Breakdown

- **Data Layout**: A dedicated, hidden `_Data` sheet is created to store the aggregated summary tables that feed the charts, keeping the presentation sheet clean.
- **Formula Logic**: None required; relies on structured ranges passed into standard charts. 
- **Visual Design**: Gridlines are disabled. A prominent header spans the top of the sheet, utilizing the primary theme color. A pseudo-"Control Panel" column is styled on the left to indicate where Slicers should be placed.
- **Charts/Tables**: 
  - 1x Stacked Column Chart (`BarChart` with `type="col"`, `grouping="stacked"`) for cross-sectional analysis.
  - 2x Line Charts (`LineChart`) stacked vertically for temporal trends, with legends disabled to maximize plot area.
- **Theme Hooks**: The dashboard header and control panel headers consume the primary color corresponding to the injected `theme` (falling back to corporate blue).

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference

def render_sheet(wb, sheet_name: str, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders an executive three-panel dashboard layout containing a primary stacked
    column chart and two secondary line charts, plus a reserved control panel area.
    """
    # 1. Create Dashboard Sheet
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    # Theme Setup
    theme_colors = {
        "corporate_blue": "2F5597",
        "emerald_green": "27AE60",
        "slate_gray": "708090"
    }
    bg_color = theme_colors.get(theme, "2F5597")
    
    # 2. Setup Header
    ws.merge_cells("A1:S3")
    header = ws["A1"]
    header.value = f"   {title}"
    header.font = Font(size=24, bold=True, color="FFFFFF")
    header.fill = PatternFill(start_color=bg_color, fill_type="solid")
    header.alignment = Alignment(vertical="center")
    
    # Column sizing to create the grid layout
    ws.column_dimensions['A'].width = 15
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 2   # spacer
    
    # 3. Create Hidden Data Sheet
    data_ws = wb.create_sheet(f"{sheet_name}_Data")
    data_ws.sheet_state = 'hidden'

    # Populate Data for Bar Chart
    bar_data = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Sugar", "White Macadamia"],
        ["India", 62000, 4800, 21000, 25000, 23000],
        ["United States", 36000, 6300, 22000, 9900, 32000],
        ["United Kingdom", 46000, 5200, 11000, 14000, 26000],
        ["Philippines", 54000, 7000, 22000, 8300, 24000],
        ["Malaysia", 46000, 5500, 17000, 20000, 20000]
    ]
    for row in bar_data:
        data_ws.append(row)

    # Populate Data for Line Charts
    line_data = [
        ["Month", "Units Sold", "Profit"],
        ["Sep", 50601, 124812],
        ["Oct", 95622, 228275],
        ["Nov", 65481, 160228],
        ["Dec", 52970, 136337]
    ]
    for r_idx, row in enumerate(line_data, start=10):
        for c_idx, val in enumerate(row, start=1):
            data_ws.cell(row=r_idx, column=c_idx, value=val)
            
    # 4. Generate Main Stacked Column Chart
    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    
    data1 = Reference(data_ws, min_col=2, min_row=1, max_col=6, max_row=6)
    cats1 = Reference(data_ws, min_col=1, min_row=2, max_row=6)
    chart1.add_data(data1, titles_from_data=True)
    chart1.set_categories(cats1)
    
    chart1.width = 20
    chart1.height = 13
    ws.add_chart(chart1, "D5")

    # 5. Generate Secondary Line Charts
    chart2 = LineChart()
    chart2.title = "Units sold each month"
    chart2.style = 13
    chart2.legend = None
    
    data2 = Reference(data_ws, min_col=2, min_row=10, max_col=2, max_row=14)
    cats2 = Reference(data_ws, min_col=1, min_row=11, max_row=14)
    chart2.add_data(data2, titles_from_data=True)
    chart2.set_categories(cats2)
    
    chart2.width = 14
    chart2.height = 6.2
    ws.add_chart(chart2, "N5")

    chart3 = LineChart()
    chart3.title = "Profit by month"
    chart3.style = 13
    chart3.legend = None
    
    data3 = Reference(data_ws, min_col=3, min_row=10, max_col=3, max_row=14)
    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(cats2) 
    
    chart3.width = 14
    chart3.height = 6.2
    ws.add_chart(chart3, "N13")
    
    # 6. Build Control Panel Placeholder Area (Left Column)
    ws.merge_cells("A5:B5")
    filter_header = ws["A5"]
    filter_header.value = "Control Panel"
    filter_header.font = Font(bold=True, color="FFFFFF")
    filter_header.fill = PatternFill(start_color=bg_color, fill_type="solid")
    filter_header.alignment = Alignment(horizontal="center")
    
    thin_bottom = Border(bottom=Side(style="thin", color="CCCCCC"))
    for r, label in zip([7, 11, 15], ["Date Timeline", "Country Filter", "Product Filter"]):
        ws.merge_cells(f"A{r}:B{r+2}")
        ws[f"A{r}"] = f"[ Add Slicer: {label} ]"
        ws[f"A{r}"].font = Font(color="888888", italic=True, size=9)
        ws[f"A{r}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"A{r}"].border = thin_bottom
        ws[f"B{r}"].border = thin_bottom
```