```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Dashboard Shell Layout

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a multi-chart dashboard layout by disabling sheet gridlines, merging cells for a prominent themed header, rendering a left-hand control panel (mocking slicers/filters), and generating a grid of charts linked to a hidden, dedicated data worksheet.
* **Applicability**: Ideal for generating clean, read-only executive summary dashboards, or as a scaffold that users can later swap with interactive PivotCharts. 

### 2. Structural Breakdown

- **Data Layout**: Places raw/aggregated data on a secondary hidden sheet (`{sheet_name}_Data`) to keep the front-end dashboard canvas pristine.
- **Formula Logic**: Uses openpyxl's `Reference` objects to securely bind the dashboard charts to the hidden aggregated data arrays without cross-sheet formula string complexity.
- **Visual Design**: Disables standard gridlines (`showGridLines = False`). Uses bold, high-contrast block headers and subtle border lines for the control panel. 
- **Charts/Tables**: Arranges a `LineChart` and two `BarChart` objects in a distinct grid layout. 
- **Theme Hooks**: Consumes `primary` (header background), `secondary` (control panel header), and `text` (header font color) tokens from the theme dictionary.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, BarChart, Reference

def render_sheet(wb, sheet_name: str, *, title: str = "Heroic Insights 2023-24", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Creates a dashboard shell with a header, left-side control panel, and a grid of charts.
    Data is stored on a hidden companion sheet to keep the dashboard clean.
    """
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    # Theme palette fallback
    palettes = {
        "corporate_blue": {"primary": "1F497D", "secondary": "D9E1F2", "bg": "FFFFFF", "text": "FFFFFF"},
        "dark_mode": {"primary": "202020", "secondary": "505050", "bg": "000000", "text": "FFFFFF"}
    }
    palette = palettes.get(theme, palettes["corporate_blue"])
    
    # 1. Dashboard Header (Top Panel)
    ws.merge_cells("D2:O4")
    header = ws["D2"]
    header.value = title
    header.font = Font(name="Arial", size=24, bold=True, color=palette["text"])
    header.fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    header.alignment = Alignment(horizontal="center", vertical="center")
    
    # 2. Setup Data Sheet (Hidden from user view)
    data_ws = wb.create_sheet(f"{sheet_name}_Data")
    data_ws.sheet_state = "hidden"
    
    # -- Populate Line Chart Data --
    data_ws.append(["Month", "2023", "2024"]) # Row 1
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    val1 = [10500, 12000, 15000, 14200, 18000, 20500, 22000, 21000, 24000, 26000, 28500, 30000]
    val2 = [12000, 14500, 16000, 15500, 20000, 22000, 25000, 24000, 27000, 29000, 31000, 33500]
    for i in range(12):
        data_ws.append([months[i], val1[i], val2[i]]) # Rows 2-13
        
    # -- Populate Bar Chart Data (Category) --
    data_ws.append([]) # Row 14
    data_ws.append(["Year", "Hoodies", "T-shirts"]) # Row 15
    data_ws.append(["2023", 15201, 17141]) # Row 16
    data_ws.append(["2024", 17538, 22342]) # Row 17
    
    # -- Populate Bar Chart Data (State) --
    data_ws.append([]) # Row 18
    data_ws.append(["State", "Profit"]) # Row 19
    data_ws.append(["California", 38906]) # Row 20
    data_ws.append(["Texas", 34420]) # Row 21
    data_ws.append(["New York", 32641]) # Row 22
    data_ws.append(["Florida", 31908]) # Row 23
    data_ws.append(["Illinois", 29800]) # Row 24
    
    # 3. Create and Place Charts
    # Chart 1: Line Chart (Spans top half)
    lc = LineChart()
    lc.title = "Monthly Revenue Trend"
    lc.style = 13
    lc.height = 8
    lc.width = 16
    lc.y_axis.number_format = '$#,##0'
    data_ref = Reference(data_ws, min_col=2, max_col=3, min_row=1, max_row=13)
    cats_ref = Reference(data_ws, min_col=1, min_row=2, max_row=13)
    lc.add_data(data_ref, titles_from_data=True)
    lc.set_categories(cats_ref)
    ws.add_chart(lc, "D6")
    
    # Chart 2: Column Chart (Bottom Left)
    bc1 = BarChart()
    bc1.title = "Units Sold: Hoodies vs T-shirts"
    bc1.type = "col"
    bc1.style = 10
    bc1.height = 8
    bc1.width = 7.5
    data_ref2 = Reference(data_ws, min_col=2, max_col=3, min_row=15, max_row=17)
    cats_ref2 = Reference(data_ws, min_col=1, min_row=16, max_row=17)
    bc1.add_data(data_ref2, titles_from_data=True)
    bc1.set_categories(cats_ref2)
    ws.add_chart(bc1, "D20")
    
    # Chart 3: Column Chart (Bottom Right)
    bc2 = BarChart()
    bc2.title = "Top 5 States by Profit"
    bc2.type = "col"
    bc2.style = 10
    bc2.height = 8
    bc2.width = 8
    bc2.y_axis.number_format = '$#,##0'
    data_ref3 = Reference(data_ws, min_col=2, max_col=2, min_row=19, max_row=24)
    cats_ref3 = Reference(data_ws, min_col=1, min_row=20, max_row=24)
    bc2.add_data(data_ref3, titles_from_data=True)
    bc2.set_categories(cats_ref3)
    bc2.legend = None
    ws.add_chart(bc2, "I20")
    
    # 4. Mock Slicers (Control Panel on the Left)
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    slicer_header_fill = PatternFill(start_color=palette["secondary"], end_color=palette["secondary"], fill_type="solid")
    
    def draw_control_panel_box(start_row, col, title, items):
        """Draws a vertical UI box resembling an Excel Slicer"""
        cell = ws.cell(row=start_row, column=col)
        cell.value = title
        cell.font = Font(bold=True)
        cell.fill = slicer_header_fill
        cell.border = thin_border
        cell.alignment = Alignment(horizontal="center")
        
        for i, item in enumerate(items):
            c = ws.cell(row=start_row + 1 + i, column=col)
            c.value = item
            c.border = thin_border
            c.alignment = Alignment(horizontal="left", indent=1)
            
    draw_control_panel_box(6, 2, "Years", ["2023", "2024"])
    draw_control_panel_box(10, 2, "Category", ["Hoodies", "T-shirts"])
    draw_control_panel_box(14, 2, "State", ["California", "Texas", "New York", "Florida", "Illinois"])
    
    # Adjust control panel column width
    ws.column_dimensions['B'].width = 16
    ws.column_dimensions['C'].width = 3
```
```