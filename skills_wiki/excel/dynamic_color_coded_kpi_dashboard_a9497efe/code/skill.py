from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule, FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
from datetime import datetime
from openpyxl.styles.colors import Color

# Helper functions for theming (assuming these exist in a _helpers module)
# For this example, I'll include basic definitions.
class Theme:
    def __init__(self, palette):
        self.palette = palette

    def get_color(self, name, default="000000"):
        return self.palette.get(name, default)

def get_theme_palette(theme_name="corporate_blue"):
    palettes = {
        "corporate_blue": {
            "header_bg": "FF4F81BD",
            "header_fg": "FFFFFFFF",
            "section_bg": "FFD8D8D8",
            "section_fg": "FF000000",
            "accent_bg": "FF8DB4E2",
            "accent_fg": "FF000000",
            "good_fill": "FFC6EFCE", # Light Green
            "good_fg": "FF006100",  # Dark Green
            "bad_fill": "FFFFC7CE",  # Light Red/Pink
            "bad_fg": "FF9C0006",   # Dark Red
            "text_fg": "FF000000",
        },
        # Add other themes here if needed
    }
    return palettes.get(theme_name, palettes["corporate_blue"])

def apply_style(cell, font_size=10, bold=False, fill_color=None, font_color=None, alignment=None, border=None):
    if font_color:
        cell.font = Font(size=font_size, bold=bold, color=Color(font_color))
    else:
        cell.font = Font(size=font_size, bold=bold)
    if fill_color:
        cell.fill = PatternFill(start_color=Color(fill_color), end_color=Color(fill_color), fill_type="solid")
    if alignment:
        cell.alignment = alignment
    if border:
        cell.border = border

def create_border(style="thin", color="000000"):
    side = Side(border_style=style, color=Color(color))
    return Border(left=side, right=side, top=side, bottom=side)

