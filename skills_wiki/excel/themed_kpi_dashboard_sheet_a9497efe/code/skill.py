from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule

def render_sheet(wb: Workbook, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a themed KPI Dashboard with standardized metric cards and conditional formatting.
    """
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # 1. Fallback Theme Palette
    theme_colors = {
        "corporate_blue": {
            "primary": "003366",     # Section headers
            "secondary": "4F81BD",   # Card titles
            "accent": "DCE6F1",      # Dropdown background
            "good_bg": "C6EFCE",     # Green CF fill
            "good_fg": "006100",     # Green CF text
            "bad_bg": "FFC7CE",      # Red CF fill
            "bad_fg": "9C0006",      # Red CF text
            "text": "000000",
            "bg": "FFFFFF",
            "border": "B2B2B2"
        }
    }
    palette = theme_colors.get(theme, theme_colors["corporate_blue"])

    # 2. Reusable Styles
    title_font = Font(name="Calibri", size=18, bold=True, color=palette["primary"])
    section_font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    card_title_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    card_val_font = Font(name="Calibri", size=24, bold=True)
    footer_label_font = Font(name="Calibri", size=9, color="595959")
    footer_val_font = Font(name="Calibri", size=10, bold=True)

    center_al = Alignment(horizontal="center", vertical="center")
    left_al = Alignment(horizontal="left", vertical="center")
    right_al = Alignment(horizontal="right", vertical="center")

    thin_side = Side(border_style="thin", color=palette["border"])
    card_border = Border(top=thin_side, left=thin_side, right=thin_side, bottom=thin_side)

    # 3. Component Render Helpers
    def set_merged_style(_ws, r, c, r2, c2, font, fill, alignment, border=None):
        _ws.merge_cells(start_row=r, start_column=c, end_row=r2, end_column=c2)
        cell = _ws.cell(row=r, column=c)
        if font: cell.font = font
        if fill: cell.fill = fill
        if alignment: cell.alignment = alignment
        
        if border:
            for row_idx in range(r, r2 + 1):
                for col_idx in range(c, c2 + 1):
                    _ws.cell(row_idx, col_idx).border = border

    def add_kpi_card(r, c, title_text, main_val, target_val, prior_val, is_lower_better, format_str="#,##0"):
        # Header Row
        fill_title = PatternFill("solid", fgColor=palette["secondary"])
        set_merged_style(ws, r, c, r, c+3, card_title_font, fill_title, center_al, card_border)
        ws.cell(r, c, title_text)

        # Main Value Row
        fill_val = PatternFill("solid", fgColor="F2F2F2")
        set_merged_style(ws, r+1, c, r+1, c+3, card_val_font, fill_val, center_al, card_border)
        v_cell = ws.cell(r+1, c, main_val)
        v_cell.number_format = format_str

        # Footer Row - 4 distinct sub-columns
        ws.cell(r+2, c, "Vs. Target").font = footer_label_font
        ws.cell(r+2, c).alignment = right_al
        ws.cell(r+2, c).border = card_border

        t_cell = ws.cell(r+2, c+1, target_val)
        t_cell.font = footer_val_font
        t_cell.alignment = left_al
        t_cell.number_format = format_str
        t_cell.border = card_border

        ws.cell(r+2, c+2, "Vs. Prior Mth").font = footer_label_font
        ws.cell(r+2, c+2).alignment = right_al
        ws.cell(r+2, c+2).border = card_border

        p_cell = ws.cell(r+2, c+3, prior_val)
        p_cell.font = footer_val_font
        p_cell.alignment = left_al
        p_cell.number_format = format_str
        p_cell.border = card_border

        # Conditional Formatting anchoring logic
        green_fill = PatternFill(start_color=palette["good_bg"], end_color=palette["good_bg"], fill_type="solid")
        green_font = Font(color=palette["good_fg"], bold=True, size=24)
        red_fill = PatternFill(start_color=palette["bad_bg"], end_color=palette["bad_bg"], fill_type="solid")
        red_font = Font(color=palette["bad_fg"], bold=True, size=24)

        op_good, op_bad = ('lessThanOrEqual', 'greaterThan') if is_lower_better else ('greaterThanOrEqual', 'lessThan')
        
        # Absolute reference to the target cell so merged range formats correctly
        target_ref = f"${t_cell.column_letter}${t_cell.row}"

        ws.conditional_formatting.add(
            v_cell.coordinate,
            CellIsRule(operator=op_good, formula=[target_ref], fill=green_fill, font=green_font)
        )
        ws.conditional_formatting.add(
            v_cell.coordinate,
            CellIsRule(operator=op_bad, formula=[target_ref], fill=red_fill, font=red_font)
        )

    # 4. Layout Construction
    ws.cell(1, 2, title).font = title_font

    # Global Month Dropdown
    ws.cell(3, 2, "For the month of:").font = Font(bold=True)
    m_cell = ws.cell(3, 3, "Aug-20")
    m_cell.fill = PatternFill("solid", fgColor=palette["accent"])
    m_cell.border = card_border
    m_cell.alignment = center_al

    dv = DataValidation(type="list", formula1='"Jan-20,Feb-20,Mar-20,Apr-20,May-20,Jun-20,Jul-20,Aug-20"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(m_cell)

    # Section 1: Working Capital
    fill_section = PatternFill("solid", fgColor=palette["primary"])
    set_merged_style(ws, 5, 2, 5, 15, section_font, fill_section, center_al)
    ws.cell(5, 2, "Working Capital Efficiency")

    add_kpi_card(7, 2, "DSO (Days Sales Outstanding)", 31, 45, 41, is_lower_better=True)
    add_kpi_card(7, 7, "DPO (Days Payables Outstanding)", 89, 90, 90, is_lower_better=True)
    add_kpi_card(7, 12, "Non-Current AR %", 0.12, 0.03, 0.12, is_lower_better=True, format_str="0%")

    # Section 2: Sales Metrics
    set_merged_style(ws, 11, 2, 11, 15, section_font, fill_section, center_al)
    ws.cell(11, 2, "Sales KPIs")

    add_kpi_card(13, 2, "CAC (Customer Acq. Cost)", 26319, 15000, 17725, is_lower_better=True, format_str="$#,##0")
    add_kpi_card(13, 7, "Sales vs. Budget %", 1.62, 1.00, 1.27, is_lower_better=False, format_str="0%")
    add_kpi_card(13, 12, "Gross Margin", 0.20, 0.38, 0.26, is_lower_better=False, format_str="0%")

    # 5. Column Formatting Constraints
    widths = {
        'A': 3,
        'B': 14, 'C': 10, 'D': 14, 'E': 10, # Card 1 (4 Cols)
        'F': 3,                             # Gutter
        'G': 14, 'H': 10, 'I': 14, 'J': 10, # Card 2 (4 Cols)
        'K': 3,                             # Gutter
        'L': 14, 'M': 10, 'N': 14, 'O': 10  # Card 3 (4 Cols)
    }
    for col_letter, width in widths.items():
        ws.column_dimensions[col_letter].width = width
