### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dark Sidebar KPI Dashboard

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a modern, interactive-style dashboard layout using grid cell formatting rather than brittle floating shapes. It splits the worksheet into a narrow, dark-themed left sidebar for high-level KPI metrics, and a wide, light-themed main canvas for charts and data tables. Gridlines are disabled to create a software-like application feel.
* **Applicability**: Best suited for executive summaries, performance overviews, or any reporting scenario where 3-5 critical metrics need persistent visibility on the left, while supporting visualizations occupy the primary right-hand viewing area.

### 2. Structural Breakdown

- **Data Layout**: 
  - Column A: Narrow padding (width 2)
  - Column B: Sidebar metric container (width 25)
  - Column C: Divider/padding (width 3)
  - Column D-M: Main chart/table canvas. 
- **Formula Logic**: Acts as the presentation layer. In practice, the KPI values injected into Column B should link to external PivotTables or aggregate calculations (e.g., `=Pivots!B4`).
- **Visual Design**: High contrast. The sidebar uses a deep `primary_dark` fill with bright `text_light` labels and vibrantly colored `accent` metric values. The main canvas uses a subtle off-white or light gray fill to pop against the charts.
- **Charts/Tables**: The canvas area is designed to host `BarChart`, `LineChart`, or `DoughnutChart` objects. 
- **Theme Hooks**: 
  - `sidebar_bg`: Deep primary brand color.
  - `canvas_bg`: Light neutral color (e.g., F3F3F3).
  - `text_light`: White or near-white for readability on dark background.
  - `accent`: Vibrant color for KPI numbers (e.g., gold, bright blue, or green).

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, Reference

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a modern dashboard shell with a dark left-hand KPI sidebar 
    and a light main canvas for charts.
    """
    # 1. Theme Configuration
    # Fallback palette showcasing how themes drive the high-contrast UI
    palettes = {
        "corporate_blue": {
            "sidebar_bg": "002B5B", 
            "canvas_bg": "F8F9FA", 
            "text_light": "FFFFFF", 
            "accent": "00D2D3"
        },
        "forest_green": {
            "sidebar_bg": "1B3E2F", 
            "canvas_bg": "FFFFFF", 
            "text_light": "E8F5E9", 
            "accent": "FFC107"
        }
    }
    palette = palettes.get(theme, palettes["corporate_blue"])
    
    # 2. Setup Worksheet
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    # 3. Define Grid Layout (Grid-based UI instead of Shapes)
    ws.column_dimensions['A'].width = 2.5
    ws.column_dimensions['B'].width = 25.0
    ws.column_dimensions['C'].width = 3.0
    
    for col_letter in ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']:
        ws.column_dimensions[col_letter].width = 12.0

    # 4. Apply Background Fills
    sidebar_fill = PatternFill(start_color=palette["sidebar_bg"], end_color=palette["sidebar_bg"], fill_type="solid")
    canvas_fill = PatternFill(start_color=palette["canvas_bg"], end_color=palette["canvas_bg"], fill_type="solid")
    
    for row in range(1, 45):
        # Paint Sidebar
        ws.cell(row=row, column=1).fill = sidebar_fill
        ws.cell(row=row, column=2).fill = sidebar_fill
        # Paint Canvas
        for col in range(3, 15):
            ws.cell(row=row, column=col).fill = canvas_fill

    # 5. Render Sidebar Content (Title & KPIs)
    title_cell = ws.cell(row=2, column=2, value=title.upper())
    title_cell.font = Font(color=palette["text_light"], size=16, bold=True)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # KPI Data Injection
    kpis = kwargs.get("kpis", [
        ("Total Sales", "$649.0K"),
        ("Total Orders", "2,400"),
        ("Units Sold", "11,997"),
        ("Avg Delivery Days", "2.3")
    ])
    
    current_row = 6
    for label, value in kpis:
        # Label
        lbl_cell = ws.cell(row=current_row, column=2, value=label)
        lbl_cell.font = Font(color=palette["text_light"], size=11)
        lbl_cell.alignment = Alignment(horizontal="center")
        
        # Value
        val_cell = ws.cell(row=current_row + 1, column=2, value=value)
        val_cell.font = Font(color=palette["accent"], size=20, bold=True)
        val_cell.alignment = Alignment(horizontal="center")
        
        current_row += 4

    # 6. Render Canvas Content (Example Chart)
    # Write some hidden chart data to fuel the visualization
    chart_data = [
        ("Category", "Revenue"),
        ("Apparel", 240500),
        ("Footwear", 185000),
        ("Accessories", 95300),
        ("Equipment", 128200)
    ]
    
    # We place data out of the main view (e.g., column Z)
    for r_idx, row_data in enumerate(chart_data, start=1):
        for c_idx, value in enumerate(row_data, start=26): 
            ws.cell(row=r_idx, column=c_idx, value=value)

    # Create Bar Chart
    chart = BarChart()
    chart.title = "Revenue by Category"
    chart.style = 11  # Clean style
    chart.width = 16
    chart.height = 8
    chart.legend = None

    data_ref = Reference(ws, min_col=27, min_row=1, max_row=len(chart_data), max_col=27)
    cats_ref = Reference(ws, min_col=26, min_row=2, max_row=len(chart_data))
    
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    
    # Place chart in the canvas area
    ws.add_chart(chart, "D5")
```