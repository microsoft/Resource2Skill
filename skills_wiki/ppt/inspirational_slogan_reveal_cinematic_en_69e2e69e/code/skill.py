def create_slide(
    output_pptx_path: str,
    title_text: str = "AIM HIGH. EXECUTE FASTER.",
    watermark_text: str = "2024",
    metadata_text: str = "Presenter: Steven | Department of Strategy\nDecember 2024",
    bg_image_url: str = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1200&auto=format&fit=crop",
    **kwargs,
) -> str:
    """
    Creates an impactful "Cinematic Slogan End Page" replacing the generic "Thank You" slide.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.enum.shapes import MSO_SHAPE
    import urllib.request
    import io
    from PIL import Image

    # 1. Initialize Presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # 2. Generate Background with Dark Overlay via PIL
    bg_io = io.BytesIO()
    try:
        # Download image
        req = urllib.request.Request(bg_image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            bg_img = Image.open(io.BytesIO(response.read())).convert("RGBA")
        
        # Resize/Crop to match 16:9 approx
        target_size = (1280, 720)
        bg_img = bg_img.resize(target_size, Image.Resampling.LANCZOS)
        
        # Create dark overlay (Deep Navy Blue with ~60% opacity)
        overlay_color = (13, 17, 28, 160)
        overlay = Image.new('RGBA', target_size, overlay_color)
        
        # Composite
        final_bg = Image.alpha_composite(bg_img, overlay)
        final_bg.convert("RGB").save(bg_io, format='PNG')
    except Exception as e:
        # Fallback to solid dark gradient-like color if download fails
        fallback = Image.new('RGB', (1280, 720), (20, 30, 50))
        fallback.save(bg_io, format='PNG')
    
    bg_io.seek(0)
    
    # Insert Background
    slide.shapes.add_picture(bg_io, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # 3. Add Giant "Watermark" Text (Simulating Transparency)
    # Using a muted blue-gray color creates the optical illusion of transparent white on dark blue.
    watermark_box = slide.shapes.add_textbox(Inches(0), Inches(1.5), prs.slide_width, Inches(3))
    tf_wm = watermark_box.text_frame
    tf_wm.word_wrap = True
    p_wm = tf_wm.paragraphs[0]
    p_wm.text = watermark_text
    p_wm.alignment = PP_ALIGN.CENTER
    font_wm = p_wm.font
    font_wm.name = "Arial Black"
    font_wm.size = Pt(160)
    font_wm.bold = True
    font_wm.color.rgb = RGBColor(50, 70, 110) # Simulated Alpha

    # 4. Add Main Slogan - Drop Shadow Layer
    # Placed exactly +0.05 inches offset
    offset = 0.05
    shadow_box = slide.shapes.add_textbox(Inches(offset), Inches(2.8 + offset), prs.slide_width, Inches(2))
    tf_shadow = shadow_box.text_frame
    tf_shadow.word_wrap = True
    p_shadow = tf_shadow.paragraphs[0]
    p_shadow.text = title_text
    p_shadow.alignment = PP_ALIGN.CENTER
    font_shadow = p_shadow.font
    font_shadow.name = "Arial"
    font_shadow.size = Pt(65)
    font_shadow.bold = True
    font_shadow.color.rgb = RGBColor(10, 10, 10)

    # 5. Add Main Slogan - Pure White Layer
    slogan_box = slide.shapes.add_textbox(Inches(0), Inches(2.8), prs.slide_width, Inches(2))
    tf_slogan = slogan_box.text_frame
    tf_slogan.word_wrap = True
    p_slogan = tf_slogan.paragraphs[0]
    p_slogan.text = title_text
    p_slogan.alignment = PP_ALIGN.CENTER
    font_slogan = p_slogan.font
    font_slogan.name = "Arial"
    font_slogan.size = Pt(65)
    font_slogan.bold = True
    font_slogan.color.rgb = RGBColor(255, 255, 255)

    # 6. Add Bottom Anchor Frame
    frame_height = Inches(1.8)
    top_pos = prs.slide_height - frame_height
    anchor_rect = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, top_pos, prs.slide_width, frame_height
    )
    anchor_rect.fill.solid()
    anchor_rect.fill.fore_color.rgb = RGBColor(255, 255, 255)
    anchor_rect.line.fill.background() # No border

    # Add a thin accent line sitting right on top of the anchor block
    accent_line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, top_pos, prs.slide_width, Pt(3)
    )
    accent_line.fill.solid()
    accent_line.fill.fore_color.rgb = RGBColor(0, 100, 200) # Brand blue accent
    accent_line.line.fill.background()

    # 7. Add Metadata into the Anchor Frame
    meta_box = slide.shapes.add_textbox(
        Inches(1), top_pos + Inches(0.4), prs.slide_width - Inches(2), Inches(1)
    )
    tf_meta = meta_box.text_frame
    tf_meta.word_wrap = True
    p_meta = tf_meta.paragraphs[0]
    p_meta.text = metadata_text
    p_meta.alignment = PP_ALIGN.CENTER
    font_meta = p_meta.font
    font_meta.name = "Arial"
    font_meta.size = Pt(16)
    font_meta.bold = False
    font_meta.color.rgb = RGBColor(60, 60, 60)

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
