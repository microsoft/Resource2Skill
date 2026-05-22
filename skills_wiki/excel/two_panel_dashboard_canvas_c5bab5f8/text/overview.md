### 1. High-level Skill Pattern Extraction

> **Skill Name**: Two-Panel Dashboard Canvas

* **Tier**: sheet_shell
* **Core Mechanism**: Transforms a standard worksheet into an application-like UI by hiding gridlines, establishing a narrow, dark-filled left sidebar column for high-level KPIs, and a wide, light-filled main canvas area designed to hold charts or matrix tables. 
* **Applicability**: Best used for executive summaries or interactive dashboards. It visually separates high-level metrics (sidebar) from detailed visualizations (main canvas), guiding the user's eye and providing a clean, modern aesthetic without relying on brittle Excel shapes.

### 2. Structural Breakdown

- **Data Layout**: Employs column `B` as the sidebar (width ~25), leaving column `A` and `C` as narrow margins (width ~2). Columns `D` onwards form the main canvas.
- **Formula Logic**: KPI values can be injected statically or set as formulas pointing to a hidden `Pivots` sheet (e.g., `='Pivots'!A4`), mirroring the tutorial's trick of turning off `GETPIVOTDATA` to use simple references.
- **Visual Design**: Gridlines disabled. Sidebar uses a deep primary theme color (e.g., dark green/blue) with white/light text. Main canvas uses a very light thematic background. KPI labels use a lighter accent color; KPI values are large and bold.
- **Charts/Tables**: Provides a structured staging ground; chart elements or matrix tables are meant to be overlaid on the canvas area.
- **Theme Hooks**: Consumes `primary` (sidebar background), `bg_light` (canvas background), `text_light` (KPI values), and `accent` (KPI labels).

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str, kpis: list = None, theme: str = "viva_green", **kwargs) -> None:
    """
    Renders a two-panel dashboard shell with a left KPI sidebar and a main content canvas.
    
    :param kpis: List of dicts, e.g., [{"label": "Total Orders", "value": 2400, "format": "#,##0"}]
    """
    # Standard theme palette fallback setup
    palettes = {
        "viva_green": {
            "primary": "1B3F2A",     # Dark green sidebar
            "bg_light": "EAF3E6",    # Light green canvas
            "text_light": "FFFFFF",  # White KPI values
            "accent": "A8D08D",      # Light green KPI labels
            "canvas_text": "333333"
        },
        "corporate_blue": {
            "primary": "1F497D",     
            "bg_light": "F2F5F9",    
            "text_light": "FFFFFF",  
            "accent": "8DB4E2",      
            "canvas_text": "1F497D"
        }
    }
    colors = palettes.get(theme, palettes["corporate_blue"])

    if kpis is None:
        kpis = [
            {"label": "Orders", "value": 2400, "format": "#,##0"},
            {"label": "Quantity", "value": 11997, "format": "#,##0"},
            {"label": "Revenue", "value": 649019.8, "format": "$#,##0.0k"},
            {"label": "Avg Rating", "value": 4.0, "format": "0.0"}
        ]

    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # 1. Column Sizing setup
    ws.column_dimensions['A'].width = 2
    ws.column_dimensions['B'].width = 28  # Sidebar
    ws.column_dimensions['C'].width = 2   # Gutter
    
    for col in range(4, 20):
        ws.column_dimensions[get_column_letter(col)].width = 12

    # 2. Paint the Panels
    sidebar_fill = PatternFill(start_color=colors["primary"], fill_type="solid")
    canvas_fill = PatternFill(start_color=colors["bg_light"], fill_type="solid")

    # Assuming a dashboard height of about 45 rows
    for row in range(1, 46):
        ws.cell(row=row, column=2).fill = sidebar_fill
        for col in range(4, 20):
            ws.cell(row=row, column=col).fill = canvas_fill

    # 3. Sidebar Header / Logo area
    title_cell = ws.cell(row=2, column=2, value=title.upper())
    title_cell.font = Font(color=colors["text_light"], size=24, bold=True)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # Optional subtitle
    subtitle_cell = ws.cell(row=3, column=2, value="DASHBOARD")
    subtitle_cell.font = Font(color=colors["accent"], size=12, bold=True)
    subtitle_cell.alignment = Alignment(horizontal="center", vertical="center")

    # 4. Inject KPI Cards down the sidebar
    start_row = 6
    for kpi in kpis:
        # Label
        lbl_cell = ws.cell(row=start_row, column=2, value=kpi["label"])
        lbl_cell.font = Font(color=colors["accent"], size=12, bold=True)
        lbl_cell.alignment = Alignment(horizontal="center", vertical="center")

        # Value
        val_cell = ws.cell(row=start_row + 1, column=2, value=kpi["value"])
        val_cell.font = Font(color=colors["text_light"], size=22, bold=True)
        val_cell.alignment = Alignment(horizontal="center", vertical="center")
        val_cell.number_format = kpi.get("format", "General")

        start_row += 4

    # 5. Canvas Header Layout
    canvas_title = ws.cell(row=2, column=4, value="Business Performance Overview")
    canvas_title.font = Font(size=18, bold=True, color=colors["canvas_text"])
    
    canvas_subtitle = ws.cell(row=3, column=4, value="Filter interactions map directly to charts placed in this region.")
    canvas_subtitle.font = Font(size=11, italic=True, color="666666")
```