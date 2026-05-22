import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR
from lxml import etree

# Helper to register XML namespaces for lxml
_ns = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
}

def _add_shadow_to_shape(shape, angle, dist):
    """
    Adds an outer shadow effect to a shape using lxml.
    angle is in degrees, dist is in EMU.
    """
    shape_element = shape.element
    spPr = shape_element.get_or_add_spPr()
    
    effect_lst = etree.SubElement(spPr, f"{{{_ns['a']}}}effectLst")
    outer_shdw = etree.SubElement(effect_lst, f"{{{_ns['a']}}}outerShdw")
    outer_shdw.set('blurRad', '254000')  # 25 pt blur
    outer_shdw.set('dist', str(dist))    # 3 pt distance
    outer_shdw.set('dir', str(angle * 60000)) # Angle in 60,000ths of a degree
    outer_shdw.set('algn', 'tl')
    outer_shdw.set('rotWithShape', '0')
    
    srgb_clr = etree.SubElement(outer_shdw, f"{{{_ns['a']}}}srgbClr")
    srgb_clr.set('val', 'A9A9A9') # A dark gray color
    alpha = etree.SubElement(srgb_clr, f"{{{_ns['a']}}}alpha")
    alpha.set('val', '37000') # 37% transparency

def _add_motion_path(slide, shape, from_x, from_y, to_x, to_y, start_delay_ms, duration_s):
    """
    Adds a 'Lines' motion path animation to a shape.
    Coordinates are in EMU.
    """
    spTree = slide.shapes.element
    shape_id = shape.shape_id
    shape_name = shape.name

    # Find or create timing elements
    timing = slide.element.find(f".//{{{_ns['p']}}}timing")
    if timing is None:
        cSld = slide.element.find(f".//{{{_ns['p']}}}cSld")
        timing = etree.SubElement(cSld, f"{{{_ns['p']}}}timing")
    
    tnLst = timing.find(f".//{{{_ns['p']}}}tnLst")
    if tnLst is None:
        tnLst = etree.SubElement(timing, f"{{{_ns['p']}}}tnLst")
        
    par = tnLst.find(f".//{{{_ns['p']}}}par")
    if par is None:
        par = etree.SubElement(tnLst, f"{{{_ns['p']}}}par")
        
    cTn = par.find(f".//{{{_ns['p']}}}cTn")
    if cTn is None:
        cTn = etree.SubElement(par, f"{{{_ns['p']}}}cTn", id="1", dur="indefinite", restart="never", nodeType="tmRoot")

    childTnLst = cTn.find(f".//{{{_ns['p']}}}childTnLst")
    if childTnLst is None:
        childTnLst = etree.SubElement(cTn, f"{{{_ns['p']}}}childTnLst")

    # Animation Sequence
    seq = etree.SubElement(childTnLst, f"{{{_ns['p']}}}seq", concurrent="1", nextAc="seek")
    
    prev_cTn_id = len(childTnLst.findall(f".//{{{_ns['p']}}}cTn")) + 1
    
    cTn_seq = etree.SubElement(seq, f"{{{_ns['p']}}}cTn", id=str(prev_cTn_id), fill="hold")
    stCondLst = etree.SubElement(cTn_seq, f"{{{_ns['p']}}}stCondLst")
    etree.SubElement(stCondLst, f"{{{_ns['p']}}}cond", delay=str(start_delay_ms), evt="onPrev")
    
    childTnLst_seq = etree.SubElement(cTn_seq, f"{{{_ns['p']}}}childTnLst")
    par_anim = etree.SubElement(childTnLst_seq, f"{{{_ns['p']}}}par")
    cTn_anim = etree.SubElement(par_anim, f"{{{_ns['p']}}}cTn", id=str(prev_cTn_id + 1), fill="hold")
    stCondLst_anim = etree.SubElement(cTn_anim, f"{{{_ns['p']}}}stCondLst")
    etree.SubElement(stCondLst_anim, f"{{{_ns['p']}}}cond", delay="0")
    
    childTnLst_anim = etree.SubElement(cTn_anim, f"{{{_ns['p']}}}childTnLst")

    # Actual Animation Element
    anim = etree.SubElement(childTnLst_anim, f"{{{_ns['p']}}}anim", calcmode="lin", valueType="str")
    cBhvr = etree.SubElement(anim, f"{{{_ns['p']}}}cBhvr")
    cTn_bhvr = etree.SubElement(cBhvr, f"{{{_ns['p']}}}cTn", id=str(prev_cTn_id + 2), dur=str(int(duration_s * 1000)))
    etree.SubElement(cTn_bhvr, f"{{{_ns['p']}}}stCondLst").append(etree.Element(f"{{{_ns['p']}}}cond", delay="0"))
    tgtEl = etree.SubElement(cBhvr, f"{{{_ns['p']}}}tgtEl")
    etree.SubElement(tgtEl, f"{{{_ns['p']}}}spTgt", spid=str(shape_id))
    
    tavLst = etree.SubElement(cBhvr, f"{{{_ns['p']}}}tavLst")
    etree.SubElement(tavLst, f"{{{_ns['p']}}}tav", tm="0").append(etree.Element(f"{{{_ns['p']}}}val").append(etree.Element(f"{{{_ns['p']}}}strVal", val="#ppt_x")))
    etree.SubElement(tavLst, f"{{{_ns['p']}}}tav", tm="100000").append(etree.Element(f"{{{_ns['p']}}}val").append(etree.Element(f"{{{_ns['p']}}}strVal", val="#ppt_x")))
    
    anim_motion = etree.SubElement(childTnLst_anim, f"{{{_ns['p']}}}animMotion", origin="layout", pathEditMode="relative", rAng="0")
    cBhvr_motion = etree.SubElement(anim_motion, f"{{{_ns['p']}}}cBhvr")
    cTn_motion = etree.SubElement(cBhvr_motion, f"{{{_ns['p']}}}cTn", id=str(prev_cTn_id + 3), dur=str(int(duration_s * 1000)))
    etree.SubElement(cTn_motion, f"{{{_ns['p']}}}stCondLst").append(etree.Element(f"{{{_ns['p']}}}cond", delay="0"))
    
    tgtEl_motion = etree.SubElement(cBhvr_motion, f"{{{_ns['p']}}}tgtEl")
    etree.SubElement(tgtEl_motion, f"{{{_ns['p']}}}spTgt", spid=str(shape_id))
    
    attrNameLst = etree.SubElement(cBhvr_motion, f"{{{_ns['p']}}}attrNameLst")
    etree.SubElement(attrNameLst, f"{{{_ns['p']}}}attrName").text = "ppt_x"
    etree.SubElement(attrNameLst, f"{{{_ns['p']}}}attrName").text = "ppt_y"
    
    etree.SubElement(anim_motion, f"{{{_ns['p']}}}from", x=str(from_x), y=str(from_y))
    etree.SubElement(anim_motion, f"{{{_ns['p']}}}to", x=str(to_x), y=str(to_y))

