# Dynamic In-Cell Gantt Chart

## Applicability

Essential for project management templates, resource allocation trackers, and marketing schedules. Best applied when you want a robust timeline visualization without relying on complex Excel charts or external add-ins.

## Analysis

### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic In-Cell Gantt Chart

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a dynamic, horizontally scrolling project timeline using a formula-driven calendar header and layered `Rule(type="expression")` conditional formatting to render Gantt bars. It handles durations, task statuses (Blocked, In Progress, Complete), and visually overlays the percentage complete directly onto the bars.
* **Applicability**: Essential for project management templates, resource allocation trackers, and marketing schedules. Best applied when you want a robust timeline visualization without relying on complex Excel charts or external add-ins.

### 2. Structural Breakdown

- **Data Layout**: 
  - **Left Pane (A:H)**: Project metadata including ID, Activity Name, Assignee, Start Date, End Date, Duration (Days), Status dropdown, and % Complete.
  - **Right Pane (I:AL)**: The timeline. Row 3 holds the Month format (`mmm`), Row 4 holds the weekly start dates (`d-mmm`).
- **Formula Logic**: 
  - Duration is calculated via `=IF(ISBLANK(E6), "", NETWORKDAYS(D6,E6))`.
  - Timeline increments by 7 days: `I4` refs the global start date, `J4` is `=I4+7`, and so on.
- **Visual Design**: Uses specific conditional formatting rule hierarchies. Blocked tasks turn the data row red. Gantt bars are shaded conditionally based on date overlaps and status values. Gridlines are removed and panes are frozen at `I6` for seamless scrolling.
- **Charts/Tables**: Replaces native bar charts with a grid of cells acting as pixels/blocks, driven entirely by Conditional Formatting expression rules.
- **Theme Hooks**: Consumes standard structural colors (`primary_bg`, `text_main`) and semantic token colors (`success_bg` for Complete, `warning_bg` for Blocked, `accent_dark` for % complete progress).

### 3. Reproduction Code

