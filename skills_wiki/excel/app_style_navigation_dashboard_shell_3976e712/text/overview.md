### 1. High-level Skill Pattern Extraction

> **Skill Name**: App-Style Navigation Dashboard Shell

* **Tier**: archetype
* **Core Mechanism**: Sets up a multi-sheet workbook where every sheet features a fixed, solid-colored navigation sidebar in Column A. It utilizes internal cell hyperlinks (`#'SheetName'!A1`) to create a web-app-like tab-switching experience. Gridlines are disabled, and main content is laid out inside emulated floating "cards" (painted cell boundaries) on an off-white canvas.
* **Applicability**: Perfect for executive summaries, reporting packages, and financial models where an end-user needs to navigate easily between Dashboard, Input, and Contact/Settings tabs without relying on native Excel sheet tabs. 

### 2. Structural Breakdown

- **Data Layout**: Sidebar is locked to Column A (width 16). The main dashboard canvas spans Columns B to P. Widget "cards" are rigidly positioned using specific row/column grids with empty columns serving as gutters.
- **Formula Logic**: Relies purely on internal Excel hyperlink syntax (`#'Sheet Name'!Cell`) embedded directly on the sidebar cells to trigger navigation jumps.
- **Visual Design**: Gridlines are hidden. Strong contrast is created using a dark background for the sidebar and a light gray background for the canvas. The data cards are created with a white fill and a thin gray border perimeter to emulate drop-shadow UI containers.
- **Charts/Tables**: Lays out structured, empty white card boundaries ("Sales Trend", "Customer Satisfaction", etc.) ready to house embedded OpenPyXL charts or formatted data tables.
- **Theme Hooks**: Consumes palette tokens for `sidebar_bg`, `sidebar_fg`, `canvas_bg`, `card_bg`, `border`, and `text_main`.

### 3. Reproduction Code

```python
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

def render_workbook(wb: Workbook, *, title: str = "Regional Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Builds a web-app style interactive dashboard shell with a persistent sidebar menu
    and a card-based layout structure ready for charts and data.
    """
    # 1. Define Theme Colors
    themes = {
        "corporate_blue": {
            "sidebar_bg": "1E3A8A",  # Dark Navy
            "sidebar_fg": "FFFFFF",  # White
            "canvas_bg":  "F3F4F6",  # Light Gray
            "card_bg":    "FFFFFF",  # White
            "border":     "D1D5DB",  # Medium Gray
            "text_main":  "111827",  # Dark Charcoal
        },
        "dark_mode": {
            "sidebar_bg": "111827",
            "sidebar_fg": "F9FAFB",
            "canvas_bg":  "1F2937",
            "card_bg":    "374151",
            "border":     "4B5563",
            "text_main":  "F9FAFB",
        }
    }
    palette = themes.get(theme, themes["corporate_blue"])

    # Sheet definitions and sidebar labels
    sheets_info = [
        ("Dashboard", "🏠 Dashboard"),
        ("Inputs",    "⚙️ Inputs"),
        ("Contacts",  "👥 Contacts")
    ]

    # 2. Setup Sheets
    for name, _ in sheets_info:
        wb.create_sheet(name)
    if "Sheet" in wb.sheetnames:
        del wb["Sheet"]

    # Reusable styles
    sidebar_fill = PatternFill("solid", fgColor=palette["sidebar_bg"])
    canvas_fill = PatternFill("solid", fgColor=palette["canvas_bg"])
    nav_font = Font(color=palette["sidebar_fg"], bold=True, size=11)
    center_align = Alignment(horizontal="center", vertical="center")

    def _draw_card(ws, min_col: int, min_row: int, max_col: int, max_row: int, card_title: str):
        """Helper to draw a UI card on the canvas using bordered white cells."""
        card_fill = PatternFill("solid", fgColor=palette["card_bg"])
        bd = Side(style="thin", color=palette["border"])
        
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = card_fill
                
                # Apply perimeter borders only
                b_top = bd if r == min_row else None
                b_bot = bd if r == max_row else None
                b_lft = bd if c == min_col else None
                b_rgt = bd if c == max_col else None
                
                if any([b_top, b_bot, b_lft, b_rgt]):
                    cell.border = Border(top=b_top, bottom=b_bot, left=b_lft, right=b_rgt)

        # Insert Card Title
        tc = ws.cell(row=min_row + 1, column=min_col + 1, value=card_title)
        tc.font = Font(color=palette["text_main"], bold=True, size=12)

    # 3. Apply Shell Layout to all sheets
    for sheet_name, _ in sheets_info:
        ws = wb[sheet_name]
        ws.sheet_view.showGridLines = False

        # Paint Canvas (Rows 1-40, Cols B-P)
        for r in range(1, 41):
            for c in range(2, 17):
                ws.cell(row=r, column=c).fill = canvas_fill

        # Paint Sidebar (Col A, Rows 1-40)
        ws.column_dimensions['A'].width = 16
        for r in range(1, 41):
            ws.cell(row=r, column=1).fill = sidebar_fill

        # Set Sheet Header Title
        title_cell = ws.cell(row=2, column=3, value=f"{title} - {sheet_name}")
        title_cell.font = Font(color=palette["sidebar_bg"], size=20, bold=True)

        # Insert Interactive Navigation Links
        for idx, (link_sheet, link_label) in enumerate(sheets_info):
            row_idx = 6 + (idx * 3)  # Spacing out the links
            nav_cell = ws.cell(row=row_idx, column=1, value=link_label)
            nav_cell.font = nav_font
            nav_cell.alignment = center_align
            # Link jumps directly to A1 of the target sheet
            nav_cell.hyperlink = f"#'{link_sheet}'!A1"

        # 4. Generate Cards on the Dashboard View
        if sheet_name == "Dashboard":
            # Top KPI Row (3 evenly spaced blocks)
            _draw_card(ws, 3,  5,  6, 12, "Sales ($)")
            _draw_card(ws, 8,  5, 11, 12, "Profit ($)")
            _draw_card(ws, 13, 5, 16, 12, "Customers (#)")

            # Bottom Visuals Row (Asymmetrical layout for charts)
            _draw_card(ws, 3,  14, 9,  28, "2021-2022 Sales Trend")
            _draw_card(ws, 11, 14, 16, 28, "Customer Satisfaction")
```