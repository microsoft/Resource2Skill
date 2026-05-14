### 1. High-level Skill Pattern Extraction

> **Skill Name**: Sidebar KPI Panel

* **Tier**: component
* **Core Mechanism**: Constructs a vertical KPI sidebar directly in the worksheet grid using continuous cell fills, variable row heights, and contrasting font formats. This replaces the need for brittle floating shape/text boxes by embedding the layout natively in the cells, mapping emojis to labels, and formatting values with prominent typography.
* **Applicability**: Ideal for interactive dashboard layouts that require a high-visibility summary of key metrics along the left or right margin. Works best on a dedicated "Presentation" sheet where gridlines are hidden and columns are manipulated to act as layout containers.

### 2. Structural Breakdown

- **Data Layout**: Single widened column acting as a vertical container. Uses alternating rows: Row `N` for the Label/Icon, Row `N+1` (widened height) for the Value, and Row `N+2` as an empty spacer to maintain visual padding.
- **Formula Logic**: Directly injects pre-formatted string values (can seamlessly be adapted to accept `=Calculation!A1` formula links).
- **Visual Design**: Hides sheet gridlines. Applies a deep, continuous thematic background fill down the entire column. Uses large, bold white typography for KPI values and smaller, accent-colored typography for labels. 
- **Charts/Tables**: Layout structure component (creates the anchor space for adjacent charts).
- **Theme Hooks**: Utilizes `primary_bg` for the sidebar background, `primary_fg` (typically white) for main values and title, and an `accent` color for the metric labels.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
from openpyxl.worksheet.worksheet import Worksheet

def render(ws: Worksheet, anchor: str, *, title: str = "VIVA CALIF", kpis: list[dict] = None, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a vertical KPI sidebar panel natively in the grid.
    
    :param ws: The openpyxl worksheet.
    :param anchor: Top-left cell for the sidebar (e.g., 'B2').
    :param title: The title at the top of the sidebar.
    :param kpis: List of dicts with 'label', 'value', and optional 'icon'.
    :param theme: Theme identifier string.
    """
    if not kpis:
        kpis = [
            {"label": "Orders", "value": "2,400", "icon": "🛒"},
            {"label": "Quantity", "value": "11,997", "icon": "📦"},
            {"label": "Amount", "value": "$649.0k", "icon": "💰"},
            {"label": "Avg Rating", "value": "4.0", "icon": "⭐"}
        ]

    # Minimal self-contained theme palette
    palettes = {
        "corporate_blue": {"bg": "1F4E78", "fg": "FFFFFF", "accent": "D9E1F2"},
        "viva_green": {"bg": "1E463A", "fg": "FFFFFF", "accent": "A8D08D"}, # Matches tutorial's dark green sidebar
        "dark_slate": {"bg": "262626", "fg": "FFFFFF", "accent": "D9D9D9"}
    }
    palette = palettes.get(theme, palettes["corporate_blue"])

    # Style Definitions
    bg_fill = PatternFill(start_color=palette["bg"], end_color=palette["bg"], fill_type="solid")
    title_font = Font(name="Arial Black", size=18, bold=True, color=palette["fg"])
    val_font = Font(name="Arial", size=22, bold=True, color=palette["fg"])
    lbl_font = Font(name="Arial", size=12, bold=True, color=palette["accent"])
    center_align = Alignment(horizontal="center", vertical="center")

    # Resolve coordinates
    col_str, row_idx = coordinate_from_string(anchor)
    col_idx = column_index_from_string(col_str)

    # Configure Sheet and Column
    ws.sheet_view.showGridLines = False
    ws.column_dimensions[col_str].width = 24

    # Pre-paint the background for the entire sidebar area
    total_rows = 4 + (len(kpis) * 3) + 4 # Title area + KPI blocks + Bottom padding
    for r in range(row_idx, row_idx + total_rows):
        ws.cell(row=r, column=col_idx).fill = bg_fill

    # Render Title
    title_cell = ws.cell(row=row_idx + 1, column=col_idx)
    title_cell.value = title
    title_cell.font = title_font
    title_cell.alignment = center_align

    # Render KPIs
    current_row = row_idx + 4
    for kpi in kpis:
        # Construct and render the label row
        lbl_cell = ws.cell(row=current_row, column=col_idx)
        icon_str = kpi.get('icon', '')
        label_str = kpi.get('label', '')
        lbl_cell.value = f"{icon_str} {label_str}".strip()
        lbl_cell.font = lbl_font
        lbl_cell.alignment = center_align

        # Construct and render the value row
        val_cell = ws.cell(row=current_row + 1, column=col_idx)
        val_cell.value = kpi.get("value", "")
        val_cell.font = val_font
        val_cell.alignment = center_align
        
        # Increase the row height of the value row to give structural padding 
        ws.row_dimensions[current_row + 1].height = 35 

        # Advance down to the next block (Label, Value, Blank Spacer)
        current_row += 3
```