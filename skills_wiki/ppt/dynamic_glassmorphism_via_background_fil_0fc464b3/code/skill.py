import os
import urllib.request
from lxml import etree
from PIL import Image, ImageDraw, ImageFilter
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_slide(
    output_pptx_path: str,
    title_text: str = "ANIMATED GLASS",
    subtitle_text: str = "Effect",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Dynamic Glassmorphism effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide

    # ---------------------------------------------------------
    # 1. Prepare Base Images (Sharp and Blurred)
    # ---------------------------------------------------------
    sharp_path = 'temp_sharp_bg.jpg'
    blur_path = 'temp_blur_bg.jpg'
    icon_path = 'temp_icon.png'

    try:
        # Fetch a beautiful mountain landscape
        url = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1920&q=80"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(sharp_path, 'wb') as f:
                f.write(response.read())
        img = Image.open(sharp_path)
        img_blur = img.filter(ImageFilter.GaussianBlur(30)) # Heavy blur for the frosted effect
        img_blur.save(blur_path)
    except Exception as e:
        print(f"Download failed, creating synthetic fallback images: {e}")
        # Synthetic fallback
        img = Image.new('RGB', (1920, 1080))
        draw = ImageDraw.Draw(img)
        for y in range(1080):
            r, g, b = int(10 + y/1080*20), int(30 + y/1080*40), int(50 + y/1080*80)
            draw.line([(0, y), (1920, y)], fill=(r, g, b))
        draw.polygon([(0, 1080), (600, 500), (1200, 1080)], fill=(20, 40, 60))
        draw.polygon([(800, 1080), (1500, 300), (1920, 1080)], fill=(15, 30, 50))
        img.save(sharp_path)
        img.filter(ImageFilter.GaussianBlur(30)).save(blur_path)

    # Simple icon generation
    icon = Image.new('RGBA', (200, 200), (255, 255, 255, 0))
    draw = ImageDraw.Draw(icon)
    draw.ellipse([(50, 50), (150, 150)], outline=(255, 255, 255, 255), width=8)
    draw.line([(100, 50), (100, 150)], fill=(255, 255, 255, 255), width=8)
    draw.line([(50, 100), (150, 100)], fill=(255, 255, 255, 255), width=8)
    icon.save(icon_path)

    # ---------------------------------------------------------
    # 2. Inject Blurred Image into Slide Background
    # ---------------------------------------------------------
    # Hack: Add dummy picture to generate a valid rId, then remove shape
    dummy_pic = slide.shapes.add_picture(blur_path, 0, 0)
    rId = dummy_pic._element.blipFill.blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
    slide._element.cSld.spTree.remove(dummy_pic._element)

    bg_xml = f'''
    <p:bg xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
          xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
          xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
        <p:bgPr>
            <a:blipFill dpi="72" rotWithShape="0">
                <a:blip r:embed="{rId}">
                    <a:lum/>
                </a:blip>
                <a:srcRect/>
                <a:stretch><a:fillRect/></a:stretch>
            </a:blipFill>
            <a:effectLst/>
        </p:bgPr>
    </p:bg>
    '''
    bg_element = etree.fromstring(bg_xml)
    cSld = slide._element.cSld
    if cSld.bg is not None:
        cSld.remove(cSld.bg)
    cSld.insert(0, bg_element)

    # ---------------------------------------------------------
    # 3. Add Sharp Image as Foreground layer
    # ---------------------------------------------------------
    # This covers the background. Glass shapes will punch through this.
    slide.shapes.add_picture(sharp_path, 0, 0, prs.slide_width, prs.slide_height)

    # ---------------------------------------------------------
    # 4. Add Typography Header
    # ---------------------------------------------------------
    title_box = slide.shapes.add_textbox(Inches(0), Inches(0.8), prs.slide_width, Inches(1.5))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = title_text
    run.font.size = Pt(64)
    run.font.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255)
    title_box.shadow.inherit = False
    title_box.shadow.color.rgb = RGBColor(0, 0, 0)
    title_box.shadow.blur_radius = Pt(15)
    title_box.shadow.distance = Pt(0)

    sub_box = slide.shapes.add_textbox(Inches(0), Inches(1.6), prs.slide_width, Inches(1.0))
    p2 = sub_box.text_frame.paragraphs[0]
    p2.alignment = PP_ALIGN.CENTER
    run2 = p2.add_run()
    run2.text = subtitle_text
    run2.font.size = Pt(48)
    run2.font.italic = True
    run2.font.color.rgb = RGBColor(255, 220, 50)
    sub_box.shadow.inherit = False
    sub_box.shadow.color.rgb = RGBColor(0, 0, 0)
    sub_box.shadow.blur_radius = Pt(10)
    sub_box.shadow.distance = Pt(0)

    # ---------------------------------------------------------
    # 5. Generate Glass Panels via XML Injection
    # ---------------------------------------------------------
    panel_width = Inches(3.0)
    panel_height = Inches(4.0)
    spacing = Inches(1.0)
    start_y = Inches(2.8)
    start_x = (prs.slide_width - (panel_width * 3 + spacing * 2)) / 2

    for i in range(3):
        x = start_x + (panel_width + spacing) * i
        
        # Base Shape
        panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, start_y, panel_width, panel_height)
        panel.adjustments[0] = 0.1 # Rounded corner radius
        panel.line.width = Pt(1.5)
        panel.line.color.rgb = RGBColor(255, 255, 255)
        
        spPr = panel._element.spPr
        
        # A. Inject Slide Background Fill (<a:bgFill>)
        for tag in ['solidFill', 'gradFill', 'pattFill', 'blipFill', 'noFill']:
            fill_elem = spPr.find(f'{{http://schemas.openxmlformats.org/drawingml/2006/main}}{tag}')
            if fill_elem is not None:
                bg_fill_xml = '<a:bgFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'
                spPr.replace(fill_elem, etree.fromstring(bg_fill_xml))
                break

        # B. Inject Gradient Line for Edge Highlight
        ln = spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}ln')
        if ln is not None:
            ln_solid = ln.find('{http://schemas.openxmlformats.org/drawingml/2006/main}solidFill')
            if ln_solid is not None:
                grad_line_xml = '''
                <a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
                    <a:gsLst>
                        <a:gs pos="0"><a:srgbClr val="FFFFFF"><a:alpha val="90000"/></a:srgbClr></a:gs>
                        <a:gs pos="100000"><a:srgbClr val="FFFFFF"><a:alpha val="10000"/></a:srgbClr></a:gs>
                    </a:gsLst>
                    <a:lin ang="18900000" scaled="1"/>
                </a:gradFill>
                '''
                ln.replace(ln_solid, etree.fromstring(grad_line_xml))

        # C. Inject 3D Bevel for Glass Thickness
        sp3d_xml = '''
        <a:sp3d xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:bevelT w="317500" h="127000"/>
            <a:bevelB h="76200"/>
        </a:sp3d>
        '''
        spPr.append(etree.fromstring(sp3d_xml))

        # D. Add subtle drop shadow behind the glass
        panel.shadow.inherit = False
        panel.shadow.color.rgb = RGBColor(0, 0, 0)
        panel.shadow.blur_radius = Pt(20)
        panel.shadow.distance = Pt(5)

        # ---------------------------------------------------------
        # 6. Add Content Inside Panels
        # ---------------------------------------------------------
        # Icon
        icon_size = Inches(0.6)
        slide.shapes.add_picture(icon_path, x + (panel_width - icon_size)/2, start_y + Inches(0.4), icon_size, icon_size)

        # Content Text
        tb = slide.shapes.add_textbox(x, start_y + Inches(1.3), panel_width, Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_title = tf.paragraphs[0]
        p_title.alignment = PP_ALIGN.CENTER
        r_title = p_title.add_run()
        r_title.text = "Lorem Ipsum Dolor"
        r_title.font.size = Pt(16)
        r_title.font.bold = True
        r_title.font.color.rgb = RGBColor(255, 255, 255)
        
        p_body = tf.add_paragraph()
        p_body.alignment = PP_ALIGN.CENTER
        r_body = p_body.add_run()
        r_body.text = "\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas porttitor congue massa."
        r_body.font.size = Pt(11)
        r_body.font.color.rgb = RGBColor(255, 255, 255)
        
        # Text Glow
        tb.shadow.inherit = False
        tb.shadow.color.rgb = RGBColor(255, 255, 255)
        tb.shadow.blur_radius = Pt(12)
        tb.shadow.distance = Pt(0)

    # Cleanup temp files
    for f in [sharp_path, blur_path, icon_path]:
        if os.path.exists(f):
            os.remove(f)

    prs.save(output_pptx_path)
    return output_pptx_path
