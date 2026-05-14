def create_slide(
    output_pptx_path: str,
    title_text: str = "Default Title",
    body_text: str = "",
    bg_palette: str = "technology",
    accent_color: tuple = (0, 191, 255),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Kinetic Sliced-Typography" visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from PIL import Image, ImageDraw, ImageFont
    import os

    # 1. Setup Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide

    # Helper: Generate Gradient Background via PIL
    def generate_gradient_bg(filename, width=1920, height=1080):
        base = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(base)
        # Deep Purple to Vibrant Pink/Red
        color1 = (60, 16, 83)
        color2 = (212, 63, 141)
        for y in range(height):
            r = int(color1[0] + (color2[0] - color1[0]) * y / height)
            g = int(color1[1] + (color2[1] - color1[1]) * y / height)
            b = int(color1[2] + (color2[2] - color1[2]) * y / height)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        base.save(filename)
        return filename

    # Helper: Generate Sliced/Glitched Text via PIL
    def generate_sliced_text(text, filename, font_size=200, shift_amount=20, is_hollow=False):
        # Try to load a bold font, fallback to default if missing
        try:
            # Common bold fonts on Windows/Mac/Linux
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("Impact.ttf", font_size)
            except:
                font = ImageFont.load_default()

        # Measure text size
        temp_img = Image.new("RGBA", (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        bbox = temp_draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        # Create canvas slightly larger to accommodate shifts
        img_w = text_w + abs(shift_amount) * 4
        img_h = text_h + 40
        canvas = Image.new("RGBA", (img_w, img_h), (255, 255, 255, 0))
        draw = ImageDraw.Draw(canvas)
        
        # Draw text
        text_pos = (abs(shift_amount)*2, 10)
        if is_hollow:
            # Draw stroke/outline only
            draw.text(text_pos, text, font=font, fill=(255, 255, 255, 0), stroke_width=4, stroke_fill=(255, 255, 255, 255))
        else:
            draw.text(text_pos, text, font=font, fill=(255, 255, 255, 255))
        
        # Slice logic
        slice_y = img_h // 2
        top_half = canvas.crop((0, 0, img_w, slice_y))
        bottom_half = canvas.crop((0, slice_y, img_w, img_h))
        
        # Recombine with shift
        final_img = Image.new("RGBA", (img_w, img_h), (255, 255, 255, 0))
        final_img.paste(top_half, (shift_amount, 0))
        final_img.paste(bottom_half, (-shift_amount, slice_y))
        
        final_img.save(filename)
        return filename

    # Helper: Generate Stylized Subject Silhouette
    def generate_subject_silhouette(filename, width=600, height=800):
        # Creates a dynamic stylized player/character silhouette to guarantee overlapping works
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Bright yellow accent (like the Lakers jersey in the tutorial)
        jersey_color = (253, 185, 39, 255)
        skin_color = (40, 30, 25, 255)
        
        # Draw a dynamic, abstracted jumping figure
        # Torso
        draw.polygon([(150, 400), (350, 350), (450, 600), (200, 800)], fill=jersey_color)
        # Head
        draw.ellipse([(280, 150), (380, 250)], fill=skin_color)
        # Arm reaching up (like holding a ball)
        draw.line([(320, 200), (100, 50)], fill=skin_color, width=40)
        # Ball
        draw.ellipse([(40, 10), (120, 90)], fill=(200, 100, 50, 255))
        
        img.save(filename)
        return filename

    # --- Execute and Build Slide ---
    
    # 1. Background Layer
    bg_file = "temp_bg.png"
    generate_gradient_bg(bg_file)
    slide.shapes.add_picture(bg_file, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # 2. Background Text Layer (Behind Subject)
    txt_bg1 = "temp_txt_go.png"
    txt_bg2 = "temp_txt_never.png"
    generate_sliced_text("GO", txt_bg1, font_size=240, shift_amount=15)
    generate_sliced_text("NEVER", txt_bg2, font_size=160, shift_amount=-10)
    
    # Place text randomly but structured
    pic = slide.shapes.add_picture(txt_bg1, Inches(2), Inches(1), width=Inches(4))
    pic.rotation = -5
    pic = slide.shapes.add_picture(txt_bg2, Inches(1.5), Inches(3.5), width=Inches(5))
    pic.rotation = -2

    # 3. The Subject Layer (The Interleaver)
    subject_file = "temp_subject.png"
    generate_subject_silhouette(subject_file)
    # Position subject dead center
    slide.shapes.add_picture(subject_file, Inches(4), Inches(1.5), height=Inches(6))

    # 4. Foreground Text Layer (In Front of Subject)
    txt_fg1 = "temp_txt_up.png"
    txt_fg2 = "temp_txt_give.png"
    # Make one of them hollow for stylistic variance
    generate_sliced_text("UP", txt_fg1, font_size=200, shift_amount=20, is_hollow=True)
    generate_sliced_text("GIVE UP", txt_fg2, font_size=180, shift_amount=15)
    
    pic = slide.shapes.add_picture(txt_fg1, Inches(7.5), Inches(2), width=Inches(4))
    pic.rotation = 3
    pic = slide.shapes.add_picture(txt_fg2, Inches(5.5), Inches(5.5), width=Inches(6))
    pic.rotation = 0

    # 5. Detail/Accent Typography (Native PPTX)
    # Top Right detail text
    txBox = slide.shapes.add_textbox(Inches(9.5), Inches(0.5), Inches(3.5), Inches(1))
    tf = txBox.text_frame
    tf.text = "LOREM IPSUM DOLOR SIT AMET\nHigh impact kinetic typography intro style.\nDesigned via Python PPTX."
    for paragraph in tf.paragraphs:
        for run in paragraph.runs:
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(255, 255, 255)

    # Bottom left date detail
    txBox2 = slide.shapes.add_textbox(Inches(0.5), Inches(6.8), Inches(3), Inches(0.5))
    tf2 = txBox2.text_frame
    p = tf2.paragraphs[0]
    p.text = "1978.08.23 — 2020.01.26"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(255, 255, 255)

    # Clean up temp files
    prs.save(output_pptx_path)
    
    for f in [bg_file, txt_bg1, txt_bg2, subject_file, txt_fg1, txt_fg2]:
        if os.path.exists(f):
            os.remove(f)

    return output_pptx_path
