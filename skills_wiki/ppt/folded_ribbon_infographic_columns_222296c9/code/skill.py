import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from lxml import etree

def apply_soft_shadow(shape):
    """
    Injects OpenXML to apply a soft outer drop shadow to a shape.
    """
    spPr = shape.element.spPr
    effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
    # blurRad is in EMUs (1 inch = 914400 EMUs). 150000 is a nice soft blur.
    # dist is the distance of the shadow.
    outerShdw = etree.SubElement(effectLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw',
                                 blurRad="150000", dist="30000", dir="5400000", algn="ctr", rotWithShape="0")
    srgbClr = etree.SubElement(outerShdw, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr', val="000000")
    # alpha val is a percentage out of 100000. 15000 = 15% opacity.
    etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', val="15000")

def darken_color(rgb, factor=0.7):
    """Returns a darker version of the given RGB tuple."""
    return tuple(max(0, int(c * factor)) for c in rgb)

def create_slide(
    output_pptx_path: str,
    title_text: str = "4 Rectangular Options",
    body_text: str = "",
    bg_palette: str = "none", 
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Folded Ribbon Infographic Columns visual effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide

    # Set Background Color (Light Gray)
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 245)

    # Configuration for the 4 columns
    colors = [
        (255, 192, 0),   # Yellow
        (0, 112, 192),   # Blue
        (0, 176, 80),    # Green
        (112, 48, 160)   # Purple
    ]
    
    titles = ["RESEARCH", "EXPERIENCE", "PLANNING", "EXECUTION"]
    icons = ["💡", "💼", "📄", "🎯"] # Unicode placeholders for icons
    
    # Dimensions & Positioning
    num_cards = 4
    card_w = Inches(2.2)
    card_h = Inches(4.5)
    margin_x = Inches(1.5)
    y_offset = Inches(1.5)
    
    # Calculate gap to distribute evenly
    total_cards_width = num_cards * card_w
    available_width = prs.slide_width - (2 * margin_x)
    gap = (available_width - total_cards_width) / (num_cards - 1)
    
    banner_overhang = Inches(0.2)
    banner_w = Inches(1.0)
    banner_h = Inches(0.5)

    for i in range(num_cards):
        card_x = margin_x + (i * (card_w + gap))
        
        # 1. Base Card (White Rectangle with Shadow)
        card = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, card_x, y_offset, card_w, card_h
        )
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(255, 255, 255)
        card.line.color.rgb = RGBColor(220, 220, 220)
        card.line.width = Pt(2)
        apply_soft_shadow(card)

        # 2. Folded Ribbon Triangle (Drawn before banner to sit behind it, but overlaps card)
        # Vertices: 
        # A: (card_x - overhang, bottom of banner)
        # B: (card_x, bottom of banner)
        # C: (card_x, bottom of banner + overhang down the card edge)
        banner_y = y_offset + Inches(0.4)
        banner_bottom = banner_y + banner_h
        
        builder = slide.shapes.build_freeform()
        builder.add_line_segments([
            (card_x - banner_overhang, banner_bottom),
            (card_x, banner_bottom),
            (card_x, banner_bottom + banner_overhang),
            (card_x - banner_overhang, banner_bottom) # close
        ], close=True)
        triangle = builder.convert_to_shape()
        
        dark_rgb = darken_color(colors[i], factor=0.65)
        triangle.fill.solid()
        triangle.fill.fore_color.rgb = RGBColor(*dark_rgb)
        triangle.line.fill.background() # No line

        # 3. Main Ribbon Banner
        banner = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, card_x - banner_overhang, banner_y, banner_w, banner_h
        )
        banner.fill.solid()
        banner.fill.fore_color.rgb = RGBColor(*colors[i])
        banner.line.fill.background()

        # Add Number to Banner
        txBox_num = slide.shapes.add_textbox(card_x - banner_overhang, banner_y, banner_w, banner_h)
        tf_num = txBox_num.text_frame
        tf_num.vertical_anchor = MSO_SHAPE.RECTANGLE
        p_num = tf_num.paragraphs[0]
        p_num.text = f"0{i+1}"
        p_num.alignment = PP_ALIGN.CENTER
        p_num.font.bold = True
        p_num.font.size = Pt(20)
        p_num.font.color.rgb = RGBColor(255, 255, 255)

        # 4. Card Content - Title
        txBox_title = slide.shapes.add_textbox(card_x, banner_bottom + Inches(0.2), card_w, Inches(0.4))
        tf_title = txBox_title.text_frame
        p_title = tf_title.paragraphs[0]
        p_title.text = titles[i]
        p_title.alignment = PP_ALIGN.CENTER
        p_title.font.bold = True
        p_title.font.size = Pt(14)
        p_title.font.color.rgb = RGBColor(50, 50, 50)

        # 5. Separator Line
        line_w = Inches(1.5)
        line_x = card_x + (card_w - line_w) / 2
        line_y = banner_bottom + Inches(0.7)
        sep_line = slide.shapes.add_shape(
            MSO_SHAPE.LINE, line_x, line_y, line_w, 0
        )
        sep_line.line.color.rgb = RGBColor(200, 200, 200)
        sep_line.line.width = Pt(1.5)

        # 6. Body Text
        txBox_body = slide.shapes.add_textbox(card_x + Inches(0.1), line_y + Inches(0.1), card_w - Inches(0.2), Inches(1.5))
        tf_body = txBox_body.text_frame
        tf_body.word_wrap = True
        p_body = tf_body.paragraphs[0]
        p_body.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas porttitor congue massa."
        p_body.alignment = PP_ALIGN.CENTER
        p_body.font.size = Pt(10)
        p_body.font.color.rgb = RGBColor(100, 100, 100)

        # 7. Bottom Icon Placeholder
        txBox_icon = slide.shapes.add_textbox(card_x, y_offset + card_h - Inches(0.8), card_w, Inches(0.6))
        tf_icon = txBox_icon.text_frame
        p_icon = tf_icon.paragraphs[0]
        p_icon.text = icons[i]
        p_icon.alignment = PP_ALIGN.CENTER
        p_icon.font.size = Pt(32)

    prs.save(output_pptx_path)
    return output_pptx_path
