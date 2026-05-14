import os
import io
import urllib.request
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement

def add_morph_transition(slide):
    """Injects Morph transition XML into a slide."""
    transition = OxmlElement('p:transition')
    transition.set('spd', 'fast')
    morph = OxmlElement('p:morph')
    transition.append(morph)
    slide._element.append(transition)

def create_transparent_overlay(url: str, alpha: int = 40, output_path: str = "temp_overlay.png") -> str:
    """Downloads an image, applies global transparency, and saves as PNG."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            img_data = response.read()
        
        img = Image.open(io.BytesIO(img_data)).convert("RGB")
        # Apply alpha (0-255, where 40 is approx 15% opacity)
        img.putalpha(alpha)
        img.save(output_path, "PNG")
        return output_path
    except Exception as e:
        print(f"Failed to generate transparent overlay: {e}")
        return None

def create_slide(
    output_pptx_path: str,
    title_text: str = "COMPANY PROFILE",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas porttitor congue massa. Fusce posuere, magna sed pulvinar ultricies, purus lectus malesuada libero.",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Dynamic Morphing Color Ribbon effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Palette definition
    dark_slate = RGBColor(52, 60, 75)
    ribbon_colors = [
        RGBColor(33, 150, 243),  # Blue
        RGBColor(76, 175, 80),   # Green
        RGBColor(255, 152, 0),   # Orange
        RGBColor(244, 67, 54),   # Red
        RGBColor(255, 193, 7)    # Yellow
    ]
    
    compressed_width = Inches(0.6)
    
    # --- Helper to draw the ribbon state ---
    def draw_ribbon(slide, active_index=-1):
        """
        Draws the vertical ribbons. 
        If active_index is -1, draws the title state (all compressed).
        If active_index is 0-4, expands that specific ribbon.
        Returns the (left, width) bounding box of the active/content area.
        """
        current_x = 0
        content_x = 0
        content_w = 0
        
        for i, color in enumerate(ribbon_colors):
            if active_index == -1:
                w = compressed_width
            else:
                if i == active_index:
                    # Expanded width = Total width - (Width of the other 4 compressed ribbons)
                    w = prs.slide_width - (compressed_width * (len(ribbon_colors) - 1))
                    content_x = current_x
                    content_w = w
                else:
                    w = compressed_width
            
            shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, current_x, 0, w, prs.slide_height)
            shape.fill.solid()
            shape.fill.fore_color.rgb = color
            # Remove outlines for a seamless flat look
            shape.line.fill.background()
            
            current_x += w
            
        if active_index == -1:
            # For title slide, content area is the space after the ribbons
            content_x = len(ribbon_colors) * compressed_width
            content_w = prs.slide_width - content_x
            
        return content_x, content_w

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    slide_title = prs.slides.add_slide(prs.slide_layouts[6])
    bg_x, bg_w = draw_ribbon(slide_title, active_index=-1)
    
    # Add dark background for title area
    title_bg = slide_title.shapes.add_shape(MSO_SHAPE.RECTANGLE, bg_x, 0, bg_w, prs.slide_height)
    title_bg.fill.solid()
    title_bg.fill.fore_color.rgb = dark_slate
    title_bg.line.fill.background()
    
    # Add Title Text
    tb = slide_title.shapes.add_textbox(bg_x + Inches(1), Inches(3), bg_w - Inches(2), Inches(1))
    p = tb.text_frame.add_paragraph()
    p.text = title_text
    p.font.name = 'Arial Black'
    p.font.size = Pt(48)
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    # Add Divider Line
    line = slide_title.shapes.add_shape(MSO_SHAPE.RECTANGLE, bg_x + Inches(1), Inches(4.2), bg_w - Inches(3), Pt(3))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(255, 255, 255)
    line.line.fill.background()
    
    # Add Subtext
    tb_sub = slide_title.shapes.add_textbox(bg_x + Inches(1), Inches(4.5), bg_w - Inches(3), Inches(1.5))
    tb_sub.text_frame.word_wrap = True
    p_sub = tb_sub.text_frame.add_paragraph()
    p_sub.text = body_text
    p_sub.font.name = 'Arial'
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = RGBColor(220, 220, 220)

    # ==========================================
    # SLIDE 2: CONTENT SLIDE (Red Ribbon Expands)
    # ==========================================
    slide_red = prs.slides.add_slide(prs.slide_layouts[6])
    add_morph_transition(slide_red)
    
    active_idx = 3 # Red
    cont_x, cont_w = draw_ribbon(slide_red, active_index=active_idx)
    
    # Add subtle transparent image overlay to the expanded red section
    overlay_img_path = create_transparent_overlay("https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=1200&auto=format&fit=crop", alpha=35)
    if overlay_img_path:
        pic = slide_red.shapes.add_picture(overlay_img_path, cont_x, 0, cont_w, prs.slide_height)
        # Send picture to back (but in front of the background rectangle) so text is readable
        # Native pptx doesn't expose z-order cleanly after creation, but since we create it before text, text will be on top.
        
    # Content Title
    tb2 = slide_red.shapes.add_textbox(cont_x + Inches(0.5), Inches(0.5), cont_w - Inches(1), Inches(1))
    p2 = tb2.text_frame.add_paragraph()
    p2.text = "WHO WE ARE?"
    p2.font.name = 'Arial Black'
    p2.font.size = Pt(40)
    p2.font.color.rgb = RGBColor(255, 255, 255)
    
    # Content Body
    tb2_sub = slide_red.shapes.add_textbox(cont_x + Inches(0.5), Inches(1.5), cont_w - Inches(2), Inches(2))
    tb2_sub.text_frame.word_wrap = True
    p2_sub = tb2_sub.text_frame.add_paragraph()
    p2_sub.text = body_text
    p2_sub.font.name = 'Arial'
    p2_sub.font.size = Pt(16)
    p2_sub.font.color.rgb = RGBColor(255, 255, 255)

    # ==========================================
    # SLIDE 3: CONTENT SLIDE (Yellow Ribbon Expands)
    # ==========================================
    slide_yellow = prs.slides.add_slide(prs.slide_layouts[6])
    add_morph_transition(slide_yellow)
    
    active_idx = 4 # Yellow
    cont_x, cont_w = draw_ribbon(slide_yellow, active_index=active_idx)
    
    # Re-use overlay
    if overlay_img_path and os.path.exists(overlay_img_path):
        slide_yellow.shapes.add_picture(overlay_img_path, cont_x, 0, cont_w, prs.slide_height)
        
    # Content Title
    tb3 = slide_yellow.shapes.add_textbox(cont_x + Inches(0.5), Inches(0.5), cont_w - Inches(1), Inches(1))
    p3 = tb3.text_frame.add_paragraph()
    p3.text = "OUR SERVICES"
    p3.font.name = 'Arial Black'
    p3.font.size = Pt(40)
    p3.font.color.rgb = RGBColor(255, 255, 255)

    tb3_sub = slide_yellow.shapes.add_textbox(cont_x + Inches(0.5), Inches(1.5), cont_w - Inches(2), Inches(2))
    tb3_sub.text_frame.word_wrap = True
    p3_sub = tb3_sub.text_frame.add_paragraph()
    p3_sub.text = "Dynamic content seamlessly transitions between states."
    p3_sub.font.name = 'Arial'
    p3_sub.font.size = Pt(16)
    p3_sub.font.color.rgb = RGBColor(255, 255, 255)

    # Cleanup temp file
    if overlay_img_path and os.path.exists(overlay_img_path):
        try:
            os.remove(overlay_img_path)
        except Exception:
            pass

    prs.save(output_pptx_path)
    return output_pptx_path
