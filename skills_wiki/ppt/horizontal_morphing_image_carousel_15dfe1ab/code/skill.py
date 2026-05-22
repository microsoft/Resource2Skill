def create_slide(
    output_pptx_path: str,
    title_text: str = "Default Title",
    body_text: str = "",
    bg_palette: str = "technology",
    accent_color: tuple = (0, 191, 255),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Horizontal Morphing Image Carousel' effect.
    Generates a sequence of 4 slides to fully demonstrate the Morph transition.
    
    Returns: path to the saved PPTX file.
    """
    import os
    import urllib.request
    from PIL import Image
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from lxml import etree

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Demo content sequence
    topics = [
        ("TOPIC 01", "The Jewelled Beetle", "https://images.unsplash.com/photo-1532822160912-78d12fc0c7cb?w=500&q=80"),
        ("TOPIC 02", "The Paper Kite Butterfly", "https://images.unsplash.com/photo-1550236520-7050f3582da0?w=500&q=80"),
        ("TOPIC 03", "The Golden Hour Stag", "https://images.unsplash.com/photo-1484406593171-41b7938c9143?w=500&q=80"),
        ("TOPIC 04", "The Green Sprout", "https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?w=500&q=80"),
        ("TOPIC 05", "The Pink Cosmos", "https://images.unsplash.com/photo-1463319611694-4bf9eb5a6e72?w=500&q=80"),
        ("TOPIC 06", "The Common Kingfisher", "https://images.unsplash.com/photo-1552728089-57169264c70a?w=500&q=80")
    ]

    # Step 1: Download and center-crop images to perfect squares via PIL
    img_paths = []
    for i, (_, _, url) in enumerate(topics):
        path = f"temp_carousel_img_{i}.jpg"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                with open(path, 'wb') as f:
                    f.write(response.read())
            img = Image.open(path)
            w, h = img.size
            size = min(w, h)
            left, top = (w - size) / 2, (h - size) / 2
            right, bottom = (w + size) / 2, (h + size) / 2
            img = img.crop((left, top, right, bottom)) # Force 1:1 ratio
            img.save(path)
        except Exception:
            # Fallback if download fails
            img = Image.new('RGB', (500, 500), color=(100 + i*20, 150, 200))
            img.save(path)
        img_paths.append(path)

    # Layout Math Variables
    Y_c = 4.6               # Vertical center for the circles
    D_large = 4.5           # Active circle diameter
    D_small = 2.5           # Inactive circle diameter
    G = 0.5                 # Horizontal gap between shapes
    X_center = 13.333 / 2   # Horizontal center of the slide

    # Step 2: Generate slides to show the progression/morph
    num_slides_to_demo = 4
    for active_idx in range(num_slides_to_demo):
        slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
        
        # Set clean white background
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = RGBColor(255, 255, 255)

        # Step 3: Inject Morph Transition XML safely according to schema
        slide_element = slide._element
        transition = etree.Element('{http://schemas.openxmlformats.org/presentationml/2006/main}transition')
        transition.set('spd', 'slow')
        morph = etree.SubElement(transition, '{http://schemas.openxmlformats.org/presentationml/2006/main}morph')
        morph.set('option', 'byObject')
        
        # Insert transition immediately after the cSld element to prevent schema validation errors
        cSld = slide_element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}cSld')
        if cSld is not None:
            slide_element.insert(slide_element.index(cSld) + 1, transition)

        # Step 4: Render all topics dynamically based on their distance to the active index
        for i, (top_text, bot_text, _) in enumerate(topics):
            dist = i - active_idx
            
            # Spatial calculations
            if dist == 0:
                d = D_large
                x = X_center
            elif dist > 0:
                x = X_center + (D_large/2) + G + (D_small/2) + (dist - 1) * (D_small + G)
                d = D_small
            else:
                x = X_center - (D_large/2) - G - (D_small/2) - (abs(dist) - 1) * (D_small + G)
                d = D_small

            # Create Circle Shape
            left = Inches(x - d/2)
            top = Inches(Y_c - d/2)
            shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, Inches(d), Inches(d))
            
            # Using '!!' forces strict morph tracking in PPT for flawless animation
            shape.name = f"!!TopicCircle_{i}" 
            shape.fill.user_picture(img_paths[i])
            
            # Visual emphasis for the active circle
            if dist == 0:
                shape.line.fill.solid()
                shape.line.fill.fore_color.rgb = RGBColor(0, 0, 0)
                shape.line.width = Pt(1.5)
            else:
                shape.line.fill.background()

            # Create Typography
            if dist == 0:
                tw = 6.0
                ty = Y_c - d/2 - 1.2
                fontsize_top, fontsize_bot = Pt(16), Pt(28)
                font_weight = True
            else:
                tw = 4.0
                ty = Y_c - d/2 - 0.8
                fontsize_top, fontsize_bot = Pt(11), Pt(14)
                font_weight = False

            tx = x - tw/2
            tb = slide.shapes.add_textbox(Inches(tx), Inches(ty), Inches(tw), Inches(1))
            tb.name = f"!!TopicText_{i}"
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            
            # Top label text (e.g. "TOPIC 01")
            run = p.add_run()
            run.text = top_text + "\n"
            run.font.size = fontsize_top
            run.font.color.rgb = RGBColor(120, 120, 120)
            run.font.name = "Calibri Light"

            # Bottom title text
            run2 = p.add_run()
            run2.text = bot_text
            run2.font.size = fontsize_bot
            run2.font.color.rgb = RGBColor(30, 30, 30)
            run2.font.bold = font_weight
            run2.font.name = "Calibri"

    # Cleanup temporary cropped images
    for path in img_paths:
        if os.path.exists(path):
            os.remove(path)

    prs.save(output_pptx_path)
    return output_pptx_path
