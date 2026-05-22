def create_slide(
    output_pptx_path: str,
    target_number: str = "6782",
    bg_color: tuple = (13, 17, 28),
    accent_color: tuple = (218, 165, 32), # Goldenrod
    **kwargs,
) -> str:
    """
    Creates a 2-slide PPTX reproducing the Odometer/Rolling Number effect using Morph.
    Slide 1: Starts at "0000" (or length of target)
    Slide 2: Rolls to the target_number
    """
    import os
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw
    from lxml import etree

    # 1. Generate the Matte Overlay Image using PIL
    # This acts as a background AND a mask hiding the vertical text strips.
    slide_w_px, slide_h_px = 1280, 720
    matte = Image.new("RGBA", (slide_w_px, slide_h_px), bg_color + (255,))
    draw = ImageDraw.Draw(matte)
    
    # Calculate Window Hole dimensions
    num_digits = len(target_number)
    digit_width_px = 120
    window_w = num_digits * digit_width_px + 100
    window_h = 160
    
    x0 = (slide_w_px - window_w) // 2
    y0 = (slide_h_px - window_h) // 2
    x1 = x0 + window_w
    y1 = y0 + window_h
    
    # "Cut out" the transparent hole
    draw.rounded_rectangle([x0, y0, x1, y1], radius=20, fill=(0, 0, 0, 0))
    # Draw the gold frame
    draw.rounded_rectangle([x0, y0, x1, y1], radius=20, outline=accent_color + (255,), width=6)
    
    matte_path = "temp_matte_overlay.png"
    matte.save(matte_path)

    # 2. Setup Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # Configuration for Text Strips
    font_size_pt = 96
    line_spacing_pt = 110 # Absolute distance between numbers
    line_spacing_inches = line_spacing_pt / 72.0
    
    center_y_inches = 3.75
    # The Y position to align a number exactly in the center of the window
    base_top_inches = center_y_inches - (line_spacing_inches / 2)
    
    strip_width_inches = 1.2
    total_width_inches = num_digits * strip_width_inches
    start_x_inches = (13.333 - total_width_inches) / 2.0

    number_sequence = "0\n1\n2\n3\n4\n5\n6\n7\n8\n9"

    # --- SLIDE 1: Start State (All 0s) ---
    slide1 = prs.slides.add_slide(blank_layout)
    slide1.background.fill.solid()
    slide1.background.fill.fore_color.rgb = RGBColor(*bg_color)
    
    # Add text strips starting at '0'
    for i in range(num_digits):
        tx_box = slide1.shapes.add_textbox(
            Inches(start_x_inches + i * strip_width_inches),
            Inches(base_top_inches), # '0' is at the top, so placing it at base_top centers '0'
            Inches(strip_width_inches),
            Inches(10)
        )
        tf = tx_box.text_frame
        tf.text = number_sequence
        tf.word_wrap = False
        for p in tf.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            p.line_spacing = Pt(line_spacing_pt)
            p.font.size = Pt(font_size_pt)
            p.font.bold = True
            p.font.name = "Arial"
            p.font.color.rgb = RGBColor(*accent_color)
            
    # Add Matte on top
    slide1.shapes.add_picture(matte_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # --- SLIDE 2: End State (Rolled to target numbers) ---
    slide2 = prs.slides.add_slide(blank_layout)
    slide2.background.fill.solid()
    slide2.background.fill.fore_color.rgb = RGBColor(*bg_color)
    
    # Add text strips shifted upwards
    for i, digit_char in enumerate(target_number):
        digit_val = int(digit_char)
        # Shift the box UP by (digit_val * line_spacing) so the target digit lands in the window
        shifted_top = base_top_inches - (digit_val * line_spacing_inches)
        
        tx_box = slide2.shapes.add_textbox(
            Inches(start_x_inches + i * strip_width_inches),
            Inches(shifted_top),
            Inches(strip_width_inches),
            Inches(10)
        )
        tf = tx_box.text_frame
        tf.text = number_sequence
        tf.word_wrap = False
        for p in tf.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            p.line_spacing = Pt(line_spacing_pt)
            p.font.size = Pt(font_size_pt)
            p.font.bold = True
            p.font.name = "Arial"
            p.font.color.rgb = RGBColor(*accent_color)

    # Add Matte on top
    slide2.shapes.add_picture(matte_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # --- Inject Morph Transition into Slide 2 via lxml ---
    morph_xml = '''
    <mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">
      <mc:Choice Requires="p14" xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main">
        <p:transition spd="slow" p14:dur="2000" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
          <p19:morph option="byObject" xmlns:p19="http://schemas.microsoft.com/office/powerpoint/2018/4/main"/>
        </p:transition>
      </mc:Choice>
      <mc:Fallback>
        <p:transition spd="slow" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>
      </mc:Fallback>
    </mc:AlternateContent>
    '''
    try:
        transition_el = etree.fromstring(morph_xml)
        # Append to the end of the slide element
        slide2.element.append(transition_el)
    except Exception as e:
        print(f"Warning: Could not inject Morph XML automatically. {e}")

    # Cleanup and Save
    prs.save(output_pptx_path)
    if os.path.exists(matte_path):
        os.remove(matte_path)
        
    return output_pptx_path

# Example execution:
# create_slide("odometer_morph.pptx", target_number="6782")
