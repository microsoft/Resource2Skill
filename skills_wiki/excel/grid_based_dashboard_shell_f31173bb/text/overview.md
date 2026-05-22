### 1. High-level Skill Pattern Extraction

> **Skill Name**: Grid-Based Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Fills a worksheet with a solid dark base theme, disables gridlines, and draws multiple "card" panels using a 45-degree linear `GradientFill` on merged cell regions. Applies an outer border and title separator to each panel to define the container edges natively without floating vector shapes.
* **Applicability**: Ideal for the visual foundation of an executive dashboard. Use this layout to hold KPI values, sparklines, or act as background mounting targets for floating charts, emulating the look of vector shapes using native, robust cell formatting.

### 2. Structural Breakdown

- **Data Layout**: Defines a dynamic grid background range based on the maximum extents of the provided `cards` array.
- **Formula Logic**: None (purely layout and visual styling).
- **Visual Design**: Removes sheet gridlines and applies a linear `GradientFill` (top-left to bottom-right) to specific block ranges.
- **Charts/Tables**: Serves as the canvas/background for placing transparent charts.
- **Theme Hooks**: Uses custom dictionary overrides for `bg`, `card_top`, `card_bot`, `text`, and `card_border`.

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side, GradientFill
from openpyxl.utils import coordinate_to_tuple

def render_sheet(wb, sheet_name: str, *, title: str, cards: list[dict], theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a stylized dashboard background shell with gradient-filled card containers.
    
    :param cards: List of dictionaries defining the layout, e.g.:
                  [
                      {"anchor": "B5", "cols": 4, "rows": 4, "title": "TOTAL SALES"},
                      {"anchor": "G5", "cols": 4, "rows": 4, "title": "TOTAL PROFIT"},
                      {"anchor": "B10", "cols": 9, "rows": 12, "title": "Sales by Category"}
                  ]
    """
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    # Theme palette fallback
    palettes = {
        "corporate_blue": {
            "bg": "FF0A2B3E",          # Dark navy background
            "card_top": "FF1B6B93",    # Gradient start (darker teal/blue)
            "card_bot": "FF4FC0E8",    # Gradient end (lighter cyan)
            "card_border": "FF8ED8F8", # Subtle card outline
            "text": "FFFFFFFF",        # White text
            "title_bg": "FF041C2B"     # Slightly darker than bg for the header
        }
    }
    palette = palettes.get(theme, palettes["corporate_blue"])
    
    # 1. Determine dynamic canvas size
    max_r = 15
    max_c = 10
    for card in cards:
        r, c = coordinate_to_tuple(card["anchor"])
        max_r = max(max_r, r + card.get("rows", 6) + 2)
        max_c = max(max_c, c + card.get("cols", 4) + 2)
        
    # 2. Apply solid dashboard background
    bg_fill = PatternFill(start_color=palette["bg"], end_color=palette["bg"], fill_type="solid")
    for row in ws.iter_rows(min_row=1, max_row=max_r, min_col=1, max_col=max_c):
        for cell in row:
            cell.fill = bg_fill

    # 3. Add Dashboard Header
    ws.merge_cells("B2:K3")
    title_cell = ws["B2"]
    title_cell.value = title.upper()
    title_cell.font = Font(name="Segoe UI", size=24, bold=True, color=palette["text"])
    title_cell.alignment = Alignment(horizontal="left", vertical="center")
    
    title_bg_fill = PatternFill(start_color=palette["title_bg"], end_color=palette["title_bg"], fill_type="solid")
    for row in ws.iter_rows(min_row=2, max_row=3, min_col=2, max_col=11):
        for cell in row:
            cell.fill = title_bg_fill

    # 4. Render Gradient Cards
    card_fill = GradientFill(type="linear", degree=45, stop=(palette["card_top"], palette["card_bot"]))
    border_side = Side(style="thin", color=palette["card_border"])
    sep_side = Side(style="hair", color=palette["card_border"])
    
    for card in cards:
        anchor = card["anchor"]
        cols = card.get("cols", 4)
        rows = card.get("rows", 6)
        card_title = card.get("title", "")
        
        start_row, start_col = coordinate_to_tuple(anchor)
        end_row = start_row + rows - 1
        end_col = start_col + cols - 1
        
        # Apply fill and perimeter borders to the card area
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = card_fill
                
                # Calculate outer edges
                b_top = border_side if r == start_row else None
                b_bot = border_side if r == end_row else None
                b_left = border_side if c == start_col else None
                b_right = border_side if c == end_col else None
                
                # Add a subtle separator below the title row
                if r == start_row and card_title and rows > 1:
                    b_bot = sep_side
                    
                cell.border = Border(top=b_top, bottom=b_bot, left=b_left, right=b_right)
        
        # Add Card Title (merges the top row of the card)
        if card_title:
            if cols > 1:
                ws.merge_cells(start_row=start_row, start_column=start_col, end_row=start_row, end_column=end_col)
            ct_cell = ws.cell(row=start_row, column=start_col)
            ct_cell.value = card_title
            ct_cell.font = Font(name="Segoe UI", size=11, bold=True, color=palette["text"])
            ct_cell.alignment = Alignment(horizontal="center", vertical="center")
```