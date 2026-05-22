def create_slide(
    output_pptx_path: str,
    title_text: str = "Our Team",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas porttitor congue massa. Fusce posuere, magna sed pulvinar ultricies, purus lectus malesuada libero, sit amet commodo magna eros quis urna.",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Instagram-Style Interactive Team Roster visual effect.
    """
    import io
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw
    from lxml import etree

    # === Helper Functions ===

    def get_image(url: str, fallback_color: tuple) -> bytes:
        """Download image or provide a fallback color square."""
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.read()
        except Exception:
            img = Image.new('RGB', (400, 400), fallback_color)
            out = io.BytesIO()
            img.save(out, format='PNG')
            return out.getvalue()

    def create_circle_image(img_bytes: bytes, size: int = 400) -> io.BytesIO:
        """Crop an image to a transparent anti-aliased circle using PIL."""
        img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim) / 2
        top = (h - min_dim) / 2
        img = img.crop((left, top, left + min_dim, top + min_dim))
        
        # Create high-res mask for anti-aliasing
        mask = Image.new("L", (min_dim * 3, min_dim * 3), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, min_dim * 3, min_dim * 3), fill=255)
        mask = mask.resize((min_dim, min_dim), Image.LANCZOS)
        
        img.putalpha(mask)
        img = img.resize((size, size), Image.LANCZOS)
        
        out = io.BytesIO()
        img.save(out, format="PNG")
        out.seek(0)
        return out

    def add_gradient_fill(shape, colors: list):
        """Inject an angled linear gradient fill to a shape via lxml."""
        spPr = shape.element.spPr
        # Remove existing fills
        for child in spPr.xpath('./a:solidFill | ./a:noFill | ./a:blipFill | ./a:gradFill', namespaces=spPr.nsmap):
            spPr.remove(child)
            
        ns_a = "http://schemas.openxmlformats.org/drawingml/2006/main"
        gradFill = etree.SubElement(spPr, f'{{{ns_a}}}gradFill')
        gradFill.set('rotWithShape', '1')
        gsLst = etree.SubElement(gradFill, f'{{{ns_a}}}gsLst')
        
        for i, clr in enumerate(colors):
            pos = str(int((i / (len(colors) - 1)) * 100000))
            gs = etree.SubElement(gsLst, f'{{{ns_a}}}gs')
            gs.set('pos', pos)
            srgbClr = etree.SubElement(gs, f'{{{ns_a}}}srgbClr')
            srgbClr.set('val', clr)
            
        lin = etree.SubElement(gradFill, f'{{{ns_a}}}lin')
        lin.set('ang', '3300000')  # Angle for the gradient
        lin.set('scaled', '1')

    def add_shadow(shape):
        """Inject a soft drop shadow to a shape via lxml."""
        spPr = shape.element.spPr
        ns_a = "http://schemas.openxmlformats.org/drawingml/2006/main"
        effectLst = spPr.find(f'{{{ns_a}}}effectLst')
        if effectLst is None:
            effectLst = etree.SubElement(spPr, f'{{{ns_a}}}effectLst')
            
        outerShdw = etree.SubElement(effectLst, f'{{{ns_a}}}outerShdw')
        outerShdw.set('blurRad', '150000') # Softness
        outerShdw.set('dist', '30000')     # Distance
        outerShdw.set('dir', '5400000')    # Angle
        outerShdw.set('algn', 'b')
        
        srgbClr = etree.SubElement(outerShdw, f'{{{ns_a}}}srgbClr')
        srgbClr.set('val', '000000')
        alpha = etree.SubElement(srgbClr, f'{{{ns_a}}}alpha')
        alpha.set('val', '15000')          # 15% opacity

    # === Setup Presentation ===
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 1. Background
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(242, 242, 242)  # Light gray F2F2F2

    # 2. Left Sidebar Icons (Simulated via Unicode)
    sidebar_icons = ["\u2302", "\u1F50D", "\u25B6", "\u2661", "\u2295"] # Home, Search, Play, Heart, Create
    for i, icon in enumerate(sidebar_icons):
        tx_box = slide.shapes.add_textbox(Inches(0.4), Inches(2.0 + (i * 0.8)), Inches(0.5), Inches(0.5))
        p = tx_box.text_frame.add_paragraph()
        p.text = icon
        p.font.size = Pt(24)
        p.font.color.rgb = RGBColor(50, 50, 50)
        p.alignment = PP_ALIGN.CENTER

    # 3. Top Title
    title_box = slide.shapes.add_textbox(Inches(0.4), Inches(0.4), Inches(3.0), Inches(1.0))
    p = title_box.text_frame.add_paragraph()
    p.text = title_text
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.name = "Georgia" # Fallback for cursive/script

    # === Data Generation ===
    team_members = [
        {"name": "Aurora", "handle": "auroramoon", "full": "Aurora Moon", "role": "28, Design Specialist", "img_url": "https://picsum.photos/seed/team1/400/400", "fallback": (200,100,100)},
        {"name": "Draven", "handle": "dravenswift", "full": "Draven Swift", "role": "25, Technical Lead", "img_url": "https://picsum.photos/seed/team2/400/400", "fallback": (100,200,100)},
        {"name": "Max",    "handle": "maxsteele",   "full": "Max Steele",   "role": "28, Marketing Guru", "img_url": "https://picsum.photos/seed/team3/400/400", "fallback": (100,100,200)},
        {"name": "Zoe",    "handle": "zoeatlas",    "full": "Zoe Atlas",    "role": "27, Research Analyst","img_url": "https://picsum.photos/seed/team4/400/400", "fallback": (200,200,100)},
        {"name": "Jackson","handle": "jacksonsparks","full":"Jackson Sparks","role": "32, Project Coord.", "img_url": "https://picsum.photos/seed/team5/400/400", "fallback": (200,100,200)}
    ]
    
    active_index = 0  # Making Aurora the selected state
    active_member = team_members[active_index]
    active_img_bytes = get_image(active_member["img_url"], active_member["fallback"])
    active_circle_img = create_circle_image(active_img_bytes)

    # 4. Top Story Rings
    start_x = 2.8
    ring_y = 0.6
    ring_size = 1.0
    gap = 1.4

    for i, member in enumerate(team_members):
        cx = start_x + (i * gap)
        is_active = (i == active_index)
        
        # Download and crop profile pic
        if is_active:
            member_circle_img = active_circle_img
        else:
            img_bytes = get_image(member["img_url"], member["fallback"])
            member_circle_img = create_circle_image(img_bytes)

        if is_active:
            # Active Gradient Ring
            outer_ring = slide.shapes.add_shape(1, Inches(cx - 0.05), Inches(ring_y - 0.05), Inches(ring_size + 0.1), Inches(ring_size + 0.1)) # 1 = msoShapeOval
            outer_ring.line.fill.background() # No border
            add_gradient_fill(outer_ring, ["F58529", "DD2A7B", "8134AF"])
            
            # Inner Cutout Ring (matches background)
            inner_ring = slide.shapes.add_shape(1, Inches(cx + 0.02), Inches(ring_y + 0.02), Inches(ring_size - 0.04), Inches(ring_size - 0.04))
            inner_ring.fill.solid()
            inner_ring.fill.fore_color.rgb = RGBColor(242, 242, 242)
            inner_ring.line.fill.background()
            
            # Picture
            slide.shapes.add_picture(member_circle_img, Inches(cx + 0.05), Inches(ring_y + 0.05), Inches(ring_size - 0.1), Inches(ring_size - 0.1))
        else:
            # Inactive Gray Ring
            ring = slide.shapes.add_shape(1, Inches(cx), Inches(ring_y), Inches(ring_size), Inches(ring_size))
            ring.fill.background()
            ring.line.color.rgb = RGBColor(200, 200, 200)
            ring.line.width = Pt(2)
            
            # Picture (slightly smaller to leave gap)
            slide.shapes.add_picture(member_circle_img, Inches(cx + 0.075), Inches(ring_y + 0.075), Inches(ring_size - 0.15), Inches(ring_size - 0.15))
            
        # Name Label
        lbl_box = slide.shapes.add_textbox(Inches(cx - 0.25), Inches(ring_y + ring_size), Inches(1.5), Inches(0.4))
        p = lbl_box.text_frame.add_paragraph()
        p.text = member["name"]
        p.font.size = Pt(12)
        if is_active:
            p.font.bold = True
        p.alignment = PP_ALIGN.CENTER

    # 5. Main Content Card
    card = slide.shapes.add_shape(1, Inches(2.2), Inches(2.3), Inches(10.5), Inches(4.8)) # 1 = msoShapeRectangle
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(255, 255, 255)
    card.line.fill.background()
    add_shadow(card)

    # 6. Inside Card: Handle & Mini Avatar
    slide.shapes.add_picture(active_circle_img, Inches(2.6), Inches(2.6), Inches(0.4), Inches(0.4))
    
    handle_box = slide.shapes.add_textbox(Inches(3.1), Inches(2.55), Inches(3.0), Inches(0.4))
    p = handle_box.text_frame.add_paragraph()
    p.text = active_member["handle"]
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(30, 30, 30)

    # 7. Inside Card: Main Portrait
    # Just insert the square image to mimic the post image
    img_io = io.BytesIO(active_img_bytes)
    slide.shapes.add_picture(img_io, Inches(2.6), Inches(3.2), Inches(3.5), Inches(3.5))

    # 8. Inside Card: Bio & Details
    text_x = 6.6
    
    # Full Name
    name_box = slide.shapes.add_textbox(Inches(text_x), Inches(3.2), Inches(5.5), Inches(0.6))
    p = name_box.text_frame.add_paragraph()
    p.text = active_member["full"]
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 0, 0)
    
    # Subtitle (Age, Role)
    role_box = slide.shapes.add_textbox(Inches(text_x), Inches(3.7), Inches(5.5), Inches(0.5))
    p = role_box.text_frame.add_paragraph()
    p.text = active_member["role"]
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = RGBColor(80, 80, 80)
    
    # Body Text
    body_box = slide.shapes.add_textbox(Inches(text_x), Inches(4.3), Inches(5.5), Inches(2.0))
    body_box.text_frame.word_wrap = True
    p = body_box.text_frame.add_paragraph()
    p.text = body_text
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(100, 100, 100)

    prs.save(output_pptx_path)
    return output_pptx_path
