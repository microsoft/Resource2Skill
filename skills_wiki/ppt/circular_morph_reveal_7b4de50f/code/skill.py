import math
from io import BytesIO
import requests
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.drawing.fill import FillFormat
from pptx.oxml.ns import nsdecls
from pptx.oxml import parse_xml

# Helper for lxml to handle namespaces
from lxml import etree
def qn(tag):
    """
    Stands for 'qualified name', a utility function to turn a namespace
    prefixed tag name into a Clark-notation qualified tag name for lxml.
    """
    prefix, tagroot = tag.split(':')
    uri = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    }[prefix]
    return f'{{{uri}}}{tagroot}'

def _set_morph_transition(slide):
    """Injects the Morph transition XML into a slide."""
    slide_xml = slide._element
    transition_xml = f"""
    <p:transition {nsdecls('p', 'r')}>
        <p:morph/>
    </p:transition>
    """
    transition_element = parse_xml(transition_xml)
    slide_xml.insert(2, transition_element)

def _get_image_from_url(url, fallback_color=(100, 100, 100)):
    """Downloads an image from a URL or provides a solid color fallback."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return BytesIO(response.content)
    except requests.exceptions.RequestException:
        print(f"Warning: Could not download image from {url}. Using fallback color.")
        img = Image.new('RGB', (100, 100), color=fallback_color)
        fallback_io = BytesIO()
        img.save(fallback_io, format='PNG')
        fallback_io.seek(0)
        return fallback_io

def create_circular_morph_reveal(
    output_pptx_path: str,
    topics: list,
    main_title: str = "Healthy Living",
) -> str:
    """
    Creates a PPTX file with the Circular Morph Reveal effect.

    Args:
        output_pptx_path: Path to save the output .pptx file.
        topics: A list of dictionaries, where each dict contains:
                'title': The slide title (str).
                'text': The bullet points (list of str).
                'image_url': URL for the segment image (str).
                'bg_url': URL for the slide background image (str).
        main_title: The title in the center of the wheel on the first slide.

    Returns:
        Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    num_segments = len(topics)
    angle_step = 360 / num_segments
    
    # --- Slide 1: Title Slide ---
    slide1 = prs.slides.add_slide(blank_layout)
    
    # Set background
    bg_img_stream = _get_image_from_url(topics[0]['bg_url'])
    slide1.background.fill.picture(bg_img_stream)

    # Make background slightly transparent/faded
    fill = slide1.background.fill
    fill.solid() # Must be solid before setting transparency
    fill.fore_color.rgb = RGBColor(255, 255, 255)
    picture_fill = slide1.background.fill._xPr.find(qn('a:blipFill'))
    if picture_fill is not None:
        props = etree.SubElement(picture_fill, qn('a:blip'))
        alpha_mod = etree.SubElement(props, qn('a:alphaModFix'))
        alpha_mod.set('amt', '80000') # 80% transparent

    # Add shapes
    group_shape = slide1.shapes.add_group_shape()
    center_x, center_y = Inches(3.5), prs.slide_height / 2
    outer_radius, inner_radius = Inches(2.5), Inches(1.5)

    for i, topic in enumerate(topics):
        start_angle = i * angle_step
        end_angle = (i + 1) * angle_step
        
        shape = group_shape.shapes.add_shape(MSO_SHAPE.ACTION_BUTTON_BLANK, Inches(1), Inches(1), Inches(1), Inches(1))
        sp = shape._sp
        sp.nvSpPr.cNvSpPr.txBox = "1" # Allow text, which enables picture fill
        
        # Create donut segment geometry
        path = etree.Element(qn('a:custGeom'))
        avLst = etree.SubElement(path, qn('a:avLst'))
        pathLst = etree.SubElement(path, qn('a:pathLst'))
        path_el = etree.SubElement(pathLst, qn('a:path'))
        path_el.set('w', str(int(2*outer_radius)))
        path_el.set('h', str(int(2*outer_radius)))

        num_points_per_arc = 20
        # Outer arc
        for j in range(num_points_per_arc + 1):
            angle = math.radians(start_angle + (end_angle - start_angle) * j / num_points_per_arc)
            x = int(outer_radius + outer_radius * math.cos(angle))
            y = int(outer_radius + outer_radius * math.sin(angle))
            if j == 0:
                etree.SubElement(path_el, qn('a:moveTo')).append(etree.Element(qn('a:pt'), x=str(x), y=str(y)))
            else:
                etree.SubElement(path_el, qn('a:lnTo')).append(etree.Element(qn('a:pt'), x=str(x), y=str(y)))
        
        # Inner arc (in reverse)
        for j in range(num_points_per_arc, -1, -1):
            angle = math.radians(start_angle + (end_angle - start_angle) * j / num_points_per_arc)
            x = int(outer_radius + inner_radius * math.cos(angle))
            y = int(outer_radius + inner_radius * math.sin(angle))
            etree.SubElement(path_el, qn('a:lnTo')).append(etree.Element(qn('a:pt'), x=str(x), y=str(y)))

        etree.SubElement(path_el, qn('a:close'))
        
        sp.spPr.prstGeom.getparent().replace(sp.spPr.prstGeom, path)

        shape.width, shape.height = int(2*outer_radius), int(2*outer_radius)
        shape.left, shape.top = int(center_x-outer_radius), int(center_y-outer_radius)
        
        # Fill with image
        img_stream = _get_image_from_url(topic['image_url'])
        shape.fill.picture(img_stream)
        shape.line.fill.background()
        shape.name = f"Segment_{i}" # Name for Morph to track

    # Add central circle and title
    slide1.shapes.add_shape(MSO_SHAPE.OVAL, center_x - inner_radius, center_y - inner_radius, 2*inner_radius, 2*inner_radius).fill.solid.fore_color.rgb = RGBColor(255, 255, 255)
    tx_box = slide1.shapes.add_textbox(center_x - Inches(1), center_y - Inches(0.5), Inches(2), Inches(1))
    p = tx_box.text_frame.paragraphs[0]
    p.text = main_title
    p.font.name = "Georgia"
    p.font.size = Pt(36)
    p.font.bold = True
    
    # --- Slides 2 to N: Topic Slides ---
    for i, topic in enumerate(topics):
        slide = prs.slides.add_slide(blank_layout)
        _set_morph_transition(slide)

        # Background
        bg_img_stream = _get_image_from_url(topic['bg_url'])
        slide.background.fill.picture(bg_img_stream)
        fill = slide.background.fill
        fill.solid() 
        fill.fore_color.rgb = RGBColor(255, 255, 255)
        picture_fill = slide.background.fill._xPr.find(qn('a:blipFill'))
        if picture_fill is not None:
            props = etree.SubElement(picture_fill, qn('a:blip'))
            alpha_mod = etree.SubElement(props, qn('a:alphaModFix'))
            alpha_mod.set('amt', '60000')

        # Add donut shapes in their new positions
        rotation_angle = - (i * angle_step)
        group = slide.shapes.add_group_shape()
        group.rotation = rotation_angle
        
        for j, t in enumerate(topics):
            start_angle = j * angle_step
            end_angle = (j + 1) * angle_step

            # Re-create the same shape geometry as slide 1
            shape = group.shapes.add_shape(MSO_SHAPE.ACTION_BUTTON_BLANK, Inches(1), Inches(1), Inches(1), Inches(1))
            sp = shape._sp
            sp.nvSpPr.cNvSpPr.txBox = "1"
            path = etree.Element(qn('a:custGeom'))
            etree.SubElement(path, qn('a:avLst'))
            pathLst = etree.SubElement(path, qn('a:pathLst'))
            path_el = etree.SubElement(pathLst, qn('a:path'), w=str(int(2*outer_radius)), h=str(int(2*outer_radius)))
            for k in range(num_points_per_arc + 1):
                angle = math.radians(start_angle + (end_angle - start_angle) * k / num_points_per_arc)
                x, y = int(outer_radius + outer_radius * math.cos(angle)), int(outer_radius + outer_radius * math.sin(angle))
                if k == 0: etree.SubElement(path_el, qn('a:moveTo')).append(etree.Element(qn('a:pt'), x=str(x), y=str(y)))
                else: etree.SubElement(path_el, qn('a:lnTo')).append(etree.Element(qn('a:pt'), x=str(x), y=str(y)))
            for k in range(num_points_per_arc, -1, -1):
                angle = math.radians(start_angle + (end_angle - start_angle) * k / num_points_per_arc)
                x, y = int(outer_radius + inner_radius * math.cos(angle)), int(outer_radius + inner_radius * math.sin(angle))
                etree.SubElement(path_el, qn('a:lnTo')).append(etree.Element(qn('a:pt'), x=str(x), y=str(y)))
            etree.SubElement(path_el, qn('a:close'))
            sp.spPr.prstGeom.getparent().replace(sp.spPr.prstGeom, path)

            shape.width, shape.height = int(2*outer_radius), int(2*outer_radius)
            shape.left, shape.top = int(center_x-outer_radius), int(center_y-outer_radius)

            img_stream = _get_image_from_url(t['image_url'])
            shape.fill.picture(img_stream)
            shape.line.fill.background()
            shape.name = f"Segment_{j}"
            
            # Pop out the active segment
            if j == i:
                shape.left += Inches(0.5)

        # Add text content
        tx_box = slide.shapes.add_textbox(Inches(7.5), Inches(1.5), Inches(5), Inches(4.5))
        tf = tx_box.text_frame
        p_title = tf.paragraphs[0]
        p_title.text = topic['title']
        p_title.font.name = "Georgia"
        p_title.font.size = Pt(44)
        p_title.font.bold = True

        for line in topic['text']:
            p_body = tf.add_paragraph()
            p_body.text = line
            p_body.font.size = Pt(20)
            p_body.level = 1

    prs.save(output_pptx_path)
    return output_pptx_path

