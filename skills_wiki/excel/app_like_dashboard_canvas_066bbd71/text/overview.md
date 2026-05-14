### 1. High-level Skill Pattern Extraction

> **Skill Name**: App-Like Dashboard Canvas

* **Tier**: sheet_shell
* **Core Mechanism**: Configures a worksheet to look like an interactive application dashboard. It hides native gridlines, creates a solid header banner, establishes a left-side panel for form controls/slicers, and defines a structured main content region for chart placement.
* **Applicability**: Best used as the primary viewing sheet for reporting workbooks, shifting the UX from a raw spreadsheet grid to a structured, presentation-ready report interface.

### 2. Structural Breakdown

- **Data Layout**: Uses structural spacing (Col A as left margin, Col E as gap). Divides the sheet into Header (Rows 1-4), Sidebar (Cols B-D), and Main Content Area (Cols F-W).
- **Formula Logic**: None (purely structural layout).
- **Visual Design**: Turns off gridlines (`showGridLines = False`). Uses a deep primary color for the top banner with bold white text. Uses a subtle light gray for the control panel to visually separate it from the white chart canvas.
- **Charts/Tables**: Provides standard cell anchor placeholders (`F6`, `O6`, etc.) mapping exactly to where `openpyxl` charts should be assigned (e.g., `chart.anchor = "F7"`).
- **Theme Hooks**: 
  - `primary_color`: Top banner background, sidebar text accent.
  - `text_on_primary`: Banner title text color.
  - `sidebar_bg`: Soft background for the left control panel.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment

def render_sheet(wb, sheet_name: str, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Initialize Sheet
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)
    
    # 2. Theme Definitions (Fallback palette mapping)
    primary_color = "1F4E78"  # Default: Corporate Blue
    if theme == "emerald":
        primary_color = "006B54"
    elif theme == "crimson":
        primary_color = "9E1B32"
        
    sidebar_bg = "F2F2F2"
    text_on_primary = "FFFFFF"
    
    # 3. Canvas Setup (Hide Gridlines)
    ws.sheet_view.showGridLines = False
    
    # 4. Top Banner (Rows 1 to 4)
    ws.merge_cells('A1:W4')
    title_cell = ws['A1']
    title_cell.value = f"   {title}"
    title_cell.font = Font(name="Segoe UI", size=24, bold=True, color=text_on_primary)
    title_cell.alignment = Alignment(horizontal="left", vertical="center")
    
    banner_fill = PatternFill(start_color=primary_color, end_color=primary_color, fill_type="solid")
    for row in ws.iter_rows(min_row=1, max_row=4, min_col=1, max_col=23):
        for cell in row:
            cell.fill = banner_fill
            
    # 5. Left Sidebar for Slicers/Controls (Cols B to D)
    sidebar_fill = PatternFill(start_color=sidebar_bg, end_color=sidebar_bg, fill_type="solid")
    for row in ws.iter_rows(min_row=6, max_row=35, min_col=2, max_col=4):
        for cell in row:
            cell.fill = sidebar_fill
            
    ws.merge_cells('B6:D6')
    sidebar_title = ws['B6']
    sidebar_title.value = "FILTERS & CONTROLS"
    sidebar_title.font = Font(name="Segoe UI", size=10, bold=True, color=primary_color)
    sidebar_title.alignment = Alignment(horizontal="center", vertical="center")
    
    # 6. Structural Column Widths
    ws.column_dimensions['A'].width = 3   # Left outer margin
    ws.column_dimensions['B'].width = 12  # Sidebar partition 1
    ws.column_dimensions['C'].width = 12  # Sidebar partition 2
    ws.column_dimensions['D'].width = 12  # Sidebar partition 3
    ws.column_dimensions['E'].width = 4   # Spacer gap between sidebar and charts
    
    # Set uniform width for main canvas columns to help charts scale predictably
    for col_letter in "FGHIJKLMNOPQRSTUVW":
        ws.column_dimensions[col_letter].width = 10

    # 7. Visual Chart Anchors / Placeholders
    anchors = {
        'F6': "Main Chart Area (e.g. Stacked Bar)",
        'O6': "Secondary Chart (e.g. Line Chart)",
        'F21': "Detail Chart 1",
        'O21': "Detail Chart 2"
    }
    
    for cell_ref, placeholder_text in anchors.items():
        cell = ws[cell_ref]
        cell.value = f"[ {placeholder_text} ]"
        cell.font = Font(name="Segoe UI", italic=True, color="A6A6A6")
```