def render_workbook(wb, *, title: str = "KPI Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    palette = get_theme_palette(theme)

    # 1. Data Sheet
    ws_data = wb.create_sheet("1) Data", 0)
    data_header = ["Category", "Jan-20", "Feb-20", "Mar-20", "Apr-20", "May-20", "Jun-20", "Jul-20", "Aug-20", "Sep-20", "Oct-20", "Nov-20", "Dec-20"]
    ws_data.append(data_header)

    # Sample Data (as seen in video, simplified)
    data_rows = [
        ["Sales", 1500000, 1590000, 1685400, 1786524, 1893716, 2007338, 2127778, 2255445, 2390772, 2534158, 2686208, 2847380],
        ["COGS", 900000, 954000, 1010320, 1070922, 1135178, 1203289, 1275486, 1351988, 1432907, 1519881, 1610074, 1706678],
        ["Gross Profit", 600000, 636000, 655080, 684082, 725126, 729125, 852292, 903457, 957865, 1014277, 1076134, 1140702],
        ["Account Receivables Balance", 2800000, 2940000, 3087000, 3241350, 3403418, 3573588, 3752268, 3939881, 4136875, 4343719, 4560905, 4788950],
        ["Past due Accounts Receivables", 150000, 140000, 122500, 111500, 100000, 90000, 80000, 70000, 60000, 50000, 40000, 30000],
        ["Accounts Payable Balance", 3100000, 3255000, 3417750, 3588638, 3768069, 3956473, 4154296, 4362011, 4580112, 4809117, 5050573, 5303578],
        ["OPEX Actual", 600500, 626510, 643136, 675292, 709057, 720594, 750000, 787500, 826875, 868219, 911630, 957211],
        ["Full Time Employees", 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57],
        ["Sales & Marketing Costs", 350000, 360000, 377000, 394000, 411000, 428000, 445000, 462000, 479000, 496000, 513000, 530000],
        ["# of new customers", 40, 48, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100],
        ["Sales Budget", 1680000, 1750000, 1820000, 1890000, 1960000, 2030000, 2100000, 2170000, 2240000, 2310000, 2380000, 2450000],
        ["COGS Budget", 990000, 1050000, 1110000, 1170000, 1230000, 1290000, 1350000, 1410000, 1470000, 1530000, 1590000, 1650000],
        ["OPEX Budget", 550000, 550000, 550000, 550000, 550000, 550000, 550000, 550000, 550000, 550000, 550000, 550000],
    ]
    for row_data in data_rows:
        ws_data.append(row_data)

    # Format data sheet (basic)
    for row_idx, row in enumerate(ws_data.iter_rows()):
        for cell_idx, cell in enumerate(row):
            if row_idx == 0:
                apply_style(cell, bold=True, fill_color=palette["header_bg"], font_color=palette["header_fg"])
            elif cell_idx > 0:
                if row_idx in [1,2,3,4,6,8,11,12,13]: # Rows with currency or large numbers
                    cell.number_format = '$#,##0'
                else:
                    cell.number_format = '#,##0'

    # 2. Staging Sheet
    ws_staging = wb.create_sheet("2) Staging", 1)
    ws_staging.column_dimensions['A'].width = 30 # Category column
    for col in range(2, len(data_header) + 1):
        ws_staging.column_dimensions[get_column_letter(col)].width = 15

    # Working Capital Efficiency KPIs
    ws_staging.cell(row=1, column=1, value="1) Working Capital Efficiency")
    apply_style(ws_staging.cell(row=1, column=1), bold=True, fill_color=palette["section_bg"], font_color=palette["section_fg"])

    ws_staging.cell(row=3, column=1, value="Category")
    for col_idx, month_str in enumerate(data_header[1:], 2):
        # Store full date objects in staging to allow EOMONTH logic to work correctly
        ws_staging.cell(row=3, column=col_idx, value=datetime.strptime(month_str, "%b-%y"))
        ws_staging.cell(row=3, column=col_idx).number_format = 'MMM-yy' # Display as month-year
        apply_style(ws_staging.cell(row=3, column=col_idx), bold=True, fill_color=palette["accent_bg"], font_color=palette["accent_fg"])

    # Account Receivables Balance, Credit Sales, # of days
    ws_staging.cell(row=4, column=1, value="Account Receivables Balance")
    ws_staging.cell(row=5, column=1, value="Credit Sales")
    ws_staging.cell(row=6, column=1, value="# of days")
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=4, column=col, value=f"='1) Data'!{get_column_letter(col)}5") # AR Balance is row 5 in Data
        ws_staging.cell(row=5, column=col, value=f"='1) Data'!{get_column_letter(col)}2") # Sales is row 2 in Data (used as Credit Sales)
        ws_staging.cell(row=6, column=col, value=f"=DAY({get_column_letter(col)}3)") # Days in month
        ws_staging.cell(row=4, column=col).number_format = '$#,##0'
        ws_staging.cell(row=5, column=col).number_format = '$#,##0'

    # DSO (Days Sales Outstanding)
    ws_staging.cell(row=7, column=1, value="DSO (Days Sales Outstanding)")
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=7, column=col, value=f"=IFERROR(({get_column_letter(col)}4/{get_column_letter(col)}5)*{get_column_letter(col)}6,0)")
    ws_staging.cell(row=8, column=1, value="Target")
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=8, column=col, value=45) # Hardcoded target as per video

    # Accounts Payable Balance, COGS, # of days
    ws_staging.cell(row=10, column=1, value="Accounts Payable Balance")
    ws_staging.cell(row=11, column=1, value="COGS")
    ws_staging.cell(row=12, column=1, value="# of days")
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=10, column=col, value=f"='1) Data'!{get_column_letter(col)}7") # AP Balance is row 7 in Data
        ws_staging.cell(row=11, column=col, value=f"='1) Data'!{get_column_letter(col)}3") # COGS is row 3 in Data
        ws_staging.cell(row=12, column=col, value=f"=DAY({get_column_letter(col)}3)") # Days in month
        ws_staging.cell(row=10, column=col).number_format = '$#,##0'
        ws_staging.cell(row=11, column=col).number_format = '$#,##0'

    # DPO (Days Payables Outstanding)
    ws_staging.cell(row=13, column=1, value="DPO (Days Payables Outstanding)")
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=13, column=col, value=f"=IFERROR(({get_column_letter(col)}10/{get_column_letter(col)}11)*{get_column_letter(col)}12,0)")
    ws_staging.cell(row=14, column=1, value="Target")
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=14, column=col, value=90) # Hardcoded target as per video

    # Non-Current AR %
    ws_staging.cell(row=16, column=1, value="Accounts Receivables Balance")
    ws_staging.cell(row=17, column=1, value="Past Due Accounts Receivables")
    ws_staging.cell(row=18, column=1, value="Non-Current AR %")
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=16, column=col, value=f"='1) Data'!{get_column_letter(col)}5") # AR Balance
        ws_staging.cell(row=17, column=col, value=f"='1) Data'!{get_column_letter(col)}6") # Past Due AR Balance
        ws_staging.cell(row=16, column=col).number_format = '$#,##0'
        ws_staging.cell(row=17, column=col).number_format = '$#,##0'
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=18, column=col, value=f"=IFERROR({get_column_letter(col)}17/{get_column_letter(col)}16,0)")
        ws_staging.cell(row=18, column=col).number_format = '0%'
    ws_staging.cell(row=19, column=1, value="Target")
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=19, column=col, value=0.03) # Hardcoded target as per video (3%)

    # Sales KPIs
    ws_staging.cell(row=21, column=1, value="2) Sales KPIs")
    apply_style(ws_staging.cell(row=21, column=1), bold=True, fill_color=palette["section_bg"], font_color=palette["section_fg"])

    # Sales & Marketing Costs, # of new customers
    ws_staging.cell(row=23, column=1, value="Sales & Marketing Costs")
    ws_staging.cell(row=24, column=1, value="# of new customers")
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=23, column=col, value=f"='1) Data'!{get_column_letter(col)}10") # S&M Costs is row 10 in Data
        ws_staging.cell(row=24, column=col, value=f"='1) Data'!{get_column_letter(col)}11") # New Customers is row 11 in Data
        ws_staging.cell(row=23, column=col).number_format = '$#,##0'

    # CAC (Customer Acquisition Cost)
    ws_staging.cell(row=25, column=1, value="CAC (Customer Acquisition Cost)")
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=25, column=col, value=f"=IFERROR({get_column_letter(col)}23/{get_column_letter(col)}24,0)")
        ws_staging.cell(row=25, column=col).number_format = '$#,##0'
    ws_staging.cell(row=26, column=1, value="Target")
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=26, column=col, value=15000) # Hardcoded target as per video ($15,000)

    # Sales vs. Budget%
    ws_staging.cell(row=28, column=1, value="Sales Actual")
    ws_staging.cell(row=29, column=1, value="Sales Budget")
    ws_staging.cell(row=30, column=1, value="Sales vs. Budget%")
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=28, column=col, value=f"='1) Data'!{get_column_letter(col)}2") # Sales Actual
        ws_staging.cell(row=29, column=col, value=f"='1) Data'!{get_column_letter(col)}12") # Sales Budget
        ws_staging.cell(row=28, column=col).number_format = '$#,##0'
        ws_staging.cell(row=29, column=col).number_format = '$#,##0'
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=30, column=col, value=f"=IFERROR({get_column_letter(col)}28/{get_column_letter(col)}29,0)")
        ws_staging.cell(row=30, column=col).number_format = '0%'
    ws_staging.cell(row=31, column=1, value="Target")
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=31, column=col, value=1) # Hardcoded target as per video (100%)

    # Gross Margin
    ws_staging.cell(row=33, column=1, value="Gross Profit")
    ws_staging.cell(row=34, column=1, value="Sales")
    ws_staging.cell(row=35, column=1, value="Gross Margin")
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=33, column=col, value=f"='1) Data'!{get_column_letter(col)}4") # Gross Profit
        ws_staging.cell(row=34, column=col, value=f"='1) Data'!{get_column_letter(col)}2") # Sales
        ws_staging.cell(row=33, column=col).number_format = '$#,##0'
        ws_staging.cell(row=34, column=col).number_format = '$#,##0'
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=35, column=col, value=f"=IFERROR({get_column_letter(col)}33/{get_column_letter(col)}34,0)")
        ws_staging.cell(row=35, column=col).number_format = '0%'
    ws_staging.cell(row=36, column=1, value="Target")
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=36, column=col, value=0.38) # Hardcoded target as per video (38%)

    # Cost KPIs
    ws_staging.cell(row=38, column=1, value="3) Cost KPIs")
    apply_style(ws_staging.cell(row=38, column=1), bold=True, fill_color=palette["section_bg"], font_color=palette["section_fg"])

    # OPEX Actual vs. Budget
    ws_staging.cell(row=40, column=1, value="OPEX Actual")
    ws_staging.cell(row=41, column=1, value="OPEX Budget")
    ws_staging.cell(row=42, column=1, value="OPEX Actual vs. Budget")
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=40, column=col, value=f"='1) Data'!{get_column_letter(col)}8") # OPEX Actual is row 8 in Data
        ws_staging.cell(row=41, column=col, value=f"='1) Data'!{get_column_letter(col)}14") # OPEX Budget is row 14 in Data
        ws_staging.cell(row=40, column=col).number_format = '$#,##0'
        ws_staging.cell(row=41, column=col).number_format = '$#,##0'
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=42, column=col, value=f"=IFERROR({get_column_letter(col)}40/{get_column_letter(col)}41,0)")
        ws_staging.cell(row=42, column=col).number_format = '0%'
    ws_staging.cell(row=43, column=1, value="Target")
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=43, column=col, value=1) # Hardcoded target as per video (100%)

    # CPFTE (Cost Per Full Time Employee)
    ws_staging.cell(row=45, column=1, value="OPEX Actual")
    ws_staging.cell(row=46, column=1, value="Full Time Employees")
    ws_staging.cell(row=47, column=1, value="CPFTE (Cost Per Full Time Employee)")
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=45, column=col, value=f"='1) Data'!{get_column_letter(col)}8") # OPEX Actual
        ws_staging.cell(row=46, column=col, value=f"='1) Data'!{get_column_letter(col)}9") # FTE
        ws_staging.cell(row=45, column=col).number_format = '$#,##0'
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=47, column=col, value=f"=IFERROR({get_column_letter(col)}45/{get_column_letter(col)}46,0)")
        ws_staging.cell(row=47, column=col).number_format = '$#,##0'
    ws_staging.cell(row=48, column=1, value="Target")
    for col in range(2, len(data_header) + 1):
        ws_staging.cell(row=48, column=col, value=12500) # Hardcoded target as per video ($12,500)

    # Make staging sheet less visible (hide it)
    ws_staging.sheet_state = 'hidden'


    # 3. Dashboard Sheet
    ws_dashboard = wb.create_sheet("3) Dashboard", 2)
    ws_dashboard.column_dimensions['A'].width = 1
    for col_idx in range(2, 10): # Adjusting column widths for KPI cards
        ws_dashboard.column_dimensions[get_column_letter(col_idx)].width = 15

    # Main Title
    ws_dashboard.merge_cells('A1:J2') # Adjusted to cover all columns for a wider dashboard
    title_cell = ws_dashboard['A1']
    title_cell.value = title
    apply_style(title_cell, font_size=36, bold=True, fill_color=palette["header_bg"], font_color=palette["header_fg"],
                alignment=Alignment(horizontal='center', vertical='center'))
    title_cell.border = create_border()

    # Month Selector
    ws_dashboard.cell(row=4, column=1, value="For the month of")
    apply_style(ws_dashboard.cell(row=4, column=1), font_size=12, bold=True, font_color=palette["text_fg"])
    ws_dashboard.cell(row=4, column=2, value=datetime(2020, 8, 31)) # Default month: Aug-20
    ws_dashboard.cell(row=4, column=2).number_format = 'MMM-yy'
    apply_style(ws_dashboard.cell(row=4, column=2), bold=True, font_color=palette["text_fg"], border=create_border())

    # Data Validation for Month Selector (Dropdown)
    months_range_str = ','.join([f"'{ws_data.title}'!{c.coordinate}" for c in ws_data['B1:M1'][0]]) # Get cell references for months
    dv = DataValidation(type="list", formula1=f"={months_range_str}")
    ws_dashboard.add_data_validation(dv)
    dv.add('B4') # Apply to the month selection cell


    # --- KPI Card Creation Helper Function ---
    def create_kpi_card(ws, row_start, col_start, title_text, data_row_staging, target_row_staging, is_percentage=False, higher_is_better=True, font_size=36):
        # KPI Card Header
        ws.merge_cells(start_row=row_start, start_column=col_start, end_row=row_start, end_column=col_start + 2)
        header_cell = ws.cell(row=row_start, column=col_start, value=title_text)
        apply_style(header_cell, bold=True, font_size=12, fill_color=palette["accent_bg"], font_color=palette["accent_fg"], alignment=Alignment(horizontal='center', vertical='center'), border=create_border())

        # KPI Value
        kpi_cell_coord = ws.cell(row=row_start + 1, column=col_start).coordinate # Top-left cell of the merged region
        ws.merge_cells(start_row=row_start + 1, start_column=col_start, end_row=row_start + 1, end_column=col_start + 2)
        kpi_cell = ws.cell(row=row_start + 1, column=col_start)
        kpi_cell.value = f"=INDEX('2) Staging'!{data_row_staging}:{data_row_staging},MATCH($B$4,'2) Staging'!$3:$3,0))"
        kpi_cell.number_format = '0%' if is_percentage else ('$#,##0' if '$' in title_text else '#,##0') # Adjust format based on title
        apply_style(kpi_cell, font_size=font_size, bold=True, alignment=Alignment(horizontal='center', vertical='center'), border=create_border())

        # Comparison Labels
        ws.cell(row=row_start + 2, column=col_start, value="Vs. Target")
        ws.cell(row=row_start + 2, column=col_start + 1).value = "" # Spacer
        ws.cell(row=row_start + 2, column=col_start + 2, value="Vs. Prior Month")
        apply_style(ws.cell(row=row_start + 2, column=col_start), font_size=10, bold=True, alignment=Alignment(horizontal='center', vertical='center'))
        apply_style(ws.cell(row=row_start + 2, column=col_start + 2), font_size=10, bold=True, alignment=Alignment(horizontal='center', vertical='center'))


        # Target Value
        target_cell = ws.cell(row=row_start + 3, column=col_start)
        target_cell.value = f"=INDEX('2) Staging'!{target_row_staging}:{target_row_staging},MATCH($B$4,'2) Staging'!$3:$3,0))"
        target_cell.number_format = '0%' if is_percentage else ('$#,##0' if '$' in title_text else '#,##0')
        apply_style(target_cell, font_size=10, bold=False, alignment=Alignment(horizontal='center', vertical='center'), border=create_border())

        # Prior Month Value
        # Uses EOMONTH(current_month, -1) to get the date for the previous month
        prior_month_cell = ws.cell(row=row_start + 3, column=col_start + 2)
        prior_month_cell.value = f"=INDEX('2) Staging'!{data_row_staging}:{data_row_staging},MATCH(EOMONTH($B$4,-1),'2) Staging'!$3:$3,0))"
        prior_month_cell.number_format = '0%' if is_percentage else ('$#,##0' if '$' in title_text else '#,##0')
        apply_style(prior_month_cell, font_size=10, bold=False, alignment=Alignment(horizontal='center', vertical='center'), border=create_border())

        # Conditional Formatting for KPI Value (applying to the merged cell range of the KPI value)
        merged_kpi_range = f"{kpi_cell_coord}:{get_column_letter(kpi_cell.column + 2)}{kpi_cell.row}"
        
        # Determine good/bad conditions based on higher_is_better and is_percentage
        if higher_is_better: # e.g., DPO, Sales vs. Budget%, Gross Margin
            good_formula = f"AND(NOT(ISBLANK({kpi_cell_coord})), {kpi_cell_coord}>={target_cell.coordinate})"
            bad_formula = f"AND(NOT(ISBLANK({kpi_cell_coord})), {kpi_cell_coord}<{target_cell.coordinate})"
        else: # e.g., DSO, Non-Current AR %, CAC, OPEX Actual vs. Budget, CPFTE
            good_formula = f"AND(NOT(ISBLANK({kpi_cell_coord})), {kpi_cell_coord}<={target_cell.coordinate})"
            bad_formula = f"AND(NOT(ISBLANK({kpi_cell_coord})), {kpi_cell_coord}>{target_cell.coordinate})"

        ws.conditional_formatting.add(
            merged_kpi_range,
            FormulaRule(
                formula=[good_formula],
                fill=PatternFill(start_color=Color(palette["good_fill"]), end_color=Color(palette["good_fill"]), fill_type="solid"),
                font=Font(color=Color(palette["good_fg"]))
            )
        )
        ws.conditional_formatting.add(
            merged_kpi_range,
            FormulaRule(
                formula=[bad_formula],
                fill=PatternFill(start_color=Color(palette["bad_fill"]), end_color=Color(palette["bad_fill"]), fill_type="solid"),
                font=Font(color=Color(palette["bad_fg"]))
            )
        )

    # --- Working Capital Efficiency Section ---
    ws_dashboard.merge_cells('A3:J3') # Span across all 3 KPI cards (3*3 columns + 1 extra for spacing)
    section_header_wc = ws_dashboard['A3']
    section_header_wc.value = "Working Capital Efficiency"
    apply_style(section_header_wc, font_size=14, bold=True, fill_color=palette["section_bg"], font_color=palette["section_fg"], alignment=Alignment(horizontal='center', vertical='center'))
    section_header_wc.border = create_border()

    # DSO KPI
    create_kpi_card(ws_dashboard, row_start=5, col_start=2, title_text="DSO (Days Sales Outstanding)",
                    data_row_staging=7, target_row_staging=8, higher_is_better=False, font_size=36)
    # DPO KPI
    create_kpi_card(ws_dashboard, row_start=5, col_start=5, title_text="DPO (Days Payables Outstanding)",
                    data_row_staging=13, target_row_staging=14, higher_is_better=True, font_size=36)
    # Non-Current AR % KPI
    create_kpi_card(ws_dashboard, row_start=5, col_start=8, title_text="Non-Current AR %",
                    data_row_staging=18, target_row_staging=19, is_percentage=True, higher_is_better=False, font_size=36)


    # --- Sales KPIs Section ---
    ws_dashboard.merge_cells('A10:J10')
    section_header_sales = ws_dashboard['A10']
    section_header_sales.value = "Sales KPIs"
    apply_style(section_header_sales, font_size=14, bold=True, fill_color=palette["section_bg"], font_color=palette["section_fg"], alignment=Alignment(horizontal='center', vertical='center'))
    section_header_sales.border = create_border()

    # CAC (Customer Acquisition Cost) KPI
    create_kpi_card(ws_dashboard, row_start=12, col_start=2, title_text="CAC (Customer Acquisition Cost)",
                    data_row_staging=25, target_row_staging=26, higher_is_better=False, font_size=36)
    # Sales vs. Budget% KPI
    create_kpi_card(ws_dashboard, row_start=12, col_start=5, title_text="Sales vs. Budget%",
                    data_row_staging=30, target_row_staging=31, is_percentage=True, higher_is_better=True, font_size=36)
    # Gross Margin KPI
    create_kpi_card(ws_dashboard, row_start=12, col_start=8, title_text="Gross Margin",
                    data_row_staging=35, target_row_staging=36, is_percentage=True, higher_is_better=True, font_size=36)

    # --- Cost KPIs Section ---
    ws_dashboard.merge_cells('A17:J17')
    section_header_cost = ws_dashboard['A17']
    section_header_cost.value = "Cost KPIs"
    apply_style(section_header_cost, font_size=14, bold=True, fill_color=palette["section_bg"], font_color=palette["section_fg"], alignment=Alignment(horizontal='center', vertical='center'))
    section_header_cost.border = create_border()

    # OPEX Actual vs. Budget KPI
    create_kpi_card(ws_dashboard, row_start=19, col_start=2, title_text="OPEX Actual vs. Budget",
                    data_row_staging=42, target_row_staging=43, is_percentage=True, higher_is_better=False, font_size=36)
    # CPFTE (Cost Per Full Time Employee) KPI
    create_kpi_card(ws_dashboard, row_start=19, col_start=5, title_text="CPFTE (Cost Per Full Time Employee)",
                    data_row_staging=47, target_row_staging=48, higher_is_better=False, font_size=36)
    
    # Hide the data and staging sheets for cleaner dashboard view
    ws_data.sheet_state = 'hidden'
    ws_staging.sheet_state = 'hidden'

    # Set Dashboard as active sheet
    wb.active = ws_dashboard
