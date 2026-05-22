```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Two-Panel Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a modern, software-like dashboard layout by disabling gridlines, establishing a dark thematic left sidebar for KPIs, and leaving a spacious, subtly-tinted main area for charts. While the tutorial uses floating shapes for backgrounds, this pattern adapts the concept natively to Excel cell fills and column width adjustments, providing a far more robust grid for `openpyxl` generation without floating object alignment issues.
* **Applicability**: Best for executive summaries and overview dashboards where high-level metrics (KPIs) need to be anchored visibly and consistently alongside a main grid of deeper visual analysis.

### 2. Structural Breakdown

- **Data Layout**: 
  - Column A: Sidebar Left Margin (width: 3)
  - Column B: Sidebar Content (width: 28, holds Titles and KPIs)
  - Column C: Sidebar Right Margin (width: 3)
  - Column D: Main Content Margin (width: 4)
  - Columns E+: Main Charting Area
- **Formula Logic**: Static layout scaffolding. Designed to accept injected string values or external formula references via the `kpis` list.
- **Visual Design**: Gridlines disabled. The sidebar uses a deep primary theme color with bright white text to force high contrast. KPI values are scaled up to size 24 and bolded to create a strict visual hierarchy against the size 11 labels.
- **Charts/Tables**: Establishes the spatial grid where subsequent charts should be anchored (e.g., top-left chart at E5).
- **Theme Hooks**: 
  - `primary`: Drives the dark sidebar background.
  - `text_light`: Drives the high-contrast text and divider lines on the sidebar.
  - `background`: Drives the subtle canvas color for the main charting area.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def render_sheet(wb, sheet_name: str, *, title: str = "Executive Dashboard", theme: str = "forest_green", **kwargs) -> None:
    """
    Renders a two-panel dashboard shell with a dark KPI sidebar and a light main canvas.
    """
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)
        
    # Create a clean canvas
    ws.sheet_view.showGridLines = False

    # Standard inline theme fallback
    themes = {
        "corporate_blue": {
            "primary": "003366",
            "background": "F2F4F7",
            "text_light": "FFFFFF"
        },
        "forest_green": {
            "primary": "2E5339",
            "background": "F4F6F4",
            "text_light": "FFFFFF"
        }
    }
    palette = themes.get(theme, themes["corporate_blue"])

    sidebar_fill = PatternFill("solid", fgColor=palette["primary"])
    main_fill = PatternFill("solid", fgColor=palette["background"])
    
    # Fill main charting area (Columns D through X)
    for row in range(1, 51):
        for col in range(4, 25): 
            ws.cell(row=row, column=col).fill = main_fill

    # Fill dark sidebar area (Columns A through C)
    for row in range(1, 51):
        for col in range(1, 4):  
            ws.cell(row=row, column=col).fill = sidebar_fill

    # Set column widths to establish the split-pane layout
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 28
    ws.column_dimensions['C'].width = 3
    ws.column_dimensions['D'].width = 4
    
    # Render Sidebar Title
    title_cell = ws.cell(row=3, column=2, value=title.upper())
    title_cell.font = Font(color=palette["text_light"], size=18, bold=True)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # Divider line under title
    thin_light_border = Border(bottom=Side(style="thin", color=palette["text_light"]))
    ws.cell(row=4, column=2).border = thin_light_border

    # Sample KPIs (can be overridden via kwargs)
    kpis = kwargs.get("kpis", [
        {"label": "Total Orders", "value": "2,400", "emoji": "🛒"},
        {"label": "Total Quantity", "value": "11,997", "emoji": "📦"},
        {"label": "Total Revenue", "value": "$649.0k", "emoji": "💰"},
        {"label": "Avg. Rating", "value": "4.0", "emoji": "⭐"},
        {"label": "Days to Deliver", "value": "2.3", "emoji": "🚚"}
    ])

    current_row = 7
    for kpi in kpis:
        label = kpi.get("label", "")
        value = kpi.get("value", "")
        emoji = kpi.get("emoji", "")
        
        # KPI Label
        lbl_cell = ws.cell(row=current_row, column=2, value=f"{emoji}  {label}".strip())
        lbl_cell.font = Font(color=palette["text_light"], size=11, bold=True)
        lbl_cell.alignment = Alignment(horizontal="left", vertical="center")
        
        # KPI Value
        val_cell = ws.cell(row=current_row + 1, column=2, value=value)
        val_cell.font = Font(color=palette["text_light"], size=24, bold=True)
        val_cell.alignment = Alignment(horizontal="left", vertical="center")
        
        current_row += 4  # Spacing between KPI blocks
```
```