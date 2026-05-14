import os
import io
import requests
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.action import PP_ACTION
from PIL import Image, ImageDraw, ImageOps, ImageFont
from lxml import etree

# Helper to add namespaces for lxml
def qn(tag):
    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'
    }
    prefix, tagroot = tag.split(':')
    return f'{{{ns[prefix]}}}{tagroot}'

def set_morph_transition(slide, prs):
    """Injects XML to set the Morph transition for a slide."""
    slide_id = slide.slide_id
    slide_part = prs.part.related_parts[slide.rId]
    sld = slide_part.element
    
    # Check if a transition element already exists, remove it if so
    existing_transition = sld.find(qn('p:transition'))
    if existing_transition is not None:
        sld.remove(existing_transition)

    # Create the new transition element
    transition = etree.SubElement(sld, qn('p:transition'), {qn('p14:dur'): "1000"})
    morph = etree.SubElement(transition, qn('p:morph'))
    return sld

def create_rounded_image(img_path, size, radius, grayscale=False):
    """Creates a rounded-corner, optionally grayscaled image as a PNG in memory."""
    try:
        if img_path.startswith('http'):
            response = requests.get(img_path, stream=True)
            response.raise_for_status()
            image_file = io.BytesIO(response.content)
            im = Image.open(image_file)
        else:
            im = Image.open(img_path)
    except Exception as e:
        print(f"Could not load image {img_path}. Using placeholder. Error: {e}")
        im = Image.new('RGB', (800, 1200), color = 'gray')

    if grayscale:
        im = ImageOps.grayscale(im)
    
    im = im.convert("RGBA")

    # Resize and crop to fit the target size
    im_w, im_h = im.size
    target_w, target_h = size
    scale = max(target_w / im_w, target_h / im_h)
    new_w, new_h = int(im_w * scale), int(im_h * scale)
    im = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    left = (new_w - target_w) / 2
    top = (new_h - target_h) / 2
    right = (new_w + target_w) / 2
    bottom = (new_h + target_h) / 2
    im = im.crop((left, top, right, bottom))
    
    # Create rounded mask
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + size, radius, fill=255)
    
    im.putalpha(mask)
    
    img_byte_arr = io.BytesIO()
    im.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

