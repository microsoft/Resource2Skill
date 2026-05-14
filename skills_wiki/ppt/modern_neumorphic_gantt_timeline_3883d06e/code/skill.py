import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml import parse_xml
from pptx.oxml.ns import qn

def add_inner_shadow(shape):
    """
    Injects DrawingML XML to add an inner shadow to a shape, creating a recessed look.
    """
    shadow_xml = """
    <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:innerShdw blurRad="80000" dist="40000" dir="5400000">
            <a:srgbClr val="000000">
                <a:alpha val="20000"/>
            </a:srgbClr>
        </a:innerShdw>
    </a:effectLst>
    """
    effectLst = parse_xml(shadow_xml)
    spPr = shape.element.spPr
    
    # Remove existing effectLst if it exists to avoid XML corruption
    for e in spPr.findall('.//a:effectLst', namespaces=spPr.nsmap):
        spPr.remove(e)
        
    spPr.append(effectLst)

def create_slide(
    output_pptx_path: str,
    title_text: str = "PROJECT TIMELINE - GANTT CHART",
    projects: list = None
) -> str:
    """
    Creates a PPTX file reproducing the Modern Neumorphic Gantt Timeline.
    """
    if projects is None:
        # Default mock data
        projects = [
            {"name": "Phase 1 Name", "start_month": 0, "duration": 2, "color": (244, 185, 66), "detail": "JAN - FEB"},
            {"name": "Phase 2 Name", "start_month": 2, "duration": 3, "color": (214, 88, 88), "detail": "MAR - MAY"},
            {"name": "Phase 3 Name", "start_month": 3, "duration": 4, "color": (153, 51, 85), "detail": "APR - JUL"},
            {"name": "Phase 4 Name", "start_month": 7, "duration": 4, "color": (46, 134, 171), "detail": "AUG - NOV"}
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
    
    # Colors
    bg_track_color = RGBColor(235, 240, 245) # Light grayish blue
    text_color_dark = RGBColor(50, 50, 50)
    text_color_light = RGBColor(120, 120, 120)

    # --- Title ---
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Century Gothic"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = text_color_dark
    p.alignment = PP_ALIGN.CENTER

    # --- Grid Math ---
    margin_left = Inches(1.5)
    margin_right = Inches(1.5)
    track_area_width = prs.slide_width - margin_left - margin_right
    total_months = 12
    month_width = track_area_width / total_months
    
    start_y = Inches(1.8)
    row_height = Inches(1.1)
    bar_height = Inches(0.45)

    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

    # --- Draw Month Headers (Vertical Text) ---
    for i, month in enumerate(months):
        x = margin_left + (i * month_width)
        y = start_y - Inches(0.8)
        
        txBox = slide.shapes.add_textbox(x, y, month_width, Inches(0.8))
        tf = txBox.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.text = month
        p.font.name = "Century Gothic"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = text_color_dark
        p.alignment = PP_ALIGN.CENTER
        
        # Make text vertical using lxml
        bodyPr = txBox.element.xpath('./p:txBody/a:bodyPr')[0]
        bodyPr.set('vert', 'eaVert') # Vertical text (East Asian style vertical, works well for standard letters too in this context, or 'vert270' for rotated)
        bodyPr.set('vert', 'vert270') # Rotate 270 degrees (bottom to top)

    # --- Draw Rows ---
    for i, proj in enumerate(projects):
        current_y = start_y + (i * row_height)
        
        # 1. Row Label
        lbl_box = slide.shapes.add_textbox(Inches(0.2), current_y - Inches(0.05), margin_left - Inches(0.3), bar_height)
        tf = lbl_box.text_frame
        p = tf.paragraphs[0]
        p.text = proj["name"]
        p.font.name = "Century Gothic"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = text_color_dark
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p.alignment = PP_ALIGN.RIGHT

        # 2. Background Track (Recessed)
        bg_track = slide.shapes.add_shape(
            5, # msoShapeRoundedRectangle
            margin_left, current_y, track_area_width, bar_height
        )
        bg_track.fill.solid()
        bg_track.fill.fore_color.rgb = bg_track_color
        bg_track.line.fill.background() # No line
        bg_track.adjustments[0].value = 0.5 # Force pure pill shape (fully rounded)
        add_inner_shadow(bg_track) # Apply lxml inner shadow

        # 3. Active Gantt Bar
        bar_left = margin_left + (proj["start_month"] * month_width)
        bar_width = proj["duration"] * month_width
        
        active_bar = slide.shapes.add_shape(
            5, # msoShapeRoundedRectangle
            bar_left, current_y, bar_width, bar_height
        )
        active_bar.fill.solid()
        active_bar.fill.fore_color.rgb = RGBColor(*proj["color"])
        active_bar.line.fill.background()
        active_bar.adjustments[0].value = 0.5 # Force pure pill shape
        
        # Add a subtle drop shadow to the active bar for popping out
        active_bar.shadow.inherit = False
        active_bar.shadow.visible = True
        active_bar.shadow.distance = Pt(3)
        active_bar.shadow.angle = 45
        active_bar.shadow.blur_radius = Pt(4)
        active_bar.shadow.alpha = 0.3

        # 4. Detail Text inside/on active bar
        # Create a tiny white pill container for the text to sit inside the colored bar
        detail_width = Inches(1.0)
        if bar_width > detail_width:
            detail_bg = slide.shapes.add_shape(
                5,
                bar_left + Inches(0.05), current_y + Inches(0.05), bar_width - Inches(0.1), bar_height - Inches(0.1)
            )
            detail_bg.fill.solid()
            detail_bg.fill.fore_color.rgb = RGBColor(255, 255, 255)
            detail_bg.fill.transparency = 0.8 # slightly transparent white overlay
            detail_bg.line.fill.background()
            detail_bg.adjustments[0].value = 0.5
            
            tf = detail_bg.text_frame
            p = tf.paragraphs[0]
            p.text = proj["detail"]
            p.font.name = "Century Gothic"
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255,255,255)
            p.alignment = PP_ALIGN.CENTER
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE

        # 5. Helper text to the right
        help_box = slide.shapes.add_textbox(
            bar_left + bar_width + Inches(0.1), current_y - Inches(0.05), Inches(2.5), bar_height
        )
        tf = help_box.text_frame
        p = tf.paragraphs[0]
        p.text = "This is your detail text column."
        p.font.name = "Century Gothic"
        p.font.size = Pt(9)
        p.font.color.rgb = text_color_light
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE

    prs.save(output_pptx_path)
    return output_pptx_path
