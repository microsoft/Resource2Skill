# Agile Kanban Task Tracker

## Applicability

Best for project management dashboards, sprint trackers, or any scenario where items are manually moved through a pipeline of stages and continuous aggregation (hours, points, costs) per stage is required.

## Analysis

```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Agile Kanban Task Tracker

* **Tier**: sheet_shell
* **Core Mechanism**: Creates a single-sheet task board with distinct categorical sections (e.g., "Backlog", "In Progress"). It uses a dynamic `=SUBTOTAL(9, OFFSET(current, 1, 0):OFFSET(next, -1, 0))` formula for section headers. This allows users to physically drag and drop rows between sections (using Shift+Drag) while keeping all category totals perfectly accurate without formula adjustments. It also features drop-downs, conditional formatting tags, and an in-cell `REPT` progress bar.
* **Applicability**: Best for project management dashboards, sprint trackers, or any scenario where items are manually moved through a pipeline of stages and continuous aggregation (hours, points, costs) per stage is required.

### 2. Structural Breakdown

- **Data Layout**: 
  - Top header row with overall project stats.
  - Column headers: Type, Role, Task Description, Priority, Est. Days, Actual Days.
  - Section Headers acting as category dividers and subtotal containers.
  - Task rows nested between Section Headers.
- **Formula Logic**: 
  - Dynamic Block Sum: `=SUBTOTAL(9, OFFSET(F6, 1, 0):OFFSET(F10, -1, 0))` (Sums exactly the rows between the current section header and the next one).
  - In-cell Progress Bar: `=REPT("■", INT(H2*10)) & REPT("□", 10 - INT(H2*10))` based on completion percentage.
- **Visual Design**: 
  - Distinct background colors for section headers to separate blocks.
  - Conditional formatting on the "Type" and "Priority" columns to create pill-like colored tags.
- **Charts/Tables**: Standard ranges (not Excel Tables) to allow for easier row drag-and-drop mechanics between arbitrary header blocks.
- **Theme Hooks**: Uses `primary` for main headers, `secondary` for section dividers, and specific semantic colors (red/yellow/green) for conditional formatting tags.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.worksheet.datavalidation import DataValidation

def render_sheet(wb, sheet_name: str, *, title: str = "Agile Kanban", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # Minimal fallback theme palette
    theme_colors = {
        "primary": "2B5B84",
        "primary_text": "FFFFFF",
        "secondary": "D9E1E8",
        "secondary_text": "1A365D",
        "accent": "E26D5C",
        "bg_light": "F8FAFC"
    }

    # Helper styles
    header_font = Font(bold=True, color=theme_colors["primary_text"])
    header_fill = PatternFill("solid", fgColor=theme_colors["primary"])
    section_font = Font(bold=True, size=14, color=theme_colors["secondary_text"])
    section_fill = PatternFill("solid", fgColor=theme_colors["secondary"])
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")
    thin_border = Border(
        left=Side(style='thin', color='CCCCCC'),
        right=Side(style='thin', color='CCCCCC'),
        top=Side(style='thin', color='CCCCCC'),
        bottom=Side(style='thin', color='CCCCCC')
    )

    # 1. Setup Overall Dashboard Header (Rows 1-4)
    ws.merge_cells("A1:C3")
    title_cell = ws["A1"]
    title_cell.value = title
    title_cell.font = Font(bold=True, size=24, color=theme_colors["primary"])
    title_cell.alignment = center_align

    ws["D2"] = "Start Date:"
    ws["E2"] = "2023-10-01"
    ws["F2"] = "Total Est:"
    ws["F3"] = "Total Act:"
    ws["F2"].font = Font(bold=True)
    ws["F3"].font = Font(bold=True)
    
    # Overall totals summing the section subtotals
    ws["G2"] = "=F6+F11+F15" 
    ws["G3"] = "=G6+G11+G15"
    
    ws["H2"] = "Progress:"
    ws["H2"].font = Font(bold=True)
    # Calculate progress % (Actual / Est)
    ws["I2"] = "=IF(G2>0, G3/G2, 0)"
    ws["I2"].number_format = "0.0%"
    # In-cell Progress Bar
    ws["I3"] = '=REPT("■", INT(I2*10)) & REPT("□", 10 - INT(I2*10))'
    ws["I3"].font = Font(color=theme_colors["primary"])

    # 2. Setup Column Headers (Row 5)
    headers = ["Type", "Role", "Task Description", "Priority", "Status", "Est. Days", "Actual Days"]
    for col_idx, text in enumerate(headers, start=1):
        cell = ws.cell(row=5, column=col_idx, value=text)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align
        cell.border = thin_border

    # Set column widths
    ws.column_dimensions['A'].width = 12
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 40
    ws.column_dimensions['D'].width = 12
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 12
    ws.column_dimensions['G'].width = 12
    ws.column_dimensions['I'].width = 15

    # 3. Data Validation for Dropdowns
    dv_type = DataValidation(type="list", formula1='"Feature,Bug,Research,Docs"', allow_blank=True)
    dv_priority = DataValidation(type="list", formula1='"High,Medium,Low"', allow_blank=True)
    ws.add_data_validation(dv_type)
    ws.add_data_validation(dv_priority)

    # 4. Define Sections and Data
    sections = [
        {"row": 6, "title": "Sprint Backlog", "next_row": 11, "data": [
            ["Feature", "Frontend", "Build user profile page", "High", "Not Started", 5, 0],
            ["Research", "Design", "Competitor analysis", "Medium", "Not Started", 3, 0],
            ["Feature", "Backend", "API for user auth", "High", "Not Started", 4, 0],
            ["Docs", "Product", "Write release notes", "Low", "Not Started", 2, 0]
        ]},
        {"row": 11, "title": "In Progress", "next_row": 15, "data": [
            ["Bug", "Frontend", "Fix navbar alignment", "High", "Working", 2, 1],
            ["Feature", "Backend", "Database schema migration", "High", "Working", 3, 2],
            ["Research", "Data", "Analyze Q3 usage metrics", "Medium", "Working", 4, 2]
        ]},
        {"row": 15, "title": "Done", "next_row": 19, "data": [
            ["Feature", "Frontend", "Initial landing page", "Medium", "Completed", 4, 4],
            ["Bug", "Backend", "Fix timeout issue", "High", "Completed", 1, 1],
            ["Docs", "Product", "API Documentation v1", "Medium", "Completed", 3, 3]
        ]},
        {"row": 19, "title": "END OF BOARD", "next_row": 20, "data": []} # Hidden boundary row
    ]

    for sec in sections:
        r = sec["row"]
        # Write Section Header
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
        cell = ws.cell(row=r, column=1, value=sec["title"])
        cell.font = section_font
        cell.fill = section_fill
        cell.alignment = left_align
        
        # Color the whole header row
        for c in range(1, 8):
            ws.cell(row=r, column=c).fill = section_fill
            ws.cell(row=r, column=c).border = thin_border

        # Add the dynamic OFFSET subtotal formula for Est and Actual Days
        # This allows rows to be dragged between sections and automatically re-summed
        if sec["title"] != "END OF BOARD":
            ws.cell(row=r, column=6, value=f"=SUBTOTAL(9, OFFSET(F{r}, 1, 0):OFFSET(F{sec['next_row']}, -1, 0))").font = Font(bold=True)
            ws.cell(row=r, column=7, value=f"=SUBTOTAL(9, OFFSET(G{r}, 1, 0):OFFSET(G{sec['next_row']}, -1, 0))").font = Font(bold=True)

        # Write Task Rows
        for i, task_data in enumerate(sec["data"]):
            current_row = r + 1 + i
            for j, val in enumerate(task_data):
                cell = ws.cell(row=current_row, column=j+1, value=val)
                cell.alignment = center_align if j in [0, 1, 3, 4, 5, 6] else left_align
                cell.border = thin_border
            
            # Apply data validation to cells
            dv_type.add(ws.cell(row=current_row, column=1))
            dv_priority.add(ws.cell(row=current_row, column=4))

    # Hide the boundary row
    ws.row_dimensions[19].hidden = True

    # 5. Conditional Formatting for Tags (Type and Priority)
    # Type Formatting
    type_colors = {
        "Feature": "D0E8F2", # Light Blue
        "Bug": "F2D0D0",     # Light Red
        "Research": "E8D0F2",# Light Purple
        "Docs": "D0F2D0"     # Light Green
    }
    for val, color in type_colors.items():
        rule = CellIsRule(operator="equal", formula=[f'"{val}"'], stopIfTrue=True, fill=PatternFill("solid", fgColor=color))
        ws.conditional_formatting.add("A6:A18", rule)

    # Priority Formatting
    priority_colors = {
        "High": "FFC7CE",    # Red
        "Medium": "FFEB9C",  # Yellow
        "Low": "C6EFCE"      # Green
    }
    for val, color in priority_colors.items():
        # Text colors to match standard Excel presets
        text_color = {"High": "9C0006", "Medium": "9C6500", "Low": "006100"}[val]
        rule = CellIsRule(operator="equal", formula=[f'"{val}"'], stopIfTrue=True, 
                          fill=PatternFill("solid", fgColor=color), font=Font(color=text_color))
        ws.conditional_formatting.add("D6:D18", rule)
```
```