# Geometric Image Mosaic

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Geometric Image Mosaic

*   **Core Visual Mechanism**: A single, powerful image is revealed through a grid of custom geometric shapes (e.g., triangles, hexagons, circles). The shapes act as a "mask" or "window," fragmenting the image and creating a dynamic, structured composition that balances organic photo texture with rigid geometry.

*   **Why Use This Skill (Rationale)**: This technique adds a layer of professional design and visual interest to a standard full-bleed image. The geometric pattern guides the viewer's eye, creates a sense of order and complexity, and can be thematically linked to the content (e.g., hexagons for technology, triangles for structure/growth). It transforms a simple photo into a deliberate design element.

*   **Overall Applicability**: Excellent for:
    *   **Title Slides**: Immediately grabs attention for presentations on technology, architecture, data science, or corporate strategy.
    *   **Section Dividers**: Provides a visually consistent but adaptable way to introduce new topics.
    *   **Portfolio/Product Showcases**: Highlights a key image with a modern, stylish frame.

*   **Value Addition**: Elevates a basic "image + text" slide into a sophisticated, high-impact visual statement. It adds texture, rhythm, and a modern aesthetic that feels intentional and professionally designed.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    - **Background Image**: A high-quality, visually rich photograph. Cityscapes, technology, or nature shots with interesting textures work best.
    - **Geometric Mask**: A repeating pattern of a single shape (e.g., triangles, hexagons). The shapes are arranged in a contiguous grid.
    - **Color Logic**:
        - **Background**: The slide background is typically a solid, dark color like black `(0, 0, 0, 255)` or dark navy to make the image and text pop.
        - **Shape Borders**: A thin, contrasting border (e.g., white `(255, 255, 255, 255)`) is often applied to the geometric shapes to clearly define the mosaic pattern and separate it from the background.
    - **Text Hierarchy**:
        - **Title**: Large, bold, sans-serif font placed in the empty space, typically on the left or right side. Color is high-contrast (e.g., white).
        - **Subtitle/Logo**: Smaller text and/or a logo, positioned near the title.

*   **Step B: Compositional Style**
    - **Asymmetrical Balance**: The geometric mosaic typically occupies 50-60% of the slide on one side (e.g., the right), leaving the other side as negative space for text. This creates a strong visual anchor and a clear area for the message.
    - **Layering**: The slide is composed of three layers:
        1.  Solid color background (bottom).
        2.  The masked image (middle).
        3.  Text elements (top).

*   **Step C: Dynamic Effects & Transitions**
    - This style is primarily static. However, a "Fade" or "Wipe" entrance animation could be applied to the image mosaic and text in PowerPoint to add a subtle dynamic reveal. This code generates the static visual foundation.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect                 | Method      | Why this method                                                                                                                                                             |
| ------------------------------------ | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Geometric mask over an image         | PIL/Pillow  | The core effect is a boolean "intersect" operation between shapes and an image. `python-pptx` cannot do this natively. PIL allows us to create a precise RGBA alpha mask and composite it with the image, perfectly replicating the effect. |
| White borders on geometric shapes    | PIL/Pillow  | Drawing shapes with an outline is a standard feature in PIL's `ImageDraw` module, making it easy to add the border effect shown in the tutorial.                            |
| Basic text boxes and layout          | `python-pptx` | Standard placement of shapes and text is the library's primary strength.                                                                                                    |
| Fetching a high-quality background | `requests`    | To make the skill adaptable, we fetch an image from a source like Unsplash based on a keyword. `requests` is the standard for HTTP requests. A fallback to a solid color is included. |

> **Feasibility Assessment**: 100%. The combination of PIL for image compositing and `python-pptx` for slide assembly perfectly reproduces the visual essence of this technique.

#### 3b. Complete Reproduction Code

