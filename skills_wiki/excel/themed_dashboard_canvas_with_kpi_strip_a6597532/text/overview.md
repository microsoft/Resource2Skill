### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Dashboard Canvas with KPI Strip

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a sleek, "shape-free" dashboard canvas by disabling gridlines, applying distinct background fills for a header banner and content area, and building a responsive row of KPI cards using merged cells, contrasting background colors, and precise alignments (translating the video's floating shape approach into a highly robust, automation-friendly cell grid).
* **Applicability**: Ideal for generating the foundational layout of executive summaries or KPI dashboards. Provides a clean, SaaS-like UI using native cell formatting, which is much more stable to automate and populate via Python than floating shape objects.

### 2. Structural Breakdown

- **Data Layout**: 
  - Row 1–8: Header block containing the Title (Row 2), Subtitle (Row 3), and KPI Cards (Row 5–6).
  - Row 9+: Main canvas block reserved for charts and tables.
  - KPI Cards: Anchored dynamically starting at Column C, spaced by empty columns. Each card spans 2 columns (accent strip + content) and 2 rows.
- **Formula Logic**: Readies static or aggregated top-line metrics directly into the cell values, bypassing the need for shape-to-cell formula links (`GETPIVOTDATA`).
- **Visual Design**: Gridlines disabled. Dual-tone canvas (dark header, light background). KPI cards use a solid colored left-border cell and a white data block with varying font sizes (18pt bold for values, 10pt regular for labels) to establish visual hierarchy.
- **Charts/Tables**: Leaves the underlying `ws` grid ready for downstream component insertion (like pivot charts or data bar leaderboards).
- **Theme Hooks**: Utilizes `header_bg` (Dark Purple banner), `canvas_bg` (Light Purple canvas background), `accent` (Gold subtitles and KPI accent strips), `text_light` (White), and `text_dark` (Dark Purple).

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard", subtitle: str = "Evaluating Sales Agent Performance", kpis: list = None, theme: dict = None, **kwargs) -> None:
    """
    Generates a styled dashboard canvas with a dark header banner, light canvas background,
    and a strip of cell-based KPI cards.
    """
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)

    # 1. Theme Configuration (Fallback to the video's purple/gold theme)
    theme = theme or {}
    header_bg = theme.get("header_bg", "4B286D")  # Dark Purple
    canvas_bg = theme.get("canvas_bg", "F2EFF5")  # Light Purple
    accent_color = theme.get("accent", "E5A823")  # Gold
    text_light = theme.get("text_light", "FFFFFF")
    text_dark = theme.get("text_dark", "4B286D")

    # 2. Canvas Setup
    ws.sheet_view.showGridLines = False
    header_fill = PatternFill(start_color=header_bg, end_color=header_bg, fill_type="solid")
    canvas_fill = PatternFill(start_color=canvas_bg, end_color=canvas_bg, fill_type="solid")

    # Apply background fills (A1:Z50 as default canvas bounding area)
    for row in range(1, 51):
        for col in range(1, 27):
            cell = ws.cell(row=row, column=col)
            if row <= 8:
                cell.fill = header_fill
            else:
                cell.fill = canvas_fill

    # 3. Header Text Setup
    ws.column_dimensions['A'].width = 3  # Left margin padding
    ws.column_dimensions['B'].width = 5  # Title margin padding

    title_cell = ws["B2"]
    title_cell.value = title
    title_cell.font = Font(name="Arial", size=28, color=text_light, bold=True)

    subtitle_cell = ws["B3"]
    subtitle_cell.value = subtitle
    subtitle_cell.font = Font(name="Arial", size=14, color=accent_color)

    # 4. KPI Ribbon Generation
    if not kpis:
        kpis = [
            {"label": "TOTAL CALLS", "value": "16,749"},
            {"label": "CALLS REACHED", "value": "3,328"},
            {"label": "DEALS CLOSED", "value": "1,203"},
            {"label": "DEAL VALUE", "value": "$646,979"}
        ]

    start_col = 3  # Start KPI cards at column C
    for kpi in kpis:
        # Layout: 2 columns wide (Accent strip + Value/Label box), 2 rows high
        accent_col_letter = get_column_letter(start_col)
        content_col_letter = get_column_letter(start_col + 1)

        # Left Accent Strip (Merge rows 5-6)
        ws.merge_cells(start_row=5, start_column=start_col, end_row=6, end_column=start_col)
        accent_cell = ws.cell(row=5, column=start_col)
        accent_cell.fill = PatternFill(start_color=accent_color, end_color=accent_color, fill_type="solid")

        # Top Right: Value (Large text, bottom aligned)
        val_cell = ws.cell(row=5, column=start_col + 1)
        val_cell.value = kpi["value"]
        val_cell.fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
        val_cell.font = Font(name="Arial", size=18, color=text_dark, bold=True)
        val_cell.alignment = Alignment(horizontal="center", vertical="bottom")

        # Bottom Right: Label (Small text, top aligned)
        lbl_cell = ws.cell(row=6, column=start_col + 1)
        lbl_cell.value = kpi["label"]
        lbl_cell.fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
        lbl_cell.font = Font(name="Arial", size=10, color=text_dark)
        lbl_cell.alignment = Alignment(horizontal="center", vertical="top")

        # Set specific dimensions for the KPI card to look like a contiguous block
        ws.column_dimensions[accent_col_letter].width = 2
        ws.column_dimensions[content_col_letter].width = 18

        # Move to next card position (leaving 1 column as spacing buffer)
        start_col += 3  

    # Expand row heights to give the KPI cards breathing room
    ws.row_dimensions[5].height = 25
    ws.row_dimensions[6].height = 18
```