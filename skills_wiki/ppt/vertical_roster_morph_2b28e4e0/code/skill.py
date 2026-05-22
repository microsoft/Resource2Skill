import os
import urllib.request
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from PIL import Image, ImageDraw

def _add_morph_transition(slide, duration_ms="1000"):
    """Injects the Morph transition XML into a slide part."""
    slide_part = slide.part
    # The transition is a child of the cSld element
    csld = slide_part.get_or_add_slideLayout().getparent()

    # Check if a transition element already exists and remove it to ensure a clean slate
    transition_node = csld.find(qn("p:transition"))
    if transition_node is not None:
        csld.remove(transition_node)

    # Create the transition element <p:transition>
    transition_xml = f"""
    <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med" advClick="true" dur="{duration_ms}">
        <p:morph option="byObject"/>
    </p:transition>
    """
    transition_element = etree.fromstring(transition_xml)
    csld.append(transition_element)

def _create_placeholder_image(size=(400, 400), color=(128, 128, 128), text="IMG"):
    """Creates a placeholder image with PIL if a real image fails to download."""
    img = Image.new('RGB', size, color=color)
    d = ImageDraw.Draw(img)
    try:
        from pptx.util import Inches
        font_size = int(size[1] / 4)
        # A common system font, no need for file path
        font = ImageFont.load_default(size=font_size)
        text_bbox = d.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (size[0] - text_width) / 2
        text_y = (size[1] - text_height) / 2
        d.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
    except ImportError:
        pass # Pillow not installed, just return grey box
    
    path = f"placeholder_{color}.png"
    img.save(path)
    return path

