def create_presentation_morphing_team_cards(
    output_pptx_path: str,
    team_members: list = None,
    title_text: str = "Meet Our Team",
    **kwargs,
) -> str:
    """
    Creates a PowerPoint presentation with a dynamic team profile card reveal effect
    using the Morph transition.

    To see the effect:
    1. Open the generated PPTX file.
    2. In the slide thumbnail pane on the left, select slides 2, 3, and 4.
    3. Go to the "Transitions" tab in the PowerPoint ribbon.
    4. Click "Morph".

    Args:
        output_pptx_path (str): The path to save the generated .pptx file.
        team_members (list, optional): A list of dictionaries, where each dictionary
                                       represents a team member.
                                       Defaults to a sample list.
                                       Example:
                                       [{'name': 'Marcus Lee',
                                         'title': 'Photographer | Videographer',
                                         'color': (146, 208, 80),
                                         'img_url': '...'}, ...]
        title_text (str, optional): The main title for the slide.

    Returns:
        str: The path to the saved presentation file.
    """
    import os
    import urllib.request
    from io import BytesIO
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw, ImageFont

    # --- Default Data ---
    if team_members is None:
        team_members = [
            {
                "name": "Marcus Lee",
                "title": "Professional Photographer |\nVideographer | Journalist",
                "color": (146, 208, 80),  # Green
                "img_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=256&h=256&fit=crop",
            },
            {
                "name": "David Ryan",
                "title": "Professional Photographer |\nVideographer | Journalist",
                "color": (79, 129, 189),  # Blue
                "img_url": "https://images.unsplash.com/photo-1583864697784-a0efc8379f70?q=80&w=256&h=256&fit=crop",
            },
            {
                "name": "Jason Cole",
                "title": "Professional Photographer |\nVideographer | Journalist",
                "color": (0, 176, 150),  # Teal
                "img_url": "https://images.unsplash.com/photo-1542327897-4141b355e20e?q=80&w=256&h=256&fit=crop",
            },
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    def add_title(slide, text):
        title_shape = slide.shapes.add_textbox(Inches(0), Inches(0.5), prs.slide_width, Inches(1))
        title_shape.name = "Main_Title"
        p = title_shape.text_frame.paragraphs[0]
        p.text = text
        p.font.name = 'Dancing Script'
        p.font.size = Pt(44)
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER

    def create_circular_image(url):
        try:
            with urllib.request.urlopen(url) as response:
                img_data = response.read()
            img = Image.open(BytesIO(img_data)).convert("RGBA")
            size = (min(img.size), min(img.size))
            mask = Image.new('L', size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + size, fill=255)
            
            # Crop to center
            left = (img.width - size[0]) / 2
            top = (img.height - size[1]) / 2
            right = (img.width + size[0]) / 2
            bottom = (img.height + size[1]) / 2
            img = img.crop((left, top, right, bottom))
            
            img.putalpha(mask)
            
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            return img_byte_arr
        except Exception:
            # Fallback if image download fails
            img = Image.new('RGBA', (256, 256), (200, 200, 200, 255))
            mask = Image.new('L', (256, 256), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 256, 256), fill=255)
            img.putalpha(mask)
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            return img_byte_arr

    def _draw_card(slide, member_data, index, is_revealed):
        card_width = Inches(3.0)
        card_height = Inches(4.0)
        total_width = len(team_members) * card_width + (len(team_members) - 1) * Inches(0.75)
        start_x = (prs.slide_width - total_width) / 2
        card_x = start_x + index * (card_width + Inches(0.75))
        card_y = Inches(2.0)
        
        # --- Background Reveal Shape (Only add if revealed) ---
        if is_revealed:
            bg_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, 
                                            card_x - Inches(0.1), card_y - Inches(0.1), 
                                            card_width + Inches(0.2), card_height + Inches(0.2))
            bg_shape.name = f"Card_{index}_BG"
            bg_shape.rotation = -15.0
            fill = bg_shape.fill
            fill.solid()
            fill.fore_color.rgb = RGBColor(*member_data['color'])
            bg_shape.line.fill.background()

        # --- Main White Card ---
        base_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, card_x, card_y, card_width, card_height)
        base_card.name = f"Card_{index}_Base"
        fill = base_card.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(255, 255, 255)
        base_card.line.fill.background()
        base_card.shadow.inherit = False

        # --- Profile Photo ---
        img_size = Inches(1.5)
        img_stream = create_circular_image(member_data['img_url'])
        pic = slide.shapes.add_picture(img_stream, card_x + (card_width - img_size) / 2, card_y + Inches(0.5), width=img_size, height=img_size)
        pic.name = f"Card_{index}_Photo"

        # --- Name Text ---
        name_box = slide.shapes.add_textbox(card_x, card_y + Inches(2.2), card_width, Inches(0.75))
        name_box.name = f"Card_{index}_Name"
        p = name_box.text_frame.paragraphs[0]
        p.text = member_data['name']
        p.font.name = 'Dancing Script'
        p.font.size = Pt(28)
        p.font.color.rgb = RGBColor(38, 38, 38)
        p.alignment = PP_ALIGN.CENTER
        
        # --- Details Text (Only add if revealed) ---
        if is_revealed:
            details_box = slide.shapes.add_textbox(card_x + Inches(0.25), card_y + Inches(2.8), card_width - Inches(0.5), Inches(1.0))
            details_box.name = f"Card_{index}_Details"
            p = details_box.text_frame.paragraphs[0]
            p.text = member_data['title']
            p.font.name = 'Calibri'
            p.font.size = Pt(12)
            p.font.color.rgb = RGBColor(100, 100, 100)
            p.alignment = PP_ALIGN.CENTER
            details_box.text_frame.word_wrap = True

    # --- Create Slides ---
    
    # Slide 1: Initial state (all cards hidden)
    slide_initial = prs.slides.add_slide(blank_slide_layout)
    add_title(slide_initial, title_text)
    for i, member in enumerate(team_members):
        _draw_card(slide_initial, member, i, is_revealed=False)

    # Subsequent slides: One card revealed at a time
    for i, member in enumerate(team_members):
        slide = prs.slides.add_slide(blank_slide_layout)
        add_title(slide, title_text)
        for j, other_member in enumerate(team_members):
            _draw_card(slide, other_member, j, is_revealed=(i == j))

    prs.save(output_pptx_path)
    print(f"Presentation saved to {output_pptx_path}")
    print("REMINDER: Open the file, select slides 2 onward, and apply the 'Morph' transition.")
    return output_pptx_path

# Example Usage:
# create_presentation_morphing_team_cards("team_cards_morph.pptx")