def create_slide(
    output_pptx_path: str,
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with a dynamic, diagonal kinetic typography layout.
    
    Returns: Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(242, 242, 242)

    # === Layer 2: Diagonal Shapes & Shadows ===
    # Left Shape (Orange)
    left_shape_vtx = [
        (0, 0), 
        (Inches(6.7), 0), 
        (Inches(1.7), Inches(7.5)), 
        (0, Inches(7.5))
    ]
    left_shape = slide.shapes.add_freeform_shape(left_shape_vtx)
    fill = left_shape.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(237, 85, 42)
    left_shape.line.fill.background()
    _add_shadow_to_shape(left_shape, angle=45, dist=Emu(27432)) # 45 degrees, 3pt

    # Right Shape (Blue)
    right_shape_vtx = [
        (Inches(11.63), 0),
        (Inches(13.333), 0),
        (Inches(13.333), Inches(7.5)),
        (Inches(6.63), Inches(7.5))
    ]
    right_shape = slide.shapes.add_freeform_shape(right_shape_vtx)
    fill = right_shape.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(29, 172, 214)
    right_shape.line.fill.background()
    _add_shadow_to_shape(right_shape, angle=225, dist=Emu(27432)) # 225 degrees, 3pt

    # === Layer 3: Text & Content ===
    # Angle for text rotation
    ROTATION_ANGLE = -45

    # Text Block 1 (Left side)
    tb1 = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(3), Inches(1))
    tb1.text_frame.text = "LEARN"
    p1 = tb1.text_frame.paragraphs[0]
    p1.font.name = 'Century Gothic'
    p1.font.bold = True
    p1.font.size = Pt(88)
    p1.font.color.rgb = RGBColor(45, 45, 45)
    tb1.rotation = ROTATION_ANGLE

    tb2 = slide.shapes.add_textbox(Inches(0.5), Inches(1.8), Inches(4), Inches(1))
    tb2.text_frame.text = "HOW TO CREATE"
    p2 = tb2.text_frame.paragraphs[0]
    p2.font.name = 'Dosis'
    p2.font.bold = True
    p2.font.size = Pt(72)
    p2.font.color.rgb = RGBColor(255, 255, 255)
    tb2.rotation = ROTATION_ANGLE
    
    # Text Block 2 (Center)
    tb3 = slide.shapes.add_textbox(Inches(3.2), Inches(3.2), Inches(6), Inches(1.5))
    tb3.text_frame.text = "BASIC MOTION\nGRAPHICS"
    p3_1 = tb3.text_frame.paragraphs[0]
    p3_1.font.name = 'Century Gothic'
    p3_1.font.bold = True
    p3_1.font.size = Pt(72)
    p3_1.font.color.rgb = RGBColor(45, 45, 45)
    p3_2 = tb3.text_frame.paragraphs[1]
    p3_2.font.name = 'Century Gothic'
    p3_2.font.bold = True
    p3_2.font.size = Pt(80)
    p3_2.font.color.rgb = RGBColor(237, 85, 42)
    tb3.rotation = ROTATION_ANGLE

    # Ampersand
    tb4 = slide.shapes.add_textbox(Inches(7.5), Inches(0.5), Inches(3), Inches(3))
    tb4.text_frame.text = "&"
    p4 = tb4.text_frame.paragraphs[0]
    p4.font.name = 'Century Gothic'
    p4.font.size = Pt(199)
    p4.font.color.rgb = RGBColor(29, 172, 214)
    tb4.rotation = ROTATION_ANGLE

    # Text Block 3 (Right side)
    tb5 = slide.shapes.add_textbox(Inches(9), Inches(3), Inches(4), Inches(1))
    tb5.text_frame.text = "KINETIC"
    p5 = tb5.text_frame.paragraphs[0]
    p5.font.name = 'Century Gothic'
    p5.font.bold = True
    p5.font.size = Pt(88)
    p5.font.color.rgb = RGBColor(45, 45, 45)
    tb5.rotation = ROTATION_ANGLE

    tb6 = slide.shapes.add_textbox(Inches(9), Inches(4.3), Inches(4), Inches(1))
    tb6.text_frame.text = "TYPOGRAPHY"
    p6 = tb6.text_frame.paragraphs[0]
    p6.font.name = 'Dosis'
    p6.font.bold = True
    p6.font.size = Pt(72)
    p6.font.color.rgb = RGBColor(255, 255, 255)
    tb6.rotation = ROTATION_ANGLE
    
    # === Layer 4: Animation ===
    # Animate "LEARN" text box
    tb1.name = "LearnTextBox"
    _add_motion_path(slide, tb1, from_x="-0.25", from_y="0", to_x="0", to_y="0", start_delay_ms=250, duration_s=0.75)
    
    # Animate "HOW TO CREATE" text box
    tb2.name = "HowToTextBox"
    _add_motion_path(slide, tb2, from_x="0", from_y="-0.25", to_x="0", to_y="0", start_delay_ms=350, duration_s=0.75)
    
    # Animate "KINETIC" text box
    tb5.name = "KineticTextBox"
    _add_motion_path(slide, tb5, from_x="0.25", from_y="0", to_x="0", to_y="0", start_delay_ms=450, duration_s=0.75)

    prs.save(output_pptx_path)
    return output_pptx_path
