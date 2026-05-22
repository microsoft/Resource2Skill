### 1. High-level Skill Pattern Extraction

> **Skill Name**: Grid-Based Dashboard UI Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Adapts a shape-based dashboard UI into a robust cell-grid layout suitable for programmatic generation. It dedicates the first column to a dark navigation sidebar with cross-sheet hyperlinks, paints a light "canvas" background across the worksheet, and draws distinct white "cards" via borders and fills to act as modular containers for KPIs and charts.
* **Applicability**: Best for high-level executive summaries and KPI tracking sheets where a modern, web-app-like presentation layer is required directly within an Excel file, avoiding the complexity and instability of floating shape objects.

### 2. Structural Breakdown

- **Data Layout**: Col A (width 8) serves as the persistent navigation sidebar. Col B (width 2) acts as the left canvas margin. Content is organized into modular layout blocks (e.g., cols C-E for Card 1, G-I for Card 2) separated by spacer columns (width 2).
- **Formula Logic**: Utilizes native internal workbook hyperlinking (`#'SheetName'!A1`) applied to sidebar cells to simulate a clickable navigation menu.
- **Visual Design**: Hides native gridlines to create a clean canvas. The canvas is painted light slate (`#F1F5F9`), the sidebar is dark navy (`#1E293B`), and cards are white (`#FFFFFF`) with thin gray boundaries simulating a subtle drop shadow/edge.
- **Charts/Tables**: Prepares empty, perfectly dimensioned grid regions ready to receive standard components (like Line charts or Donut charts).
- **Theme Hooks**: Consumes standard structural colors: `primary` (sidebar), `bg_canvas` (main sheet fill), `bg_card` (container fill), and `border` (card outlines).

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.worksheet.worksheet import Worksheet

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard South America", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders an app-like dashboard layout shell using cell background grids.
    Provides a left navigation sidebar and modular white 'cards' for inserting visual KPIs.
    """
    if sheet_name not in wb.sheetnames:
        ws = wb.create_sheet(sheet_name)
    else:
        ws = wb[sheet_name]

    # Theme Fallbacks
    colors = {
        "sidebar": "1E293B",   # Dark Slate
        "canvas": "F1F5F9",    # Light Gray
        "card": "FFFFFF",      # White
        "text_light": "FFFFFF",
        "text_dark": "0F172A",
        "border": "CBD5E1"     # Light Outline
    }

    # Hide native gridlines to break the "spreadsheet" look
    ws.sheet_view.showGridLines = False

    # 1. Paint Canvas Background
    canvas_fill = PatternFill(start_color=colors["canvas"], end_color=colors["canvas"], fill_type="solid")
    for row in ws.iter_rows(min_row=1, max_row=35, min_col=1, max_col=15):
        for cell in row:
            cell.fill = canvas_fill

    # 2. Setup Persistent Sidebar (Column A)
    ws.column_dimensions['A'].width = 10
    sidebar_fill = PatternFill(start_color=colors["sidebar"], end_color=colors["sidebar"], fill_type="solid")
    for row in range(1, 36):
        ws.cell(row=row, column=1).fill = sidebar_fill

    # Render Sidebar Navigation
    nav_links = kwargs.get("nav_links", [
        {"label": "DASH", "sheet": sheet_name},
        {"label": "DATA", "sheet": "Inputs"},
        {"label": "CONTACT", "sheet": "Contacts"}
    ])
    
    start_row = 6
    for link in nav_links:
        # Create target sheet if it doesn't exist to ensure valid hyperlink
        if link["sheet"] not in wb.sheetnames:
            wb.create_sheet(link["sheet"])
            
        cell = ws.cell(row=start_row, column=1)
        cell.value = link["label"]
        cell.font = Font(color=colors["text_light"], bold=True)
        cell.alignment = Alignment(horizontal="center", vertical="center", textRotation=90)
        cell.hyperlink = f"#'{link['sheet']}'!A1"
        start_row += 6

    # 3. Setup Layout Grid Dimensions (Spacers and Content Columns)
    ws.column_dimensions['B'].width = 2   # Canvas Margin
    ws.column_dimensions['F'].width = 2   # Card Spacer 1
    ws.column_dimensions['J'].width = 2   # Card Spacer 2
    
    for col in ['C', 'D', 'E', 'G', 'H', 'I', 'K', 'L', 'M']:
        ws.column_dimensions[col].width = 13

    ws.row_dimensions[2].height = 30
    ws.row_dimensions[3].height = 10
    ws.row_dimensions[9].height = 10

    # 4. Insert Dashboard Header
    title_cell = ws.cell(row=2, column=3)
    title_cell.value = title
    title_cell.font = Font(size=20, bold=True, color=colors["text_dark"])
    title_cell.alignment = Alignment(vertical="center")

    # 5. UI Card Drawing Helper
    def draw_card(sheet: Worksheet, min_col: int, min_row: int, max_col: int, max_row: int, card_title: str):
        card_fill = PatternFill(start_color=colors["card"], end_color=colors["card"], fill_type="solid")
        thin_side = Side(style='thin', color=colors["border"])

        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                cell = sheet.cell(row=r, column=c)
                cell.fill = card_fill
                
                # Apply precise outer borders
                cell.border = Border(
                    top=thin_side if r == min_row else None,
                    bottom=thin_side if r == max_row else None,
                    left=thin_side if c == min_col else None,
                    right=thin_side if c == max_col else None
                )

        # Card Header
        t_cell = sheet.cell(row=min_row + 1, column=min_col)
        t_cell.value = f"  {card_title}"
        t_cell.font = Font(size=12, bold=True, color=colors["text_dark"])

    # 6. Render Dashboard Cards
    # Top Row: 3x KPI Metric Widgets
    draw_card(ws, min_col=3, min_row=4, max_col=5, max_row=8, card_title="Total Sales")
    draw_card(ws, min_col=7, min_row=4, max_col=9, max_row=8, card_title="Net Profit")
    draw_card(ws, min_col=11, min_row=4, max_col=13, max_row=8, card_title="# Customers")

    # Bottom Row: Wide Charts
    draw_card(ws, min_col=3, min_row=10, max_col=8, max_row=24, card_title="2021-2022 Sales Trend")
    draw_card(ws, min_col=9, min_row=10, max_col=13, max_row=24, card_title="Customer Satisfaction")
```