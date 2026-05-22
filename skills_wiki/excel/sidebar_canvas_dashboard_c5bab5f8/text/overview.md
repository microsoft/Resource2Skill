### 1. High-level Skill Pattern Extraction

> **Skill Name**: Sidebar Canvas Dashboard

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a modern dashboard UI using cell formatting rather than floating shapes. It builds a high-contrast dark sidebar for key metrics/KPIs on the left, paired with a light-colored main canvas area. Distinct "card" regions are drawn onto the canvas using soft borders and top-accent lines, acting as standardized drop-zones for charts and tables.
* **Applicability**: Ideal for executive summaries, financial overviews, and master dashboards where top-level metrics need to be anchored persistently alongside detailed visualizations.

### 2. Structural Breakdown

- **Data Layout**: 
  - Sidebar: Columns A through C (merged or sized for text).
  - Canvas Margin: Column D (spacer).
  - Canvas Cards: Columns E+ arranged in grid blocks.
- **Formula Logic**: Uses openpyxl number formatting directly on the value cells rather than linking text boxes to formulas, ensuring exact alignment and clean rendering.
- **Visual Design**: Turns off native gridlines. Uses `primary` theme color for the continuous sidebar background, high-contrast white/large fonts for the KPIs, and a subtle light gray/green background for the main canvas.
- **Charts/Tables**: Creates empty "Card" zones (white background, thin gray outline, medium primary top border) designed to host openpyxl charts or structured tables.
- **Theme Hooks**: Consumes `primary`, `bg_light`, `card_bg`, `text_light`, and `text_dark`.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "botanical_green", **kwargs) -> None:
    """
    Renders a fully structured dashboard canvas with a dark left KPI sidebar 
    and a light main content area with designated "cards" for charts.
    """
    # Palette lookup
    themes = {
        "corporate_blue": {"primary": "1F4E78", "bg_light": "F2F5F8", "card_bg": "FFFFFF", "text_light": "FFFFFF", "text_dark": "333333"},
        "botanical_green": {"primary": "2E4E3F", "bg_light": "E9EFEA", "card_bg": "FFFFFF", "text_light": "FFFFFF", "text_dark": "1A2B22"}
    }
    palette = themes.get(theme, themes["corporate_blue"])

    # Default realistic data from the tutorial
    kpis = kwargs.get("kpis", [
        {"label": "Total Orders", "value": 2400, "fmt": "#,##0"},
        {"label": "Quantity", "value": 11997, "fmt": "#,##0"},
        {"label": "Total Revenue", "value": 649019, "fmt": "$#,##0"},
        {"label": "Avg Rating", "value": 4.0, "fmt": "0.0"},
        {"label": "Days to Deliver", "value": 2.3, "fmt": "0.0"}
    ])

    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # 1. Configure Column Widths
    ws.column_dimensions['A'].width = 2
    ws.column_dimensions['B'].width = 18
    ws.column_dimensions['C'].width = 2
    ws.column_dimensions['D'].width = 4  # Spacer
    
    # Grid columns for canvas
    for col_idx in range(5, 20):
        ws.column_dimensions[chr(64 + col_idx)].width = 12

    # 2. Paint Backgrounds
    sidebar_fill = PatternFill("solid", fgColor=palette["primary"])
    canvas_fill = PatternFill("solid", fgColor=palette["bg_light"])

    for row in range(1, 45):
        # Sidebar (A-C)
        for col in range(1, 4):
            ws.cell(row=row, column=col).fill = sidebar_fill
        # Canvas (D-S)
        for col in range(4, 20):
            ws.cell(row=row, column=col).fill = canvas_fill

    # 3. Render Title
    title_cell = ws.cell(row=3, column=5, value=title)
    title_cell.font = Font(color=palette["primary"], size=22, bold=True)

    # 4. Render Sidebar KPIs
    kpi_start_row = 6
    for kpi in kpis:
        # Label
        lbl_cell = ws.cell(row=kpi_start_row, column=2, value=kpi["label"])
        lbl_cell.font = Font(color=palette["text_light"], bold=False, size=11)
        lbl_cell.alignment = Alignment(vertical="center")
        
        # Value
        val_cell = ws.cell(row=kpi_start_row + 1, column=2, value=kpi["value"])
        val_cell.font = Font(color=palette["text_light"], bold=True, size=20)
        val_cell.alignment = Alignment(vertical="center")
        if "fmt" in kpi:
            val_cell.number_format = kpi["fmt"]
            
        kpi_start_row += 5

    # 5. Helper to draw Chart Cards
    def draw_card(start_row, start_col, end_row, end_col, card_title):
        card_fill = PatternFill("solid", fgColor=palette["card_bg"])
        
        # Borders to create elevation effect
        accent_top = Side(style="medium", color=palette["primary"])
        normal_side = Side(style="thin", color="CCCCCC")

        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = card_fill
                
                # Apply boundary borders
                top = accent_top if r == start_row else None
                bottom = normal_side if r == end_row else None
                left = normal_side if c == start_col else None
                right = normal_side if c == end_col else None
                cell.border = Border(top=top, bottom=bottom, left=left, right=right)

        # Card Title Header
        ws.merge_cells(start_row=start_row, start_column=start_col, end_row=start_row, end_column=end_col)
        header_cell = ws.cell(row=start_row, column=start_col, value=card_title)
        header_cell.font = Font(color=palette["text_dark"], bold=True, size=12)
        header_cell.alignment = Alignment(vertical="center", indent=1)

    # 6. Render Placeholder Cards for Visuals
    draw_card(6, 5, 18, 11, "Last 13 Week Trends - Qty & Amount")
    draw_card(6, 12, 18, 18, "How Customers Like to Buy")
    draw_card(20, 5, 38, 11, "Popular Products - Breakdown")
    draw_card(20, 12, 38, 18, "Customer Demographic Map")

```