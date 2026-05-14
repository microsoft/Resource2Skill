### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Static Sales Dashboard Layout

*   **Tier**: sheet_shell
*   **Core Mechanism**: Sets up a visually cohesive dashboard layout on a single worksheet, including a styled header, KPI cards (simulated with styled cells), icon placeholders (simulated with text), and pre-styled charts/tables based on static data. It demonstrates cohesive theming and layout for a dashboard presentation, suitable for reports where the visual structure and branding are paramount.
*   **Applicability**: Useful for creating aesthetically pleasing, static report dashboards in Excel. Can serve as a template where data is manually updated or processed by external scripts. Ideal when the primary requirement is visual presentation over dynamic in-Excel interaction, or when dynamic features are handled by external tools (e.g., Power Query or Power BI data models that refresh the pivot cache but `openpyxl` only sets up the layout). *Note: Openpyxl does not support creating interactive PivotTables or Slicers, nor dynamic linking of shapes to changing cell values. This skill focuses on the static visual design aspect.*

### 2. Structural Breakdown

-   **Data Layout**: Assumes raw data is in a sheet named 'Data'. The 'Dashboard' sheet is designed for presentation, referencing static summary data (mocked here on an 'Analysis' sheet for chart data).
-   **Formula Logic**: Placeholder for KPI values (e.g., direct cell references or mocked `GETPIVOTDATA` results). Conditional formatting for highlighting a selected agent's row (demonstrated with a static formula).
-   **Visual Design**:
    *   **Header**: Deep purple background (merged cells), white main title (36pt, bold), yellow subtitle (16pt).
    *   **KPI Cards**: Simulated using styled cell ranges. Gold accent bar on the left, white main area. Purple text for values (32pt) and labels (18pt). Icon placeholders represented by basic shapes/text.
    *   **Charts/Tables**: No fill or outline for chart areas. Themed colors for chart series (gold, medium purple). Shadows applied to charts.
    *   **Sales Agent KPIs Table**: Purple header with white text, alternating light lavender and lighter grey for rows. Conditional data bars (gold for calls, medium purple for deals). Highlighting for selected row (e.g., a specific border).
-   **Charts/Tables**:
    *   **KPI Cards**: 4 cards (Total Calls, Calls Reached, Deals Closed, Deal Value), each composed of styled merged cells for background/accent and two cells for value and label. Icons are simple text placeholders.
    *   **Sales Agent KPIs Table**: A static table (cells D9:H39) with sample data, headers, and applied conditional formatting rules.
    *   **"Sum of Calls Reached vs. Deals Closed" Chart**: Stacked Column Chart (cells J9:N23).
    *   **"Total Sales" Chart**: Column Chart with a linear trendline (cells Q9:U23).
    *   **"Average Call Duration (seconds)" Chart**: Column Chart (cells J25:N39).
    *   **"Average Call Drop Rate %" Chart**: Area Chart (cells Q25:U39).
-   **Theme Hooks**: `header_bg`, `header_text`, `subheader_text`, `background_body`, `accent_1`, `accent_2`, `text_main`, `chart_series_1`, `chart_series_2`, `chart_trendline`, `table_header_bg`, `table_header_text`, `table_row_bg_1`, `table_row_bg_2`, `border_color`.

### 3. Reproduction Code

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, AreaChart, Reference
from openpyxl.formatting.rule import FormulaRule, Rule
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter

# --- Helper functions (mocked _helpers.py content for self-contained skill) ---
def get_theme_colors(theme_name="default"):
    # Default theme inspired by the video's 'Aspect' theme
    return {
        "header_bg": "800080", # Deep Purple
        "header_text": "FFFFFF", # White
        "subheader_text": "FFFF00", # Yellow
        "background_body": "F2EFF5", # Light Lavender (similar to F2EFF5)
        "accent_1": "FFD700", # Gold (for main KPI cards, chart bars)
        "accent_2": "9370DB", # Medium Purple (for other chart bars, conditional formatting)
        "text_main": "333333", # Dark Grey
        "border_color": "800080", # Purple for borders
    }

