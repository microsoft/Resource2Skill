### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed KPI Card Row

* **Tier**: component
* **Core Mechanism**: Renders a visually distinct section header and a row of KPI cards side-by-side. Each card employs a merged-cell layout for large value displays and a split 4-column footer for target/prior period comparisons, complete with conditional formatting applied to the main value.
* **Applicability**: Perfect for high-level executive dashboards where summarizing key metrics (like DSO, Gross Margin, CAC) with clear visual performance indicators is required.

### 2. Structural Breakdown

- **Data Layout**: Each KPI card occupies 4 columns and 3 rows. A row of 3 cards requires 14 columns total (including 1-column spacers).
- **Formula Logic**: Applies `CellIsRule` conditional formatting to the merged main value cell to dynamically color it green or red based on a comparison to the target cell.
- **Visual Design**: 
  - Section Header: Theme accent background, white bold text, centered.
  - Card Title: Light gray/theme secondary background, centered, bold.
  - Card Value: Large font (size 24), centered, vertical center.
  - Card Footer: Small font (size 9), gray borders, subtle row layout.
- **Charts/Tables**: N/A (Visual grid layout)
- **Theme Hooks**: Uses `accent_bg` for section headers, `secondary_bg` for card headers, and `good_bg`/`bad_bg` for conditional formatting colors.

### 3. Reproduction Code

```python
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string, get_column_letter
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule

def _get_theme(theme_name: str) -> dict:
    """Mock theme loader for standardized palette access."""
    themes = {
        "corporate_blue": {
            "accent_bg": "F79646",   # Orange section headers like the video
            "accent_fg": "FFFFFF",
            "card_header_bg": "DCE6F1",
            "card_header_fg": "000000",
            "footer_bg": "F2F2F2",
            "good_bg": "C4D79B",     # Light green
            "bad_bg": "F2DCDB",      # Light pink/red
            "border_color": "BFBFBF"
        }
    }
    return themes.get(theme_name, themes["corporate_blue"])

def render(ws, anchor: str, *, section_title: str, kpis: list[dict], theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a row of KPI cards with a section header.
    
    :param ws: openpyxl Worksheet
    :param anchor: Top-left cell (e.g., "B2")
    :param section_title: Title for the section (e.g., "Working Capital Efficiency")
    :param kpis: List of KPI dicts: 
                 [{"title": "DSO", "value": 31, "target": 45, "prior": 41, "good_direction": "down"}]
    """
    palette = _get_theme(theme)
    
    # Setup styles
    thin_border = Border(
        left=Side(style='thin', color=palette["border_color"]),
        right=Side(style='thin', color=palette["border_color"]),
        top=Side(style='thin', color=palette["border_color"]),
        bottom=Side(style='thin', color=palette["border_color"])
    )
    center_align = Alignment(horizontal="center", vertical="center")
    
    header_fill = PatternFill(start_color=palette["accent_bg"], end_color=palette["accent_bg"], fill_type="solid")
    header_font = Font(color=palette["accent_fg"], bold=True, size=14)
    
    card_title_fill = PatternFill(start_color=palette["card_header_bg"], end_color=palette["card_header_bg"], fill_type="solid")
    card_title_font = Font(color=palette["card_header_fg"], bold=True, size=11)
    
    footer_fill = PatternFill(start_color=palette["footer_bg"], end_color=palette["footer_bg"], fill_type="solid")
    footer_font = Font(size=9)
    footer_font_bold = Font(size=9, bold=True)
    
    good_fill = PatternFill(start_color=palette["good_bg"], end_color=palette["good_bg"], fill_type="solid")
    bad_fill = PatternFill(start_color=palette["bad_bg"], end_color=palette["bad_bg"], fill_type="solid")

    xy = coordinate_from_string(anchor)
    start_col = column_index_from_string(xy[0])
    start_row = xy[1]
    
    # Calculate total width (4 cols per KPI + 1 spacer col between them)
    num_kpis = len(kpis)
    total_cols = (num_kpis * 4) + (num_kpis - 1)
    end_col = start_col + total_cols - 1
    
    # 1. Render Section Title
    section_title_cell = ws.cell(row=start_row, column=start_col, value=section_title)
    section_title_cell.fill = header_fill
    section_title_cell.font = header_font
    section_title_cell.alignment = center_align
    ws.merge_cells(start_row=start_row, start_column=start_col, end_row=start_row, end_column=end_col)
    ws.row_dimensions[start_row].height = 25
    
    # 2. Render KPIs
    current_col = start_col
    card_start_row = start_row + 1
    
    ws.row_dimensions[card_start_row + 1].height = 40  # Make the value row tall
    
    for kpi in kpis:
        # Layout: 4 columns wide
        c1, c2, c3, c4 = current_col, current_col+1, current_col+2, current_col+3
        
        # Title Row
        title_cell = ws.cell(row=card_start_row, column=c1, value=kpi["title"])
        title_cell.fill = card_title_fill
        title_cell.font = card_title_font
        title_cell.alignment = center_align
        ws.merge_cells(start_row=card_start_row, start_column=c1, end_row=card_start_row, end_column=c4)
        
        # Apply border to title
        for col in range(c1, c4 + 1):
            ws.cell(row=card_start_row, column=col).border = thin_border
            
        # Value Row
        val_cell = ws.cell(row=card_start_row + 1, column=c1, value=kpi["value"])
        val_cell.font = Font(size=24, bold=True)
        val_cell.alignment = center_align
        ws.merge_cells(start_row=card_start_row + 1, start_column=c1, end_row=card_start_row + 1, end_column=c4)
        
        for col in range(c1, c4 + 1):
            ws.cell(row=card_start_row + 1, column=col).border = thin_border
            
        # Footer Row (Vs Target | Target Val | Vs Prior | Prior Val)
        f_labels = ["Vs. Target", "Vs. Prior Month"]
        f_vals = [kpi["target"], kpi["prior"]]
        
        for i, col in enumerate([c1, c2, c3, c4]):
            cell = ws.cell(row=card_start_row + 2, column=col)
            cell.fill = footer_fill
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center", vertical="center")
            
            if i % 2 == 0:
                cell.value = f_labels[i // 2]
                cell.font = footer_font
            else:
                cell.value = f_vals[i // 2]
                cell.font = footer_font_bold
                
        # Conditional Formatting on the Value Cell
        val_coord = val_cell.coordinate
        target_coord = ws.cell(row=card_start_row + 2, column=c2).coordinate
        
        if kpi.get("good_direction", "up") == "up":
            # Higher is better
            ws.conditional_formatting.add(
                f"{val_coord}:{val_coord}",
                CellIsRule(operator='greaterThanOrEqual', formula=[target_coord], fill=good_fill)
            )
            ws.conditional_formatting.add(
                f"{val_coord}:{val_coord}",
                CellIsRule(operator='lessThan', formula=[target_coord], fill=bad_fill)
            )
        else:
            # Lower is better (e.g., DSO)
            ws.conditional_formatting.add(
                f"{val_coord}:{val_coord}",
                CellIsRule(operator='lessThanOrEqual', formula=[target_coord], fill=good_fill)
            )
            ws.conditional_formatting.add(
                f"{val_coord}:{val_coord}",
                CellIsRule(operator='greaterThan', formula=[target_coord], fill=bad_fill)
            )

        # Move to next card anchor (skip 1 column for spacing)
        current_col += 5
```