def create_slide(
    output_pptx_path: str,
    title_text: str = "AI PPT/PDF to Video",
    body_text: str = "Premium Logo Animation Generation & Video Editing",
    bg_palette: str = "technology", 
    accent_color: tuple = (0, 229, 255),  # Electric Cyan
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Deep Tech Cyber-Glow Panel' visual effect.
    """
    import os
    import requests
    from io import BytesIO
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw, ImageFilter
    
    # 1. Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # 2. === Layer 1: Background Generation ===
    bg_width, bg_height = int(13.333 * 300), int(7.5 * 300) # 300 DPI
    bg_image = None
    
    # Try fetching a tech network background
    try:
        url = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1920&auto=format&fit=crop"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        bg_image = Image.open(BytesIO(response.content)).convert("RGBA")
        bg_image = bg_image.resize((bg_width, bg_height))
        
        # Add a dark blue overlay to ensure text readability and match video vibe
        overlay = Image.new("RGBA", (bg_width, bg_height), (10, 14, 23, 180))
        bg_image = Image.alpha_composite(bg_image, overlay)
    except Exception as e:
        print(f"Image download failed, using fallback PIL gradient: {e}")
        # Fallback: Deep radial gradient
        bg_image = Image.new('RGBA', (bg_width, bg_height), (5, 7, 12, 255))
        draw = ImageDraw.Draw(bg_image)
        for i in range(bg_height):
            # Gradient from deep navy to black
            color = (int(10 * (1 - i/bg_height)), int(14 * (1 - i/bg_height)), int(23 * (1 - i/bg_height)), 255)
            draw.line([(0, i), (bg_width, i)], fill=color)

    bg_stream = BytesIO()
    bg_image.save(bg_stream, format='PNG')
    bg_stream.seek(0)
    slide.shapes.add_picture(bg_stream, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # 3. === Layer 2: Glowing Cyber Panel (PIL) ===
    # Panel dimensions: 8 inches wide, 3.5 inches high
    panel_w_in, panel_h_in = 9.0, 3.5
    pw, ph = int(panel_w_in * 300), int(panel_h_in * 300)
    
    # Create transparent canvas for the panel
    panel_img = Image.new('RGBA', (pw, ph), (0, 0, 0, 0))
    
    # Box coordinates with padding for the blur
    pad = 60
    box = [pad, pad, pw - pad, ph - pad]
    radius = 30
    
    # Step A: Draw thick glowing outline and blur it
    glow_img = Image.new('RGBA', (pw, ph), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    glow_draw.rounded_rectangle(box, radius=radius, outline=accent_color + (255,), width=25)
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(20)) # The bloom effect
    
    # Step B: Draw the sharp semi-transparent dark panel on top
    panel_draw = ImageDraw.Draw(glow_img)
    # Fill with semi-transparent dark navy
    panel_draw.rounded_rectangle(box, radius=radius, fill=(10, 14, 23, 210), outline=accent_color + (255,), width=4)
    
    # Step C: Add a Magenta Accent Bar on the left side (like the video's subtitle blocks)
    magenta = (255, 0, 127, 255)
    accent_box = [box[0] - 2, box[1] + 100, box[0] + 15, box[3] - 100]
    panel_draw.rounded_rectangle(accent_box, radius=5, fill=magenta)

    panel_stream = BytesIO()
    glow_img.save(panel_stream, format='PNG')
    panel_stream.seek(0)
    
    # Center the panel on the slide
    left = (prs.slide_width - Inches(panel_w_in)) / 2
    top = (prs.slide_height - Inches(panel_h_in)) / 2
    slide.shapes.add_picture(panel_stream, left, top, width=Inches(panel_w_in), height=Inches(panel_h_in))

    # 4. === Layer 3: Typography ===
    # Title Text
    tx_box = slide.shapes.add_textbox(left, top + Inches(0.6), Inches(panel_w_in), Inches(1.0))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p = tf.add_paragraph()
    p.text = title_text.upper()
    p.alignment = PP_ALIGN.CENTER
    p.font.name = 'Arial' # Universally available sans-serif
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    # Subtitle / Body Text (wrapped in a magenta highlighted background logic using lxml if needed, 
    # but here we use the cyan text color for contrast)
    sub_box = slide.shapes.add_textbox(left + Inches(1), top + Inches(1.8), Inches(panel_w_in - 2), Inches(1.0))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.add_paragraph()
    p_sub.text = body_text
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.font.name = 'Arial'
    p_sub.font.size = Pt(22)
    p_sub.font.bold = False
    p_sub.font.color.rgb = RGBColor(0, 229, 255) # Match the cyan glow

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_slide("cyber_glow_panel.pptx")
