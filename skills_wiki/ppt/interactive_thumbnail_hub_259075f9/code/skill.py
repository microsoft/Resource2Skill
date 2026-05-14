import os
import io
import random
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image, ImageDraw, ImageFont, ImageOps
from lxml import etree

# Helper to register namespaces for lxml
def register_namespaces():
    return {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main',
        'p188': 'http://schemas.microsoft.com/office/powerpoint/2018/8/main'
    }

def create_slide(
    output_pptx_path: str,
    section_titles: list = None,
    **kwargs,
) -> str:
    """
    Creates a PPTX file with an interactive thumbnail hub agenda.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        section_titles: A list of strings for the section titles.

    Returns:
        The path to the saved PPTX file.
    """
    if section_titles is None:
        section_titles = [
            "SWOT Analysis", "SCQA Framework", "BCG Matrix",
            "Ansoff Matrix", "Eisenhower Matrix", "Risk-Reward Matrix",
            "Perceptual Map", "Mendelow's Matrix", "Competitive Advantage"
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # --- 1. Create the Hub Slide (Agenda) ---
    hub_slide_layout = prs.slide_layouts[6] # Blank layout
    hub_slide = prs.slides.add_slide(hub_slide_layout)
    
    # Set hub background color
    background = hub_slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(240, 238, 233)
    
    # Add a title to the hub slide
    title_shape = hub_slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12), Inches(1))
    tf = title_shape.text_frame
    p = tf.paragraphs[0]
    p.text = "Table of Contents"
    p.font.bold = True
    p.font.size = Pt(44)
    p.font.color.rgb = RGBColor(30, 30, 30)

    # --- 2. Create Content Slides and Generate Thumbnails ---
    content_slides = []
    thumbnail_paths = []
    
    # Define a set of random colors for slide backgrounds
    color_palette = [
        (68, 84, 106), (107, 124, 147), (204, 112, 85), (84, 139, 84),
        (75, 123, 166), (204, 85, 85), (75, 159, 151), (142, 124, 107), (221, 168, 68)
    ]
    random.shuffle(color_palette)

    for i, title in enumerate(section_titles):
        slide = prs.slides.add_slide(hub_slide_layout)
        content_slides.append(slide)

        # Add background color
        bg_color = color_palette[i % len(color_palette)]
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(*bg_color)

        # Add title to content slide
        content_title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12), Inches(1.5))
        tf = content_title_shape.text_frame
        p = tf.paragraphs[0]
        p.text = title.upper()
        p.font.bold = True
        p.font.size = Pt(40)
        p.font.color.rgb = RGBColor(255, 255, 255)

        # --- Generate Thumbnail using PIL ---
        thumb_w, thumb_h = 480, 270
        img = Image.new('RGB', (thumb_w, thumb_h), color=bg_color)
        draw = ImageDraw.Draw(img)
        try:
            # Use a common system font, with a fallback
            font = ImageFont.truetype("Arial.ttf", 20)
        except IOError:
            font = ImageFont.load_default()
        
        text_bbox = draw.textbbox((0, 0), title.upper(), font=font)
        text_w, text_h = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        draw.text(((thumb_w - text_w) / 2, (thumb_h - text_h) / 2), title.upper(), font=font, fill=(255, 255, 255))
        
        # Add a subtle white border
        img_with_border = ImageOps.expand(img, border=3, fill='white')

        # Save to a byte stream
        img_byte_arr = io.BytesIO()
        img_with_border.save(img_byte_arr, format='PNG')
        thumbnail_paths.append(img_byte_arr)

    # --- 3. Add "Home" buttons to content slides ---
    for slide in content_slides:
        # The home button links to the first slide in the presentation
        home_button = slide.shapes.add_shape(MSO_SHAPE.ACTION_BUTTON_HOME, Inches(12.5), Inches(6.7), Inches(0.6), Inches(0.6))
        
        # This python-pptx call creates the basic shape, but the hyperlink action is set by default in the XML.
        # For full control, lxml could be used to ensure the hyperlink points to the first slide.
        # The default behavior of ACTION_BUTTON_HOME is already "Hyperlink to: First Slide", which is what we want.
        # So, no extra XML manipulation is needed for this specific use case.
        
    # --- 4. Add Slide Zoom objects to Hub Slide using lxml ---
    ns = register_namespaces()
    
    # Grid layout parameters
    cols = 3
    rows = (len(section_titles) + cols - 1) // cols
    thumb_w_in, thumb_h_in = 3.5, 1.97
    start_x, start_y = Inches(1.4), Inches(1.5)
    gap_x, gap_y = Inches(0.2), Inches(0.2)

    for i, slide in enumerate(content_slides):
        row = i // cols
        col = i % cols
        x = start_x + col * (Inches(thumb_w_in) + gap_x)
        y = start_y + row * (Inches(thumb_h_in) + gap_y)

        # Add image part to presentation
        image_part, rId_img = hub_slide.part.get_or_add_image_part(thumbnail_paths[i])
        
        # Add relationship from hub slide to target slide
        target_slide_part = slide.part
        rId_slide = hub_slide.part.relate_to(target_slide_part, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide")

        # Create the XML structure for the Slide Zoom
        graphic_frame = etree.fromstring(f"""
        <p:graphicFrame xmlns:p="{ns['p']}" xmlns:a="{ns['a']}" xmlns:r="{ns['r']}">
            <p:nvGraphicFramePr>
                <p:cNvPr id="{10+i}" name="Zoom"/>
                <p:cNvGraphicFramePr/>
                <p:nvPr/>
            </p:nvGraphicFramePr>
            <p:xfrm>
                <a:off x="{int(x)}" y="{int(y)}"/>
                <a:ext cx="{int(Inches(thumb_w_in))}" cy="{int(Inches(thumb_h_in))}"/>
            </p:xfrm>
            <a:graphic>
                <a:graphicData uri="http://schemas.microsoft.com/office/powerpoint/2018/8/main">
                    <p188:zoom xmlns:p188="{ns['p188']}" r:id="{rId_slide}">
                        <p188:img r:embed="{rId_img}" />
                    </p188:zoom>
                </a:graphicData>
            </a:graphic>
        </p:graphicFrame>
        """)
        
        hub_slide.shapes._spTree.append(graphic_frame)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# if __name__ == '__main__':
#     output_file = "interactive_agenda.pptx"
#     create_slide(output_file)
#     print(f"Presentation saved to {output_file}")
#     if os.name == 'nt': # For Windows
#         os.startfile(output_file)
#     elif os.name == 'posix': # For MacOS/Linux
#         import subprocess
#         subprocess.call(['open', output_file])

