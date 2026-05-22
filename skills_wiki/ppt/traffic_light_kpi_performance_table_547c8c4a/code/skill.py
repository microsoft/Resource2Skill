import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_slide(
    output_pptx_path: str,
    title_text: str = "Water Desalination KPI Dashboard - 2025",
    selected_month: str = "November 2025",
    kpi_data: list = None,
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with a Traffic Light KPI Performance Table.

    Args:
        output_pptx_path (str): The path to save the generated PPTX file.
        title_text (str): The main title for the dashboard.
        selected_month (str): The month to display in the header.
        kpi_data (list): A list of dictionaries, where each dictionary represents a KPI row.
                         If None, sample data is used. Each item must include a 'type' key:
                         'UTB' (Up is Better) or 'LTB' (Lower is Better).
                         Example:
                         [
                             {'group': 'Production', 'kpi': 'Freshwater Output', 'unit': 'M Gallons/D',
                              'mtd_actual': 136.0, 'mtd_target': 130.1, 'mtd_py': 136.2,
                              'ytd_actual': 1386.5, 'ytd_target': 1318.8, 'ytd_py': 1373.1, 'type': 'UTB'},
                             ...
                         ]

    Returns:
        str: The path to the saved PPTX file.
    """
    # --- 1. Data Setup ---
    if kpi_data is None:
        # Sample data mimicking the video
        kpi_data = [
            {'group': 'Production', 'kpi': 'Freshwater Output', 'unit': 'MGD', 'type': 'UTB', 'mtd_actual': 136.0, 'mtd_target': 130.1, 'mtd_py': 136.2, 'ytd_actual': 1386.5, 'ytd_target': 1318.8, 'ytd_py': 1373.1},
            {'group': 'Operations', 'kpi': 'Capacity Utilization', 'unit': '%', 'type': 'UTB', 'mtd_actual': 100.0, 'mtd_target': 105.0, 'mtd_py': 102.0, 'ytd_actual': 1018.6, 'ytd_target': 1096.6, 'ytd_py': 1039.6},
            {'group': 'Quality', 'kpi': 'Water Quality Index', 'unit': 'Score', 'type': 'UTB', 'mtd_actual': 95.8, 'mtd_target': 98.0, 'mtd_py': 96.2, 'ytd_actual': 979.7, 'ytd_target': 998.6, 'ytd_py': 982.6},
            {'group': 'Efficiency', 'kpi': 'Energy Consumption', 'unit': 'kWh/Gal', 'type': 'LTB', 'mtd_actual': 8.8, 'mtd_target': 8.3, 'mtd_py': 8.8, 'ytd_actual': 89.8, 'ytd_target': 85.1, 'ytd_py': 91.1},
            {'group': 'Maintenance', 'kpi': 'Uptime Rate', 'unit': '%', 'type': 'UTB', 'mtd_actual': 98.0, 'mtd_target': 99.0, 'mtd_py': 97.3, 'ytd_actual': 98.2, 'ytd_target': 99.1, 'ytd_py': 98.1},
            {'group': 'Safety', 'kpi': 'Safety Incidents', 'unit': 'Count', 'type': 'LTB', 'mtd_actual': 1, 'mtd_target': 0, 'mtd_py': 2, 'ytd_actual': 5, 'ytd_target': 2, 'ytd_py': 8},
        ]
    df = pd.DataFrame(kpi_data)

    # --- 2. Presentation Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor(245, 245, 250)

    # Define colors from the video
    COLOR_DARK_PURPLE = RGBColor(76, 36, 145)
    COLOR_LIGHT_PURPLE = RGBColor(221, 214, 237)
    COLOR_HEADER_BLUE = RGBColor(68, 114, 196)
    COLOR_GREEN = RGBColor(0, 176, 80)
    COLOR_RED = RGBColor(255, 0, 0)
    COLOR_GRAY = RGBColor(128, 128, 128)
    COLOR_WHITE = RGBColor(255, 255, 255)

    # --- 3. Slide Header ---
    header = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.2), Inches(0.2), prs.slide_width - Inches(0.4), Inches(0.5))
    header.fill.solid(); header.fill.fore_color.rgb = COLOR_DARK_PURPLE
    header.line.fill.background()
    p = header.text_frame.paragraphs[0]
    p.text = title_text
    p.font.color.rgb = COLOR_WHITE; p.font.bold = True; p.font.size = Pt(24)
    p.alignment = PP_ALIGN.CENTER

    month_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.8), Inches(3), Inches(0.3))
    p = month_box.text_frame.paragraphs[0]
    p.text = f"Selected Month: {selected_month}"
    p.font.size = Pt(12); p.font.bold = True

    # --- 4. Table Creation ---
    num_kpis = len(df)
    table_rows, table_cols = num_kpis + 2, 15
    table_shape = slide.shapes.add_table(table_rows, table_cols, Inches(0.3), Inches(1.3), Inches(12.7), Inches(0.4 * (num_kpis + 2)))
    table = table_shape.table

    widths = [1.2, 1.8, 0.6, 0.4, 0.6, 0.6, 0.3, 0.7, 0.6, 0.6, 0.6, 0.3, 0.7, 0.3, 0.7]
    for i, w in enumerate(widths):
        table.columns[i].width = Inches(w)

    # --- 5. Populate Table Headers ---
    table.cell(0, 4).merge(table.cell(0, 8))
    table.cell(0, 9).merge(table.cell(0, 14))

    for cell, text in [(table.cell(0, 4), 'MTD'), (table.cell(0, 9), 'YTD')]:
        cell.fill.solid(); cell.fill.fore_color.rgb = COLOR_LIGHT_PURPLE
        p = cell.text_frame.paragraphs[0]
        p.text = text; p.alignment = PP_ALIGN.CENTER; p.font.bold = True

    headers = ['KPI Group', 'KPI Name', 'Unit', 'Type', 'Actual', 'Target', '', 'Target vs Actual', 'PY', 'Actual', 'Target', '', 'Target vs Actual', '', 'PY vs Actual']
    for i, h in enumerate(headers):
        cell = table.cell(1, i)
        cell.fill.solid(); cell.fill.fore_color.rgb = COLOR_HEADER_BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h; p.font.color.rgb = COLOR_WHITE; p.font.bold = True
        p.font.size = Pt(10); p.alignment = PP_ALIGN.CENTER

    # --- 6. Populate Data and Apply Traffic Lights ---
    for i, data_row in df.iterrows():
        r_idx = i + 2
        # KPI Info
        table.cell(r_idx, 0).text = data_row['group']
        table.cell(r_idx, 1).text = data_row['kpi']
        table.cell(r_idx, 2).text = str(data_row['unit'])
        table.cell(r_idx, 3).text = str(data_row['type'])

        # MTD Data
        table.cell(r_idx, 4).text = f"{data_row['mtd_actual']:.1f}"
        table.cell(r_idx, 5).text = f"{data_row['mtd_target']:.1f}"
        table.cell(r_idx, 8).text = f"{data_row['mtd_py']:.1f}"
        mtd_perf_val = data_row['mtd_actual'] / data_row['mtd_target'] if data_row['mtd_target'] != 0 else 1
        table.cell(r_idx, 7).text = f"{mtd_perf_val:.0%}"

        is_good_mtd = (data_row['mtd_actual'] >= data_row['mtd_target']) if data_row['type'] == 'UTB' else (data_row['mtd_actual'] <= data_row['mtd_target'])
        mtd_icon_cell = table.cell(r_idx, 6)
        p = mtd_icon_cell.text_frame.paragraphs[0]; p.font.bold = True
        if abs(1 - mtd_perf_val) < 0.02: # Within 2% is neutral
            p.text = '▬'; p.font.color.rgb = COLOR_GRAY
        elif is_good_mtd:
            p.text = '▲'; p.font.color.rgb = COLOR_GREEN
        else:
            p.text = '▼'; p.font.color.rgb = COLOR_RED

        # YTD Data
        table.cell(r_idx, 9).text = f"{data_row['ytd_actual']:.1f}"
        table.cell(r_idx, 10).text = f"{data_row['ytd_target']:.1f}"
        ytd_perf_val = data_row['ytd_actual'] / data_row['ytd_target'] if data_row['ytd_target'] != 0 else 1
        table.cell(r_idx, 12).text = f"{ytd_perf_val:.0%}"
        ytd_py_perf_val = data_row['ytd_actual'] / data_row['ytd_py'] if data_row['ytd_py'] != 0 else 1
        table.cell(r_idx, 14).text = f"{ytd_py_perf_val:.0%}"

        is_good_ytd = (data_row['ytd_actual'] >= data_row['ytd_target']) if data_row['type'] == 'UTB' else (data_row['ytd_actual'] <= data_row['ytd_target'])
        ytd_icon_cell_target = table.cell(r_idx, 11)
        p = ytd_icon_cell_target.text_frame.paragraphs[0]; p.font.bold = True
        if abs(1 - ytd_perf_val) < 0.02:
            p.text = '▬'; p.font.color.rgb = COLOR_GRAY
        elif is_good_ytd:
            p.text = '▲'; p.font.color.rgb = COLOR_GREEN
        else:
            p.text = '▼'; p.font.color.rgb = COLOR_RED

        is_good_py = (data_row['ytd_actual'] >= data_row['ytd_py'])
        ytd_icon_cell_py = table.cell(r_idx, 13)
        p = ytd_icon_cell_py.text_frame.paragraphs[0]; p.font.bold = True
        if abs(1 - ytd_py_perf_val) < 0.02:
            p.text = '▬'; p.font.color.rgb = COLOR_GRAY
        elif is_good_py:
            p.text = '▲'; p.font.color.rgb = COLOR_GREEN
        else:
            p.text = '▼'; p.font.color.rgb = COLOR_RED

    # --- 7. Final Table Styling ---
    for row in table.rows:
        for cell in row.cells:
            cell.vertical_anchor = 'middle'
            for para in cell.text_frame.paragraphs:
                para.alignment = PP_ALIGN.CENTER
                if not para.font.bold: # Don't shrink headers
                    para.font.size = Pt(10)

    prs.save(output_pptx_path)
    return output_pptx_path

