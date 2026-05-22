from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, Reference
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles.colors import Color
import openpyxl.utils

def render_workbook(wb: Workbook, *, title: str = "E-Commerce Scenario Planning Model", theme: str = "corporate_blue", **kwargs) -> None:
    # Remove default sheet
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])

    # Define colors (could be theme-driven, but hardcoding for self-contained example)
    HEADER_BG_COLOR = "ADD8E6" # Light Blue
    INPUT_CELL_BG_COLOR = "E0EBF7" # Lighter Blue Grey for input background
    INPUT_CELL_FONT_COLOR = "0000FF" # Blue font for input values
    MATCH_COLOR = "C6EFCE" # Light Green
    MISMATCH_COLOR = "FFC7CE" # Light Red

    # --- Assumptions Sheet ---
    ws_assumptions = wb.create_sheet("Assumptions", 0)
    ws_assumptions.title = "Assumptions"

    # Title
    ws_assumptions["A1"] = f"{title} - Assumptions"
    ws_assumptions["A1"].font = Font(bold=True, size=14)

    # Headers and Data for Accessories
    ws_assumptions["A3"] = "ACCESSORIES"
    ws_assumptions["A3"].font = Font(bold=True)
    assumptions_acc = {
        "Average Order Value ($)": 45,
        "Starting Monthly Orders": 2000,
        "Monthly Order Growth Rate": 0.06, # 6%
        "Gross Margin (%)": 0.35, # 35%
        "Product Line": "Accessories"
    }
    row = 4
    for label, value in assumptions_acc.items():
        ws_assumptions[f"A{row}"] = label
        cell_b = ws_assumptions[f"B{row}"]
        cell_b.value = value
        cell_b.fill = PatternFill(start_color=INPUT_CELL_BG_COLOR, end_color=INPUT_CELL_BG_COLOR, fill_type="solid")
        cell_b.font = Font(color=Color(INPUT_CELL_FONT_COLOR))
        if isinstance(value, float):
            cell_b.number_format = "0.0%" if "Margin" in label or "Rate" in label else "$#,##0.00"
        elif isinstance(value, int):
            cell_b.number_format = "#,##0"
        row += 1

    # Headers and Data for Devices
    ws_assumptions[f"A{row+1}"] = "DEVICES"
    ws_assumptions[f"A{row+1}"].font = Font(bold=True)
    row += 2
    assumptions_dev = {
        "Average Order Value ($)": 280,
        "Starting Monthly Orders": 500,
        "Monthly Order Growth Rate": 0.04, # 4%
        "Gross Margin (%)": 0.22, # 22%
        "Product Line": "Devices"
    }
    for label, value in assumptions_dev.items():
        ws_assumptions[f"A{row}"] = label
        cell_b = ws_assumptions[f"B{row}"]
        cell_b.value = value
        cell_b.fill = PatternFill(start_color=INPUT_CELL_BG_COLOR, end_color=INPUT_CELL_BG_COLOR, fill_type="solid")
        cell_b.font = Font(color=Color(INPUT_CELL_FONT_COLOR))
        if isinstance(value, float):
            cell_b.number_format = "0.0%" if "Margin" in label or "Rate" in label else "$#,##0.00"
        elif isinstance(value, int):
            cell_b.number_format = "#,##0"
        row += 1

    # Headers and Data for General
    ws_assumptions[f"A{row+1}"] = "GENERAL"
    ws_assumptions[f"A{row+1}"].font = Font(bold=True)
    row += 2
    assumptions_gen = {
        "Forward Forecast (Months)": 24,
        "Model Start Date (Month)": 1,
        "Marketing Spend (% of Total Revenue)": 0.12 # 12%
    }
    for label, value in assumptions_gen.items():
        ws_assumptions[f"A{row}"] = label
        cell_b = ws_assumptions[f"B{row}"]
        cell_b.value = value
        cell_b.fill = PatternFill(start_color=INPUT_CELL_BG_COLOR, end_color=INPUT_CELL_BG_COLOR, fill_type="solid")
        cell_b.font = Font(color=Color(INPUT_CELL_FONT_COLOR))
        if isinstance(value, float):
            cell_b.number_format = "0.0%" if "Spend" in label else "#,##0"
        elif isinstance(value, int):
            cell_b.number_format = "#,##0"
        row += 1

    # Set column widths for assumptions tab
    ws_assumptions.column_dimensions['A'].width = 30
    ws_assumptions.column_dimensions['B'].width = 15

    # --- Model Sheet ---
    ws_model = wb.create_sheet("Model")
    ws_model.title = "Model"

    # Title
    ws_model["A1"] = f"{title} - 24-Month Forecast"
    ws_model["A1"].font = Font(bold=True, size=14)

    # Month Headers
    num_months = ws_assumptions["B18"].value
    for col in range(num_months):
        col_letter = openpyxl.utils.get_column_letter(col + 2)
        ws_model[f"{col_letter}3"] = f"Month {col+1}"
        ws_model[f"{col_letter}3"].font = Font(bold=True)
        ws_model[f"{col_letter}3"].alignment = Alignment(horizontal='center')
        ws_model.column_dimensions[col_letter].width = 15 # Set width for monthly columns
    ws_model.column_dimensions['A'].width = 30 # Adjust A column width

    # Row mappings for easier formula generation
    ROW_MAP = {
        "ACC_ORDERS": 6, "ACC_AVG_ORDER_VALUE": 7, "ACC_REVENUE": 8, "ACC_GROSS_MARGIN_PCT": 9, "ACC_GROSS_PROFIT": 10,
        "DEV_ORDERS": 13, "DEV_AVG_ORDER_VALUE": 14, "DEV_REVENUE": 15, "DEV_GROSS_MARGIN_PCT": 16, "DEV_GROSS_PROFIT": 17,
        "TOTAL_REVENUE": 20, "TOTAL_GROSS_PROFIT": 21, "BLEND_GROSS_MARGIN_PCT": 22, "MARKETING_SPEND_PCT": 23, "MARKETING_SPEND_DOL": 24, "CONTRIBUTION_MARGIN": 25,
        "SC_ACC_DEV_REV": 28, "SC_MATCH_TOTAL_REV": 29,
        "CHART_ACC_REV": 32, "CHART_DEV_REV": 33, "CHART_CONTRIB_MARGIN": 34
    }

    # ACCESSORIES Section Headers
    ws_model.cell(row=ROW_MAP["ACC_ORDERS"]-1, column=1, value="ACCESSORIES").font = Font(bold=True)
    ws_model.cell(row=ROW_MAP["ACC_ORDERS"], column=1, value="Orders")
    ws_model.cell(row=ROW_MAP["ACC_AVG_ORDER_VALUE"], column=1, value="Avg Order Value ($)")
    ws_model.cell(row=ROW_MAP["ACC_REVENUE"], column=1, value="Revenue ($)")
    ws_model.cell(row=ROW_MAP["ACC_GROSS_MARGIN_PCT"], column=1, value="Gross Margin (%)")
    ws_model.cell(row=ROW_MAP["ACC_GROSS_PROFIT"], column=1, value="Gross Profit ($)")

    # DEVICES Section Headers
    ws_model.cell(row=ROW_MAP["DEV_ORDERS"]-1, column=1, value="DEVICES").font = Font(bold=True)
    ws_model.cell(row=ROW_MAP["DEV_ORDERS"], column=1, value="Orders")
    ws_model.cell(row=ROW_MAP["DEV_AVG_ORDER_VALUE"], column=1, value="Avg Order Value ($)")
    ws_model.cell(row=ROW_MAP["DEV_REVENUE"], column=1, value="Revenue ($)")
    ws_model.cell(row=ROW_MAP["DEV_GROSS_MARGIN_PCT"], column=1, value="Gross Margin (%)")
    ws_model.cell(row=ROW_MAP["DEV_GROSS_PROFIT"], column=1, value="Gross Profit ($)")

    # COMBINED TOTALS Section Headers
    ws_model.cell(row=ROW_MAP["TOTAL_REVENUE"]-1, column=1, value="COMBINED TOTALS").font = Font(bold=True)
    ws_model.cell(row=ROW_MAP["TOTAL_REVENUE"], column=1, value="Total Revenue ($)")
    ws_model.cell(row=ROW_MAP["TOTAL_GROSS_PROFIT"], column=1, value="Total Gross Profit ($)")
    ws_model.cell(row=ROW_MAP["BLEND_GROSS_MARGIN_PCT"], column=1, value="Blended Gross Margin (%)")
    ws_model.cell(row=ROW_MAP["MARKETING_SPEND_PCT"], column=1, value="Marketing Spend (% of Rev)")
    ws_model.cell(row=ROW_MAP["MARKETING_SPEND_DOL"], column=1, value="Marketing Spend ($)")
    ws_model.cell(row=ROW_MAP["CONTRIBUTION_MARGIN"], column=1, value="Contribution Margin ($)")

    # SANITY CHECK Section Headers
    ws_model.cell(row=ROW_MAP["SC_ACC_DEV_REV"]-1, column=1, value="SANITY CHECK").font = Font(bold=True)
    ws_model.cell(row=ROW_MAP["SC_ACC_DEV_REV"], column=1, value="Accessories Rev + Devices Rev ($)")
    ws_model.cell(row=ROW_MAP["SC_MATCH_TOTAL_REV"], column=1, value="Matches Total Revenue?")

    # Populate Model with Formulas
    for month_col in range(num_months):
        col_idx = month_col + 2 # B column is 2, C is 3, etc.
        col_letter = openpyxl.utils.get_column_letter(col_idx)

        # ACCESSORIES
        # Orders
        if month_col == 0:
            ws_model[f"{col_letter}{ROW_MAP['ACC_ORDERS']}"] = "=Assumptions!B5"
        else:
            prev_col_letter = openpyxl.utils.get_column_letter(col_idx-1)
            ws_model[f"{col_letter}{ROW_MAP['ACC_ORDERS']}"] = f"={prev_col_letter}{ROW_MAP['ACC_ORDERS']}*(1+Assumptions!B6)"
        ws_model[f"{col_letter}{ROW_MAP['ACC_ORDERS']}"].number_format = "#,##0"

        # Avg Order Value ($)
        ws_model[f"{col_letter}{ROW_MAP['ACC_AVG_ORDER_VALUE']}"] = "=Assumptions!B4"
        ws_model[f"{col_letter}{ROW_MAP['ACC_AVG_ORDER_VALUE']}"].number_format = "$#,##0.00"

        # Revenue ($)
        ws_model[f"{col_letter}{ROW_MAP['ACC_REVENUE']}"] = f"={col_letter}{ROW_MAP['ACC_ORDERS']}*{col_letter}{ROW_MAP['ACC_AVG_ORDER_VALUE']}"
        ws_model[f"{col_letter}{ROW_MAP['ACC_REVENUE']}"].number_format = "$#,##0"

        # Gross Margin (%)
        ws_model[f"{col_letter}{ROW_MAP['ACC_GROSS_MARGIN_PCT']}"] = "=Assumptions!B7"
        ws_model[f"{col_letter}{ROW_MAP['ACC_GROSS_MARGIN_PCT']}"].number_format = "0.0%"

        # Gross Profit ($)
        ws_model[f"{col_letter}{ROW_MAP['ACC_GROSS_PROFIT']}"] = f"={col_letter}{ROW_MAP['ACC_REVENUE']}*{col_letter}{ROW_MAP['ACC_GROSS_MARGIN_PCT']}"
        ws_model[f"{col_letter}{ROW_MAP['ACC_GROSS_PROFIT']}"].number_format = "$#,##0"

        # DEVICES
        # Orders
        if month_col == 0:
            ws_model[f"{col_letter}{ROW_MAP['DEV_ORDERS']}"] = "=Assumptions!B12"
        else:
            prev_col_letter = openpyxl.utils.get_column_letter(col_idx-1)
            ws_model[f"{col_letter}{ROW_MAP['DEV_ORDERS']}"] = f"={prev_col_letter}{ROW_MAP['DEV_ORDERS']}*(1+Assumptions!B13)"
        ws_model[f"{col_letter}{ROW_MAP['DEV_ORDERS']}"].number_format = "#,##0"

        # Avg Order Value ($)
        ws_model[f"{col_letter}{ROW_MAP['DEV_AVG_ORDER_VALUE']}"] = "=Assumptions!B11"
        ws_model[f"{col_letter}{ROW_MAP['DEV_AVG_ORDER_VALUE']}"].number_format = "$#,##0.00"

        # Revenue ($)
        ws_model[f"{col_letter}{ROW_MAP['DEV_REVENUE']}"] = f"={col_letter}{ROW_MAP['DEV_ORDERS']}*{col_letter}{ROW_MAP['DEV_AVG_ORDER_VALUE']}"
        ws_model[f"{col_letter}{ROW_MAP['DEV_REVENUE']}"].number_format = "$#,##0"

        # Gross Margin (%)
        ws_model[f"{col_letter}{ROW_MAP['DEV_GROSS_MARGIN_PCT']}"] = "=Assumptions!B14"
        ws_model[f"{col_letter}{ROW_MAP['DEV_GROSS_MARGIN_PCT']}"].number_format = "0.0%"

        # Gross Profit ($)
        ws_model[f"{col_letter}{ROW_MAP['DEV_GROSS_PROFIT']}"] = f"={col_letter}{ROW_MAP['DEV_REVENUE']}*{col_letter}{ROW_MAP['DEV_GROSS_MARGIN_PCT']}"
        ws_model[f"{col_letter}{ROW_MAP['DEV_GROSS_PROFIT']}"].number_format = "$#,##0"

        # COMBINED TOTALS
        # Total Revenue ($)
        ws_model[f"{col_letter}{ROW_MAP['TOTAL_REVENUE']}"] = f"={col_letter}{ROW_MAP['ACC_REVENUE']}+{col_letter}{ROW_MAP['DEV_REVENUE']}"
        ws_model[f"{col_letter}{ROW_MAP['TOTAL_REVENUE']}"].number_format = "$#,##0"

        # Total Gross Profit ($)
        ws_model[f"{col_letter}{ROW_MAP['TOTAL_GROSS_PROFIT']}"] = f"={col_letter}{ROW_MAP['ACC_GROSS_PROFIT']}+{col_letter}{ROW_MAP['DEV_GROSS_PROFIT']}"
        ws_model[f"{col_letter}{ROW_MAP['TOTAL_GROSS_PROFIT']}"].number_format = "$#,##0"

        # Blended Gross Margin (%)
        ws_model[f"{col_letter}{ROW_MAP['BLEND_GROSS_MARGIN_PCT']}"] = f"={col_letter}{ROW_MAP['TOTAL_GROSS_PROFIT']}/{col_letter}{ROW_MAP['TOTAL_REVENUE']}"
        ws_model[f"{col_letter}{ROW_MAP['BLEND_GROSS_MARGIN_PCT']}"].number_format = "0.0%"

        # Marketing Spend (% of Rev)
        ws_model[f"{col_letter}{ROW_MAP['MARKETING_SPEND_PCT']}"] = "=Assumptions!B20"
        ws_model[f"{col_letter}{ROW_MAP['MARKETING_SPEND_PCT']}"].number_format = "0.0%"

        # Marketing Spend ($)
        ws_model[f"{col_letter}{ROW_MAP['MARKETING_SPEND_DOL']}"] = f"={col_letter}{ROW_MAP['TOTAL_REVENUE']}*{col_letter}{ROW_MAP['MARKETING_SPEND_PCT']}"
        ws_model[f"{col_letter}{ROW_MAP['MARKETING_SPEND_DOL']}"].number_format = "$#,##0"

        # Contribution Margin ($)
        ws_model[f"{col_letter}{ROW_MAP['CONTRIBUTION_MARGIN']}"] = f"={col_letter}{ROW_MAP['TOTAL_GROSS_PROFIT']}-{col_letter}{ROW_MAP['MARKETING_SPEND_DOL']}"
        ws_model[f"{col_letter}{ROW_MAP['CONTRIBUTION_MARGIN']}"].number_format = "$#,##0"

        # SANITY CHECK
        ws_model[f"{col_letter}{ROW_MAP['SC_ACC_DEV_REV']}"] = f"={col_letter}{ROW_MAP['ACC_REVENUE']}+{col_letter}{ROW_MAP['DEV_REVENUE']}"
        ws_model[f"{col_letter}{ROW_MAP['SC_ACC_DEV_REV']}"].number_format = "$#,##0"

        ws_model[f"{col_letter}{ROW_MAP['SC_MATCH_TOTAL_REV']}"] = f'=IF({col_letter}{ROW_MAP["SC_ACC_DEV_REV"]}={col_letter}{ROW_MAP["TOTAL_REVENUE"]},"Match","Mismatch")'
        ws_model[f"{col_letter}{ROW_MAP['SC_MATCH_TOTAL_REV']}"].font = Font(bold=True)

    # Apply conditional formatting for Sanity Check
    sanity_check_range = f"B{ROW_MAP['SC_MATCH_TOTAL_REV']}:{openpyxl.utils.get_column_letter(1 + num_months)}{ROW_MAP['SC_MATCH_TOTAL_REV']}"
    ws_model.conditional_formatting.add(
        sanity_check_range,
        CellIsRule(operator='equal', formula=['"Match"'], fill=PatternFill(start_color=MATCH_COLOR, end_color=MATCH_COLOR, fill_type="solid"))
    )
    ws_model.conditional_formatting.add(
        sanity_check_range,
        CellIsRule(operator='equal', formula=['"Mismatch"'], fill=PatternFill(start_color=MISMATCH_COLOR, end_color=MISMATCH_COLOR, fill_type="solid"))
    )

    # Prepare data for chart below
    chart_title_row = ROW_MAP["SC_MATCH_TOTAL_REV"] + 3
    ws_model.cell(row=chart_title_row, column=1, value="Monthly Revenue & Contribution Margin by Product Line").font = Font(bold=True)

    chart_data_start_row = chart_title_row + 1
    ws_model.cell(row=chart_data_start_row, column=1, value="Accessories Revenue")
    ws_model.cell(row=chart_data_start_row + 1, column=1, value="Devices Revenue")
    ws_model.cell(row=chart_data_start_row + 2, column=1, value="Contribution Margin")

    # Link chart data to model calculations
    for month_col in range(num_months):
        col_idx = month_col + 2
        col_letter = openpyxl.utils.get_column_letter(col_idx)
        ws_model[f"{col_letter}{chart_data_start_row}"] = f"={col_letter}{ROW_MAP['ACC_REVENUE']}"
        ws_model[f"{col_letter}{chart_data_start_row}"].number_format = "$#,##0"
        ws_model[f"{col_letter}{chart_data_start_row + 1}"] = f"={col_letter}{ROW_MAP['DEV_REVENUE']}"
        ws_model[f"{col_letter}{chart_data_start_row + 1}"].number_format = "$#,##0"
        ws_model[f"{col_letter}{chart_data_start_row + 2}"] = f"={col_letter}{ROW_MAP['CONTRIBUTION_MARGIN']}"
        ws_model[f"{col_letter}{chart_data_start_row + 2}"].number_format = "$#,##0"

    # Create Chart
    chart = LineChart()
    chart.title = "Monthly Revenue & Contribution Margin by Product Line"
    chart.style = 10 # A basic chart style
    chart.y_axis.title = "Amount ($)"
    chart.x_axis.title = "Month"
    chart.x_axis.delete = False # Ensure x-axis labels are visible

    # Add series to chart
    data = Reference(ws_model, min_col=2, min_row=chart_data_start_row, max_col=1+num_months, max_row=chart_data_start_row + 2)
    categories = Reference(ws_model, min_col=2, min_row=3, max_col=1+num_months)
    
    chart.add_data(data, titles_from_data=False)
    chart.set_categories(categories)

    # Set custom titles and colors for the series
    s1 = chart.series[0]
    s1.tx.v = ws_model.cell(row=chart_data_start_row, column=1).value # dynamically get title from cell A32
    s1.graphicalProperties.line.solidFill = "0000FF" # Blue

    s2 = chart.series[1]
    s2.tx.v = ws_model.cell(row=chart_data_start_row + 1, column=1).value # dynamically get title from cell A33
    s2.graphicalProperties.line.solidFill = "FFA500" # Orange

    s3 = chart.series[2]
    s3.tx.v = ws_model.cell(row=chart_data_start_row + 2, column=1).value # dynamically get title from cell A34
    s3.graphicalProperties.line.solidFill = "008000" # Green

    # Position chart
    ws_model.add_chart(chart, f"A{chart_data_start_row + 5}")

    # Final formatting for the Model tab
    # Add borders to the main data area
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    for r in range(ROW_MAP["ACC_ORDERS"], ROW_MAP["CONTRIBUTION_MARGIN"] + 1):
        for c in range(1, num_months + 2):
            ws_model.cell(row=r, column=c).border = thin_border
    # Add borders to Sanity Check section
    for r in range(ROW_MAP["SC_ACC_DEV_REV"], ROW_MAP["SC_MATCH_TOTAL_REV"] + 1):
        for c in range(1, num_months + 2):
            ws_model.cell(row=r, column=c).border = thin_border
