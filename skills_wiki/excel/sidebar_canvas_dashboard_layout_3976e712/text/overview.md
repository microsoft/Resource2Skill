```
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Sidebar Canvas Dashboard Layout

* **Tier**: sheet_shell
* **Core Mechanism**: Uses cell background colors and borders to simulate floating "layout cards" on a light canvas, combined with a dark vertical sidebar for navigation. Bypasses the need for brittle floating shape rectangles, making the layout fully programmatic, grid-aligned, and easily targetable by charts.
* **Applicability**: When building an interactive, top-level executive dashboard that needs to look like a modern web app but stay entirely within native Excel grid features.

### 2. Structural Breakdown

- **Data Layout**: Uses slim spacer columns (B, F, J, N) and spacer rows (4, 9, 16) to create visual gutters between the white "card" regions.
- **Formula Logic**: Purely structural layout shell; designed to accept values or formulas dynamically in the KPI value cells.
- **Visual Design**: Gridlines are hidden. The canvas uses a light gray fill (`F2F2F2`), the sidebar uses a primary dark fill (`1F4E78`), and the cards use a solid white fill (`FFFFFF`) with a thin gray (`D9D9D9`) perimeter border to simulate a drop shadow / elevation effect.
- **Charts/Tables**: Provides designated cell ranges (cards) acting as anchoring zones for line charts, donut charts, or maps.
- **Theme Hooks**: Consumes `primary` for the sidebar background and main header text, a light `canvas_bg` for the worksheet, and `card_bg` for the content blocks.

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Border, Side, Font, Alignment

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a modern, card-based dashboard shell using a left sidebar and 
    a grid of white 'cards' set against a light gray canvas.
    """
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    # Palette definition (mocked for standalone execution; adapt to theme engine)
    sidebar_color = "1F4E78" # e.g., theme.primary
    canvas_color = "F2F2F2"  # e.g., theme.background
    card_color = "FFFFFF"    # e.g., theme.surface
    border_color = "D9D9D9"  # e.g., theme.border
    text_color = "333333"    # e.g., theme.text
    
    sidebar_fill = PatternFill(start_color=sidebar_color, end_color=sidebar_color, fill_type="solid")
    canvas_fill = PatternFill(start_color=canvas_color, end_color=canvas_color, fill_type="solid")
    card_fill = PatternFill(start_color=card_color, end_color=card_color, fill_type="solid")
    
    # 1. Paint the entire canvas area
    for row in ws.iter_rows(min_row=1, max_row=25, min_col=2, max_col=14):
        for cell in row:
            cell.fill = canvas_fill
            
    # 2. Paint the left navigation sidebar
    for row in range(1, 26):
        ws.cell(row=row, column=1).fill = sidebar_fill
    ws.column_dimensions['A'].width = 8
    
    # 3. Helper function to draw cell-based cards with borders
    def make_card(min_col, min_row, max_col, max_row, card_title=""):
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = card_fill
                
                # Apply thin borders only to the perimeter of the card range
                top = Side(style='thin', color=border_color) if r == min_row else None
                bottom = Side(style='thin', color=border_color) if r == max_row else None
                left = Side(style='thin', color=border_color) if c == min_col else None
                right = Side(style='thin', color=border_color) if c == max_col else None
                cell.border = Border(top=top, bottom=bottom, left=left, right=right)
        
        # Add card title in the top-left cell
        if card_title:
            title_cell = ws.cell(row=min_row, column=min_col)
            title_cell.value = card_title
            title_cell.font = Font(bold=True, size=11, color=text_color)
            title_cell.alignment = Alignment(vertical="center")
            ws.row_dimensions[min_row].height = 25

    # Format spacer columns (gutters)
    for col in ['B', 'F', 'J', 'N']:
        ws.column_dimensions[col].width = 2
        
    # Format card content columns
    for col in ['C', 'D', 'E', 'G', 'H', 'I', 'K', 'L', 'M']:
        ws.column_dimensions[col].width = 12

    # --- Draw Dashboard Cards ---
    
    # Main Header Card
    make_card(3, 2, 13, 3, card_title=title)
    ws.cell(row=2, column=3).font = Font(bold=True, size=16, color=sidebar_color)
    
    # Top Row: KPI Cards
    make_card(3, 5, 5, 8, card_title="Sales")
    make_card(7, 5, 9, 8, card_title="Profit")
    make_card(11, 5, 13, 8, card_title="Customers")
    
    # Bottom Row: Chart Cards
    make_card(3, 10, 9, 22, card_title="2021-2022 Sales Trend")
    make_card(11, 10, 13, 15, card_title="Sales by Country")
    make_card(11, 17, 13, 22, card_title="Customer Satisfaction")

    # Add placeholder KPI values into the cards
    kpis = [
        (3, "$2,544"), 
        (7, "$890"), 
        (11, "87.0")
    ]
    
    for col, val in kpis:
        kpi_cell = ws.cell(row=6, column=col, value=val)
        kpi_cell.font = Font(size=20, bold=True, color=sidebar_color)
        kpi_cell.alignment = Alignment(horizontal="left", vertical="center")
```
```