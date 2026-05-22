import os
import io
import urllib.request
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from lxml import etree

def generate_placeholder_image(text, size=(400, 500), bg_color=(200, 200, 220), text_color=(100, 100, 120)):
    """Generates a fallback image using PIL if web fetching fails."""
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    # Simple centered text (initials)
    font_size = 80
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    
    # Calculate text bounding box for centering
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((size[0]-w)/2, (size[1]-h)/2), text, font=font, fill=text_color)
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

def fetch_image_or_fallback(url, fallback_text):
    """Attempts to fetch an image, returns PIL generated image on failure."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            image_data = response.read()
            return io.BytesIO(image_data)
    except Exception:
        return generate_placeholder_image(fallback_text)

def apply_morph_transition(slide):
    """Injects Morph transition XML into a python-pptx slide."""
    slide_elm = slide._element
    # Check if transition already exists
    transition = slide_elm.find('{http://schemas.openxmlformats.org/presentationml/2006/main}transition')
    if transition is None:
        transition = etree.SubElement(slide_elm, '{http://schemas.openxmlformats.org/presentationml/2006/main}transition')
    
    # Clear existing transitions if any
    for child in list(transition):
        transition.remove(child)
        
    # Add morph transition
    morph = etree.SubElement(transition, '{http://schemas.openxmlformats.org/presentationml/2006/main}morph')
    morph.set('option', 'byObject')

def create_slide(
    output_pptx_path: str = "Team_Carousel_Morph.pptx",
    accent_color: tuple = (24, 134, 131), # Deep Teal
    bg_color: tuple = (245, 245, 245),    # Light Gray
    **kwargs
) -> str:
    """
    Creates a presentation with a vertical scrolling morph carousel for team profiles.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Team Data
    team_data = [
        {
            "name": "ALEX",
            "surname": "MERCER",
            "role": "LEAD DESIGNER",
            "bio": "Alex brings 10 years of experience in human-computer interaction. Some text goes here. Some text goes here. She believes in form following function, ensuring all interfaces are beautiful and intuitive.",
            "img_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=500&fit=crop"
        },
        {
            "name": "JULIAN",
            "surname": "BAKER",
            "role": "SYSTEMS ARCHITECT",
            "bio": "Julian specializes in scalable cloud infrastructure. Some text goes here. Some text goes here. He ensures our backend runs smoothly under high load and maintains robust security protocols.",
            "img_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=500&fit=crop"
        },
        {
            "name": "SOPHIA",
            "surname": "CHEN",
            "role": "PRODUCT MANAGER",
            "bio": "Sophia bridges the gap between engineering and marketing. Some text goes here. Some text goes here. With a sharp eye for market trends, she guides the product roadmap to success.",
            "img_url": "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=400&h=500&fit=crop"
        }
    ]

    # Pre-fetch images to ensure consistent aspect ratios and avoiding lag in loop
    images = []
    for member in team_data:
        images.append(fetch_image_or_fallback(member["img_url"], member["name"][0] + member["surname"][0]))

    # Layout configurations
    img_width = Inches(3.0)
    img_height = Inches(3.75)
    img_x = Inches(8.5) # Anchored to the right
    active_y = Inches(1.875) # Centered vertically: (7.5 - 3.75) / 2
    y_spacing = Inches(4.0) # Height + padding

    # Create one slide per team member
    for i, active_member in enumerate(team_data):
        slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
        
        # Apply background color via rectangle
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(*bg_color)
        bg.line.fill.background()

        # Place the image track
        for j, img_stream in enumerate(images):
            # Calculate dynamic Y position based on distance from the active index (i)
            current_y = active_y + ((j - i) * y_spacing)
            
            pic = slide.shapes.add_picture(img_stream, img_x, current_y, width=img_width, height=img_height)
            # Give pictures a name so Morph tracks them perfectly across slides
            pic.name = f"ProfilePic_{j}" 

        # Place Text elements ONLY for the active member
        # 1. Designation Pill Shape
        pill_width = Inches(2.5)
        pill_height = Inches(0.5)
        pill_x = Inches(1.5)
        pill_y = Inches(2.2)
        
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, pill_x, pill_y, pill_width, pill_height)
        # Adjust pill roundness using adjust value (100000 is fully rounded)
        if pill.adjustments:
            pill.adjustments[0] = 0.5 
            
        pill.fill.solid()
        pill.fill.fore_color.rgb = RGBColor(*accent_color)
        pill.line.fill.background()
        
        tf = pill.text_frame
        tf.text = active_member["role"]
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.size = Pt(14)
        tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        
        # 2. Name & Surname
        text_box_x = Inches(4.5)
        name_y = Inches(2.0)
        
        name_box = slide.shapes.add_textbox(text_box_x, name_y, Inches(3.5), Inches(1.5))
        tf_name = name_box.text_frame
        
        p1 = tf_name.add_paragraph()
        p1.text = active_member["name"]
        p1.font.size = Pt(36)
        p1.font.bold = True
        p1.font.color.rgb = RGBColor(40, 40, 40)
        
        p2 = tf_name.add_paragraph()
        p2.text = active_member["surname"]
        p2.font.size = Pt(48)
        p2.font.bold = True
        p2.font.color.rgb = RGBColor(20, 20, 20)
        
        # 3. Bio Description
        bio_y = Inches(3.8)
        bio_box = slide.shapes.add_textbox(text_box_x, bio_y, Inches(3.5), Inches(2.0))
        tf_bio = bio_box.text_frame
        tf_bio.word_wrap = True
        
        p_bio = tf_bio.paragraphs[0]
        p_bio.text = active_member["bio"]
        p_bio.font.size = Pt(12)
        p_bio.font.color.rgb = RGBColor(100, 100, 100)

        # Apply Morph Transition to this slide
        apply_morph_transition(slide)

    prs.save(output_pptx_path)
    return output_pptx_path

if __name__ == "__main__":
    out_path = create_slide()
    print(f"Presentation saved successfully at: {out_path}")
