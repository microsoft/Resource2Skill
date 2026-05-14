import os
import random
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from lxml import etree
from PIL import Image, ImageDraw

def create_morphing_gallery(
    output_pptx_path: str,
    slide_data: list,
    **kwargs,
) -> str:
    """
    Creates a PowerPoint presentation with a Morphing Gallery and Windowed Reveal effect.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        slide_data: A list of dictionaries, where each dictionary contains:
                    'image_url': URL to a background image.
                    'title': The main title text for the slide.
                    'subtitle': The smaller subtitle text.
                    'body': The descriptive body text.
    Returns:
        The path to the saved .pptx file.
    """

    # === Helper Functions ===
    def qn(tag):
        nsmap = {
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
            'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        }
        prefix, tagroot = tag.split(':')
        return f'{{{nsmap[prefix]}}}{tagroot}'

    def set_slide_background_fill(shape):
        spPr = shape.element.get_or_add_spPr()
        for fill_prop in [qn("a:noFill"), qn("a:solidFill"), qn("a:gradFill"), qn("a:blipFill"), qn("a:pattFill"), qn("a:grpFill")]:
            if spPr.find(fill_prop) is not None:
                spPr.remove(spPr.find(fill_prop))
        spPr.append(etree.fromstring(f'<a:sldBgFill xmlns:a="{qn("a:")[1:-1]}"/>'))

    def add_offset_center_shadow(shape):
        spPr = shape.element.get_or_add_spPr()
        effectLst = etree.SubElement(spPr, qn("a:effectLst"))
        shadow_xml = f"""
        <a:outerShdw xmlns:a="{qn('a:')[1:-1]}" blurRad="152400" dist="0" dir="0" algn="ctr" rotWithShape="0">
            <a:srgbClr val="000000">
                <a:alpha val="60000"/>
            </a:srgbClr>
        </a:outerShdw>
        """
        effectLst.append(etree.fromstring(shadow_xml))

    def crop_picture_to_oval(pic):
        spPr = pic._pic.spPr
        spPr.insert(0, etree.fromstring(f'<a:prstGeom xmlns:a="{qn("a:")[1:-1]}" prst="ellipse"><a:avLst/></a:prstGeom>'))

    def set_morph_transition(slide):
        slide_xml = slide.element
        transition_xml_str = f'<p:transition xmlns:p="{qn("p:")[1:-1]}"><p:morph/></p:transition>'
        transition_element = etree.fromstring(transition_xml_str)
        csld = slide_xml.find(qn('p:cSld'))
        csld.addnext(transition_element)

    def get_image_from_url(url, fallback_size=(1920, 1080)):
        try:
            image_path, _ = urllib.request.urlretrieve(url)
            return image_path
        except Exception:
            img = Image.new('RGB', fallback_size, color = (20, 20, 30))
            fallback_path = "fallback_image.png"
            img.save(fallback_path)
            return fallback_path
            
    # === Presentation Setup ===
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    
    # Pre-defined layouts for window heights for animation effect
    window_height_patterns = [
        [0.7, 0.85, 1.0, 0.8, 0.6, 0.75],
        [0.8, 0.6, 0.75, 1.0, 0.85, 0.7],
        [1.0, 0.8, 0.6, 0.7, 0.9, 0.75],
        [0.6, 1.0, 0.85, 0.7, 0.75, 0.9],
        [0.75, 0.9, 0.7, 1.0, 0.6, 0.8]
    ]

    # === Slide Generation Loop ===
    for i, data in enumerate(slide_data):
        slide_layout = prs.slide_layouts[6]  # Blank layout
        slide = prs.slides.add_slide(slide_layout)

        # -- Layer 1: Background Image --
        image_path = get_image_from_url(data['image_url'])
        slide.background.fill.solid() # Must add a fill before a picture
        slide.background.fill.picture(image_path)
        if "fallback" not in image_path:
             os.remove(image_path)

        # -- Layer 2: Window Shapes --
        num_windows = 6
        window_width = Inches(1.2)
        total_window_width = num_windows * window_width
        start_left = prs.slide_width - total_window_width - Inches(1.5)
        
        height_pattern = window_height_patterns[i % len(window_height_patterns)]
        for j in range(num_windows):
            max_height = Inches(7)
            h = max_height * height_pattern[j]
            t = (prs.slide_height - h) / 2
            l = start_left + (j * window_width)
            
            # Use MSO_SHAPE.ROUNDED_RECTANGLE
            window = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, window_width, h)
            
            # Make it fully rounded
            # 50000 is 50% which means fully rounded for the smaller dimension.
            window.adjustments[0] = 50000 
            
            # Remove outline
            window.line.fill.background()
            
            # Set fill to slide background and add shadow
            set_slide_background_fill(window)
            add_offset_center_shadow(window)

        # -- Layer 3: Gradient Overlay --
        grad_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        grad_rect.line.fill.background()
        fill = grad_rect.fill
        fill.gradient()
        fill.gradient_angle = 0  # Linear Right
        gs1 = fill.gradient_stops.add()
        gs1.position = 0.0
        gs1.color.rgb = RGBColor(0,0,0)
        gs1.color.brightness = 0
        gs1.alpha = 0 # 0% transparent (solid)
        
        gs2 = fill.gradient_stops.add()
        gs2.position = 1.0
        gs2.color.rgb = RGBColor(0,0,0)
        gs2.color.brightness = 0
        gs2.alpha = 100000 # 100% transparent

        # -- Layer 4: Navigation Thumbnails --
        thumb_small_size = Inches(0.8)
        thumb_large_size = Inches(1.5)
        thumb_start_top = Inches(1)
        thumb_left = Inches(0.5)
        
        for k, thumb_data in enumerate(slide_data):
            size = thumb_large_size if i == k else thumb_small_size
            top = thumb_start_top + k * (thumb_small_size + Inches(0.2))
            
            thumb_image_path = get_image_from_url(thumb_data['image_url'])
            pic = slide.shapes.add_picture(thumb_image_path, thumb_left, top, height=size)
            if "fallback" not in thumb_image_path:
                os.remove(thumb_image_path)
            
            crop_picture_to_oval(pic)

        # -- Layer 5: Text --
        title_box = slide.shapes.add_textbox(Inches(2.5), Inches(1.5), Inches(6), Inches(1.5))
        p = title_box.text_frame.paragraphs[0]
        p.text = data['title']
        p.font.name = 'Arial Black'
        p.font.size = Pt(40)
        p.font.color.rgb = RGBColor(255, 255, 255)

        subtitle_box = slide.shapes.add_textbox(Inches(2.5), Inches(2.5), Inches(6), Inches(0.5))
        p = subtitle_box.text_frame.paragraphs[0]
        p.text = data['subtitle']
        p.font.name = 'Arial'
        p.font.size = Pt(20)
        p.font.color.rgb = RGBColor(200, 200, 200)

        body_box = slide.shapes.add_textbox(Inches(2.5), Inches(3.2), Inches(4), Inches(2))
        tf = body_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = data['body']
        p.font.name = 'Arial'
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(180, 180, 180)

        # -- Final Step: Apply Transition --
        set_morph_transition(slide)

    prs.save(output_pptx_path)
    if os.path.exists("fallback_image.png"):
        os.remove("fallback_image.png")
    return output_pptx_path

