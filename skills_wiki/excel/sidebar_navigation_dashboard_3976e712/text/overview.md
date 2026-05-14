```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Sidebar Navigation Dashboard

* **Tier**: archetype
* **Core Mechanism**: Creates an app-like multi-sheet workbook architecture. It uses a narrow, dark-filled Column A as a universal sidebar across all sheets, containing hyperlink-enabled icon cells to navigate between tabs. The main content area utilizes contrasting background fills and edge-only borders to create distinct "cards" that simulate container shapes.
* **Applicability**: Ideal for interactive reports, financial models, or executive dashboards where users need to seamlessly jump between a high-level summary view, data inputs, and settings/contacts.

### 2. Structural Breakdown

- **Data Layout**: Multi-sheet structure. Column A acts as the static sidebar (width 8). Columns B-M serve as the main canvas (width 12).
- **Formula Logic**: Utilizes `cell.hyperlink = "#'Sheet Name'!A1"` to create interactive navigation buttons.
- **Visual Design**: The sidebar uses a deep primary theme color (e.g., dark blue), with the active sheet indicated by a lighter highlight fill. The dashboard background uses a light gray fill, making white "cards" visually pop.
- **Charts/Tables**: Card areas are designated for specific elements (Top row for KPIs, bottom rows for charts).
- **Theme Hooks**: Requires `sidebar_bg`, `sidebar_active`, `dash_bg`, `card_bg`, and `text_accent` (handled via fallbacks in the code).

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def render_workbook(wb: openpyxl.Workbook, *, sheets: list[str] = ["Dashboard", "Inputs", "Settings"], theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Setup Theme Colors
    sidebar_fill = PatternFill("solid", fgColor="1F4E78")  # Dark blue
    active_fill = PatternFill("solid", fgColor="2F75B5")   # Lighter blue highlight
    dash_bg_fill = PatternFill("solid", fgColor="F2F2F2")  # Light gray background
    card_fill = PatternFill("solid", fgColor="FFFFFF")     # White cards
    text_color = "FFFFFF"
    
    # Simple Unicode icons for the sidebar
    icons = {
        "Dashboard": "🏠",
        "Inputs": "✏️",
        "Settings": "⚙️",
        "Contacts": "✉️"
    }

    # Clean default sheet
    if "Sheet" in wb.sheetnames:
        del wb["Sheet"]

    # Ensure all target sheets exist
    for sheet_name in sheets:
        if sheet_name not in wb.sheetnames:
            wb.create_sheet(title=sheet_name)

    # Helper function to create elevated "cards" using cells and borders
    def create_card(ws, start_row, start_col, end_row, end_col):
        side = Side(style='thin', color='D9D9D9')
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = card_fill
                # Apply borders only to the outer perimeter of the card range
                cell.border = Border(
                    top=side if r == start_row else None,
                    bottom=side if r == end_row else None,
                    left=side if c == start_col else None,
                    right=side if c == end_col else None
                )

    # 2. Build the Layout across all sheets
    for sheet_name in sheets:
        ws = wb[sheet_name]
        ws.sheet_view.showGridLines = False
        
        # Grid sizing
        ws.column_dimensions['A'].width = 8
        for col in "BCDEFGHIJKLM":
            ws.column_dimensions[col].width = 12
            
        # Canvas Background Fill
        for row in range(1, 35):
            for col in range(2, 14):
                ws.cell(row=row, column=col).fill = dash_bg_fill
                
        # Sidebar Fill
        for row in range(1, 35):
            ws.cell(row=row, column=1).fill = sidebar_fill

        # Render Navigation Links
        start_row = 4
        for idx, target_sheet in enumerate(sheets):
            center_row = start_row + (idx * 4)
            cell = ws.cell(row=center_row, column=1)
            cell.value = icons.get(target_sheet, "▪")
            cell.font = Font(color=text_color, size=20)
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.hyperlink = f"#'{target_sheet}'!A1"
            
            # Indicate active sheet with a highlight block
            if target_sheet == sheet_name:
                for r_adj in [-1, 0, 1]:
                    ws.cell(row=center_row + r_adj, column=1).fill = active_fill

        # 3. Apply specific layouts depending on the active sheet
        if sheet_name == sheets[0]:  # Primary Dashboard View
            ws.cell(row=2, column=2, value="Sales Dashboard").font = Font(size=24, bold=True, color="1F4E78")
            
            # KPI Cards (Top Row)
            create_card(ws, start_row=4, start_col=2, end_row=8, end_col=4)
            ws.cell(row=5, column=2, value="Total Sales").font = Font(bold=True, color="595959")
            ws.cell(row=6, column=2, value="$2,544M").font = Font(size=20, bold=True, color="1F4E78")
            
            create_card(ws, start_row=4, start_col=6, end_row=8, end_col=8)
            ws.cell(row=5, column=6, value="Total Profit").font = Font(bold=True, color="595959")
            ws.cell(row=6, column=6, value="$890M").font = Font(size=20, bold=True, color="1F4E78")

            create_card(ws, start_row=4, start_col=10, end_row=8, end_col=12)
            ws.cell(row=5, column=10, value="Total Customers").font = Font(bold=True, color="595959")
            ws.cell(row=6, column=10, value="87.0M").font = Font(size=20, bold=True, color="1F4E78")

            # Main Chart Containers
            create_card(ws, start_row=10, start_col=2, end_row=22, end_col=7)
            ws.cell(row=11, column=2, value="Sales Trend Over Time").font = Font(bold=True, color="595959")
            
            create_card(ws, start_row=10, start_col=9, end_row=22, end_col=12)
            ws.cell(row=11, column=9, value="Sales by Region").font = Font(bold=True, color="595959")
            
        else:  # Secondary Sheets (Inputs, Settings, etc.)
            ws.cell(row=2, column=2, value=f"{sheet_name}").font = Font(size=24, bold=True, color="1F4E78")
            create_card(ws, start_row=4, start_col=2, end_row=28, end_col=12)
            ws.cell(row=5, column=3, value=f"Data and configuration for {sheet_name} goes here...").font = Font(italic=True, color="595959")
```
```