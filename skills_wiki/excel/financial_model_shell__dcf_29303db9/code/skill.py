from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "Company DCF", ticker: str = "AMZN", start_year: int = 2023, num_years: int = 5, theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # Clean canvas: standard for financial modeling
    ws.sheet_view.showGridLines = False

    # Theme palette fallback
    palettes = {
        "corporate_blue": {"header_bg": "D9D9D9", "text": "000000"}, # Standard light gray for IB models
        "dark": {"header_bg": "404040", "text": "FFFFFF"}
    }
    palette = palettes.get(theme, palettes["corporate_blue"])

    # Styles
    header_fill = PatternFill(start_color=palette["header_bg"], end_color=palette["header_bg"], fill_type="solid")
    title_font = Font(size=16, bold=True, color=palette["text"])
    bold_font = Font(bold=True, color=palette["text"])
    italic_font = Font(italic=True, color=palette["text"])
    
    thin_border = Border(top=Side(style='thin'), bottom=Side(style='thin'))
    bottom_border = Border(bottom=Side(style='thin'))

    # Top Information Block
    ws["A2"] = title
    ws["A2"].font = title_font
    
    ws["A4"] = "Ticker"
    ws["B4"] = ticker
    ws["A5"] = "Date"
    ws["B5"] = "12/31/2023"
    
    # Standard Model Column Widths
    ws.column_dimensions['A'].width = 28  # Labels
    ws.column_dimensions['B'].width = 3   # Spacer
    for col in range(3, 3 + num_years):
        ws.column_dimensions[get_column_letter(col)].width = 12  # Projection Years
        
    current_row = 7
    
    def add_section(name: str, items: list, include_years: bool = False):
        nonlocal current_row
        
        # Section Header (Spans across all projection columns)
        ws.cell(row=current_row, column=1, value=name).font = bold_font
        for col in range(1, 3 + num_years):
            cell = ws.cell(row=current_row, column=col)
            cell.fill = header_fill
            cell.border = thin_border
            
        current_row += 1
        
        # Timeline Header
        if include_years:
            for i in range(num_years):
                c = ws.cell(row=current_row, column=3 + i, value=start_year + i)
                c.font = bold_font
                c.alignment = Alignment(horizontal="right")
            
            # Bottom border under the timeline
            for col in range(1, 3 + num_years):
                ws.cell(row=current_row, column=col).border = bottom_border
            current_row += 1
            
        # Section Line Items
        for item in items:
            c = ws.cell(row=current_row, column=1, value=item)
            # Stylistic convention: italicize rates and margins
            if item.startswith("%") or "margin" in item.lower() or "growth" in item.lower():
                c.font = italic_font
            current_row += 1
            
        current_row += 2 # Padding before next section

    # Build the model shell sections
    add_section("Assumptions", [
        "Revenue Growth",
        "EBIT Margin",
        "Tax Rate",
        "WACC",
        "Terminal Growth Rate"
    ])
    
    add_section("Income Statement", [
        "Revenue",
        "% growth",
        "EBIT",
        "% margin",
        "Taxes",
        "EBIAT"
    ], include_years=True)
    
    add_section("Cash Flow Items", [
        "D&A",
        "% of sales",
        "CapEx",
        "% of sales",
        "Change in NWC",
        "% of change in sales"
    ], include_years=True)
    
    add_section("DCF", [
        "Unlevered FCF",
        "Time Period",
        "Discount Factor",
        "Present Value of FCF"
    ], include_years=True)

