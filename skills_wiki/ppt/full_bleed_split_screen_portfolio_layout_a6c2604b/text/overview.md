# Full-Bleed Split-Screen Portfolio Layout

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Full-Bleed Split-Screen Portfolio Layout

*   **Core Visual Mechanism**: The slide is divided into two distinct, uncompromising geometric zones. One side is a solid-colored anchor block dedicated to typography (title and descriptive text), while the other side features a full-bleed, edge-to-edge hero image. This transforms floating text boxes into structural architectural elements.
*   **Why Use This Skill (Rationale)**: In the original video, the creator attempted to separate text and images using floating grey boxes on a white background, which often feels disjointed. A full-bleed split layout forces visual order. It provides high contrast for readability on the text panel while allowing the artwork/product to dominate its own dedicated space without overlapping or competing with the text.
*   **Overall Applicability**: Perfect for artist portfolios (like the Jeff Koons subject), product feature highlights, case study introductions, or any scenario where you must balance a dense paragraph of descriptive text with a high-impact visual.
*   **Value Addition**: Brings a magazine-like, editorial polish to basic informational slides. It eliminates the "pasted-in" look by making the image and text containers structural elements of the slide canvas itself.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    *   **Text Panel Background**: A solid, dark anchor color to contrast with the image. (e.g., Dark Slate `(40, 44, 52, 255)`).
    *   **Typography**: High-contrast text on the dark panel. White `(255, 255, 255, 255)` for readability.
    *   **Accent Detail**: A small, vibrant geometric accent line (e.g., Coral Red `(255, 107, 107, 255)`) to draw the eye to the title and add a touch of modern design flair.
    *   **Image**: A high-resolution image that strictly adheres to its bounding box, bleeding off the edges of the slide.

*   **Step B: Compositional Style**
    *   **Layout Proportion**: Typically a 40/60 or 35/65 split. The text panel occupies ~38% of the width (5 inches on a 13.33-inch slide), leaving the remaining 62% for the visual artwork.
    *   **Alignment**: Text is strictly left-aligned within its panel, respecting a generous inner margin (0.5 inches) to create breathing room.

*   **Step C: Dynamic Effects & Transitions**
    *   **Transitions (PowerPoint Native)**: This layout pairs beautifully with a simple "Push" transition from left or right, or a "Fade" transition.
    *   **Animation**: The text block can wipe in from the left, followed by the image fading in.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
| :--- | :--- | :--- |
| **Geometric Layout & Panels** | `python-pptx` native | Simple rectangles and text boxes are perfectly suited for building solid structural panels. |
| **Edge-to-Edge Image** | `python-pptx` native + PIL (Math) | `python-pptx` does not have a native "crop-to-fill" feature. We must use PIL to calculate the image's aspect ratio, compute the necessary crop percentages to avoid distortion, and apply them via the `python-pptx` crop attributes. |
| **Image Fallback** | `PIL/Pillow` | Ensures the code executes successfully by generating a synthetic gradient/geometric placeholder if external image downloads fail. |

*Feasibility Assessment*: 100%. The code structurally reproduces the intent of the video's layout (grouping text in a box next to an image) but elevates it to a professional, distortion-free split-screen design.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Balloon Dog",
    body_text: str = "The Balloon Dog is one of Jeff Koons' most famous sculptures. Completed in the 1990s, the ten-foot-tall piece is made out of mirror-polished stainless steel with a transparent color coating. It represents childhood innocence and the joy of simple celebrations.",
    image_keyword: str = "art,sculpture",
    panel_color: tuple = (40, 44, 52),      # Dark Slate RGB
    text_color: tuple = (255, 255, 255),    # White RGB
    accent_color: tuple = (255, 107, 107),  # Coral Red RGB
    **kwargs,
) -> str:
    """
    Creates a PPTX file featuring a Full-Bleed Split-Screen layout.
    """
    import os
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.dml.color import RGBColor
    from PIL import Image, ImageDraw

    # Initialize Presentation (16:9 Widescreen)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Left Content Panel ===
    left_panel_width = Inches(5.0)
    
    # Solid background block
    panel = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, left_panel_width, prs.slide_height
    )
    panel.fill.solid()
    panel.fill.fore_color.rgb = RGBColor(*panel_color)
    panel.line.fill.background() # Remove border

    # === Layer 2: Typography & Details ===
    # Decorative accent line above title
    accent = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.3), Inches(0.6), Inches(0.06)
    )
    accent.fill.solid()
    accent.fill.fore_color.rgb = RGBColor(*accent_color)
    accent.line.fill.background()

    # Title Box
    title_box = slide.shapes.add_textbox(
        Inches(0.4), Inches(1.5), Inches(4.2), Inches(1.0)
    )
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(44)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(*text_color)
    p_title.font.name = "Arial"

    # Body Text Box
    body_box = slide.shapes.add_textbox(
        Inches(0.4), Inches(2.8), Inches(4.0), Inches(4.0)
    )
    tf_body = body_box.text_frame
    tf_body.word_wrap = True
    p_body = tf_body.paragraphs[0]
    p_body.text = body_text
    p_body.font.size = Pt(16)
    p_body.font.color.rgb = RGBColor(*text_color)
    p_body.font.name = "Arial"

    # === Layer 3: Right Hero Image (with auto-crop-to-fill) ===
    img_path = "temp_split_img.jpg"
    target_w = prs.slide_width - left_panel_width
    target_h = prs.slide_height

    # 1. Acquire Image (Download or Fallback)
    try:
        url = f"https://picsum.photos/1200/800?random=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response, open(img_path, 'wb') as out_file:
            out_file.write(response.read())
    except Exception:
        # Generate synthetic fallback image if network fails
        img = Image.new('RGB', (1200, 800), color=(220, 224, 230))
        draw = ImageDraw.Draw(img)
        # Draw some abstract aesthetic shapes
        draw.ellipse([-200, -200, 600, 600], fill=(200, 205, 215))
        draw.rectangle([800, 400, 1400, 1000], fill=(205, 210, 220))
        img.save(img_path)

    # 2. Calculate Crop Percentages to prevent distortion
    with Image.open(img_path) as img:
        img_w, img_h = img.size
    
    img_ar = img_w / img_h
    target_ar = target_w / target_h

    # Insert picture without constraints initially
    pic = slide.shapes.add_picture(img_path, left_panel_width, 0)

    # Apply mathematically calculated crops
    if img_ar > target_ar:
        # Image is wider than target area -> crop sides
        crop_fraction = 1.0 - (target_ar / img_ar)
        pic.crop_left = crop_fraction / 2
        pic.crop_right = crop_fraction / 2
    elif img_ar < target_ar:
        # Image is taller than target area -> crop top/bottom
        crop_fraction = 1.0 - (img_ar / target_ar)
        pic.crop_top = crop_fraction / 2
        pic.crop_bottom = crop_fraction / 2

    # 3. Force the final cropped bounding box to fit the right pane perfectly
    pic.width = int(target_w)
    pic.height = int(target_h)

    # Cleanup temporary file
    if os.path.exists(img_path):
        os.remove(img_path)

    prs.save(output_pptx_path)
    return output_pptx_path
```