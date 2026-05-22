### 1. High-level Skill Pattern Extraction

> **Skill Name**: E-commerce Scenario Planning Model

*   **Tier**: archetype
*   **Core Mechanism**: This skill enables the dynamic creation and enhancement of multi-sheet financial planning models based on natural language prompts. It builds an "Assumptions" sheet to manage input variables and a "Model" sheet that calculates monthly financial metrics (revenue, gross profit, marketing spend, contribution margin) over a specified forecast horizon. Formulas dynamically link to assumptions, allowing for easy scenario analysis. It also integrates line charts to visualize key trends by product line.
*   **Applicability**: Ideal for financial analysts, business owners, or consultants in e-commerce or similar industries. It's used when a user needs to quickly generate a comprehensive financial forecast, perform what-if analysis by adjusting key assumptions, or enhance existing models with new metrics and visualizations, without manually building complex Excel formulas and structures.

### 2. Structural Breakdown

-   **Data Layout**:
    -   **Assumptions Tab**: Contains clearly labeled input variables for two product lines (e.g., Accessories, Devices), including `Average Order Value ($)`, `Starting Monthly Orders`, `Monthly Order Growth Rate`, and `Gross Margin %`. A `Forecast Horizon (Months)` and `Marketing Spend % (of Total Revenue)` are also included as general parameters. Input cells are formatted distinctly.
    -   **Model Tab**: Displays a monthly 24-month forecast. For each product line, it calculates `Avg Order Value ($)`, `Monthly Orders`, `Revenue ($)`, `Gross Margin %`, and `Gross Profit ($)`. It aggregates these into `COMBINED TOTALS` for `Total Revenue ($)`, `Total Gross Profit ($)`, `Blended Gross Margin %`, `Marketing Spend (% of Rev)`, `Marketing Spend ($)`, and `Contribution Margin ($)`. A `SANITY CHECK` row confirms `Accessories Rev + Devices Rev ($)` matches `Total Revenue ($)`. Below the main table, a section prepares data for the chart, including `Accessories Revenue`, `Devices Revenue`, and `Contribution Margin` by month.
-   **Formula Logic**:
    -   All calculated fields in the "Model" tab (e.g., `Avg Order Value`, `Gross Margin %`, `Monthly Order Growth Rate`, `Marketing Spend %`) dynamically reference corresponding input cells in the "Assumptions" tab using `='Assumptions'!<cell_ref>`.
    -   `Monthly Orders` grow compoundingly based on the `Monthly Order Growth Rate`.
    -   `Revenue ($)` is calculated as `Avg Order Value * Monthly Orders`.
    -   `Gross Profit ($)` is `Revenue ($) * Gross Margin %`.
    -   `Total Revenue ($)` and `Total Gross Profit ($)` in "COMBINED TOTALS" sum values from individual product lines.
    -   `Blended Gross Margin %` is `Total Gross Profit / Total Revenue`.
    -   `Marketing Spend ($)` is `Total Revenue * Marketing Spend (% of Total Revenue)` (from Assumptions).
    -   `Contribution Margin ($)` is `Total Gross Profit - Marketing Spend ($)`.
    -   `SANITY CHECK` uses an `IF` statement to compare sums of product line revenues against `Total Revenue`.
-   **Visual Design**:
    -   Sheet titles are bold and larger.
    -   Section headers (e.g., "ACCESSORIES", "COMBINED TOTALS", "SANITY CHECK") have a light blue background fill and bold text.
    -   Input cells in the "Assumptions" tab have a light grey background fill and an accent blue font color.
    -   Number formats are applied consistently (currency, percentage, comma-separated numbers).
    -   Borders are used to delineate sections and cells.
-   **Charts/Tables**:
    -   **Line Chart**: Named "Monthly Revenue & Contribution Margin by Product Line". It displays three data series: `Accessories Revenue` (blue line), `Devices Revenue` (orange line), and `Contribution Margin` (green line) over the `Forecast Horizon (Months)`.
-   **Theme Hooks**:
    -   `header_bg`: For main section headers (e.g., product line titles, combined totals header).
    -   `input_bg`: For editable input cells in the "Assumptions" tab.
    -   `text_color`: For general text and non-input labels.
    -   `accent_1`: For line chart series 1 (Accessories Revenue) and input cell font color.
    -   `accent_2`: For line chart series 2 (Devices Revenue).
    -   `accent_3`: For line chart series 3 (Contribution Margin).
    -   `border_color`: For cell borders.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, Reference
