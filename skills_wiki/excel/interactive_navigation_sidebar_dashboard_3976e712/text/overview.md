### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive Navigation Sidebar Dashboard

* **Tier**: archetype
* **Core Mechanism**: Creates a multi-sheet workbook with a persistent left-hand navigation sidebar. Uses the `=HYPERLINK()` formula with internal sheet references to allow users to click between tabs seamlessly. Freezes panes and hides gridlines to simulate a cohesive web-app experience.
* **Applicability**: Ideal for complex reports, financial models, or interactive dashboards that separate visuals, data inputs, and settings across multiple sheets, requiring an intuitive, app-like user navigation experience.

### 2. Structural Breakdown

- **Data Layout**: Column A acts as the global sidebar across all sheets. Row 2 acts as the global header. The main content canvas begins at `B3`.
- **Formula Logic**: `=HYPERLINK("#'<SheetName>'!A1", "Label")` creates internal links to cell `A1` on target sheets.
- **Visual Design**: The sidebar uses a dark primary fill, with white bold text. The currently active sheet link uses a slightly lighter secondary background to indicate state. Gridlines are hidden to clean up the canvas.
- **Charts/Tables**: N/A for the shell, but sets up the exact framing where KPI cards and charts are placed.
- **Theme Hooks**: Uses `primary` for the sidebar background, `secondary` for the active tab indicator, and `background` (white) for the text.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment

def render_workbook(wb, *, title: str = "Interactive Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Creates a multi-sheet dashboard archetype with a persistent, clickable 
    left-hand navigation sidebar to simulate a web application layout.
    """
    # Attempt to load theme, fallback to defaults
    try:
        from _helpers import get_theme
        palette = get_theme(theme)
        sidebar_bg = palette.get("primary", "1F4E78")
        active_bg = palette.get("secondary", "2F75B5")
        sidebar_fg = palette.get("background", "FFFFFF")
        text_color = palette.get("text", "000000")
    except ImportError:
        sidebar_bg = "1F4E78" # Dark blue
        active_bg = "2F75B5"  # Lighter active blue
        sidebar_fg = "FFFFFF" # White text
        text_color = "000000"

    # Define the sheets that make up the dashboard ecosystem
    tabs = ["Dashboard", "Inputs", "Settings"]
    
    # Store default sheets to remove them later (openpyxl requires at least 1 sheet to exist)
    default_sheets = wb.sheetnames
    
    # Create the new dashboard sheets
    sheets = {}
    for tab_name in tabs:
        sheets[tab_name] = wb.create_sheet(title=tab_name)
        
    # Remove original default sheets
    for sn in default_sheets:
        del wb[sn]
        
    # Build the layout and navigation on every sheet
    for current_sheet_name in tabs:
        ws = sheets[current_sheet_name]
        
        # Hide gridlines for a clean dashboard look
        ws.sheet_view.showGridLines = False
        
        # 1. Setup Sidebar Width
        ws.column_dimensions['A'].width = 18
        
        # 2. Paint Sidebar Background
        for row in range(1, 50):
            cell = ws.cell(row=row, column=1)
            cell.fill = PatternFill(start_color=sidebar_bg, end_color=sidebar_bg, fill_type="solid")
            
        # 3. Top Global Header
        ws.row_dimensions[2].height = 30
        ws.merge_cells('C2:K2')
        header_cell = ws['C2']
        header_cell.value = f"{title}"
        header_cell.font = Font(size=20, bold=True, color=sidebar_bg)
        header_cell.alignment = Alignment(vertical="center")
        
        # 4. Sheet-specific Subheader
        ws['C4'] = f"{current_sheet_name} View"
        ws['C4'].font = Font(size=14, bold=True, color=text_color)
        
        # 5. Inject Navigation Links into Sidebar
        start_row = 5
        for i, target_sheet_name in enumerate(tabs):
            link_row = start_row + (i * 3) # Space them out
            cell = ws.cell(row=link_row, column=1)
            
            # The # prefix dictates an internal workbook reference
            cell.value = f'=HYPERLINK("#\'{target_sheet_name}\'!A1", "  {target_sheet_name}")'
            
            # Highlight the active tab differently
            is_active = (current_sheet_name == target_sheet_name)
            bg_color = active_bg if is_active else sidebar_bg
            
            cell.fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
            cell.font = Font(color=sidebar_fg, bold=is_active, size=12)
            cell.alignment = Alignment(horizontal="left", vertical="center")
            
        # 6. Freeze Panes
        # Freezing at C3 means the sidebar (A, B) and top header (1, 2) stay locked
        # We include B as a small margin column
        ws.column_dimensions['B'].width = 3
        ws.freeze_panes = 'C3'
```