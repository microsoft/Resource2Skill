def create_slide(
    output_pptx_path: str,
    title_text: str = "Kevin's Cookie Company",
    body_text: str = "Automated Master Layout Demo",
    bg_palette: str = "white",
    accent_color: tuple = (210, 105, 30),  # Cookie orange/brown
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Unified Master Layout Branding effect.
    Generates a Title slide and a Content slide with programmatic master-level 
    branding (consistent font, anchored logo, and conditional title assets).
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from PIL import Image, ImageDraw
    import os

    # Initialize presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # ==========================================
    # Layer 1: Generate Master Brand Assets via PIL
    # ==========================================
    logo_path = "master_logo_temp.png"
    # Create a nice branded badge
    logo_img = Image.new('RGBA', (250, 80), (255, 255, 255, 0))
    draw_logo = ImageDraw.Draw(logo_img)
    draw_logo.rounded_rectangle([(0,0), (249, 79)], radius=15, fill=(255, 245, 230, 255), outline=accent_color, width=4)
    # Simple geometry to represent a cookie/logo icon
    draw_logo.ellipse([(15, 15), (65, 65)], fill=accent_color)
    draw_logo.ellipse([(25, 25), (35, 35)], fill=(139, 69, 19, 255)) # Choc chip
    draw_logo.ellipse([(45, 35), (55, 45)], fill=(139, 69, 19, 255)) # Choc chip
    draw_logo.text((80, 30), "BRAND LOGO", fill=(0, 0, 0, 255)) 
    logo_img.save(logo_path)

    speaker_path = "master_speaker_temp.png"
    # Create a circular speaker headshot placeholder
    speaker_img = Image.new('RGBA', (200, 200), (255, 255, 255, 0))
    draw_spk = ImageDraw.Draw(speaker_img)
    draw_spk.ellipse([(0,0), (199, 199)], fill=(100, 150, 200, 255)) # Blue background
    draw_spk.ellipse([(60, 40), (140, 120)], fill=(200, 200, 200, 255)) # Head
    draw_spk.chord([(30, 120), (170, 260)], start=180, end=0, fill=(200, 200, 200, 255)) # Shoulders
    speaker_img.save(speaker_path)

    # ==========================================
    # Layer 2: Master Formatting Helper
    # ==========================================
    def apply_master_formatting(slide, is_title_layout=False):
        """Mimics editing the Slide Master by globally updating fonts and adding locked assets."""
        # 1. Force Global Font (equivalent to changing master font to Segoe UI)
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        run.font.name = 'Segoe UI'
                        
        # 2. Add anchored Global Logo (Bottom Right)
        slide.shapes.add_picture(logo_path, Inches(10.8), Inches(6.4), width=Inches(2.2))
        
        # 3. Add Layout-Specific Elements (e.g., speaker only on Title Layout)
        if is_title_layout:
            slide.shapes.add_picture(speaker_path, Inches(11.0), Inches(4.2), width=Inches(1.8))

    # ==========================================
    # Layer 3: Slide Generation
    # ==========================================
    
    # --- Slide 1: Title Layout ---
    slide1 = prs.slides.add_slide(prs.slide_layouts[0])
    slide1.shapes.title.text = title_text
    slide1.placeholders[1].text = body_text
    
    # Apply Master Logic
    apply_master_formatting(slide1, is_title_layout=True)

    # --- Slide 2: Content Layout ---
    slide2 = prs.slides.add_slide(prs.slide_layouts[1])
    slide2.shapes.title.text = "Company Progress"
    
    tf = slide2.placeholders[1].text_frame
    tf.text = "Sales should increase exponentially."
    tf.add_paragraph().text = "Customers love our products."
    tf.add_paragraph().text = "Staff love our unified branding."
    
    # Apply Master Logic (Notice is_title_layout is False, so no speaker is added)
    apply_master_formatting(slide2, is_title_layout=False)

    # Clean up temp assets
    try:
        os.remove(logo_path)
        os.remove(speaker_path)
    except:
        pass

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
