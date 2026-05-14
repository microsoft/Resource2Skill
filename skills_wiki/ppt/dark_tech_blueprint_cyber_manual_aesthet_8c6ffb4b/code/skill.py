import os
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from PIL import Image, ImageDraw, ImageFilter

def add_shadow_via_lxml(shape, color_hex="000000", blur_rad=100000, dist=50000, dir=2700000, alpha=50000):
    """
    Injects an Outer Shadow effect into a shape using lxml.
    Blur/Dist are in EMUs (1 pt = 12700 EMUs).
    Alpha is in thousandths of a percent (50000 = 50%).
    """
    spPr = shape.element.spPr
    effectLst = etree.SubElement(spPr, "{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst")
    outerShdw = etree.SubElement(effectLst, "{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw")
    outerShdw.set("blurRad", str(blur_rad))
    outerShdw.set("dist", str(dist))
    outerShdw.set("dir", str(dir))
    outerShdw.set("algn", "ctr")
    
    srgbClr = etree.SubElement(outerShdw, "{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr")
    srgbClr.set("val", color_hex)
    etree.SubElement(srgbClr, "{http://schemas.openxmlformats.org/drawingml/2006/main}alpha").set("val", str(alpha))

def create_slide(
    output_pptx_path: str,
    title_text: str = "准 备 规 范",
    subtitle_text: str = "P R E P A R I N G   S P E C I F I C A T I O N",
    tech_tags: list = ["防", "御", "打", "造", "完", "美", "幻", "灯", "片"],
    bg_color: tuple = (20, 24, 28),
    accent_color: tuple = (44, 181, 195), # Cyber Cyan
    **kwargs,
) -> str:
    """
    Creates a PPTX slide recreating the 'Dark Tech Blueprint' cyber-manual aesthetic.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Generate & Apply Ambient Glow Background via PIL ===
    bg_img_path = "temp_cyber_bg.png"
    img_w, img_h = 1920, 1080
    bg_img = Image.new('RGB', (img_w, img_h), bg_color)
    draw = ImageDraw.Draw(bg_img)
    
    # Draw a soft cyan glow in the center-bottom
    glow_radius = 600
    glow_color = accent_color
    draw.ellipse(
        [img_w/2 - glow_radius, img_h*0.7 - glow_radius, 
         img_w/2 + glow_radius, img_h*0.7 + glow_radius],
        fill=glow_color
    )
    # Apply heavy blur to create ambient light
    bg_img = bg_img.filter(ImageFilter.GaussianBlur(radius=250))
    # Darken it slightly by blending with base color
    dark_overlay = Image.new('RGB', (img_w, img_h), bg_color)
    bg_img = Image.blend(bg_img, dark_overlay, alpha=0.6)
    
    bg_img.save(bg_img_path)
    slide.shapes.add_picture(bg_img_path, 0, 0, prs.slide_width, prs.slide_height)

    # === Layer 2: Tech UI Elements & Structural Ribbons ===
    
    # Top-Left "Manual" UI Badge
    badge_l, badge_t, badge_w, badge_h = Inches(1), Inches(0.8), Inches(2.2), Inches(0.4)
    badge = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, badge_l, badge_t, badge_w, badge_h)
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(255, 255, 255)
    badge.line.color.rgb = RGBColor(*accent_color)
    badge.line.width = Pt(1.5)
    
    tf_badge = badge.text_frame
    tf_badge.text = "工作型PPT // 品控手册"
    tf_badge.paragraphs[0].font.size = Pt(12)
    tf_badge.paragraphs[0].font.bold = True
    tf_badge.paragraphs[0].font.color.rgb = RGBColor(*bg_color) # Dark text
    tf_badge.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Main Cyan Center Ribbon
    ribbon_w = Inches(10)
    ribbon_h = Inches(1.8)
    ribbon_l = (prs.slide_width - ribbon_w) / 2
    ribbon_t = Inches(2.8)
    
    ribbon = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, ribbon_l, ribbon_t, ribbon_w, ribbon_h)
    ribbon.fill.solid()
    ribbon.fill.fore_color.rgb = RGBColor(*accent_color)
    ribbon.line.fill.background() # No line
    # Add shadow via lxml to make it pop from the background
    add_shadow_via_lxml(ribbon, color_hex="000000", blur_rad=250000, dist=80000, alpha=60000)

    # Sub-ribbon (Dark frame underneath/around)
    frame_w = Inches(10.2)
    frame_h = Inches(2.4)
    frame_l = (prs.slide_width - frame_w) / 2
    frame_t = Inches(2.5)
    frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, frame_l, frame_t, frame_w, frame_h)
    frame.fill.background() # Transparent
    frame.line.color.rgb = RGBColor(*accent_color)
    frame.line.width = Pt(1)
    # Move frame to back, then ribbon to back, then bg to back to fix Z-order
    # But since we just added them linearly: bg -> badge -> ribbon -> frame. 
    # We want frame BEHIND ribbon. We can just re-insert or sort Z-order. 
    # Let's adjust order via code: frame is transparent so it can sit on top of ribbon slightly.

    # === Layer 3: Typography ===
    
    # Main Title on the Ribbon
    title_box = slide.shapes.add_textbox(ribbon_l, ribbon_t + Inches(0.2), ribbon_w, Inches(1))
    tf_title = title_box.text_frame
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(64)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(20, 24, 28) # Dark text on cyan
    p_title.alignment = PP_ALIGN.CENTER

    # Subtitle on the Ribbon
    sub_box = slide.shapes.add_textbox(ribbon_l, ribbon_t + Inches(1.2), ribbon_w, Inches(0.5))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = RGBColor(20, 24, 28)
    p_sub.alignment = PP_ALIGN.CENTER
    
    # Bottom Tech Tags (Slash Separated)
    tag_string = "  /  ".join(tech_tags)
    tag_box = slide.shapes.add_textbox(0, frame_t + frame_h + Inches(0.3), prs.slide_width, Inches(0.5))
    tf_tag = tag_box.text_frame
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = tag_string
    p_tag.font.size = Pt(12)
    p_tag.font.color.rgb = RGBColor(*accent_color)
    p_tag.alignment = PP_ALIGN.CENTER
    
    # Large Watermark Text (Bottom Right)
    wm_box = slide.shapes.add_textbox(Inches(8), Inches(5.5), Inches(4.5), Inches(1.5))
    tf_wm = wm_box.text_frame
    p_wm = tf_wm.paragraphs[0]
    p_wm.text = "FPT"
    p_wm.font.size = Pt(120)
    p_wm.font.bold = True
    # Semi-transparent pure cyan for watermark
    p_wm.font.color.rgb = RGBColor(*accent_color)
    # LXML trick: To make text transparent in python-pptx natively is hard, so we fake it with very dark cyan
    p_wm.font.color.rgb = RGBColor(20, 60, 65) 
    p_wm.alignment = PP_ALIGN.RIGHT

    # Cleanup temp file
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("cyber_manual.pptx")