if __name__ == '__main__':
    from PIL import Image

    # --- Sample Data ---
    sample_topics = [
        {
            "title": "Good Night Sleep",
            "text": ["Ensure you get 7-9 hours of quality sleep each night.", "Establish a regular sleep schedule and create a relaxing bedtime routine."],
            "image_url": "https://images.unsplash.com/photo-1534790566855-4B819d5161b3?w=800",
            "bg_url": "https://images.unsplash.com/photo-1536746803837-3a13af1455ea?w=1200"
        },
        {
            "title": "Stay Hydrated",
            "text": ["Drink an adequate amount of water throughout the day.", "Limit sugary drinks and excessive caffeine."],
            "image_url": "https://images.unsplash.com/photo-1563224536-3722a5fe691b?w=800",
            "bg_url": "https://images.unsplash.com/photo-1542345558-151a6c475632?w=1200"
        },
        {
            "title": "Healthy Diet",
            "text": ["Eat a variety of fruits, vegetables, whole grains, and lean proteins.", "Limit processed foods and excessive red meat."],
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800",
            "bg_url": "https://images.unsplash.com/photo-1543362906-acfc16c67564?w=1200"
        },
        {
            "title": "Regular Exercise",
            "text": ["Aim for at least 150 minutes of moderate aerobic exercise per week.", "Include strength training at least twice a week."],
            "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800",
            "bg_url": "https://images.unsplash.com/photo-1534255534162-55f144421b5a?w=1200"
        },
        {
            "title": "Avoid Smoking",
            "text": ["Avoid smoking and limit exposure to secondhand smoke.", "If you drink alcohol, do so in moderation."],
            "image_url": "https://images.unsplash.com/photo-1620227184231-831414300642?w=800",
            "bg_url": "https://images.unsplash.com/photo-1507525428034-b723a996f329?w=1200"
        },
        {
            "title": "Low Stress",
            "text": ["Practice stress-reducing techniques like meditation or yoga.", "Take breaks and engage in activities you enjoy."],
            "image_url": "https://images.unsplash.com/photo-1506126613408-4e7e9b78bf77?w=800",
            "bg_url": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1200"
        }
    ]

    output_file = "circular_morph_reveal.pptx"
    create_circular_morph_reveal(output_file, sample_topics, main_title="Healthy Living")
    print(f"Presentation saved to {output_file}")
