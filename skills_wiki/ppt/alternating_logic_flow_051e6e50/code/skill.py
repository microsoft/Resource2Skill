import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image, ImageDraw
from lxml import etree

def create_slide(
    output_pptx_path: str,
    title_text: str = "Pros and Cons",
    pros_cons_data: list = None,
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with the 'Alternating Logic Flow' effect for pros and cons.

    :param output_pptx_path: Path to save the generated PPTX file.
    :param title_text: The title text for the slide.
    :param pros_cons_data: A list of tuples, where each tuple is (con_text, pro_text).
    :return: Path to the saved PPTX file.
    """

    # --- XML Namespace Helper ---
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    }

    def qn(tag):
        prefix, tagroot = tag.split(':')
        return '{{{}}}{}'.format(ns[prefix], tagroot)

    # --- Data Initialization ---
    if pros_cons_data is None:
        pros_cons_data = [
            ("Initial Concern or Objection", "Counter-argument or Solution"),
            ("A second potential problem", "How we address this issue"),
            ("A final risk to consider", "The ultimate benefit that outweighs it"),
        ]

    CON_COLOR = RGBColor(217, 94, 2)
    PRO_COLOR = RGBColor(49, 133, 156)

    # --- Presentation Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Title ---
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), prs.slide_width - Inches(1), Inches(0.75))
    title_tf = title_shape.text_frame
    p = title_tf.paragraphs[0]
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(36)
    p.font.color.rgb = RGBColor(89, 89, 89)

    # --- Shadow Image Generation (PIL) ---
    def create_shadow_image(filename, direction='left'):
        width, height = 30, int(prs.slide_height * 96) # 96 DPI for inches to pixels
        img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        for i in range(width):
            alpha = int(100 * (1 - (i / width)**0.5)) if direction == 'left' else int(100 * (i / width)**0.5)
            draw.line([(i, 0), (i, height)], fill=(0, 0, 0, alpha))
        img.save(filename)

    shadow_left_path = "shadow_left.png"
    shadow_right_path = "shadow_right.png"
    create_shadow_image(shadow_left_path, direction='left')
    create_shadow_image(shadow_right_path, direction='right')

    # --- Central Divider and Shadows ---
    center_x = prs.slide_width / 2
    slide.shapes.add_picture(shadow_left_path, center_x - Inches(0.15), 0, width=Inches(0.15))
    slide.shapes.add_picture(shadow_right_path, center_x, 0, width=Inches(0.15))
    
    # --- Create Shapes and Store IDs ---
    pill_height = Inches(0.75)
    pill_width = Inches(5)
    v_spacing = Inches(0.25)
    start_y = Inches(1.5)
    shape_ids = []

    for i, (con_text, pro_text) in enumerate(pros_cons_data):
        y_pos = start_y + i * (pill_height + v_spacing)
        
        # Con Shape (Left)
        con_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, center_x - pill_width, y_pos, pill_width, pill_height)
        con_shape.fill.solid()
        con_shape.fill.fore_color.rgb = CON_COLOR
        con_shape.line.fill.background()
        con_shape.text = con_text
        con_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        con_shape.text_frame.paragraphs[0].font.bold = True
        shape_ids.append(con_shape.shape_id)

        # Pro Shape (Right)
        pro_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, center_x, y_pos, pill_width, pill_height)
        pro_shape.fill.solid()
        pro_shape.fill.fore_color.rgb = PRO_COLOR
        pro_shape.line.fill.background()
        pro_shape.text = pro_text
        pro_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        pro_shape.text_frame.paragraphs[0].font.bold = True
        shape_ids.append(pro_shape.shape_id)
        
    # --- Animation XML Injection (lxml) ---
    slide_xml = slide.element
    timing_node = slide_xml.find(qn('p:timing'))
    if timing_node is None:
        timing_node = etree.SubElement(slide_xml.find(qn('p:cSld')), qn('p:timing'))
    
    main_seq_node = timing_node.find(qn('p:tnLst')).find(qn('p:par')).find(qn('p:cTn')).find(qn('p:childTnLst')).find(qn('p:seq'))
    if main_seq_node is None:
        # This structure is complex, we'll assume a basic sequence exists and append to it.
        # For a truly robust solution, one would build this entire tree if absent.
        # For this example, we'll find the most common path.
        main_seq_node = slide_xml.xpath("//p:seq[@concurrent='1']")[0]

    click_id_counter = 1
    
    for i in range(len(pros_cons_data)):
        con_id = shape_ids[i * 2]
        pro_id = shape_ids[i * 2 + 1]

        # 1. Con IN (On Click)
        if i == 0:
            trigger_node = etree.SubElement(main_seq_node, qn('p:par'))
            etree.SubElement(trigger_node, qn('p:cTn'), id=str(click_id_counter), dur="500").append(
                etree.fromstring(f'<p:stCondLst xmlns:p="{ns["p"]}"><p:cond delay="0"/></p:stCondLst>')
            )
            child_tn_list_in = etree.SubElement(etree.SubElement(trigger_node, qn('p:childTnLst')), qn('p:par'))
            cTn_in = etree.SubElement(child_tn_list_in, qn('p:cTn'), id=str(click_id_counter+1), fill="hold")
            cTn_in.append(etree.fromstring(f'<p:stCondLst xmlns:p="{ns["p"]}"><p:cond delay="0"/></p:stCondLst>'))
            anim_node_in = etree.fromstring(f'<p:anim xmlns:p="{ns["p"]}" calcmode="lin" valueType="num"><p:cBhvr><p:cTn id="{click_id_counter+2}" dur="500" fill="hold"/><p:tgtEl><p:spTgt spid="{con_id}"/></p:tgtEl><p:attrNameLst><p:attrName>ppt_x</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst><p:tav tm="0"><p:val><p:strVal val="1"/></p:val></p:tav><p:tav tm="100000"><p:val><p:strVal val="0"/></p:val></p:tav></p:tavLst></p:anim>')
            cTn_in.append(etree.fromstring(f'<p:childTnLst xmlns:p="{ns["p"]}"/>')).append(anim_node_in)
            etree.SubElement(anim_node_in.find(qn('p:cBhvr')), qn('p:animEffect'), transition="in", filter="peek(right)").set("prstCls", "entr")
            click_id_counter += 3
        else:
            # Previous Pro OUT, Current Con IN (On Click)
            prev_pro_id = shape_ids[(i - 1) * 2 + 1]
            trigger_node = etree.SubElement(main_seq_node, qn('p:par'))
            cTn_trigger = etree.SubElement(trigger_node, qn('p:cTn'), id=str(click_id_counter), dur="500")
            cTn_trigger.append(etree.fromstring(f'<p:stCondLst xmlns:p="{ns["p"]}"><p:cond delay="0"/></p:stCondLst>'))
            child_tn_list = etree.SubElement(etree.SubElement(trigger_node, qn('p:childTnLst')), qn('p:par'))

            # Pro OUT
            cTn_out = etree.SubElement(child_tn_list, qn('p:cTn'), id=str(click_id_counter+1), fill="hold")
            cTn_out.append(etree.fromstring(f'<p:stCondLst xmlns:p="{ns["p"]}"><p:cond delay="0"/></p:stCondLst>'))
            anim_node_out = etree.fromstring(f'<p:anim xmlns:p="{ns["p"]}" calcmode="lin" valueType="num"><p:cBhvr><p:cTn id="{click_id_counter+2}" dur="500"/><p:tgtEl><p:spTgt spid="{prev_pro_id}"/></p:tgtEl><p:attrNameLst><p:attrName>ppt_x</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst><p:tav tm="0"><p:val><p:strVal val="0"/></p:val></p:tav><p:tav tm="100000"><p:val><p:strVal val="1"/></p:val></p:tav></p:tavLst></p:anim>')
            cTn_out.append(etree.fromstring(f'<p:childTnLst xmlns:p="{ns["p"]}"/>')).append(anim_node_out)
            etree.SubElement(anim_node_out.find(qn('p:cBhvr')), qn('p:animEffect'), transition="out", filter="peek(left)").set("prstCls", "exit")

            # Con IN
            cTn_in = etree.SubElement(child_tn_list, qn('p:cTn'), id=str(click_id_counter+3), fill="hold")
            cTn_in.append(etree.fromstring(f'<p:stCondLst xmlns:p="{ns["p"]}"><p:cond delay="0"/></p:stCondLst>'))
            anim_node_in = etree.fromstring(f'<p:anim xmlns:p="{ns["p"]}" calcmode="lin" valueType="num"><p:cBhvr><p:cTn id="{click_id_counter+4}" dur="500" fill="hold"/><p:tgtEl><p:spTgt spid="{con_id}"/></p:tgtEl><p:attrNameLst><p:attrName>ppt_x</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst><p:tav tm="0"><p:val><p:strVal val="1"/></p:val></p:tav><p:tav tm="100000"><p:val><p:strVal val="0"/></p:val></p:tav></p:tavLst></p:anim>')
            cTn_in.append(etree.fromstring(f'<p:childTnLst xmlns:p="{ns["p"]}"/>')).append(anim_node_in)
            etree.SubElement(anim_node_in.find(qn('p:cBhvr')), qn('p:animEffect'), transition="in", filter="peek(right)").set("prstCls", "entr")
            click_id_counter += 5

        # 2. Con OUT, Pro IN (On Click)
        trigger_node = etree.SubElement(main_seq_node, qn('p:par'))
        cTn_trigger = etree.SubElement(trigger_node, qn('p:cTn'), id=str(click_id_counter), dur="500")
        cTn_trigger.append(etree.fromstring(f'<p:stCondLst xmlns:p="{ns["p"]}"><p:cond delay="0"/></p:stCondLst>'))
        child_tn_list = etree.SubElement(etree.SubElement(trigger_node, qn('p:childTnLst')), qn('p:par'))
        
        # Con OUT
        cTn_out = etree.SubElement(child_tn_list, qn('p:cTn'), id=str(click_id_counter+1), fill="hold")
        cTn_out.append(etree.fromstring(f'<p:stCondLst xmlns:p="{ns["p"]}"><p:cond delay="0"/></p:stCondLst>'))
        anim_node_out = etree.fromstring(f'<p:anim xmlns:p="{ns["p"]}" calcmode="lin" valueType="num"><p:cBhvr><p:cTn id="{click_id_counter+2}" dur="500"/><p:tgtEl><p:spTgt spid="{con_id}"/></p:tgtEl><p:attrNameLst><p:attrName>ppt_x</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst><p:tav tm="0"><p:val><p:strVal val="0"/></p:val></p:tav><p:tav tm="100000"><p:val><p:strVal val="1"/></p:val></p:tav></p:tavLst></p:anim>')
        cTn_out.append(etree.fromstring(f'<p:childTnLst xmlns:p="{ns["p"]}"/>')).append(anim_node_out)
        etree.SubElement(anim_node_out.find(qn('p:cBhvr')), qn('p:animEffect'), transition="out", filter="peek(right)").set("prstCls", "exit")

        # Pro IN
        cTn_in = etree.SubElement(child_tn_list, qn('p:cTn'), id=str(click_id_counter+3), fill="hold")
        cTn_in.append(etree.fromstring(f'<p:stCondLst xmlns:p="{ns["p"]}"><p:cond delay="0"/></p:stCondLst>'))
        anim_node_in = etree.fromstring(f'<p:anim xmlns:p="{ns["p"]}" calcmode="lin" valueType="num"><p:cBhvr><p:cTn id="{click_id_counter+4}" dur="500" fill="hold"/><p:tgtEl><p:spTgt spid="{pro_id}"/></p:tgtEl><p:attrNameLst><p:attrName>ppt_x</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst><p:tav tm="0"><p:val><p:strVal val="1"/></p:val></p:tav><p:tav tm="100000"><p:val><p:strVal val="0"/></p:val></p:tav></p:tavLst></p:anim>')
        cTn_in.append(etree.fromstring(f'<p:childTnLst xmlns:p="{ns["p"]}"/>')).append(anim_node_in)
        etree.SubElement(anim_node_in.find(qn('p:cBhvr')), qn('p:animEffect'), transition="in", filter="peek(left)").set("prstCls", "entr")
        click_id_counter += 5


    # --- Save and Cleanup ---
    prs.save(output_pptx_path)
    os.remove(shadow_left_path)
    os.remove(shadow_right_path)
    
    return output_pptx_path

