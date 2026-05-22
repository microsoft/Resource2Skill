import os
import tempfile
from lxml import etree
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches

def _generate_diorama_assets(temp_dir: str):
    """
    Generates flat, vector-style transparent PNG assets simulating 
    the Pixton / Freepik illustrations seen in the video.
    """
    # 1. Generate Subway Background
    bg_path = os.path.join(temp_dir, "bg.png")
    bg = Image.new("RGBA", (1280, 720), (210, 215, 220, 255))
    draw = ImageDraw.Draw(bg)
    # Wall tiles / wainscoting
    draw.rectangle([0, 360, 1280, 720], fill=(180, 185, 190, 255))
    # Train tracks / tunnel void
    draw.rectangle([0, 150, 1280, 360], fill=(40, 45, 55, 255))
    # Subway train car
    draw.rounded_rectangle([100, 100, 1180, 450], radius=20, fill=(230, 230, 235, 255))
    # Train stripe
    draw.rectangle([100, 380, 1180, 410], fill=(0, 102, 204, 255))
    # Train windows
    for x in range(150, 1100, 200):
        draw.rectangle([x, 200, x+120, 320], fill=(20, 25, 30, 255))
    bg.save(bg_path)

    # 2. Generate Food Stand (Transparent)
    stand_path = os.path.join(temp_dir, "stand.png")
    stand = Image.new("RGBA", (600, 600), (0, 0, 0, 0))
    draw = ImageDraw.Draw(stand)
    # Poles
    draw.rectangle([60, 200, 90, 600], fill=(140, 140, 150, 255))
    draw.rectangle([510, 200, 540, 600], fill=(140, 140, 150, 255))
    # Counter/Base
    draw.rectangle([30, 400, 570, 600], fill=(193, 154, 107, 255))
    draw.rectangle([40, 420, 560, 580], fill=(160, 110, 70, 255))
    # Awning (Red & White stripes)
    draw.rectangle([20, 100, 580, 220], fill=(255, 255, 255, 255))
    for i in range(20, 580, 80):
        draw.rectangle([i, 100, i+40, 220], fill=(220, 50, 50, 255))
    # Scalloped edge
    for i in range(20, 580, 40):
        fill_color = (220, 50, 50, 255) if (i - 20) % 80 == 0 else (255, 255, 255, 255)
        draw.pieslice([i, 200, i+40, 240], 0, 180, fill=fill_color)
    stand.save(stand_path)

    # 3. Generate Characters
    char_paths = []
    colors = [(0, 150, 136, 255), (255, 152, 0, 255)] # Teal shirt, Orange shirt
    for idx, color in enumerate(colors):
        char_path = os.path.join(temp_dir, f"char_{idx}.png")
        char = Image.new("RGBA", (200, 500), (0, 0, 0, 0))
        draw = ImageDraw.Draw(char)
        # Head (Peach skin)
        draw.ellipse([60, 20, 140, 100], fill=(255, 218, 185, 255))
        # Torso
        draw.rounded_rectangle([40, 110, 160, 320], radius=25, fill=color)
        # Legs (Dark pants)
        draw.rectangle([60, 320, 90, 500], fill=(40, 40, 50, 255))
        draw.rectangle([110, 320, 140, 500], fill=(40, 40, 50, 255))
        # Arm
        draw.rounded_rectangle([30, 120, 55, 260], radius=10, fill=(255, 218, 185, 255))
        char.save(char_path)
        char_paths.append(char_path)

    return bg_path, stand_path, char_paths

def _apply_morph_transition(slide):
    """
    Injects OpenXML to apply the Morph transition to a slide.
    """
    p_ns = "http://schemas.openxmlformats.org/presentationml/2006/main"
    # Find insertion point (after cSld or clrMapOvr)
    cSld = slide.element.find(f'{{{p_ns}}}cSld')
    clrMapOvr = slide.element.find(f'{{{p_ns}}}clrMapOvr')
    insert_idx = slide.element.index(clrMapOvr) + 1 if clrMapOvr is not None else slide.element.index(cSld) + 1
    
    # Create transition XML
    transition = etree.Element(f'{{{p_ns}}}transition')
    transition.set('spd', 'slow')
    etree.SubElement(transition, f'{{{p_ns}}}morph')
    
    # Inject
    slide.element.insert(insert_idx, transition)

def create_slide(output_pptx_path: str, **kwargs) -> str:
    """
    Create a PPTX file reproducing the Animated Comic Diorama effect.
    Generates a 2-slide sequence that utilizes the Morph transition to
    bring flat-illustrated characters into a built scene.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    with tempfile.TemporaryDirectory() as tmpdir:
        bg_img, stand_img, char_imgs = _generate_diorama_assets(tmpdir)

        # ==========================================
        # SLIDE 1: Setup Scene (Characters Off-Screen)
        # ==========================================
        slide1 = prs.slides.add_slide(blank_layout)
        
        # Layer 0: Background
        slide1.shapes.add_picture(bg_img, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))
        
        # Layer 1: Prop (Food Stand centered)
        stand_w = Inches(6)
        stand_left = (prs.slide_width - stand_w) / 2
        slide1.shapes.add_picture(stand_img, stand_left, Inches(2), width=stand_w)
        
        # Layer 2: Characters (Off-screen left and right)
        char_w = Inches(2)
        # Identical variable assignment used to force python-pptx to maintain sequence 
        # so Morph matching registers the identical shapes across slides.
        c1 = slide1.shapes.add_picture(char_imgs[0], -Inches(2.5), Inches(2.5), width=char_w)
        c2 = slide1.shapes.add_picture(char_imgs[1], Inches(14), Inches(2.5), width=char_w)
        # Optional: Set shape names to ensure Morph matching
        c1.name = "!!Char1"
        c2.name = "!!Char2"

        # ==========================================
        # SLIDE 2: Resolve Scene (Characters On-Screen)
        # ==========================================
        slide2 = prs.slides.add_slide(blank_layout)
        
        # Re-add Background and Stand exactly as before
        slide2.shapes.add_picture(bg_img, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))
        slide2.shapes.add_picture(stand_img, stand_left, Inches(2), width=stand_w)
        
        # Move Characters on-screen to trigger the Morph "Walk-in"
        c1_s2 = slide2.shapes.add_picture(char_imgs[0], Inches(2), Inches(2.5), width=char_w)
        c2_s2 = slide2.shapes.add_picture(char_imgs[1], Inches(9.5), Inches(2.5), width=char_w)
        c1_s2.name = "!!Char1"
        c2_s2.name = "!!Char2"

        # Inject Morph Transition
        _apply_morph_transition(slide2)

    prs.save(output_pptx_path)
    return output_pptx_path
