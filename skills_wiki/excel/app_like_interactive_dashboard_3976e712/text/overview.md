### 1. High-level Skill Pattern Extraction

> **Skill Name**: App-Like Interactive Dashboard

* **Tier**: archetype
* **Core Mechanism**: Constructs a multi-sheet workbook where every sheet shares a frozen, styled left-hand "sidebar" column containing internal hyperlink buttons. The main dashboard sheet disables standard gridlines and uses merged, bordered cell blocks to emulate a web-based card layout for KPIs and charts. 
* **Applicability**: Ideal for interactive executive summaries, financial models, or sales trackers where users need a primary dashboard view but also require seamless, application-like navigation to underlying data or input tabs without relying on Excel's default sheet tabs.

### 2. Structural Breakdown

- **Data Layout**: Multi-sheet structure ("Dashboard", "Inputs", "Contacts"). Column A serves as the universal navigation sidebar across all sheets. The "Dashboard" sheet utilizes a distinct grid layout (Columns C through M) for content cards.
- **Formula Logic**: Utilizes `HYPERLINK("#'SheetName'!A1", "Label")` internal linking to create clickable navigation buttons.
- **Visual Design**: The sidebar uses a dark primary fill with bold, centered white text. The dashboard canvas hides standard gridlines. Content cards utilize a light grey fill with a thin, slightly darker grey outer border to simulate rounded rectangle shapes.
- **Charts/Tables**: Replaces standard floating shapes with structural cell grids, making the layout highly resilient to screen resizing and ensuring visual elements snap perfectly to the grid.
- **Theme Hooks**: Sidebar background consumes `primary` or `dark_bg`. Card backgrounds consume `surface` or light greys. Typography strictly uses standard, clean sans-serif styles.

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

def render_workbook(wb, *, title: str = "Executive Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # Clear default sheets
    for sheet in wb.sheetnames:
        del wb[sheet]
        
    # Define app structure
    sheets = ["Dashboard", "Inputs", "Contacts"]
    for s in sheets:
        wb.create_sheet(s)
        
    # Styling Variables (acting as theme fallbacks)
    sidebar_color = "1F4E78"     # Dark Blue
    card_bg_color = "F9F9F9"     # Off-white / Light grey
    card_border_color = "D9D9D9" # Mid grey
    
    sidebar_fill = PatternFill(start_color=sidebar_color, fill_type="solid")
    nav_font = Font(color="FFFFFF", bold=True, size=11)
    nav_align = Alignment(horizontal="center", vertical="center")
    
    # 1. Apply Universal Sidebar to all sheets
    for s in sheets:
        ws = wb[s]
        ws.column_dimensions['A'].width = 12
        
        # Fill sidebar background down to row 40
        for r in range(1, 41):
            ws.cell(row=r, column=1).fill = sidebar_fill
            
        # Create Navigation Buttons
        nav_items = [("Dashboard", 5, "DASH"), ("Inputs", 8, "DATA"), ("Contacts", 11, "TEAM")]
        for target_sheet, r, label in nav_items:
            cell = ws.cell(row=r, column=1, value=label)
            cell.font = nav_font
            cell.alignment = nav_align
            # Internal Excel hyperlink syntax
            cell.hyperlink = f"#'{target_sheet}'!A1"
            
        # Freeze the sidebar so it stays visible during horizontal scroll
        ws.freeze_panes = "B1"

    # 2. Build Dashboard Card Layout on the primary sheet
    dash_ws = wb["Dashboard"]
    dash_ws.sheet_view.showGridLines = False
    
    # Adjust column widths for the dashboard grid
    for col in "BCDEFGHIJKLM":
        dash_ws.column_dimensions[col].width = 11

    # Add Dashboard Title
    dash_ws.row_dimensions[2].height = 30
    title_cell = dash_ws.cell(row=2, column=3, value=title)
    title_cell.font = Font(size=20, bold=True, color=sidebar_color)
    
    # Helper function to create resilient "Cards" using cells
    def create_card(ws, start_col: int, start_row: int, end_col: int, end_row: int, label: str):
        card_fill = PatternFill(start_color=card_bg_color, fill_type="solid")
        
        # Apply fill and strict outer borders to the range
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = card_fill
                
                top = Side(style='thin', color=card_border_color) if r == start_row else None
                bottom = Side(style='thin', color=card_border_color) if r == end_row else None
                left = Side(style='thin', color=card_border_color) if c == start_col else None
                right = Side(style='thin', color=card_border_color) if c == end_col else None
                
                cell.border = Border(top=top, bottom=bottom, left=left, right=right)

        # Merge the area to act as a single container
        ws.merge_cells(start_row=start_row, start_column=start_col, end_row=end_row, end_column=end_col)
        
        # Format the top-left cell as the card header
        top_left = ws.cell(row=start_row, column=start_col)
        top_left.value = f" {label}" # Padding space for aesthetics
        top_left.font = Font(bold=True, size=12, color="333333")
        top_left.alignment = Alignment(horizontal="left", vertical="top")

    # 3. Render Dashboard Cards
    # Top Row: 3 KPI Cards
    create_card(dash_ws, start_col=3,  start_row=4, end_col=5,  end_row=8, label="Total Sales")
    create_card(dash_ws, start_col=7,  start_row=4, end_col=9,  end_row=8, label="Net Profit")
    create_card(dash_ws, start_col=11, start_row=4, end_col=13, end_row=8, label="Active Customers")
    
    # Bottom Row: 2 Chart Containers
    create_card(dash_ws, start_col=3,  start_row=10, end_col=8,  end_row=24, label="Monthly Revenue Trend")
    create_card(dash_ws, start_col=10, start_row=10, end_col=13, end_row=24, label="Customer Satisfaction")
    
    # Set focus to the Dashboard
    wb.active = wb["Dashboard"]
```