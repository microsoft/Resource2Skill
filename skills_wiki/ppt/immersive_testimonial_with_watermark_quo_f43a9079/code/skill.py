def create_slide(
    output_pptx_path: str,
    title_text: str = "Homebuy.ie were exceptional throughout our move. We could not recommend Fiona any more highly, especially in this crazy pandemic",
    body_text: str = "Patricia and Michael Kiernan",
    bg_palette: str = "happy couple home real estate", 
    accent_color: tuple = (255, 255, 255), 
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Immersive Testimonial with Watermark Quote Overlay' visual effect.
    """
    import requests
    from io import BytesIO
    from PIL import Image, ImageEnhance
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.oxml import parse_xml

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background Image with Brightness Reduction (-30%) ===
    # Attempt to download a relevant image, fallback to dark slate if offline
    img_url = f"https://source.unsplash.com/featured/1920x1080/?{bg_palette.replace(' ', ',')}"
    
    try:
        resp = requests.get(img_url, timeout=7)
        if resp.status_code == 200:
            img = Image.open(BytesIO(resp.content)).convert("RGB")
            # Reduce brightness to 70% (effectively -30% brightness) to match tutorial
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.70)
            
            bg_io = BytesIO()
            img.save(bg_io, format="JPEG", quality=90)
            bg_io.seek(0)
            slide.shapes.add_picture(bg_io, 0, 0, width=prs.slide_width, height=prs.slide_height)
        else:
            raise ValueError("Invalid response")
    except Exception:
        # Fallback to solid dark slate gray if download fails
        bg = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(40, 45, 50)
        bg.line.fill.background()

    # === Layer 2: Watermark Quote Icon (Semi-Transparent) ===
    # We use a massive double-quote text character and inject XML transparency
    quote_box = slide.shapes.add_textbox(Inches(4.8), Inches(4.2), Inches(3), Inches(3))
    tf_quote = quote_box.text_frame
    tf_quote.word_wrap = False
    p_quote = tf_quote.paragraphs[0]
    p_quote.text = '”'
    p_quote.font.size = Pt(220)
    p_quote.font.name = 'Arial Black'
    p_quote.font.color.rgb = RGBColor(255, 255, 255)

    # Inject 45% Opacity (55% transparent) using lxml
    for run in p_quote.runs:
        rPr = run._r.get_or_add_rPr()
        srgbClr = rPr.xpath(".//a:srgbClr")
        if srgbClr:
            # 45000 = 45% Opacity
            alpha = parse_xml(r'<a:alpha xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" val="45000"/>')
            srgbClr[0].append(alpha)

    # === Layer 3: Main Testimonial Text & Attribution ===
    text_box = slide.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(9.0), Inches(4.5))
    text_box.text_frame.word_wrap = True
    
    # Main Quote
    p_main = text_box.text_frame.paragraphs[0]
    p_main.text = title_text
    p_main.font.size = Pt(36)
    p_main.font.name = 'Arial Black'
    p_main.font.bold = True
    p_main.font.color.rgb = RGBColor(255, 255, 255)

    # Attribution (Author)
    p_attr = text_box.text_frame.add_paragraph()
    p_attr.text = f"\n{body_text}"
    p_attr.font.size = Pt(18)
    p_attr.font.name = 'Arial'
    p_attr.font.italic = True
    p_attr.font.bold = False
    p_attr.font.color.rgb = RGBColor(255, 255, 255)

    # === Layer 4: Brand Logo (Top Right) ===
    logo_box = slide.shapes.add_textbox(Inches(10.0), Inches(0.5), Inches(2.8), Inches(1.0))
    logo_p = logo_box.text_frame.paragraphs[0]
    logo_p.text = "⌂ HOMEBUY.IE"
    logo_p.font.size = Pt(22)
    logo_p.font.name = 'Arial Black'
    logo_p.font.bold = True
    logo_p.font.color.rgb = RGBColor(255, 255, 255)

    prs.save(output_pptx_path)
    return output_pptx_path
