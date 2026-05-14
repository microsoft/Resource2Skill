### 1. High-level Skill Pattern Extraction

> **Skill Name**: App-Style Navigation Dashboard

* **Tier**: archetype
* **Core Mechanism**: Builds a multi-sheet workbook where every sheet features a consistent left-hand sidebar containing hyperlinks to all other sheets. The main content area is styled with a soft background, and a helper routine punches out white, bordered "cards" to neatly enclose KPIs and charts. 
* **Applicability**: Ideal for creating premium, web-app-like reporting packages. It replaces standard Excel tab navigation with a unified sidebar, giving the output a software-like feel. Best used when a workbook has a few primary interactive sections (e.g., Dashboard, Data Inputs, Contacts).

### 2. Structural Breakdown

- **Data Layout**: 
  - **Column A**: Sidebar container (width 18).
  - **Column B**: Gutter/spacer (width 2).
  - **Columns C+**: Main content grid for widgets.
- **Formula Logic**: Uses `cell.hyperlink = f"#'{sheet_name}'!A1"` to create native, macro-free navigation buttons that jump between tabs.
- **Visual Design**: Gridlines are disabled. The active sidebar tab is highlighted with a distinct background fill. The helper function simulates the video's floating shape layout by applying white fills and perimeter borders to specific cell blocks.
- **Theme Hooks**: Consumes `sidebar_bg`, `sidebar_fg`, `canvas_bg`, `card_bg`, and `border` to ensure colors match the corporate branding.

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

def render_workbook(wb, *, title: str = "Sales Dashboard", tabs: list = None, theme: str = "corporate_blue", **kwargs) -> None:
    if not tabs:
        tabs = ["Dashboard", "Inputs", "Contacts"]
        
    # Standard theme fallback colors
    theme_colors = {
        "sidebar_bg": "1A365D", # Dark Navy
        "sidebar_fg": "FFFFFF", # White
        "canvas_bg": "EDF2F7",  # Light Gray/Blue
        "card_bg": "FFFFFF",    # White
        "border": "E2E8F0",     # Light Gray
        "text_main": "2D3748"   # Dark Gray
    }
    
    fill_sidebar = PatternFill(start_color=theme_colors["sidebar_bg"], fill_type="solid")
    fill_canvas = PatternFill(start_color=theme_colors["canvas_bg"], fill_type="solid")
    fill_card = PatternFill(start_color=theme_colors["card_bg"], fill_type="solid")
    fill_active = PatternFill(start_color="2B6CB0", fill_type="solid") # Lighter highlight
    
    font_nav = Font(color=theme_colors["sidebar_fg"], bold=True, size=11)
    font_title = Font(color=theme_colors["sidebar_bg"], bold=True, size=20)
    font_card_title = Font(color=theme_colors["text_main"], bold=True, size=12)
    
    align_left = Alignment(horizontal="left", vertical="center")
    
    # Store default sheets to clean up later
    sheets_to_remove = wb.sheetnames
        
    for tab in tabs:
        ws = wb.create_sheet(title=tab)
        ws.sheet_view.showGridLines = False
        
        # 1. Paint the Canvas
        for row in range(1, 40):
            for col in range(1, 20):
                ws.cell(row=row, column=col).fill = fill_canvas
                
        # 2. Build Sidebar (Col A)
        ws.column_dimensions['A'].width = 18
        for row in range(1, 40):
            ws.cell(row=row, column=1).fill = fill_sidebar
            
        # 3. Add Navigation Links
        start_row = 6
        for i, nav_tab in enumerate(tabs):
            cell = ws.cell(row=start_row + i*3, column=1)
            cell.value = f"   {nav_tab}" # Indent slightly
            cell.font = font_nav
            cell.alignment = align_left
            cell.hyperlink = f"#'{nav_tab}'!A1"
            
            # Highlight active tab
            if nav_tab == tab:
                cell.fill = fill_active
                
        # 4. Content Area Layout
        ws.column_dimensions['B'].width = 2 # Spacer
        ws.cell(row=2, column=3, value=title).font = font_title
        
        def apply_card(min_r, min_c, max_r, max_c, card_title=""):
            """Helper to punch out a styled 'card' region on the canvas."""
            for r in range(min_r, max_r + 1):
                for c in range(min_c, max_c + 1):
                    cell = ws.cell(row=r, column=c)
                    cell.fill = fill_card
                    
                    # Apply borders strictly to the perimeter of the block
                    top_side = Side(style='thin', color=theme_colors["border"]) if r == min_r else None
                    bottom_side = Side(style='thin', color=theme_colors["border"]) if r == max_r else None
                    left_side = Side(style='thin', color=theme_colors["border"]) if c == min_c else None
                    right_side = Side(style='thin', color=theme_colors["border"]) if c == max_c else None
                    
                    cell.border = Border(top=top_side, bottom=bottom_side, left=left_side, right=right_side)
            
            if card_title:
                ws.cell(row=min_r + 1, column=min_c + 1, value=card_title).font = font_card_title

        # Build an example layout on the primary Dashboard tab
        if tab == tabs[0]:
            # Three KPI Cards at the top
            apply_card(4, 3, 8, 6, "Sales")
            apply_card(4, 8, 8, 11, "Profit")
            apply_card(4, 13, 8, 16, "Customers")
            
            # Two large visual containers below
            apply_card(10, 3, 22, 9, "Sales Trend")
            apply_card(10, 11, 22, 16, "Customer Satisfaction")

    # Clean up default sheets
    for sheet in sheets_to_remove:
        if sheet in wb:
            del wb[sheet]
```