def create_slide(
    output_pptx_path: str,
    team_members: list = None,
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the 'Vertical Roster Morph' visual effect.

    The animation is achieved by creating a sequence of slides and applying the
    Morph transition, which animates the movement of objects between their
    positions on consecutive slides.

    Returns:
        str: The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    blank_slide_layout = prs.slide_layouts[6]

    # --- Default Data & Styling ---
    if team_members is None:
        team_members = [
            {"name": "ADRIANNA", "surname": "VANCE", "designation": "DESIGNATION1", "bio": "Some text goes here. Some text goes here. Some text goes here. Some text goes here. 1", "image_url": "https://source.unsplash.com/400x400/?portrait,woman"},
            {"name": "MARCUS", "surname": "REID", "designation": "DESIGNATION2", "bio": "Some text goes here. Some text goes here. Some text goes here. Some text goes here. 2", "image_url": "https://source.unsplash.com/400x400/?portrait,man"},
            {"name": "ELARA", "surname": "FINCH", "designation": "DESIGNATION3", "bio": "Some text goes here. Some text goes here. Some text goes here. Some text goes here. 3", "image_url": "https://source.unsplash.com/400x400/?portrait,person"},
            {"name": "SOFIA", "surname": "CHEN", "designation": "DESIGNATION4", "bio": "Some text goes here. Some text goes here. Some text goes here. Some text goes here. 4", "image_url": "https://source.unsplash.com/400x400/?portrait,female"},
            {"name": "LEO", "surname": "SANTIAGO", "designation": "DESIGNATION5", "bio": "Some text goes here. Some text goes here. Some text goes here. Some text goes here. 5", "image_url": "https://source.unsplash.com/400x400/?portrait,male"},
            {"name": "JASPER", "surname": "KNIGHT", "designation": "DESIGNATION6", "bio": "Some text goes here. Some text goes here. Some text goes here. Some text goes here. 6", "image_url": "https://source.unsplash.com/400x400/?portrait,beard"},
        ]

    local_image_paths = []
    for i, member in enumerate(team_members):
        path = f"temp_image_{i}.jpg"
        try:
            urllib.request.urlretrieve(member["image_url"], path)
            local_image_paths.append(path)
        except Exception:
            print(f"Warning: Could not download image for {member['name']}. Using placeholder.")
            placeholder_path = _create_placeholder_image(color=(50 + i*20, 50 + i*20, 50 + i*20))
            local_image_paths.append(placeholder_path)

    # --- Slide Creation Loop ---
    for i in range(len(team_members)):
        slide = prs.slides.add_slide(blank_slide_layout)
        
        # --- Common Colors & Fonts ---
        TEXT_COLOR = RGBColor(89, 89, 89)
        TITLE_COLOR = RGBColor(0, 0, 0)
        HIGHLIGHT_COLOR = RGBColor(12, 126, 132)
        HIGHLIGHT_TEXT_COLOR = RGBColor(255, 255, 255)
        
        # --- 1. Right Column: Image Strip ---
        IMAGE_WIDTH = Inches(4.5)
        image_strip_left = prs.slide_width - IMAGE_WIDTH
        slide_center_y = prs.slide_height / 2
        
        # Calculate the top position of the entire strip to center the i-th image
        first_image_top = (slide_center_y - (IMAGE_WIDTH / 2)) - (i * IMAGE_WIDTH)

        for j, img_path in enumerate(local_image_paths):
            top_pos = first_image_top + (j * IMAGE_WIDTH)
            slide.shapes.add_picture(img_path, image_strip_left, top_pos, width=IMAGE_WIDTH, height=IMAGE_WIDTH)

        # --- 2. Center Column: Name and Bio ---
        name_box = slide.shapes.add_textbox(Inches(5), Inches(2.5), Inches(6), Inches(1))
        name_box.text_frame.text = f"{team_members[i]['name']}\n{team_members[i]['surname']}"
        p = name_box.text_frame.paragraphs[0]
        p.font.name = "Arial Black"
        p.font.size = Pt(44)
        p.font.color.rgb = TITLE_COLOR
        
        bio_box = slide.shapes.add_textbox(Inches(5), Inches(4), Inches(5), Inches(2))
        bio_box.text_frame.text = team_members[i]['bio']
        p_bio = bio_box.text_frame.paragraphs[0]
        p_bio.font.name = "Arial"
        p_bio.font.size = Pt(14)
        p_bio.font.color.rgb = TEXT_COLOR

        # --- 3. Left Column: Designations & Highlight ---
        designation_start_top = Inches(1.5)
        designation_spacing = Inches(0.8)
        
        # Add the highlight bar
        highlight_bar = slide.shapes.add_shape(1, Inches(1), designation_start_top + (i * designation_spacing) - Inches(0.1), Inches(3.5), Inches(0.6))
        highlight_bar.fill.solid()
        highlight_bar.fill.fore_color.rgb = HIGHLIGHT_COLOR
        highlight_bar.line.fill.background()
        highlight_bar.shadow.inherit = False
        # Make the rounded rectangle fully rounded
        adj = highlight_bar.adjustments
        adj[0] = 0.5 # Corresponds to the roundness handle
        
        # Add all designation labels
        for k, member in enumerate(team_members):
            des_box = slide.shapes.add_textbox(Inches(1.2), designation_start_top + (k * designation_spacing), Inches(3), Inches(0.5))
            des_box.text_frame.text = member['designation']
            p_des = des_box.text_frame.paragraphs[0]
            p_des.font.name = "Arial"
            p_des.font.bold = True
            p_des.font.size = Pt(18)
            
            if k == i: # Highlighted text
                p_des.font.color.rgb = HIGHLIGHT_TEXT_COLOR
            else:
                p_des.font.color.rgb = TEXT_COLOR

        # --- 4. Apply Morph Transition to all but the first slide ---
        if i > 0:
            _add_morph_transition(slide, duration_ms="1250")

    # --- Clean up downloaded images ---
    for path in local_image_paths:
        if os.path.exists(path):
            os.remove(path)
            
    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# if __name__ == '__main__':
#     create_slide("team_roster_morph.pptx")
