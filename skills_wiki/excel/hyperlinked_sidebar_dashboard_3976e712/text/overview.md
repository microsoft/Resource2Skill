### 1. High-level Skill Pattern Extraction

> **Skill Name**: Hyperlinked Sidebar Dashboard

* **Tier**: archetype
* **Core Mechanism**: Transforms a standard workbook into an interactive app-like experience by using Column A as a global navigation sidebar. Applies internal cell hyperlinks (`#'SheetName'!A1`) to switch between views, highlights the active tab's button, and creates distinct white "panels" over a light gray canvas for chart placement.
* **Applicability**: Best for complex reporting workbooks (Dashboards, Data Inputs, Settings) where users need an intuitive, macro-free "homepage" structure to navigate between different domains of the report.

### 2. Structural Breakdown

- **Data Layout**: Column A (width 18) serves as the persistent sidebar. Main content spans columns B through S. Sub-regions are mapped as "panels" (e.g., C3:I10).
- **Formula Logic**: Uses internal references via the cell hyperlink attribute: `cell.hyperlink = "#'Target Sheet'!A1"`.
- **Visual Design**: Gridlines are hidden globally. The sidebar uses a dark primary theme color. Active navigation buttons receive a lighter secondary highlight across 3 rows. The main canvas uses a subtle gray (`#F3F4F6`), while data panels use pure white with thin borders to create depth.
- **Charts/Tables**: Serves as the outer layout shell; individual charts/tables are rendered inside the defined panel coordinate blocks.
- **Theme Hooks**: Consumes `primary` (sidebar), `secondary` (active button), `background` (canvas), `panel` (cards), `text_light` (nav text), and `text_dark` (panel headers).

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

def render_workbook(wb, *, title: str = "Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Builds a multi-sheet interactive dashboard using Column A as a navigation sidebar.
    """
    # Mock palette loading (in framework, use _helpers.get_palette(theme))
    palette = {
        "primary": "1E3A8A",      # Dark blue sidebar
        "secondary": "3B82F6",    # Active link highlight
        "background": "F3F4F6",   # App canvas background
        "panel": "FFFFFF",        # White cards
        "text_light": "FFFFFF",   # Sidebar text
        "text_dark": "111827",    # Headers
        "border": "E5E7EB"        # Subtle panel borders
    }
    
    sheets = ["Dashboard", "Inputs", "Contacts"]
    
    # Clean up default sheet
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])
        
    # Set up reusable styles
    fill_sidebar = PatternFill("solid", fgColor=palette["primary"])
    fill_active = PatternFill("solid", fgColor=palette["secondary"])
    fill_bg = PatternFill("solid", fgColor=palette["background"])
    fill_panel = PatternFill("solid", fgColor=palette["panel"])
    
    font_link = Font(color=palette["text_light"], bold=True, size=12)
    font_panel_title = Font(color=palette["text_dark"], bold=True, size=14)
    align_center = Alignment(horizontal="center", vertical="center")
    bd_thin = Side(style='thin', color=palette["border"])

    for sheet_name in sheets:
        ws = wb.create_sheet(sheet_name)
        ws.sheet_view.showGridLines = False
        
        # 1. Paint Global Background
        for row in range(1, 40):
            for col in range(2, 20):
                ws.cell(row=row, column=col).fill = fill_bg
                
        # 2. Paint Left Sidebar
        ws.column_dimensions['A'].width = 18
        for row in range(1, 40):
            ws.cell(row=row, column=1).fill = fill_sidebar
            
        # 3. Add Navigation Links
        nav_start_row = 5
        for i, target_sheet in enumerate(sheets):
            link_row = nav_start_row + (i * 4)
            cell = ws.cell(row=link_row, column=1)
            cell.value = target_sheet
            cell.font = font_link
            cell.alignment = align_center
            
            # Internal hyperlink magic
            cell.hyperlink = f"#'{target_sheet}'!A1"
            
            # Highlight the active sheet's button (3 rows tall)
            if target_sheet == sheet_name:
                for r_offset in range(-1, 2):
                    ws.cell(row=link_row + r_offset, column=1).fill = fill_active
                
        # 4. Draw Dashboard Panels (if on the main sheet)
        if sheet_name == "Dashboard":
            panels = [
                {"min_col": 3, "min_row": 3, "max_col": 9, "max_row": 10, "title": "Key Metrics"},
                {"min_col": 11, "min_row": 3, "max_col": 18, "max_row": 10, "title": "Map View"},
                {"min_col": 3, "min_row": 12, "max_col": 18, "max_row": 25, "title": "Sales Trend"}
            ]
            
            for p in panels:
                # Fill panel area and apply outer borders
                for r in range(p["min_row"], p["max_row"] + 1):
                    for c in range(p["min_col"], p["max_col"] + 1):
                        cell = ws.cell(row=r, column=c)
                        cell.fill = fill_panel
                        
                        border_kwargs = {}
                        if r == p["min_row"]: border_kwargs['top'] = bd_thin
                        if r == p["max_row"]: border_kwargs['bottom'] = bd_thin
                        if c == p["min_col"]: border_kwargs['left'] = bd_thin
                        if c == p["max_col"]: border_kwargs['right'] = bd_thin
                        
                        if border_kwargs:
                            cell.border = Border(**border_kwargs)
                            
                # Inject Panel Title
                title_cell = ws.cell(row=p["min_row"] + 1, column=p["min_col"] + 1)
                title_cell.value = p["title"]
                title_cell.font = font_panel_title
```