```python
from datetime import date, timedelta
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import Rule
from openpyxl.styles.differential import DifferentialStyle

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a fully dynamic, formula-driven Gantt Chart worksheet.
    Includes data validation, network days formulas, and complex conditional formatting.
    """
    # Mock theme fallback
    colors = {
        "primary_bg": "203764", "primary_fg": "FFFFFF",
        "header_bg": "D9E1F2", "header_fg": "000000",
        "base_bar": "DCE6F1", "prog_bar": "4F81BD", 
        "complete_bar": "FFD700", "blocked_bar": "FF9999", "blocked_row": "FFCCCC",
        "border": "D9D9D9"
    }

    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)

    ws.sheet_view.showGridLines = False
    
    # Setup Title and Global Start Date
    ws["B2"] = title
    ws["B2"].font = Font(size=18, bold=True, color=colors["primary_bg"])
    ws["D2"] = "Project Start:"
    ws["D2"].font = Font(bold=True)
    ws["E2"] = date(2023, 1, 2)
    ws["E2"].number_format = "dd-mmm-yyyy"

    # Define Columns
    headers = ["#", "Activity", "Assigned To", "Start", "End", "Days", "Status", "% Done"]
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=5, column=col_idx, value=header)
        cell.font = Font(bold=True, color=colors["primary_fg"])
        cell.fill = PatternFill(start_color=colors["primary_bg"], end_color=colors["primary_bg"], fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # Set Column Widths
    widths = {"A": 4, "B": 25, "C": 15, "D": 12, "E": 12, "F": 8, "G": 12, "H": 10}
    for col, width in widths.items():
        ws.column_dimensions[col].width = width

    # Setup Timeline Headers (Weekly)
    for i in range(30):
        col_letter = ws.cell(row=4, column=9+i).column_letter
        ws.column_dimensions[col_letter].width = 4.5
        
        # Month Header (Row 3)
        month_cell = ws.cell(row=3, column=9+i)
        if i == 0:
            month_cell.value = "=$E$2"
        else:
            prev_col = ws.cell(row=4, column=8+i).column_letter
            month_cell.value = f"={col_letter}4"
        month_cell.number_format = "mmm"
        month_cell.font = Font(bold=True, color="595959")
        month_cell.alignment = Alignment(horizontal="left")

        # Week Date Header (Row 4)
        week_cell = ws.cell(row=4, column=9+i)
        if i == 0:
            week_cell.value = "=$E$2"
        else:
            prev_col = ws.cell(row=4, column=8+i).column_letter
            week_cell.value = f"={prev_col}4+7"
        week_cell.number_format = "d-mmm"
        week_cell.alignment = Alignment(textRotation=90, horizontal="center", vertical="center")
        week_cell.font = Font(size=9)
        
        # Style Timeline Headers
        ws.cell(row=5, column=9+i).fill = PatternFill(start_color=colors["header_bg"], end_color=colors["header_bg"], fill_type="solid")
        ws.cell(row=5, column=9+i).border = Border(bottom=Side(style="medium", color=colors["primary_bg"]))

    # Insert Sample Data & Formulas
    tasks = [
        (1, "Project Kick-off", "Alice", date(2023, 1, 2), date(2023, 1, 6), "Complete", 1.0),
        (2, "Requirements Gathering", "Bob", date(2023, 1, 9), date(2023, 1, 27), "Complete", 1.0),
        (3, "Design Phase", "Charlie", date(2023, 1, 23), date(2023, 2, 17), "In progress", 0.6),
        (4, "Core Development", "Dave", date(2023, 2, 13), date(2023, 4, 14), "In progress", 0.25),
        (5, "API Integration", "Eve", date(2023, 3, 6), date(2023, 3, 24), "Blocked", 0.1),
        (6, "QA Testing", "Alice", date(2023, 4, 10), date(2023, 5, 5), "Not started", 0.0),
        (7, "Deployment & Go-Live", "Bob", date(2023, 5, 1), date(2023, 5, 12), "Not started", 0.0),
    ]

    thin_border = Border(left=Side(style="thin", color=colors["border"]), 
                         right=Side(style="thin", color=colors["border"]),
                         top=Side(style="thin", color=colors["border"]), 
                         bottom=Side(style="thin", color=colors["border"]))

    for row_idx, task in enumerate(tasks, 6):
        ws.cell(row=row_idx, column=1, value=task[0]).alignment = Alignment(horizontal="center")
        ws.cell(row=row_idx, column=2, value=task[1])
        ws.cell(row=row_idx, column=3, value=task[2])
        
        ws.cell(row=row_idx, column=4, value=task[3]).number_format = "dd-mmm-yy"
        ws.cell(row=row_idx, column=5, value=task[4]).number_format = "dd-mmm-yy"
        
        # Duration Formula
        ws.cell(row=row_idx, column=6, value=f'=IF(ISBLANK(E{row_idx}), "", NETWORKDAYS(D{row_idx},E{row_idx}))').alignment = Alignment(horizontal="center")
        
        ws.cell(row=row_idx, column=7, value=task[5])
        ws.cell(row=row_idx, column=8, value=task[6]).number_format = "0%"

        # Apply basic borders to timeline grid for readability
        for c in range(1, 39):
            ws.cell(row=row_idx, column=c).border = thin_border

    # Status Data Validation
    dv = DataValidation(type="list", formula1='"Not started,In progress,Blocked,Complete"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"G6:G{5+len(tasks)}")

    # Conditional Formatting Rules
    last_row = 5 + len(tasks)
    timeline_range = f"I6:AL{last_row}"
    data_range = f"A6:H{last_row}"

    # 1. Blocked Row Highlight
    dxf_blocked_row = DifferentialStyle(fill=PatternFill(bgColor=colors["blocked_row"], fill_type="solid"), 
                                        font=Font(color="9C0006"))
    rule_blocked_row = Rule(type="expression", formula=['$G6="Blocked"'], dxf=dxf_blocked_row)
    ws.conditional_formatting.add(data_range, rule_blocked_row)

    # 2. Blocked Gantt Bar
    dxf_blocked_bar = DifferentialStyle(fill=PatternFill(bgColor=colors["blocked_bar"], fill_type="solid"))
    rule_blocked_bar = Rule(type="expression", formula=['AND(I$4<=$E6, I$4+6>=$D6, $G6="Blocked")'], dxf=dxf_blocked_bar)

    # 3. Complete Gantt Bar
    dxf_complete_bar = DifferentialStyle(fill=PatternFill(bgColor=colors["complete_bar"], fill_type="solid"))
    rule_complete_bar = Rule(type="expression", formula=['AND(I$4<=$E6, I$4+6>=$D6, $G6="Complete")'], dxf=dxf_complete_bar)

    # 4. In Progress (% Done) Gantt Bar
    dxf_prog_bar = DifferentialStyle(fill=PatternFill(bgColor=colors["prog_bar"], fill_type="solid"))
    rule_prog_bar = Rule(type="expression", formula=['AND(I$4<=$E6, I$4+6>=$D6, I$4<=$D6+($E6-$D6)*$H6)'], dxf=dxf_prog_bar)

    # 5. Base Gantt Bar (Remaining duration)
    dxf_base_bar = DifferentialStyle(fill=PatternFill(bgColor=colors["base_bar"], fill_type="solid"))
    rule_base_bar = Rule(type="expression", formula=['AND(I$4<=$E6, I$4+6>=$D6)'], dxf=dxf_base_bar)

    # Add rules in specific priority order
    ws.conditional_formatting.add(timeline_range, rule_blocked_bar)
    ws.conditional_formatting.add(timeline_range, rule_complete_bar)
    ws.conditional_formatting.add(timeline_range, rule_prog_bar)
    ws.conditional_formatting.add(timeline_range, rule_base_bar)

    # Freeze panes so task details stay visible while scrolling time
    ws.freeze_panes = "I6"
```