### 1. High-level Skill Pattern Extraction

> **Skill Name**: Cell-Based Dashboard Canvas

* **Tier**: sheet_shell
* **Core Mechanism**: Disables gridlines and applies a global muted background fill. Generates floating "cards" (containers for charts and KPIs) by applying white backgrounds and thin outer borders to specific cell ranges, replicating modern floating-shape layouts without the fragility of Excel shape objects.
* **Applicability**: Use for generating professional, structured report dashboards programmatically. It provides a clean, modern UI grid that avoids the cross-version rendering issues often associated with floating shape objects.

### 2. Structural Breakdown

- **Data Layout**: Establishes a strict grid layout, using narrow "spacer" columns (width 3) to create visually equal gutters between the data cards.
- **Formula Logic**: N/A (Structural shell).
- **Visual Design**: Uses a muted gray (`#F3F4F6`) for the global canvas background and stark white (`#FFFFFF`) for the data cards to create depth. Outer borders are a very light gray (`#E5E7EB`). 
- **Charts/Tables**: Defines the precise bounding box ranges (e.g., `C13:M26`) where subsequent chart and KPI components should be anchored.
- **Theme Hooks**: Consumes the theme's primary accent color to fill the persistent left-side navigation rail.

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Border, Side, Font, Alignment

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a modern, card-based dashboard structure directly onto the cell grid,
    mimicking floating shape layouts without using fragile shape objects.
    """
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # Standard dashboard palette (neutral backing, white cards)
    bg_color = "F3F4F6"     # Muted gray background
    card_color = "FFFFFF"   # White card background
    nav_color = "1E3A8A"    # Deep blue navigation rail (theme primary anchor)
    text_color = "111827"   # Dark slate text
    border_color = "E5E7EB" # Light gray border

    # 1. Apply global background color (viewport area)
    fill_bg = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    for row in ws.iter_rows(min_row=1, max_row=40, min_col=1, max_col=24):
        for cell in row:
            cell.fill = fill_bg

    # 2. Build Navigation Rail (Column A)
    ws.column_dimensions['A'].width = 8
    fill_nav = PatternFill(start_color=nav_color, end_color=nav_color, fill_type="solid")
    for row in range(1, 41):
        ws[f"A{row}"].fill = fill_nav

    # Add navigation placeholder icons
    nav_items = ["🏠", "📊", "✉️", "❓"]
    for i, icon in enumerate(nav_items):
        cell = ws.cell(row=4 + (i*4), column=1, value=icon)
        cell.font = Font(size=16, color="FFFFFF")
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # 3. Add Dashboard Title & Subtitle
    title_cell = ws['C2']
    title_cell.value = title
    title_cell.font = Font(size=22, bold=True, color=text_color)

    subtitle_cell = ws['C3']
    subtitle_cell.value = "Figures in millions of USD"
    subtitle_cell.font = Font(size=11, color="6B7280", italic=True)

    # 4. Helper function to create a clean 'Card' container
    def create_card(min_col: int, max_col: int, min_row: int, max_row: int, card_title: str):
        card_fill = PatternFill(start_color=card_color, end_color=card_color, fill_type="solid")
        thin_side = Side(style='thin', color=border_color)

        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = card_fill

                # Calculate outer borders relative to the bounding box
                t = thin_side if r == min_row else None
                b = thin_side if r == max_row else None
                l = thin_side if c == min_col else None
                right = thin_side if c == max_col else None

                cell.border = Border(top=t, bottom=b, left=l, right=right)

        # Add Card Title in the top-left cell of the container
        header_cell = ws.cell(row=min_row, column=min_col)
        header_cell.value = f"  {card_title}" # Left padding spacing
        header_cell.font = Font(size=12, bold=True, color=text_color)
        header_cell.alignment = Alignment(vertical="center")

    # 5. Render standard layout cards matching the tutorial's structure
    # Row 1: KPI Cards
    create_card(min_col=3, max_col=7, min_row=5, max_row=11, card_title="Sales")
    create_card(min_col=9, max_col=13, min_row=5, max_row=11, card_title="Profit")
    create_card(min_col=15, max_col=19, min_row=5, max_row=11, card_title="# of Customers")

    # Row 2: Trend & Distribution Analysis
    create_card(min_col=3, max_col=13, min_row=13, max_row=26, card_title="2021-2022 Sales Trend")
    create_card(min_col=15, max_col=19, min_row=13, max_row=26, card_title="Customer Satisfaction")

    # Side Panel: Map/Geography Analysis
    create_card(min_col=21, max_col=24, min_row=5, max_row=26, card_title="Sales by Country")

    # 6. Set generic column gutters and row spacing
    ws.column_dimensions['B'].width = 3   # Margin left of cards
    ws.column_dimensions['H'].width = 3   # Gutter between KPI cards 1 & 2
    ws.column_dimensions['N'].width = 3   # Gutter between KPI cards 2 & 3
    ws.column_dimensions['T'].width = 3   # Gutter between main body and side panel

    # Expand columns inside the cards to provide a wider default canvas
    for col in ['C','D','E','F','G', 'I','J','K','L','M', 'O','P','Q','R','S', 'U','V','W','X']:
        ws.column_dimensions[col].width = 11

    # Give header rows slightly more room to breathe
    ws.row_dimensions[5].height = 25
    ws.row_dimensions[13].height = 25
```