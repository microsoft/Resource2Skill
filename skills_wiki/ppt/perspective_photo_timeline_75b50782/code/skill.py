import os
import io
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from PIL import Image, ImageDraw
from lxml import etree

# Helper for XML namespace mapping
ns = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
}

def qn(tag):
    """
    Stands for 'qualified name', a utility function to turn a namespace
    prefixed tag name into a Clark-notation qualified tag name for lxml.
    """
    prefix, tagroot = tag.split(':')
    return '{{{}}}{}'.format(ns[prefix], tagroot)

def create_slide(
    output_pptx_path: str,
    image_keywords: list = ["nature", "mountains", "ocean", "forest", "city", "sky"],
    timeline_dates: list = ["2023.3", "2022.6", "2021.4", "2020.9", "2019.7", "2018.5"],
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the 'Perspective Photo Timeline' effect.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        image_keywords: A list of keywords to search for background images on Unsplash.
        timeline_dates: A list of date strings for the labels.

    Returns:
        The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # --- Layer 1: Background ---
    # Create a dark radial gradient background with PIL
    width, height = prs.slide_width, prs.slide_height
    img = Image.new('RGB', (int(width/Emu(1)*96), int(height/Emu(1)*96)), '#0a0f1e')
    draw = ImageDraw.Draw(img)
    center_x, center_y = img.width / 2, img.height / 2
    max_radius = (img.width**2 + img.height**2)**0.5 / 2
    for i in range(int(max_radius), 0, -1):
        ratio = i / max_radius
        # Interpolate between center color (lighter) and edge color (darker)
        r = int(20 + (10 - 20) * (1-ratio))
        g = int(30 + (15 - 30) * (1-ratio))
        b = int(60 + (30 - 60) * (1-ratio))
        draw.ellipse((center_x-i, center_y-i, center_x+i, center_y+i), fill=(r, g, b))

    bg_image_stream = io.BytesIO()
    img.save(bg_image_stream, format='PNG')
    bg_image_stream.seek(0)
    slide.shapes.add_picture(bg_image_stream, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # --- Layer 2 & 3: Shapes, Text, and Effects ---
    num_items = len(image_keywords)
    slide_shapes = []

    for i in range(num_items):
        # 1. Generate shapes with interpolated size and position (tweening)
        start_w, end_w = Inches(2.5), Inches(1.8)
        start_h, end_h = Inches(3.5), Inches(2.5)
        start_x, end_x = Inches(0.5), Inches(9.5)
        start_y, end_y = Inches(2.0), Inches(1.0)
        
        ratio = i / (num_items - 1) if num_items > 1 else 0
        
        # Linear interpolation
        current_w = start_w + (end_w - start_w) * ratio
        current_h = start_h + (end_h - start_h) * ratio
        current_x = start_x + (end_x - start_x) * ratio
        current_y = start_y + (end_y - start_y) * ratio

        # Create Shape
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, current_x, current_y, current_w, current_h)
        shape.adjustments[0] = 0.1 # Adjust corner radius
        sp = shape.element
        sp.getparent().remove(sp) # Remove and re-add to control z-order
        slide.shapes._spTree.insert(2+i, sp)
        
        # 2. Add Picture Fill using lxml
        try:
            url = f"https://source.unsplash.com/800x1200/?{image_keywords[i]}"
            with urllib.request.urlopen(url) as response:
                image_data = response.read()
            pic = slide.shapes.add_picture(io.BytesIO(image_data), 0, 0)
            rId = pic.part.rId
            pic.element.getparent().remove(pic.element) # remove temp picture
        except Exception:
            # Fallback to a solid fill if image download fails
            rId = None

        spPr = sp.xpath('.//p:spPr', namespaces=ns)[0]
        spPr.remove(spPr.find(qn('a:solidFill'))) # Remove solid fill
        
        if rId:
            blip_fill = etree.SubElement(spPr, qn('a:blipFill'))
            blip = etree.SubElement(blip_fill, qn('a:blip'), {qn('r:embed'): rId})
            stretch = etree.SubElement(blip_fill, qn('a:stretch'))
            etree.SubElement(stretch, qn('a:fillRect'))
        else: # Add solid fill back if image failed
            solidFill = etree.SubElement(spPr, qn('a:solidFill'))
            srgbClr = etree.SubElement(solidFill, qn('a:srgbClr'), val="556677")
            

        # 3. Add 3D Format and Rotation using lxml
        xfrm = spPr.xpath('.//a:xfrm', namespaces=ns)[0]
        # "Off Axis 1 Left" preset rotation
        xfrm.set('rot', '-13200000') 
        
        sp3d = etree.SubElement(spPr, qn('a:sp3d'))
        # 6pt depth
        sp3d.set('contourW', '38100')
        sp3d.set('extrusionH', '76200')
        
        # Add reflection
        reflection = etree.SubElement(spPr, qn('a:reflection'), {
            'dist': '0', 'dir': '0', 'algn': 'b', 'blurRad': '0', 'stA': '60000', 
            'endA': '1000', 'endPos': '90000', 'sy': '-100000'
        })

        # 4. Add and format text
        tx = slide.shapes.add_textbox(current_x - Inches(0.1), current_y + current_h - Inches(0.8), current_w, Inches(1))
        tx.text = timeline_dates[i]
        p = tx.text_frame.paragraphs[0]
        p.font.name = 'Arial Black'
        p.font.size = Pt(28)
        p.font.color.rgb = RGBColor(255, 255, 255)
        
        # Apply same 3D and reflection to textbox shape
        tx_sp = tx.element
        tx_spPr = tx_sp.xpath('.//p:spPr', namespaces=ns)[0]
        tx_xfrm = tx_spPr.xpath('.//a:xfrm', namespaces=ns)[0]
        tx_xfrm.set('rot', '-13200000') # Same rotation
        
        tx_sp3d = etree.SubElement(tx_spPr, qn('a:sp3d'))
        tx_sp3d.set('contourW', '19050') # 3pt depth for text
        tx_sp3d.set('extrusionH', '38100')
        
        tx_reflection = etree.SubElement(tx_spPr, qn('a:reflection'), {
            'dist': '0', 'dir': '0', 'algn': 'b', 'blurRad': '0', 'stA': '60000', 
            'endA': '1000', 'endPos': '90000', 'sy': '-100000'
        })
        slide_shapes.append((shape, tx))


    # 5. Add Animation using lxml
    slide_xml = slide.element
    if slide_xml.find(qn('p:timing')) is None:
        timing = etree.SubElement(slide_xml, qn('p:timing'))
        tnLst = etree.SubElement(timing, qn('p:tnLst'))
        par = etree.SubElement(tnLst, qn('p:par'))
        cTn = etree.SubElement(par, qn('p:cTn'), id="1", dur="indefinite", restart="never", nodeType="tmRoot")
    
    main_seq = etree.SubElement(cTn, qn('p:childTnLst')).find(qn('p:seq'))
    if main_seq is None:
        main_seq = etree.SubElement(cTn, qn('p:childTnLst'))
        main_seq = etree.SubElement(main_seq, qn('p:seq'), concurrent="1", nextAc="seek")
        etree.SubElement(main_seq, qn('p:cTn'), id="2", dur="indefinite", nodeType="mainSeq")
        etree.SubElement(main_seq, qn('p:prevCondLst')).append(etree.Element(qn('p:cond'), delay="indefinite"))
        etree.SubElement(main_seq, qn('p:nextCondLst')).append(etree.Element(qn('p:cond'), delay="indefinite"))

    next_id = 3
    for i, (shape, tx) in enumerate(slide_shapes):
        for s in [shape, tx]:
            spid = s.shape_id
            par_node = etree.SubElement(main_seq, qn('p:par'))
            ctn_par = etree.SubElement(par_node, qn('p:cTn'), id=str(next_id), fill="hold")
            next_id += 1
            st_cond_lst = etree.SubElement(ctn_par, qn('p:stCondLst'))
            # Staggered start delay
            etree.SubElement(st_cond_lst, qn('p:cond'), delay=str(i * 100)) 

            child_tn_lst = etree.SubElement(ctn_par, qn('p:childTnLst'))
            anim_par = etree.SubElement(child_tn_lst, qn('p:par'))
            anim_ctn = etree.SubElement(anim_par, qn('p:cTn'), id=str(next_id), fill="hold", dur="1500")
            next_id += 1
            # Add "Smooth End"
            etree.SubElement(anim_ctn, qn('p:decel'), val="100000") 
            
            anim_child_tn_lst = etree.SubElement(anim_ctn, qn('p:childTnLst'))
            
            # Fly In from Bottom
            anim = etree.SubElement(anim_child_tn_lst, qn('p:anim'), calcmode="lin", valueType="num")
            anim_ctn_inner = etree.SubElement(anim, qn('p:cBhvr'))
            etree.SubElement(anim_ctn_inner, qn('p:cTn'), id=str(next_id), dur="1500")
            next_id += 1
            etree.SubElement(anim_ctn_inner, qn('p:tgtEl')).append(etree.Element(qn('p:spTgt'), spid=str(spid)))
            etree.SubElement(anim_ctn_inner, qn('p:attrNameLst')).append(etree.Element(qn('p:attrName'), val="ppt_y"))
            tav_lst = etree.SubElement(anim, qn('p:tavLst'))
            etree.SubElement(tav_lst, qn('p:tav'), tm="0").append(etree.Element(qn('p:val'), val="100000"))
            etree.SubElement(tav_lst, qn('p:tav'), tm="100000").append(etree.Element(qn('p:val'), val="0"))
            
    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# create_slide("perspective_timeline.pptx")

