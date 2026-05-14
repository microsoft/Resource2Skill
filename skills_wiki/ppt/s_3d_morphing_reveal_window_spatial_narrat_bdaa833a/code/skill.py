def create_slide(
    output_pptx_path: str,
    title_text: str = "A New Perspective",
    body_text: str = "",
    bg_palette: str = "cityscape",
    accent_color: tuple = (160, 82, 45), 
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 3D Morphing Reveal Window effect.
    """
    from pptx import Presentation
    from pptx.util import Inches
    from pptx.dml.color import RGBColor
    from pptx.oxml import parse_xml
    from PIL import Image, ImageDraw
    import urllib.request
    import os

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # --- HELPER 1: Generate Window Pane Image via PIL ---
    pane_path = "temp_window_pane.png"
    pane_width, pane_height = 400, 800
    img = Image.new("RGBA", (pane_width, pane_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    wood_color = accent_color + (255,) # e.g., (160, 82, 45, 255)
    glass_color = (220, 240, 220, 140) # Semi-transparent green-ish glass
    frame_thick = 30
    
    # Draw Glass
    draw.rectangle([frame_thick, frame_thick, pane_width-frame_thick, pane_height-frame_thick], fill=glass_color)
    # Draw Outer Frame
    draw.rectangle([0, 0, pane_width, pane_height], outline=wood_color, width=frame_thick)
    # Draw Crossbars
    draw.rectangle([0, pane_height//2 - 15, pane_width, pane_height//2 + 15], fill=wood_color)
    draw.rectangle([pane_width//2 - 15, 0, pane_width//2 + 15, pane_height], fill=wood_color)
    img.save(pane_path)

    # --- HELPER 2: Download Reveal Image ---
    bg_img_path = "temp_reveal_bg.jpg"
    try:
        url = f"https://source.unsplash.com/featured/1600x900/?{bg_palette}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(bg_img_path, 'wb') as out_file:
            out_file.write(response.read())
    except Exception:
        # Fallback if download fails: generate a gradient image
        bg_img = Image.new("RGB", (1600, 900), (20, 30, 60))
        bg_draw = ImageDraw.Draw(bg_img)
        for i in range(900):
            bg_draw.line([(0, i), (1600, i)], fill=(20 + int(i*0.1), 30 + int(i*0.15), 60 + int(i*0.2)))
        bg_img.save(bg_img_path)

    # --- HELPER 3: Inject 3D Rotation ---
    def apply_3d_rotation(shape, rot_y_deg):
        # rot_y_deg: positive swings right side back, negative swings left side back
        lon_val = int(rot_y_deg * 60000) # OpenXML uses 1/60000th of a degree
        xml = f"""
        <a:scene3d xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:camera prst="orthographicFront">
                <a:rot lat="0" lon="{lon_val}" rev="0"/>
            </a:camera>
            <a:lightRig rig="threePt" dir="t"/>
        </a:scene3d>
        """
        scene3d = parse_xml(xml)
        shape._element.spPr.append(scene3d)

    # --- SLIDE 1: CLOSED WINDOW ---
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])
    # Set wall background color (Light Blue)
    bg1 = slide1.background
    fill1 = bg1.fill
    fill1.solid()
    fill1.fore_color.rgb = RGBColor(173, 216, 230)

    # Positioning for closed state
    center_x = 13.333 / 2
    center_y = 7.5 / 2
    w_w, w_h = 3.0, 5.0
    
    left_pane_closed_x = Inches(center_x - w_w)
    right_pane_closed_x = Inches(center_x)
    pane_y = Inches(center_y - (w_h / 2))

    # Add panes
    s1_left = slide1.shapes.add_picture(pane_path, left_pane_closed_x, pane_y, width=Inches(w_w), height=Inches(w_h))
    s1_left.name = "MorphWindowLeft"
    s1_right = slide1.shapes.add_picture(pane_path, right_pane_closed_x, pane_y, width=Inches(w_w), height=Inches(w_h))
    s1_right.name = "MorphWindowRight"

    # Add Title text
    title_box1 = slide1.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.33), Inches(1))
    tf1 = title_box1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = title_text
    p1.font.bold = True
    p1.font.size = Pt(40)
    p1.font.color.rgb = RGBColor(50, 50, 50)
    p1.alignment = 2 # Center

    # --- SLIDE 2: OPEN WINDOW (REVEAL) ---
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    # Same wall background
    bg2 = slide2.background
    fill2 = bg2.fill
    fill2.solid()
    fill2.fore_color.rgb = RGBColor(173, 216, 230)

    # Insert Reveal Background Image
    pic_w, pic_h = 10.0, 5.625
    pic_x = Inches(center_x - (pic_w/2))
    pic_y = Inches(center_y - (pic_h/2) + 0.3)
    slide2.shapes.add_picture(bg_img_path, pic_x, pic_y, width=Inches(pic_w), height=Inches(pic_h))

    # Positioning for open state
    # Shift outward and apply 3D rotation to simulate hinge
    left_pane_open_x = Inches(center_x - w_w - 1.2)
    right_pane_open_x = Inches(center_x + 1.2)

    s2_left = slide2.shapes.add_picture(pane_path, left_pane_open_x, pane_y, width=Inches(w_w), height=Inches(w_h))
    s2_left.name = "MorphWindowLeft"  # MUST match Slide 1 for Morph
    apply_3d_rotation(s2_left, -70)   # Swing left door outward

    s2_right = slide2.shapes.add_picture(pane_path, right_pane_open_x, pane_y, width=Inches(w_w), height=Inches(w_h))
    s2_right.name = "MorphWindowRight" # MUST match Slide 1 for Morph
    apply_3d_rotation(s2_right, 70)    # Swing right door outward

    # Add Title text (to maintain continuity)
    title_box2 = slide2.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.33), Inches(1))
    tf2 = title_box2.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = title_text
    p2.font.bold = True
    p2.font.size = Pt(40)
    p2.font.color.rgb = RGBColor(50, 50, 50)
    p2.alignment = 2

    # --- INJECT MORPH TRANSITION ON SLIDE 2 ---
    morph_xml = """
    <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="slow">
        <p:morph option="byObject"/>
    </p:transition>
    """
    transition_el = parse_xml(morph_xml)
    slide2._element.append(transition_el)

    # Save and clean up
    prs.save(output_pptx_path)
    if os.path.exists(pane_path):
        os.remove(pane_path)
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)

    return output_pptx_path
