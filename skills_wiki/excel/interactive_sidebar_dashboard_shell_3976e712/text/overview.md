### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive Sidebar Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Establishes a modern, "app-like" layout in Excel by setting a continuous canvas background color and disabling gridlines. It constructs a fixed-width left-hand navigation sidebar loaded with internal workbook hyperlinks, and draws blank "card" regions (white fill, thin borders) to house charts and KPIs seamlessly.
* **Applicability**: Ideal for executive dashboards, reports requiring multiple views (sheets), or any workbook intended to feel like a standalone interactive application rather than a raw spreadsheet grid.

### 2. Structural Breakdown

- **Data Layout**: Column A acts as the navigation sidebar. Column B is a margin spacer. Columns C through P contain a grid of merged cell regions acting as container "cards". 
- **Formula Logic**: Uses internal cell hyperlinks (`#'SheetName'!A1`) to allow click-to-navigate functionality between different dashboard tabs.
- **Visual Design**: Hides native Excel gridlines (`showGridLines = False`). Uses a dark primary color for the sidebar, a light gray for the canvas, and crisp white with subtle gray borders for the content cards. 
- **Charts/Tables**: Prepares the structural UI zones; actual charts or PivotTables would be anchored to the top-left cells of these card regions.
- **Theme Hooks**: Utilizes `sidebar_bg` (dark brand color), `sidebar_fg` (white/light), `canvas_bg` (light neutral), and `card_border` (subtle gray) to lock the layout into the overarching corporate theme.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def render_sheet(wb, sheet_name: str, *, title: str = "South America Sales Dashboard 2022", nav_links: dict = None, cards: list = None, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Builds a modern dashboard layout with a navigation sidebar and content cards.
    
    :param nav_links: Dict mapping display text -> target sheet name.
    :param cards: List of dicts defining card regions, e.g., [{"label": "Sales", "bounds": (min_r, min_c, max_r, max_c)}]
    """
    # 1. Initialize sheet and disable gridlines for a clean UI
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)
    
    ws.sheet_view.showGridLines = False

    # Minimal inline theme dictionary (framework themes would override this)
    colors = {
        "sidebar_bg": "1F3864",  # Dark Blue
        "sidebar_fg": "FFFFFF",  # White
        "canvas_bg": "F3F3F3",   # Light Gray
        "card_bg": "FFFFFF",     # White
        "card_border": "D9D9D9", # Subtle Gray
        "text_main": "1F3864",
        "text_sub": "595959"
    }

    fill_canvas = PatternFill("solid", fgColor=colors["canvas_bg"])
    fill_sidebar = PatternFill("solid", fgColor=colors["sidebar_bg"])
    fill_card = PatternFill("solid", fgColor=colors["card_bg"])

    # 2. Paint the Background Canvas
    for row in ws.iter_rows(min_row=1, max_row=40, min_col=1, max_col=20):
        for cell in row:
            cell.fill = fill_canvas

    # 3. Build the Navigation Sidebar (Column A)
    ws.column_dimensions['A'].width = 15
    for row in range(1, 41):
        ws.cell(row=row, column=1).fill = fill_sidebar

    if nav_links is None:
        nav_links = {
            "🏠 Dashboard": "Dashboard", 
            "📊 Data Inputs": "Inputs", 
            "📞 Contacts": "Contacts"
        }

    start_row = 5
    for text, target_sheet in nav_links.items():
        nav_cell = ws.cell(row=start_row, column=1, value=text)
        nav_cell.font = Font(color=colors["sidebar_fg"], bold=True)
        nav_cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        # Create an internal hyperlink to the target sheet
        nav_cell.hyperlink = f"#'{target_sheet}'!A1"
        start_row += 3

    # 4. Add Dashboard Title & Subtitle
    ws.column_dimensions['B'].width = 3 # Spacer column
    
    title_cell = ws.cell(row=2, column=3, value=title)
    title_cell.font = Font(size=20, bold=True, color=colors["text_main"])
    
    sub_cell = ws.cell(row=3, column=3, value="Figures in millions of USD")
    sub_cell.font = Font(size=10, italic=True, color=colors["text_sub"])

    # 5. Create Card Containers (Simulates the floating rounded shapes from the video)
    if cards is None:
        cards = [
            {"label": "Sales", "bounds": (5, 3, 9, 6)},
            {"label": "Profit", "bounds": (5, 8, 9, 11)},
            {"label": "# of Customers", "bounds": (5, 13, 9, 16)},
            {"label": "2021-2022 Sales Trend", "bounds": (11, 3, 25, 11)},
            {"label": "Customer Satisfaction", "bounds": (11, 13, 25, 16)}
        ]

    for card in cards:
        r_min, c_min, r_max, c_max = card["bounds"]
        
        # Merge the inner area so it acts as a single blank canvas for charts
        # We start the merge on r_min + 1 to leave the top row for the card label
        ws.merge_cells(start_row=r_min + 1, start_column=c_min, end_row=r_max, end_column=c_max)
        
        for r in range(r_min, r_max + 1):
            for c in range(c_min, c_max + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = fill_card
                
                # Apply borders exclusively to the outer perimeter of the card
                b_top = Side(style="thin", color=colors["card_border"]) if r == r_min else None
                b_bottom = Side(style="thin", color=colors["card_border"]) if r == r_max else None
                b_left = Side(style="thin", color=colors["card_border"]) if c == c_min else None
                b_right = Side(style="thin", color=colors["card_border"]) if c == c_max else None
                
                cell.border = Border(top=b_top, bottom=b_bottom, left=b_left, right=b_right)
        
        # Inject Card Label
        label_cell = ws.cell(row=r_min, column=c_min, value=card.get("label", ""))
        label_cell.font = Font(bold=True, size=12, color=colors["text_main"])
        label_cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
```