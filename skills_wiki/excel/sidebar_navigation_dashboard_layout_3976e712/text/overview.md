### 1. High-level Skill Pattern Extraction

> **Skill Name**: Sidebar Navigation Dashboard Layout

* **Tier**: sheet_shell
* **Core Mechanism**: Simulates a modern app UI using cell formatting instead of native shapes. It configures a narrow, dark-filled column for global navigation links and a light gray canvas. White, bordered cell ranges act as visual 'cards' to hold KPIs and charts, while standard gridlines are hidden for a clean look.
* **Applicability**: Use as the foundational shell when generating an interactive management dashboard. It provides a structured grid for content and a ready-made sidebar for linking multiple sheets.

### 2. Structural Breakdown

- **Data Layout**: Employs a strict column grid where specific columns act as spacers (width 4) and others act as content containers (width 12).
- **Formula Logic**: Uses standard Excel hyperlink references (e.g., `#'SheetName'!A1`) to bind the sidebar text to other sheets.
- **Visual Design**: Hides sheet gridlines. Employs a tri-tone palette: Dark Deep Blue (sidebar), Light Gray (canvas background), and White (cards).
- **Charts/Tables**: Pre-allocates specific rows/columns for KPIs (top row) and Charts (bottom row) using `draw_card()`.
- **Theme Hooks**: Consumes semantic colors for `sidebar_bg`, `canvas_bg`, `card_bg`, and `text_main`.

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.worksheet.worksheet import Worksheet

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Builds a structured dashboard layout with a navigation sidebar and KPI/Chart cards.
    Simulates a 'rounded rectangle shape' UI using cleanly formatted cell ranges.
    """
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)
        
    # --- Theme & Colors ---
    sidebar_bg = "1E3A8A"  # Deep Blue
    sidebar_fg = "FFFFFF"  # White
    canvas_bg = "F3F4F6"   # Light Gray canvas
    card_bg = "FFFFFF"     # White cards
    card_border = "D1D5DB" # Gray border
    text_main = "111827"   # Dark text
    text_muted = "6B7280"  # Muted text
    
    # --- 1. Canvas Setup ---
    ws.sheet_view.showGridLines = False
    
    canvas_fill = PatternFill(fill_type="solid", start_color=canvas_bg)
    # Fill visible canvas area
    for row in ws.iter_rows(min_row=1, max_row=32, min_col=2, max_col=15):
        for cell in row:
            cell.fill = canvas_fill
            
    # --- 2. Navigation Sidebar (Column A) ---
    ws.column_dimensions['A'].width = 12
    sidebar_fill = PatternFill(fill_type="solid", start_color=sidebar_bg)
    for r in range(1, 33):
        ws.cell(row=r, column=1).fill = sidebar_fill
        
    nav_font = Font(color=sidebar_fg, bold=True, size=10)
    nav_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    
    # Emojis act as simple icons
    nav_items = [
        (4, "🏠\nHome", f"#'{sheet_name}'!A1"),
        (9, "📊\nInputs", "#'Inputs'!A1"),
        (14, "📞\nContacts", "#'Contacts'!A1")
    ]
    
    for r, text, link in nav_items:
        ws.merge_cells(start_row=r, end_row=r+2, start_column=1, end_column=1)
        cell = ws.cell(row=r, column=1, value=text)
        cell.font = nav_font
        cell.alignment = nav_align
        cell.hyperlink = link

    # --- 3. Dashboard Title ---
    title_cell = ws.cell(row=2, column=3, value=title)
    title_cell.font = Font(size=22, bold=True, color=text_main)
    subtitle_cell = ws.cell(row=3, column=3, value="Figures in USD")
    subtitle_cell.font = Font(size=11, italic=True, color=text_muted)

    # --- 4. Card Generator Engine ---
    thin_side = Side(border_style="thin", color=card_border)
    card_fill = PatternFill(fill_type="solid", start_color=card_bg)
    
    def draw_card(min_col: int, min_row: int, max_col: int, max_row: int, header: str):
        # Paint the card background and establish borders
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = card_fill
                cell.border = Border(
                    top=thin_side if r == min_row else None,
                    bottom=thin_side if r == max_row else None,
                    left=thin_side if c == min_col else None,
                    right=thin_side if c == max_col else None
                )
        
        # Merge the top row of the card for a clean header
        ws.merge_cells(start_row=min_row, end_row=min_row, start_column=min_col, end_column=max_col)
        header_cell = ws.cell(row=min_row, column=min_col, value=f"  {header}")
        header_cell.font = Font(bold=True, size=11, color=text_main)
        header_cell.alignment = Alignment(vertical="center")

    # --- 5. Draw Layout Grid ---
    # Top Row: KPI Cards
    draw_card(min_col=3, min_row=5, max_col=5, max_row=9, header="Sales")
    draw_card(min_col=7, min_row=5, max_col=9, max_row=9, header="Profit")
    draw_card(min_col=11, min_row=5, max_col=13, max_row=9, header="Customers")
    
    # Bottom Row: Chart Cards
    draw_card(min_col=3, min_row=11, max_col=9, max_row=28, header="Sales Trend")
    draw_card(min_col=11, min_row=11, max_col=13, max_row=28, header="Distribution")
    
    # Establish structural column widths (Spacers = 4, Content = 12)
    for c in [2, 6, 10, 14]:
        ws.column_dimensions[ws.cell(row=1, column=c).column_letter].width = 4
    for c in [3, 4, 5, 7, 8, 9, 11, 12, 13]:
        ws.column_dimensions[ws.cell(row=1, column=c).column_letter].width = 12
```