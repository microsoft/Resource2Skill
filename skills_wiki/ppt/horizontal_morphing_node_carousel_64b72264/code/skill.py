def create_slide(
    output_pptx_path: str,
    title_text: str = "Few Words from our clients",
    subtitle_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    accent_color: tuple = (0, 191, 255),  # Not heavily used here, but good for customization
    **kwargs,
) -> str:
    """
    Creates a Morphing Node Carousel presentation (Testimonials).
    Generates multiple slides, each highlighting a different client, and applies Morph.
    """
    import urllib.request
    from io import BytesIO
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.oxml import parse_xml
    from PIL import Image, ImageDraw, ImageOps
    
    # --- Data Definition ---
    clients = [
        {"name": "Mrs. Client Y", "rating": 5, "text": "Outstanding service! They went above and beyond my expectations.", "img_url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=300&q=80"},
        {"name": "Mr. Client X", "rating": 4, "text": "Very solid execution. Delivered on time and with great quality.", "img_url": "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=300&q=80"},
        {"name": "Ms. Director A", "rating": 5, "text": "A game changer for our business. The transition was flawless.", "img_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=300&q=80"},
        {"name": "Mr. Manager B", "rating": 3, "text": "Good work overall. A few minor hiccups but resolved quickly.", "img_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=300&q=80"},
    ]

    # --- Helper: Create Circular Image via PIL ---
    def get_circular_avatar(img_url: str, size: int = 300) -> BytesIO:
        try:
            req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                img = Image.open(BytesIO(response.read())).convert("RGBA")
        except Exception:
            # Fallback to a solid colored circle with initials if download fails
            img = Image.new("RGBA", (size, size), (220, 220, 220, 255))
            
        # Crop to square
        w, h = img.size
        min_dim = min(w, h)
        img = img.crop(((w - min_dim) // 2, (h - min_dim) // 2, (w + min_dim) // 2, (h + min_dim) // 2))
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        
        # Create circular mask
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        
        # Apply mask
        output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        output.paste(img, (0, 0), mask)
        
        img_io = BytesIO()
        output.save(img_io, format="PNG")
        img_io.seek(0)
        return img_io

    # Pre-process avatars to save time during slide generation
    avatars = [get_circular_avatar(c["img_url"]) for c in clients]

    # --- Presentation Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Layout Calculations
    num_clients = len(clients)
    track_y = Inches(4.5)
    start_x = Inches(2.0)
    end_x = Inches(11.333)
    step_x = (end_x - start_x) / (num_clients - 1) if num_clients > 1 else 0
    
    # Generate one slide per client to demonstrate the Morph effect
    for active_idx, active_client in enumerate(clients):
        slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
        
        # 1. Add Title & Subtitle
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(8), Inches(1))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(32)
        p.font.bold = True
        
        sub_p = tf.add_paragraph()
        sub_p.text = subtitle_text
        sub_p.font.size = Pt(14)
        sub_p.font.color.rgb = RGBColor(100, 100, 100)
        
        # 2. Draw the Track (Horizontal Line)
        track = slide.shapes.add_connector(MSO_SHAPE.LINE_INVERSE, Inches(1), track_y, Inches(12.333), track_y)
        track.line.color.rgb = RGBColor(200, 200, 200)
        track.line.width = Pt(2)
        
        # 3. Draw Nodes and Content
        for i, client in enumerate(clients):
            node_x = start_x + (i * step_x)
            
            if i == active_idx:
                # --- ACTIVE STATE ---
                # Active Avatar (Large, above line)
                avatar_size = Inches(1.8)
                avatar_pic = slide.shapes.add_picture(
                    avatars[i], 
                    node_x - (avatar_size/2), 
                    track_y - avatar_size - Inches(0.2), 
                    avatar_size, avatar_size
                )
                # Assign a specific name so PowerPoint Morph forces a match across slides
                avatar_pic.name = "!!ActiveAvatar" 
                
                # Active Detail Card (Below line)
                card_width = Inches(5.0)
                card_height = Inches(1.5)
                # Ensure card stays within slide bounds
                card_x = node_x - (card_width/2)
                if card_x < Inches(0.5): card_x = Inches(0.5)
                if card_x + card_width > Inches(12.8): card_x = Inches(12.833) - card_width
                
                card_y = track_y + Inches(0.3)
                
                card = slide.shapes.add_shape(
                    MSO_SHAPE.ROUNDED_RECTANGLE, 
                    card_x, card_y, card_width, card_height
                )
                card.fill.solid()
                card.fill.fore_color.rgb = RGBColor(245, 247, 250)  # Light grey-blue
                card.line.color.rgb = RGBColor(220, 220, 220)
                card.name = "!!ActiveCard"
                
                # Pointer Triangle to connect card to node
                tri_width = Inches(0.3)
                tri_height = Inches(0.2)
                tri = slide.shapes.add_shape(
                    MSO_SHAPE.ISOSCELES_TRIANGLE,
                    node_x - (tri_width/2), card_y - tri_height + Pt(1), tri_width, tri_height
                )
                tri.fill.solid()
                tri.fill.fore_color.rgb = RGBColor(245, 247, 250)
                tri.line.color.rgb = RGBColor(220, 220, 220)
                tri.name = "!!ActiveTriangle"
                
                # Content inside card
                tf = card.text_frame
                tf.word_wrap = True
                tf.margin_left = Inches(0.2)
                tf.margin_right = Inches(0.2)
                tf.margin_top = Inches(0.1)
                
                # Name
                p_name = tf.paragraphs[0]
                p_name.text = client["name"]
                p_name.font.bold = True
                p_name.font.size = Pt(14)
                
                # Stars
                p_stars = tf.add_paragraph()
                stars_filled = "★" * client["rating"]
                stars_empty = "☆" * (5 - client["rating"])
                p_stars.text = f"User Rating: {stars_filled}{stars_empty}"
                p_stars.font.size = Pt(12)
                p_stars.font.color.rgb = RGBColor(255, 190, 0) # Gold stars
                
                # Testimonial Text
                p_text = tf.add_paragraph()
                p_text.text = f'"{client["text"]}"'
                p_text.font.size = Pt(12)
                p_text.font.italic = True
                p_text.font.color.rgb = RGBColor(80, 80, 80)
                
            else:
                # --- INACTIVE STATE ---
                # Small circle node on the line
                node_size = Inches(0.3)
                node = slide.shapes.add_shape(
                    MSO_SHAPE.OVAL, 
                    node_x - (node_size/2), 
                    track_y - (node_size/2), 
                    node_size, node_size
                )
                node.fill.solid()
                node.fill.fore_color.rgb = RGBColor(180, 180, 180)
                node.line.fill.background()
                
                # Client Name Text below the line
                name_box = slide.shapes.add_textbox(
                    node_x - Inches(1), 
                    track_y + Inches(0.2), 
                    Inches(2), Inches(0.5)
                )
                name_tf = name_box.text_frame
                name_p = name_tf.paragraphs[0]
                name_p.text = client["name"]
                name_p.alignment = PP_ALIGN.CENTER
                name_p.font.size = Pt(12)
                name_p.font.color.rgb = RGBColor(120, 120, 120)

        # 4. INJECT MORPH TRANSITION via lxml
        # This adds <p:transition spd="slow"><p:morph/></p:transition> to the slide xml
        if active_idx > 0: # Don't need transition on the very first slide
            slide_element = slide._element
            transition_xml = """
            <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="slow">
                <p:morph/>
            </p:transition>
            """
            transition_element = parse_xml(transition_xml)
            # Insert the transition element right before the timing or attribute elements
            # A safe place is typically at the end of the slide element but before shape tree concludes, 
            # actually PowerPoint schema expects transition after alternateContent/timing.
            # appending to slide element works in most modern PPTX readers.
            slide_element.append(transition_element)

    prs.save(output_pptx_path)
    return output_pptx_path
