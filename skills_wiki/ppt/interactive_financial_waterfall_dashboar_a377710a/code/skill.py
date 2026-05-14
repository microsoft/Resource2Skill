import os
from pptx import Presentation
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR

def create_slide(
    output_pptx_path: str,
    cor_value: int = 400,
    sales_exp_value: int = 250,
    **kwargs,
) -> str:
    """
    Creates a static PowerPoint slide reproducing the Financial Waterfall Dashboard.

    This function generates a single slide containing a Profit & Loss table and a
    corresponding waterfall chart based on the provided input values for
    Cost of Revenue (CoR) and Sales Expenses.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        cor_value: The value for Cost of Revenue.
        sales_exp_value: The value for Sales Expenses.

    Returns:
        The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)

    # --- P&L Calculations ---
    revenue = 2000
    ga_expense = 300
    gross_profit = revenue - cor_value
    operating_profit = gross_profit - sales_exp_value - ga_expense

    pnl_data = [
        ("Revenue", revenue),
        ("CoR", cor_value),
        ("Gross Profit", gross_profit),
        ("Sales Expenses", sales_exp_value),
        ("G&A", ga_expense),
        ("Operating Profit", operating_profit),
    ]
    
    expense_accounts = ["CoR", "Sales Expenses", "G&A"]

    # --- 1. Create P&L Table ---
    rows, cols = 7, 3
    left, top, width, height = Inches(3.5), Inches(1.5), Inches(4), Inches(3)
    table = slide.shapes.add_table(rows, cols, left, top, width, height).table
    
    # Set headers
    table.cell(0, 0).text = "Profit & Loss Account"
    table.cell(0, 1).text = "Amount"
    table.cell(0, 2).text = "% to Revenue"

    # Populate table and apply formatting
    for i, (account, amount) in enumerate(pnl_data, 1):
        table.cell(i, 0).text = account
        table.cell(i, 1).text = f"{amount:,}"
        
        # Calculate and format percentage
        if revenue > 0:
            percent = amount / revenue
            table.cell(i, 2).text = f"{percent:.0%}"
        else:
            table.cell(i, 2).text = "N/A"

        # Apply conditional formatting-like fill
        if account in expense_accounts:
            fill = table.cell(i, 2).fill
            fill.solid()
            fill.fore_color.rgb = RGBColor(255, 192, 0) # Gold/Orange
    
    # Style table text
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.text_frame.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(14)
                    run.font.name = 'Calibri'
                    if cell.row_idx == 0:
                        run.font.bold = True

    # --- 2. Create Waterfall Chart ---
    chart_data = ChartData()
    chart_data.categories = ['Revenue', 'CoR', 'Gross Profit', 'Sales Expenses', 'G&A', 'Operating Profit']
    
    # Use negative values for decreases and None for subtotals to be calculated
    series_values = (revenue, -cor_value, None, -sales_exp_value, -ga_expense, None)
    chart_data.add_series('P&L', series_values)

    x, y, cx, cy = Inches(7.5), Inches(1.0), Inches(5.5), Inches(5.5)
    chart = slide.shapes.add_chart(XL_CHART_TYPE.WATERFALL, x, y, cx, cy, chart_data).chart

    # Set subtotal points
    plot = chart.plots[0]
    plot.series[0].points[2].is_subtotal = True  # Gross Profit
    plot.series[0].points[5].is_subtotal = True  # Operating Profit

    # --- 3. Style the Chart ---
    chart.has_legend = False
    chart.chart_title.text_frame.text = "Financial Performance"
    chart.chart_title.text_frame.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    # Style plot area
    plot_format = chart.plot_area.format
    plot_format.fill.solid()
    plot_format.fill.fore_color.rgb = RGBColor(82, 82, 82) # Dark Gray

    # Style axes
    category_axis = chart.category_axis
    category_axis.tick_labels.font.color.rgb = RGBColor(255, 255, 255)
    category_axis.format.line.color.rgb = RGBColor(255, 255, 255)

    value_axis = chart.value_axis
    value_axis.tick_labels.font.color.rgb = RGBColor(255, 255, 255)
    value_axis.has_major_gridlines = False
    value_axis.format.line.color.rgb = RGBColor(255, 255, 255)

    # Style data labels
    plot.has_data_labels = True
    data_labels = plot.data_labels
    data_labels.font.size = Pt(10)
    data_labels.font.color.rgb = RGBColor(255, 255, 255)
    data_labels.number_format = '#,##0'

    # Style bars
    plot.show_connector_lines = True
    if plot.connector_lines:
        plot.connector_lines.format.line.color.rgb = RGBColor(192, 192, 192)

    # Set colors for up/down bars
    up_bars = plot.up_bars
    up_bars.format.fill.solid()
    up_bars.format.fill.fore_color.rgb = RGBColor(0, 176, 80) # Green

    down_bars = plot.down_bars
    down_bars.format.fill.solid()
    down_bars.format.fill.fore_color.rgb = RGBColor(255, 0, 0) # Red

    prs.save(output_pptx_path)
    return output_pptx_path

if __name__ == '__main__':
    # Example usage:
    output_path = "financial_dashboard.pptx"
    create_slide(output_path, cor_value=650, sales_exp_value=350)
    print(f"Dashboard slide saved to {output_path}")
    # To view the generated file on Windows
    if os.name == 'nt':
        os.startfile(output_path)
