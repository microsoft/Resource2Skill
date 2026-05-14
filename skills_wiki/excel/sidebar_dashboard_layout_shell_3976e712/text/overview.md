### 1. High-level Skill Pattern Extraction

> **Skill Name**: Sidebar Dashboard Layout Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a grid-based, web-app style layout by configuring column widths, hiding gridlines, and applying contrasting background fills. Uses specific cell perimeters with subtle borders to simulate clean floating "cards" (to hold KPIs/charts), alongside a hyperlinked sidebar for cross-sheet navigation.
* **Applicability**: Use as the structural foundation for interactive reports and dashboards. Creating UI containers via cell formatting (rather than floating shapes) ensures perfect alignment, prevents rendering glitches across different Excel versions, and keeps layout robust when scaling.

### 2. Structural Breakdown

- **Data Layout**: Fixed-width columns create a standardized grid. Column A acts as the sidebar; Columns B, G, and L act as empty margin/gutter spacers; the remaining columns house the content cards. 
- **Formula Logic**: Simulated interactive navigation using `cell.hyperlink` pointing to local sheet references (e.g., `#'SheetName'!A1`).
- **Visual Design**: The global sheet view hides default gridlines (`showGridLines = False`). A light gray fill covers the background, while the cards are painted solid white with a light gray 1px border around their exact perimeter.
- **Charts/Tables**: This shell leaves designated empty cell regions (the white cards) ready to act as anchors for subsequently inserted charts or KPI data. 
- **Theme Hooks**: Consumes standard hex codes for the sidebar (`primary` or custom dark), background (`bg_light`), card fill (`white`), and borders (`gray`).

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # Create or get the sheet
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)
    
    # Define palette (normally extracted from theme)
    bg_hex = "F3F4F6"      # Light gray background
    card_hex = "FFFFFF"    # White cards
    sidebar_hex = "1E2A38" # Dark sidebar
    primary_hex = "1F4E78" # Dark blue text/accents
    border_hex = "D9D9D9"  # Subtle borders
    
    # Hide standard gridlines for a clean UI
    ws.sheet_view.showGridLines = False

    # 1. Setup Column Widths for a Grid Layout
    ws.column_dimensions['A'].width = 15  # Sidebar
    ws.column_dimensions['B'].width = 3   # Left margin
    for col in ['C', 'D', 'E', 'F', 'H', 'I', 'J', 'K', 'M', 'N', 'O', 'P']:
        ws.column_dimensions[col].width = 12 # Card content
    for col in ['G', 'L']:
        ws.column_dimensions[col].width = 3  # Gutters between cards

    # 2. Paint Main Background
    gray_fill = PatternFill(start_color=bg_hex, end_color=bg_hex, fill_type="solid")
    for row in range(1, 35):
        for col in range(2, 18): # B to Q
            ws.cell(row=row, column=col).fill = gray_fill

    # 3. Build Navigation Sidebar
    sidebar_fill = PatternFill(start_color=sidebar_hex, end_color=sidebar_hex, fill_type="solid")
    for row in range(1, 35):
        ws.cell(row=row, column=1).fill = sidebar_fill
    
    nav_items = [
        ("🏠 Home", f"#'{sheet_name}'!A1"), 
        ("📊 Data", f"#'{sheet_name}'!A1"), 
        ("⚙️ Settings", f"#'{sheet_name}'!A1")
    ]
    for i, (item, link) in enumerate(nav_items):
        cell = ws.cell(row=5 + i*4, column=1)
        cell.value = item
        cell.font = Font(color="FFFFFF", bold=True, underline="single")
        cell.alignment = Alignment(horizontal="center")
        cell.hyperlink = link

    # 4. Add Dashboard Header
    ws.cell(row=2, column=3, value=title).font = Font(size=20, bold=True, color=primary_hex)
    ws.cell(row=3, column=3, value="Figures in millions of USD").font = Font(size=11, italic=True, color="595959")

    # 5. Helper function to draw "Cards" using cell perimeters
    def make_card(start_col, start_row, end_col, end_row, title_text):
        white_fill = PatternFill(start_color=card_hex, end_color=card_hex, fill_type="solid")
        
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = white_fill
                
                # Apply perimeter borders selectively
                b_left = Side(style="thin", color=border_hex) if c == start_col else None
                b_right = Side(style="thin", color=border_hex) if c == end_col else None
                b_top = Side(style="thin", color=border_hex) if r == start_row else None
                b_bottom = Side(style="thin", color=border_hex) if r == end_row else None
                
                if b_left or b_right or b_top or b_bottom:
                    cell.border = Border(left=b_left, right=b_right, top=b_top, bottom=b_bottom)
                
        # Card Header
        title_c = ws.cell(row=start_row + 1, column=start_col + 1)
        title_c.value = title_text
        title_c.font = Font(size=14, bold=True, color="333333")

    # 6. Instantiate Dashboard Cards
    # KPI Row (3 cards side-by-side)
    make_card(3, 6, 6, 12, "Sales")
    make_card(8, 6, 11, 12, "Profit")
    make_card(13, 6, 16, 12, "Customers")

    # Visual Row (2 larger cards)
    make_card(3, 14, 11, 28, "2021-2022 Sales Trend")
    make_card(13, 14, 16, 28, "Customer Satisfaction")

    # 7. Populate mock KPI data inside the first row of cards
    kpi_font = Font(size=24, bold=True, color=primary_hex)
    
    ws.cell(row=9, column=4, value="$2,544").font = kpi_font
    ws.cell(row=9, column=9, value="$890").font = kpi_font
    ws.cell(row=9, column=14, value="87.0").font = kpi_font
```