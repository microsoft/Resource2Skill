import requests
from io import BytesIO
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import os

def add_morph_transition(slide, duration_ms=2500):
    """Adds a Morph transition to a slide using lxml."""
    slide_element = slide._element
    # Find or create the <p:transition> element
    transition_list = slide_element.xpath('//p:transition')
    if transition_list:
        transition_element = transition_list[0]
        # Clear existing children to ensure morph is the only transition
        transition_element.clear()
    else:
        # Add a new transition element
        transition_element = etree.SubElement(slide_element, '{http://schemas.openxmlformats.org/presentationml/2006/main}transition')

    transition_element.set('dur', str(duration_ms))
    morph_element = etree.SubElement(transition_element, '{http://schemas.openxmlformats.org/presentationml/2006/main}morph')
    morph_element.set('type', 'byObject')

def remove_sky_from_image(image_bytes: BytesIO, tolerance: int = 50, edge_blur: int = 3) -> BytesIO:
    """A simple color-keying function to make the blue sky transparent."""
    img = Image.open(image_bytes).convert("RGBA")
    
    # Increase saturation to make colors more distinct
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.5)
    
    data = img.getdata()
    new_data = []
    for item in data:
        # Simple heuristic for blue sky: blue channel is significantly higher than red and green
        if item[2] > item[0] + tolerance and item[2] > item[1] + tolerance:
            new_data.append((255, 255, 255, 0))  # Make transparent
        else:
            new_data.append(item)
    img.putdata(new_data)
    
    # Soften the alpha channel edges to reduce jaggedness
    alpha = img.getchannel('A')
    blurred_alpha = alpha.filter(ImageFilter.GaussianBlur(radius=edge_blur))
    img.putalpha(blurred_alpha)

    output = BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return output

def create_slide(
    output_pptx_path: str,
    title_text: str = "BRAZIL",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Text-Behind-Scenery Reveal effect.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    blank_layout = prs.slide_layouts[6]

    # --- Image URLs (Royalty-free from Pexels) ---
    foreground_url = "https://images.pexels.com/photos/1598775/pexels-photo-1598775.jpeg?auto=compress&cs=tinysrgb&w=1920&h=1080"
    background_url = "https://images.pexels.com/photos/2310641/pexels-photo-2310641.jpeg?auto=compress&cs=tinysrgb&w=1920&h=1080"
    flag_url = "https://upload.wikimedia.org/wikipedia/en/thumb/0/05/Flag_of_Brazil.svg/320px-Flag_of_Brazil.svg.png"
    
    # --- SLIDE 1: Starting positions for Morph ---
    slide1 = prs.slides.add_slide(blank_layout)
    off_slide_left = Emu(-prs.slide_width)
    off_slide_top = Emu(-prs.slide_height)

    try:
        response_bg = requests.get(background_url)
        bg_image_stream = BytesIO(response_bg.content)
        slide1.shapes.add_picture(bg_image_stream, 0, 0, width=prs.slide_width, height=prs.slide_height)
    except requests.exceptions.RequestException:
        fill = slide1.background.fill
        fill.gradient()
        fill.gradient_stops[0].color.rgb = RGBColor(217, 87, 0)
        fill.gradient_stops[1].color.rgb = RGBColor(75, 43, 91)

    # --- SLIDE 2: Final positions ---
    slide2 = prs.slides.add_slide(blank_layout)
    add_morph_transition(slide2, duration_ms=2500)

    try:
        bg_image_stream.seek(0)
        slide2.shapes.add_picture(bg_image_stream, 0, 0, width=prs.slide_width, height=prs.slide_height)
    except (NameError, requests.exceptions.RequestException):
        fill = slide2.background.fill
        fill.gradient()
        fill.gradient_stops[0].color.rgb = RGBColor(217, 87, 0)
        fill.gradient_stops[1].color.rgb = RGBColor(75, 43, 91)

    # Layer 2: Solid Text (Behind Scenery)
    text_box_solid = slide2.shapes.add_textbox(Inches(0.5), Inches(2.5), width=Inches(15), height=Inches(4))
    tf_solid = text_box_solid.text_frame
    p_solid = tf_solid.paragraphs[0]
    p_solid.text = title_text
    p_solid.font.name = 'Arial Black'
    p_solid.font.size = Pt(220)
    p_solid.font.bold = True
    p_solid.font.color.rgb = RGBColor(255, 255, 255)

    # Layer 3: Foreground Scenery Image
    try:
        response_fg = requests.get(foreground_url)
        fg_image_original_stream = BytesIO(response_fg.content)
        fg_image_processed_stream = remove_sky_from_image(fg_image_original_stream)
        pic_scenery = slide2.shapes.add_picture(fg_image_processed_stream, 0, 0, width=prs.slide_width, height=prs.slide_height)
        # Add starting scenery to Slide 1
        fg_image_processed_stream.seek(0)
        slide1.shapes.add_picture(fg_image_processed_stream, off_slide_left, 0, width=prs.slide_width, height=prs.slide_height)
    except requests.exceptions.RequestException:
        print("Foreground image download failed. Skipping scenery layer.")

    # Layer 4: Hollow Text (In Front of Scenery)
    text_box_hollow = slide2.shapes.add_textbox(Inches(0.5), Inches(2.5), width=Inches(15), height=Inches(4))
    run = text_box_hollow.text_frame.paragraphs[0].add_run()
    run.text = title_text
    font = run.font
    font.name = 'Arial Black'
    font.size = Pt(220)
    font.bold = True
    
    rPr = run._r.get_or_add_rPr()
    etree.SubElement(rPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}noFill')
    ln = etree.SubElement(rPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}ln')
    ln.set('w', '10000') # 1pt outline
    solidFill = etree.SubElement(ln, '{http://schemas.openxmlformats.org/drawingml/2006/main}solidFill')
    srgbClr = etree.SubElement(solidFill, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
    srgbClr.set('val', 'FFFFFF')
    
    # Add starting text to Slide 1 (will be invisible, just for morph mapping)
    slide1.shapes.add_textbox(off_slide_left, Inches(2.5), width=Inches(15), height=Inches(4)).text = title_text
    slide1.shapes.add_textbox(off_slide_left, Inches(2.5), width=Inches(15), height=Inches(4)).text = title_text
    
    # Layer 5: UI Elements
    nav_items = ["HOME", "VISIT", "ABOUT", "LOG OUT"]
    positions = [(1, 0.5), (2.5, 0.5), (12, 0.5), (13.5, 0.5)]
    for i, item in enumerate(nav_items):
        shape = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(positions[i][0]), Inches(positions[i][1]), Inches(1.2), Inches(0.4))
        shape.fill.solid(); shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
        shape.line.color.rgb = RGBColor(200, 200, 200); shape.line.width = Pt(1)
        tf = shape.text_frame; tf.text = item
        p = tf.paragraphs[0]; p.font.size = Pt(12); p.font.color.rgb = RGBColor(80, 80, 80)
        # Add starting UI to Slide 1
        slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(positions[i][0]), off_slide_top, Inches(1.2), Inches(0.4)).text = item

    try:
        response_flag = requests.get(flag_url)
        flag_stream = BytesIO(response_flag.content)
        slide2.shapes.add_picture(flag_stream, Inches(7.4), Inches(0.4), height=Inches(0.6))
        # Add starting flag to Slide 1
        flag_stream.seek(0)
        slide1.shapes.add_picture(flag_stream, Inches(7.4), off_slide_top, height=Inches(0.6))
    except requests.exceptions.RequestException:
        print("Flag image download failed.")
        
    prs.save(output_pptx_path)
    return output_pptx_path
