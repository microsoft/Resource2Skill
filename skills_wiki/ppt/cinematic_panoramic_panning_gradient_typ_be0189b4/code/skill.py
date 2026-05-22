import os
import io
import copy
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from lxml import etree

def download_image(url: str) -> io.BytesIO:
    """Download an image from a URL and return it as a BytesIO object."""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    return io.BytesIO(response.read())

def apply_morph_transition(slide):
    """Injects the XML required for the Morph (平滑) transition into the slide."""
    sld_xml = slide._element
    # Remove existing transitions if any to prevent conflicts
    for child in sld_xml:
        if child.tag.endswith('transition'):
            sld_xml.remove(child)
    
    # Construct the Morph transition XML
    transition_xml = '''
    <p:transition spd="slow" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
        <p:morph/>
    </p:transition>
    '''
    morph_element = etree.fromstring(transition_xml)
    sld_xml.append(morph_element)

def apply_text_gradient_xml(shape, angle_deg=90):
    """
    Injects OOXML to apply a White-to-Transparent gradient fill to text.
    angle_deg: 90 is top-to-bottom, 0 is left-to-right.
    """
    # OOXML angle: 60000 units per degree
    ang_val = int(angle_deg * 60000)
    
    grad_fill_xml = f'''
    <a:gradFill rotWithShape="1" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:gsLst>
            <a:gs pos="0">
                <a:srgbClr val="FFFFFF"><a:alpha val="100000"/></a:srgbClr>
            </a:gs>
            <a:gs pos="100000">
                <a:srgbClr val="FFFFFF"><a:alpha val="0"/></a:srgbClr>
            </a:gs>
        </a:gsLst>
        <a:lin ang="{ang_val}" scaled="1"/>
    </a:gradFill>
    '''
    grad_fill_element = etree.fromstring(grad_fill_xml)

    # Apply to all text runs in the shape
    for paragraph in shape.text_frame.paragraphs:
        for run in paragraph.runs:
            rPr = run._r.get_or_add_rPr()
            # Remove solid fill if it exists
            for child in rPr:
                if child.tag.endswith('solidFill'):
                    rPr.remove(child)
            # Append the gradient fill
            rPr.append(copy.deepcopy(grad_fill_element))

def create_slide(
    output_pptx_path: str = "Cinematic_Journey_Morph.pptx",
    title_text: str = "JOURNEY",
    subtitle_text: str = "TO THE SECRET LAND",
    body_text: str = "Explore the untouched wilderness and experience nature like never before. \nA five-day immersive expedition.",
    bg_image_url: str = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2400&auto=format&fit=crop", 
    **kwargs,
) -> str:
    """
    Creates a 2-slide presentation demonstrating the cinematic panning 
    and transparent gradient text effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333) # 16:9 Aspect Ratio
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Fetch the ultra-wide background image once
    try:
        bg_img_stream = download_image(bg_image_url)
    except Exception as e:
        print(f"Failed to download image. Please check internet connection. Error: {e}")
        return ""

    # Dimensions for the oversized panoramic image
    # Canvas is 13.333" wide. We make the image 22" wide to allow panning.
    img_width = Inches(22)
    img_height = Inches(7.5)

    # ==========================================
    # SLIDE 1: The Initial View (Left aligned)
    # ==========================================
    slide_1 = prs.slides.add_slide(blank_layout)
    
    # Background Image (Positioned at Left = 0)
    slide_1.shapes.add_picture(bg_img_stream, 0, 0, width=img_width, height=img_height)
    
    # Dark subtle overlay for text readability
    overlay_1 = slide_1.shapes.add_shape(1, 0, 0, Inches(13.333), Inches(7.5))
    overlay_1.fill.solid()
    overlay_1.fill.fore_color.rgb = RGBColor(0, 0, 0)
    overlay_1.fill.transparency = 0.6
    overlay_1.line.fill.background()

    # Main Artistic Title (Left side)
    title_box_1 = slide_1.shapes.add_textbox(Inches(1), Inches(2), Inches(6), Inches(2))
    tf_1 = title_box_1.text_frame
    p_1 = tf_1.paragraphs[0]
    run_1 = p_1.add_run()
    run_1.text = title_text
    run_1.font.size = Pt(96)
    run_1.font.name = "Georgia"
    run_1.font.bold = True
    # Apply the secret sauce: Transparent Gradient via XML
    apply_text_gradient_xml(title_box_1, angle_deg=90)

    # Subtitle
    sub_box_1 = slide_1.shapes.add_textbox(Inches(1.2), Inches(3.8), Inches(4), Inches(1))
    sub_p_1 = sub_box_1.text_frame.paragraphs[0]
    sub_run_1 = sub_p_1.add_run()
    sub_run_1.text = subtitle_text
    sub_run_1.font.size = Pt(16)
    sub_run_1.font.color.rgb = RGBColor(255, 255, 255)
    sub_run_1.font.name = "Arial"
    
    # Add Morph Transition to Slide 1
    apply_morph_transition(slide_1)


    # ==========================================
    # SLIDE 2: The Panned View (Right aligned)
    # ==========================================
    slide_2 = prs.slides.add_slide(blank_layout)
    
    # Background Image (Positioned at Left = -8.667 to pan right)
    bg_img_stream.seek(0) # Reset stream
    # By using the exact same image and just shifting X, PPT 'Morph' will pan it!
    slide_2.shapes.add_picture(bg_img_stream, -Inches(8.667), 0, width=img_width, height=img_height)

    # Dark subtle overlay
    overlay_2 = slide_2.shapes.add_shape(1, 0, 0, Inches(13.333), Inches(7.5))
    overlay_2.fill.solid()
    overlay_2.fill.fore_color.rgb = RGBColor(0, 0, 0)
    overlay_2.fill.transparency = 0.5
    overlay_2.line.fill.background()

    # Main Artistic Title (Shifted to the right side, changed text for storyline)
    title_box_2 = slide_2.shapes.add_textbox(Inches(6), Inches(1.5), Inches(6), Inches(2))
    tf_2 = title_box_2.text_frame
    p_2 = tf_2.paragraphs[0]
    p_2.alignment = PP_ALIGN.RIGHT
    run_2 = p_2.add_run()
    run_2.text = "DESTINATION"
    run_2.font.size = Pt(80)
    run_2.font.name = "Georgia"
    run_2.font.bold = True
    # Apply gradient again
    apply_text_gradient_xml(title_box_2, angle_deg=70)

    # Body Text (Details of the tour)
    body_box = slide_2.shapes.add_textbox(Inches(6.5), Inches(3.5), Inches(5.5), Inches(2))
    body_p = body_box.text_frame.paragraphs[0]
    body_p.alignment = PP_ALIGN.RIGHT
    body_run = body_p.add_run()
    body_run.text = body_text
    body_run.font.size = Pt(14)
    body_run.font.color.rgb = RGBColor(220, 220, 220)
    
    # Add Morph Transition to Slide 2
    apply_morph_transition(slide_2)

    prs.save(output_pptx_path)
    return output_pptx_path

if __name__ == "__main__":
    # Test the function
    output_path = create_slide()
    print(f"Presentation saved successfully to: {output_path}")
    print("Open the file in PowerPoint and enter Presentation Mode to view the seamless pan and gradient text.")
