### 1. High-level Skill Pattern Extraction

> **Skill Name**: App-like Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Builds an application-style dashboard layout by narrowing the first column into a dark navigation sidebar with hyperlinked icons. The main canvas hides gridlines and uses a light gray background, overlaying stark white cell ranges with subtle borders to simulate elevated "cards" for charts and KPIs.
* **Applicability**: Ideal for executive summaries, financial models, or any multi-sheet reporting workbook where user navigation and clear visual separation of metrics are required.

### 2. Structural Breakdown

- **Data Layout**: 
  - **Column A**: Navigation sidebar (width 8, rows 1-30).
  - **Columns C-E, G-I, K-M**: White "card" regions for KPIs and charts.
  - **Columns B, F, J**: Narrow spacer columns (width 4) to provide visual gutters between cards.
- **Formula Logic**: Uses Excel internal hyperlinks (e.g., `#Inputs!A1`) attached to sidebar cells to simulate app navigation.
- **Visual Design**: 
  - **Sidebar**: Dark blue background, white centered icons.
  - **Canvas**: Light gray fill over the entire main area with sheet gridlines explicitly disabled.
  - **Cards**: White background with a thin light-gray outer border to simulate a drop-shadow/elevation effect.
- **Charts/Tables**: This shell provides the mounting points (the white cards) for subsequent chart or table components to be injected.
- **Theme Hooks**: Consumes `primary_bg` for the sidebar, `canvas_bg` for the backdrop, and `card_bg` for the mount points.

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import range_boundaries

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders an app-like dashboard layout with a navigation sidebar and structured KPI cards.
    """
    ws = wb.create_sheet(sheet_name)
    
    # Hide gridlines for a clean app UI
    ws.sheet_view.showGridLines = False

    # Standard fallback palette mapping
    palette = {
        "sidebar_bg": "002060",  # Dark Blue
        "sidebar_fg": "FFFFFF",  # White
        "canvas_bg": "F2F2F2",   # Light Gray
        "card_bg": "FFFFFF",     # White
        "border": "D9D9D9",      # Light Gray Border
        "text_sub": "595959"     # Dark Gray Subtitle
    }

    sidebar_fill = PatternFill("solid", fgColor=palette["sidebar_bg"])
    canvas_fill = PatternFill("solid", fgColor=palette["canvas_bg"])
    card_fill = PatternFill("solid", fgColor=palette["card_bg"])

    # 1. Size columns for gutters and cards
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 4
    ws.column_dimensions['F'].width = 4
    ws.column_dimensions['J'].width = 4
    
    for col in ["C", "D", "E", "G", "H", "I", "K", "L", "M"]:
        ws.column_dimensions[col].width = 12

    # 2. Paint the main canvas light gray
    for row in range(1, 30):
        for col in range(2, 15):
            ws.cell(row=row, column=col).fill = canvas_fill

    # 3. Paint the sidebar dark blue
    for row in range(1, 30):
        cell = ws.cell(row=row, column=1)
        cell.fill = sidebar_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # 4. Add Dashboard Headers
    title_cell = ws.cell(row=2, column=3, value=title)
    title_cell.font = Font(size=20, bold=True, color=palette["sidebar_bg"])
    
    subtitle_cell = ws.cell(row=3, column=3, value="Figures in millions of USD")
    subtitle_cell.font = Font(size=11, italic=True, color=palette["text_sub"])

    # 5. Create Card Areas (simulating floating shapes)
    card_ranges = [
        "C4:E8",   # KPI 1
        "G4:I8",   # KPI 2
        "K4:M8",   # KPI 3
        "C10:I25", # Main Bottom Chart
        "K10:M25"  # Side Bottom Chart
    ]

    for cr in card_ranges:
        min_col, min_row, max_col, max_row = range_boundaries(cr)
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = card_fill
                
                # Apply outer border only to the perimeter of the card range
                b_top = Side(style='thin', color=palette["border"]) if r == min_row else None
                b_bottom = Side(style='thin', color=palette["border"]) if r == max_row else None
                b_left = Side(style='thin', color=palette["border"]) if c == min_col else None
                b_right = Side(style='thin', color=palette["border"]) if c == max_col else None
                
                cell.border = Border(top=b_top, bottom=b_bottom, left=b_left, right=b_right)

    # 6. Populate Interactive Sidebar Menu
    menu_items = kwargs.get("menu_items") or [
        {"target": f"{sheet_name}!A1", "icon": "🏠"},
        {"target": "Inputs!A1", "icon": "📥"},
        {"target": "Contacts!A1", "icon": "📞"},
        {"target": "Help!A1", "icon": "❓"}
    ]

    sidebar_font = Font(color=palette["sidebar_fg"], size=16, bold=True)
    start_row = 4
    for item in menu_items:
        cell = ws.cell(row=start_row, column=1, value=item["icon"])
        cell.font = sidebar_font
        cell.hyperlink = f"#{item['target']}"
        cell.alignment = Alignment(horizontal="center", vertical="center")
        start_row += 3
```