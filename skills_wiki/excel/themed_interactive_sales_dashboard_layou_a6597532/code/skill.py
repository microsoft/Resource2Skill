from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as OpenpyxlImage
from io import BytesIO
from base64 import b64decode
import os
import sys

# Add skills_library to sys.path if not already there
script_dir = os.path.dirname(__file__)
skills_library_path = os.path.abspath(os.path.join(script_dir, '../../../'))
if skills_library_path not in sys.path:
    sys.path.insert(0, skills_library_path)

from skills_library.excel.components._helpers import (
    get_theme_colors, apply_fill_and_font, apply_border
)

def render_sheet(wb: Workbook, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders an interactive sales dashboard layout on a new sheet.

    Args:
        wb (Workbook): The openpyxl workbook object.
        sheet_name (str): The name for the new dashboard sheet.
        title (str): The main title for the dashboard.
        theme (str): The name of the color theme to use.
        **kwargs: Additional keyword arguments for customization.
    """
    ws = wb.create_sheet(sheet_name)
    theme_colors = get_theme_colors(theme)

    # 1. Set up sheet dimensions and background colors
    ws.column_dimensions['A'].width = 5 # Narrow left margin
    for col_letter in ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
        ws.column_dimensions[col_letter].width = 10 # Standard column width

    # Header background (rows 1-8)
    header_fill = PatternFill(start_color=theme_colors.header_bg, end_color=theme_colors.header_bg, fill_type="solid")
    for row in range(1, 9):
        for col_idx in range(1, ws.max_column + 1):
            ws.cell(row=row, column=col_idx).fill = header_fill

    # Body background (rows 9-40)
    body_fill = PatternFill(start_color=theme_colors.body_bg, end_color=theme_colors.body_bg, fill_type="solid")
    for row in range(9, 41):
        for col_idx in range(1, ws.max_column + 1):
            ws.cell(row=row, column=col_idx).fill = body_fill

    # 2. Add main title and subheading
    ws.merge_cells('B2:F2')
    title_cell = ws['B2']
    title_cell.value = title
    apply_fill_and_font(title_cell, fill_color=theme_colors.header_bg, font_color=theme_colors.text_light, font_size=36, bold=True)
    title_cell.alignment = Alignment(horizontal='left', vertical='center')

    ws.merge_cells('B4:F4')
    subtitle_cell = ws['B4']
    subtitle_cell.value = "Evaluating Sales Agent Performance"
    apply_fill_and_font(subtitle_cell, fill_color=theme_colors.header_bg, font_color=theme_colors.accent_primary, font_size=16)
    subtitle_cell.alignment = Alignment(horizontal='left', vertical='center')

    # 3. Create KPI placeholders and icons (simplified for layout demonstration)
    kpi_data = [
        {"label": "CALLS", "value": "16,749", "icon_base64": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iIzVjMjU2ZSI+PHBhdGggZD0iTTE4LDBIMjEuNUEyLjUgMi41IDAgMCAxIDI0IDIuNVYxOEExLjk5IDEuOTkgMCAwIDEtMjIgMjEuNkwxOSwxOGMtLjU1LTEuNTctMS4xMi0zLjE1LTEuNjctNC43MkMyMS41IDcuOTQgMjQuMDkgMi4wNiAxOCAyLjA2WiIgLz48cGF0aCBkPSJNOSwxNmE2LjQ5IDYuNDkgMCAwIDAtNi41LTkuNjcgNi40OS1lMi02LjUtNi40OS02LjVsOS40OSAyLjA2LTMuNjcgMy41OCAxLjY3LS45MiAxLjY3LS45MiAyLjUuNSAyLjUsNS41LjUgMi41TDE4LjUgNi41IDYuNSAxOC41bC02LjUtNi41TDAuNSAxOEwtLjUgMjIuNS02LjUgMTkuMDkgNC41IDYuNTcgMTYuNS01Ljg3WiIgLz48L3N2Zz4="},
        {"label": "REACHED", "value": "3,328", "icon_base64": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iIzVjMjU2ZSI+PHBhdGggZD0iTTEyLDIuMDY1YTEwLjk4NyAxMC45ODcgMCAwIDAgLTExIDEwLjkzNSAxMS4wMDggMTEuMDA4IDAgMCAwIDExLDEwLjgzNCAxMC45ODYgMTAuOTg2IDAgMCAwIDExLTAuOTM1IDExLjAwOSAxMS4wMDkgMCAwIDAgLTEgLTExLjE3MUwxMiwyLjA2NVpNMTIuNTY2LDE3LjI5OEgxMS4yOTFWOC4zMzNsNC42MzItMS42NzdjMC41MDQtMC4xNjggMS4wMDgtMC40MiAxLjM0NC0uNjczbC0wLjUyNS0yLjQzM2MtMC40MiAwLjE1Ni0wLjc1NiAwLjMyNC0xLjM2NSAwLjUyNS0xLjAyOSAwLjMyNC0yLjA1OCAwLjcwMy0zLjI5MiAxLjExN0wxMi41NjYsMTcuMjk4WiIgLz48L3N2Zz4="},
        {"label": "CLOSED", "value": "1,203", "icon_base64": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iIzVjMjU2ZSI+PHBhdGggZD0iTTEyLDEuMTI1YTIuNzUgMi43NSAwIDAgMSAyLjc1IDIuNzVjMCAxLjUzLTIuNzUgNC4xMi0yLjc1IDQuMTJDOS4yNSA4LDE2LjUuMTI1LDEyLDEuMTI1eiIgLz48cGF0aCBkPSJNMjEuNSwxMi40MzhhMTAuNSAxMC41IDAgMSAxIC0xMC41LTEwLjUgMTAuNTggMTAuNTggMCAwIDEgMTAuNSAxMC41eiIvPjxwYXRoIGQ9Ik03LjI1LDE0Ljk1MmE3LjI1IDcuMjUgMCAwIDEgLTUuNTA0LTcuMjUgNy40OSA3LjQ5IDAgMCAxIDUuNTA0LTcuMjUgNy4yNTEgNy4yNTEgMCAwIDEgNy4yNS01LjUwNCA3LjQ4OSA3LjQ4OSAwIDAgMSAgNy4yNS01LjUwNCBMNy4yNSAxNC45NTJaIiAvPjwvc3ZnPg=="},
        {"label": "VALUE", "value": "$646,979", "icon_base64": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iIzVjMjU2ZSI+PHBhdGggZD0iTTE5LDIxSDBWMy41aDE5VjIxWiIvPjxwYXRoIGQ9Ik02LjUuNjgyVjcuMTAyTDMuNTc2LDguMzcyTDYuNSw5LjU5Mkw5LjQyNCwxMC44NjJMNi41LDEyLjA3NlYxOC4xODJMMjQsMTQuODQ4VjEuNTgyTDE5LDEuMTI1TDYuNSwuNjgyWiIvPjwvc3ZnPg=="},
    ]

    # Use a base-64 encoded transparent 1x1 GIF for blank images
    BLANK_GIF = "R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=="

    kpi_shape_fill = PatternFill(start_color=theme_colors.accent_primary, end_color=theme_colors.accent_primary, fill_type="solid")
    kpi_inner_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    kpi_border = Border(left=Side(style='thin', color=theme_colors.accent_primary),
                        right=Side(style='thin', color=theme_colors.accent_primary),
                        top=Side(style='thin', color=theme_colors.accent_primary),
                        bottom=Side(style='thin', color=theme_colors.accent_primary))

    for i, kpi in enumerate(kpi_data):
        col_start = 8 + (i * 4) + 1 # Start at I column (8+1), then increment by 4
        col_end = col_start + 3 # 4 columns wide per KPI

        # Outer rounded shape (gold)
        ws.merge_cells(start_row=5, start_column=col_start, end_row=7, end_column=col_end)
        outer_shape_cell = ws.cell(row=5, column=col_start)
        # In openpyxl, shapes are not directly drawn into cells like in Excel GUI.
        # We simulate the layout with merged cells and background fills.
        for r in range(5, 8):
            for c in range(col_start, col_end + 1):
                ws.cell(row=r, column=c).fill = kpi_shape_fill
                ws.cell(row=r, column=c).border = kpi_border
        # This is a simplification. Actual rounded corner shapes in openpyxl are more complex.

        # Inner white shape (simulated with merged cell)
        ws.merge_cells(start_row=5, start_column=col_start + 1, end_row=7, end_column=col_end)
        inner_shape_cell = ws.cell(row=5, column=col_start + 1)
        for r in range(5, 8):
            for c in range(col_start + 1, col_end + 1):
                ws.cell(row=r, column=c).fill = kpi_inner_fill
                ws.cell(row=r, column=c).border = kpi_border

        # Icon (placed approximately)
        icon_data = b64decode(kpi["icon_base64"])
        img_stream = BytesIO(icon_data)
        img = OpenpyxlImage(img_stream)
        img.width = 30
        img.height = 30
        ws.add_image(img, anchor=f'{get_column_letter(col_start+1)}5') # E.g., J5 for the first icon

        # Value
        value_cell = ws.cell(row=6, column=col_start + 2) # E.g., K6 for the first value
        value_cell.value = kpi["value"] # In real scenario, link to Analysis sheet: =Analysis!B4
        apply_fill_and_font(value_cell, fill_color="FFFFFF", font_color=theme_colors.text_dark, font_size=32, bold=True)
        value_cell.alignment = Alignment(horizontal='center', vertical='center')

        # Label
        label_cell = ws.cell(row=7, column=col_start + 2) # E.g., K7 for the first label
        label_cell.value = kpi["label"]
        apply_fill_and_font(label_cell, fill_color="FFFFFF", font_color=theme_colors.text_dark, font_size=18)
        label_cell.alignment = Alignment(horizontal='center', vertical='center')

    # 4. Placeholders for PivotTable and Charts (actual data/charts would be inserted dynamically)
    # Sales Agent KPIs Table Placeholder
    ws.merge_cells('B9:G38')
    sales_agent_kpis_title_cell = ws['B9']
    sales_agent_kpis_title_cell.value = "Sales Agent KPIs"
    apply_fill_and_font(sales_agent_kpis_title_cell, fill_color=theme_colors.accent_secondary, font_color=theme_colors.text_light, font_size=16)
    sales_agent_kpis_title_cell.alignment = Alignment(horizontal='left', vertical='center')
    # This cell would be followed by a PivotTable. In openpyxl, you would create the PivotTable
    # on a separate sheet (e.g., 'Analysis') and copy-paste it as a picture or embed it as a chart.
    # For a sheet_shell, we're just setting up the *space* and *style*.

    # Slicer Placeholder (Name)
    # The slicer would be an object on the sheet, typically generated from a PivotTable.
    # We just create space for it here.
    ws.merge_cells('B10:B38')
    slicer_placeholder_cell = ws['B10']
    slicer_placeholder_cell.value = "Name Slicer" # Placeholder text
    slicer_placeholder_cell.fill = PatternFill(start_color=theme_colors.accent_secondary, end_color=theme_colors.accent_secondary, fill_type="solid")
    slicer_placeholder_cell.font = Font(color=theme_colors.text_light)
    slicer_placeholder_cell.alignment = Alignment(horizontal='center', vertical='center')

    # Monthly Trends Charts (4 placeholders for various charts)
    chart_areas = [
        ('H9:M23', "Sum of Calls Reached + Deals Closed"),
        ('N9:S23', "Total Sales"),
        ('H24:M38', "Average Call Duration (Seconds)"),
        ('N24:S38', "Call Drop Rate %"),
    ]
    for chart_range, chart_title in chart_areas:
        ws.merge_cells(chart_range)
        chart_cell = ws[chart_range.split(':')[0]]
        chart_cell.value = chart_title + " (Chart Placeholder)" # Placeholder text
        chart_cell.fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
        chart_cell.font = Font(color=theme_colors.text_dark)
        chart_cell.alignment = Alignment(horizontal='center', vertical='center')
        chart_cell.border = kpi_border # Use the same border for consistency

    # Deactivate gridlines
    ws.sheet_view.showGridLines = False

# Example of how to use it
if __name__ == '__main__':
    wb = Workbook()
    # Remove default sheet
    if 'Sheet' in wb.sheetnames:
        wb.remove(wb['Sheet'])

    # Example theme definition (mimicking "Aspect" purple/yellow)
    my_custom_theme = {
        "header_bg": "5C256E", # Dark purple
        "body_bg": "F2EFF5",  # Light purple
        "accent_primary": "FFBF00", # Gold/Yellow
        "accent_secondary": "9E7BB5", # Medium purple
        "text_dark": "5C256E",
        "text_light": "FFFFFF",
        "neutral_dark": "666666",
        "neutral_light": "CCCCCC",
    }

    render_sheet(wb, "Dashboard", title="Sales Dashboard", theme=my_custom_theme)

    # Save the workbook
    # wb.save("themed_sales_dashboard.xlsx")
    # print("Dashboard saved to themed_sales_dashboard.xlsx")
