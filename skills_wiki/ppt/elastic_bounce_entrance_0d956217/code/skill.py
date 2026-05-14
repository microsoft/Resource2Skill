import os
from pptx import Presentation
from pptx.util import Inches, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from lxml import etree

def create_slide(
    output_pptx_path: str,
    title_text: str = "Elastic Bounce Entrance",
    shape_type: MSO_SHAPE = MSO_SHAPE.OVAL,
    accent_color: tuple = (255, 87, 34),
    animation_direction: str = 'top',
    bounce_duration_s: float = 0.5,
    animation_duration_s: float = 0.75,
    **kwargs
) -> str:
    """
    Creates a PPTX slide demonstrating the "Elastic Bounce Entrance" effect.

    This is achieved by applying a "Fly In" animation and setting the 'bounceEnd'
    property via direct Open XML manipulation, as this feature is not
    exposed in the python-pptx API.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        title_text: Text for the title of the slide.
        shape_type: The MSO_SHAPE enum for the object to animate.
        accent_color: RGB tuple for the shape's color.
        animation_direction: 'top', 'bottom', 'left', or 'right'.
        bounce_duration_s: Duration of the bounce effect in seconds.
        animation_duration_s: Duration of the main fly-in animation in seconds.

    Returns:
        Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Background & Title ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(15, 15, 15)

    title_shape = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(14), Inches(1))
    title_shape.text = title_text
    p = title_shape.text_frame.paragraphs[0]
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.font.size = Inches(0.5)

    # === Layer 2: Animated Shape ===
    shape = slide.shapes.add_shape(
        shape_type, Inches(6.5), Inches(3), Inches(3), Inches(3)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(*accent_color)
    shape.line.fill.background()

    # === Layer 3: Animation via XML Injection ===
    # Get the lxml element for the shape
    shape_element = shape.element
    shape_id = shape_element.xpath('.//p:spid', namespaces=shape_element.nsmap)[0].text

    # Namespace map for XML creation
    nsmap = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    }

    def qn(tag):
        """Qualified name helper for lxml"""
        prefix, tag_name = tag.split(':')
        return f'{{{nsmap[prefix]}}}{tag_name}'

    # Create the timing.xml part if it doesn't exist
    if not slide.has_timing:
        slide.part.get_or_add_timing()
    
    timing_elm = slide.part.timing_part.element
    
    # Build the animation XML structure
    main_seq = etree.SubElement(timing_elm.find(qn('p:tnLst')).find(qn('p:par')).find(qn('p:cTn')).find(qn('p:childTnLst')), qn('p:seq'))
    main_seq.set('concurrent', '1')
    main_seq.set('nextAc', 'seq')

    c_tn_1 = etree.SubElement(main_seq, qn('p:cTn'))
    c_tn_1.set('id', '1')
    c_tn_1.set('dur', 'indefinite')
    c_tn_1.set('restart', 'never')
    c_tn_1.set('nodeType', 'tmRoot')
    
    st_cond_lst = etree.SubElement(c_tn_1, qn('p:stCondLst'))
    etree.SubElement(st_cond_lst, qn('p:cond')).set('delay', 'indefinite')
    
    end_cond_lst = etree.SubElement(c_tn_1, qn('p:endCondLst'))
    etree.SubElement(end_cond_lst, qn('p:cond')).set('evt', 'end')

    child_tn_lst_1 = etree.SubElement(c_tn_1, qn('p:childTnLst'))
    
    # This sequence triggers on click
    click_seq = etree.SubElement(child_tn_lst_1, qn('p:seq'))
    click_seq.set('concurrent', '1')
    click_seq.set('nextAc', 'seq')

    c_tn_2 = etree.SubElement(click_seq, qn('p:cTn'))
    c_tn_2.set('id', '2')
    c_tn_2.set('restart', 'whenNotActive')
    
    st_cond_lst_2 = etree.SubElement(c_tn_2, qn('p:stCondLst'))
    etree.SubElement(st_cond_lst_2, qn('p:cond')).set('evt', 'onNext')
    etree.SubElement(st_cond_lst_2.find(qn('p:cond')), qn('p:tgtEl')).set(qn('p:spid'), '1')

    child_tn_lst_2 = etree.SubElement(c_tn_2, qn('p:childTnLst'))
    
    # This parallel element holds the animation for our shape
    par_anim = etree.SubElement(child_tn_lst_2, qn('p:par'))
    
    c_tn_3 = etree.SubElement(par_anim, qn('p:cTn'))
    c_tn_3.set('id', '3')
    # *** THIS IS THE KEY ATTRIBUTE FOR THE BOUNCE EFFECT ***
    c_tn_3.set('bounceEnd', str(int(bounce_duration_s * 1000)))
    c_tn_3.set('dur', str(int(animation_duration_s * 1000)))
    
    st_cond_lst_3 = etree.SubElement(c_tn_3, qn('p:stCondLst'))
    etree.SubElement(st_cond_lst_3, qn('p:cond')).set('delay', '0')

    child_tn_lst_3 = etree.SubElement(c_tn_3, qn('p:childTnLst'))

    par_anim_2 = etree.SubElement(child_tn_lst_3, qn('p:par'))
    c_tn_4 = etree.SubElement(par_anim_2, qn('p:cTn'))
    c_tn_4.set('id', '4')

    child_tn_lst_4 = etree.SubElement(c_tn_4, qn('p:childTnLst'))

    # Define the actual "Fly In" animation effect
    anim_set = etree.SubElement(child_tn_lst_4, qn('p:set'))
    c_bhvr = etree.SubElement(anim_set, qn('p:cBhvr'))
    
    c_tn_bhvr = etree.SubElement(c_bhvr, qn('p:cTn'))
    c_tn_bhvr.set('id', '5')
    c_tn_bhvr.set('dur', str(int(animation_duration_s * 1000)))

    # Target the shape
    tgt_el = etree.SubElement(c_bhvr, qn('p:tgtEl'))
    etree.SubElement(tgt_el, qn('p:spTgt')).set('spid', shape_id)

    # Define the animation effect properties
    attr_name_lst = etree.SubElement(c_bhvr, qn('p:attrNameLst'))
    etree.SubElement(attr_name_lst, qn('p:attrName')).text = 'style.visibility'
    
    to_val = etree.SubElement(anim_set, qn('p:to'))
    etree.SubElement(to_val, qn('p:strVal')).set('val', 'visible')
    
    anim_effect = etree.SubElement(c_bhvr, qn('p:animEffect'))
    
    direction_map = {
        'left': 'fromLeft',
        'right': 'fromRight',
        'top': 'fromTop',
        'bottom': 'fromBottom'
    }
    fly_direction = direction_map.get(animation_direction, 'fromTop')
    
    anim_effect.set('transition', 'in')
    anim_effect.set('filter', f'fly(in,{fly_direction})')

    # Save the presentation
    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# if __name__ == '__main__':
#     file_path = "elastic_bounce_entrance_demo.pptx"
#     create_slide(
#         output_pptx_path=file_path,
#         title_text="PPT Fly-In with Elastic Bounce",
#         shape_type=MSO_SHAPE.ROUNDED_RECTANGLE,
#         accent_color=(0, 120, 215),
#         animation_direction='right',
#         bounce_duration_s=0.6,
#         animation_duration_s=1.0
#     )
#     print(f"Presentation saved to {os.path.abspath(file_path)}")
#     # To view, open the file and start the slideshow. Click to trigger the animation.

