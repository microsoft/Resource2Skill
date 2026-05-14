def create_slide(
    output_pptx_path: str,
    title_text: str = "EVENT",
    sections: list = ["JUNE", "ELECTRICAL CARS", "LUNCH", "HIKING", "DIVING", "GEAR"],
    wheel_diameter_inches: float = 6.0,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Interactive Morphing Image Wheel effect.
    """
    import os
    import io
    import urllib.request
    import math
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from pptx.oxml import parse_xml
    from PIL import Image, ImageDraw, ImageOps

    # --- Helper: Apply Morph Transition via lxml ---
    def apply_morph_transition(slide):
        transition_xml = (
            '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
            'xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" '
            'spd="slow">'
            '<p14:morph val="byObject"/>'
            '</p:transition>'
        )
        transition = parse_xml(transition_xml)
        slide._element.append(transition)

    # --- Helper: Generate Image Slice ---
    def generate_pie_slice_image(image_url, start_angle, end_angle, fallback_color, size=800):
        try:
            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as url_response:
                img = Image.open(io.BytesIO(url_response.read())).convert("RGBA")
        except Exception:
            # Fallback to solid color if download fails
            img = Image.new("RGBA", (size, size), fallback_color)

        # Fit image to square
        img = ImageOps.fit(img, (size, size), method=Image.Resampling.LANCZOS)
        
        # Create anti-aliased mask (4x resolution)
        mask_size = size * 4
        mask = Image.new("L", (mask_size, mask_size), 0)
        draw = ImageDraw.Draw(mask)
        # PIL angles start from +x axis, moving clockwise
        draw.pieslice([0, 0, mask_size, mask_size], start_angle, end_angle, fill=255)
        mask = mask.resize((size, size), Image.Resampling.LANCZOS)
        
        # Apply mask
        img.putalpha(mask)
        
        # Save to buffer
        img_io = io.BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        return img_io

    # Configuration
    num_slices = len(sections)
    angle_per_slice = 360 / num_slices
    
    # Placeholder images (Unsplash Source) & Fallback colors
    image_themes = ["abstract", "technology", "food", "nature", "ocean", "texture"]
    fallback_colors = [
        (255, 99, 71, 255), (54, 162, 235, 255), (255, 206, 86, 255),
        (75, 192, 192, 255), (153, 102, 255, 255), (255, 159, 64, 255)
    ]

    print("Generating transparent pie slices (this may take a few seconds)...")
    slice_buffers = []
    for i in range(num_slices):
        start_a = i * angle_per_slice
        end_a = (i + 1) * angle_per_slice
        url = f"https://source.unsplash.com/random/800x800/?{image_themes[i%len(image_themes)]}"
        img_io = generate_pie_slice_image(url, start_a, end_a, fallback_colors[i%len(fallback_colors)])
        slice_buffers.append(img_io)

    # Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Calculate positions
    # Slide 1: Center
    center_x = (prs.slide_width.inches - wheel_diameter_inches) / 2
    center_y = (prs.slide_height.inches - wheel_diameter_inches) / 2
    
    # Slide 2: Shifted Left
    left_x = -1.0  # Partially off-screen
    left_y = center_y

    # ==========================================
    # SLIDE 1: The Central Hub Overview
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    
    # Insert slices
    for i in range(num_slices):
        slice_buffers[i].seek(0)
        pic = slide1.shapes.add_picture(
            slice_buffers[i], 
            Inches(center_x), Inches(center_y), 
            Inches(wheel_diameter_inches), Inches(wheel_diameter_inches)
        )
        pic.name = f"WheelSlice_{i}" # Crucial for Morph

    # Insert Center White Hub
    hub_diameter = wheel_diameter_inches * 0.45
    hub_offset = (wheel_diameter_inches - hub_diameter) / 2
    hub1 = slide1.shapes.add_shape(
        1, # msoShapeOval
        Inches(center_x + hub_offset), Inches(center_y + hub_offset),
        Inches(hub_diameter), Inches(hub_diameter)
    )
    hub1.name = "CenterHub"
    hub1.fill.solid()
    hub1.fill.fore_color.rgb = RGBColor(255, 255, 255)
    hub1.line.fill.background() # No line
    
    # Add text to hub
    text_frame = hub1.text_frame
    text_frame.text = title_text
    text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    font = text_frame.paragraphs[0].runs[0].font
    font.name = 'Arial Black'
    font.size = Pt(32)
    font.color.rgb = RGBColor(0, 0, 0)

    # ==========================================
    # SLIDE 2: Shifted and Rotated Reveal
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    apply_morph_transition(slide2) # Inject Morph transition

    # Insert and rotate slices
    rotation_angle = angle_per_slice # Rotate wheel by 1 step
    
    for i in range(num_slices):
        slice_buffers[i].seek(0)
        pic = slide2.shapes.add_picture(
            slice_buffers[i], 
            Inches(left_x), Inches(left_y), 
            Inches(wheel_diameter_inches), Inches(wheel_diameter_inches)
        )
        pic.name = f"WheelSlice_{i}" # Match names for Morph
        pic.rotation = rotation_angle # Spin the wheel

    # Insert Center White Hub (Shifted)
    hub2 = slide2.shapes.add_shape(
        1, # msoShapeOval
        Inches(left_x + hub_offset), Inches(left_y + hub_offset),
        Inches(hub_diameter), Inches(hub_diameter)
    )
    hub2.name = "CenterHub"
    hub2.fill.solid()
    hub2.fill.fore_color.rgb = RGBColor(255, 255, 255)
    hub2.line.fill.background()
    
    text_frame = hub2.text_frame
    text_frame.text = sections[0] # Updated text
    text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    font = text_frame.paragraphs[0].runs[0].font
    font.name = 'Arial Black'
    font.size = Pt(28)
    font.color.rgb = RGBColor(0, 0, 0)

    # Add Reveal Content to the right
    content_x = Inches(left_x + wheel_diameter_inches + 0.5)
    content_y = Inches(2.0)
    
    title_box = slide2.shapes.add_textbox(content_x, content_y, Inches(6.0), Inches(1.0))
    title_frame = title_box.text_frame
    title_p = title_frame.paragraphs[0]
    title_p.text = sections[1] # E.g., "ELECTRICAL CARS"
    title_p.font.name = 'Arial Black'
    title_p.font.size = Pt(44)
    title_p.font.color.rgb = RGBColor(0, 0, 0)

    # Decorative Line
    line = slide2.shapes.add_connector(
        1, # msoConnectorStraight
        content_x, content_y + Inches(0.8),
        Inches(12.5), content_y + Inches(0.8)
    )
    line.line.color.rgb = RGBColor(0, 0, 0)
    line.line.width = Pt(3)

    body_box = slide2.shapes.add_textbox(content_x, content_y + Inches(1.0), Inches(6.0), Inches(2.0))
    body_frame = body_box.text_frame
    body_frame.word_wrap = True
    body_p = body_frame.paragraphs[0]
    body_p.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas porttitor congue massa. Fusce posuere, magna sed pulvinar ultricies, purus lectus malesuada libero, sit amet commodo magna eros quis urna."
    body_p.font.name = 'Calibri'
    body_p.font.size = Pt(14)
    body_p.font.color.rgb = RGBColor(80, 80, 80)

    # Save presentation
    prs.save(output_pptx_path)
    print(f"Presentation saved to {output_pptx_path}. Note: View in Slide Show mode to see the Morph transition.")
    return output_pptx_path
