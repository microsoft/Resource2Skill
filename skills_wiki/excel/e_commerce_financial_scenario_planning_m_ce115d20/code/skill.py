import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, Reference
from openpyxl.utils import get_column_letter
import datetime

# Define a basic theme palette for demonstration based on video colors
def get_theme_colors(theme_name):
    colors = {
        "corporate_blue": {
            "header_bg": "FFDDEBF7",  # Light blue
            "header_fg": "FF000000",  # Black
            "input_fg": "FF0000FF",   # Blue
            "border_color": "FFD3D3D3", # Light gray
            "chart_line_1": "FF4472C4", # Blue
            "chart_line_2": "FFE69138", # Orange
            "chart_line_3": "FF6DBC47", # Green (for contribution margin)
            "match_color": "FFC6EFCE",  # Light green for match
            "match_text_color": "FF006100", # Dark green text
        }
    }
    return colors.get(theme_name, colors["corporate_blue"])

def render_workbook(wb, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    # Load theme colors
    theme_colors = get_theme_colors(theme)

    # --- Assumptions Sheet ---
    ws_assumptions = wb.create_sheet("Assumptions", 0)
    ws_assumptions.title = "Assumptions"

    # Title
    ws_assumptions['A1'] = "E-Commerce Scenario Planning Model -- Assumptions"
    ws_assumptions['A1'].font = Font(bold=True, size=14)

    # Headers for product lines
    ws_assumptions['A3'] = "ACCESSORIES"
    ws_assumptions['A3'].font = Font(bold=True)
    ws_assumptions['A9'] = "DEVICES"
    ws_assumptions['A9'].font = Font(bold=True)
    ws_assumptions['A15'] = "GENERAL"
    ws_assumptions['A15'].font = Font(bold=True)

    # Assumptions data (static for template, user would change blue cells)
    assumptions_config = {
        "ACCESSORIES": {
            "Average Order Value ($)": (45, "B4"),
            "Starting Monthly Orders": (2000, "B5"),
            "Monthly Growth Rate (%)": (0.06, "B6"),
            "Gross Margin (%)": (0.35, "B7")
        },
        "DEVICES": {
            "Average Order Value ($)": (280, "B10"),
            "Starting Monthly Orders": (500, "B11"),
            "Monthly Growth Rate (%)": (0.04, "B12"),
            "Gross Margin (%)": (0.22, "B13")
        },
        "GENERAL": {
            "Forecast Horizon (Months)": (24, "B16"),
            "Model Start Date (Month)": ("Jan 2024", "B17"),
            "Marketing Spend (% of Total Revenue)": (0.12, "B18")
        }
    }

    # Populate assumptions sheet
    for section_name, section_data in assumptions_config.items():
        start_row = 3
        if section_name == "DEVICES": start_row = 9
        if section_name == "GENERAL": start_row = 15

        for i, (label, (value, cell_ref)) in enumerate(section_data.items()):
            ws_assumptions[f'A{start_row+i+1}'] = label
            ws_assumptions[cell_ref] = value
            ws_assumptions[cell_ref].font = Font(color=theme_colors["input_fg"])
            if "%" in label:
                ws_assumptions[cell_ref].number_format = '0.0%'
            elif "$" in label:
                ws_assumptions[cell_ref].number_format = '$#,##0'
    
    # Optional styling for input explanation
    ws_assumptions['A20'] = "Note: Blue values are editable inputs. Change any assumption to update the Model tab automatically."
    ws_assumptions['A20'].font = Font(italic=True, size=9, color='FF808080')


    # --- Model Sheet ---
    ws_model = wb.create_sheet("Model", 1)
    ws_model.title = "Model"

    # Model Title
    ws_model['A1'] = "E-Commerce Scenario Planning Model -- 24-Month Forecast"
    ws_model['A1'].font = Font(bold=True, size=14)

    # Timeframe setup
    forecast_months = ws_assumptions[assumptions_config["GENERAL"]["Forecast Horizon (Months)"][1]].value
    start_date_str = ws_assumptions[assumptions_config["GENERAL"]["Model Start Date (Month)"][1]].value
    start_date = datetime.datetime.strptime(start_date_str, "%b %Y")

    # Headers for months
    month_row_idx = 3
    ws_model[f'A{month_row_idx}'] = "Metrics"
    thin_border = Border(left=Side(style='thin', color=theme_colors["border_color"]), 
                         right=Side(style='thin', color=theme_colors["border_color"]), 
                         top=Side(style='thin', color=theme_colors["border_color"]), 
                         bottom=Side(style='thin', color=theme_colors["border_color"]))

    for i in range(forecast_months):
        current_date = start_date + datetime.timedelta(days=i * 30) # Approx month start
        month_label = f"Month {i+1}\n{current_date.strftime('%b')}"
        col_letter = get_column_letter(i+2)
        ws_model[f'{col_letter}{month_row_idx}'] = month_label
        ws_model[f'{col_letter}{month_row_idx}'].alignment = Alignment(wrapText=True, horizontal='center', vertical='center')
        ws_model[f'{col_letter}{month_row_idx}'].fill = PatternFill(start_color=theme_colors["header_bg"], end_color=theme_colors["header_bg"], fill_type="solid")
        ws_model[f'{col_letter}{month_row_idx}'].font = Font(bold=True)
        ws_model[f'{col_letter}{month_row_idx}'].border = thin_border
    ws_model[f'A{month_row_idx}'].border = thin_border # Border for 'Metrics' cell

    # Row definitions and initial values/formulas
    acc_start_row = month_row_idx + 1
    dev_start_row = acc_start_row + 7
    total_start_row = dev_start_row + 7
    sanity_check_row = total_start_row + 8

    row_metrics = {
        "ACCESSORIES": {
            "header_row": acc_start_row,
            "metrics": {
                "Average Order Value ($)": acc_start_row+1,
                "Orders": acc_start_row+2,
                "Revenue ($)": acc_start_row+3,
                "Gross Margin (%)": acc_start_row+4,
                "Gross Profit ($)": acc_start_row+5
            }
        },
        "DEVICES": {
            "header_row": dev_start_row,
            "metrics": {
                "Average Order Value ($)": dev_start_row+1,
                "Orders": dev_start_row+2,
                "Revenue ($)": dev_start_row+3,
                "Gross Margin (%)": dev_start_row+4,
                "Gross Profit ($)": dev_start_row+5
            }
        },
        "COMBINED TOTALS": {
            "header_row": total_start_row,
            "metrics": {
                "Total Revenue ($)": total_start_row+1,
                "Total Gross Profit ($)": total_start_row+2,
                "Blended Gross Margin (%)": total_start_row+3,
                "Marketing Spend (% of Rev)": total_start_row+4, # Enhanced
                "Marketing Spend ($)": total_start_row+5, # Enhanced
                "Contribution Margin ($)": total_start_row+6 # Enhanced
            }
        }
    }

    # Populate metric labels
    for section, data in row_metrics.items():
        ws_model[f'A{data["header_row"]}'] = section
        ws_model[f'A{data["header_row"]}'].font = Font(bold=True)
        for label, row_idx in data["metrics"].items():
            ws_model[f'A{row_idx}'] = label

    # Sanity Check Label
    ws_model[f'A{sanity_check_row}'] = "SANITY CHECK"
    ws_model[f'A{sanity_check_row}'].font = Font(bold=True)
    ws_model[f'A{sanity_check_row+1}'] = "Accessories Rev + Devices Rev = Total Revenue?"


    # Fill in formulas for Month 1 and subsequent months
    currency_format = '$#,##0'
    percent_format = '0.0%'

    for i in range(forecast_months):
        col_letter = get_column_letter(i + 2) # B for Month 1, C for Month 2 etc.
        prev_col_letter = get_column_letter(i + 1) if i > 0 else None

        # ACCESSORIES
        ws_model[f'{col_letter}{row_metrics["ACCESSORIES"]["metrics"]["Average Order Value ($)"]}'] = f'=\'Assumptions\'!{assumptions_config["ACCESSORIES"]["Average Order Value ($)"][1]}'
        if i == 0:
            ws_model[f'{col_letter}{row_metrics["ACCESSORIES"]["metrics"]["Orders"]}'] = f'=\'Assumptions\'!{assumptions_config["ACCESSORIES"]["Starting Monthly Orders"][1]}'
        else:
            ws_model[f'{col_letter}{row_metrics["ACCESSORIES"]["metrics"]["Orders"]}'] = f'={prev_col_letter}{row_metrics["ACCESSORIES"]["metrics"]["Orders"]}*(1+\'Assumptions\'!{assumptions_config["ACCESSORIES"]["Monthly Growth Rate (%)"][1]})'
        ws_model[f'{col_letter}{row_metrics["ACCESSORIES"]["metrics"]["Revenue ($)"]}'] = f'={col_letter}{row_metrics["ACCESSORIES"]["metrics"]["Average Order Value ($)"]}*{col_letter}{row_metrics["ACCESSORIES"]["metrics"]["Orders"]}'
        ws_model[f'{col_letter}{row_metrics["ACCESSORIES"]["metrics"]["Gross Margin (%)"]}'] = f'=\'Assumptions\'!{assumptions_config["ACCESSORIES"]["Gross Margin (%)"][1]}'
        ws_model[f'{col_letter}{row_metrics["ACCESSORIES"]["metrics"]["Gross Profit ($)"]}'] = f'={col_letter}{row_metrics["ACCESSORIES"]["metrics"]["Revenue ($)"]}*{col_letter}{row_metrics["ACCESSORIES"]["metrics"]["Gross Margin (%)"]}'

        # DEVICES
        ws_model[f'{col_letter}{row_metrics["DEVICES"]["metrics"]["Average Order Value ($)"]}'] = f'=\'Assumptions\'!{assumptions_config["DEVICES"]["Average Order Value ($)"][1]}'
        if i == 0:
            ws_model[f'{col_letter}{row_metrics["DEVICES"]["metrics"]["Orders"]}'] = f'=\'Assumptions\'!{assumptions_config["DEVICES"]["Starting Monthly Orders"][1]}'
        else:
            ws_model[f'{col_letter}{row_metrics["DEVICES"]["metrics"]["Orders"]}'] = f'={prev_col_letter}{row_metrics["DEVICES"]["metrics"]["Orders"]}*(1+\'Assumptions\'!{assumptions_config["DEVICES"]["Monthly Growth Rate (%)"][1]})'
        ws_model[f'{col_letter}{row_metrics["DEVICES"]["metrics"]["Revenue ($)"]}'] = f'={col_letter}{row_metrics["DEVICES"]["metrics"]["Average Order Value ($)"]}*{col_letter}{row_metrics["DEVICES"]["metrics"]["Orders"]}'
        ws_model[f'{col_letter}{row_metrics["DEVICES"]["metrics"]["Gross Margin (%)"]}'] = f'=\'Assumptions\'!{assumptions_config["DEVICES"]["Gross Margin (%)"][1]}'
        ws_model[f'{col_letter}{row_metrics["DEVICES"]["metrics"]["Gross Profit ($)"]}'] = f'={col_letter}{row_metrics["DEVICES"]["metrics"]["Revenue ($)"]}*{col_letter}{row_metrics["DEVICES"]["metrics"]["Gross Margin (%)"]}'

        # COMBINED TOTALS
        ws_model[f'{col_letter}{row_metrics["COMBINED TOTALS"]["metrics"]["Total Revenue ($)"]}'] = f'={col_letter}{row_metrics["ACCESSORIES"]["metrics"]["Revenue ($)"]}+{col_letter}{row_metrics["DEVICES"]["metrics"]["Revenue ($)"]}'
        ws_model[f'{col_letter}{row_metrics["COMBINED TOTALS"]["metrics"]["Total Gross Profit ($)"]}'] = f'={col_letter}{row_metrics["ACCESSORIES"]["metrics"]["Gross Profit ($)"]}+{col_letter}{row_metrics["DEVICES"]["metrics"]["Gross Profit ($)"]}'
        ws_model[f'{col_letter}{row_metrics["COMBINED TOTALS"]["metrics"]["Blended Gross Margin (%)"]}'] = f'={col_letter}{row_metrics["COMBINED TOTALS"]["metrics"]["Total Gross Profit ($)"]}/{col_letter}{row_metrics["COMBINED TOTALS"]["metrics"]["Total Revenue ($)"]}'
        ws_model[f'{col_letter}{row_metrics["COMBINED TOTALS"]["metrics"]["Marketing Spend (% of Rev)"]}'] = f'=\'Assumptions\'!{assumptions_config["GENERAL"]["Marketing Spend (% of Total Revenue)"][1]}'
        ws_model[f'{col_letter}{row_metrics["COMBINED TOTALS"]["metrics"]["Marketing Spend ($)"]}'] = f'={col_letter}{row_metrics["COMBINED TOTALS"]["metrics"]["Total Revenue ($)"]}*{col_letter}{row_metrics["COMBINED TOTALS"]["metrics"]["Marketing Spend (% of Rev)"]}'
        ws_model[f'{col_letter}{row_metrics["COMBINED TOTALS"]["metrics"]["Contribution Margin ($)"]}'] = f'={col_letter}{row_metrics["COMBINED TOTALS"]["metrics"]["Total Gross Profit ($)"]}-{col_letter}{row_metrics["COMBINED TOTALS"]["metrics"]["Marketing Spend ($)"]}'

        # Sanity Check
        ws_model[f'{col_letter}{sanity_check_row+1}'] = f'=IF({col_letter}{row_metrics["ACCESSORIES"]["metrics"]["Revenue ($)"]}+{col_letter}{row_metrics["DEVICES"]["metrics"]["Revenue ($)"]}={col_letter}{row_metrics["COMBINED TOTALS"]["metrics"]["Total Revenue ($)"]}, "✔ Match", "X Mismatch")'
        ws_model[f'{col_letter}{sanity_check_row+1}'].fill = PatternFill(start_color=theme_colors["match_color"], end_color=theme_colors["match_color"], fill_type="solid")
        ws_model[f'{col_letter}{sanity_check_row+1}'].font = Font(color=theme_colors["match_text_color"])

        # Apply number formats
        for r_idx in [row_metrics["ACCESSORIES"]["metrics"]["Average Order Value ($)"], row_metrics["ACCESSORIES"]["metrics"]["Revenue ($)"], row_metrics["ACCESSORIES"]["metrics"]["Gross Profit ($)"],
                      row_metrics["DEVICES"]["metrics"]["Average Order Value ($)"], row_metrics["DEVICES"]["metrics"]["Revenue ($)"], row_metrics["DEVICES"]["metrics"]["Gross Profit ($)"],
                      row_metrics["COMBINED TOTALS"]["metrics"]["Total Revenue ($)"], row_metrics["COMBINED TOTALS"]["metrics"]["Total Gross Profit ($)"],
                      row_metrics["COMBINED TOTALS"]["metrics"]["Marketing Spend ($)"], row_metrics["COMBINED TOTALS"]["metrics"]["Contribution Margin ($)"]]:
            ws_model[f'{col_letter}{r_idx}'].number_format = currency_format

        for r_idx in [row_metrics["ACCESSORIES"]["metrics"]["Gross Margin (%)"], row_metrics["DEVICES"]["metrics"]["Gross Margin (%)"],
                      row_metrics["COMBINED TOTALS"]["metrics"]["Blended Gross Margin (%)"], row_metrics["COMBINED TOTALS"]["metrics"]["Marketing Spend (% of Rev)"]]:
            ws_model[f'{col_letter}{r_idx}'].number_format = percent_format


    # CHART
    chart_title_row = sanity_check_row + 4
    ws_model[f'A{chart_title_row}'] = "Monthly Revenue & Contribution Margin by Product Line"
    ws_model[f'A{chart_title_row}'].font = Font(bold=True)

    # Chart Data Preparation (for easier referencing by chart)
    chart_data_start_row = chart_title_row + 2
    ws_model[f'A{chart_data_start_row}'] = "Month"
    ws_model[f'A{chart_data_start_row+1}'] = "Accessories Revenue"
    ws_model[f'A{chart_data_start_row+2}'] = "Devices Revenue"
    ws_model[f'A{chart_data_start_row+3}'] = "Contribution Margin"

    for i in range(forecast_months):
        col_letter = get_column_letter(i + 2)
        ws_model[f'{col_letter}{chart_data_start_row}'] = f"Month {i+1}"
        ws_model[f'{col_letter}{chart_data_start_row+1}'] = f'={col_letter}{row_metrics["ACCESSORIES"]["metrics"]["Revenue ($)"]}'
        ws_model[f'{col_letter}{chart_data_start_row+2}'] = f'={col_letter}{row_metrics["DEVICES"]["metrics"]["Revenue ($)"]}'
        ws_model[f'{col_letter}{chart_data_start_row+3}'] = f'={col_letter}{row_metrics["COMBINED TOTALS"]["metrics"]["Contribution Margin ($)"]}'
        ws_model[f'{col_letter}{chart_data_start_row+1}'].number_format = currency_format
        ws_model[f'{col_letter}{chart_data_start_row+2}'].number_format = currency_format
        ws_model[f'{col_letter}{chart_data_start_row+3}'].number_format = currency_format


    chart = LineChart()
    chart.title = "Monthly Revenue & Contribution Margin by Product Line"
    chart.style = 10
    chart.y_axis.title = "Amount ($)"
    chart.x_axis.title = "Month"

    # Define data series
    acc_revenue_data = Reference(ws_model, min_col=2, min_row=chart_data_start_row + 1, max_col=forecast_months + 1, max_row=chart_data_start_row + 1)
    acc_revenue_series = chart.series.add(acc_revenue_data, title_from_data=True)
    acc_revenue_series.graphicalProperties.line.solidFill = theme_colors["chart_line_1"] 

    dev_revenue_data = Reference(ws_model, min_col=2, min_row=chart_data_start_row + 2, max_col=forecast_months + 1, max_row=chart_data_start_row + 2)
    dev_revenue_series = chart.series.add(dev_revenue_data, title_from_data=True)
    dev_revenue_series.graphicalProperties.line.solidFill = theme_colors["chart_line_2"] 

    cm_data = Reference(ws_model, min_col=2, min_row=chart_data_start_row + 3, max_col=forecast_months + 1, max_row=chart_data_start_row + 3)
    cm_series = chart.series.add(cm_data, title_from_data=True)
    cm_series.graphicalProperties.line.solidFill = theme_colors["chart_line_3"] 

    # Categories for X-axis (Months)
    months_category = Reference(ws_model, min_col=2, min_row=chart_data_start_row, max_col=forecast_months + 1)
    chart.set_categories(months_category)

    ws_model.add_chart(chart, f'B{chart_data_start_row + 5}') # Position chart

    # Set column widths for better readability
    ws_assumptions.column_dimensions['A'].width = 30
    ws_assumptions.column_dimensions['B'].width = 15
    ws_model.column_dimensions['A'].width = 30
    for col in range(2, forecast_months + 2):
        ws_model.column_dimensions[get_column_letter(col)].width = 12

    # Remove default sheet if it exists
    if 'Sheet' in wb.sheetnames:
        wb.remove(wb['Sheet'])