from openpyxl.utils import get_column_letter

# Simplified theme loader for demonstration purposes.
# In a real setup, these helpers would typically be imported from a shared utility file.
def load_theme_colors(theme_name):
    if theme_name == "corporate_blue":
        return {
            "header_bg": "FFDDEBF7",  # Light blue header
            "input_bg": "FFF2F2F2",   # Light grey for inputs
            "text_color": "FF000000", # Black text
            "accent_1": "FF4472C4",   # Blue for accessories/inputs
            "accent_2": "FFED7D31",   # Orange for devices
            "accent_3": "FF70AD47",   # Green for contribution margin
            "border_color": "FFD3D3D3" # Light grey border
        }
    return {} # Default to empty if theme not found

def get_fill(color):
    return PatternFill(start_color=color, end_color=color, fill_type="solid")

def get_font(name="Calibri", size=11, bold=False, color="FF000000"):
    return Font(name=name, size=size, bold=bold, color=color)

def get_border(side_color="FFD3D3D3", style="thin"):
    thin = Side(border_style=style, color=side_color)
    return Border(left=thin, right=thin, top=thin, bottom=thin)

def render_workbook(wb, *, title: str = "E-commerce Scenario Planning Model", theme: str = "corporate_blue", **kwargs) -> None:
    colors = load_theme_colors(theme)

    # Default parameters based on video prompt
    # Accessories Product Line
    accessories = kwargs.get('accessories', {
        'avg_order_value': 45,
        'monthly_orders': 2000,
        'monthly_growth_rate': 0.06,
        'gross_margin': 0.35
    })
    # Devices Product Line
    devices = kwargs.get('devices', {
        'avg_order_value': 280,
        'monthly_orders': 500,
        'monthly_growth_rate': 0.04,
        'gross_margin': 0.22
    })
    forecast_months = kwargs.get('forecast_months', 24)
    marketing_spend_pct = kwargs.get('marketing_spend_pct', 0.12) # Added in enhancement step

    # --- Assumptions Sheet ---
    ws_assumptions = wb.active
    ws_assumptions.title = "Assumptions"
    ws_assumptions.column_dimensions['A'].width = 30
    ws_assumptions.column_dimensions['B'].width = 15

    # Title
    ws_assumptions['A1'] = title + " -- Assumptions"
    ws_assumptions['A1'].font = get_font(size=14, bold=True, color=colors["text_color"])
    ws_assumptions.merge_cells('A1:B1')

    # Accessories Inputs
    ws_assumptions['A3'] = "ACCESSORIES"
    ws_assumptions['A3'].font = get_font(bold=True, color=colors["text_color"])
    ws_assumptions['A4'] = "Average Order Value ($)"
    ws_assumptions['A5'] = "Starting Monthly Orders"
    ws_assumptions['A6'] = "Monthly Order Growth Rate"
    ws_assumptions['A7'] = "Gross Margin %"
    ws_assumptions['B4'] = accessories['avg_order_value']
    ws_assumptions['B5'] = accessories['monthly_orders']
    ws_assumptions['B6'] = accessories['monthly_growth_rate']
    ws_assumptions['B7'] = accessories['gross_margin']

    # Devices Inputs
    ws_assumptions['A9'] = "DEVICES"
    ws_assumptions['A9'].font = get_font(bold=True, color=colors["text_color"])
    ws_assumptions['A10'] = "Average Order Value ($)"
    ws_assumptions['A11'] = "Starting Monthly Orders"
    ws_assumptions['A12'] = "Monthly Order Growth Rate"
    ws_assumptions['A13'] = "Gross Margin %"
    ws_assumptions['B10'] = devices['avg_order_value']
    ws_assumptions['B11'] = devices['monthly_orders']
    ws_assumptions['B12'] = devices['monthly_growth_rate']
    ws_assumptions['B13'] = devices['gross_margin']

    # General Inputs
    ws_assumptions['A15'] = "GENERAL"
    ws_assumptions['A15'].font = get_font(bold=True, color=colors["text_color"])
    ws_assumptions['A16'] = "Forecast Horizon (Months)"
    ws_assumptions['A17'] = "Marketing Spend % (of Total Revenue)"
    ws_assumptions['B16'] = forecast_months
    ws_assumptions['B17'] = marketing_spend_pct

    # Formatting input cells
    input_cells = ['B4', 'B5', 'B6', 'B7', 'B10', 'B11', 'B12', 'B13', 'B16', 'B17']
    for cell_ref in input_cells:
        ws_assumptions[cell_ref].fill = get_fill(colors["input_bg"])
        ws_assumptions[cell_ref].border = get_border(side_color=colors["border_color"])
        ws_assumptions[cell_ref].font = get_font(color=colors["accent_1"])
        ws_assumptions[cell_ref].alignment = Alignment(horizontal='right')

    # Number formatting for assumptions
    ws_assumptions['B4'].number_format = '"$"#,##0'
    ws_assumptions['B5'].number_format = '#,##0'
    ws_assumptions['B6'].number_format = '0.0%'
    ws_assumptions['B7'].number_format = '0.0%'
    ws_assumptions['B10'].number_format = '"$"#,##0'
    ws_assumptions['B11'].number_format = '#,##0'
    ws_assumptions['B12'].number_format = '0.0%'
    ws_assumptions['B13'].number_format = '0.0%'
    ws_assumptions['B17'].number_format = '0.0%'


    # --- Model Sheet ---
    ws_model = wb.create_sheet("Model")
    ws_model.column_dimensions['A'].width = 30

    # Title
    ws_model['A1'] = title + " -- 24-Month Forecast"
    ws_model['A1'].font = get_font(size=14, bold=True, color=colors["text_color"])
    ws_model.merge_cells('A1:C1')

    # Month Headers
    for i in range(1, forecast_months + 1):
        col_letter = get_column_letter(i + 1) # B, C, D...
        ws_model[col_letter + '3'] = f"Month {i}"
        ws_model[col_letter + '3'].font = get_font(bold=True, color=colors["text_color"])
        ws_model[col_letter + '3'].fill = get_fill(colors["header_bg"])
        ws_model[col_letter + '3'].border = get_border(side_color=colors["border_color"])
        ws_model.column_dimensions[col_letter].width = 12

    # Populate data for each product line
    # Define starting row for first product line data
    data_start_row = 4
    for product_type, assumption_start_row in [
        ("ACCESSORIES", 4), # Assumptions!B4 for Avg Order Value
        ("DEVICES", 10)     # Assumptions!B10 for Avg Order Value
    ]:
        # Product Line Header
        ws_model[f'A{data_start_row}'] = product_type
        ws_model[f'A{data_start_row}'].font = get_font(bold=True, color=colors["text_color"])
        ws_model[f'A{data_start_row}'].fill = get_fill(colors["header_bg"])
        ws_model[f'A{data_start_row}'].border = get_border(side_color=colors["border_color"])
        data_start_row += 1

        # Metric Labels
        ws_model[f'A{data_start_row}'] = "Avg Order Value ($)"
        ws_model[f'A{data_start_row+1}'] = "Monthly Orders"
        ws_model[f'A{data_start_row+2}'] = "Revenue ($)"
        ws_model[f'A{data_start_row+3}'] = "Gross Margin %"
        ws_model[f'A{data_start_row+4}'] = "Gross Profit ($)"

        # Populate Monthly Data and Formulas
        for i in range(1, forecast_months + 1):
            col_letter = get_column_letter(i + 1)
            # Avg Order Value (fixed from assumptions)
            ws_model[col_letter + str(data_start_row)] = f"='Assumptions'!B{assumption_start_row}"
            ws_model[col_letter + str(data_start_row)].number_format = '"$"#,##0'

            # Monthly Orders (grows based on rate)
            if i == 1:
                ws_model[col_letter + str(data_start_row+1)] = f"='Assumptions'!B{assumption_start_row+1}"
            else:
                prev_col_letter = get_column_letter(i)
                ws_model[col_letter + str(data_start_row+1)] = f"={prev_col_letter}{data_start_row+1}*(1+'Assumptions'!B{assumption_start_row+2})"
            ws_model[col_letter + str(data_start_row+1)].number_format = '#,##0'

            # Revenue
            ws_model[col_letter + str(data_start_row+2)] = f"={col_letter}{data_start_row}*{col_letter}{data_start_row+1}"
            ws_model[col_letter + str(data_start_row+2)].number_format = '"$"#,##0'

            # Gross Margin % (fixed from assumptions)
            ws_model[col_letter + str(data_start_row+3)] = f"='Assumptions'!B{assumption_start_row+3}"
            ws_model[col_letter + str(data_start_row+3)].number_format = '0.0%'

            # Gross Profit
            ws_model[col_letter + str(data_start_row+4)] = f"={col_letter}{data_start_row+2}*{col_letter}{data_start_row+3}"
            ws_model[col_letter + str(data_start_row+4)].number_format = '"$"#,##0'
        data_start_row += 6 # Move to next product line section

    # Combined Totals
    combined_totals_start_row = data_start_row + 1 # Row after last product line
    ws_model[f'A{combined_totals_start_row}'] = "COMBINED TOTALS"
    ws_model[f'A{combined_totals_start_row}'].font = get_font(bold=True, color=colors["text_color"])
    ws_model[f'A{combined_totals_start_row}'].fill = get_fill(colors["header_bg"])
    ws_model[f'A{combined_totals_start_row}'].border = get_border(side_color=colors["border_color"])
    combined_totals_start_row += 1

    ws_model[f'A{combined_totals_start_row}'] = "Total Revenue ($)"
    ws_model[f'A{combined_totals_start_row+1}'] = "Total Gross Profit ($)"
    ws_model[f'A{combined_totals_start_row+2}'] = "Blended Gross Margin %"
    ws_model[f'A{combined_totals_start_row+3}'] = "Marketing Spend (% of Rev)"
    ws_model[f'A{combined_totals_start_row+4}'] = "Marketing Spend ($)"
    ws_model[f'A{combined_totals_start_row+5}'] = "Contribution Margin ($)"

    # Helper row references (assuming Accessories is first, Devices second)
    acc_rev_row_in_model = 5 + 2 # A5 (Accessories section starts at A4) + 2 for Revenue row
    dev_rev_row_in_model = 5 + 6 + 2 # D11 (Devices section starts at A10) + 2 for Revenue row
    acc_gp_row_in_model = 5 + 4 # A5 (Accessories section starts at A4) + 4 for Gross Profit row
    dev_gp_row_in_model = 5 + 6 + 4 # D11 (Devices section starts at A10) + 4 for Gross Profit row

    for i in range(1, forecast_months + 1):
        col_letter = get_column_letter(i + 1)
        # Total Revenue
        ws_model[col_letter + str(combined_totals_start_row)] = f"={col_letter}{acc_rev_row_in_model}+{col_letter}{dev_rev_row_in_model}"
        ws_model[col_letter + str(combined_totals_start_row)].number_format = '"$"#,##0'

        # Total Gross Profit
        ws_model[col_letter + str(combined_totals_start_row+1)] = f"={col_letter}{acc_gp_row_in_model}+{col_letter}{dev_gp_row_in_model}"
        ws_model[col_letter + str(combined_totals_start_row+1)].number_format = '"$"#,##0'

        # Blended Gross Margin %
        ws_model[col_letter + str(combined_totals_start_row+2)] = f"={col_letter}{combined_totals_start_row+1}/{col_letter}{combined_totals_start_row}"
        ws_model[col_letter + str(combined_totals_start_row+2)].number_format = '0.0%'

        # Marketing Spend (% of Rev)
        ws_model[col_letter + str(combined_totals_start_row+3)] = f"='Assumptions'!B17"
        ws_model[col_letter + str(combined_totals_start_row+3)].number_format = '0.0%'

        # Marketing Spend ($)
        ws_model[col_letter + str(combined_totals_start_row+4)] = f"={col_letter}{combined_totals_start_row}*{col_letter}{combined_totals_start_row+3}"
        ws_model[col_letter + str(combined_totals_start_row+4)].number_format = '"$"#,##0'

        # Contribution Margin ($)
        ws_model[col_letter + str(combined_totals_start_row+5)] = f"={col_letter}{combined_totals_start_row+1}-{col_letter}{combined_totals_start_row+4}"
        ws_model[col_letter + str(combined_totals_start_row+5)].number_format = '"$"#,##0'

    # Sanity Check
    sanity_check_row = combined_totals_start_row + 7
    ws_model[f'A{sanity_check_row}'] = "SANITY CHECK"
    ws_model[f'A{sanity_check_row}'].font = get_font(bold=True, color=colors["text_color"])
    ws_model[f'A{sanity_check_row}'].fill = get_fill(colors["header_bg"])
    ws_model[f'A{sanity_check_row}'].border = get_border(side_color=colors["border_color"])
    sanity_check_row += 1

    ws_model[f'A{sanity_check_row}'] = "Accessories Rev + Devices Rev ($)"
    ws_model[f'A{sanity_check_row+1}'] = "Matches Total Revenue?"

    for i in range(1, forecast_months + 1):
        col_letter = get_column_letter(i + 1)
        ws_model[col_letter + str(sanity_check_row)] = f"={col_letter}{acc_rev_row_in_model}+{col_letter}{dev_rev_row_in_model}"
        ws_model[col_letter + str(sanity_check_row)].number_format = '"$"#,##0'

        match_formula = f"=IF({col_letter}{sanity_check_row}={col_letter}{combined_totals_start_row},\"Match\",\"No Match\")"
        ws_model[col_letter + str(sanity_check_row+1)] = match_formula
        ws_model[col_letter + str(sanity_check_row+1)].font = get_font(bold=True) # Bold for visibility

    # Chart Data Preparation
    chart_data_start_row = sanity_check_row + 4
    ws_model[f'A{chart_data_start_row}'] = "Monthly Revenue & Contribution Margin by Product Line"
    ws_model[f'A{chart_data_start_row}'].font = get_font(size=12, bold=True, color=colors["text_color"])
    ws_model.merge_cells(f'A{chart_data_start_row}:{get_column_letter(forecast_months+1)}{chart_data_start_row}')
    chart_data_start_row += 1

    ws_model[f'A{chart_data_start_row}'] = "Accessories Revenue"
    ws_model[f'A{chart_data_start_row+1}'] = "Devices Revenue"
    ws_model[f'A{chart_data_start_row+2}'] = "Contribution Margin"

    for i in range(1, forecast_months + 1):
        col_letter = get_column_letter(i + 1)
        ws_model[col_letter + str(chart_data_start_row)] = f"={col_letter}{acc_rev_row_in_model}"
        ws_model[col_letter + str(chart_data_start_row+1)] = f"={col_letter}{dev_rev_row_in_model}"
        ws_model[col_letter + str(chart_data_start_row+2)] = f"={col_letter}{combined_totals_start_row+5}"


    # Line Chart
    chart = LineChart()
    chart.title = "Monthly Revenue & Contribution Margin by Product Line"
    chart.style = 10 # A default chart style
    chart.x_axis.title = "Month"
    chart.y_axis.title = "Amount ($)"

    # Category axis (Months)
    months_ref = Reference(ws_model, min_col=2, min_row=chart_data_start_row - 1, max_col=forecast_months + 1, max_row=chart_data_start_row - 1)
    chart.set_categories(months_ref)

    # Accessories Revenue Series
    acc_revenue_data_ref = Reference(ws_model, min_col=2, min_row=chart_data_start_row, max_col=forecast_months + 1, max_row=chart_data_start_row)
    chart.add_data(acc_revenue_data_ref, titles_from_data=True)
    s1 = chart.series[0]
    s1.tx.v = ws_model[f'A{chart_data_start_row}']
    s1.graphicalProperties.line.solidFill = colors["accent_1"] # Blue line

    # Devices Revenue Series
    dev_revenue_data_ref = Reference(ws_model, min_col=2, min_row=chart_data_start_row + 1, max_col=forecast_months + 1, max_row=chart_data_start_row + 1)
    chart.add_data(dev_revenue_data_ref, titles_from_data=True)
    s2 = chart.series[1]
    s2.tx.v = ws_model[f'A{chart_data_start_row+1}']
    s2.graphicalProperties.line.solidFill = colors["accent_2"] # Orange line

    # Contribution Margin Series
    contrib_margin_data_ref = Reference(ws_model, min_col=2, min_row=chart_data_start_row + 2, max_col=forecast_months + 1, max_row=chart_data_start_row + 2)
    chart.add_data(contrib_margin_data_ref, titles_from_data=True)
    s3 = chart.series[2]
    s3.tx.v = ws_model[f'A{chart_data_start_row+2}']
    s3.graphicalProperties.line.solidFill = colors["accent_3"] # Green line

    chart.height = 10 # cm
    chart.width = 20 # cm
    ws_model.add_chart(chart, f"B{chart_data_start_row + 4}") # Position chart
```