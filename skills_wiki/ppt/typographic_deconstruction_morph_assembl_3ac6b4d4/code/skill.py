def create_slide(
    output_pptx_path: str,
    title_text: str = "创新不止·未来可期",
    bg_palette: str = "technology",
    accent_color: tuple = (0, 220, 255),
    **kwargs,
) -> str:
    """
    Creates a PPTX reproducing the 'Typographic Deconstruction & Morph Assembly' effect.
    Generates two slides: Slide 1 (Scattered/Fragmented) and Slide 2 (Assembled).
    Applies the Morph transition between them.
    """
    import os
    import random
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw
    from lxml import etree

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Remove default slides
    for i in range(len(prs.slides) - 1, -1, -1):
        rId = prs.slides._sldIdLst[i].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[i]

    # Helper: Create a tech gradient background using PIL
    def create_gradient_bg(filename="tech_bg.png"):
        width, height = 1920, 1080
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        # Deep blue to darker blue radial-ish gradient
        center_x, center_y = width // 2, height // 2
        max_dist = (center_x**2 + center_y**2)**0.5
        for y in range(height):
            for x in range(width):
                dist = ((x - center_x)**2 + (y - center_y)**2)**0.5
                ratio = dist / max_dist
                r = int(11 * (1 - ratio) + 5 * ratio)
                g = int(35 * (1 - ratio) + 10 * ratio)
                b = int(80 * (1 - ratio) + 20 * ratio)
                draw.point((x, y), fill=(r, g, b))
        # Add some faint cyan grid lines
        for x in range(0, width, 100):
            draw.line([(x, 0), (x, height)], fill=(0, 220, 255, 30), width=1)
        for y in range(0, height, 100):
            draw.line([(0, y), (width, y)], fill=(0, 220, 255, 30), width=1)
        img.save(filename)
        return filename

    bg_path = create_gradient_bg()

    # --- Setup Data for Elements ---
    chars = list(title_text)
    num_particles = 15  # Geometric fragments acting as 'strokes'
    
    # Calculate final assembled positions (Slide 2)
    slide_w = prs.slide_width
    slide_h = prs.slide_height
    font_size_pt = 64
    char_spacing = Pt(font_size_pt * 1.2)
    total_width = len(chars) * char_spacing
    start_x = (slide_w - total_width) / 2
    final_y = (slide_h - char_spacing) / 2

    final_positions = []
    for i, char in enumerate(chars):
        final_positions.append({
            "name": f"!!char_{i}",
            "text": char,
            "x": start_x + (i * char_spacing),
            "y": final_y,
            "rot": 0,
            "font_size": font_size_pt
        })

    # Particle final positions (arranged neatly around the text)
    particle_finals = []
    for i in range(num_particles):
        x = start_x + (i * (total_width / num_particles))
        y = final_y + (char_spacing * 1.5) if i % 2 == 0 else final_y - (char_spacing * 0.5)
        w = Pt(random.randint(5, 30))
        h = Pt(random.randint(2, 6))
        particle_finals.append({
            "name": f"!!part_{i}",
            "x": x, "y": y, "w": w, "h": h, "rot": 0
        })

    # Calculate scattered positions (Slide 1)
    scattered_positions = []
    for char in final_positions:
        scattered_positions.append({
            "name": char["name"],
            "text": char["text"],
            "x": random.uniform(0, slide_w - char_spacing),
            "y": random.uniform(0, slide_h - char_spacing),
            "rot": random.uniform(-45, 45),
            "font_size": font_size_pt * random.uniform(0.5, 2.0)
        })

    particle_scattered = []
    for part in particle_finals:
        particle_scattered.append({
            "name": part["name"],
            "x": random.uniform(0, slide_w),
            "y": random.uniform(0, slide_h),
            "w": part["w"], "h": part["h"],
            "rot": random.uniform(0, 360)
        })

    # Helper: Build a slide given a set of positions
    def build_slide(char_data, part_data):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Add background
        pic = slide.shapes.add_picture(bg_path, 0, 0, slide_w, slide_h)
        # Send background to back via XML
        slide.shapes._spTree.remove(pic._element)
        slide.shapes._spTree.insert(2, pic._element)
        
        # Add Particles (Geometric fragments)
        for p in part_data:
            shape = slide.shapes.add_shape(
                1, p["x"], p["y"], p["w"], p["h"]  # 1 = Rectangle
            )
            shape.name = p["name"]
            shape.rotation = p["rot"]
            shape.fill.solid()
            shape.fill.fore_color.rgb = RGBColor(*accent_color)
            shape.line.fill.background()

        # Add Characters
        for c in char_data:
            tb = slide.shapes.add_textbox(c["x"], c["y"], char_spacing, char_spacing)
            tb.name = c["name"]
            tb.rotation = c["rot"]
            tf = tb.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            run = p.add_run()
            run.text = c["text"]
            run.font.size = Pt(c["font_size"])
            run.font.bold = True
            run.font.name = "Microsoft YaHei"
            run.font.color.rgb = RGBColor(255, 255, 255)
            
        return slide

    # Build Slide 1 (Scattered)
    slide1 = build_slide(scattered_positions, particle_scattered)

    # Build Slide 2 (Assembled)
    slide2 = build_slide(final_positions, particle_finals)

    # --- Inject Morph Transition to Slide 2 ---
    # This XML manipulation natively adds the Morph transition
    transition_xml = """
    <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="slow">
        <p:morph option="byObject"/>
    </p:transition>
    """
    morph_element = etree.fromstring(transition_xml)
    slide2._element.insert(-1, morph_element) # Insert right before the end of the slide XML

    prs.save(output_pptx_path)
    
    # Cleanup background image
    if os.path.exists(bg_path):
        os.remove(bg_path)
        
    return output_pptx_path
