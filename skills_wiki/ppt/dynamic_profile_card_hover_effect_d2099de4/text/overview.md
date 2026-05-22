# Dynamic Profile Card Hover Effect

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic Profile Card Hover Effect

*   **Core Visual Mechanism**: The design uses a minimalist layout for team profiles that reveals more detail through a dynamic "hover" effect. This is achieved using PowerPoint's **Morph transition**. An initially clean profile card (photo and name) animates to a more detailed state, with a colorful, rotated background shape emerging from behind, creating a sense of depth and interactivity.

*   **Why Use This Skill (Rationale)**: This technique presents information progressively, keeping the initial slide clean and uncluttered while inviting user engagement. The smooth, fluid animation of the Morph transition feels modern and professional, turning a static list of names into a visually engaging experience. It focuses attention on one team member at a time.

*   **Overall Applicability**: This style is highly effective for:
    *   "Meet Our Team" or "About Us" slides.
    *   Speaker introductions for a webinar or conference agenda.
    *   Highlighting project leads or key stakeholders.
    *   Showcasing client testimonials with a photo and quote reveal.

*   **Value Addition**: It elevates a standard informational slide into a polished, interactive-feeling presentation. The animation adds a "wow" factor that captures audience attention and makes the content more memorable.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    *   **Profile Card (Foreground)**: A white, rounded rectangle that serves as the main container for the profile information.
    *   **Profile Picture**: A circular picture, positioned at the top of the card.
    *   **Name Text**: A prominent, stylized script font to give it personality. Example: "Dancing Script".
    *   **Details Text**: A clean, smaller sans-serif font for the job title and other details. Example: "Calibri". This text is initially absent and appears during the morph.
    *   **Background Shape (Reveal)**: A larger, solid-colored rounded rectangle that is hidden in the initial state. During the morph, it appears behind the profile card, rotated at a slight angle.
    *   **Color Logic**:
        *   Card Fill: White `(255, 255, 255)`
        *   Text: Dark Gray/Black `(38, 38, 38)`
        *   Background Shape 1 (Green): `(146, 208, 80)`
        *   Background Shape 2 (Blue): `(79, 129, 189)`
        *   Background Shape 3 (Teal): `(0, 176, 150)`
    *   **Text Hierarchy**:
        *   Title: "Meet Our Team" - large, script font.
        *   Name: Medium-large script font on the card.
        *   Details: Small sans-serif font below the name.

*   **Step B: Compositional Style**
    *   **Layout**: A clean, symmetrical grid, typically with three profile cards distributed horizontally across the slide.
    *   **Layering**: The effect relies on precise layering. From back to front: Rotated Background Shape -> White Profile Card -> Circular Photo & Text.
    *   **Proportions**: The background shape is roughly 10-15% larger than the profile card. It's rotated approximately -15 degrees to create a dynamic, asymmetrical accent.

*   **Step C: Dynamic Effects & Transitions**
    *   The entire animation is powered by the **PowerPoint Morph Transition**.
    *   To make it work, objects that persist across slides (like the profile card and photo) **must have the same name**. Objects that appear or disappear (like the background shape and details text) are simply added or removed from a slide, and Morph handles the fade/animation.
    *   The animation sequence is built across multiple slides, each representing a "hover" state for one of the cards.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect                 | Method           | Why this method                                                                                                                                                                                                                                                                                            |
| ------------------------------------ | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Layout, Shapes, and Text             | `python-pptx`      | All core elements are standard shapes (rounded rectangles, ovals) and text boxes, which are natively supported.                                                                                                                                                                                            |
| Profile Pictures                     | `urllib` & `PIL`   | `urllib` is used to fetch placeholder images. `PIL` is used to crop the downloaded images into a circle by creating a circular alpha mask, ensuring a clean look. A PIL-generated fallback is included if image download fails.                                                                                |
| **Morph Transition Logic**           | **`python-pptx` (Object Naming)** | The key to the Morph transition is consistent object naming. `python-pptx` allows setting the `shape.name` property. The code programmatically creates the necessary slides and names each corresponding object identically (e.g., `Card_1_Photo` on slide 1 and slide 2), which enables PowerPoint's Morph engine to animate them. |

> **Feasibility Assessment**: **99%**. The code generates a complete set of slides with all visual elements and consistent object naming, perfectly setting the stage for the Morph transition. The final 1% is the user's manual action of selecting the slides in PowerPoint and clicking the "Morph" transition button. This is the most robust and reliable way to automate this effect.

#### 3b. Complete Reproduction Code

```python
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
```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback)?
- [x] Are all color values explicit RGB tuples?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes, it creates the exact static slide layouts needed).
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes, after applying the Morph transition, the effect is identical).