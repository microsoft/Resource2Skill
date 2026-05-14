### 1. High-level Skill Pattern Extraction

> **Skill Name**: Clean Static Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Generates a presentation-ready dashboard worksheet by disabling gridlines/headers, establishing a prominent themed title banner, and precisely positioning multiple `openpyxl` charts (Stacked Column and Line) mapped to a hidden backend data sheet. 
* **Applicability**: Best for rendering aggregate metrics and visual summaries suitable for executive reporting or PDF exports where interactive features (like Slicers) are not required or supported.

### 2. Structural Breakdown

- **Data Layout**: A hidden companion worksheet (`{sheet_name}_Backend`) is generated to hold the summary matrices and time-series arrays that feed the charts, keeping the presentation layer clean.
- **Formula Logic**: Directly writes static aggregated values. Real-world applications would inject dynamic values or summary formulas into the backend sheet.
- **Visual Design**: Uses `ws.sheet_view.showGridLines = False` and `ws.sheet_view.showRowColHeaders = False` for a polished "canvas" feel. The banner spans `A1:Q3` with a solid fill and centered, bold text.
- **Charts/Tables**: 
  - **Stacked Column**: `BarChart(type="col", grouping="stacked", overlap=100)` for market breakdown.
  - **Lines**: `LineChart()` for time-series trend analysis. 
  - Number formats are mapped securely by applying Excel formats (`"$"#,##0`) directly to backend data cells which the charts inherit.
- **Theme Hooks**: The title banner's background color and text color dynamically map to `primary` and `text` properties of the selected theme palette.

### 3. Reproduction Code

```python
def render_sheet(wb, sheet_name: str, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.chart import BarChart, LineChart, Reference
    
    # 1. Theme Configuration
    themes = {
        "corporate_blue": {"primary": "203764", "text": "FFFFFF"},
        "modern_green": {"primary": "2CA02C", "text": "FFFFFF"},
        "slate_gray": {"primary": "374151", "text": "FFFFFF"}
    }
    palette = themes.get(theme, themes["corporate_blue"])
    
    # 2. Setup Backend Data Sheet
    data_ws = wb.create_sheet(f"{sheet_name}_Backend")
    data_ws.sheet_state = 'hidden'  # Keep dashboard clean
    
    # Data A: Matrix for Stacked Column Chart
    matrix_data = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Sugar"],
        ["India", 62000, 4800, 21000, 18000],
        ["Philippines", 54000, 7000, 22000, 14000],
        ["United Kingdom", 46000, 5200, 11000, 19000],
        ["Malaysia", 46000, 5500, 17000, 20000],
        ["United States", 36000, 6300, 22000, 9000]
    ]
    for r in matrix_data:
        data_ws.append(r)
        
    # Apply Currency formatting to Matrix
    for row in data_ws.iter_rows(min_row=2, max_row=6, min_col=2, max_col=5):
        for cell in row:
            cell.number_format = '"$"#,##0'
            
    # Data B: Time Series for Units Sold (Line Chart)
    units_data = [
        ["Month", "Units Sold"],
        ["Sep", 50601],
        ["Oct", 95622],
        ["Nov", 65481],
        ["Dec", 52970]
    ]
    data_ws.append([])  # Spacer
    start_row_units = data_ws.max_row + 1
    for r in units_data:
        data_ws.append(r)
        
    # Apply Standard Number formatting to Units
    for row in data_ws.iter_rows(min_row=start_row_units+1, max_row=start_row_units+4, min_col=2, max_col=2):
        for cell in row:
            cell.number_format = '#,##0'
            
    # Data C: Time Series for Profit (Line Chart)
    profit_data = [
        ["Month", "Profit"],
        ["Sep", 124812],
        ["Oct", 228275],
        ["Nov", 160228],
        ["Dec", 136337]
    ]
    data_ws.append([])  # Spacer
    start_row_profit = data_ws.max_row + 1
    for r in profit_data:
        data_ws.append(r)
        
    # Apply Currency formatting to Profit
    for row in data_ws.iter_rows(min_row=start_row_profit+1, max_row=start_row_profit+4, min_col=2, max_col=2):
        for cell in row:
            cell.number_format = '"$"#,##0'
            
    # 3. Setup Dashboard Presentation Layer
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    ws.sheet_view.showRowColHeaders = False
    
    # Title Banner Strip
    ws.merge_cells("A1:Q3")
    banner = ws["A1"]
    banner.value = title
    banner.font = Font(size=24, bold=True, color=palette["text"])
    banner.fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    banner.alignment = Alignment(horizontal="center", vertical="center")
    
    # 4. Chart Setup: Stacked Column (Profit by Market & Cookie)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    
    data_ref1 = Reference(data_ws, min_col=2, min_row=1, max_col=5, max_row=6)
    cats_ref1 = Reference(data_ws, min_col=1, min_row=2, max_row=6)
    chart1.add_data(data_ref1, titles_from_data=True)
    chart1.set_categories(cats_ref1)
    chart1.legend.position = "b"
    chart1.width = 16
    chart1.height = 10
    
    ws.add_chart(chart1, "B5")
    
    # 5. Chart Setup: Line Chart (Units Sold)
    chart2 = LineChart()
    chart2.title = "Units sold each month"
    chart2.legend = None
    
    data_ref2 = Reference(data_ws, min_col=2, min_row=start_row_units, max_row=start_row_units+4)
    cats_ref2 = Reference(data_ws, min_col=1, min_row=start_row_units+1, max_row=start_row_units+4)
    chart2.add_data(data_ref2, titles_from_data=True)
    chart2.set_categories(cats_ref2)
    chart2.width = 12
    chart2.height = 7
    
    ws.add_chart(chart2, "K5")
    
    # 6. Chart Setup: Line Chart (Profit by Month)
    chart3 = LineChart()
    chart3.title = "Profit by month"
    chart3.legend = None
    
    data_ref3 = Reference(data_ws, min_col=2, min_row=start_row_profit, max_row=start_row_profit+4)
    cats_ref3 = Reference(data_ws, min_col=1, min_row=start_row_profit+1, max_row=start_row_profit+4)
    chart3.add_data(data_ref3, titles_from_data=True)
    chart3.set_categories(cats_ref3)
    chart3.width = 12
    chart3.height = 7
    
    ws.add_chart(chart3, "K20")
```