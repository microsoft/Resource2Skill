import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from lxml import etree
from PIL import Image, ImageDraw

def _generate_placeholder_portraits(num_images: int = 5):
    """Generates placeholder portrait images locally using PIL."""
    colors = [
        (255, 99, 71),   # Tomato
        (60, 179, 113),  # Medium Sea Green
        (30, 144, 255),  # Dodger Blue
        (218, 165, 32),  # Goldenrod
        (138, 43, 226)   # Blue Violet
    ]
    img_paths = []
    for i in range(num_images):
        path = f"temp_team_member_{i}.jpg"
        img = Image.new('RGB', (400, 600), color=colors[i % len(colors)])
        draw = ImageDraw.Draw(img)
        # Draw a simplistic "person" vector
        draw.ellipse((100, 120, 300, 320), fill=(255, 255, 255, 120)) # Head
        draw.polygon([(50, 600), (200, 350), (350, 600)], fill=(255, 255, 255, 120)) # Shoulders
        img.save(path)
        img_paths.append(path)
    return img_paths

def _insert_rounded_picture(slide, img_path, shape_name, cx, cy, w, h):
    """
    Inserts a picture into a rounded rectangle shape using lxml injection.
    """
    left = Inches(cx - w/2)
    top = Inches(cy - h/2)
    width = Inches(w)
    height = Inches(h)

    # 1. Add dummy pic to load the image and get its relationship ID
    dummy = slide.shapes.add_picture(img_path, 0, 0, Inches(0.1), Inches(0.1))
    rel_id = dummy._element.blipFill.blip.embed
    dummy_element = dummy._element
    dummy_element.getparent().remove(dummy_element) # Delete dummy

    # 2. Add rounded rectangle
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.name = shape_name # MUST be identical across slides for Morph to work!
    
    # 3. Inject blipFill (Picture Fill) and remove solid background & outline
    spPr = shape._element.spPr
    
    # Remove existing solid fill
    solidFill = spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}solidFill")
    if solidFill is not None:
        spPr.remove(solidFill)

    # Create blipFill
    blipFill = etree.SubElement(spPr, "{http://schemas.openxmlformats.org/drawingml/2006/main}blipFill")
    blip = etree.SubElement(blipFill, "{http://schemas.openxmlformats.org/drawingml/2006/main}blip")
    blip.set("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed", rel_id)
    stretch = etree.SubElement(blipFill, "{http://schemas.openxmlformats.org/drawingml/2006/main}stretch")
    etree.SubElement(stretch, "{http://schemas.openxmlformats.org/drawingml/2006/main}fillRect")

    # Remove Outline
    ln = spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}ln")
    if ln is not None:
        spPr.remove(ln)
    ln = etree.SubElement(spPr, "{http://schemas.openxmlformats.org/drawingml/2006/main}ln")
    etree.SubElement(ln, "{http://schemas.openxmlformats.org/drawingml/2006/main}noFill")

    return shape

def create_slide(
    output_pptx_path: str,
    title_text: str = "ANIMATED TEAM INTRODUCTION TEMPLATE",
    body_text: str = "",
    bg_palette: str = "dark",
    accent_color: tuple = (0, 191, 255), 
    **kwargs,
) -> str:
    """
    Creates a presentation demonstrating the Dynamic Carousel Morphing effect.
    Builds 2 slides to showcase the progression.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Generate assets
    num_members = 5
    img_paths = _generate_placeholder_portraits(num_members)
    
    # Pre-calculate slot geometries (Relative index: (X_center, Y_center, Width, Height))
    gap = 0.3
    cy = 4.0
    w_large, h_large = 3.5, 4.5
    w_small, h_small = 1.8, 2.4
    x_center = 13.333 / 2
    
    slots = {
        0: (x_center, cy, w_large, h_large), # Active center
        -1: (x_center - (w_large/2) - gap - (w_small/2), cy, w_small, h_small),
        -2: (x_center - (w_large/2) - gap - w_small - gap - (w_small/2), cy, w_small, h_small),
        -3: (x_center - (w_large/2) - gap - w_small*2 - gap*2 - (w_small/2), cy, w_small, h_small), # Offscreen Left
        1: (x_center + (w_large/2) + gap + (w_small/2), cy, w_small, h_small),
        2: (x_center + (w_large/2) + gap + w_small + gap + (w_small/2), cy, w_small, h_small),
        3: (x_center + (w_large/2) + gap + w_small*2 + gap*2 + (w_small/2), cy, w_small, h_small), # Offscreen Right
    }

    # Build 2 consecutive slides focusing on Member 2, then Member 3
    active_indices = [2, 3]

    for slide_idx, active_idx in enumerate(active_indices):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # 1. Background
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(50, 50, 50)
        
        # 2. Static Title
        title_box = slide.shapes.add_textbox(Inches(0), Inches(0.5), Inches(13.333), Inches(1.0))
        tf = title_box.text_frame
        tf.text = title_text
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        tf.paragraphs[0].font.size = Pt(28)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = RGBColor(220, 220, 220)
        
        # 3. Carousel Images (Ensure we insert in exact loop order to match z-index for Morph)
        for i in range(num_members):
            slot_pos = i - active_idx
            
            # If out of defined slots, clamp to offscreen
            if slot_pos < -3: slot_pos = -3
            if slot_pos > 3: slot_pos = 3
                
            cx, cy_pos, w, h = slots[slot_pos]
            shape_name = f"TeamMember_Card_{i}"
            
            _insert_rounded_picture(slide, img_paths[i], shape_name, cx, cy_pos, w, h)
            
            # Active Member specific styling (Name Tag)
            if slot_pos == 0:
                tag_w, tag_h = 2.8, 0.6
                tag_left = Inches(cx - tag_w/2)
                tag_top = Inches(cy_pos + h/2 - 0.2)
                
                tag = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, tag_left, tag_top, Inches(tag_w), Inches(tag_h))
                tag.name = "Active_Name_Tag"
                tag.fill.solid()
                tag.fill.fore_color.rgb = RGBColor(*accent_color)
                tag.line.color.rgb = RGBColor(*accent_color)
                
                tag_tf = tag.text_frame
                tag_tf.text = f"MEMBER 0{i+1}"
                tag_tf.paragraphs[0].alignment = PP_ALIGN.CENTER
                tag_tf.paragraphs[0].font.size = Pt(16)
                tag_tf.paragraphs[0].font.bold = True
                tag_tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

        # Inject Morph Transition XML for Slide 2
        if slide_idx > 0:
            p_ns = "http://schemas.openxmlformats.org/presentationml/2006/main"
            try:
                transition = etree.Element(f"{{{p_ns}}}transition", spd="med")
                # PPT 2019+ morphological transition namespace
                morph = etree.SubElement(transition, "{http://schemas.microsoft.com/office/powerpoint/2018/8/main}morph", option="byObject")
                
                # Insert transition securely inside <p:sld>
                cSld = slide._element.find(f"{{{p_ns}}}cSld")
                insert_idx = slide._element.index(cSld) + 1
                slide._element.insert(insert_idx, transition)
            except Exception:
                pass # Graceful fallback; user can manually select Transitions -> Morph

    prs.save(output_pptx_path)
    
    # Cleanup dummy images
    for p in img_paths:
        if os.path.exists(p):
            os.remove(p)

    return output_pptx_path
