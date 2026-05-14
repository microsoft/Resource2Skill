def create_slide(
    output_pptx_path: str,
    title_text: str = "Company Profile",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. \nSed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    bg_theme: str = "city,night",
    slate_color: tuple = (65, 65, 80, 255),
    gold_color: tuple = (200, 160, 80, 255),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Organic Dual-Tone Wave Layout.
    """
    import os
    import io
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from PIL import Image, ImageDraw

    # Initialize Presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Dimensions in pixels (standard 1080p equivalent)
    W, H = 1920, 1080

    # ==========================================
    # Layer 1: Background Image Fetching
    # ==========================================
    bg_image_stream = io.BytesIO()
    try:
        # Fetch image from Unsplash
        url = f"https://source.unsplash.com/random/{W}x{H}/?{bg_theme}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            bg_pil = Image.open(response).convert("RGBA")
            # Darken the background slightly for better contrast
            dark_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 80))
            bg_pil = Image.alpha_composite(bg_pil, dark_overlay)
            bg_pil.save(bg_image_stream, format='PNG')
    except Exception:
        # Fallback: Solid dark gray-blue background
        bg_pil = Image.new("RGBA", (W, H), (30, 30, 40, 255))
        bg_pil.save(bg_image_stream, format='PNG')
    
    bg_image_stream.seek(0)
    slide.shapes.add_picture(bg_image_stream, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # ==========================================
    # Layer 2: Core Effect - Organic Dual Wave
    # ==========================================
    # We draw at 2x scale for anti-aliasing (Supersampling)
    scale = 2
    canvas_w, canvas_h = W * scale, H * scale
    
    # Create an empty transparent canvas
    wave_img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(wave_img)

    # To create the "swoosh", we use massive overlapping circles.
    # Base Wave (Gold) - slightly protruding
    gold_circle_bbox = [
        int(canvas_w * 0.1),  # x0
        int(-canvas_h * 0.5), # y0
        int(canvas_w * 2.5),  # x1
        int(canvas_h * 1.5)   # y1
    ]
    draw.ellipse(gold_circle_bbox, fill=gold_color)

    # Foreground Wave (Slate) - covers most of the gold, leaving a trim
    slate_circle_bbox = [
        int(canvas_w * 0.18), # x0 (shifted right)
        int(-canvas_h * 0.6), # y0 (shifted up)
        int(canvas_w * 2.6),  # x1
        int(canvas_h * 1.6)   # y1
    ]
    draw.ellipse(slate_circle_bbox, fill=slate_color)

    # Resize down with Lanczos for buttery smooth edges
    wave_img = wave_img.resize((W, H), Image.Resampling.LANCZOS)
    
    # Save wave to stream and add to slide
    wave_stream = io.BytesIO()
    wave_img.save(wave_stream, format='PNG')
    wave_stream.seek(0)
    slide.shapes.add_picture(wave_stream, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # ==========================================
    # Layer 3: Text & Elements Layout
    # ==========================================
    # Add Title
    title_box = slide.shapes.add_textbox(Inches(6.5), Inches(2.5), Inches(6.0), Inches(1.5))
    title_tf = title_box.text_frame
    title_tf.word_wrap = True
    p = title_tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.name = "Arial"
    p.font.color.rgb = RGBColor(255, 255, 255) # White

    # Add a decorative gold horizontal line under the title
    # Extracted from the video style (0:11, 0:41)
    line = slide.shapes.add_shape(
        1, # msoShapeRectangle
        Inches(6.6), Inches(3.7), Inches(1.5), Inches(0.08)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(gold_color[0], gold_color[1], gold_color[2])
    line.line.fill.background() # No border

    # Add Body Text
    body_box = slide.shapes.add_textbox(Inches(6.5), Inches(4.0), Inches(5.5), Inches(2.0))
    body_tf = body_box.text_frame
    body_tf.word_wrap = True
    p2 = body_tf.paragraphs[0]
    p2.text = body_text
    p2.font.size = Pt(18)
    p2.font.name = "Arial"
    p2.font.color.rgb = RGBColor(200, 200, 210) # Soft light gray/blue

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
