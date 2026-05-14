```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Two-Tone Sidebar Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a navigation/KPI sidebar by widening a left-side column and applying a dark theme fill, contrasted against a light-filled main canvas area. Disables native gridlines to enforce a clean, application-like aesthetic. (Adapts the video's manual shape-based background approach into an Openpyxl-native cell-fill grid approach for robust layout automation).
* **Applicability**: Best for landing pages of reports or high-level dashboards where global metrics (KPIs) and slicers need a dedicated visual zone separated from the primary data visualizations.

### 2. Structural Breakdown

- **Data Layout**: 
  - Column A: Narrow outer left margin (width 2.0).
  - Column B: Wide Sidebar for KPIs/Slicers (width 28.0).
  - Column C: Narrow inner gutter (width 2.0).
  - Columns D-R: Main canvas area for charts/tables (width 14.0).
- **Formula Logic**: N/A for the shell itself, but acts as the destination for linked values calculated on backend pivot sheets.
- **Visual Design**: Hides native gridlines (`showGridLines = False`). Uses a high-contrast theme where the sidebar takes a dark, heavy fill and the main canvas takes a soft, pastel fill.
- **Charts/Tables**: Leaves the main canvas area structurally open for downstream chart components.
- **Theme Hooks**: Consumes `sidebar_bg` (dark), `sidebar_fg` (light/white), and `canvas_bg` (light/soft).

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a dashboard shell with a dark left sidebar for KPIs/Slicers
    and a light main canvas for charts and tables.
    """
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # 1. Theme configuration
    # Note: In a full pipeline, these hex codes are injected via the 'theme' loader.
    # We establish a dark olive/light pastel motif mirroring the video's design.
    theme_colors = {
        "sidebar_bg": "2B4C3B",  # Dark Olive Green
        "sidebar_fg": "FFFFFF",  # White
        "canvas_bg": "F0F4EC",   # Light Pastel Green
        "canvas_fg": "000000",   # Black
    }

    # 2. Apply Layout Fills
    sidebar_fill = PatternFill(start_color=theme_colors["sidebar_bg"], fill_type="solid")
    canvas_fill = PatternFill(start_color=theme_colors["canvas_bg"], fill_type="solid")

    # Bounding the canvas height for a standard 1080p screen view
    max_row = 45

    # Fill Sidebar (Column B)
    for row in range(1, max_row + 1):
        ws.cell(row=row, column=2).fill = sidebar_fill

    # Fill Main Canvas (Columns D to R)
    for col_idx in range(4, 19):
        for row in range(1, max_row + 1):
            ws.cell(row=row, column=col_idx).fill = canvas_fill

    # 3. Configure Column Widths for structural layout
    ws.column_dimensions['A'].width = 2.0    # Left outer margin
    ws.column_dimensions['B'].width = 28.0   # Sidebar width
    ws.column_dimensions['C'].width = 2.0    # Gutter between sidebar and canvas
    for col_idx in range(4, 19):
        ws.column_dimensions[get_column_letter(col_idx)].width = 14.0

    # 4. Add Dashboard Title in Canvas
    title_cell = ws['D2']
    title_cell.value = title.upper()
    title_cell.font = Font(name="Segoe UI", size=24, bold=True, color=theme_colors["sidebar_bg"])
    title_cell.alignment = Alignment(vertical="center")
    ws.row_dimensions[2].height = 40

    # 5. Populate Sidebar with representative KPI cards
    kpis = [
        ("TOTAL ORDERS", "2,400"),
        ("TOTAL QUANTITY", "11,997"),
        ("TOTAL REVENUE", "$649.0K"),
        ("AVG. RATING", "4.0"),
        ("DAYS TO DELIVER", "2.3")
    ]

    start_row = 5
    for label, value in kpis:
        # KPI Label
        lbl_cell = ws.cell(row=start_row, column=2)
        lbl_cell.value = label
        lbl_cell.font = Font(name="Segoe UI", size=10, bold=True, color=theme_colors["canvas_bg"])
        lbl_cell.alignment = Alignment(horizontal="center", vertical="center")

        # KPI Value
        val_cell = ws.cell(row=start_row + 1, column=2)
        val_cell.value = value
        val_cell.font = Font(name="Segoe UI", size=22, bold=True, color=theme_colors["sidebar_fg"])
        val_cell.alignment = Alignment(horizontal="center", vertical="center")

        # Spacing
        start_row += 4
```
```