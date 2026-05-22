import os
import urllib.request
from io import BytesIO

from pptx import Presentation
from pptx.util import Inches, Emu
from PIL import Image, ImageDraw
from lxml import etree

# Helper function to create XML elements with correct namespace prefixes
_nsmap = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
}

def qn(tag):
    prefix, tagroot = tag.split(':')
    return '{{{}}}{}'.format(_nsmap[prefix], tagroot)

def create_slide(
    output_pptx_path: str,
    image_url: str = "https://images.unsplash.com/photo-1574538171036-626a787b2576?w=1280",
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with an animated 'spotlight reveal' effect.

    A black overlay with a circular hole moves across a background image to reveal
    parts of it, then disappears to show the full image.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        image_url: URL of the background image to use.

    Returns:
        Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 aspect ratio
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # --- Layer 1: Background Image ---
    try:
        with urllib.request.urlopen(image_url) as response:
            image_data = BytesIO(response.read())
            slide.shapes.add_picture(image_data, 0, 0, width=prs.slide_width, height=prs.slide_height)
    except Exception:
        # Fallback to a gradient if image download fails
        fill = slide.background.fill
        fill.gradient()
        fill.gradient_stops[0].color.rgb = (20, 30, 40)
        fill.gradient_stops[1].color.rgb = (80, 120, 150)

    # --- Layer 2: Spotlight Mask (Generated with PIL) ---
    slide_px_width = int(prs.slide_width * 96 / 9600 * 100) # Simple Emu to pixel conversion approximation
    slide_px_height = int(prs.slide_height * 96 / 9600 * 100)
    
    # Create a black RGBA image
    mask_img = Image.new('RGBA', (slide_px_width, slide_px_height), (0, 0, 0, 255))
    
    # Create a transparent circular hole in it
    draw = ImageDraw.Draw(mask_img)
    spotlight_radius = slide_px_height // 6
    spotlight_center = (slide_px_width // 4, slide_px_height // 2) # Start position
    bbox = [
        spotlight_center[0] - spotlight_radius,
        spotlight_center[1] - spotlight_radius,
        spotlight_center[0] + spotlight_radius,
        spotlight_center[1] + spotlight_radius,
    ]
    draw.ellipse(bbox, fill=(0, 0, 0, 0)) # Draw a fully transparent ellipse

    mask_buffer = BytesIO()
    mask_img.save(mask_buffer, format='PNG')
    mask_buffer.seek(0)
    
    mask_shape = slide.shapes.add_picture(mask_buffer, 0, 0, width=prs.slide_width, height=prs.slide_height)
    mask_shape_id = mask_shape.shape_id

    # --- Layer 3: Animation (Injected with lxml) ---
    # This XML structure defines two animations: a custom motion path and a disappear effect that follows.
    
    # Get the slide's timing element tree
    slide_part = slide.part
    tree = etree.fromstring(slide_part.blob)
    timing = tree.find('.//p:timing', namespaces=_nsmap)
    if timing is None:
        # If no timing element, create it. It must be after <p:cSld>
        common_slide_data = tree.find('.//p:cSld', namespaces=_nsmap)
        timing = etree.SubElement(common_slide_data, qn('p:timing'))

    # Build the animation sequence
    tn_lst = etree.SubElement(timing, qn('p:tnLst'))
    par_1 = etree.SubElement(tn_lst, qn('p:par'))
    ctn_1 = etree.SubElement(par_1, qn('p:cTn'), id="1", dur="indefinite", restart="never", nodeType="tmRoot")
    child_tn_lst_1 = etree.SubElement(ctn_1, qn('p:childTnLst'))
    seq_1 = etree.SubElement(child_tn_lst_1, qn('p:seq'), concurrent="1", nextAc="seek")
    ctn_2 = etree.SubElement(seq_1, qn('p:cTn'), id="2", dur="indefinite", nodeType="mainSeq")
    child_tn_lst_2 = etree.SubElement(ctn_2, qn('p:childTnLst'))
    
    par_2 = etree.SubElement(child_tn_lst_2, qn('p:par'))
    ctn_3 = etree.SubElement(par_2, qn('p:cTn'), id="3", fill="hold")
    st_cond_lst_1 = etree.SubElement(ctn_3, qn('p:stCondLst'))
    etree.SubElement(st_cond_lst_1, qn('p:cond'), delay="indefinite")
    child_tn_lst_3 = etree.SubElement(ctn_3, qn('p:childTnLst'))

    # 1. Motion Path Animation
    par_motion = etree.SubElement(child_tn_lst_3, qn('p:par'))
    ctn_motion = etree.SubElement(par_motion, qn('p:cTn'), id="4", fill="hold")
    st_cond_lst_motion = etree.SubElement(ctn_motion, qn('p:stCondLst'))
    cond_motion = etree.SubElement(st_cond_lst_motion, qn('p:cond'), delay="0")
    etree.SubElement(cond_motion, qn('p:tn'), val="3")
    child_tn_lst_motion = etree.SubElement(ctn_motion, qn('p:childTnLst'))
    
    # A representative S-curve path. M=Move, C=Cubic Bezier curve. Coordinates are relative (0.0 to 1.0).
    path_str = "M 0 0 C 0.25 0.5 0.25 -0.5 0.5 0 C 0.75 0.5 0.75 -0.5 1 0"
    anim_motion = etree.SubElement(child_tn_lst_motion, qn('p:animMotion'), dur="8000", path=path_str)
    c_bhvr_motion = etree.SubElement(anim_motion, qn('p:cBhvr'))
    etree.SubElement(c_bhvr_motion, qn('p:cTn'), id="5", dur="8000")
    tgt_el_motion = etree.SubElement(c_bhvr_motion, qn('p:tgtEl'))
    etree.SubElement(tgt_el_motion, qn('p:spTgt'), spid=str(mask_shape_id))

    # 2. Exit (Disappear) Animation
    par_exit = etree.SubElement(child_tn_lst_3, qn('p:par'))
    # 'nodeType="afterPrev"' makes this animation start after the previous one (the motion path) ends.
    ctn_exit = etree.SubElement(par_exit, qn('p:cTn'), id="6", fill="hold", nodeType="afterPrev")
    st_cond_lst_exit = etree.SubElement(ctn_exit, qn('p:stCondLst'))
    cond_exit = etree.SubElement(st_cond_lst_exit, qn('p:cond'), delay="0")
    etree.SubElement(cond_exit, qn('p:tn'), val="4", evt="end")

    child_tn_lst_exit = etree.SubElement(ctn_exit, qn('p:childTnLst'))
    anim_effect_exit = etree.SubElement(child_tn_lst_exit, qn('p:animEffect'), transition="out", filter="disappear")
    c_bhvr_exit = etree.SubElement(anim_effect_exit, qn('p:cBhvr'))
    etree.SubElement(c_bhvr_exit, qn('p:cTn'), id="7", dur="1") # Minimal duration
    tgt_el_exit = etree.SubElement(c_bhvr_exit, qn('p:tgtEl'))
    etree.SubElement(tgt_el_exit, qn('p:spTgt'), spid=str(mask_shape_id))

    # Overwrite the slide's XML with our modified version
    slide_part._blob = etree.tostring(tree, pretty_print=True)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# if __name__ == '__main__':
#     output_file = "spotlight_reveal_slide.pptx"
#     create_slide(output_file)
#     print(f"Slide saved to {output_file}")
#     if os.name == 'nt': # For Windows
#         os.startfile(output_file)
#     elif os.name == 'posix': # For MacOS/Linux
#         os.system(f"open {output_file}")