def apply_fill(ws, cell_range, color):
    fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
    for row in ws[cell_range]:
        for cell in row:
            cell.fill = fill

def apply_font(ws, cell_range, size, color, bold=False):
    font = Font(size=size, color=color, bold=bold)
    for row in ws[cell_range]:
        for cell in row:
            cell.font = font

def apply_alignment(ws, cell_range, horizontal='center', vertical='center', wrap_text=False):
    alignment = Alignment(horizontal=horizontal, vertical=vertical, wrap_text=wrap_text)
    for row in ws[cell_range]:
        for cell in row:
            cell.alignment = alignment

def create_border(color="000000", style="thin"):
    side = Side(border_style=style, color=color)
    return Border(left=side, right=side, top=side, bottom=side)

def apply_border_to_range(ws, cell_range, border_style, border_color):
    border = create_border(border_color, border_style)
    for row in ws[cell_range]:
        for cell in row:
            cell.border = border
            
# --- End Helper functions ---


def render_sheet(ws, sheet_name: str, *, title: str, theme: str = "default", **kwargs) -> None:
    """
    Renders a visually coherent sales dashboard layout on a single worksheet,
    including a styled header, KPI cards (simulated with styled cells),
    icon placeholders (simulated with text), and pre-styled charts/tables
    based on static data.

    Args:
        ws: The openpyxl worksheet to render on.
        sheet_name (str): The name of the sheet (used for context, not directly in openpyxl for sheet_shell).
        title (str): The main title of the dashboard.
        theme (str): The theme name for color application.
        **kwargs: Additional keyword arguments.
    """
    theme_colors = get_theme_colors(theme)
    ws.title = "Dashboard" # Ensure the sheet has the correct name

    # Set default column widths for better spacing (inspired by video)
    for i in range(1, 25): # A to X
        ws.column_dimensions[get_column_letter(i)].width = 4.5 # Roughly matches the video's spacing for cells

    # 1. Dashboard Header
    ws.merge_cells('B1:U8')
    header_cell = ws['B1']
    header_cell.value = title
    header_cell.fill = PatternFill(start_color=theme_colors["header_bg"], end_color=theme_colors["header_bg"], fill_type="solid")
    header_cell.font = Font(size=36, color=theme_colors["header_text"], bold=True)
    header_cell.alignment = Alignment(horizontal='left', vertical='center')

    subheader_cell = ws['B5'] # Adjust based on actual header cell size if needed
    subheader_cell.value = "Evaluating Sales Agent Performance"
    subheader_cell.font = Font(size=16, color=theme_colors["subheader_text"], bold=False)
    subheader_cell.alignment = Alignment(horizontal='left', vertical='center')

    # Apply background color to the rest of the sheet below the header
    for r in range(9, ws.max_row + 1):
        for c in range(1, ws.max_column + 1):
            ws.cell(row=r, column=c).fill = PatternFill(start_color=theme_colors["background_body"], end_color=theme_colors["background_body"], fill_type="solid")

    # --- KPI Cards (simulated with merged cells and text) ---
    kpi_definitions = [
        {"anchor": "D2", "value": 16749, "label": "CALLS", "icon": "📞"},
        {"anchor": "I2", "value": 3328, "label": "REACHED", "icon": "👥"},
        {"anchor": "N2", "value": 1203, "label": "CLOSED", "icon": "🏅"},
        {"anchor": "S2", "value": 646979, "label": "VALUE", "icon": "💰"},
    ]

    for kpi in kpi_definitions:
        # Gold accent bar (2 columns wide, 6 rows tall)
        accent_start_col = ws[kpi["anchor"]].column
        accent_end_col = accent_start_col + 1
        accent_range = f"{get_column_letter(accent_start_col)}{ws[kpi['anchor']].row}:{get_column_letter(accent_end_col)}{ws[kpi['anchor']].row + 5}"
        apply_fill(ws, accent_range, theme_colors["accent_1"])
        
        # Main white area (3 columns wide, 6 rows tall)
        main_start_col = accent_start_col + 2
        main_end_col = accent_start_col + 4
        main_range = f"{get_column_letter(main_start_col)}{ws[kpi['anchor']].row}:{get_column_letter(main_end_col)}{ws[kpi['anchor']].row + 5}"
        apply_fill(ws, main_range, "FFFFFF")
        
        # Icon (text based for simplicity)
        icon_cell = ws.cell(row=ws[kpi['anchor']].row + 1, column=accent_start_col + 1)
        icon_cell.value = kpi["icon"]
        icon_cell.font = Font(size=24, color=theme_colors["text_main"])
        icon_cell.alignment = Alignment(horizontal='center', vertical='center')

        # Value
        value_cell = ws.cell(row=ws[kpi['anchor']].row + 1, column=main_start_col)
        ws.merge_cells(f"{get_column_letter(main_start_col)}{ws[kpi['anchor']].row + 1}:{get_column_letter(main_end_col)}{ws[kpi['anchor']].row + 1}")
        value_cell.value = kpi["value"]
        value_cell.font = Font(size=32, color=theme_colors["text_main"], bold=True)
        value_cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # Label
        label_cell = ws.cell(row=ws[kpi['anchor']].row + 3, column=main_start_col)
        ws.merge_cells(f"{get_column_letter(main_start_col)}{ws[kpi['anchor']].row + 3}:{get_column_letter(main_end_col)}{ws[kpi['anchor']].row + 3}")
        label_cell.value = kpi["label"]
        label_cell.font = Font(size=18, color=theme_colors["text_main"])
        label_cell.alignment = Alignment(horizontal='center', vertical='center')

    # --- Sales Agent KPIs Table (static data for layout demonstration) ---
    ws.cell(row=9, column=2).value = "Sales Agent KPIs"
    apply_font(ws, "B9", 14, theme_colors["text_main"], bold=True)

    # Mock data for Sales Agent KPIs table
    sa_data_header = ["Name", "Total Calls", "Calls Reached", "Deals Closed", "Deal Value ($)"]
    sa_data_rows = [
        ["Mimi", 414, 86, 67, 45236], ["Evan", 722, 368, 70, 41804], ["Ian", 949, 395, 81, 41818],
        ["Karol", 807, 348, 69, 40992], ["Alice", 827, 356, 73, 41200], ["Bob", 661, 330, 68, 40596],
        ["Charlie", 630, 310, 66, 39569], ["David", 737, 292, 59, 38580], ["Diana", 566, 225, 48, 37042],
        ["Emma", 1057, 375, 78, 37879], ["Grace", 1096, 396, 82, 38290], ["James", 705, 297, 60, 37274],
    ] # Shortened for example

    # Populate table data
    table_start_row, table_start_col = 10, 2
    for c_idx, header in enumerate(sa_data_header):
        ws.cell(row=table_start_row, column=table_start_col + c_idx).value = header
        ws.cell(row=table_start_row, column=table_start_col + c_idx).fill = PatternFill(start_color=theme_colors["table_header_bg"], end_color=theme_colors["table_header_bg"], fill_type="solid")
        ws.cell(row=table_start_row, column=table_start_col + c_idx).font = Font(color=theme_colors["table_header_text"])

    for r_idx, row_data in enumerate(sa_data_rows):
        for c_idx, cell_value in enumerate(row_data):
            cell = ws.cell(row=table_start_row + 1 + r_idx, column=table_start_col + c_idx)
            cell.value = cell_value
            # Alternating row colors
            bg_color = theme_colors["table_row_bg_1"] if r_idx % 2 == 0 else theme_colors["table_row_bg_2"]
            cell.fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
            if c_idx > 0 and isinstance(cell_value, (int, float)):
                cell.number_format = '#,##0' if c_idx < 4 else '$#,##0'
                
    # Conditional Formatting for Data Bars and highlighting (static example)
    data_bar_range_start_row = table_start_row + 1
    data_bar_range_end_row = table_start_row + len(sa_data_rows)
    
    # Data bars for Total Calls
    ws.conditional_formatting.add(f'{get_column_letter(table_start_col + 1)}{data_bar_range_start_row}:{get_column_letter(table_start_col + 1)}{data_bar_range_end_row}',
                                 Rule(type='dataBar', color=theme_colors["accent_1"], showValue=True))
    # Data bars for Calls Reached
    ws.conditional_formatting.add(f'{get_column_letter(table_start_col + 2)}{data_bar_range_start_row}:{get_column_letter(table_start_col + 2)}{data_bar_range_end_row}',
                                 Rule(type='dataBar', color=theme_colors["accent_1"], showValue=True))
    # Data bars for Deals Closed
    ws.conditional_formatting.add(f'{get_column_letter(table_start_col + 3)}{data_bar_range_start_row}:{get_column_letter(table_start_col + 3)}{data_bar_range_end_row}',
                                 Rule(type='dataBar', color=theme_colors["accent_2"], showValue=True))
    # Data bars for Deal Value
    ws.conditional_formatting.add(f'{get_column_letter(table_start_col + 4)}{data_bar_range_start_row}:{get_column_letter(table_start_col + 4)}{data_bar_range_end_row}',
                                 Rule(type='dataBar', color=theme_colors["accent_2"], showValue=True))

    # Conditional formatting to highlight a "selected" row (mocking slicer selection)
    selected_agent_name = "Evan" # For demonstration, this would dynamically come from a slicer
    highlight_range = f"{get_column_letter(table_start_col)}{data_bar_range_start_row}:{get_column_letter(table_start_col + 4)}{data_bar_range_end_row}"
    formula = f'=$B{data_bar_range_start_row}="{selected_agent_name}"' # Assumes name is in column B
    highlight_fill = PatternFill(start_color="FFFACD", end_color="FFFACD", fill_type="solid") # Light yellow highlight
    highlight_font = Font(color="FF0000", bold=True) # Red bold font
    ws.conditional_formatting.add(highlight_range, FormulaRule(formula=[formula], fill=highlight_fill, font=highlight_font))


    # --- Chart Area (Mocked data for openpyxl) ---
    # Dummy data for charts (would come from an 'Analysis' sheet in a real interactive dashboard)
    chart_data_cols = 12
    chart_data_header_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    chart_data_reach = [301, 311, 298, 307, 303, 305, 307, 301, 299, 306, 299, 306]
    chart_data_closed = [115, 118, 112, 110, 113, 111, 104, 98, 107, 109, 108, 107]
    chart_data_sales = [57863, 59230, 58127, 56084, 58261, 58580, 58654, 59025, 58654, 58137, 59137, 59137]
    chart_data_duration = [341, 343, 342, 345, 340, 339, 340, 343, 339, 344, 343, 342]
    chart_data_drop_rate = [0.049, 0.050, 0.049, 0.050, 0.050, 0.050, 0.049, 0.050, 0.050, 0.049, 0.049, 0.049]

    # Create a temporary 'Analysis' sheet for chart data sources
    analysis_ws = kwargs.get('wb').create_sheet("Analysis", 1)
    analysis_ws['A1'] = "Month"
    analysis_ws['B1'] = "Calls Reached"
    analysis_ws['C1'] = "Deals Closed"
    analysis_ws['D1'] = "Total Sales"
    analysis_ws['E1'] = "Avg Duration"
    analysis_ws['F1'] = "Drop Rate"

    for i in range(chart_data_cols):
        analysis_ws.cell(row=i+2, column=1).value = chart_data_header_months[i]
        analysis_ws.cell(row=i+2, column=2).value = chart_data_reach[i]
        analysis_ws.cell(row=i+2, column=3).value = chart_data_closed[i]
        analysis_ws.cell(row=i+2, column=4).value = chart_data_sales[i]
        analysis_ws.cell(row=i+2, column=5).value = chart_data_duration[i]
        analysis_ws.cell(row=i+2, column=6).value = chart_data_drop_rate[i]
        analysis_ws.cell(row=i+2, column=6).number_format = '0.00%' # Format drop rate as percentage

    # --- Chart 1: Sum of Calls Reached vs. Deals Closed ---
    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10
    chart1.title = "Sum of Calls Reached vs. Sum of Deals Closed"
    chart1.y_axis.title = "" # No vertical axis title
    chart1.x_axis.title = "" # No horizontal axis title
    chart1.overlap = 100 # Stacked
    chart1.gapWidth = 50 # Spacing

    ref_data_reach = Reference(analysis_ws, min_col=2, min_row=1, max_col=2, max_row=chart_data_cols+1)
    ref_data_closed = Reference(analysis_ws, min_col=3, min_row=1, max_col=3, max_row=chart_data_cols+1)
    ref_cats = Reference(analysis_ws, min_col=1, min_row=2, max_row=chart_data_cols+1)

    chart1.add_data(ref_data_reach, titles_from_data=True)
    chart1.add_data(ref_data_closed, titles_from_data=True)
    chart1.set_categories(ref_cats)

    # Styling
    s1 = chart1.series[0]
    s1.graphicalProperties.solidFill = theme_colors["chart_series_1"] # Gold
    s1.dLbls = s1.dLbls or chart1.dLbls # Ensure data labels object exists
    s1.dLbls.showVal = True
    s1.dLbls.showCatName = False
    s1.dLbls.showSerName = False
    s1.dLbls.pos = 'inEnd'
    s1.dLbls.tx.rich.p[0].r[0].rPr.kern = False # Ensure font is not kerned
    s1.dLbls.tx.rich.p[0].r[0].rPr.sz = 900 # Font size 9pt
    s1.dLbls.tx.rich.p[0].r[0].rPr.fill.solidFill.prstcl = 'white' # white color to be visible on dark

    s2 = chart1.series[1]
    s2.graphicalProperties.solidFill = theme_colors["chart_series_2"] # Purple
    s2.dLbls = s2.dLbls or chart1.dLbls
    s2.dLbls.showVal = True
    s2.dLbls.showCatName = False
    s2.dLbls.showSerName = False
    s2.dLbls.pos = 'inEnd'
    s2.dLbls.tx.rich.p[0].r[0].rPr.kern = False
    s2.dLbls.tx.rich.p[0].r[0].rPr.sz = 900
    s2.dLbls.tx.rich.p[0].r[0].rPr.fill.solidFill.prstcl = 'white' # white color

    chart1.width = 10 # Adjust chart size
    chart1.height = 7
    ws.add_chart(chart1, "J9") # Place chart

    # --- Chart 2: Total Sales ---
    chart2 = BarChart()
    chart2.type = "col"
    chart2.style = 10
    chart2.title = "Total Sales $"
    chart2.y_axis.scaling.min = 0 # Fixed vertical axis start
    chart2.y_axis.number_format = '$#,##0'
    
    ref_sales = Reference(analysis_ws, min_col=4, min_row=1, max_col=4, max_row=chart_data_cols+1)
    chart2.add_data(ref_sales, titles_from_data=True)
    chart2.set_categories(ref_cats)
    
    # Styling
    s3 = chart2.series[0]
    s3.graphicalProperties.solidFill = theme_colors["chart_series_2"] # Purple
    
    # Add Trendline
    trendline = LineChart()
    trendline.y_axis.axId = 200 # Unique axis ID
    trendline.y_axis.title = ""
    trendline.x_axis.title = ""
    ref_sales_trend = Reference(analysis_ws, min_col=4, min_row=1, max_col=4, max_row=chart_data_cols+1)
    trendline_series = trendline.add_data(ref_sales_trend, titles_from_data=True)[0]
    trendline_series.trendline = trendline_series.Trendline()
    trendline_series.trendline.dispEq = False
    trendline_series.trendline.dispRsq = False
    trendline_series.graphicalProperties.line.solidFill = theme_colors["chart_trendline"] # Yellow
    trendline_series.graphicalProperties.line.width = 25000 # 2pt
    trendline_series.graphicalProperties.line.dashStyle = 'sysDot' # Dotted line

    # Combine charts
    chart2.width = 10
    chart2.height = 7
    chart2.y_axis.majorGridlines = None # No gridlines
    chart2.legend.position = 't' # Top legend
    ws.add_chart(chart2, "Q9") # Place chart
    chart2.append(trendline) # Append trendline to main chart

    # --- Chart 3: Average Call Duration (seconds) ---
    chart3 = BarChart()
    chart3.type = "col"
    chart3.style = 10
    chart3.title = "Average Call Duration (Seconds)"
    chart3.y_axis.scaling.min = 0 # Fixed vertical axis start
    
    ref_duration = Reference(analysis_ws, min_col=5, min_row=1, max_col=5, max_row=chart_data_cols+1)
    chart3.add_data(ref_duration, titles_from_data=True)
    chart3.set_categories(ref_cats)

    # Styling
    s4 = chart3.series[0]
    s4.graphicalProperties.solidFill = theme_colors["accent_1"] # Gold
    
    chart3.width = 10
    chart3.height = 7
    chart3.y_axis.majorGridlines = None
    chart3.legend = None # No legend
    ws.add_chart(chart3, "J25")

    # --- Chart 4: Average Call Drop Rate % ---
    chart4 = AreaChart()
    chart4.style = 10
    chart4.title = "Average Call Drop Rate %"
    chart4.y_axis.scaling.min = 0 # Fixed vertical axis start
    chart4.y_axis.number_format = '0.00%' # Format axis as percentage

    ref_drop_rate = Reference(analysis_ws, min_col=6, min_row=1, max_col=6, max_row=chart_data_cols+1)
    chart4.add_data(ref_drop_rate, titles_from_data=True)
    chart4.set_categories(ref_cats)

    # Styling
    s5 = chart4.series[0]
    s5.graphicalProperties.solidFill = theme_colors["accent_1"] # Gold
    s5.graphicalProperties.gradientFill = s5.graphicalProperties.GradientFillProperties()
    s5.graphicalProperties.gradientFill.gradientStops.add(0, theme_colors["accent_1"])
    s5.graphicalProperties.gradientFill.gradientStops.add(50000, "FFFFFF") # Fading to white

    chart4.width = 10
    chart4.height = 7
    chart4.y_axis.majorGridlines = None
    chart4.legend = None # No legend
    ws.add_chart(chart4, "Q25")

    # --- Clean up / Final Touches ---
    # Hide gridlines on the dashboard sheet
    ws.sheet_view.showGridLines = False

    # Remove temporary Analysis sheet if created (for testing self-contained skill)
    # In a real app, Analysis sheet would persist.
    if 'wb' in kwargs and 'Analysis' in kwargs['wb'].sheetnames:
        kwargs['wb'].remove(kwargs['wb']['Analysis'])


# Example Usage (for testing the code)
if __name__ == "__main__":
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    
    # Pass the workbook to allow creating the 'Analysis' sheet
    render_sheet(ws, "Dashboard", title="Sales Dashboard", wb=wb) 
    
    # You might want to remove the default "Sheet" sheet if it's empty
    if "Sheet" in wb.sheetnames and len(wb["Sheet"].dimensions) == 0:
        wb.remove(wb["Sheet"])
    
    wb.save("interactive_sales_dashboard_static.xlsx")
    print("Static dashboard generated successfully as interactive_sales_dashboard_static.xlsx")
```