# Example usage:
if __name__ == '__main__':
    sample_slide_data = [
        {
            "image_url": "https://images.pexels.com/photos/33041/antelope-canyon-lower-canyon-arizona.jpg",
            "title": "WELCOME",
            "subtitle": "PowerPoint Wizard",
            "body": "Welcome to my channel dedicated to sharing PowerPoint tips and tutorials! Whether you're new to PowerPoint or a seasoned pro, our channel has something for you."
        },
        {
            "image_url": "https://images.pexels.com/photos/417054/pexels-photo-417054.jpeg",
            "title": "TO",
            "subtitle": "PowerPoint Wizard",
            "body": "Discover new design techniques, animation tricks, and productivity hacks to make your presentations stand out."
        },
        {
            "image_url": "https://images.pexels.com/photos/355465/pexels-photo-355465.jpeg",
            "title": "MY YOUTUBE",
            "subtitle": "PowerPoint Wizard",
            "body": "We believe that a great presentation can make a huge impact. Let us show you how to create slides that captivate and inform."
        },
        {
            "image_url": "https://images.pexels.com/photos/3225517/pexels-photo-3225517.jpeg",
            "title": "CHANNEL",
            "subtitle": "PowerPoint Wizard",
            "body": "Join our community of presentation enthusiasts and elevate your PowerPoint skills to the next level."
        },
        {
            "image_url": "https://images.pexels.com/photos/2387873/pexels-photo-2387873.jpeg",
            "title": "THANKS",
            "subtitle": "PowerPoint Wizard",
            "body": "Thank you for watching! Don't forget to subscribe for more tutorials and tips. Let's create something amazing together."
        }
    ]

    output_file = "Morphing_Gallery_Presentation.pptx"
    create_morphing_gallery(output_file, sample_slide_data)
    print(f"Presentation saved to {output_file}")
