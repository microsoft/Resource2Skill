import os
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.oxml import OxmlElement
from pptx.oxml.ns import qn

def set_shape_transparency(shape, opacity_percent: float):
    """
    Injects transparency (alpha) into a shape's solid fill using lxml.
    opacity_percent: 0.0 (fully transparent) to 1.0 (fully opaque)
    """
    fill = shape.fill
    if fill.type != 1:  # 1 = SOLID
        return
    
    # Calculate alpha value (100000 = 100% opaque)
    alpha_val = int(opacity_percent * 100000)
    
    spPr = shape.element.spPr
    solidFill = spPr.find(qn('a:solidFill'))
    if solidFill is not None:
        srgbClr = solidFill.find(qn('a:srgbClr'))
        if srgbClr is not None:
            # Check if alpha already exists, if so update it, otherwise create
            alpha = srgbClr.find(qn('a:alpha'))
            if alpha is None:
                alpha = OxmlElement('a:alpha')
                srgbClr.append(alpha)
            alpha.set('val', str(alpha_val))

def add_polygon(slide, vertices, color: tuple, opacity: float = 1.0, has_border: bool = False):
    """
    Helper to draw a custom polygon using FreeformBuilder and apply color/opacity.
    Vertices is a list of (x, y) tuples in Inches.
    """
    builder = slide.shapes.build_freeform()
    # Start at first vertex
    builder.add_line_segments([ (Inches(x), Inches(y)) for x, y in vertices ], close=True)
    shape = builder.convert_to_shape()
    
    # Set Color
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(color[0], color[1], color[2])
    
    # Set Border
    if not has_border:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = RGBColor(255, 255, 255)
        shape.line.width = Pt(1.5)
        
    # Set Transparency
    if opacity < 1.0:
        set_shape_transparency(shape, opacity)
        
    return shape

def create_slide(
    output_pptx_path: str,
    title_text: str = "MAIN HEADLINE",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas porttitor congue massa. Fusce posuere, magna sed pulvinar ultricies, purus lectus malesuada libero, sit amet commodo magna eros quis urna.",
    bg_image_keyword: str = "city,architecture",
    theme_color_1: tuple = (21, 67, 118),  # Navy Blue
    theme_color_2: tuple = (0, 184, 159),  # Cyan
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Transparent Geometric Shard Overlay effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Background Image ===
    bg_img_path = "temp_bg.jpg"
    try:
        url = f"https://source.unsplash.com/1600x900/?{bg_image_keyword}"
        urllib.request.urlretrieve(url, bg_img_path)
        slide.shapes.add_picture(bg_img_path, 0, 0, width=Inches(13.333))
    except Exception:
        # Fallback to dark gray background if download fails
        bg = slide.shapes.add_shape(1, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(50, 50, 50)
        bg.line.fill.background()

    # === Layer 2: Geometric Shards (Transparent Overlays) ===
    # Shard 1: Large Base Triangle (Navy)
    add_polygon(slide, [(0, 0.5), (11.5, 4.5), (0, 6.0)], theme_color_1, opacity=0.85)
    
    # Shard 2: Intersecting Sub-Triangle (Navy)
    add_polygon(slide, [(1.5, -0.5), (12.0, 3.0), (3.0, 6.5)], theme_color_1, opacity=0.65)
    
    # Shard 3: Long angled stripe crossing (Navy)
    add_polygon(slide, [(5, 0), (7, 0), (0, 7), (-2, 7)], theme_color_1, opacity=0.50)
    
    # Shard 4: Bright Accent Triangle (Cyan)
    add_polygon(slide, [(8, 2.5), (14.0, 5.0), (7.5, 6.5)], theme_color_2, opacity=0.90)

    # === Layer 3: Solid White Diagonal Base Mask ===
    # Covers the bottom half of the slide for text readability
    add_polygon(slide, [(-1, 5.0), (14.5, 3.8), (14.5, 8.0), (-1, 8.0)], (255, 255, 255), opacity=1.0)

    # === Layer 4: Content & Typography ===
    
    # Main Headline
    tb_title = slide.shapes.add_textbox(Inches(4.0), Inches(5.0), Inches(5.3), Inches(0.8))
    tf_title = tb_title.text_frame
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(*theme_color_1)

    # Body Text
    tb_body = slide.shapes.add_textbox(Inches(4.0), Inches(5.8), Inches(7.0), Inches(1.5))
    tf_body = tb_body.text_frame
    tf_body.word_wrap = True
    p_body = tf_body.paragraphs[0]
    p_body.text = body_text
    p_body.font.size = Pt(14)
    p_body.font.color.rgb = RGBColor(100, 100, 100)

    # Year Accent Text (on the Cyan shard)
    tb_year = slide.shapes.add_textbox(Inches(10.5), Inches(3.8), Inches(2.0), Inches(0.8))
    p_year = tb_year.text_frame.paragraphs[0]
    p_year.text = "2024" # Example year
    p_year.font.size = Pt(40)
    p_year.font.bold = True
    p_year.font.color.rgb = RGBColor(255, 255, 255)

    # Circular Icon Placeholders (on Navy Shards)
    icon_spacing = 1.3
    start_x = 1.0
    for i in range(3):
        # Draw circle
        circle = slide.shapes.add_shape(
            9, # MSO_SHAPE.OVAL
            Inches(start_x + (i * icon_spacing)), Inches(3.2), Inches(0.6), Inches(0.6)
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = RGBColor(255, 255, 255)
        circle.line.fill.background()
        
        # Add tiny label under circle
        tb_lbl = slide.shapes.add_textbox(
            Inches(start_x + (i * icon_spacing) - 0.2), Inches(3.8), Inches(1.0), Inches(0.4)
        )
        p_lbl = tb_lbl.text_frame.paragraphs[0]
        p_lbl.text = "Type your\ntext here"
        p_lbl.font.size = Pt(10)
        p_lbl.font.color.rgb = RGBColor(255, 255, 255)
        p_lbl.alignment = 2 # center

    # Cleanup temp image
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution
# create_slide("shard_overlay_design.pptx")
