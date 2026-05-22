def create_slide(
    output_pptx_path: str,
    title_text: str = "NYC",
    body_text: str = "PRESENTATION",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the "Depth-Layered Interlocking Title" effect.
    Uses layered images and XML-injected text shadows to sandwich text behind a foreground subject.
    """
    import os
    import urllib.request
    from pptx import Presentation
    from pptx.util import Pt, Pt
    from pptx.dml.color import RGBColor
    from pptx.oxml import parse_xml
    from PIL import Image, ImageDraw, ImageFilter
    
    prs = Presentation()
    # 16:9 Widescreen format
    prs.slide_width = Pt(960)
    prs.slide_height = Pt(540)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide
    
    bg_img_path = "temp_bg.jpg"
    fg_img_path = "temp_fg.png"
    
    # 1. Prepare Background Image (Skyline)
    try:
        # A scenic skyline image
        req = urllib.request.Request(
            "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?q=80&w=1920&auto=format&fit=crop",
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response, open(bg_img_path, 'wb') as out_file:
            out_file.write(response.read())
    except Exception:
        # Fallback background
        bg = Image.new('RGB', (1920, 1080), color=(230, 225, 220))
        bg.save(bg_img_path)

    # 2. Prepare Foreground Image (To simulate the isolated object)
    try:
        # A transparent PNG of a skyscraper/building to act as the occluding layer
        req = urllib.request.Request(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Empire_State_Building_transparent.png/400px-Empire_State_Building_transparent.png",
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response, open(fg_img_path, 'wb') as out_file:
            out_file.write(response.read())
            
        # Resize to fit height
        fg = Image.open(fg_img_path).convert("RGBA")
        aspect = fg.width / fg.height
        new_height = int(prs.slide_height)
        new_width = int(new_height * aspect)
        fg = fg.resize((new_width, new_height), Image.Resampling.LANCZOS)
        fg.save(fg_img_path)
    except Exception:
        # Fallback: Create a sleek dark architectural pillar with PIL
        fg = Image.new('RGBA', (300, int(prs.slide_height)), (0, 0, 0, 0))
        draw = ImageDraw.Draw(fg)
        draw.rectangle([50, 0, 300, int(prs.slide_height)], fill=(20, 25, 30, 240))
        fg.save(fg_img_path)

    # === LAYER 1: Background ===
    slide.shapes.add_picture(bg_img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # === LAYER 2: Text (Sandwiched in the middle) ===
    # Title
    txBox = slide.shapes.add_textbox(Pt(200), Pt(180), Pt(500), Pt(150))
    tf = txBox.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = title_text
    run.font.name = "Arial Black" # Standard heavy fallback
    run.font.size = Pt(160)
    run.font.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255)
    
    # Subtitle
    txBox_sub = slide.shapes.add_textbox(Pt(210), Pt(360), Pt(400), Pt(50))
    tf_sub = txBox_sub.text_frame
    p_sub = tf_sub.paragraphs[0]
    run_sub = p_sub.add_run()
    run_sub.text = body_text
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(40)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(255, 255, 255)

    # Apply Drop Shadow using lxml
    # PowerPoint requires this XML inside the <a:rPr> (Run Properties) tag.
    shadow_xml = """
    <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:outerShdw blurRad="101600" dist="38100" dir="2700000" algn="b" rotWithShape="0">
            <a:srgbClr val="000000">
                <a:alpha val="60000"/>
            </a:srgbClr>
        </a:outerShdw>
    </a:effectLst>
    """
    
    for shape in [txBox, txBox_sub]:
        for paragraph in shape.text_frame.paragraphs:
            for run in paragraph.runs:
                rPr = run._r.get_or_add_rPr()
                effect_lst = parse_xml(shadow_xml)
                rPr.append(effect_lst)

    # === LAYER 3: Foreground Subject (The Occlusion Layer) ===
    # Align the foreground object to the right side of the screen, overlapping the text.
    fg_img = Image.open(fg_img_path)
    left_position = prs.slide_width - Pt(fg_img.width) - Pt(50)
    slide.shapes.add_picture(fg_img_path, left_position, 0, height=prs.slide_height)

    prs.save(output_pptx_path)
    
    # Cleanup temps
    if os.path.exists(bg_img_path): os.remove(bg_img_path)
    if os.path.exists(fg_img_path): os.remove(fg_img_path)
    
    return output_pptx_path
