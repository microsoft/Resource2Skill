```
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Sales Dashboard

*   **Tier**: sheet_shell
*   **Core Mechanism**: Constructs a visually coherent and interactive Excel dashboard within a single sheet. It leverages a structured layout using stylized merged cells, integrates common chart types (line, donut) with theme-aligned formatting, and displays key performance indicators (KPIs) linked to source data.
*   **Applicability**: Creating professional, interactive management dashboards for sales, marketing, operations, or any domain requiring a visual summary of performance metrics, trend analysis, and performance tracking against targets. Suitable for data analysis reports needing a clean, dynamic, and easy-to-read interface.

### 2. Structural Breakdown

-   **Data Layout**: Data is organized in a separate 'Inputs' sheet, with tables for KPIs (actual, target, % complete, remainder), monthly sales figures for multiple years, sales by country, and customer satisfaction scores. The dashboard sheet acts as a visual layer.
-   **Formula Logic**:
    -   **KPI Completion Percentages**: `Inputs!D7 = Inputs!D5/Inputs!D6` (for Sales), `Inputs!G7 = Inputs!G5/Inputs!G6` (for Profit), `Inputs!J7 = Inputs!J5/Inputs!J6` (for Customers). These drive the donut charts.
    -   **KPI Display Values**: Dashboard displays actual numerical values and associated donut charts for percentage completion. Numerical values for Sales, Profit, and #Customers are dynamically linked via cell references (e.g., `=Inputs!D5`) within text boxes (simulated by merged cells in this openpyxl example).
-   **Visual Design**:
    -   **Overall Background**: White.
    -   **Sidebar**: Column A is filled with `header_bg` color. Text placeholders for icons with `header_fg` color, hyperlinked for navigation.
    -   **Main Title Bar**: Large merged cell (B2:M4) formatted as a rounded rectangle. `primary_bg` fill, no border, mimicked shadow. Text in `text_color` font, bold, large size.
    -   **KPI Boxes**: Merged cells (e.g., B5:E8) formatted as rounded rectangles. `primary_bg` fill, no border, mimicked shadow. Titles in `text_color` font, bold.
    -   **Chart Boxes**: Merged cells (e.g., B10:H19 for sales trend) formatted as rounded rectangles. `primary_bg` fill, no border, mimicked shadow. Titles in `text_color` font, bold.
-   **Charts/Tables**:
    -   **Donut Charts**: Three charts (placed at D5, H5, L5) for Sales, Profit, and #Customers. Data from respective `% Complete` and `Remainder` cells. Doughnut hole size 65%. Segments colored with `accent1` (complete) and `secondary_bg` (remainder). No title, no legend. Percentage text dynamically shown via a merged cell placed within the donut.
    -   **Line Chart (Sales Trend)**: Placed at B12. Data from `Inputs!C21:D32` with categories from `B21:B32`. No title, legend at bottom. Y-axis min 180. Line 2021: `accent1`, circle markers (white fill, `accent1` border). Line 2022: `accent2`, circle markers (white fill, `accent2` border). No chart area fill or border.
    -   **Radar Chart & Map Chart**: Represented by merged cell placeholders due to `openpyxl`'s current limitations for direct creation and dynamic embedding of these specific chart types with all tutorial features.
-   **Theme Hooks**: `header_bg`, `header_fg`, `primary_bg`, `text_color`, `accent1`, `accent2`, `secondary_bg`, `transparent`.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, Reference, PieChart
from openpyxl.chart.series import DataPoint
from openpyxl.chart.label import DataLabelList
from openpyxl.utils import get_column_letter

# --- Helper Functions (normally imported from _helpers.py) ---
# Defined here for self-containment as per prompt requirements.

def load_palette(theme: str):
    # Default palette similar to 'corporate_blue' from the video
    palettes = {
        "corporate_blue": {
            'header_bg': '1F497D',  # Dark Blue
            'header_fg': 'FFFFFF',  # White
            'primary_bg': 'FFFFFF', # White
            'text_color': '000000', # Black for general text, or a dark grey
            'accent1': '1F497D',    # Dark Blue
            'accent2': 'FF0000',    # Red
            'secondary_bg': 'D9E1F2', # Lighter Blue for donut remainder
            'transparent': '00000000' # Alpha for transparency
        }
    }
    return palettes.get(theme, palettes["corporate_blue"])

def set_fill(color_hex: str):
    return PatternFill(start_color=color_hex, end_color=color_hex, fill_type="solid")

def set_font(color_hex: str, size: int = 11, bold: bool = False, name: str = 'Calibri', underline: str = None):
    return Font(name=name, size=size, bold=bold, color=color_hex, underline=underline)

def set_border(color_hex: str, style: str = 'thin'):
    side = Side(border_style=style, color=color_hex)
    return Border(left=side, right=side, top=side, bottom=side)

def create_styled_cell_shape(ws, top_left_cell: str, bottom_right_cell: str, text: str = "", font: Font = None, fill: PatternFill = None, border: Border = None, text_h_align='left', text_v_align='top', is_shadowed: bool = False):
    """
    Simulates a styled shape (like a rounded rectangle) by merging cells and applying formatting.
    Note: openpyxl doesn't directly support complex Drawing.Shape objects with shadows
    and text wrapping in a simple API way like Excel UI for this tier.
    Shadowing is a visual hint, not a direct openpyxl property for merged cells.
    """
    ws.merge_cells(f'{top_left_cell}:{bottom_right_cell}')
    merged_cell = ws[top_left_cell]
    merged_cell.value = text

    if font:
        merged_cell.font = font
    if fill:
        merged_cell.fill = fill
    if border:
        merged_cell.border = border

    merged_cell.alignment = Alignment(horizontal=text_h_align, vertical=text_v_align, wrap_text=True)
    # Cannot apply actual shadows to merged cells in openpyxl. is_shadowed is illustrative.

def create_text_box_like_cell(ws, cell_ref: str, text_or_link: str, font: Font = None, width: int = None, height: int = None, text_h_align='center', text_v_align='center'):
    """
    Simulates a textbox linked to a cell. Openpyxl does not dynamically link
    Drawing.Text objects to cells like Excel's formula bar feature.
    This creates a merged cell with the content.
    """
    start_col = openpyxl.utils.column_index_from_string(cell_ref[:-1])
    start_row = int(cell_ref[1:])
    
    # Define a default size for the textbox if not provided
    if width is None: width = 2
    if height is None: height = 1

    end_col_letter = get_column_letter(start_col + width -1)
    end_row = start_row + height -1

    merged_range = f"{cell_ref}:{end_col_letter}{end_row}"
    ws.merge_cells(merged_range)
    merged_cell = ws[cell_ref]

    # If it's a formula link, set it as a formula. Otherwise, set as text.
    if text_or_link.startswith('='):
        merged_cell.value = text_or_link
    else:
        merged_cell.value = text_or_link

    if font:
        merged_cell.font = font
    merged_cell.alignment = Alignment(horizontal=text_h_align, vertical=text_v_align)
    merged_cell.fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid") # White background
    merged_cell.border = Border(left=Side(), right=Side(), top=Side(), bottom=Side()) # No border
    return merged_cell # Return the merged cell for potential further styling


# --- Main Render Function ---
def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", data: dict = None) -> None:
    ws = wb.create_sheet(sheet_name)
    palette = load_palette(theme)

    # --- Setup Data Sheet (Inputs) ---
    if 'Inputs' not in wb.sheetnames:
        inputs_ws = wb.create_sheet('Inputs')
    else:
        inputs_ws = wb['Inputs']

    # Sample KPI Data
    inputs_ws['C4'] = 'Actual'
    inputs_ws['D4'] = 'Amount'
    inputs_ws['D5'] = 2544
    inputs_ws['C6'] = 'Target'
    inputs_ws['D6'] = 3000
    inputs_ws['C7'] = '=D5/D6'
    inputs_ws['C8'] = 'Remainder'
    inputs_ws['D8'] = '=1-D7'

    inputs_ws['F4'] = 'Actual'
    inputs_ws['G4'] = 'Amount'
    inputs_ws['G5'] = 890
    inputs_ws['F6'] = 'Target'
    inputs_ws['G6'] = 1000
    inputs_ws['F7'] = '=G5/G6'
    inputs_ws['F8'] = 'Remainder'
    inputs_ws['G8'] = '=1-G7'

    inputs_ws['I4'] = 'Actual'
    inputs_ws['J4'] = 'Amount'
    inputs_ws['J5'] = 87.0
    inputs_ws['I6'] = 'Target'
    inputs_ws['J6'] = 100.0
    inputs_ws['I7'] = '=J5/J6'
    inputs_ws['I8'] = 'Remainder'
    inputs_ws['J8'] = '=1-J7'

    # Format percentages
    inputs_ws['D7'].number_format = '0%'
    inputs_ws['D8'].number_format = '0%'
    inputs_ws['G7'].number_format = '0%'
    inputs_ws['G8'].number_format = '0%'
    inputs_ws['J7'].number_format = '0%'
    inputs_ws['J8'].number_format = '0%'

    # Sales Trend Data
    inputs_ws['B20'] = 'Figures in SM'
    inputs_ws['C20'] = '2021'
    inputs_ws['D20'] = '2022'
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data_2021 = [201.9, 204.2, 198.6, 199.2, 195.3, 192.4, 186.3, 199.2, 205.2, 210.6, 209.4, 212.8]
    data_2022 = [215.3, 217.6, 220.1, 206.4, 203.0, 200.6, 194.2, 200.6, 202.4, 216.6, 223.3, 225.8]
    for i, month in enumerate(months):
        inputs_ws[f'B{21+i}'] = month
        inputs_ws[f'C{21+i}'] = data_2021[i]
        inputs_ws[f'D{21+i}'] = data_2022[i]

    # Sales by Country Data (for Map Chart)
    inputs_ws['F20'] = 'Sales by count Figures in SA'
    countries = ['Argentina', 'Colombia', 'Brazil', 'Ecuador', 'Peru', 'Chile', 'Bolivia']
    sales_sa = [953.3, 453.2, 553.2, 445.3, 425.1, 253.6, 387.5]
    for i, country in enumerate(countries):
        inputs_ws[f'F{21+i}'] = country
        inputs_ws[f'G{21+i}'] = sales_sa[i]

    # Customer Satisfaction Data (for Radar Chart)
    inputs_ws['I12'] = 'Customer Satisfac'
    inputs_ws['J12'] = 'Score'
    factors = ['Speed (54%)', 'Quality (86%)', 'Hygiene (93%)', 'Service (53%)', 'Availability (95%)']
    scores = [0.54, 0.86, 0.93, 0.53, 0.95]
    for i, factor in enumerate(factors):
        inputs_ws[f'I{13+i}'] = factor
        inputs_ws[f'J{13+i}'] = scores[i]
    inputs_ws['J13'].number_format = '0%'
    inputs_ws['J14'].number_format = '0%'
    inputs_ws['J15'].number_format = '0%'
    inputs_ws['J16'].number_format = '0%'
    inputs_ws['J17'].number_format = '0%'
    
    # --- Dashboard Layout and Styling ---
    # Set default column widths for better visual spacing
    ws.column_dimensions['A'].width = 8 # Sidebar width
    for col_idx in range(2, 15): # Columns B to N for dashboard content
        ws.column_dimensions[get_column_letter(col_idx)].width = 9.5

    # Hide gridlines
    ws.sheet_view.showGridLines = False

    # Sidebar (Column A)
    for row in range(1, ws.max_row + 1):
        ws[f'A{row}'].fill = set_fill(palette['header_bg'])

    # Top Title Shape
    create_styled_cell_shape(ws, 'B2', 'I4',
        text=f"{title} South America 2022\nFigures in millions of USD",
        font=set_font(palette['text_color'], size=18, bold=True),
        fill=set_fill(palette['primary_bg']),
        border=set_border(palette['transparent']),
        text_h_align='left', text_v_align='center', is_shadowed=True
    )

    # KPI Shapes (Sales, Profit, Customers)
    kpi_shape_ranges = ['B5:E9', 'F5:I9', 'J5:M9']
    kpi_titles = ['Sales', 'Profit', '# of Customers']
    for i, kpi_range in enumerate(kpi_shape_ranges):
        create_styled_cell_shape(ws, kpi_range.split(':')[0], kpi_range.split(':')[1],
            text=kpi_titles[i],
            font=set_font(palette['text_color'], size=12, bold=True),
            fill=set_fill(palette['primary_bg']),
            border=set_border(palette['transparent']),
            text_h_align='left', text_v_align='top', is_shadowed=True
        )

    # Sales by Country Map Chart Area (Top right)
    create_styled_cell_shape(ws, 'J2', 'M4', # Adjusted range
        text='Sales by Country 2022',
        font=set_font(palette['text_color'], size=12, bold=True),
        fill=set_fill(palette['primary_bg']),
        border=set_border(palette['transparent']),
        text_h_align='left', text_v_align='top', is_shadowed=True
    )

    # Chart Shapes (Sales Trend, Customer Satisfaction)
    create_styled_cell_shape(ws, 'B10:I19', 'I19', # Sales Trend
        text='2021-2022 Sales Trend (in millions)',
        font=set_font(palette['text_color'], size=12, bold=True),
        fill=set_fill(palette['primary_bg']),
        border=set_border(palette['transparent']),
        text_h_align='left', text_v_align='top', is_shadowed=True
    )
    create_styled_cell_shape(ws, 'J10:M19', 'M19', # Customer Satisfaction
        text='Customer Satisfaction',
        font=set_font(palette['text_color'], size=12, bold=True),
        fill=set_fill(palette['primary_bg']),
        border=set_border(palette['transparent']),
        text_h_align='left', text_v_align='top', is_shadowed=True
    )

    # --- Visuals (Charts and KPIs) ---

    # KPI Actual Values (Text Boxes)
    kpi_value_cells = ['B7', 'F7', 'J7']
    kpi_value_links = ['=Inputs!D5', '=Inputs!G5', '=Inputs!J5']
    kpi_value_fonts = [set_font(palette['text_color'], size=16, bold=True),
                       set_font(palette['text_color'], size=16, bold=True),
                       set_font(palette['text_color'], size=16, bold=True)]
    kpi_value_num_formats = ['"$#,##0"', '"$#,##0"', '0.0']

    for i, cell_ref in enumerate(kpi_value_cells):
        merged_cell = create_text_box_like_cell(ws, cell_ref, kpi_value_links[i],
                                                 font=kpi_value_fonts[i], width=2, height=1,
                                                 text_h_align='center', text_v_align='center')
        merged_cell.number_format = kpi_value_num_formats[i]


    # Donut Charts for % Complete
    donut_data_ranges = ['D7:D8', 'G7:G8', 'J7:J8']
    donut_chart_anchors = ['D5', 'H5', 'L5'] # Position for the actual chart anchor
    for i, r_str in enumerate(donut_data_ranges):
        chart = PieChart()
        chart.type = "doughnut"
        chart.style = 10
        chart.title = None
        chart.width = 2.5
        chart.height = 2.5

        labels = Reference(inputs_ws, min_col=openpyxl.utils.column_index_from_string(r_str.split(':')[0][:-1]), min_row=int(r_str.split(':')[0][1:]), max_row=int(r_str.split(':')[1][1:]))
        data = Reference(inputs_ws, min_col=openpyxl.utils.column_index_from_string(r_str.split(':')[0][:-1]), min_row=int(r_str.split(':')[0][1:]), max_row=int(r_str.split(':')[1][1:]))
        series = openpyxl.chart.Series(data, labels=labels)
        chart.append(series)

        chart.series[0].d_lbls = DataLabelList()
        chart.series[0].d_lbls.showCatName = False
        chart.series[0].d_lbls.showVal = False
        chart.series[0].d_lbls.showPercent = False # Percentage will be in a textbox on top

        chart.series[0].doughnutHoleSize = 65

        colors = [palette['accent1'], palette['secondary_bg']]
        for idx, color_val in enumerate(colors):
            data_point = DataPoint(idx=idx)
            data_point.graphicalProperties.solidFill = color_val
            chart.series[0].dPt.append(data_point)

        chart.plot_area.spPr.noFill = True
        chart.border.noFill = True
        chart.fill.noFill = True
        ws.add_chart(chart, donut_chart_anchors[i])

        # Text box for percentage inside the donut
        # Calculate cell for dynamic text box: center of donut
        percent_cell_col = openpyxl.utils.column_index_from_string(donut_chart_anchors[i][:-1]) + 1
        percent_cell_row = int(donut_chart_anchors[i][1:]) + 2
        percent_text_cell_ref = get_column_letter(percent_cell_col) + str(percent_cell_row)

        create_text_box_like_cell(ws, percent_text_cell_ref, f"=Inputs!{r_str.split(':')[0]}",
                                   font=set_font(palette['text_color'], size=14, bold=True),
                                   width=1, height=1, text_h_align='center', text_v_align='center')
        ws[percent_text_cell_ref].number_format = '0%'


    # Line Chart (2021-2022 Sales Trend)
    line_chart = LineChart()
    line_chart.style = 10
    line_chart.title = None
    line_chart.legend.position = 'b' # Bottom legend
    line_chart.width = 7.5
    line_chart.height = 7.5

    cats = Reference(inputs_ws, min_col=2, min_row=21, max_row=32)
    data = Reference(inputs_ws, min_col=3, min_row=20, max_col=4, max_row=32)
    line_chart.add_data(data, titles_from_data=True)
    line_chart.set_categories(cats)

    line_chart.y_axis.scaling.min = 180
    line_chart.y_axis.title = None
    line_chart.x_axis.title = None

    # Line 2021 (blue)
    s1 = line_chart.series[0]
    s1.graphicalProperties.line.solidFill = palette['accent1']
    s1.graphicalProperties.line.width = 1.0 * 12700
    s1.marker.symbol = 'circle'
    s1.marker.size = 5
    s1.marker.graphicalProperties.solidFill = palette['primary_bg']
    s1.marker.graphicalProperties.ln.solidFill = palette['accent1']

    # Line 2022 (red)
    s2 = line_chart.series[1]
    s2.graphicalProperties.line.solidFill = palette['accent2']
    s2.graphicalProperties.line.width = 1.0 * 12700
    s2.marker.symbol = 'circle'
    s2.marker.size = 5
    s2.marker.graphicalProperties.solidFill = palette['primary_bg']
    s2.marker.graphicalProperties.ln.solidFill = palette['accent2']

    line_chart.plot_area.spPr.noFill = True
    line_chart.border.noFill = True
    line_chart.fill.noFill = True
    ws.add_chart(line_chart, "B12")

    # Radar Chart Placeholder
    create_styled_cell_shape(ws, 'K12', 'M18',
        text='Radar Chart Placeholder\n(Openpyxl Limitation)',
        font=set_font(palette['text_color'], size=10, name='Arial'),
        fill=set_fill(palette['primary_bg']),
        border=set_border(palette['transparent']),
        text_h_align='center', text_v_align='center'
    )

    # Map Chart Placeholder
    create_styled_cell_shape(ws, 'J4', 'M9',
        text='Map Chart Placeholder\n(Openpyxl Limitation)',
        font=set_font(palette['text_color'], size=10, name='Arial'),
        fill=set_fill(palette['primary_bg']),
        border=set_border(palette['transparent']),
        text_h_align='center', text_v_align='center'
    )

    # --- Sidebar Navigation (Simplified) ---
    # Contacts sheet for hyperlink
    if 'Contacts' not in wb.sheetnames:
        contacts_ws = wb.create_sheet('Contacts')
        contacts_ws['A1'] = "Contact List"
        contacts_ws.cell(row=1, column=1).font = set_font(palette['text_color'], size=14, bold=True)


    sidebar_icons = {
        'A1': ('M', 'yellow', f"#{sheet_name}!A1"), # McDonald's logo, linking to dashboard
        'A5': ('📊', palette['header_fg'], f"#{sheet_name}!A1"), # Dashboard
        'A7': ('📝', palette['header_fg'], "#Inputs!A1"), # Inputs
        'A9': ('📞', palette['header_fg'], "#Contacts!A1"), # Contacts
        'A11': ('❓', palette['header_fg'], "mailto:info@support.com") # Help/Email
    }

    for cell_ref, (icon_text, icon_color, hyperlink) in sidebar_icons.items():
        cell = ws[cell_ref]
        cell.value = icon_text
        cell.font = set_font(icon_color, size=16, bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center')
        if hyperlink:
            cell.hyperlink = hyperlink
            # For cell hyperlinks, openpyxl automatically styles them.

    # Final inputs sheet adjustments
    inputs_ws.sheet_view.showGridLines = False
    inputs_ws.column_dimensions['A'].width = 8
    inputs_ws.column_dimensions['B'].width = 15
    inputs_ws.column_dimensions['C'].width = 10
    inputs_ws.column_dimensions['D'].width = 15
    inputs_ws.column_dimensions['F'].width = 10
    inputs_ws.column_dimensions['G'].width = 15
    inputs_ws.column_dimensions['I'].width = 10
    inputs_ws.column_dimensions['J'].width = 15
    inputs_ws.column_dimensions['E'].width = 5
    inputs_ws.column_dimensions['H'].width = 5
    inputs_ws.column_dimensions['K'].width = 5

    # Contacts sheet adjustments
    contacts_ws.sheet_view.showGridLines = False
    contacts_ws.column_dimensions['A'].width = 15
    contacts_ws.column_dimensions['B'].width = 30
    contacts_ws.column_dimensions['C'].width = 40
    contacts_ws['A3'] = 'Country'
    contacts_ws['B3'] = 'General Manager'
    contacts_ws['C3'] = 'Email'
    contacts_data = [
        ('Argentina', 'Fernando Gonzalez', 'f.gonzalez@mcdonalds.com'),
        ('Colombia', 'Radamel Lopez', 'r.lopez@mcdonalds.com'),
        ('Brazil', 'Joao Silva', 'j.silva@mcdonalds.com'),
        ('Ecuador', 'Jaime Lomo', 'j.lomo@mcdonalds.com'),
        ('Peru', 'Samuel Armando', 's.armando@mcdonalds.com'),
        ('Chile', 'Alvaro Sanchez', 'a.sanchez@mcdonalds.com'),
        ('Bolivia', 'Angel Garcia', 'a.garcia@mcdonalds.com')
    ]
    for r_idx, row_data in enumerate(contacts_data):
        for c_idx, cell_value in enumerate(row_data):
            contacts_ws.cell(row=4+r_idx, column=1+c_idx).value = cell_value
            if c_idx == 2: # Apply hyperlink for email
                contacts_ws.cell(row=4+r_idx, column=1+c_idx).hyperlink = f"mailto:{cell_value}"
                contacts_ws.cell(row=4+r_idx, column=1+c_idx).font = set_font(palette['accent1'], size=11, underline='single') # Blue underline for links
```