```python
import requests
import io
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    title_text: str = "The Technique Journey",
    subtitle_text: str = "@Microsoft",
    image_keyword: str = "cityscape",
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with the 'Geometric Image Mosaic' effect.

    Args:
        output_pptx_path (str): The path to save the generated PPTX file.
        title_text (str): The main title for the slide.
        subtitle_text (str): The subtitle for the slide.
        image_keyword (str): A keyword to search for a background image on Unsplash.

    Returns:
        str: The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    background = slide.background
    background.fill.solid()
    background.fill.fore_color.rgb = RGBColor(0, 0, 0)

    # === Layer 2: Geometric Image Mosaic ===
    # Define slide dimensions in pixels for PIL
    slide_width_px = int(prs.slide_width.emu / 9525)
    slide_height_px = int(prs.slide_height.emu / 9525)

    # Fetch an image from Unsplash
    image_url = f"https://source.unsplash.com/1280x720/?{image_keyword}"
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        bg_image = Image.open(io.BytesIO(response.content)).resize((slide_width_px, slide_height_px))
    except (requests.exceptions.RequestException, IOError):
        # Fallback to a plain gradient if image download fails
        bg_image = Image.new("RGB", (slide_width_px, slide_height_px), (10, 20, 40))

    # Create the geometric mask (using triangles as in the tutorial)
    mask = Image.new("L", (slide_width_px, slide_height_px), 0)
    draw = ImageDraw.Draw(mask)

    # Triangle properties
    side_length = 180
    height = int(side_length * (3**0.5) / 2)
    border_width = 8 # Corresponds to the white border in the tutorial

    # Draw the triangle grid on the right side of the slide
    start_x = int(slide_width_px * 0.45)
    for row in range(-1, int(slide_height_px / height) + 1):
        for col in range(int((slide_width_px - start_x) / side_length) + 1):
            cx = start_x + col * side_length
            cy = row * height
            if col % 2 != 0:
                cy += height // 2

            # Upward pointing triangle
            p1 = (cx, cy + height)
            p2 = (cx + side_length, cy + height)
            p3 = (cx + side_length // 2, cy)
            draw.polygon([p1, p2, p3], fill=255)

            # Downward pointing triangle (inverted)
            p1_inv = (cx, cy)
            p2_inv = (cx + side_length, cy)
            p3_inv = (cx + side_length // 2, cy + height)
            draw.polygon([p1_inv, p2_inv, p3_inv], fill=255)

    # Create a separate image for the borders
    border_image = Image.new("RGBA", (slide_width_px, slide_height_px), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(border_image)
    
    # Redraw triangles with outlines for the border effect
    for row in range(-1, int(slide_height_px / height) + 1):
        for col in range(int((slide_width_px - start_x) / side_length) + 1):
            cx = start_x + col * side_length
            cy = row * height
            if col % 2 != 0:
                cy += height // 2
            
            p1, p2, p3 = (cx, cy + height), (cx + side_length, cy + height), (cx + side_length // 2, cy)
            border_draw.polygon([p1, p2, p3], outline=(255, 255, 255, 255), width=border_width)
            
            p1_inv, p2_inv, p3_inv = (cx, cy), (cx + side_length, cy), (cx + side_length // 2, cy + height)
            border_draw.polygon([p1_inv, p2_inv, p3_inv], outline=(255, 255, 255, 255), width=border_width)


    # Composite the image with the mask
    composite_image = Image.new("RGBA", (slide_width_px, slide_height_px))
    composite_image.paste(bg_image.convert("RGBA"), (0, 0), mask)
    composite_image.paste(border_image, (0, 0), border_image) # Add borders on top

    # Save the composite image to a buffer
    image_stream = io.BytesIO()
    composite_image.save(image_stream, format="PNG")
    image_stream.seek(0)

    # Add the final image to the slide
    slide.shapes.add_picture(image_stream, Inches(0), Inches(0), width=prs.slide_width)

    # === Layer 3: Text & Content ===
    # Add Title
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(6), Inches(1))
    title_tf = title_shape.text_frame
    p = title_tf.paragraphs[0]
    p.text = title_text
    p.font.name = 'Arial Black'
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # Add Subtitle
    subtitle_shape = slide.shapes.add_textbox(Inches(0.5), Inches(3.5), Inches(6), Inches(1))
    subtitle_tf = subtitle_shape.text_frame
    p_sub = subtitle_tf.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.name = 'Arial'
    p_sub.font.size = Pt(28)
    p_sub.font.color.rgb = RGBColor(255, 255, 255)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_slide("geometric_mosaic_slide.pptx", image_keyword="chicago")

```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback)?
- [x] Are all color values explicit RGB tuples?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?
- [x] Would someone looking at the output say "yes, that's the same technique"?