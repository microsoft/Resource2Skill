import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from lxml import etree

def create_slide(
    output_pptx_path: str,
    title_text: str = "Four stages of business assessment process",
    stages: list = None,
    **kwargs,
) -> str:
    """
    Creates a PPTX slide reproducing the 'Soft Focus Assessment Stages' visual effect.

    Args:
        output_pptx_path: The path to save the generated PPTX file.
        title_text: The main title for the slide.
        stages: A list of dictionaries, each representing a stage.
                Example: [{'title': 'Designing', 'points': ['Point 1', 'Point 2']}]

    Returns:
        The path to the saved PPTX file.
    """
    
    # --- Default Stage Data ---
    if stages is None:
        stages = [
            {'title': 'Designing', 'points': ['Pin point customer expectations.', 'Collect all relevant requirements.', 'Create strategical interface if required.'], 'icon': MSO_SHAPE.RECTANGLE},
            {'title': 'Finalizing Scope', 'points': ['Pin point process.', 'Target required improvements.', 'Discuss scope with key stakeholders.'], 'icon': MSO_SHAPE.GEAR_6},
            {'title': 'Building Use Case', 'points': ['Analyze and give assessment report.', 'Evaluate Proof of Concept (POC).'], 'icon': MSO_SHAPE.CUBE},
            {'title': 'Finalizing Client Agreement', 'points': ['Pin point customer expectations.', 'Collect all relevant requirements.', 'Create strategical interface if required.'], 'icon': MSO_SHAPE.DOCUMENT},
        ]

    # --- Presentation Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Helper function for lxml shadow injection ---
    def add_shadow_to_shape(shape):
        """Applies a soft outer shadow to a shape using lxml."""
        shape_xml = shape.element
        spPr = shape_xml.spPr
        
        effect_list = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
        
        outer_shadow = etree.SubElement(effect_list, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw',
                                        blurRad="101600", dist="12700", dir="2700000", algn="ctr", rotWithShape="0")
        
        srgb_clr = etree.SubElement(outer_shadow, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr', val="000000")
        etree.SubElement(srgb_clr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', val="20000")

    # === Layer 1: Background Generation with PIL ===
    width, height = int(prs.slide_width * 96), int(prs.slide_height * 96)
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    # Gradient background
    bg_start = (230, 222, 255)
    bg_end = (200, 192, 235)
    for i in range(height):
        r = int(bg_start[0] + (bg_end[0] - bg_start[0]) * (i / height))
        g = int(bg_start[1] + (bg_end[1] - bg_start[1]) * (i / height))
        b = int(bg_start[2] + (bg_end[2] - bg_start[2]) * (i / height))
        draw.line([(0, i), (width, i)], fill=(r, g, b))

    # Bokeh layer
    bokeh_layer = Image.new('RGBA', (width, height))
    bokeh_draw = ImageDraw.Draw(bokeh_layer)
    bokeh_colors = [(200, 210, 255, 128), (230, 220, 255, 150)]
    bokeh_positions = [
        (int(width*0.1), int(height*0.2), int(width*0.25)),
        (int(width*0.8), int(height*0.1), int(width*0.2)),
        (int(width*0.9), int(height*0.8), int(width*0.22)),
    ]
    for x, y, r in bokeh_positions:
        bokeh_draw.ellipse([(x-r, y-r), (x+r, y+r)], fill=bokeh_colors[bokeh_positions.index((x, y, r)) % 2])
        
    bokeh_layer = bokeh_layer.filter(ImageFilter.GaussianBlur(radius=width*0.08))
    img.paste(bokeh_layer, (0, 0), bokeh_layer)

    background_path = "temp_background.png"
    img.save(background_path)
    slide.background.fill.solid() # Must add a fill before a picture
    slide.background.fill.picture(background_path)
    os.remove(background_path)

    # === Layer 2: Content ===
    
    # Slide Title
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), prs.slide_width - Inches(1), Inches(0.75))
    title_tf = title_shape.text_frame
    p = title_tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Segoe UI"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(89, 79, 119)
    p.alignment = PP_ALIGN.CENTER
    title_tf.margin_bottom = Inches(0)

    # --- Stages Layout ---
    num_stages = len(stages)
    total_width = prs.slide_width - Inches(2)
    panel_width = Inches(2.7)
    panel_height = Inches(4.0)
    gap = (total_width - (num_stages * panel_width)) / (num_stages - 1) if num_stages > 1 else 0
    start_x = Inches(1)

    # Colors
    text_dark = RGBColor(89, 79, 119)
    text_light = RGBColor(120, 110, 150)
    accent_color = RGBColor(150, 130, 220)

    for i, stage in enumerate(stages):
        x = start_x + i * (panel_width + gap)
        
        # Icon Holder
        icon_holder_y = Inches(1.5)
        icon_size = Inches(0.8)
        holder = slide.shapes.add_shape(MSO_SHAPE.OVAL, x + (panel_width-icon_size)/2, icon_holder_y, icon_size, icon_size)
        holder.fill.solid()
        holder.fill.fore_color.rgb = RGBColor(230, 222, 255)
        holder.line.fill.solid()
        holder.line.fill.fore_color.rgb = RGBColor(255, 255, 255)
        holder.line.width = Pt(1.5)

        # Placeholder Icon
        icon_inset = Inches(0.2)
        icon = slide.shapes.add_shape(stage.get('icon', MSO_SHAPE.STAR_5_POINT), 
                                     x + (panel_width - icon_size) / 2 + icon_inset, 
                                     icon_holder_y + icon_inset, 
                                     icon_size - 2 * icon_inset, 
                                     icon_size - 2 * icon_inset)
        icon.fill.solid()
        icon.fill.fore_color.rgb = accent_color
        icon.line.fill.background()


        # Content Panel
        panel_y = icon_holder_y + icon_size - Inches(0.2)
        panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, panel_y, panel_width, panel_height)
        panel.adjustments[0] = 0.18 # Corner radius
        panel.fill.solid()
        panel.fill.fore_color.rgb = RGBColor(255, 255, 255)
        panel.line.fill.background()
        add_shadow_to_shape(panel)
        
        # Text inside panel
        tf = panel.text_frame
        tf.clear()
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.7) # Space for icon holder overlap
        tf.word_wrap = True

        p_title = tf.paragraphs[0]
        p_title.text = stage['title']
        p_title.font.name = "Segoe UI"
        p_title.font.size = Pt(16)
        p_title.font.bold = True
        p_title.font.color.rgb = text_dark
        p_title.alignment = PP_ALIGN.CENTER
        
        for point in stage['points']:
            p_bullet = tf.add_paragraph()
            p_bullet.text = point
            p_bullet.font.name = "Segoe UI"
            p_bullet.font.size = Pt(11)
            p_bullet.font.color.rgb = text_light
            p_bullet.level = 0
            p_bullet.space_before = Pt(8)

        # Number circle
        num_y = panel_y + panel_height + Inches(0.1)
        num_size = Inches(0.4)
        num_circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, x + (panel_width-num_size)/2, num_y, num_size, num_size)
        num_circle.fill.solid()
        num_circle.fill.fore_color.rgb = RGBColor(230, 222, 255)
        num_circle.line.fill.background()
        
        num_tf = num_circle.text_frame
        num_tf.clear()
        p_num = num_tf.paragraphs[0]
        p_num.text = f"0{i+1}"
        p_num.font.name = "Segoe UI"
        p_num.font.bold = True
        p_num.font.size = Pt(14)
        p_num.font.color.rgb = accent_color
        p_num.alignment = PP_ALIGN.CENTER
        num_tf.vertical_anchor = 3 # MSO_ANCHOR.MIDDLE

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# create_slide("assessment_stages_reproduction.pptx")
