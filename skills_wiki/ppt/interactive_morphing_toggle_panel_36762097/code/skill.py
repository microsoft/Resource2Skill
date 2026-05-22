import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from pptx.oxml import OxmlElement
from lxml import etree

def create_interactive_toggle_slide(
    output_pptx_path: str,
    pros_title: str = "PROS",
    pros_body: list = None,
    cons_title: str = "CONS",
    cons_body: list = None,
) -> str:
    """
    Creates a two-slide PowerPoint presentation with an interactive Pros/Cons toggle switch
    that uses the Morph transition.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        pros_title: Title for the 'Pros' section.
        pros_body: A list of strings for the 'Pros' content.
        cons_title: Title for the 'Cons' section.
        cons_body: A list of strings for the 'Cons' content.

    Returns:
        The path to the saved .pptx file.
    """

    # Default content if none is provided
    if pros_body is None:
        pros_body = [
            ("Visual Appeal:", "PowerPoint allows users to create visually appealing presentations."),
            ("Flexibility:", "PowerPoint offers flexibility in terms of customization and adaptability."),
            ("Audience Engagement:", "PowerPoint enables presenters to engage their audience."),
        ]
    if cons_body is None:
        cons_body = [
            ("Potential for Boredom:", "If not used effectively, presentations can lead to boredom."),
            ("Lack of Adaptability:", "PowerPoint presentations are often linear and follow a predefined sequence."),
            ("Limited Flexibility:", "This lack of flexibility may limit the presenter's ability to digress."),
        ]
    
    # --- Helper functions for XML manipulation ---
    def add_hyperlink(shape, slide_target_idx):
        slide_part = shape.part.package.parts[slide_target_idx]
        rId = shape.part.relate_to(slide_part, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide")
        
        c_nv_pr = shape.element.nvSpPr.cNvPr
        hlink = OxmlElement("a:hlinkClick")
        hlink.set(qn("r:id"), rId)
        c_nv_pr.append(hlink)

    def add_glow(text_run, color_rgb, size_pt=10):
        rpr = text_run.element.get_or_add_rPr()
        glow = OxmlElement("a:glow")
        rgb_color = OxmlElement("a:srgbClr")
        rgb_color.set("val", f"{color_rgb[0]:02x}{color_rgb[1]:02x}{color_rgb[2]:02x}")
        glow.append(rgb_color)
        glow.set("rad", str(Emu(Pt(size_pt))))
        rpr.append(glow)

    def set_morph_transition(slide):
        transition_elm = OxmlElement("p:transition")
        transition_elm.set("advTm", "0") # No auto-advance
        
        morph_elm = OxmlElement("p:morph")
        morph_elm.set("type", "byObject")
        transition_elm.append(morph_elm)
        
        slide.element.insert(0, transition_elm)

    # --- Presentation Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- Define Colors and Fonts ---
    COLOR_BG = RGBColor(0, 0, 0)
    COLOR_PROS = RGBColor(57, 255, 20)
    COLOR_CONS = RGBColor(255, 0, 0)
    COLOR_INACTIVE_BG = RGBColor(38, 38, 38)
    COLOR_INACTIVE_TEXT = RGBColor(166, 166, 166)
    COLOR_ACTIVE_TEXT = RGBColor(255, 255, 255)
    FONT_TITLE = "Cooper Black"
    FONT_BODY = "Arial"

    # --- Create Slide 1 (Pros Active) ---
    slide1 = prs.slides.add_slide(blank_layout)
    slide1.background.fill.solid()
    slide1.background.fill.fore_color.rgb = COLOR_BG

    # Content Boxes
    pros_box1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1), Inches(1.5), Inches(5), Inches(5))
    pros_box1.fill.solid(); pros_box1.fill.fore_color.rgb = COLOR_PROS
    pros_box1.line.fill.background()
    
    cons_box1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.33), Inches(1.5), Inches(5), Inches(5))
    cons_box1.fill.solid(); cons_box1.fill.fore_color.rgb = COLOR_INACTIVE_BG
    cons_box1.line.fill.background()

    # Titles
    title_pros1_tf = slide1.shapes.add_textbox(Inches(1), Inches(0.5), Inches(5), Inches(1)).text_frame
    p_pros1 = title_pros1_tf.paragraphs[0]
    run_pros1 = p_pros1.add_run(); run_pros1.text = pros_title
    run_pros1.font.name = FONT_TITLE; run_pros1.font.size = Pt(44); run_pros1.font.color.rgb = COLOR_ACTIVE_TEXT
    add_glow(run_pros1, COLOR_PROS)

    title_cons1_tf = slide1.shapes.add_textbox(Inches(7.33), Inches(0.5), Inches(5), Inches(1)).text_frame
    p_cons1 = title_cons1_tf.paragraphs[0]
    run_cons1 = p_cons1.add_run(); run_cons1.text = cons_title
    run_cons1.font.name = FONT_TITLE; run_cons1.font.size = Pt(44); run_cons1.font.color.rgb = COLOR_ACTIVE_TEXT
    add_glow(run_cons1, COLOR_CONS)

    # Body Text
    pros_body1_tf = pros_box1.text_frame
    for bold_text, regular_text in pros_body:
        p = pros_body1_tf.add_paragraph()
        run_b = p.add_run(); run_b.text = bold_text + " "; run_b.font.bold = True
        run_r = p.add_run(); run_r.text = regular_text
        for run in [run_b, run_r]: run.font.name = FONT_BODY; run.font.size = Pt(16); run.font.color.rgb = COLOR_ACTIVE_TEXT

    cons_body1_tf = cons_box1.text_frame
    for bold_text, regular_text in cons_body:
        p = cons_body1_tf.add_paragraph()
        p.text = bold_text + " " + regular_text
        p.font.name = FONT_BODY; p.font.size = Pt(16); p.font.color.rgb = COLOR_INACTIVE_TEXT
    
    # Toggle
    toggle_base1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.16), Inches(6.7), Inches(3), Inches(0.5))
    toggle_base1.fill.solid(); toggle_base1.fill.fore_color.rgb = COLOR_BG
    toggle_base1.line.color.rgb = COLOR_PROS; toggle_base1.line.width = Pt(3)
    toggle_base1.adjustments[0] = 0.5 # fully rounded

    toggle_knob1 = slide1.shapes.add_shape(MSO_SHAPE.OVAL, Inches(5.2), Inches(6.72), Inches(0.45), Inches(0.45))
    toggle_knob1.fill.solid(); toggle_knob1.fill.fore_color.rgb = COLOR_PROS
    toggle_knob1.line.fill.background()
    
    # --- Create Slide 2 (Cons Active) ---
    slide2 = prs.slides.add_slide(blank_layout)
    slide2.background.fill.solid()
    slide2.background.fill.fore_color.rgb = COLOR_BG

    # Content Boxes
    pros_box2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1), Inches(1.5), Inches(5), Inches(5))
    pros_box2.fill.solid(); pros_box2.fill.fore_color.rgb = COLOR_INACTIVE_BG
    pros_box2.line.fill.background()
    
    cons_box2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.33), Inches(1.5), Inches(5), Inches(5))
    cons_box2.fill.solid(); cons_box2.fill.fore_color.rgb = COLOR_CONS
    cons_box2.line.fill.background()

    # Titles
    title_pros2_tf = slide2.shapes.add_textbox(Inches(1), Inches(0.5), Inches(5), Inches(1)).text_frame
    p_pros2 = title_pros2_tf.paragraphs[0]
    run_pros2 = p_pros2.add_run(); run_pros2.text = pros_title
    run_pros2.font.name = FONT_TITLE; run_pros2.font.size = Pt(44); run_pros2.font.color.rgb = COLOR_ACTIVE_TEXT
    add_glow(run_pros2, COLOR_PROS)

    title_cons2_tf = slide2.shapes.add_textbox(Inches(7.33), Inches(0.5), Inches(5), Inches(1)).text_frame
    p_cons2 = title_cons2_tf.paragraphs[0]
    run_cons2 = p_cons2.add_run(); run_cons2.text = cons_title
    run_cons2.font.name = FONT_TITLE; run_cons2.font.size = Pt(44); run_cons2.font.color.rgb = COLOR_ACTIVE_TEXT
    add_glow(run_cons2, COLOR_CONS)

    # Body Text
    pros_body2_tf = pros_box2.text_frame
    for bold_text, regular_text in pros_body:
        p = pros_body2_tf.add_paragraph()
        p.text = bold_text + " " + regular_text
        p.font.name = FONT_BODY; p.font.size = Pt(16); p.font.color.rgb = COLOR_INACTIVE_TEXT
        
    cons_body2_tf = cons_box2.text_frame
    for bold_text, regular_text in cons_body:
        p = cons_body2_tf.add_paragraph()
        run_b = p.add_run(); run_b.text = bold_text + " "; run_b.font.bold = True
        run_r = p.add_run(); run_r.text = regular_text
        for run in [run_b, run_r]: run.font.name = FONT_BODY; run.font.size = Pt(16); run.font.color.rgb = COLOR_ACTIVE_TEXT

    # Toggle
    toggle_base2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.16), Inches(6.7), Inches(3), Inches(0.5))
    toggle_base2.fill.solid(); toggle_base2.fill.fore_color.rgb = COLOR_BG
    toggle_base2.line.color.rgb = COLOR_CONS; toggle_base2.line.width = Pt(3)
    toggle_base2.adjustments[0] = 0.5
    
    toggle_knob2 = slide2.shapes.add_shape(MSO_SHAPE.OVAL, Inches(7.66), Inches(6.72), Inches(0.45), Inches(0.45))
    toggle_knob2.fill.solid(); toggle_knob2.fill.fore_color.rgb = COLOR_CONS
    toggle_knob2.line.fill.background()

    # --- Interactivity & Transitions ---
    # Invisible click areas
    click_to_cons = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.66), Inches(6.7), Inches(1.5), Inches(0.5))
    click_to_cons.fill.background(); click_to_cons.line.fill.background()
    add_hyperlink(click_to_cons, 1)

    click_to_pros = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.16), Inches(6.7), Inches(1.5), Inches(0.5))
    click_to_pros.fill.background(); click_to_pros.line.fill.background()
    add_hyperlink(click_to_pros, 0)
    
    # Apply Morph Transitions
    set_morph_transition(slide1)
    set_morph_transition(slide2)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example of how to run the function
if __name__ == '__main__':
    file_path = "interactive_toggle_slide.pptx"
    create_interactive_toggle_slide(file_path)
    print(f"Presentation saved to {file_path}")
    # To view, open the file and start the slideshow.
    if os.name == 'nt': # For Windows
        os.startfile(file_path)
