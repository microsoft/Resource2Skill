from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_VERTICAL_ANCHOR
from pptx.enum.dml import MSO_THEME_COLOR

def create_slide(
    output_pptx_path: str,
    title_text: str = "Recycling Infrastructure KPI Dashboard - 2025",
    reporting_month: str = "March 2025",
    kpi_data: list = None
) -> str:
    """
    Creates a PPTX file with a Strategic KPI Performance Dashboard.

    Args:
        output_pptx_path: Path to save the generated PPTX file.
        title_text: The main title for the dashboard.
        reporting_month: The reporting month to display in the header.
        kpi_data: A list of dictionaries, each representing a KPI row.
                  If None, default sample data will be used.

    Returns:
        Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Define colors
    HEADER_FILL = RGBColor(98, 48, 48)
    SECTION_HEADER_FILL = RGBColor(148, 88, 88)
    COLUMN_HEADER_FILL = RGBColor(197, 150, 150)
    WHITE_TEXT = RGBColor(255, 255, 255)
    BLACK_TEXT = RGBColor(0, 0, 0)
    GREEN_ARROW = RGBColor(0, 176, 80)
    RED_ARROW = RGBColor(255, 0, 0)
    ZEBRA_FILL = RGBColor(242, 242, 242)

    # === Sample Data if not provided ===
    if kpi_data is None:
        kpi_data = [
            {"#": 1, "group": "Operations", "name": "Recycling Rate", "unit": "%", "type": "UTB", "mtd_actual": 125.0, "mtd_target": 120.0, "mtd_py": 118.0, "ytd_actual": 366.0, "ytd_target": 375.0, "ytd_py": 350.0},
            {"#": 2, "group": "Collection", "name": "Material Collected", "unit": "Tons", "type": "UTB", "mtd_actual": 98.0, "mtd_target": 105.0, "mtd_py": 95.0, "ytd_actual": 290.0, "ytd_target": 310.0, "ytd_py": 285.0},
            {"#": 3, "group": "Quality", "name": "Material Contamination", "unit": "%", "type": "LTB", "mtd_actual": 8.8, "mtd_target": 9.0, "mtd_py": 9.2, "ytd_actual": 26.0, "ytd_target": 27.0, "ytd_py": 28.0},
            {"#": 4, "group": "Safety", "name": "Safety Incidents", "unit": "Count", "type": "LTB", "mtd_actual": 1, "mtd_target": 0, "mtd_py": 2, "ytd_actual": 3, "ytd_target": 2, "ytd_py": 5},
            {"#": 5, "group": "Finance", "name": "Revenue per Ton", "unit": "USD", "type": "UTB", "mtd_actual": 127.6, "mtd_target": 125.0, "mtd_py": 122.0, "ytd_actual": 380.0, "ytd_target": 370.0, "ytd_py": 360.0},
        ]

    # === Header Section ===
    header_shape = slide.shapes.add_shape(1, Inches(0.5), Inches(0.5), Inches(12.333), Inches(0.5))
    header_shape.fill.solid()
    header_shape.fill.fore_color.rgb = HEADER_FILL
    header_shape.text = title_text
    header_shape.text_frame.paragraphs[0].font.color.rgb = WHITE_TEXT
    header_shape.text_frame.paragraphs[0].font.name = 'Arial Black'
    header_shape.text_frame.paragraphs[0].font.size = Pt(20)
    header_shape.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    header_shape.line.fill.background()

    month_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.1), Inches(2.0), Inches(0.3))
    month_box.text_frame.text = f"Select Month:  {reporting_month}"
    month_box.text_frame.paragraphs[0].font.name = 'Calibri'
    month_box.text_frame.paragraphs[0].font.size = Pt(12)
    
    # === Table Creation ===
    num_rows = len(kpi_data) + 3  # 3 header rows
    num_cols = 15
    table_shape = slide.shapes.add_table(num_rows, num_cols, Inches(0.5), Inches(1.5), Inches(12.333), Inches(0.5))
    tbl = table_shape.table

    # Define column widths
    col_widths = [0.4, 1.2, 2.0, 0.5, 0.5, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]
    for i, width in enumerate(col_widths):
        tbl.columns[i].width = Inches(width)

    # --- Helper for cell styling ---
    def style_cell(cell, text, font_size=10, bold=False, font_color=BLACK_TEXT, fill_color=None, align=PP_ALIGN.CENTER):
        cell.text = str(text)
        para = cell.text_frame.paragraphs[0]
        para.font.name = 'Calibri'
        para.font.size = Pt(font_size)
        para.font.bold = bold
        para.font.color.rgb = font_color
        para.alignment = align
        cell.vertical_anchor = MSO_VERTICAL_ANCHOR.MIDDLE
        if fill_color:
            cell.fill.solid()
            cell.fill.fore_color.rgb = fill_color

    # --- Populate Table Headers ---
    # Row 0: Main Sections
    style_cell(tbl.cell(0, 0), "KPI", 11, True, WHITE_TEXT, HEADER_FILL, PP_ALIGN.LEFT)
    tbl.cell(0,0).merge(tbl.cell(0,4)); tbl.cell(0,0).merge(tbl.cell(1,4)); tbl.cell(0,0).merge(tbl.cell(2,4))
    style_cell(tbl.cell(0, 5), "MTD", 12, True, WHITE_TEXT, SECTION_HEADER_FILL)
    tbl.cell(0,5).merge(tbl.cell(0,9)); tbl.cell(0,5).merge(tbl.cell(1,9))
    style_cell(tbl.cell(0, 10), "YTD", 12, True, WHITE_TEXT, SECTION_HEADER_FILL)
    tbl.cell(0,10).merge(tbl.cell(0,14)); tbl.cell(0,10).merge(tbl.cell(1,14))

    # Row 2: Column Headers
    kpi_headers = ["#", "KPI Group", "KPI Name", "Unit", "Type"]
    metric_headers = ["Actual", "Target", "Var %", "PY", "PY Var %"]
    for i, h in enumerate(kpi_headers):
        style_cell(tbl.cell(2, i), h, 10, True, WHITE_TEXT, COLUMN_HEADER_FILL, PP_ALIGN.LEFT if i in [1,2] else PP_ALIGN.CENTER)
    for i, h in enumerate(metric_headers * 2):
        style_cell(tbl.cell(2, 5 + i), h, 10, True, WHITE_TEXT, COLUMN_HEADER_FILL)

    # --- Helper for variance cell ---
    def style_variance_cell(cell, actual, benchmark, kpi_type):
        if benchmark is None or benchmark == 0:
            variance_pct_text = "N/A"
            arrow_char, font_color = "", BLACK_TEXT
        else:
            variance_pct = round((actual / benchmark) * 100)
            variance_pct_text = f"{variance_pct}%"
            is_positive = (actual >= benchmark) if kpi_type == 'UTB' else (actual <= benchmark)
            arrow_char, font_color = ("▲", GREEN_ARROW) if is_positive else ("▼", RED_ARROW)

        cell.text = f"{variance_pct_text} "
        p = cell.text_frame.paragraphs[0]
        p.font.name, p.font.size, p.font.color.rgb, p.alignment = 'Calibri', Pt(10), BLACK_TEXT, PP_ALIGN.CENTER
        
        run = p.add_run()
        run.text, run.font.name, run.font.size, run.font.color.rgb = arrow_char, 'Calibri', Pt(12), font_color
        cell.vertical_anchor = MSO_VERTICAL_ANCHOR.MIDDLE

    # --- Populate Data Rows ---
    for idx, data_row in enumerate(kpi_data):
        row_idx = idx + 3
        row_fill = ZEBRA_FILL if idx % 2 != 0 else None
        
        # KPI Info
        style_cell(tbl.cell(row_idx, 0), data_row["#"], fill_color=row_fill)
        style_cell(tbl.cell(row_idx, 1), data_row["group"], align=PP_ALIGN.LEFT, fill_color=row_fill)
        style_cell(tbl.cell(row_idx, 2), data_row["name"], align=PP_ALIGN.LEFT, fill_color=row_fill)
        style_cell(tbl.cell(row_idx, 3), data_row["unit"], fill_color=row_fill)
        style_cell(tbl.cell(row_idx, 4), data_row["type"], fill_color=row_fill)

        # MTD Data
        style_cell(tbl.cell(row_idx, 5), f'{data_row["mtd_actual"]:.1f}', align=PP_ALIGN.RIGHT, fill_color=row_fill)
        style_cell(tbl.cell(row_idx, 6), f'{data_row["mtd_target"]:.1f}', align=PP_ALIGN.RIGHT, fill_color=row_fill)
        style_variance_cell(tbl.cell(row_idx, 7), data_row["mtd_actual"], data_row["mtd_target"], data_row["type"])
        tbl.cell(row_idx, 7).fill.solid(); tbl.cell(row_idx, 7).fill.fore_color.rgb = row_fill or RGBColor(255,255,255)
        style_cell(tbl.cell(row_idx, 8), f'{data_row["mtd_py"]:.1f}', align=PP_ALIGN.RIGHT, fill_color=row_fill)
        style_variance_cell(tbl.cell(row_idx, 9), data_row["mtd_actual"], data_row["mtd_py"], data_row["type"])
        tbl.cell(row_idx, 9).fill.solid(); tbl.cell(row_idx, 9).fill.fore_color.rgb = row_fill or RGBColor(255,255,255)

        # YTD Data
        style_cell(tbl.cell(row_idx, 10), f'{data_row["ytd_actual"]:.1f}', align=PP_ALIGN.RIGHT, fill_color=row_fill)
        style_cell(tbl.cell(row_idx, 11), f'{data_row["ytd_target"]:.1f}', align=PP_ALIGN.RIGHT, fill_color=row_fill)
        style_variance_cell(tbl.cell(row_idx, 12), data_row["ytd_actual"], data_row["ytd_target"], data_row["type"])
        tbl.cell(row_idx, 12).fill.solid(); tbl.cell(row_idx, 12).fill.fore_color.rgb = row_fill or RGBColor(255,255,255)
        style_cell(tbl.cell(row_idx, 13), f'{data_row["ytd_py"]:.1f}', align=PP_ALIGN.RIGHT, fill_color=row_fill)
        style_variance_cell(tbl.cell(row_idx, 14), data_row["ytd_actual"], data_row["ytd_py"], data_row["type"])
        tbl.cell(row_idx, 14).fill.solid(); tbl.cell(row_idx, 14).fill.fore_color.rgb = row_fill or RGBColor(255,255,255)


    prs.save(output_pptx_path)
    return output_pptx_path
