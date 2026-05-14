### 1. High-level Skill Pattern Extraction

> **Skill Name**: Multi-Chart Dashboard Layout Canvas

* **Tier**: archetype
* **Core Mechanism**: Builds a complete reporting workbook consisting of a hidden data sheet and a polished interactive dashboard canvas. The dashboard features a clean, grid-free layout with a unified header, a dedicated control sidebar for slicers (controls), and a composed multi-chart grid (main stacked bar chart + supporting line charts).
* **Applicability**: Perfect for high-level management reports or KPI dashboards. It establishes the exact UI shell needed for an interactive PivotTable/Slicer dashboard without requiring VBA.

### 2. Structural Breakdown

- **Data Layout**: A hidden `DashboardData` sheet contains the underlying chart datasets.
- **Formula Logic**: Charts reference dynamic ranges from the hidden sheet via `Reference` objects.
- **Visual Design**: Gridlines are disabled to create a white "canvas". A solid `primary` color bar forms the top header. A `sidebar` column on the left is shaded light gray to house slicer controls and filters.
- **Charts/Tables**: Combines a large Stacked Bar chart (for multi-dimensional analysis like Market vs. Product) alongside two vertically stacked Line charts (for temporal trends like Sales/Profit over time).
- **Theme Hooks**: Consumes `primary` for the header banner and `sidebar` for the control panel background. `text` drives the header font color.

### 3. Reproduction Code

```python
def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.chart import BarChart, LineChart, Reference
    
    # Clean up default sheet
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])
        
    themes = {
        "corporate_blue": {"primary": "203764", "sidebar": "F2F2F2", "text": "FFFFFF"},
        "modern_dark": {"primary": "2A2A2A", "sidebar": "E0E0E0", "text": "FFFFFF"},
        "emerald": {"primary": "008A00", "sidebar": "EBF4EC", "text": "FFFFFF"}
    }
    palette = themes.get(theme, themes["corporate_blue"])
    
    # --- 1. Hidden Data Sheet ---
    dws = wb.create_sheet("DashboardData")
    dws.sheet_state = 'hidden'
    
    # Stacked bar data (Profit by Market & Cookie)
    dws.append(["Market", "Chocolate Chip", "Oatmeal Raisin", "Sugar Cookie"])
    dws.append(["United States", 125000, 85000, 60000])
    dws.append(["United Kingdom", 95000, 72000, 45000])
    dws.append(["India", 140000, 95000, 82000])
    dws.append(["Philippines", 80000, 55000, 35000])
    
    # Line chart data 1 (Units Sold)
    dws.append([])
    dws.append(["Month", "Units Sold"])
    dws.append(["Jan", 15000])
    dws.append(["Feb", 18500])
    dws.append(["Mar", 22000])
    dws.append(["Apr", 19500])
    dws.append(["May", 25000])
    
    # Line chart data 2 (Profit Trend)
    dws.append([])
    dws.append(["Month", "Profit"])
    dws.append(["Jan", 45000])
    dws.append(["Feb", 52000])
    dws.append(["Mar", 65000])
    dws.append(["Apr", 58000])
    dws.append(["May", 75000])
    
    # --- 2. Dashboard Sheet (Canvas UI) ---
    ws = wb.create_sheet("Dashboard")
    ws.sheet_view.showGridLines = False
    
    # Column widths sizing
    ws.column_dimensions['A'].width = 12
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 12
    for col in "DEFGHIJKLMN":
        ws.column_dimensions[col].width = 10
        
    # Header Banner (A1:N3)
    ws.merge_cells('A1:N3')
    header = ws['A1']
    header.value = title
    header.font = Font(size=22, bold=True, color=palette["text"])
    header.fill = PatternFill("solid", fgColor=palette["primary"])
    header.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    
    for row in ws.iter_rows(min_row=1, max_row=3, min_col=1, max_col=14):
        for cell in row:
            cell.fill = PatternFill("solid", fgColor=palette["primary"])
            
    # Sidebar for Controls (A4:C30)
    for row in ws.iter_rows(min_row=4, max_row=30, min_col=1, max_col=3):
        for cell in row:
            cell.fill = PatternFill("solid", fgColor=palette["sidebar"])
            
    # Sidebar Placeholders for Excel Slicers/Timelines
    slicer_font = Font(bold=True, color="555555")
    
    ws.merge_cells('A5:C5')
    sl1 = ws['A5']
    sl1.value = "Date Timeline"
    sl1.font = slicer_font
    sl1.alignment = Alignment(horizontal="center")
    
    ws.merge_cells('A10:C10')
    sl2 = ws['A10']
    sl2.value = "Country Filter"
    sl2.font = slicer_font
    sl2.alignment = Alignment(horizontal="center")
    
    ws.merge_cells('A16:C16')
    sl3 = ws['A16']
    sl3.value = "Product Filter"
    sl3.font = slicer_font
    sl3.alignment = Alignment(horizontal="center")
    
    # --- 3. Interactive Charts ---
    # Stacked Bar Chart (Composition)
    bar = BarChart()
    bar.type = "col"
    bar.grouping = "stacked"
    bar.overlap = 100
    bar.title = "Profit by Market & Cookie Type"
    bar.width = 16
    bar.height = 12
    bar.legend.position = "b"
    
    bar_data = Reference(dws, min_col=2, min_row=1, max_row=5, max_col=4)
    bar_cats = Reference(dws, min_col=1, min_row=2, max_row=5)
    bar.add_data(bar_data, titles_from_data=True)
    bar.set_categories(bar_cats)
    ws.add_chart(bar, "D5")
    
    # Line Chart 1 (Secondary KPI)
    line1 = LineChart()
    line1.title = "Units Sold Each Month"
    line1.width = 13
    line1.height = 6
    line1.legend = None
    
    l1_data = Reference(dws, min_col=2, min_row=7, max_row=12, max_col=2)
    l1_cats = Reference(dws, min_col=1, min_row=8, max_row=12)
    line1.add_data(l1_data, titles_from_data=True)
    line1.set_categories(l1_cats)
    ws.add_chart(line1, "J5")
    
    # Line Chart 2 (Tertiary KPI)
    line2 = LineChart()
    line2.title = "Profit Trend"
    line2.width = 13
    line2.height = 6
    line2.legend = None
    
    l2_data = Reference(dws, min_col=2, min_row=14, max_row=19, max_col=2)
    l2_cats = Reference(dws, min_col=1, min_row=15, max_row=19)
    line2.add_data(l2_data, titles_from_data=True)
    line2.set_categories(l2_cats)
    ws.add_chart(line2, "J16")
    
    wb.active = ws
```