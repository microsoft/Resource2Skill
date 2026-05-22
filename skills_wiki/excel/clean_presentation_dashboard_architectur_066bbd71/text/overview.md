### 1. High-level Skill Pattern Extraction

> **Skill Name**: Clean Presentation Dashboard Architecture

* **Tier**: archetype
* **Core Mechanism**: Separates raw data, calculation layers, and presentation layers into distinct worksheets. The presentation sheet uses a borderless, gridline-free canvas with a unified header banner and precisely aligned, sized charts (e.g., a primary stacked bar chart and secondary trend line charts).
* **Applicability**: Ideal for executive summaries and KPI reporting. This sets up the structural foundation required for interactive dashboards. In a complete workflow, users map these charts to PivotTables and connect Excel Slicers/Timelines for full interactivity.

### 2. Structural Breakdown

- **Data Layout**: Employs a multi-sheet architecture: `Data` (raw tables), `Calc` (summarized data or pivot caches), and `Dashboard` (visuals only).
- **Formula Logic**: Isolates summarization to the `Calc` sheet, keeping the `Dashboard` clean.
- **Visual Design**: Disables sheet gridlines (`showGridLines = False`). Uses a full-width merged cell with a solid background fill and bold, contrasting text for the dashboard title.
- **Charts/Tables**: 
  - Main Chart: Stacked Column chart (100% overlap) to show composition across categories.
  - Secondary Charts: Line charts to show metric trends over time. 
  - Charts are sized explicitly (`width`, `height`) and aligned to create a grid layout.
- **Theme Hooks**: The title banner background uses the primary theme color (e.g., `theme.primary_bg`), and the font uses `theme.primary_fg`.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart, Reference

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Builds a multi-sheet dashboard architecture with a clean presentation layer,
    aligned charts, and a hidden calculation sheet.
    """
    # 1. Setup sheets
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_calc = wb.create_sheet("Calc")
    ws_data = wb.create_sheet("Data")
    
    # 2. Setup the Dashboard Presentation Layer
    ws_dash.sheet_view.showGridLines = False
    
    # Simple theme color fallback mapping
    theme_bg = "4F81BD" # Corporate Blue default
    if theme == "dark":
        theme_bg = "203764"
    elif theme == "success":
        theme_bg = "00B050"
        
    # Build Dashboard Header
    header_cell = ws_dash['A1']
    header_cell.value = title
    header_cell.font = Font(size=24, bold=True, color="FFFFFF")
    header_cell.fill = PatternFill(start_color=theme_bg, end_color=theme_bg, fill_type="solid")
    header_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws_dash.merge_cells('A1:P2')
    ws_dash.row_dimensions[1].height = 20
    ws_dash.row_dimensions[2].height = 20

    # 3. Populate Calculation Data (Simulating PivotTable summaries)
    # Chart 1 Data: Profit by Market & Cookie Type
    ws_calc.append(["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin"])
    ws_calc.append(["India", 62349, 4872, 21028])
    ws_calc.append(["United Kingdom", 46530, 5220, 11497])
    ws_calc.append(["United States", 36657, 6368, 22260])
    
    # Chart 2 & 3 Data: Monthly Metrics
    ws_calc.append([]) # Spacer row 5
    ws_calc.append(["Month", "Units Sold", "Profit"])
    ws_calc.append(["Sep", 50601, 124812])
    ws_calc.append(["Oct", 95622, 228275])
    ws_calc.append(["Nov", 65481, 160228])
    ws_calc.append(["Dec", 52970, 136337])
    
    # 4. Create and Align Charts on the Dashboard
    
    # Primary Chart: Stacked Column (Profit by Market & Cookie)
    bar = BarChart()
    bar.type = "col"
    bar.grouping = "stacked"
    bar.overlap = 100
    bar.title = "Profit by Market & Cookie Type"
    bar.y_axis.title = "Profit ($)"
    
    cats_bar = Reference(ws_calc, min_col=1, min_row=2, max_row=4)
    data_bar = Reference(ws_calc, min_col=2, max_col=4, min_row=1, max_row=4)
    bar.add_data(data_bar, titles_from_data=True)
    bar.set_categories(cats_bar)
    bar.width = 15
    bar.height = 11
    ws_dash.add_chart(bar, "B4")
    
    # Secondary Chart 1: Units Sold (Line)
    line1 = LineChart()
    line1.title = "Units sold each month"
    line1.y_axis.title = "Units"
    line1.legend = None  # Remove legend for clean look
    
    cats_line = Reference(ws_calc, min_col=1, min_row=7, max_row=10)
    data_line1 = Reference(ws_calc, min_col=2, max_col=2, min_row=6, max_row=10)
    line1.add_data(data_line1, titles_from_data=True)
    line1.set_categories(cats_line)
    line1.width = 12
    line1.height = 5.3
    ws_dash.add_chart(line1, "J4")
    
    # Secondary Chart 2: Profit by Month (Line)
    line2 = LineChart()
    line2.title = "Profit by month"
    line2.y_axis.title = "Profit ($)"
    line2.legend = None
    
    data_line2 = Reference(ws_calc, min_col=3, max_col=3, min_row=6, max_row=10)
    line2.add_data(data_line2, titles_from_data=True)
    line2.set_categories(cats_line)
    line2.width = 12
    line2.height = 5.3
    ws_dash.add_chart(line2, "J13")
    
    # 5. Final Architecture Cleanup
    ws_calc.sheet_state = 'hidden'
```