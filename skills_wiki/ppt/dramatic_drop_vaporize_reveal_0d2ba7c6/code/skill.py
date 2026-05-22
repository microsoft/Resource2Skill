import requests
import io
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    main_text: str = "超额完成",
    accent_text: str = "154%",
    bg_keyword: str = "night sky",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a 'Dramatic Drop & Vaporize Reveal' effect.

    This function programmatically builds the complex animation sequence by injecting
    Open XML into the slide, a capability not available in the standard python-pptx API.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        main_text: The primary text to be displayed.
        accent_text: The highlighted portion of the text.
        bg_keyword: A keyword for fetching a background image from Unsplash.

    Returns:
        Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- XML Namespace Helper ---
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    }
    def qn(tag):
        prefix, V = tag.split(':')
        return f'{{{ns[prefix]}}}{V}'

    # === Layer 1: Background ===
    try:
        bg_url = f"https://source.unsplash.com/1280x720/?{bg_keyword}"
        response = requests.get(bg_url, timeout=10)
        if response.status_code == 200:
            slide.shapes.add_picture(io.BytesIO(response.content), 0, 0, width=prs.slide_width, height=prs.slide_height)
        else:
            raise Exception("Failed to download background")
    except Exception:
        # Fallback to a gradient background
        img = Image.new('RGB', (1280, 720))
        draw = ImageDraw.Draw(img)
        for i in range(720):
            r = int(10 + (30 * i / 720))
            g = int(20 + (40 * i / 720))
            b = int(40 + (80 * i / 720))
            draw.line([(0, i), (1280, i)], fill=(r, g, b))
        with io.BytesIO() as output:
            img.save(output, format="PNG")
            slide.shapes.add_picture(output, 0, 0, width=prs.slide_width, height=prs.slide_height)
            
    # === Layer 2: Smoke Element ===
    try:
        smoke_url = "https://github.com/git-xiaotian/fast-photo/blob/main/ppt-asset/smoke-effect.png?raw=true"
        response = requests.get(smoke_url, timeout=10)
        smoke_pic = slide.shapes.add_picture(
            io.BytesIO(response.content),
            Inches(1.66), Inches(2.75), width=Inches(10)
        )
    except Exception as e:
        print(f"Could not download smoke asset, skipping: {e}")
        smoke_pic = None

    # === Layer 3: Text Element ===
    txBox = slide.shapes.add_textbox(Inches(1.66), Inches(3.2), Inches(10), Inches(1.5))
    p = txBox.text_frame.paragraphs[0]
    p.font.name = 'Arial Black'
    p.font.size = Pt(80)
    p.font.bold = True
    p.alignment = 1 # Center

    run1 = p.add_run()
    run1.text = main_text + " "
    run1.font.color.rgb = RGBColor(255, 255, 255)

    run2 = p.add_run()
    run2.text = accent_text
    run2.font.color.rgb = RGBColor(255, 192, 0)
    
    # --- Move text to front layer ---
    txBox.element.getparent().remove(txBox.element)
    txBox.element.getparent().append(txBox.element)

    # === Step 4: Animation Injection via lxml ===
    if not smoke_pic:
         prs.save(output_pptx_path)
         return output_pptx_path

    # Get shape IDs
    text_shape_id = txBox.shape_id
    smoke_shape_id = smoke_pic.shape_id

    # Find or create the timing element
    tree = slide.part.element
    timing = tree.find(qn('p:timing'))
    if timing is None:
        timing = etree.SubElement(tree, qn('p:timing'))
    
    tnLst = timing.find(qn('p:tnLst'))
    if tnLst is None:
        tnLst = etree.SubElement(timing, qn('p:tnLst'))

    # Main sequence container (parallel, as everything happens on one click)
    main_par = etree.SubElement(tnLst, qn('p:par'))
    main_ctn = etree.SubElement(main_par, qn('p:cTn'), id=str(1), dur="indefinite", restart="never", nodeType="tmRoot")
    child_seq = etree.SubElement(main_ctn, qn('p:childTnLst'))
    
    # Click trigger
    click_par = etree.SubElement(child_seq, qn('p:par'))
    click_ctn = etree.SubElement(click_par, qn('p:cTn'), id=str(2), fill="hold")
    etree.SubElement(click_ctn, qn('p:stCondLst')).append(etree.Element(qn('p:cond'), delay="indefinite"))
    etree.SubElement(click_ctn, qn('p:endCondLst')).append(etree.Element(qn('p:cond'), evt="end", delay="0"))
    
    anim_child_tn_lst = etree.SubElement(click_ctn, qn('p:childTnLst'))
    
    # 1. Text Animation: Fly In with Bounce
    text_anim_par = etree.SubElement(anim_child_tn_lst, qn('p:par'))
    text_anim_ctn = etree.SubElement(text_anim_par, qn('p:cTn'), id=str(3), fill="hold", presetID="1", presetClass="entr", presetSubtype="8", nodeType="clickEffect")
    etree.SubElement(text_anim_ctn, qn('p:stCondLst')).append(etree.Element(qn('p:cond'), delay="0"))
    etree.SubElement(text_anim_ctn, qn('p:endSync'), evt="end", delay="0")
    
    tgt_el = etree.SubElement(text_anim_ctn, qn('p:tgtEl'))
    etree.SubElement(tgt_el, qn('p:spTgt'), spid=str(text_shape_id))
    
    attr_name_lst = etree.SubElement(etree.SubElement(text_anim_ctn, qn('p:attrNameLst')), qn('p:attrName'))
    attr_name_lst.text = "style.visibility"
    
    # Bounce End Effect
    bld_sub = etree.SubElement(text_anim_ctn, qn('p:subTnLst'))
    bld_ctn = etree.SubElement(bld_sub, qn('p:par'))
    bld_p = etree.SubElement(bld_ctn, qn('p:cTn'), id=str(4), dur="300", fill="hold")
    etree.SubElement(bld_p, qn('p:stCondLst')).append(etree.Element(qn('p:cond'), delay="0"))
    bld_anim = etree.SubElement(etree.SubElement(bld_p, qn('p:childTnLst')), qn('p:anim'), bounceEnd="10000", calcmode="lin", valueType="num")
    etree.SubElement(bld_anim, qn('p:cBhvr')).append(etree.Element(qn('p:cTn'), id=str(5), dur="300"))
    etree.SubElement(bld_anim, qn('p:tavLst')).append(etree.Element(qn('p:tav'), tm="0"))
    
    # 2. Smoke Animations (All running in parallel with the text)
    smoke_anim_par = etree.SubElement(anim_child_tn_lst, qn('p:par'))
    smoke_anim_ctn = etree.SubElement(smoke_anim_par, qn('p:cTn'), id=str(6))
    etree.SubElement(smoke_anim_ctn, qn('p:stCondLst')).append(etree.Element(qn('p:cond'), delay="0"))
    smoke_child_tn_lst = etree.SubElement(smoke_anim_ctn, qn('p:childTnLst'))

    # 2a. Smoke Entrance: Zoom In (0.25s)
    smoke_zoom_par = etree.SubElement(smoke_child_tn_lst, qn('p:par'))
    smoke_zoom_ctn = etree.SubElement(smoke_zoom_par, qn('p:cTn'), id=str(7), dur="250", fill="hold", presetID="5", presetClass="entr", presetSubtype="0", nodeType="withEffect")
    etree.SubElement(smoke_zoom_ctn, qn('p:stCondLst')).append(etree.Element(qn('p:cond'), delay="0"))
    etree.SubElement(etree.SubElement(smoke_zoom_ctn, qn('p:tgtEl')), qn('p:spTgt'), spid=str(smoke_shape_id))

    # 2b. Smoke Emphasis: Grow (1.25s)
    smoke_grow_par = etree.SubElement(smoke_child_tn_lst, qn('p:par'))
    smoke_grow_ctn = etree.SubElement(smoke_grow_par, qn('p:cTn'), id=str(8), dur="1250", fill="hold", presetID="17", presetClass="emph", presetSubtype="0", nodeType="withEffect")
    etree.SubElement(smoke_grow_ctn, qn('p:stCondLst')).append(etree.Element(qn('p:cond'), delay="0"))
    etree.SubElement(etree.SubElement(smoke_grow_ctn, qn('p:tgtEl')), qn('p:spTgt'), spid=str(smoke_shape_id))
    etree.SubElement(etree.SubElement(etree.SubElement(smoke_grow_ctn, qn('p:animScale')), qn('p:to')), qn('a:val'), x="300000", y="300000")

    # 2c. Smoke Exit: Fade Out (1.25s)
    smoke_fade_par = etree.SubElement(smoke_child_tn_lst, qn('p:par'))
    smoke_fade_ctn = etree.SubElement(smoke_fade_par, qn('p:cTn'), id=str(9), dur="1250", fill="hold", presetID="2", presetClass="exit", presetSubtype="0", nodeType="withEffect")
    etree.SubElement(smoke_fade_ctn, qn('p:stCondLst')).append(etree.Element(qn('p:cond'), delay="0"))
    etree.SubElement(etree.SubElement(smoke_fade_ctn, qn('p:tgtEl')), qn('p:spTgt'), spid=str(smoke_shape_id))

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# create_slide("dramatic_reveal.pptx", main_text="产品年销量", accent_text="2500 万台", bg_keyword="city night")

