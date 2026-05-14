### 1. High-level Skill Pattern Extraction

> **Skill Name**: Grid-Based Card Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Paints the entire worksheet grid a base background color to hide the default cell appearance, then maps specific bounding box ranges and fills them white. It applies asymmetrical border weights (thin top/left, medium bottom/right) to simulate a UI drop-shadow, creating robust "cards" using native cells rather than fragile floating shapes.
* **Applicability**: Perfect for executive summaries, KPI dashboards, and automated report generation where you need a modern web-app aesthetic but require the stability of cell grids to anchor charts and text safely.

### 2. Structural Breakdown

- **Data Layout**: Uses standardized column widths (12 for content, 4 for margins) to create a responsive-feeling grid layout.
- **Formula Logic**: None required; structure relies purely on layout dimensions.
- **Visual Design**: Uses a Tailwind-inspired palette (Gray-100 background, White cards, Blue-900 accents). Card edges use conditional border sides to emulate depth. Gridlines are explicitly disabled.
- **Charts/Tables**: Leaves designated anchor ranges with centered placeholder text, guiding the subsequent injection of Doughnut or Line charts. 
- **Theme Hooks**: Consumes `bg_color` (canvas), `card_color` (panels), `text_color` (primary figures), `accent_color` (headers), and `shadow_color` (borders). 

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Border, Side, Font, Alignment
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # Hide gridlines for a clean canvas
    ws.sheet_view.showGridLines = False
    
    # Fallback modern palette (can be overridden by theme dict in production)
    bg_color = "F3F4F6"     # Light gray background
    card_color = "FFFFFF"   # White cards
    text_color = "1F2937"   # Dark slate for text
    accent_color = "1E3A8A" # Dark blue for headers
    shadow_color = "D1D5DB" # Slightly darker gray for faux-shadow borders
    light_border = "E5E7EB" # Light gray for standard card edges
    
    # 1. Paint background and set uniform column widths
    base_fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    
    for col_idx in range(1, 15):
        col_letter = get_column_letter(col_idx)
        # Columns A, E, I, M act as gutters/margins
        if col_idx in [1, 5, 9, 13]: 
            ws.column_dimensions[col_letter].width = 4
        else: 
            # Content columns
            ws.column_dimensions[col_letter].width = 12

    # Paint the entire visible workspace
    for row in ws.iter_rows(min_row=1, max_row=30, min_col=1, max_col=14):
        for cell in row:
            cell.fill = base_fill

    # 2. Add Dashboard Title
    ws.row_dimensions[1].height = 40
    ws["B1"] = title
    ws["B1"].font = Font(size=22, bold=True, color=text_color)
    ws["B1"].alignment = Alignment(vertical="center")
    
    # 3. Define the Grid Layout for Cards
    # Format: (min_col, min_row, max_col, max_row, card_title)
    cards = [
        (2, 3, 4, 7, "Total Sales"),             # KPI 1
        (6, 3, 8, 7, "Total Profit"),            # KPI 2
        (10, 3, 12, 7, "Total Customers"),       # KPI 3
        (2, 9, 8, 22, "2021-2022 Sales Trend"),  # Main Wide Chart
        (10, 9, 12, 22, "Customer Satisfaction") # Side Tall Chart
    ]
    
    card_fill = PatternFill(start_color=card_color, end_color=card_color, fill_type="solid")
    
    for min_col, min_row, max_col, max_row, card_title in cards:
        # Fill card area and apply outer borders to simulate depth
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = card_fill
                
                # Assign borders strictly to the perimeter of the designated block
                b_top = Side(style="thin", color=light_border) if r == min_row else None
                b_bottom = Side(style="medium", color=shadow_color) if r == max_row else None
                b_left = Side(style="thin", color=light_border) if c == min_col else None
                b_right = Side(style="medium", color=shadow_color) if c == max_col else None
                
                cell.border = Border(top=b_top, bottom=b_bottom, left=b_left, right=b_right)
                
        # Format Card Title row (adds a bottom separator line without breaking perimeter borders)
        for c in range(min_col, max_col + 1):
            tc = ws.cell(row=min_row, column=c)
            tc.border = Border(
                top=tc.border.top,
                bottom=Side(style="thin", color=light_border),
                left=tc.border.left,
                right=tc.border.right
            )
            
        title_cell = ws.cell(row=min_row, column=min_col)
        title_cell.value = card_title
        title_cell.font = Font(size=12, bold=True, color=accent_color)
        title_cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        
        # Merge the header row to keep text constrained
        ws.merge_cells(start_row=min_row, start_column=min_col, end_row=min_row, end_column=max_col)
        
        # Add placeholder text or dummy numbers inside the cards
        if max_row - min_row <= 5: 
            # Small KPI Card
            content_cell = ws.cell(row=min_row + 2, column=min_col + 1)
            content_cell.value = "$2,544M" if "Sales" in card_title else "$890M" if "Profit" in card_title else "87.0"
            content_cell.font = Font(size=24, bold=True, color=text_color)
            content_cell.alignment = Alignment(horizontal="center", vertical="center")
        else: 
            # Large Chart Card
            mid_col = min_col + (1 if max_col - min_col < 4 else 3)
            content_cell = ws.cell(row=min_row + 6, column=mid_col)
            content_cell.value = "[ Insert Chart Here ]"
            content_cell.font = Font(size=14, italic=True, color="9CA3AF")
            content_cell.alignment = Alignment(horizontal="center", vertical="center")

    # Clean up default sheet if present
    if "Sheet" in wb.sheetnames and len(wb.sheetnames) > 1:
        del wb["Sheet"]
```