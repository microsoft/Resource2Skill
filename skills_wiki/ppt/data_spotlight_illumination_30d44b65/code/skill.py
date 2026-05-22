import os
import tempfile
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def generate_spotlight_beam_png(filepath, width, height, top_width, bottom_width):
    """
    Generates a translucent spotlight beam (trapezoid with alpha gradient).
    Fades from semi-opaque white at the bottom to transparent at the top.
    """
    # Create empty RGBA image
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    
    # Create a linear alpha gradient (0 at top, 180 at bottom)
    gradient = Image.new('L', (1, height), color=0)
    for y in range(height):
        # Opacity curve: 0 at top (y=0), ~180 at bottom (y=height)
        alpha = int(180 * (y / height))
        gradient.putpixel((0, y), alpha)
    gradient = gradient.resize((width, height))

    # Create the polygon mask (Trapezoid)
    poly_mask = Image.new('L', (width, height), color=0)
    draw = ImageDraw.Draw(poly_mask)
    
    # Points for trapezoid: Top-Left, Top-Right, Bottom-Right, Bottom-Left
    poly = [
        (width/2 - top_width/2, 0),
        (width/2 + top_width/2, 0),
        (width/2 + bottom_width/2, height),
        (width/2 - bottom_width/2, height)
    ]
    draw.polygon(poly, fill=255)

    # Combine gradient and polygon mask
    final_alpha = Image.new('L', (width, height), color=0)
    final_alpha.paste(gradient, (0, 0), mask=poly_mask)

    # Apply to a white image
    beam = Image.new('RGBA', (width, height), color=(255, 255, 255))
    beam.putalpha(final_alpha)
    
    beam.save(filepath, format="PNG")
    return filepath

def create_slide(
    output_pptx_path: str,
    title_text: str = "Sales Performance - 2024",
    subtitle_text: str = "Quarterly Achievement Spotlight",
    data_points: list = None,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Data Spotlight Illumination visual effect.
    """
    if data_points is None:
        data_points = [
            {"label": "Q1 '24", "value": "$ 1200", "color": (199, 36, 122)},  # Magenta
            {"label": "Q2 '24", "value": "$ 1550", "color": (0, 168, 178)},   # Teal
            {"label": "Q3 '24", "value": "$ 1800", "color": (142, 198, 63)},  # Lime
            {"label": "Q4 '24", "value": "$ 2400", "color": (242, 101, 34)},  # Orange
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    # Deep Navy solid background for high contrast with light beams
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(25, 30, 45)
    bg.line.fill.background() # No line

    # Add Title
    title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), prs.slide_width - Inches(2), Inches(1))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # Add Subtitle
    sub_box = slide.shapes.add_textbox(Inches(1), Inches(1.3), prs.slide_width - Inches(2), Inches(0.5))
    p_sub = sub_box.text_frame.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.font.size = Pt(20)
    p_sub.font.color.rgb = RGBColor(180, 185, 200)

    # === Layer 2: Visual Effect (Spotlights & Bases) ===
    num_items = len(data_points)
    col_width = prs.slide_width / num_items
    
    # Metrics for shapes
    base_width = Inches(2.2)
    base_height = Inches(0.5)
    base_y = Inches(5.5)
    
    beam_h = Inches(3.5)
    beam_w = Inches(3.0)  # Top width of the beam
    
    # Create temp directory for PNG beams
    with tempfile.TemporaryDirectory() as tmpdir:
        # Generate the beam PNG once
        beam_png_path = os.path.join(tmpdir, "beam.png")
        generate_spotlight_beam_png(
            beam_png_path, 
            width=int(beam_w.dpi * 3),    # internal resolution 300dpi scaling
            height=int(beam_h.dpi * 3.5), 
            top_width=int(beam_w.dpi * 3), 
            bottom_width=int(base_width.dpi * 2.2 * 0.8) # slightly narrower than base
        )

        for i, item in enumerate(data_points):
            center_x = (col_width * i) + (col_width / 2)
            
            # --- Draw Podium Base ---
            # To simulate 3D, we draw a darker base oval, then a lighter top oval.
            
            # 1. Shadow/Thickness oval (Bottom)
            r, g, b = item["color"]
            dark_r, dark_g, dark_b = max(0, r-60), max(0, g-60), max(0, b-60)
            
            base_bottom = slide.shapes.add_shape(
                MSO_SHAPE.OVAL, 
                center_x - (base_width/2), 
                base_y + Inches(0.15), # Offset down
                base_width, 
                base_height
            )
            base_bottom.fill.solid()
            base_bottom.fill.fore_color.rgb = RGBColor(dark_r, dark_g, dark_b)
            base_bottom.line.fill.background()
            
            # 2. Surface oval (Top)
            base_top = slide.shapes.add_shape(
                MSO_SHAPE.OVAL, 
                center_x - (base_width/2), 
                base_y, 
                base_width, 
                base_height
            )
            base_top.fill.solid()
            base_top.fill.fore_color.rgb = RGBColor(r, g, b)
            base_top.line.fill.background()

            # --- Insert Translucent Light Beam ---
            # Placed so the bottom sits right on the top oval
            pic = slide.shapes.add_picture(
                beam_png_path, 
                center_x - (beam_w/2), 
                base_y - beam_h + Inches(0.25), 
                width=beam_w, 
                height=beam_h
            )
            
            # --- Add Content inside the Beam ---
            # Value Box
            val_width = Inches(2.0)
            val_box = slide.shapes.add_textbox(
                center_x - (val_width/2), 
                base_y - Inches(1.8), 
                val_width, 
                Inches(0.8)
            )
            val_tf = val_box.text_frame
            val_p = val_tf.paragraphs[0]
            val_p.text = item["value"]
            val_p.alignment = PP_ALIGN.CENTER
            val_p.font.size = Pt(32)
            val_p.font.bold = True
            val_p.font.color.rgb = RGBColor(255, 255, 255)
            
            # Simple decorative line below value
            line = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                center_x - Inches(0.5),
                base_y - Inches(0.9),
                Inches(1.0),
                Inches(0.03)
            )
            line.fill.solid()
            line.fill.fore_color.rgb = RGBColor(r, g, b)
            line.line.fill.background()

            # --- Add Label below Podium ---
            lbl_box = slide.shapes.add_textbox(
                center_x - (val_width/2), 
                base_y + Inches(0.8), 
                val_width, 
                Inches(0.5)
            )
            lbl_tf = lbl_box.text_frame
            lbl_p = lbl_tf.paragraphs[0]
            lbl_p.text = item["label"]
            lbl_p.alignment = PP_ALIGN.CENTER
            lbl_p.font.size = Pt(22)
            lbl_p.font.bold = True
            lbl_p.font.color.rgb = RGBColor(r, g, b)

    prs.save(output_pptx_path)
    return output_pptx_path
