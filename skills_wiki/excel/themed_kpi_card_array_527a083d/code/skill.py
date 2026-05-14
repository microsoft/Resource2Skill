from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import coordinate_to_tuple, get_column_letter

def render(ws, anchor: str, *, theme: str = "corporate_blue", kpis: list[dict] = None, **kwargs) -> None:
    """
    Renders an array of visually distinct KPI cards starting at the anchor cell.
    Mimics the look of floating shapes using robust merged-cell dashboard techniques.
    """
    if not kpis:
        # Default mock data matching the tutorial's use case
        kpis = [
            {"title": "Asia", "metric": "Revenue", "value": 369989, "num_fmt": "$#,##0", "badge": 0.05, "badge_fmt": "0%"},
            {"title": "Europe", "metric": "Revenue", "value": 916879, "num_fmt": "$#,##0", "badge": 0.12, "badge_fmt": "0%"},
            {"title": "North America", "metric": "Revenue", "value": 1915991, "num_fmt": "$#,##0", "badge": 0.25, "badge_fmt": "0%"}
        ]

    # Standard theme palette fallback
    palettes = {
        "corporate_blue": {"bg": "1E3A8A", "accent": "3B82F6", "text": "FFFFFF"}, # Navy & Bright Blue
        "executive_dark": {"bg": "1F2937", "accent": "10B981", "text": "F9FAFB"}, # Dark Slate & Emerald
        "warm_sunset": {"bg": "7C2D12", "accent": "F59E0B", "text": "FFFBEB"}     # Deep Orange & Amber
    }
    active_palette = palettes.get(theme, palettes["corporate_blue"])

    # Style definitions
    bg_fill = PatternFill(start_color=active_palette["bg"], fill_type="solid")
    accent_fill = PatternFill(start_color=active_palette["accent"], fill_type="solid")
    
    title_font = Font(color=active_palette["text"], size=12, bold=True)
    metric_font = Font(color=active_palette["text"], size=10, italic=True)
    value_font = Font(color=active_palette["text"], size=18, bold=True)
    badge_font = Font(color=active_palette["text"], size=14, bold=True)

    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center", indent=1)
    
    # Clean border to give the "card" a distinct edge
    thin_edge = Side(border_style="thin", color="FFFFFF")
    card_border = Border(top=thin_edge, left=thin_edge, right=thin_edge, bottom=thin_edge)

    start_row, start_col = coordinate_to_tuple(anchor)

    for i, kpi in enumerate(kpis):
        # Each KPI card occupies 3 columns, plus 1 column for spacing
        col_offset = i * 4 
        base_r = start_row
        base_c = start_col + col_offset

        # 1. Setup card dimensions
        ws.column_dimensions[get_column_letter(base_c)].width = 12
        ws.column_dimensions[get_column_letter(base_c+1)].width = 12
        ws.column_dimensions[get_column_letter(base_c+2)].width = 10
        ws.row_dimensions[base_r].height = 20
        ws.row_dimensions[base_r+1].height = 15
        ws.row_dimensions[base_r+2].height = 30

        # 2. Apply base background & borders to the entire 3x3 block
        for r in range(base_r, base_r + 3):
            for c in range(base_c, base_c + 3):
                cell = ws.cell(row=r, column=c)
                cell.fill = bg_fill
                cell.border = card_border

        # 3. Top Row: Title (Merged across first 2 columns of the card)
        ws.merge_cells(start_row=base_r, start_column=base_c, end_row=base_r, end_column=base_c+1)
        title_cell = ws.cell(row=base_r, column=base_c, value=kpi.get("title", ""))
        title_cell.font = title_font
        title_cell.alignment = left_align

        # 4. Middle Row: Subtitle / Metric Label
        ws.merge_cells(start_row=base_r+1, start_column=base_c, end_row=base_r+1, end_column=base_c+1)
        metric_cell = ws.cell(row=base_r+1, column=base_c, value=kpi.get("metric", ""))
        metric_cell.font = metric_font
        metric_cell.alignment = left_align

        # 5. Bottom Row: Primary Value
        ws.merge_cells(start_row=base_r+2, start_column=base_c, end_row=base_r+2, end_column=base_c+1)
        val_cell = ws.cell(row=base_r+2, column=base_c, value=kpi.get("value", 0))
        val_cell.font = value_font
        val_cell.alignment = left_align
        val_cell.number_format = kpi.get("num_fmt", "General")

        # 6. Right Column Badge: Market Share / Secondary Percentage
        ws.merge_cells(start_row=base_r, start_column=base_c+2, end_row=base_r+2, end_column=base_c+2)
        badge_cell = ws.cell(row=base_r, column=base_c+2, value=kpi.get("badge", ""))
        badge_cell.font = badge_font
        badge_cell.fill = accent_fill
        badge_cell.alignment = center_align
        badge_cell.number_format = kpi.get("badge_fmt", "General")
