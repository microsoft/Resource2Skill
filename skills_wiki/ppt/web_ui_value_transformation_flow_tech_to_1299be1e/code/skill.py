import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls

def add_modern_shadow(shape, opacity=15, blur_pt=10, dist_pt=5, angle_deg=90):
    """
    Injects OpenXML to add a modern, soft drop shadow to a shape.
    This creates the "Web UI Card" effect.
    """
    spPr = shape.element.spPr
    
    # Calculate EMU values
    blur_emu = int(blur_pt * 12700)
    dist_emu = int(dist_pt * 12700)
    angle_fd = int(angle_deg * 60000)
    opacity_val = int(opacity * 1000)
    
    shadow_xml = f"""
    <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:outerShdw blurRad="{blur_emu}" dist="{dist_emu}" dir="{angle_fd}" algn="b" rotWithShape="0">
            <a:srgbClr val="000000">
                <a:alpha val="{opacity_val}"/>
            </a:srgbClr>
        </a:outerShdw>
    </a:effectLst>
    """
    effectLst = parse_xml(shadow_xml)
    spPr.append(effectLst)

def create_slide(
    output_pptx_path: str,
    title_text: str = "玩赚AI做PPT (Play & Earn with AI PPT)",
    subtitle_text: str = "From One-Click Generation to Commercial Monetization",
    input_text: str = "AI",
    output_text: str = "变现\n$",
    bg_color: tuple = (245, 247, 250),
    brand_blue: tuple = (13, 82, 214),
    brand_gold: tuple = (255, 171, 0),
    text_color: tuple = (30, 40, 50),
    **kwargs,
) -> str:
    
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # --- Background ---
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(*bg_color)
    bg.line.fill.background() # No line
    
    # --- Title & Subtitle ---
    title_box = slide.shapes.add_textbox(Inches(1), Inches(0.8), Inches(11.333), Inches(1))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(*text_color)
    
    sub_box = slide.shapes.add_textbox(Inches(1), Inches(1.8), Inches(11.333), Inches(0.5))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.font.size = Pt(20)
    p_sub.font.color.rgb = RGBColor(100, 110, 120)
    
    # --- Graphic Center Layout ---
    center_y = Inches(3.5)
    
    # 1. Left Node (The "AI" Folders/Stack)
    # Back Folder
    back_folder = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.5), center_y - Inches(0.8), Inches(2.5), Inches(2.5)
    )
    back_folder.fill.solid()
    back_folder.fill.fore_color.rgb = RGBColor(brand_blue[0], brand_blue[1], brand_blue[2])
    # Make it slightly darker or transparent for depth
    back_folder.line.fill.background()
    add_modern_shadow(back_folder, opacity=10)
    
    # Front Folder
    front_folder = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.8), center_y - Inches(0.5), Inches(2.5), Inches(2.5)
    )
    front_folder.fill.solid()
    front_folder.fill.fore_color.rgb = RGBColor(*brand_blue)
    front_folder.line.color.rgb = RGBColor(255, 255, 255)
    front_folder.line.width = Pt(3)
    add_modern_shadow(front_folder, opacity=20, blur_pt=15)
    
    # Front Folder Text
    tf_front = front_folder.text_frame
    tf_front.word_wrap = True
    p_front = tf_front.paragraphs[0]
    p_front.text = input_text
    p_front.alignment = PP_ALIGN.CENTER
    p_front.font.size = Pt(54)
    p_front.font.bold = True
    p_front.font.color.rgb = RGBColor(255, 255, 255)
    
    # 2. Connector (Arrow)
    arrow = slide.shapes.add_shape(
        MSO_SHAPE.RIGHT_ARROW, Inches(6.0), center_y + Inches(0.35), Inches(1.333), Inches(0.8)
    )
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = RGBColor(200, 210, 220)
    arrow.line.fill.background()
    
    # 3. Right Node (The Outcome/Monetization Screen)
    # Screen outer border
    screen_outer = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.0), center_y - Inches(1.0), Inches(3.5), Inches(3.0)
    )
    screen_outer.fill.solid()
    screen_outer.fill.fore_color.rgb = RGBColor(255, 255, 255)
    screen_outer.line.color.rgb = RGBColor(*brand_gold)
    screen_outer.line.width = Pt(4)
    add_modern_shadow(screen_outer, opacity=25, blur_pt=20, dist_pt=8)
    
    # Screen inner content area (The Gold focus)
    screen_inner = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.2), center_y - Inches(0.8), Inches(3.1), Inches(2.6)
    )
    screen_inner.fill.solid()
    screen_inner.fill.fore_color.rgb = RGBColor(*brand_gold)
    screen_inner.line.fill.background()
    
    # Screen Text
    tf_screen = screen_inner.text_frame
    tf_screen.word_wrap = True
    p_screen = tf_screen.paragraphs[0]
    p_screen.text = output_text
    p_screen.alignment = PP_ALIGN.CENTER
    p_screen.font.size = Pt(48)
    p_screen.font.bold = True
    p_screen.font.color.rgb = RGBColor(255, 255, 255)

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("ai_monetization_flow.pptx")
