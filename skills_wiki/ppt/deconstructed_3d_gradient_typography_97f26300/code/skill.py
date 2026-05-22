import os
from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml

def create_slide(
    output_pptx_path: str,
    title_text: str = "BEST",
    body_text: str = "",
    bg_palette: str = "cyberpunk",
    accent_color: tuple = (255, 0, 127),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Deconstructed 3D Gradient Typography" visual effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide
    
    # =========================================================================
    # Helper 1: Inject XML into shape properties (for Background)
    # =========================================================================
    def apply_shape_xml(shape, xml_string):
        spPr = shape._element.spPr
        for child in list(spPr):
            if child.tag.endswith('Fill'):
                spPr.remove(child)
        spPr.append(parse_xml(xml_string))

    # =========================================================================
    # Helper 2: Inject XML into text run properties (for Typography)
    # =========================================================================
    def apply_text_run_xml(run, xml_elements):
        rPr = run._r.get_or_add_rPr()
        for child in list(rPr):
            if child.tag.endswith('Fill') or child.tag.endswith('ln'):
                rPr.remove(child)
        for element in xml_elements:
            rPr.append(parse_xml(element))

    # =========================================================================
    # Layer 0: Radial Gradient Background
    # =========================================================================
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg_shape.line.fill.background()
    
    bg_grad_xml = """
    <a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:gsLst>
            <a:gs pos="0"><a:srgbClr val="3A0CA3"/></a:gs>
            <a:gs pos="100000"><a:srgbClr val="0B0228"/></a:gs>
        </a:gsLst>
        <a:path path="circle">
            <a:fillToRect l="50000" t="50000" r="50000" b="50000"/>
        </a:path>
    </a:gradFill>
    """
    apply_shape_xml(bg_shape, bg_grad_xml)

    # =========================================================================
    # Typography Setup
    # =========================================================================
    font_name = "Arial Black"
    font_size = Pt(150)
    base_x = 0
    base_y = Inches(2.2) # Visually centered Y

    def add_hero_text_layer(offset_x, offset_y):
        """Creates a full-width text box with specific XY offset."""
        txBox = slide.shapes.add_textbox(base_x + offset_x, base_y + offset_y, prs.slide_width, Inches(3))
        tf = txBox.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = title_text.upper()
        run.font.name = font_name
        run.font.size = font_size
        run.font.bold = True
        return run

    # =========================================================================
    # Layer 1: Distant Drop Shadow (Black, 40% opacity)
    # =========================================================================
    run_shadow = add_hero_text_layer(Inches(0.4), Inches(0.4))
    apply_text_run_xml(run_shadow, [
        """
        <a:solidFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:srgbClr val="000000"><a:alpha val="40000"/></a:srgbClr>
        </a:solidFill>
        """
    ])

    # =========================================================================
    # Layer 2: 3D Volumetric Extrusion Block
    # Stack 15 dense layers going backwards to simulate deep solid 3D depth
    # =========================================================================
    extrusion_depth = 15
    for i in range(extrusion_depth, 0, -1):
        step_offset = Inches(0.015 * i)
        run_ext = add_hero_text_layer(step_offset, step_offset)
        apply_text_run_xml(run_ext, [
            """
            <a:solidFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
                <a:srgbClr val="4B0082"/>
            </a:solidFill>
            """
        ])

    # =========================================================================
    # Layer 3: Hero Gradient (Hot Pink to Gold)
    # =========================================================================
    run_hero = add_hero_text_layer(0, 0)
    apply_text_run_xml(run_hero, [
        """
        <a:gradFill rotWithShape="1" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:gsLst>
                <a:gs pos="0"><a:srgbClr val="FF007F"/></a:gs>
                <a:gs pos="40000"><a:srgbClr val="FF007F"/></a:gs>
                <a:gs pos="75000"><a:srgbClr val="FFD700"/></a:gs>
                <a:gs pos="100000"><a:srgbClr val="FFD700"/></a:gs>
            </a:gsLst>
            <a:lin ang="5400000" scaled="1"/>
        </a:gradFill>
        """ # 5400000 = 90 degrees (Bottom to Top)
    ])

    # =========================================================================
    # Layer 4: Glass Filter (White, 20% Opacity)
    # =========================================================================
    run_glass = add_hero_text_layer(-Inches(0.12), -Inches(0.12))
    apply_text_run_xml(run_glass, [
        """
        <a:solidFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:srgbClr val="FFFFFF"><a:alpha val="20000"/></a:srgbClr>
        </a:solidFill>
        """
    ])

    # =========================================================================
    # Layer 5: Wireframe Outline (No Fill, White Stroke)
    # =========================================================================
    run_outline = add_hero_text_layer(-Inches(0.25), -Inches(0.25))
    apply_text_run_xml(run_outline, [
        '<a:noFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>',
        """
        <a:ln w="25400" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
        </a:ln>
        """ # w=25400 is 2 pt line weight
    ])

    # Save output
    prs.save(output_pptx_path)
    return output_pptx_path
