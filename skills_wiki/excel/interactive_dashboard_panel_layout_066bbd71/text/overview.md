### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive Dashboard Panel Layout

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a clean, professional dashboard view by turning off gridlines, establishing a thick styled title banner, positioning multiple coordinated charts alongside each other, and using formatted cells to emulate a left-hand control panel (slicer area).
* **Applicability**: Use this when generating management reports or summary views where multiple charts need to be consumed together. Because `openpyxl` lacks native support for creating interactive Pivot Slicers from scratch, this pattern constructs the exact visual layout (including mock slicer UI panels) using standard charts linked to a hidden aggregated data sheet.

### 2. Structural Breakdown

- **Data Layout**: A separate hidden worksheet (`<SheetName>_Data`) stores the aggregated pivot tables. This keeps the presentation layer perfectly clean.
- **Visual Design**: Gridlines are hidden. A large, merged banner spans the top rows. The left column uses light blue shading and thin borders to create "Slicer" panels. 
- **Charts/Tables**: Contains a primary `BarChart` (Stacked Column) taking up the main central area, and two smaller `LineChart` objects stacked vertically on the right flank to show trend over time.
- **Theme Hooks**: Uses the primary corporate color (`header_bg`) for the top banner. Slicer UI uses light blue accents (`slicer_header_bg`, `slicer_selected_bg`) which can be overridden via palette.

### 3. Reproduction Code

```python
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def render_sheet(wb, sheet_name: str, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a multi-chart dashboard layout with a control sidebar and a bold header.
    """
    # 1. Theme Configuration (Fallback to Corporate Blue scheme)
    header_bg = kwargs.get("header_bg", "203764")
    header_fg = kwargs.get("header_fg", "FFFFFF")
    slicer_hdr_bg = kwargs.get("slicer_hdr_bg", "DDEBF7")
    slicer_hdr_fg = kwargs.get("slicer_hdr_fg", "1F4E78")
    slicer_sel_bg = kwargs.get("slicer_sel_bg", "9BC2E6")
    slicer_unsel_bg = kwargs.get("slicer_unsel_bg", "FFFFFF")
    slicer_border_color = kwargs.get("slicer_border_color", "B4C6E7")
    
    # 2. Setup Hidden Data Sheet for Chart Aggregations
    data_ws = wb.create_sheet(f"{sheet_name}_Data")
    data_ws.sheet_state = 'hidden'
    
    market_data = [
        ["Market", "Choc Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle", "Sugar"],
        ["India", 60000, 5000, 20000, 25000, 18000],
        ["Malaysia", 45000, 6000, 15000, 20000, 10000],
        ["Philippines", 50000, 7000, 22000, 8000, 14000],
        ["United Kingdom", 40000, 5000, 11000, 14000, 19000],
        ["United States", 35000, 6000, 20000, 10000, 9000]
    ]
    
    month_data = [
        ["Month", "Units Sold", "Profit"],
        ["Jan", 50000, 120000], ["Feb", 45000, 110000],
        ["Mar", 60000, 150000], ["Apr", 55000, 130000],
        ["May", 70000, 180000], ["Jun", 65000, 160000],
        ["Jul", 80000, 200000], ["Aug", 95000, 220000],
        ["Sep", 50000, 124000], ["Oct", 95000, 228000],
        ["Nov", 65000, 160000], ["Dec", 52000, 136000],
    ]
    
    for r_idx, row in enumerate(market_data, 1):
        for c_idx, val in enumerate(row, 1):
            data_ws.cell(row=r_idx, column=c_idx, value=val)

    for r_idx, row in enumerate(month_data, 1):
        for c_idx, val in enumerate(row, 8):
            data_ws.cell(row=r_idx, column=c_idx, value=val)

    # 3. Initialize Presentation Dashboard
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    # Structure column widths
    ws.column_dimensions['A'].width = 2
    ws.column_dimensions['B'].width = 22
    for col in "CDEFGHIJKLM":
        ws.column_dimensions[col].width = 11

    # Main Dashboard Title Banner
    ws.merge_cells("B2:M4")
    title_cell = ws["B2"]
    title_cell.value = title
    title_cell.font = Font(size=24, bold=True, color=header_fg)
    title_cell.fill = PatternFill(start_color=header_bg, fill_type="solid")
    title_cell.alignment = Alignment(vertical="center", indent=1)
    
    # 4. Generate UI Panel (Mock Slicers using cell formatting)
    thin = Side(border_style="thin", color=slicer_border_color)
    slicer_border = Border(top=thin, left=thin, right=thin, bottom=thin)
    
    def draw_mock_slicer(start_row, title, items, selected_indices):
        ws.cell(row=start_row, column=2, value=title).fill = PatternFill(start_color=slicer_hdr_bg, fill_type="solid")
        ws.cell(row=start_row, column=2).font = Font(color=slicer_hdr_fg, bold=True)
        ws.cell(row=start_row, column=2).border = slicer_border
        ws.cell(row=start_row, column=2).alignment = Alignment(indent=1)
        
        for idx, item in enumerate(items):
            cell = ws.cell(row=start_row + 1 + idx, column=2, value=item)
            cell.border = slicer_border
            cell.alignment = Alignment(indent=2)
            if idx in selected_indices:
                cell.fill = PatternFill(start_color=slicer_sel_bg, fill_type="solid")
                cell.font = Font(bold=True)
            else:
                cell.fill = PatternFill(start_color=slicer_unsel_bg, fill_type="solid")
    
    draw_mock_slicer(6, "Market", ["India", "Malaysia", "Philippines", "United Kingdom", "United States"], [0, 4])
    draw_mock_slicer(13, "Product", ["Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle", "Sugar"], [0, 2, 3])
    
    # 5. Insert Charts
    # Chart 1: Profit by Market (Stacked Bar)
    c1 = BarChart()
    c1.type = "col"
    c1.style = 10
    c1.grouping = "stacked"
    c1.overlap = 100
    c1.title = "Profit by Market & Cookie Type"
    c1_data = Reference(data_ws, min_col=2, min_row=1, max_col=6, max_row=6)
    c1_cats = Reference(data_ws, min_col=1, min_row=2, max_row=6)
    c1.add_data(c1_data, titles_from_data=True)
    c1.set_categories(c1_cats)
    c1.height = 13.5
    c1.width = 15.5
    ws.add_chart(c1, "C6")
    
    # Chart 2: Units Sold Trend (Line)
    c2 = LineChart()
    c2.title = "Units sold each month"
    c2.style = 13
    c2_data = Reference(data_ws, min_col=9, min_row=1, max_row=13)
    c2_cats = Reference(data_ws, min_col=8, min_row=2, max_row=13)
    c2.add_data(c2_data, titles_from_data=True)
    c2.set_categories(c2_cats)
    c2.height = 6.5
    c2.width = 14.5
    c2.legend = None
    ws.add_chart(c2, "I6")
    
    # Chart 3: Profit Trend (Line)
    c3 = LineChart()
    c3.title = "Profit by month"
    c3.style = 13
    c3_data = Reference(data_ws, min_col=10, min_row=1, max_row=13)
    c3_cats = Reference(data_ws, min_col=8, min_row=2, max_row=13)
    c3.add_data(c3_data, titles_from_data=True)
    c3.set_categories(c3_cats)
    c3.height = 6.5
    c3.width = 14.5
    c3.legend = None
    ws.add_chart(c3, "I13")
```