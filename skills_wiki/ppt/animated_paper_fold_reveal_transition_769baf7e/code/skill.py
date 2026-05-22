import os
import math
from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw, ImageFilter
from lxml import etree

def generate_gradient_bg(w, h, color1, color2, filepath):
    """Generates a smooth diagonal gradient background."""
    base = Image.new('RGBA', (w, h), color1)
    top = Image.new('RGBA', (w, h), color2)
    mask = Image.new('L', (w, h))
    mask_data = []
    for y in range(h):
        for x in range(w):
            mask_data.append(int(255 * (x + y) / (w + h)))
    mask.putdata(mask_data)
    img = Image.composite(base, top, mask)
    img.save(filepath)
    return filepath

def create_wavy_flap(w, h, is_left, filepath, color_dark, color_light, accent_color):
    """Draws a procedural wavy paper flap with 3D edge layers and shadows."""
    flap_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))

    def draw_layer(offset_x, col_start, col_end, shadow_rad=0, shadow_off=(0,0)):
        layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        mask = Image.new('L', (w, h), 0)
        draw = ImageDraw.Draw(mask)
        
        # Procedural Sine Wave Edge
        points = [(0, 0)] if is_left else [(w, 0)]
        base_x = w - 150 if is_left else 150
        amp = 60
        freq = (1.5 * math.pi) / h
        
        for y in range(h + 1):
            dx = amp * math.sin(y * freq)
            x = base_x + dx + offset_x
            points.append((x, y))
            
        points.append((0, h) if is_left else (w, h))
        draw.polygon(points, fill=255)

        # Apply Drop Shadow
        if shadow_rad > 0:
            shadow = mask.filter(ImageFilter.GaussianBlur(shadow_rad))
            shadow_comp = Image.new('RGBA', (w, h), (0, 0, 0, 0))
            shadow_color = Image.new('RGBA', (w, h), (0, 0, 0, 180))
            shadow_comp.paste(shadow_color, shadow_off, shadow)
            layer = Image.alpha_composite(layer, shadow_comp)

        # Apply Gradient Fill
        grad = Image.new('RGBA', (w, h), col_start)
        top_grad = Image.new('RGBA', (w, h), col_end)
        grad_mask = Image.new('L', (w, h))
        grad_mask.putdata([int(255 * y / h) for y in range(h) for _ in range(w)])
        grad_fill = Image.composite(grad, top_grad, grad_mask)
        
        grad_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        grad_layer.paste(grad_fill, (0, 0), mask)
        
        return Image.alpha_composite(layer, grad_layer)

    # Z-Index 1: Deep Drop Shadow Flap
    l1 = draw_layer(30 if is_left else -30, (10, 5, 25, 255), (10, 5, 25, 255), 25, (15, 0))
    # Z-Index 2: Bright Edge Highlight Flap
    l2 = draw_layer(15 if is_left else -15, accent_color, accent_color, 0, (0, 0))
    # Z-Index 3: Main Gradient Flap
    l3 = draw_layer(0, color_light, color_dark, 5, (5 if is_left else -5, 0))

    flap_img = Image.alpha_composite(flap_img, l1)
    flap_img = Image.alpha_composite(flap_img, l2)
    flap_img = Image.alpha_composite(flap_img, l3)
    
    flap_img.save(filepath)
    return filepath

