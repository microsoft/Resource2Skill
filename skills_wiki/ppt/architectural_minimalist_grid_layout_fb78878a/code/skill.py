import os
from io import BytesIO
from typing import Tuple
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def _generate_architectural_diagram(
    width_in: float, 
    height_in: float, 
    diagram_type: str, 
    accent_color: Tuple[int, int, int]
) -> BytesIO:
    """
    Generates procedurally drawn minimalist 'architectural' wireframe diagrams using PIL.
    This ensures the exact aesthetic described in the video without relying on external images.
    """
    dpi = 300
    w_px = int(width_in * dpi)
    h_px = int(height_in * dpi)
    
    # Pure white background for minimalist style
    img = Image.new('RGBA', (w_px, h_px), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Charcoal line color
    line_color = (60, 60, 60, 255)
    accent_rgba = (accent_color[0], accent_color[1], accent_color[2], 255)
    light_gray = (240, 240, 240, 255)

    # Draw grid background
    grid_spacing = int(0.25 * dpi)
    for x in range(0, w_px, grid_spacing):
        draw.line([(x, 0), (x, h_px)], fill=(245, 245, 245, 255), width=1)
    for y in range(0, h_px, grid_spacing):
        draw.line([(0, y), (w_px, y)], fill=(245, 245, 245, 255), width=1)

    if diagram_type == "site_plan":
        # Draw a top-down abstract map
        draw.rectangle([w_px*0.1, h_px*0.1, w_px*0.9, h_px*0.9], outline=line_color, width=3)
        draw.polygon([(w_px*0.2, h_px*0.2), (w_px*0.8, h_px*0.3), (w_px*0.7, h_px*0.8), (w_px*0.3, h_px*0.7)], fill=light_gray, outline=line_color, width=2)
        # Accent object
        draw.rectangle([w_px*0.4, h_px*0.4, w_px*0.6, h_px*0.6], fill=accent_rgba, outline=line_color, width=2)
        
    elif diagram_type == "perspective":
        # The 'Centralized' focal point - large geometric structure
        draw.rectangle([0, 0, w_px-1, h_px-1], outline=line_color, width=4)
        # Horizon line
        draw.line([(0, h_px*0.7), (w_px, h_px*0.7)], fill=line_color, width=2)
        # Perspective lines
        vanishing_pt = (w_px*0.5, h_px*0.5)
        draw.polygon([(w_px*0.2, h_px*0.9), (w_px*0.3, h_px*0.4), (w_px*0.7, h_px*0.4), (w_px*0.8, h_px*0.9)], fill=light_gray, outline=line_color, width=3)
        # Accent element (glass facade / structural feature)
        draw.polygon([(w_px*0.35, h_px*0.8), (w_px*0.4, h_px*0.45), (w_px*0.6, h_px*0.45), (w_px*0.65, h_px*0.8)], fill=accent_rgba, outline=line_color, width=2)
        
    elif diagram_type == "section":
        # Side cutaway
        draw.rectangle([0, 0, w_px-1, h_px-1], outline=line_color, width=2)
        # Ground level
        draw.rectangle([w_px*0.1, h_px*0.8, w_px*0.9, h_px*0.95], fill=line_color)
        # Building levels
        draw.rectangle([w_px*0.2, h_px*0.2, w_px*0.5, h_px*0.8], outline=line_color, width=3)
        draw.rectangle([w_px*0.5, h_px*0.4, w_px*0.8, h_px*0.8], outline=line_color, width=3)
        # Accent highlight
        draw.rectangle([w_px*0.25, h_px*0.25, w_px*0.45, h_px*0.4], fill=accent_rgba)

    image_stream = BytesIO()
    img.save(image_stream, format='PNG')
    image_stream.seek(0)
    return image_stream

def create_slide(
    output_pptx_path: str,
    title_text: str = "URBAN RENEWAL HUB",
    body_text: str = "A comprehensive approach to modern infrastructure.",
    bg_palette: str = "minimalist",
    accent_color: tuple = (255, 200, 0),  # Bright Yellow accent "Color Combo"
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the "Minimalist Grid Presentation Board" effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Ensure background is pure white
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    accent_rgb = RGBColor(accent_color[0], accent_color[1], accent_color[2])
    dark_gray = RGBColor(40, 40, 40)
    mid_gray = RGBColor(120, 120, 120)

    # ==========================================
    # GRID DEFINITION (3 Columns, structured)
    # ==========================================
    margin = Inches(0.5)
    gutter = Inches(0.3)
    
    col_w_1 = Inches(3.0)
    col_w_2 = Inches(6.0) # Centralized main focal point
    col_w_3 = Inches(3.0)
    
    col_1_x = margin
    col_2_x = col_1_x + col_w_1 + gutter
    col_3_x = col_2_x + col_w_2 + gutter

    # ==========================================
    # HEADER (Left Column, Top)
    # ==========================================
    # Accent line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_1_x, margin, col_w_1, Pt(4))
    line.fill.solid()
    line.fill.fore_color.rgb = accent_rgb
    line.line.fill.background()

    # Title
    tx_box = slide.shapes.add_textbox(col_1_x, margin + Inches(0.1), col_w_1, Inches(0.8))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p = tf.add_paragraph()
    p.text = title_text.upper()
    p.font.bold = True
    p.font.size = Pt(28)
    p.font.color.rgb = dark_gray
    p.font.name = "Arial"

    # Subtitle / Rationale
    p2 = tf.add_paragraph()
    p2.text = "01 // PROJECT OVERVIEW\n\n" + body_text + "\n\nThis board utilizes a minimalist grid structure to present the problem, the methodology, and the final architectural solution without visual clutter."
    p2.font.size = Pt(10)
    p2.font.color.rgb = mid_gray
    p2.font.name = "Arial"

    # ==========================================
    # COLUMN 1: SITE PLAN (Problem Statement)
    # ==========================================
    c1_img_y = margin + Inches(2.5)
    c1_img_h = Inches(4.5)
    
    site_stream = _generate_architectural_diagram(col_w_1.inches, c1_img_h.inches, "site_plan", accent_color)
    slide.shapes.add_picture(site_stream, col_1_x, c1_img_y, col_w_1, c1_img_h)

    # Label
    tx_lbl = slide.shapes.add_textbox(col_1_x, c1_img_y - Inches(0.3), col_w_1, Inches(0.3))
    tx_lbl.text_frame.text = "FIG 1. SITE PROXIMITY MATRIX"
    tx_lbl.text_frame.paragraphs[0].font.size = Pt(9)
    tx_lbl.text_frame.paragraphs[0].font.bold = True
    tx_lbl.text_frame.paragraphs[0].font.color.rgb = dark_gray

    # ==========================================
    # COLUMN 2: THE CENTRALIZED PERSPECTIVE
    # ==========================================
    # This acts as the focal point ("Centralized Layout" tip)
    c2_img_y = margin
    c2_img_h = Inches(6.5)
    
    persp_stream = _generate_architectural_diagram(col_w_2.inches, c2_img_h.inches, "perspective", accent_color)
    slide.shapes.add_picture(persp_stream, col_2_x, c2_img_y, col_w_2, c2_img_h)

    tx_lbl2 = slide.shapes.add_textbox(col_2_x, c2_img_y + c2_img_h, col_w_2, Inches(0.3))
    tx_lbl2.text_frame.text = "FIG 2. MAIN EXTERIOR PERSPECTIVE - SOUTH ELEVATION"
    tx_lbl2.text_frame.paragraphs[0].font.size = Pt(9)
    tx_lbl2.text_frame.paragraphs[0].font.bold = True
    tx_lbl2.text_frame.paragraphs[0].font.color.rgb = dark_gray
    tx_lbl2.text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT

    # ==========================================
    # COLUMN 3: DIAGRAMS & SECTIONS
    # ==========================================
    # Stacked grid items
    c3_img_h = Inches(3.1)
    
    # Section 1
    sec1_stream = _generate_architectural_diagram(col_w_3.inches, c3_img_h.inches, "section", accent_color)
    slide.shapes.add_picture(sec1_stream, col_3_x, margin, col_w_3, c3_img_h)
    
    tx_lbl3 = slide.shapes.add_textbox(col_3_x, margin + c3_img_h, col_w_3, Inches(0.3))
    tx_lbl3.text_frame.text = "FIG 3. LONGITUDINAL SECTION A-A'"
    tx_lbl3.text_frame.paragraphs[0].font.size = Pt(9)
    tx_lbl3.text_frame.paragraphs[0].font.color.rgb = dark_gray

    # Section 2
    sec2_stream = _generate_architectural_diagram(col_w_3.inches, c3_img_h.inches, "site_plan", accent_color) # reuse abstract type for variety
    slide.shapes.add_picture(sec2_stream, col_3_x, margin + c3_img_h + Inches(0.3), col_w_3, c3_img_h)
    
    tx_lbl4 = slide.shapes.add_textbox(col_3_x, margin + (c3_img_h*2) + Inches(0.3), col_w_3, Inches(0.3))
    tx_lbl4.text_frame.text = "FIG 4. SPATIAL PROGRAMMING DIAGRAM"
    tx_lbl4.text_frame.paragraphs[0].font.size = Pt(9)
    tx_lbl4.text_frame.paragraphs[0].font.color.rgb = dark_gray

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
