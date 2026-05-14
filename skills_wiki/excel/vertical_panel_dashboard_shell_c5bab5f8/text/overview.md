### 1. High-level Skill Pattern Extraction

> **Skill Name**: Vertical Panel Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Configures a worksheet with a two-tone layout: a narrow, dark-themed vertical side panel for navigation and KPIs, and a wide, light-themed main canvas for charts and data. Hides gridlines and applies structural column sizing to simulate a polished, app-like interface using native cell fills instead of floating shapes.
* **Applicability**: Best for high-level executive summaries and KPI dashboards where top-level metrics need constant visibility alongside interactive or detailed charts.

### 2. Structural Breakdown

- **Data Layout**: Columns A through C form the left panel (A and C act as padding, B holds content). Columns D onward form the main chart canvas.
- **Formula Logic**: Static structural layout. In a complete implementation, KPI values would typically be linked to calculation sheets via references (e.g., `=Pivots!A1`).
- **Visual Design**: Uses contrasting `sidebar_bg` and `canvas_bg` fills. Gridlines are explicitly disabled. Fonts in the sidebar are set to `sidebar_fg` (usually white) with strict visual hierarchy (large/bold for values, smaller/lighter for labels).
- **Charts/Tables**: Provides the structural canvas. The main area is intentionally left blank for subsequent chart components to anchor into (e.g., anchoring a trend line at E5, a heat map at J5).
- **Theme Hooks**: Consumes `sidebar_bg`, `sidebar_fg`, and `canvas_bg` tokens to color-match the corporate brand.

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "Dashboard", kpis: list[dict] = None, theme: str = "viva_green", **kwargs) -> None:
    """
    Renders a two-tone dashboard shell with a KPI side panel.
    """
    if sheet_name not in wb.sheetnames:
        ws = wb.create_sheet(sheet_name)
    else:
        ws = wb[sheet_name]

    # Minimal inline palette fallback based on the tutorial's fashion brand (Viva Calif)
    palettes = {
        "corporate_blue": {"sidebar_bg": "1E3A8A", "sidebar_fg": "FFFFFF", "canvas_bg": "F3F4F6"},
        "viva_green": {"sidebar_bg": "14532D", "sidebar_fg": "FFFFFF", "canvas_bg": "DCFCE7"},
        "dark_slate": {"sidebar_bg": "1F2937", "sidebar_fg": "F9FAFB", "canvas_bg": "FFFFFF"}
    }
    palette = palettes.get(theme, palettes["corporate_blue"])

    # 1. UI Setup: Hide gridlines for an app-like feel
    ws.sheet_view.showGridLines = False

    # 2. Layout Sizing
    ws.column_dimensions['A'].width = 3   # Left padding
    ws.column_dimensions['B'].width = 25  # KPI Content
    ws.column_dimensions['C'].width = 3   # Right padding / separator
    
    # Canvas area sizing (leaving room for charts)
    for i in range(4, 25): # D to X
        ws.column_dimensions[get_column_letter(i)].width = 12

    # 3. Apply Background Colors (simulating the tutorial's large shape rectangles)
    sidebar_fill = PatternFill(start_color=palette["sidebar_bg"], end_color=palette["sidebar_bg"], fill_type="solid")
    canvas_fill = PatternFill(start_color=palette["canvas_bg"], end_color=palette["canvas_bg"], fill_type="solid")
    
    for row in range(1, 45):
        for col in range(1, 25):
            cell = ws.cell(row=row, column=col)
            if col <= 3:
                cell.fill = sidebar_fill
            else:
                cell.fill = canvas_fill

    # 4. Add Title to Sidebar
    title_cell = ws['B2']
    title_cell.value = title.upper()
    title_cell.font = Font(name="Segoe UI", size=22, bold=True, color=palette["sidebar_fg"])
    title_cell.alignment = Alignment(horizontal="left", vertical="center")

    # 5. Populate KPIs in Sidebar
    if not kpis:
        # Default data inspired by the tutorial's transaction data
        kpis = [
            {"label": "Total Orders", "value": 2400, "format": "#,##0"},
            {"label": "Revenue", "value": 649019, "format": "$#,##0"},
            {"label": "Avg Rating", "value": 4.0, "format": "0.0"},
            {"label": "Days to Deliver", "value": 2.3, "format": "0.0"}
        ]

    start_row = 6
    for kpi in kpis:
        # KPI Label
        lbl_cell = ws.cell(row=start_row, column=2)
        lbl_cell.value = kpi.get("label", "Metric")
        lbl_cell.font = Font(name="Segoe UI", size=11, bold=True, color=palette["sidebar_fg"])
        lbl_cell.alignment = Alignment(horizontal="left", vertical="bottom")
        
        # KPI Value
        val_cell = ws.cell(row=start_row + 1, column=2)
        val_cell.value = kpi.get("value", 0)
        val_cell.font = Font(name="Segoe UI", size=24, bold=True, color=palette["sidebar_fg"])
        val_cell.alignment = Alignment(horizontal="left", vertical="top")
        
        if "format" in kpi:
            val_cell.number_format = kpi["format"]
            
        start_row += 4  # Spacing block between KPIs
```