def apply_text_shadow(shape):
    """Injects openXML to add a soft drop shadow to a text box shape."""
    spPr = shape.element.spPr
    effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
    outerShdw = etree.SubElement(effectLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw', 
                                 blurRad="120000", dist="40000", dir="2700000", algn="ctr")
    srgbClr = etree.SubElement(outerShdw, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr', val="000000")
    etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', val="60000")

def inject_morph_transition(slide):
    """Injects openXML to enable Morph transition on a slide."""
    sld = slide.element
    transition = etree.Element("{http://schemas.openxmlformats.org/presentationml/2006/main}transition", spd="slow")
    etree.SubElement(transition, "{http://schemas.openxmlformats.org/presentationml/2006/main}morph")
    
    # Insert transition before timing or extLst elements
    timing = sld.xpath('./p:timing', namespaces=sld.nsmap)
    if timing:
        timing[0].addprevious(transition)
    else:
        sld.append(transition)

def create_slide(output_pptx_path: str, title_text: str = "THANKS", subtitle_text: str = "FOR WATCHING", **kwargs) -> str:
    # --- Generate Assets ---
    bg_path = "temp_bg.png"
    flap_l_path = "temp_flap_l.png"
    flap_r_path = "temp_flap_r.png"
    
    # Colors
    bg_dark = (15, 10, 40, 255)
    bg_light = (45, 20, 80, 255)
    flap_dark = (30, 10, 70, 255)
    flap_light = (120, 50, 200, 255)
    accent = (0, 200, 255, 255)
    
    # Dimensions (Based on 13.333 x 7.5 inch slide at 96 DPI)
    slide_w_px, slide_h_px = 1280, 720
    flap_w_px = 750  # Overlap in the middle
    
    generate_gradient_bg(slide_w_px, slide_h_px, bg_dark, bg_light, bg_path)
    create_wavy_flap(flap_w_px, slide_h_px, True, flap_l_path, flap_dark, flap_light, accent)
    create_wavy_flap(flap_w_px, slide_h_px, False, flap_r_path, flap_dark, flap_light, accent)
    
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    flap_w_inch = Inches(7.8)

    # ==========================================
    # SLIDE 1: CLOSED STATE
    # ==========================================
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])
    slide1.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)
    
    # Text Behind Flaps
    tb1 = slide1.shapes.add_textbox(Inches(1), Inches(2.5), Inches(11.333), Inches(2.5))
    tf1 = tb1.text_frame
    tf1.text = title_text
    tf1.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf1.paragraphs[0].font.size = Pt(140)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.name = "Arial Black"
    tf1.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    apply_text_shadow(tb1)
    
    # Flaps (Closed position)
    flap_l_1 = slide1.shapes.add_picture(flap_l_path, 0, 0, flap_w_inch, prs.slide_height)
    flap_r_1 = slide1.shapes.add_picture(flap_r_path, prs.slide_width - flap_w_inch, 0, flap_w_inch, prs.slide_height)
    
    # MAGIC TRICK: Prefixing names with "!!" forces PowerPoint Morph to link these specific shapes
    flap_l_1.name = "!!LeftFlap"
    flap_r_1.name = "!!RightFlap"

    # ==========================================
    # SLIDE 2: OPEN STATE (REVEAL)
    # ==========================================
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    slide2.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)
    
    # Text 
    tb2 = slide2.shapes.add_textbox(Inches(1), Inches(2.5), Inches(11.333), Inches(2.5))
    tf2 = tb2.text_frame
    tf2.text = title_text
    tf2.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf2.paragraphs[0].font.size = Pt(140)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.name = "Arial Black"
    tf2.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    apply_text_shadow(tb2)
    
    # Subtitle
    sub2 = slide2.shapes.add_textbox(Inches(3), Inches(4.8), Inches(7.333), Inches(1.0))
    ts2 = sub2.text_frame
    ts2.text = subtitle_text
    ts2.paragraphs[0].alignment = PP_ALIGN.CENTER
    ts2.paragraphs[0].font.size = Pt(32)
    ts2.paragraphs[0].font.name = "Arial"
    ts2.paragraphs[0].font.color.rgb = RGBColor(200, 220, 255)
    
    # Flaps (Open position - Pulled to the sides)
    flap_l_2 = slide2.shapes.add_picture(flap_l_path, Inches(-4.5), 0, flap_w_inch, prs.slide_height)
    flap_r_2 = slide2.shapes.add_picture(flap_r_path, prs.slide_width - Inches(3.3), 0, flap_w_inch, prs.slide_height)
    
    flap_l_2.name = "!!LeftFlap"
    flap_r_2.name = "!!RightFlap"
    
    # Inject Morph Transition
    inject_morph_transition(slide2)

    prs.save(output_pptx_path)
    
    # Clean up generated assets
    for path in [bg_path, flap_l_path, flap_r_path]:
        if os.path.exists(path):
            os.remove(path)
            
    return output_pptx_path
