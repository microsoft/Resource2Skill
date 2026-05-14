def create_slide(
    output_pptx_path: str,
    project_name: str = "Project Butterfly",
    report_date: str = "August 2nd",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the One-Page Executive Project Status Dashboard.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.enum.shapes import MSO_SHAPE

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Colors
    HEADER_BG = RGBColor(33, 89, 104)     # Dark Teal
    HEADER_TXT = RGBColor(255, 255, 255)
    TEXT_MAIN = RGBColor(30, 30, 30)
    STATUS_GREEN = RGBColor(0, 176, 80)
    STATUS_YELLOW = RGBColor(255, 192, 0)
    STATUS_RED = RGBColor(255, 0, 0)
    BG_LIGHT_GRAY = RGBColor(242, 242, 242)

    # Helper function to format table cells
    def format_cell(cell, text, bold=False, align=PP_ALIGN.LEFT, font_size=11, bg_color=None, text_color=TEXT_MAIN):
        cell.text = text
        for paragraph in cell.text_frame.paragraphs:
            paragraph.alignment = align
            for run in paragraph.runs:
                run.font.size = Pt(font_size)
                run.font.bold = bold
                run.font.color.rgb = text_color
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = Inches(0.1)
        cell.margin_right = Inches(0.1)
        cell.margin_top = Inches(0.05)
        cell.margin_bottom = Inches(0.05)
        if bg_color:
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_color

    # === 1. Top Header Banner ===
    header = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.8))
    header.fill.solid()
    header.fill.fore_color.rgb = HEADER_BG
    header.line.fill.background()
    
    tf = header.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run = p.add_run()
    run.text = f"{project_name} Monthly Status Update -- {report_date}"
    run.font.size = Pt(22)
    run.font.bold = True
    run.font.color.rgb = HEADER_TXT
    header.text_frame.margin_left = Inches(0.5)

    # === 2. Project Summary Section ===
    # Section Title
    summary_title = slide.shapes.add_textbox(Inches(0.5), Inches(1.0), Inches(5), Inches(0.4))
    p = summary_title.text_frame.paragraphs[0]
    p.text = "Project Summary"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN

    # Scope Statement
    scope_lbl = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(6), Inches(0.3))
    p = scope_lbl.text_frame.paragraphs[0]
    p.text = "Scope Statement:"
    p.font.size = Pt(12)
    p.font.bold = True

    scope_body = slide.shapes.add_textbox(Inches(0.5), Inches(1.8), Inches(6.5), Inches(1.0))
    p = scope_body.text_frame.paragraphs[0]
    p.text = "To implement the new future state security center with focus on streamlining people activities and implementing technology to support the new ways of working by end of Q4."
    p.font.size = Pt(11)
    scope_body.text_frame.word_wrap = True

    # Priority Matrix Table
    matrix_title = slide.shapes.add_textbox(Inches(7.5), Inches(1.0), Inches(5), Inches(0.4))
    p = matrix_title.text_frame.paragraphs[0]
    p.text = "Project Priority Matrix"
    p.font.size = Pt(14)
    p.font.bold = True

    rows, cols = 4, 4
    matrix_table_shape = slide.shapes.add_table(rows, cols, Inches(7.5), Inches(1.5), Inches(5.33), Inches(1.2))
    matrix_table = matrix_table_shape.table
    
    # Set matrix column widths
    matrix_table.columns[0].width = Inches(1.7)
    matrix_table.columns[1].width = Inches(1.21)
    matrix_table.columns[2].width = Inches(1.21)
    matrix_table.columns[3].width = Inches(1.21)

    # Populate Matrix
    matrix_data = [
        [("Priority Matrix", True, PP_ALIGN.LEFT), ("Scope", True, PP_ALIGN.CENTER), ("Time", True, PP_ALIGN.CENTER), ("Budget", True, PP_ALIGN.CENTER)],
        [("Constraint", False, PP_ALIGN.LEFT), ("", False, PP_ALIGN.CENTER), ("1", True, PP_ALIGN.CENTER), ("", False, PP_ALIGN.CENTER)],
        [("Optimize", False, PP_ALIGN.LEFT), ("2", True, PP_ALIGN.CENTER), ("", False, PP_ALIGN.CENTER), ("", False, PP_ALIGN.CENTER)],
        [("Accept", False, PP_ALIGN.LEFT), ("", False, PP_ALIGN.CENTER), ("", False, PP_ALIGN.CENTER), ("3", True, PP_ALIGN.CENTER)]
    ]

    for r_idx, row in enumerate(matrix_data):
        for c_idx, cell_data in enumerate(row):
            text, is_bold, align = cell_data
            bg = BG_LIGHT_GRAY if r_idx == 0 else None
            txt_clr = HEADER_BG if (r_idx > 0 and text != "Constraint" and text != "Optimize" and text != "Accept") else TEXT_MAIN
            format_cell(matrix_table.cell(r_idx, c_idx), text, bold=is_bold, align=align, bg_color=bg, text_color=txt_clr)

    # === 3. Overall Status Section ===
    status_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(3.0), Inches(12.333), Inches(0.6))
    status_box.fill.solid()
    status_box.fill.fore_color.rgb = BG_LIGHT_GRAY
    status_box.line.fill.background()

    tf = status_box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    
    run1 = p.add_run()
    run1.text = f"Overall Project Status as of {report_date}: Project is "
    run1.font.size = Pt(14)
    run1.font.bold = True
    run1.font.color.rgb = TEXT_MAIN
    
    run2 = p.add_run()
    run2.text = "GREEN"
    run2.font.size = Pt(14)
    run2.font.bold = True
    run2.font.color.rgb = STATUS_GREEN

    run3 = p.add_run()
    run3.text = " and on track"
    run3.font.size = Pt(14)
    run3.font.bold = True
    run3.font.color.rgb = TEXT_MAIN

    # Legend text below status
    legend_txt = slide.shapes.add_textbox(Inches(0.5), Inches(3.6), Inches(12.333), Inches(0.3))
    p = legend_txt.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "GREEN = ON TRACK  |  YELLOW = POTENTIAL RISK  |  RED = ISSUES"
    p.font.size = Pt(10)
    p.font.color.rgb = RGBColor(100, 100, 100)

    # === 4. Deliverables Status Table ===
    deliv_title = slide.shapes.add_textbox(Inches(0.5), Inches(4.0), Inches(6), Inches(0.4))
    p = deliv_title.text_frame.paragraphs[0]
    p.text = f"Project Deliverable Status - as of {report_date}"
    p.font.size = Pt(16)
    p.font.bold = True

    deliv_rows, deliv_cols = 5, 4
    deliv_table_shape = slide.shapes.add_table(deliv_rows, deliv_cols, Inches(0.5), Inches(4.5), Inches(12.333), Inches(2.5))
    deliv_table = deliv_table_shape.table

    # Set column widths
    deliv_table.columns[0].width = Inches(2.0)
    deliv_table.columns[1].width = Inches(3.5)
    deliv_table.columns[2].width = Inches(1.5)
    deliv_table.columns[3].width = Inches(5.333)

    # Deliverables Data
    deliv_data = [
        # Headers
        [("Deliverable", True, PP_ALIGN.LEFT, BG_LIGHT_GRAY, TEXT_MAIN), 
         ("Definition", True, PP_ALIGN.LEFT, BG_LIGHT_GRAY, TEXT_MAIN), 
         ("Status", True, PP_ALIGN.CENTER, BG_LIGHT_GRAY, TEXT_MAIN), 
         ("Comments", True, PP_ALIGN.LEFT, BG_LIGHT_GRAY, TEXT_MAIN)],
        
        # Row 1
        [("Upgrade of Computer Hardware", False, PP_ALIGN.LEFT, None, TEXT_MAIN),
         ("Upgrading current models and software application", False, PP_ALIGN.LEFT, None, TEXT_MAIN),
         ("GREEN", True, PP_ALIGN.CENTER, STATUS_GREEN, HEADER_TXT),
         (f"As of {report_date} - everything on track and items ordered.", False, PP_ALIGN.LEFT, None, TEXT_MAIN)],
        
        # Row 2
        [("Upgrade of Furniture", False, PP_ALIGN.LEFT, None, TEXT_MAIN),
         ("Upgrading furniture to be more ergonomic and team interaction friendly", False, PP_ALIGN.LEFT, None, TEXT_MAIN),
         ("YELLOW", True, PP_ALIGN.CENTER, STATUS_YELLOW, TEXT_MAIN),
         (f"As of {report_date} - having issue with acquiring original design configuration. Working with supplier to find alternatives.", False, PP_ALIGN.LEFT, None, TEXT_MAIN)],
        
        # Row 3
        [("Resources", False, PP_ALIGN.LEFT, None, TEXT_MAIN),
         ("Find and hire new candidates with identified skill set and experiences", False, PP_ALIGN.LEFT, None, TEXT_MAIN),
         ("RED", True, PP_ALIGN.CENTER, STATUS_RED, HEADER_TXT),
         (f"As of {report_date} - having a difficult time finding qualified resources. Team is revisiting requirements and StC approval will be needed.", False, PP_ALIGN.LEFT, None, TEXT_MAIN)],
        
        # Row 4
        [("Training Execution", False, PP_ALIGN.LEFT, None, TEXT_MAIN),
         ("Training all new hires and existing employees on new layout and technology", False, PP_ALIGN.LEFT, None, TEXT_MAIN),
         ("GREEN", True, PP_ALIGN.CENTER, STATUS_GREEN, HEADER_TXT),
         (f"As of {report_date} - deliverable hasn't started yet.", False, PP_ALIGN.LEFT, None, TEXT_MAIN)]
    ]

    for r_idx, row in enumerate(deliv_data):
        for c_idx, cell_data in enumerate(row):
            text, is_bold, align, bg_color, txt_color = cell_data
            format_cell(deliv_table.cell(r_idx, c_idx), text, bold=is_bold, align=align, bg_color=bg_color, text_color=txt_color)

    prs.save(output_pptx_path)
    return output_pptx_path
