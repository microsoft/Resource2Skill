from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import PieChart, LineChart, RadarChart, Reference
from openpyxl.drawing.shapes import Shape, ShapeReference
from openpyxl.drawing.text import Paragraph, ParagraphProperties, CharacterProperties, RichText
from openpyxl.utils.units import pixels_to_EMU
from openpyxl.worksheet.hyperlink import Hyperlink

def render_dashboard_sheet(wb, sheet_name: str, *, title: str, figures_in_millions_of_usd_text: str, theme: str = "corporate_blue", inputs_sheet_name: str = "Inputs", contacts_sheet_name: str = "Contacts") -> None:
    # Helper to load theme colors
    def load_theme_colors(theme_name):
        themes = {
            "corporate_blue": {
                "header_bg": "FF2E4057", "header_fg": "FFFFFFFF", "accent_primary": "FF4F81BD",
                "accent_secondary_light": "FFDDEBF7", "accent_warning": "FFD9534F",
                "text_main": "FF2E4057", "text_light": "FF808080", "shadow_color": "FF808080"
            },
            # Add other themes here if needed
        }
        return themes.get(theme_name, themes["corporate_blue"])

    colors = load_theme_colors(theme)

    # Create or get the dashboard sheet
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # Set up column A for the sidebar
    ws.column_dimensions['A'].width = 8
    for row_num in range(1, 50): # Extend sidebar down
        ws[f'A{row_num}'].fill = PatternFill(start_color=colors["header_bg"], end_color=colors["header_bg"], fill_type="solid")

    # Add hyperlinked icons (placeholders for images)
    icon_rows = [1, 5, 8, 11, 14, 17]
    icon_links = [
        ("Dashboard", sheet_name, None),
        ("Presentation", sheet_name, None), # Placeholder for PPT icon
        ("Data Grid", inputs_sheet_name, None),
        ("Contacts", contacts_sheet_name, None),
        ("Email", None, "mailto:info@support.com"),
        ("Help", None, "https://example.com/help")
    ]

    for i, (icon_text, sheet_target, email_target) in enumerate(icon_links):
        row = icon_rows[i]
        cell = ws[f'A{row}']
        cell.value = "" # Text placeholder for now, actual icons would be images
        # Add shape placeholders for icons if we can't use real images easily
        icon_shape = Shape(ShapeReference.presetShapeDefinitions['roundRect'])
        icon_shape.width = pixels_to_EMU(40)
        icon_shape.height = pixels_to_EMU(40)
        icon_shape.left = pixels_to_EMU(10)
        icon_shape.top = pixels_to_EMU(15 + (row-1)*15) # Approximate vertical placement
        icon_shape.fill = PatternFill(start_color=colors["header_fg"], end_color=colors["header_fg"], fill_type="solid")
        icon_shape.noFill = False
        icon_shape.ln = None # No outline

        # Add hyperlink to the shape
        if sheet_target:
            link_ref = f"'{sheet_target}'!A1"
        elif email_target:
            link_ref = email_target
        else:
            link_ref = "" # No link if neither is provided

        if link_ref:
            # openpyxl doesn't directly hyperlink shapes. A common workaround is to link a cell *under* the shape.
            # For this example, we'll just add comment to represent it or skip for simplicity in `openpyxl`.
            # For a proper interactive dashboard, VBA or custom XML modification might be needed for shape hyperlinks.
            # Here, we'll just create simple cells with text for the icon for demonstration.
            ws[f'A{row}'].value = icon_text[0] # Just first letter as placeholder text
            ws[f'A{row}'].font = Font(color=colors["header_fg"], bold=True)
            ws[f'A{row}'].alignment = Alignment(horizontal='center', vertical='center')
            if link_ref:
                ws[f'A{row}'].hyperlink = Hyperlink(ref=link_ref, tooltip=f"Go to {icon_text}")
                ws[f'A{row}'].font = Font(color=colors["header_fg"], underline="single")


    # Define common shape styles
    shape_fill = PatternFill(start_color="FFFFFFFF", end_color="FFFFFFFF", fill_type="solid")
    shape_border = Side(style=None) # No border
    shape_shadow_color = PatternFill(start_color=colors["shadow_color"], end_color=colors["shadow_color"], fill_type="solid")

    # Helper to add a rounded rectangle shape (Simplified)
    def add_rounded_rect(ws_target, anchor_cell, width_cols, height_rows, title_text, subtitle_text=None):
        # Calculate rough pixel dimensions for placement
        start_col_letter = anchor_cell[0]
        start_row_num = int(anchor_cell[1:])
        
        # In openpyxl, shapes are anchored by top-left cell. We approximate pixel sizes.
        # A more precise implementation would use client anchor and pixel calculations.
        # For simplicity, we create a merged cell region with formatting.
        end_col_letter = chr(ord(start_col_letter) + width_cols - 1)
        end_row_num = start_row_num + height_rows - 1
        
        ws_target.merge_cells(f"{start_col_letter}{start_row_num}:{end_col_letter}{end_row_num}")
        merged_cell = ws_target[f"{start_col_letter}{start_row_num}"]
        
        merged_cell.fill = shape_fill
        merged_cell.border = Border(left=shape_border, right=shape_border, top=shape_border, bottom=shape_border)
        # No direct shadow effect on merged cells without custom XML.
        # We'll use formatting to mimic the rounded rectangle feel.
        # Set text inside
        if title_text:
            merged_cell.value = title_text
            merged_cell.font = Font(color=colors["text_main"], bold=True, size=14)
            merged_cell.alignment = Alignment(horizontal='center', vertical='top', wrapText=True)
            if subtitle_text:
                merged_cell.value += f"\n{subtitle_text}"
                merged_cell.font = Font(color=colors["text_main"], bold=True, size=14) # Title font
                ws_target[f"{start_col_letter}{start_row_num+1}"].value = subtitle_text
                ws_target[f"{start_col_letter}{start_row_num+1}"].font = Font(color=colors["text_light"], size=9)
                ws_target[f"{start_col_letter}{start_row_num+1}"].alignment = Alignment(horizontal='center', vertical='top')

        return merged_cell, f"{start_col_letter}{start_row_num}", f"{end_col_letter}{end_row_num}"

    # --- Dashboard Structure (using merged cells + formatting) ---

    # Main Title Area
    main_title_cell, _, _ = add_rounded_rect(ws, 'B2', 12, 3, title, figures_in_millions_of_usd_text)
    main_title_cell.font = Font(color=colors["text_main"], bold=True, size=18)
    ws['B3'].font = Font(color=colors["text_light"], size=10) # Subtitle font

    # KPI Boxes (Sales, Profit, Customers)
    kpi1_cell, kpi1_start, _ = add_rounded_rect(ws, 'B6', 4, 6, "Sales")
    kpi2_cell, kpi2_start, _ = add_rounded_rect(ws, 'F6', 4, 6, "Profit")
    kpi3_cell, kpi3_start, _ = add_rounded_rect(ws, 'J6', 4, 6, "# of Customers")

    # Charts Areas
    chart1_cell, chart1_start, _ = add_rounded_rect(ws, 'B13', 8, 12, "2021-2022 Sales Trend (in millions)")
    chart2_cell, chart2_start, _ = add_rounded_rect(ws, 'J13', 4, 6, "Customer Satisfaction")
    map_chart_cell, map_chart_start, _ = add_rounded_rect(ws, 'J20', 4, 5, "Sales by Country 2022")

    # --- KPI Values and Donut Charts ---
    kpi_details = [
        {'title': 'Sales', 'amount_cell': 'D5', 'percent_cell': 'D7', 'target_cell': 'D6', 'kpi_cell_ref': kpi1_start},
        {'title': 'Profit', 'amount_cell': 'G5', 'percent_cell': 'G7', 'target_cell': 'G6', 'kpi_cell_ref': kpi2_start},
        {'title': 'Customers', 'amount_cell': 'J5', 'percent_cell': 'J7', 'target_cell': 'J6', 'kpi_cell_ref': kpi3_start},
    ]

    for kpi in kpi_details:
        # Add dynamic number (e.g., $2,544)
        amount_text_box_cell = ws.cell(row=int(kpi['kpi_cell_ref'][1:]) + 1, column=ord(kpi['kpi_cell_ref'][0]) - ord('A') + 1)
        amount_text_box_cell.value = f"='{inputs_sheet_name}'!{kpi['amount_cell']}"
        amount_text_box_cell.font = Font(color=colors["text_main"], bold=True, size=16)
        amount_text_box_cell.alignment = Alignment(horizontal='left', vertical='center')

        # Create Donut Chart
        donut = PieChart()
        donut.type = "doughnut"
        donut.style = 10 # A default style
        donut.title = kpi['title'] # Not shown, but good practice
        donut.dountHoleSize = 65

        labels = Reference(wb[inputs_sheet_name], min_col=ord(kpi['percent_cell'][0])-ord('A')+1, min_row=int(kpi['percent_cell'][1:])-1, max_row=int(kpi['percent_cell'][1:])+1) # Labels for complete/remainder
        data = Reference(wb[inputs_sheet_name], min_col=ord(kpi['percent_cell'][0])-ord('A')+1, min_row=int(kpi['percent_cell'][1:]), max_row=int(kpi['percent_cell'][1:])+1)
        
        donut.add_data(data, titles_from_data=False)
        donut.set_categories(labels)
        
        # Apply specific colors to slices
        from openpyxl.chart.series import DataPoint
        s1_dp1 = DataPoint(idx=0)
        s1_dp1.graphicalProperties.solidFill = colors["accent_primary"]
        s1_dp2 = DataPoint(idx=1)
        s1_dp2.graphicalProperties.solidFill = colors["accent_secondary_light"]
        donut.series[0].dPts = [s1_dp1, s1_dp2]

        donut.width = 3.5 # inches
        donut.height = 3.5 # inches
        donut.border = None
        donut.fill = None
        
        # Position the donut chart
        donut_anchor_col = chr(ord(kpi['kpi_cell_ref'][0]) + 1)
        donut_anchor_row = int(kpi['kpi_cell_ref'][1:]) + 1
        ws.add_chart(donut, f"{donut_anchor_col}{donut_anchor_row}")

        # Add dynamic percentage in center of donut (text box)
        percent_text_box_cell = ws.cell(row=donut_anchor_row + 1, column=ord(donut_anchor_col) - ord('A') + 1)
        percent_text_box_cell.value = f"='{inputs_sheet_name}'!{kpi['percent_cell']}"
        percent_text_box_cell.number_format = '0%'
        percent_text_box_cell.font = Font(color=colors["text_main"], bold=True, size=11)
        percent_text_box_cell.alignment = Alignment(horizontal='center', vertical='center')

    # --- Chart Visuals (Line, Radar, Map) ---
    # Line Chart
    line_chart = LineChart()
    line_chart.title = None # Title handled by shape
    line_chart.style = 10
    line_chart.y_axis.title = None
    line_chart.x_axis.title = None
    line_chart.legend = None # Legend handled visually by labels

    # Set axis min/max as shown in video (180 to 250)
    line_chart.y_axis.scaling.min = 180
    line_chart.y_axis.scaling.max = 250

    # Data for line chart
    line_labels = Reference(wb[inputs_sheet_name], min_col=2, min_row=20, max_row=31) # Jan-Dec
    line_data = Reference(wb[inputs_sheet_name], min_col=3, min_row=19, max_col=4, max_row=31) # 2021-2022 Sales

    line_chart.add_data(line_data, titles_from_data=True)
    line_chart.set_categories(line_labels)
    
    # Format line chart series
    s1 = line_chart.series[0] # 2021
    s1.graphicalProperties.line.solidFill = colors["accent_primary"] # Dark Blue
    s1.marker.symbol = "circle"
    s1.marker.size = 5
    s1.marker.graphicalProperties.solidFill = "FFFFFFFF" # White fill
    s1.marker.graphicalProperties.line.solidFill = colors["accent_primary"] # Dark Blue border

    s2 = line_chart.series[1] # 2022
    s2.graphicalProperties.line.solidFill = colors["accent_warning"] # Red
    s2.marker.symbol = "circle"
    s2.marker.size = 5
    s2.marker.graphicalProperties.solidFill = "FFFFFFFF" # White fill
    s2.marker.graphicalProperties.line.solidFill = colors["accent_warning"] # Red border

    line_chart.width = 8.5 # inches
    line_chart.height = 5.5 # inches
    line_chart.border = None
    line_chart.fill = None
    ws.add_chart(line_chart, chart1_start)

    # Radar Chart
    radar_chart = RadarChart()
    radar_chart.type = "radar"
    radar_chart.style = 10
    radar_chart.title = None
    radar_chart.legend = None

    radar_labels = Reference(wb[inputs_sheet_name], min_col=11, min_row=12, max_row=16) # Speed, Quality...
    radar_data = Reference(wb[inputs_sheet_name], min_col=12, min_row=11, max_col=12, max_row=16) # Scores

    radar_chart.add_data(radar_data, titles_from_data=False)
    radar_chart.set_categories(radar_labels)

    s1 = radar_chart.series[0]
    s1.graphicalProperties.line.solidFill = colors["accent_primary"] # Dark Blue
    s1.marker.symbol = "circle"
    s1.marker.size = 5
    s1.marker.graphicalProperties.solidFill = "FFFFFFFF" # White fill
    s1.marker.graphicalProperties.line.solidFill = colors["accent_primary"] # Dark Blue border

    radar_chart.width = 4.5 # inches
    radar_chart.height = 4.5 # inches
    radar_chart.border = None
    radar_chart.fill = None
    ws.add_chart(radar_chart, chart2_start)

    # Map Chart (Placeholder using a basic shape as openpyxl does not support geo maps)
    # A more advanced implementation might use a static image or a different chart type.
    map_placeholder_shape = Shape(ShapeReference.presetShapeDefinitions['rectangularCallout']) # Or 'rectangle'
    map_placeholder_shape.width = pixels_to_EMU(300)
    map_placeholder_shape.height = pixels_to_EMU(200)
    
    # Position the map placeholder
    # openpyxl uses internal units for positioning, precise placement might require trial and error.
    # We will approximate based on column/row widths.
    map_shape_anchor_cell = ws.cell(row=int(map_chart_start[1:]) + 1, column=ord(map_chart_start[0]) - ord('A') + 1)
    # Add a simple text to indicate it's a map
    map_placeholder_shape.text = Paragraph(pPr=ParagraphProperties(defRPr=CharacterProperties(latin="Sales Map Placeholder")),
                                            lvl=[RichText(t="Sales Map Placeholder")])
    map_placeholder_shape.text.rPr.solidFill = colors["text_light"]

    # No direct adding shape to a cell in openpyxl, but to the worksheet.
    # For simplicity, we just add text to the cell, implying the chart.
    ws.cell(row=int(map_chart_start[1:]) + 1, column=ord(map_chart_start[0]) - ord('A') + 1).value = "Sales Map Placeholder"
    ws.cell(row=int(map_chart_start[1:]) + 1, column=ord(map_chart_start[0]) - ord('A') + 1).alignment = Alignment(horizontal='center', vertical='center', wrapText=True)
    ws.cell(row=int(map_chart_start[1:]) + 1, column=ord(map_chart_start[0]) - ord('A') + 1).font = Font(color=colors["text_light"], size=10)

    # Note: For real map charts, you'd export a static image from Excel's map feature and insert it.
    # ws.add_image(Image('path/to/south_america_map.png'), map_chart_start)
