### 1. High-level Skill Pattern Extraction

> **Skill Name**: Modern Sidebar Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Simulates a modern web app UI by replacing fragile floating shapes with styled cell grids. It creates a fixed dark sidebar with navigation hyperlinks, a muted main background, and white "card" regions bordered to hold KPIs and charts. 
* **Applicability**: Best used for executive summaries or interactive reporting portals where you want to hide standard Excel gridlines and provide a structured, app-like navigation experience.

### 2. Structural Breakdown

- **Data Layout**: Column A is narrowed (width 8) to act as the navigation sidebar. Columns B through N act as the responsive main area grid. Additional helper sheets (`Inputs`, `Contacts`) are targeted by the sidebar links.
- **Formula Logic**: Utilizes `Hyperlink` references attached directly to cell objects in the sidebar to create interactive document navigation without macros.
- **Visual Design**: The entire worksheet grid is first painted with a muted light gray/blue fill. White cell blocks are overlaid using exact `Border` perimeter logic to simulate the "floating tile" look from the tutorial.
- **Charts/Tables**: Line charts and KPI visuals placed in the tiles are stripped of their native backgrounds and borders (`noFill=True`) so they visually sink into the simulated white cards.
- **Theme Hooks**: Consumes `sidebar_bg`, `bg_main`, `card_bg`, and `accent` colors to maintain strict contrast between the navigation layer, the canvas, and the container cards.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import LineChart, Reference
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Setup Sheet and Hide Gridlines
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)
    
    ws.sheet_view.showGridLines = False

    # Theme palette fallback
    theme_colors = {
        "corporate_blue": {
            "sidebar_bg": "1E293B",  # Slate 800
            "sidebar_fg": "FFFFFF",  # White
            "bg_main": "F1F5F9",     # Slate 100
            "card_bg": "FFFFFF",     # White
            "border": "CBD5E1",      # Slate 300
            "text_main": "334155",   # Slate 700
            "text_accent": "2563EB"  # Blue 600
        }
    }.get(theme, {
        "sidebar_bg": "1E293B", "sidebar_fg": "FFFFFF", "bg_main": "F1F5F9",
        "card_bg": "FFFFFF", "border": "CBD5E1", "text_main": "334155", "text_accent": "2563EB"
    })

    # Styles
    fill_canvas = PatternFill("solid", fgColor=theme_colors["bg_main"])
    fill_sidebar = PatternFill("solid", fgColor=theme_colors["sidebar_bg"])
    fill_card = PatternFill("solid", fgColor=theme_colors["card_bg"])

    font_nav = Font(color=theme_colors["sidebar_fg"], size=16, bold=True)
    font_title = Font(color=theme_colors["text_main"], size=22, bold=True)
    font_card_hdr = Font(color=theme_colors["text_accent"], size=12, bold=True)

    align_center = Alignment(horizontal="center", vertical="center")
    
    bd_edge = Side(style="thin", color=theme_colors["border"])

    # 2. Paint Canvas
    for row in range(1, 40):
        for col in range(2, 16):
            ws.cell(row=row, column=col).fill = fill_canvas

    # 3. Setup Sidebar Navigation
    ws.column_dimensions['A'].width = 8
    for row in range(1, 40):
        c = ws.cell(row=row, column=1)
        c.fill = fill_sidebar
        c.alignment = align_center

    nav_items = [
        (3, "🏠", sheet_name),
        (5, "📊", "Inputs"),
        (7, "📞", "Contacts"),
        (9, "❓", "Help")
    ]

    for r, icon, target_sheet in nav_items:
        # Create dummy target sheets if they don't exist to prevent broken links
        if target_sheet not in wb.sheetnames:
            wb.create_sheet(target_sheet)
            
        nav_cell = ws.cell(row=r, column=1, value=icon)
        nav_cell.font = font_nav
        nav_cell.hyperlink = f"#'{target_sheet}'!A1"
        nav_cell.value = icon  # Re-assert value after hyperlink injection

    # 4. Standardize Column Widths for Canvas
    for col in range(2, 16):
        ws.column_dimensions[get_column_letter(col)].width = 11

    # 5. Dashboard Title
    ws.cell(row=2, column=2, value=title).font = font_title

    # 6. Card Drawing Helper
    def draw_card(start_row, start_col, end_row, end_col, card_title):
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = fill_card
                # Apply perimeter borders only
                top = bd_edge if r == start_row else None
                bottom = bd_edge if r == end_row else None
                left = bd_edge if c == start_col else None
                right = bd_edge if c == end_col else None
                cell.border = Border(top=top, bottom=bottom, left=left, right=right)

        hdr_cell = ws.cell(row=start_row, column=start_col + 1, value=card_title)
        hdr_cell.font = font_card_hdr
        hdr_cell.alignment = Alignment(vertical="center")

    # 7. Render Card Layout
    # Top KPI Row
    draw_card(4, 2, 7, 5, "Total Sales")
    draw_card(4, 6, 7, 9, "Net Profit")
    draw_card(4, 10, 7, 13, "Active Customers")
    
    # Add dummy KPI Values
    ws.cell(row=5, column=3, value="$2,544M").font = Font(size=20, bold=True, color=theme_colors["text_main"])
    ws.cell(row=5, column=7, value="$890M").font = Font(size=20, bold=True, color=theme_colors["text_main"])
    ws.cell(row=5, column=11, value="87.0M").font = Font(size=20, bold=True, color=theme_colors["text_main"])

    # Middle Row Containers
    draw_card(9, 2, 22, 8, "2021-2022 Sales Trend (in millions)")
    draw_card(9, 9, 22, 13, "Customer Satisfaction")

    # 8. Inject Chart without background (Seamless integration into the card)
    inputs_ws = wb["Inputs"]
    sample_data = [("Jan", 201), ("Feb", 204), ("Mar", 198), ("Apr", 199), ("May", 206)]
    for idx, (mon, val) in enumerate(sample_data, 1):
        inputs_ws.cell(row=idx, column=1, value=mon)
        inputs_ws.cell(row=idx, column=2, value=val)

    chart = LineChart()
    data = Reference(inputs_ws, min_col=2, min_row=1, max_row=5)
    cats = Reference(inputs_ws, min_col=1, min_row=1, max_row=5)
    chart.add_data(data)
    chart.set_categories(cats)
    chart.legend = None

    # Crucial: Strip chart background/border to match the simulated card aesthetic
    chart.graphical_properties = GraphicalProperties(noFill=True)
    chart.graphical_properties.line = LineProperties(noFill=True)

    ws.add_chart(chart, "B10")
```