### 1. High-level Skill Pattern Extraction

> **Skill Name**: Sidebar Dashboard Grid Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Simulates the clean, floating "card" layout seen in modern dashboards using cell background formatting rather than brittle Shape objects. It disables default gridlines, paints a light gray canvas, defines a dark navigation sidebar, and draws distinct white ranges with subtle perimenter borders to act as layout containers for KPIs and charts.
* **Applicability**: Use as the foundational canvas for any high-level executive dashboard, KPI tracker, or data application where clean spatial organization and visual hierarchy are required.

### 2. Structural Breakdown

- **Data Layout**: Utilizes a strict column grid structure to ensure alignment. Column A is the sidebar. Column B is a gutter. Columns C through N form a 12-column internal grid for precise card placement (e.g., three 4-column KPI cards). 
- **Formula Logic**: N/A (Structural shell).
- **Visual Design**: Hides native Excel gridlines (`showGridLines = False`). Uses high-contrast backgrounds: Slate/Dark Blue for the sidebar, Light Gray (e.g., `#F3F4F6`) for the negative space, and Pure White (`#FFFFFF`) for the content cards.
- **Charts/Tables**: Provides designated blank canvas areas configured to host charts or dynamic metrics injected later.
- **Theme Hooks**: Utilizes structural colors rather than standard accents: deep darks for the sidebar, off-whites for the app background, and subtle grays for card borders.

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str = "Dashboard", *, title: str = "Regional Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Creates a modern, card-based dashboard layout using cell formatting to simulate UI containers.
    """
    ws = wb.create_sheet(sheet_name)
    
    # Crucial for a clean dashboard look
    ws.sheet_view.showGridLines = False

    # Theme-inspired structural colors
    colors = {
        "bg_app": "F3F4F6",      # Tailwind Gray 100
        "bg_sidebar": "1E293B",  # Tailwind Slate 800
        "bg_card": "FFFFFF",     # White
        "border_card": "D1D5DB", # Tailwind Gray 300
        "text_title": "111827",  # Tailwind Gray 900
        "text_header": "4B5563"  # Tailwind Gray 600
    }

    fill_app = PatternFill(start_color=colors["bg_app"], end_color=colors["bg_app"], fill_type="solid")
    fill_sidebar = PatternFill(start_color=colors["bg_sidebar"], end_color=colors["bg_sidebar"], fill_type="solid")

    # 1. Paint the entire visible canvas with the app background color
    for row in ws.iter_rows(min_row=1, max_row=40, min_col=1, max_col=20):
        for cell in row:
            cell.fill = fill_app

    # 2. Paint the left sidebar
    for row in ws.iter_rows(min_row=1, max_row=40, min_col=1, max_col=1):
        for cell in row:
            cell.fill = fill_sidebar
    
    # 3. Configure Grid Dimensions
    ws.column_dimensions['A'].width = 8   # Sidebar
    ws.column_dimensions['B'].width = 3   # Left Gutter
    
    # Create a standard 12-column grid (Columns C through N)
    for col in range(3, 15):
        ws.column_dimensions[get_column_letter(col)].width = 12

    # Set row heights for vertical rhythm
    ws.row_dimensions[1].height = 15  # Top Gutter
    ws.row_dimensions[2].height = 30  # Title Row
    ws.row_dimensions[4].height = 15  # Spacing
    ws.row_dimensions[5].height = 25  # KPI Header
    ws.row_dimensions[6].height = 40  # KPI Value
    ws.row_dimensions[7].height = 20  # KPI Subtext
    ws.row_dimensions[8].height = 15  # Spacing

    def draw_card(ws, min_col: int, min_row: int, max_col: int, max_row: int, card_title: str, is_main_title: bool = False):
        """Helper to draw a white container with a subtle perimeter border."""
        fill_card = PatternFill(start_color=colors["bg_card"], end_color=colors["bg_card"], fill_type="solid")
        thin_border = Side(border_style="thin", color=colors["border_card"])
        
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = fill_card
                
                # Apply border only to the outer perimeter of the card range
                top = thin_border if r == min_row else None
                bottom = thin_border if r == max_row else None
                left = thin_border if c == min_col else None
                right = thin_border if c == max_col else None
                
                cell.border = Border(top=top, bottom=bottom, left=left, right=right)

        # Inject and format the card title
        title_cell = ws.cell(row=min_row, column=min_col)
        title_cell.value = f"  {card_title}" # Padding hack
        
        if is_main_title:
            title_cell.font = Font(name="Calibri", size=18, bold=True, color=colors["text_title"])
            title_cell.alignment = Alignment(vertical="center", horizontal="left")
        else:
            title_cell.font = Font(name="Calibri", size=11, bold=True, color=colors["text_header"])
            title_cell.alignment = Alignment(vertical="center", horizontal="left")

    # 4. Construct the Layout Grid
    
    # Header Card (Full width: cols 3 to 14)
    draw_card(ws, min_col=3, min_row=2, max_col=14, max_row=3, card_title=title, is_main_title=True)
    
    # KPI Row (3 blocks, 4 columns each)
    draw_card(ws, min_col=3, min_row=5, max_col=6, max_row=7, card_title="Total Revenue")
    draw_card(ws, min_col=7, min_row=5, max_col=10, max_row=7, card_title="Net Profit")
    draw_card(ws, min_col=11, min_row=5, max_col=14, max_row=7, card_title="Active Customers")
    
    # Content Row (1 large main chart area, 1 side chart area)
    draw_card(ws, min_col=3, min_row=9, max_col=10, max_row=24, card_title="Revenue Trend (YTD)")
    draw_card(ws, min_col=11, min_row=9, max_col=14, max_row=16, card_title="Customer Satisfaction")
    draw_card(ws, min_col=11, min_row=17, max_col=14, max_row=24, card_title="Sales by Region")

    # Ensure the dashboard is the active, left-most sheet
    wb.active = ws
    if sheet_name != wb.sheetnames[0]:
        wb.move_sheet(ws, offset=-wb.index(ws))
```