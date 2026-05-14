def create_slide(
    output_pptx_path: str,
    title_text: str = "Mr. Li's Coffee Workshop",
    body_text: str = "Brand Identity & Merchandise Application",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the "Curated Identity Moodboard Grid" 
    with floating UI-style shadow cards.
    """
    import os
    import urllib.request
    from io import BytesIO
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.oxml import parse_xml
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw, ImageFont

    # --- Setup Presentation ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide

    # --- Background Color ---
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 247) # UI Off-white

    # --- Helper: Image Fetcher with PIL Fallback ---
    def get_image_stream(url, fallback_color, fallback_text):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                return BytesIO(response.read())
        except Exception:
            # Fallback PIL generation
            img = Image.new('RGB', (800, 800), color=fallback_color)
            draw = ImageDraw.Draw(img)
            # Try to load a standard font, fallback to default
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except IOError:
                font = ImageFont.load_default()
            
            # Simple text centering
            text_bbox = draw.textbbox((0, 0), fallback_text, font=font)
            w = text_bbox[2] - text_bbox[0]
            h = text_bbox[3] - text_bbox[1]
            draw.text(((800-w)/2, (800-h)/2), fallback_text, font=font, fill=(255,255,255))
            
            stream = BytesIO()
            img.save(stream, format='PNG')
            stream.seek(0)
            return stream

    # --- Helper: OOXML Soft Drop Shadow Injector ---
    def add_floating_shadow(picture_shape):
        """Injects a modern, soft drop shadow via OOXML"""
        # blurRad: 400000 EMUs (~4mm), dist: 50000 EMUs (~0.5mm), dir: 5400000 (90 degrees / straight down)
        # alpha: 15000 (15% opacity)
        shadow_xml = """
        <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:outerShdw blurRad="400000" dist="50000" dir="5400000" algn="b" rotWithShape="0">
                <a:srgbClr val="000000">
                    <a:alpha val="15000"/>
                </a:srgbClr>
            </a:outerShdw>
        </a:effectLst>
        """
        effect_lst = parse_xml(shadow_xml)
        picture_shape._element.spPr.append(effect_lst)

    # --- Header Texts ---
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(8), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(29, 29, 31)
    p.font.name = "Arial"

    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(8), Inches(0.5))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = body_text
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = RGBColor(134, 134, 139)
    p_sub.font.name = "Arial"

    # --- Grid Configuration ---
    # Define images: (url, x, y, width, height, fallback_color, label)
    # Using thematic Unsplash source URLs for Coffee/Branding
    grid_items = [
        # Hero Image (Left)
        ("https://images.unsplash.com/photo-1497935586351-b67a49e012bf?auto=format&fit=crop&w=800&q=80", 
         0.8, 2.0, 5.5, 4.8, (139, 105, 20), "1. Primary Logo Concept"),
        
        # Top Right (Wide Application)
        ("https://images.unsplash.com/photo-1541167760496-1628856ab772?auto=format&fit=crop&w=800&q=80", 
         6.6, 2.0, 5.9, 2.25, (85, 107, 47), "2. Tote Bag Merchandise"),
        
        # Bottom Middle (Square Application)
        ("https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=800&q=80", 
         6.6, 4.55, 2.8, 2.25, (160, 82, 45), "3. Coffee Cup Render"),
        
        # Bottom Right (Square Application)
        ("https://images.unsplash.com/photo-1559525839-b184a4d698c7?auto=format&fit=crop&w=800&q=80", 
         9.7, 4.55, 2.8, 2.25, (70, 130, 180), "4. T-Shirt Application")
    ]

    # --- Render Grid ---
    for url, x, y, w, h, fb_color, label in grid_items:
        # Fetch & Insert Image
        img_stream = get_image_stream(url, fb_color, label.split('.')[1].strip())
        pic = slide.shapes.add_picture(img_stream, Inches(x), Inches(y), width=Inches(w), height=Inches(h))
        
        # Crop to fill shape (simulate object-fit: cover)
        # In python-pptx, setting exact width/height distorts unless cropped. 
        # For simplicity in this script, we assume images are close to the aspect ratio, 
        # but the OOXML shadow is the main focus.
        
        # Add the floating OOXML shadow
        add_floating_shadow(pic)

        # Add clean, small label under/over image
        lbl_box = slide.shapes.add_textbox(Inches(x), Inches(y + h + 0.05), Inches(w), Inches(0.3))
        lbl_tf = lbl_box.text_frame
        lbl_tf.margin_top = lbl_tf.margin_bottom = lbl_tf.margin_left = lbl_tf.margin_right = 0
        lbl_p = lbl_tf.paragraphs[0]
        lbl_p.text = label
        lbl_p.font.size = Pt(11)
        lbl_p.font.bold = True
        lbl_p.font.color.rgb = RGBColor(134, 134, 139)

    # Save output
    prs.save(output_pptx_path)
    return output_pptx_path

# To test the function:
# create_slide("brand_moodboard_showcase.pptx")
