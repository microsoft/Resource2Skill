def create_slide(
    output_pptx_path: str,
    title_text: str = "OUR SKILLS",
    skills_data: dict = None,
    **kwargs,
) -> str:
    """
    Creates a PPTX slide reproducing the 'Clean Corporate Skill Showcase' effect.

    Args:
        output_pptx_path (str): Path to save the generated PPTX file.
        title_text (str): The main title for the slide.
        skills_data (dict): A dictionary of skill names and their percentages (0-100).
                            If None, default data will be used.

    Returns:
        str: The path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.dml.color import RGBColor
    from pptx.oxml.xmlchemy import OxmlElement
    from pptx.oxml.ns import nsdecls

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Color & Font Palette ---
    BG_COLOR = RGBColor(237, 237, 242)
    TITLE_COLOR = RGBColor(47, 51, 74)
    GRAY_TEXT_COLOR = RGBColor(158, 158, 158)
    BAR_TRACK_COLOR = RGBColor(220, 220, 220)
    GRAD_START_COLOR = RGBColor(47, 51, 74)
    GRAD_END_COLOR = RGBColor(51, 194, 219)
    FONT_FAMILY = "Roboto"

    # --- Default Data ---
    if skills_data is None:
        skills_data = {
            "Web Development": 90,
            "Mobile app": 100,
            "Social Media": 95,
            "Photography": 100,
            "SEO": 100,
            "Marketing": 95,
            "UI Design": 85,
        }

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

    # === Animation Helper (OXML Injection) ===
    def _get_or_create_main_sequence(slide_part):
        """Finds or creates the main animation sequence XML tree."""
        timing = slide_part.element.find('.//p:timing', namespaces=slide_part.element.nsmap)
        if timing is None:
            sld = slide_part.element
            timing = OxmlElement('p:timing')
            tnLst = OxmlElement('p:tnLst')
            par = OxmlElement('p:par')
            cTn_root = OxmlElement('p:cTn')
            cTn_root.set('id', '1')
            cTn_root.set('dur', 'indefinite')
            cTn_root.set('nodeType', 'tmRoot')
            childTnLst_root = OxmlElement('p:childTnLst')
            seq = OxmlElement('p:seq')
            seq.set('concurrent', '1')
            seq.set('nextAc', 'seek')
            cTn_main = OxmlElement('p:cTn')
            cTn_main.set('id', '2')
            cTn_main.set('fill', 'hold')
            prevCondLst = OxmlElement('p:prevCondLst')
            cond = OxmlElement('p:cond')
            cond.set('evt', 'onNext')
            cond.set('delay', '0')
            tgtEl = OxmlElement('p:tgtEl')
            sldTgt = OxmlElement('p:sldTgt')
            tgtEl.append(sldTgt)
            cond.append(tgtEl)
            prevCondLst.append(cond)
            childTnLst_main = OxmlElement('p:childTnLst')
            cTn_main.extend([prevCondLst, childTnLst_main])
            seq.append(cTn_main)
            childTnLst_root.append(seq)
            cTn_root.append(childTnLst_root)
            par.append(cTn_root)
            tnLst.append(par)
            timing.append(tnLst)
            # Insert timing element after background properties
            bg_props = sld.find('.//p:bg', namespaces=sld.nsmap)
            if bg_props is not None:
                bg_props.addnext(timing)
            else: # Fallback if no background properties
                sld.get_or_add_cSld().addprevious(timing)

        return timing.xpath('.//p:cTn[@id="2"]/p:childTnLst')[0]

    def _add_animation(main_sequence, shape, effect, delay_ms, duration_ms, trigger='afterPrev', direction=None):
        node_id = str(len(main_sequence.xpath('.//p:cTn')) + 10) # Unique ID for the animation node
        
        par = OxmlElement('p:par')
        cTn = OxmlElement('p:cTn')
        cTn.set('id', node_id)
        cTn.set('fill', 'hold')
        
        stCondLst = OxmlElement('p:stCondLst')
        cond = OxmlElement('p:cond')
        if trigger == 'afterPrev':
            cond.set('delay', str(delay_ms))
        stCondLst.append(cond)
        
        childTnLst = OxmlElement('p:childTnLst')
        par_inner = OxmlElement('p:par')
        cTn_inner = OxmlElement('p:cTn')
        cTn_inner.set('id', str(int(node_id) + 1))
        cTn_inner.set('dur', str(duration_ms))
        cTn_inner.set('fill', 'hold')
        
        stCondLst_inner = OxmlElement('p:stCondLst')
        cond_inner = OxmlElement('p:cond')
        cond_inner.set('delay', '0')
        stCondLst_inner.append(cond_inner)

        childTnLst_inner = OxmlElement('p:childTnLst')
        anim = OxmlElement('p:anim')
        anim.set('calcmode', 'lin')
        anim.set('valueType', 'num')
        
        cBhvr = OxmlElement('p:cBhvr')
        cTn_bhvr = OxmlElement('p:cTn')
        cTn_bhvr.set('id', str(int(node_id) + 2))
        cTn_bhvr.set('dur', str(duration_ms))
        tgtEl = OxmlElement('p:tgtEl')
        spTgt = OxmlElement('p:spTgt')
        spTgt.set('spid', str(shape.shape_id))
        tgtEl.append(spTgt)
        cTn_bhvr.append(tgtEl)
        
        attrNameLst = OxmlElement('p:attrNameLst')
        attrName = OxmlElement('p:attrName')
        attrName.text = effect
        if direction:
            attrName.text = f"{effect} from-{direction}"
        attrNameLst.append(attrName)
        
        cBhvr.extend([cTn_bhvr, attrNameLst])
        anim.append(cBhvr)
        
        childTnLst_inner.append(anim)
        cTn_inner.extend([stCondLst_inner, childTnLst_inner])
        par_inner.append(cTn_inner)
        childTnLst.append(par_inner)
        cTn.extend([stCondLst, childTnLst])
        par.append(cTn)
        main_sequence.append(par)

    main_sequence = _get_or_create_main_sequence(slide.part)
    animation_delay = 250  # Start with a small delay

    # === Layer 2: Content & Animations ===
    # --- Title ---
    title_shape = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.33), Inches(1))
    title_tf = title_shape.text_frame
    title_p = title_tf.paragraphs[0]
    title_p.text = title_text
    title_p.font.name = FONT_FAMILY
    title_p.font.bold = True
    title_p.font.size = Pt(36)
    title_p.font.color.rgb = TITLE_COLOR
    title_p.alignment = 1  # Center

    # --- Skills Bars ---
    start_y = Inches(1.8)
    line_height = Inches(0.7)
    skill_label_x = Inches(2)
    skill_label_width = Inches(3)
    bar_x = Inches(5.5)
    bar_width = Inches(5)
    bar_height = Inches(0.3)
    percent_x = Inches(10.8)

    for i, (skill, percent) in enumerate(skills_data.items()):
        current_y = start_y + i * line_height

        # Skill Text Label
        txBox = slide.shapes.add_textbox(skill_label_x, current_y - Inches(0.1), skill_label_width, Inches(0.5))
        p = txBox.text_frame.paragraphs[0]
        p.text = skill
        p.font.name = FONT_FAMILY
        p.font.size = Pt(16)
        p.font.color.rgb = TITLE_COLOR
        _add_animation(main_sequence, txBox, 'fly', delay_ms=animation_delay, duration_ms=500, direction='left')
        animation_delay = 0 # Subsequent animations in the same "step" have 0 delay

        # Progress Bar Track
        slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bar_x, current_y, bar_width, bar_height)
        track_shape = slide.shapes[-1]
        track_fill = track_shape.fill
        track_fill.solid()
        track_fill.fore_color.rgb = BAR_TRACK_COLOR
        track_shape.line.fill.background()

        # Progress Bar Fill
        fill_width = bar_width * (percent / 100.0)
        if fill_width > 0:
            fill_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bar_x, current_y, fill_width, bar_height)
            grad_fill = fill_shape.fill
            grad_fill.gradient()
            grad_fill.gradient_angle = 0
            gs1 = grad_fill.gradient_stops.add()
            gs1.position = 0
            gs1.color.rgb = GRAD_START_COLOR
            gs2 = grad_fill.gradient_stops.add()
            gs2.position = 100000
            gs2.color.rgb = GRAD_END_COLOR
            fill_shape.line.fill.background()
            _add_animation(main_sequence, fill_shape, 'wipe', delay_ms=animation_delay, duration_ms=750, direction='left')

        # Percentage Text
        txBox = slide.shapes.add_textbox(percent_x, current_y - Inches(0.1), Inches(1), Inches(0.5))
        p = txBox.text_frame.paragraphs[0]
        p.text = f"{percent}%"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(16)
        p.font.color.rgb = GRAY_TEXT_COLOR
        _add_animation(main_sequence, txBox, 'appear', delay_ms=animation_delay, duration_ms=250)
        animation_delay = 250 # Add delay before starting the next row

    prs.save(output_pptx_path)
    return output_pptx_path

