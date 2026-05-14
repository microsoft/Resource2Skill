import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.utils import get_column_letter

# Mock _helpers for demonstration - in a real skill, these would be imported from _helpers.py
class ThemePalette:
    def __init__(self, theme_name):
        self.header_bg = "003366"  # Dark blue
        self.header_fg = "FFFFFF"  # White
        self.text_color = "000000"  # Black
        self.input_color = "0000FF" # Blue
        self.accent_color_1 = "0000FF" # For Accessories line (blue)
        self.accent_color_2 = "FFA500" # For Devices line (orange)
        self.accent_color_3 = "008000" # For Contribution Margin line (green)
        self.grid_color = "CCCCCC" # Light gray
        self.positive_color = "008000" # Green for match
        self.negative_color = "FF0000" # Red for mismatch

def get_font(color=None, bold=False, italic=False, size=None):
    return Font(color=color, bold=bold, italic=italic, size=size)

def get_fill(color):
    return PatternFill(start_color=color, end_color=color, fill_type="solid")

def get_border(style="thin", color="000000"):
    return Border(left=Side(border_style=style, color=color),
                  right=Side(border_style=style, color=color),
                  top=Side(border_style=style, color=color),
                  bottom=Side(border_style=style, color=color))

def render_workbook(wb, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    # Load theme colors (simplified for this example)
    palette = ThemePalette(theme)

    # --- Assumptions Tab ---
    ws_assumptions = wb.create_sheet("Assumptions")
    ws_assumptions.title = "Assumptions"

    # Set up basic structure and headers
    ws_assumptions.merge_cells('A1:B1')
    ws_assumptions['A1'] = "E-Commerce Scenario Planning Model -- Assumptions"
    ws_assumptions['A1'].font = get_font(bold=True, color=palette.header_fg)
    ws_assumptions['A1'].fill = get_fill(palette.header_bg)

    # Accessories
    ws_assumptions['A3'] = "ACCESSORIES"
    ws_assumptions['A3'].font = get_font(bold=True)
    ws_assumptions['A4'] = "Average Order Value ($)"
    ws_assumptions['B4'] = 45
    ws_assumptions['B4'].font = get_font(color=palette.input_color)
    ws_assumptions['A5'] = "Starting Monthly Orders"
    ws_assumptions['B5'] = 2000
    ws_assumptions['B5'].font = get_font(color=palette.input_color)
    ws_assumptions['A6'] = "Monthly Order Growth Rate"
    ws_assumptions['B6'] = 0.06
    ws_assumptions['B6'].font = get_font(color=palette.input_color)
    ws_assumptions['B6'].number_format = '0.0%'
    ws_assumptions['A7'] = "Gross Margin (%)"
    ws_assumptions['B7'] = 0.35
    ws_assumptions['B7'].font = get_font(color=palette.input_color)
    ws_assumptions['B7'].number_format = '0.0%'
    ws_assumptions['A8'] = "Product Line"
    ws_assumptions['B8'] = "Accessories"

    # Devices
    ws_assumptions['A10'] = "DEVICES"
    ws_assumptions['A10'].font = get_font(bold=True)
    ws_assumptions['A11'] = "Average Order Value ($)"
    ws_assumptions['B11'] = 280
    ws_assumptions['B11'].font = get_font(color=palette.input_color)
    ws_assumptions['A12'] = "Starting Monthly Orders"
    ws_assumptions['B12'] = 500
    ws_assumptions['B12'].font = get_font(color=palette.input_color)
    ws_assumptions['A13'] = "Monthly Order Growth Rate"
    ws_assumptions['B13'] = 0.04
    ws_assumptions['B13'].font = get_font(color=palette.input_color)
    ws_assumptions['B13'].number_format = '0.0%'
    ws_assumptions['A14'] = "Gross Margin (%)"
    ws_assumptions['B14'] = 0.22
    ws_assumptions['B14'].font = get_font(color=palette.input_color)
    ws_assumptions['B14'].number_format = '0.0%'
    ws_assumptions['A15'] = "Product Line"
    ws_assumptions['B15'] = "Devices"

    # General Assumptions
    ws_assumptions['A17'] = "GENERAL"
    ws_assumptions['A17'].font = get_font(bold=True)
    ws_assumptions['A18'] = "Forward Forecast (Months)"
    ws_assumptions['B18'] = 24
    ws_assumptions['B18'].font = get_font(color=palette.input_color)
    ws_assumptions['A19'] = "Model Start Date (Month)"
    ws_assumptions['B19'] = 1 # Assuming start from Month 1
    ws_assumptions['B19'].font = get_font(color=palette.input_color)
    
    # Marketing Spend (Enhanced part from video)
    ws_assumptions['A20'] = "Marketing Spend (% of Total Revenue)"
    ws_assumptions['B20'] = 0.12 # 12% as per prompt
    ws_assumptions['B20'].font = get_font(color=palette.input_color)
    ws_assumptions['B20'].number_format = '0.0%'

    ws_assumptions['A22'] = "Blue values are editable inputs. Change any assumption to update the Model tab automatically."
    ws_assumptions['A22'].font = get_font(italic=True, size=9)
    ws_assumptions.column_dimensions['A'].width = 35
    ws_assumptions.column_dimensions['B'].width = 15

    # --- Model Tab ---
    ws_model = wb.create_sheet("Model")
    ws_model.title = "E-Commerce Scenario Planning Model -- 24-Month Forecast" # Naming from video

    ws_model.merge_cells('A1:B1')
    ws_model['A1'] = "E-Commerce Scenario Planning Model -- 24-Month Forecast"
    ws_model['A1'].font = get_font(bold=True, color=palette.header_fg)
    ws_model['A1'].fill = get_fill(palette.header_bg)

    # Months header
    for col_idx in range(1, ws_assumptions['B18'].value + 1):
        ws_model.cell(row=3, column=col_idx + 1, value=f"Month {col_idx}").font = get_font(bold=True)
        ws_model.column_dimensions[get_column_letter(col_idx + 1)].width = 15

    # Accessories section
    current_row = 5
    ws_model.merge_cells(start_row=current_row - 1, start_column=1, end_row=current_row - 1, end_column=2)
    ws_model.cell(row=current_row - 1, column=1, value="ACCESSORIES").font = get_font(bold=True)
    
    ws_model.cell(row=current_row, column=1, value="Avg Order Value ($)")
    ws_model.cell(row=current_row + 1, column=1, value="Orders")
    ws_model.cell(row=current_row + 2, column=1, value="Revenue ($)")
    ws_model.cell(row=current_row + 3, column=1, value="Gross Margin %")
    ws_model.cell(row=current_row + 4, column=1, value="Gross Profit ($)")

    # Formulas for Accessories
    for col_idx in range(1, ws_assumptions['B18'].value + 1):
        month_col = get_column_letter(col_idx + 1)
        # Avg Order Value
        ws_model.cell(row=current_row, column=col_idx + 1, value=f"=Assumptions!$B$4").number_format = '$#,##0'
        # Orders
        if col_idx == 1:
            ws_model.cell(row=current_row + 1, column=col_idx + 1, value=f"=Assumptions!$B$5").number_format = '#,##0'
        else:
            prev_month_col = get_column_letter(col_idx)
            ws_model.cell(row=current_row + 1, column=col_idx + 1, value=f"={prev_month_col}{current_row+1}*(1+Assumptions!$B$6)").number_format = '#,##0'
        # Revenue
        ws_model.cell(row=current_row + 2, column=col_idx + 1, value=f"={month_col}{current_row}*{month_col}{current_row+1}").number_format = '$#,##0'
        # Gross Margin %
        ws_model.cell(row=current_row + 3, column=col_idx + 1, value=f"=Assumptions!$B$7").number_format = '0.0%'
        # Gross Profit
        ws_model.cell(row=current_row + 4, column=col_idx + 1, value=f"={month_col}{current_row+2}*{month_col}{current_row+3}").number_format = '$#,##0'

    current_row += 7 # Move down for next section

    # Devices section
    ws_model.merge_cells(start_row=current_row - 1, start_column=1, end_row=current_row - 1, end_column=2)
    ws_model.cell(row=current_row - 1, column=1, value="DEVICES").font = get_font(bold=True)

    ws_model.cell(row=current_row, column=1, value="Avg Order Value ($)")
    ws_model.cell(row=current_row + 1, column=1, value="Orders")
    ws_model.cell(row=current_row + 2, column=1, value="Revenue ($)")
    ws_model.cell(row=current_row + 3, column=1, value="Gross Margin %")
    ws_model.cell(row=current_row + 4, column=1, value="Gross Profit ($)")

    # Formulas for Devices
    for col_idx in range(1, ws_assumptions['B18'].value + 1):
        month_col = get_column_letter(col_idx + 1)
        # Avg Order Value
        ws_model.cell(row=current_row, column=col_idx + 1, value=f"=Assumptions!$B$11").number_format = '$#,##0'
        # Orders
        if col_idx == 1:
            ws_model.cell(row=current_row + 1, column=col_idx + 1, value=f"=Assumptions!$B$12").number_format = '#,##0'
        else:
            prev_month_col = get_column_letter(col_idx)
            ws_model.cell(row=current_row + 1, column=col_idx + 1, value=f"={prev_month_col}{current_row+1}*(1+Assumptions!$B$13)").number_format = '#,##0'
        # Revenue
        ws_model.cell(row=current_row + 2, column=col_idx + 1, value=f"={month_col}{current_row}*{month_col}{current_row+1}").number_format = '$#,##0'
        # Gross Margin %
        ws_model.cell(row=current_row + 3, column=col_idx + 1, value=f"=Assumptions!$B$14").number_format = '0.0%'
        # Gross Profit
        ws_model.cell(row=current_row + 4, column=col_idx + 1, value=f"={month_col}{current_row+2}*{month_col}{current_row+3}").number_format = '$#,##0'

    current_row += 7 # Move down for combined totals and sanity check

    # Combined Totals section
    ws_model.merge_cells(start_row=current_row - 1, start_column=1, end_row=current_row - 1, end_column=2)
    ws_model.cell(row=current_row - 1, column=1, value="COMBINED TOTALS").font = get_font(bold=True)

    ws_model.cell(row=current_row, column=1, value="Total Revenue ($)")
    ws_model.cell(row=current_row + 1, column=1, value="Total Gross Profit ($)")
    ws_model.cell(row=current_row + 2, column=1, value="Blended Gross Margin (%)")
    ws_model.cell(row=current_row + 3, column=1, value="Marketing Spend (% of Rev)") # Enhanced
    ws_model.cell(row=current_row + 4, column=1, value="Marketing Spend ($)") # Enhanced
    ws_model.cell(row=current_row + 5, column=1, value="Contribution Margin ($)") # Enhanced

    # Formulas for Combined Totals (and enhanced metrics)
    accessories_revenue_row = 7 # Accessories Revenue is at row 7
    devices_revenue_row = 14 # Devices Revenue is at row 14
    accessories_grossprofit_row = 9 # Accessories Gross Profit is at row 9
    devices_grossprofit_row = 16 # Devices Gross Profit is at row 16

    for col_idx in range(1, ws_assumptions['B18'].value + 1):
        month_col = get_column_letter(col_idx + 1)
        # Total Revenue
        ws_model.cell(row=current_row, column=col_idx + 1, value=f"={month_col}{accessories_revenue_row}+{month_col}{devices_revenue_row}").number_format = '$#,##0'
        # Total Gross Profit
        ws_model.cell(row=current_row + 1, column=col_idx + 1, value=f"={month_col}{accessories_grossprofit_row}+{month_col}{devices_grossprofit_row}").number_format = '$#,##0'
        # Blended Gross Margin %
        ws_model.cell(row=current_row + 2, column=col_idx + 1, value=f"={month_col}{current_row+1}/{month_col}{current_row}").number_format = '0.0%'
        # Marketing Spend (% of Rev) - Enhanced
        ws_model.cell(row=current_row + 3, column=col_idx + 1, value=f"=Assumptions!$B$20").number_format = '0.0%'
        # Marketing Spend ($) - Enhanced
        ws_model.cell(row=current_row + 4, column=col_idx + 1, value=f"={month_col}{current_row}*{month_col}{current_row+3}").number_format = '$#,##0'
        # Contribution Margin ($) - Enhanced
        ws_model.cell(row=current_row + 5, column=col_idx + 1, value=f"={month_col}{current_row+1}-{month_col}{current_row+4}").number_format = '$#,##0'

    current_row += 8 # Move down for sanity check

    # Sanity Check section
    ws_model.merge_cells(start_row=current_row - 1, start_column=1, end_row=current_row - 1, end_column=2)
    ws_model.cell(row=current_row - 1, column=1, value="SANITY CHECK").font = get_font(bold=True)

    ws_model.cell(row=current_row, column=1, value="Accessories Rev + Devices Rev ($)")
    ws_model.cell(row=current_row + 1, column=1, value="Matches Total Revenue?")

    for col_idx in range(1, ws_assumptions['B18'].value + 1):
        month_col = get_column_letter(col_idx + 1)
        # Sum of individual revenues
        ws_model.cell(row=current_row, column=col_idx + 1, value=f"={month_col}{accessories_revenue_row}+{month_col}{devices_revenue_row}").number_format = '$#,##0'
        # Total Revenue for comparison is 8 rows above the sanity check row for Total Revenue
        total_revenue_comp_row = current_row - 8 
        # Match check
        ws_model.cell(row=current_row + 1, column=col_idx + 1, value=f'=IF({month_col}{current_row}={month_col}{total_revenue_comp_row},\"Match\",\"Mismatch\")')
        # Add conditional formatting rules for "Match" / "Mismatch"
        from openpyxl.formatting.rule import FormulaRule
        from openpyxl.styles import PatternFill
        ws_model.conditional_formatting.add(f'{month_col}{current_row+1}',
                                            FormulaRule(formula=[f'{month_col}{current_row+1}=\"Match\"'],
                                                        fill=PatternFill(start_color=palette.positive_color, end_color=palette.positive_color, fill_type="solid")))
        ws_model.conditional_formatting.add(f'{month_col}{current_row+1}',
                                            FormulaRule(formula=[f'{month_col}{current_row+1}=\"Mismatch\"'],
                                                        fill=PatternFill(start_color=palette.negative_color, end_color=palette.negative_color, fill_type="solid")))


    chart_data_start_row = current_row + 4 # Start data for chart below sanity check

    # Prepare Chart Data (these cells are used as source for the chart)
    # The chart data is placed below the main table for clarity, referencing the calculated rows.
    ws_model.cell(row=chart_data_start_row, column=1, value="Accessories Revenue").font = get_font(bold=True)
    ws_model.cell(row=chart_data_start_row + 1, column=1, value="Devices Revenue").font = get_font(bold=True)
    ws_model.cell(row=chart_data_start_row + 2, column=1, value="Contribution Margin").font = get_font(bold=True) # Enhanced

    combined_totals_revenue_row = current_row - 8
    combined_totals_contribution_margin_row = current_row - 8 + 5 # Contribution Margin is 5 rows below Total Revenue in Combined Totals

    for col_idx in range(1, ws_assumptions['B18'].value + 1):
        month_col = get_column_letter(col_idx + 1)
        ws_model.cell(row=chart_data_start_row, column=col_idx + 1, value=f"={month_col}{accessories_revenue_row}").number_format = '$#,##0'
        ws_model.cell(row=chart_data_start_row + 1, column=col_idx + 1, value=f"={month_col}{devices_revenue_row}").number_format = '$#,##0'
        ws_model.cell(row=chart_data_start_row + 2, column=col_idx + 1, value=f"={month_col}{combined_totals_contribution_margin_row}").number_format = '$#,##0'

    # Add the chart
    chart = LineChart()
    chart.title = "Monthly Revenue & Contribution Margin By Product Line"
    chart.style = 10 # A reasonable default style
    chart.y_axis.title = "Amount ($)"
    chart.x_axis.title = "Month"

    # Data for the chart
    # First row is labels for series
    labels_row = chart_data_start_row -1
    for col_idx in range(1, ws_assumptions['B18'].value + 1):
        ws_model.cell(row=labels_row, column=col_idx+1, value=f"Month {col_idx}") # Add month labels above data for chart categories

    # Data series for chart
    # Data is from chart_data_start_row onwards
    accessories_series_data = Reference(ws_model, min_col=2, min_row=chart_data_start_row, max_col=ws_assumptions['B18'].value + 1)
    devices_series_data = Reference(ws_model, min_col=2, min_row=chart_data_start_row + 1, max_col=ws_assumptions['B18'].value + 1)
    contribution_series_data = Reference(ws_model, min_col=2, min_row=chart_data_start_row + 2, max_col=ws_assumptions['B18'].value + 1)

    # Categories (Months) for the chart
    categories = Reference(ws_model, min_col=2, min_row=labels_row, max_col=ws_assumptions['B18'].value + 1)

    # Add series with custom titles and colors
    s1 = chart.series.append(accessories_series_data)
    s1.tx.v = "Accessories Revenue"
    s1.graphicalProperties.line.solidFill = palette.accent_color_1

    s2 = chart.series.append(devices_series_data)
    s2.tx.v = "Devices Revenue"
    s2.graphicalProperties.line.solidFill = palette.accent_color_2

    s3 = chart.series.append(contribution_series_data)
    s3.tx.v = "Contribution Margin"
    s3.graphicalProperties.line.solidFill = palette.accent_color_3

    chart.set_categories(categories)

    # Place the chart below the data
    ws_model.add_chart(chart, f"B{chart_data_start_row + 5}") # Offset to place chart visually below data.

    # Set column width for the labels on Model tab
    ws_model.column_dimensions['A'].width = 30

    # Ensure Assumptions sheet is the first one
    wb.active = 0