def create_team_showcase_slide(output_pptx_path: str, team_data: list) -> str:
    """
    Creates a PPTX file reproducing the Interactive Morphing Team Showcase.

    Args:
        output_pptx_path (str): The path to save the generated .pptx file.
        team_data (list): A list of dictionaries, each containing info for a team member.
                          Example: 
                          [
                              {
                                  "name": "Jennifer", "role": "Advertising\nCOPYWRITER", "desc": "...",
                                  "image_url": "url_to_image_1.jpg", "role_tag": "Copywriter"
                              }, ...
                          ]

    Returns:
        str: Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    blank_layout = prs.slide_layouts[6]
    
    accent_color = RGBColor(237, 125, 49)
    
    # --- Slide 0: Title/Overview Slide ---
    slide0 = prs.slides.add_slide(blank_layout)
    
    # Background (subtle gradient)
    fill = slide0.background.fill
    fill.gradient()
    fill.gradient_stops[0].color.rgb = RGBColor(242, 242, 242)
    fill.gradient_stops[1].color.rgb = RGBColor(220, 220, 220)

    # Title
    txBox = slide0.shapes.add_textbox(Inches(1), Inches(1), Inches(5), Inches(1))
    p = txBox.text_frame.paragraphs[0]
    p.text = "Meet"
    p.font.name = "Helvetica Light"
    p.font.size = Pt(60)
    
    txBox2 = slide0.shapes.add_textbox(Inches(1), Inches(2.2), Inches(5), Inches(1))
    p2 = txBox2.text_frame.paragraphs[0]
    p2.text = "OUR TEAM"
    p2.font.name = "Helvetica"
    p2.font.bold = True
    p2.font.size = Pt(60)
    p2.font.color.rgb = accent_color
    
    # Description
    txBox3 = slide0.shapes.add_textbox(Inches(1), Inches(3.8), Inches(5.5), Inches(3))
    p3 = txBox3.text_frame.paragraphs[0]
    p3.text = "A perfect blend of creativity and technical wizardry. The best people formula for great websites.\n\n我們擁有一群傑出的專業人才所組成的行銷管理團隊提供客戶服務規劃，我們也曾服務客戶的專案進行專案編輯，以跨部門之資源整合與協作，替客戶創造最大成效。"
    p3.font.name = "Calibri"
    p3.font.size = Pt(14)
    p3.line_spacing = 1.5

    # --- Generate Detail Slides ---
    detail_slides = []
    for i in range(len(team_data)):
        slide = prs.slides.add_slide(blank_layout)
        fill = slide.background.fill
        fill.gradient()
        fill.gradient_stops[0].color.rgb = RGBColor(242, 242, 242)
        fill.gradient_stops[1].color.rgb = RGBColor(220, 220, 220)
        detail_slides.append(slide)

    # --- Add Members to all slides ---
    # Define positions and sizes for normal and highlighted states
    card_h = Inches(7)
    card_w_norm = Inches(2.8)
    card_w_high = Inches(4.5)
    y_pos = Inches(1)
    
    norm_x_positions = [Inches(7.2), Inches(10.2), Inches(13.2)]
    
    high_positions = [
        [Inches(6.5), Inches(11.2), Inches(14)], # Member 1 highlighted
        [Inches(7.2), Inches(9.2), Inches(14)],  # Member 2 highlighted
        [Inches(7.2), Inches(10), Inches(12)]   # Member 3 highlighted
    ]

    for slide_idx, slide in enumerate(prs.slides):
        is_overview = (slide_idx == 0)

        # Add home icon to detail slides
        if not is_overview:
            home_icon = slide.shapes.add_textbox(Inches(1), Inches(7.5), Inches(1), Inches(1))
            home_p = home_icon.text_frame.paragraphs[0]
            home_p.text = "⌂" # Simple home character
            home_p.font.size = Pt(40)
            home_p.font.color.rgb = accent_color
            hlink = home_icon.click_action.hyperlink
            hlink.address = None
            hlink.target_slide = slide0
            
            # Add member details text
            member_idx = slide_idx - 1
            data = team_data[member_idx]
            
            role_box = slide.shapes.add_textbox(Inches(1), Inches(1.5), Inches(5), Inches(1.5))
            role_p = role_box.text_frame.paragraphs[0]
            role_p.text = data["role"].upper()
            role_p.font.name = "Helvetica Light"
            role_p.font.size = Pt(32)
            role_p.font.color.rgb = accent_color

            name_box = slide.shapes.add_textbox(Inches(1), Inches(2.8), Inches(5), Inches(1.5))
            name_p = name_box.text_frame.paragraphs[0]
            name_p.text = data["name"]
            # A common script font; user can change if needed
            name_p.font.name = "Brush Script MT" 
            name_p.font.size = Pt(60)
            
            desc_box = slide.shapes.add_textbox(Inches(1), Inches(4.5), Inches(5), Inches(3))
            desc_p = desc_box.text_frame.paragraphs[0]
            desc_p.text = data["desc"]
            desc_p.font.name = "Calibri"
            desc_p.font.size = Pt(14)
            desc_p.line_spacing = 1.5

        # Add all 3 member cards to the current slide
        for i in range(len(team_data)):
            data = team_data[i]
            is_highlighted = not is_overview and (slide_idx - 1 == i)
            
            width = card_w_high if is_highlighted else card_w_norm
            left = high_positions[slide_idx-1][i] if not is_overview else norm_x_positions[i]
            
            # Generate image (color or grayscale)
            img_stream = create_rounded_image(data['image_url'], (int(width*914400), int(card_h*914400)), 40, grayscale=not (is_overview or is_highlighted))
            pic = slide.shapes.add_picture(img_stream, left, y_pos, width, card_h)
            
            # Add hyperlink to detail slide
            hlink = pic.click_action.hyperlink
            hlink.address = None
            hlink.target_slide = detail_slides[i]

            # Add overlay
            overlay_h = Inches(1.8)
            overlay = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, y_pos + card_h - overlay_h, width, overlay_h)
            overlay.fill.solid()
            overlay.fill.fore_color.rgb = accent_color
            overlay.fill.transparency = 0.5
            overlay.line.fill.background()
            
            # Add role tag
            tag_box = slide.shapes.add_textbox(left, y_pos + card_h - overlay_h, width, overlay_h)
            tag_box.rotation = -90
            p_tag = tag_box.text_frame.paragraphs[0]
            p_tag.text = data['role_tag']
            p_tag.font.name = 'Helvetica'
            p_tag.font.bold = True
            p_tag.font.size = Pt(20)
            p_tag.font.color.rgb = RGBColor(255, 255, 255)

    # --- Apply Morph Transition to all slides using lxml ---
    for slide in prs.slides:
        set_morph_transition(slide, prs)

    prs.save(output_pptx_path)
    return output_pptx_path

# --- Example Usage ---
if __name__ == '__main__':
    team = [
        {
            "name": "Jennifer", "role": "Advertising\nCOPYWRITER", "role_tag": "Copywriter",
            "desc": "We are big believers that great work is created through great collaborations. Production and design talent are primed to help bring your vision to life.",
            "image_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=800"
        },
        {
            "name": "James", "role": "Graphic\nDESIGNER", "role_tag": "Designer",
            "desc": "We pride ourselves on both our internal ethics and those of our clients, focussing on industries that we feel can change the world for a better place.",
            "image_url": "https://images.unsplash.com/photo-1557862921-37829c790f19?w=800"
        },
        {
            "name": "Jessica", "role": "Marketing\nSPECIALIST", "role_tag": "Marketing",
            "desc": "Being independent allows us to make decisions that are unconstrained by profit or politics, calculated risks based on what we feel is right.",
            "image_url": "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=800"
        }
    ]
    
    output_file = "Interactive_Team_Showcase.pptx"
    create_team_showcase_slide(output_file, team)
    print(f"Presentation saved to {output_file}")

    # To run this, you would open the generated file in PowerPoint.
    # The morph transition and hyperlinks will be active.

