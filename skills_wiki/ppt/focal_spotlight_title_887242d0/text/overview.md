# Focal Spotlight Title

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Focal Spotlight Title

*   **Core Visual Mechanism**: This design uses a full-screen, high-quality background image overlaid with a large, centered, semi-transparent, and soft-edged dark circle. This circle acts as a "spotlight," creating a focused container for the slide's main title, ensuring high readability while maintaining a cinematic, atmospheric feel from the background image.

*   **Why Use This Skill (Rationale)**: The technique masterfully balances aesthetic impact with clarity.
    *   **Focus & Hierarchy**: The central dark element immediately draws the viewer's eye to the most important information—the title.
    *   **Contrast & Readability**: The semi-transparent overlay darkens the area behind the text, creating strong contrast that makes white or light-colored text legible against almost any background image.
    *   **Mood & Atmosphere**: The full-bleed image sets the emotional tone for the section (e.g., nature for growth, city for business), while the soft, circular spotlight gives it a polished, professional finish.

*   **Overall Applicability**: This style is highly versatile for any slide that serves to introduce a new topic. It is particularly effective for:
    *   Chapter or section dividers in a long presentation.
    *   Title slides for reports, proposals, or lectures.
    *   Introducing key concepts or principles.

*   **Value Addition**: Compared to a plain slide, it adds a layer of visual sophistication and professionalism. It elevates simple text into a design statement, making the content feel more significant and engaging.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    *   **Background Layer**: A single, high-resolution, full-bleed photograph. The subject matter should be evocative but not overly cluttered in the center.
    *   **Overlay Layer**: A large, soft-edged circular shape.
        *   **Color**: Black `(0, 0, 0)` with transparency.
        *   **Effect**: A soft, feathered edge achieved through a Gaussian blur. The transparency is typically around 60-75% (`alpha` of 150-190).
    *   **Text Layer**:
        *   **Main Title**: A bold, sans-serif font (e.g., Arial Black, Montserrat).
            *   **Color**: White `(255, 255, 255, 255)`.
            *   **Content**: The primary topic, e.g., "Alignment Principle".
        *   **Subtitle (Optional)**: A lighter-weight, smaller, all-caps sans-serif font (e.g., Arial, Calibri).
            *   **Color**: White `(255, 255, 255, 255)`.
            *   **Content**: Supporting text, e.g., "FOUR PRINCIPLES OF TYPOGRAPHY".

*   **Step B: Compositional Style**
    *   **Layout**: Strictly centered. The circular overlay is positioned at the exact center of the slide. All text elements are horizontally and vertically centered within the circle.
    *   **Proportions**: The diameter of the circle typically occupies **50% to 60%** of the slide's height.

*   **Step C: Dynamic Effects & Transitions**
    *   **Animation**: The original video has no animations for this slide type. For added effect, a simple "Fade" entrance animation on the text elements would be appropriate. This is easily added manually in PowerPoint or via lxml.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect                  | Method                 | Why this method                                                                                                    |
| ------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Full-bleed background image           | `requests` + `PIL`       | To dynamically fetch high-quality images and provide a reliable fallback if the network fails.                     |
| Semi-transparent circle with soft edge | `PIL` / Pillow         | `python-pptx` cannot create shapes with soft/blurred edges. PIL is perfect for image compositing and filter effects. |
| Text placement and formatting         | `python-pptx` native   | Standard API for creating, positioning, and styling text boxes.                                                    |

> **Feasibility Assessment**: **95%**. The code fully reproduces the core visual style. The remaining 5% would account for specific font matching (which depends on the user's system) and advanced color grading of the background image, which is beyond the scope of a single skill.

#### 3b. Complete Reproduction Code

```python
import requests
import io
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from PIL import Image, ImageDraw, ImageFilter

def create_slide(
    output_pptx_path: str,
    title_text: str = "Alignment Principle",
    subtitle_text: str = "FOUR PRINCIPLES OF TYPOGRAPHY",
    bg_keyword: str = "forest,aerial",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a 'Focal Spotlight Title' design.

    This effect features a full-bleed background image with a semi-transparent,
    soft-edged dark circle in the center, containing the title and subtitle.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        title_text: The main text to display in the spotlight.
        subtitle_text: The smaller text to display below the main title.
        bg_keyword: A comma-separated keyword string for fetching a background
                    image from Unsplash (e.g., 'technology', 'nature,abstract').

    Returns:
        The path to the saved PPTX file.
    """
    SLIDE_WIDTH_PX = 1920
    SLIDE_HEIGHT_PX = 1080

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- 1. Create the Background with PIL ---
    try:
        # Download a background image from Unsplash
        image_url = f"https://source.unsplash.com/{SLIDE_WIDTH_PX}x{SLIDE_HEIGHT_PX}/?{bg_keyword}"
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        bg_img = Image.open(io.BytesIO(response.content)).convert("RGBA")
    except requests.exceptions.RequestException:
        # Fallback to a solid dark background if image download fails
        bg_img = Image.new("RGBA", (SLIDE_WIDTH_PX, SLIDE_HEIGHT_PX), (30, 30, 30, 255))

    # --- 2. Create the Soft-Edged Spotlight Overlay with PIL ---
    # Create a new transparent layer for the spotlight
    overlay = Image.new("RGBA", bg_img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Define circle properties
    circle_radius = SLIDE_HEIGHT_PX * 0.28  # Approx 56% of slide height
    circle_center = (SLIDE_WIDTH_PX / 2, SLIDE_HEIGHT_PX / 2)
    circle_box = [
        circle_center[0] - circle_radius,
        circle_center[1] - circle_radius,
        circle_center[0] + circle_radius,
        circle_center[1] + circle_radius,
    ]
    
    # Draw a black, semi-transparent circle onto the overlay layer
    spotlight_alpha = 180  # Control transparency (0-255)
    draw.ellipse(circle_box, fill=(0, 0, 0, spotlight_alpha))

    # Apply a Gaussian blur to create the soft edge
    blur_radius = 50
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    # Composite the spotlight overlay onto the background image
    combined_img = Image.alpha_composite(bg_img, overlay)

    # --- 3. Add the Composited Image to the Slide ---
    with io.BytesIO() as output:
        combined_img.save(output, format="PNG")
        slide.shapes.add_picture(output, Inches(0), Inches(0), width=prs.slide_width, height=prs.slide_height)

    # --- 4. Add and Format Text ---
    # Main Title
    title_shape = slide.shapes.add_textbox(
        Inches(2), Inches(3), Inches(9.333), Inches(1)
    )
    title_tf = title_shape.text_frame
    title_tf.text = title_text
    title_tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    title_font = title_tf.paragraphs[0].font
    title_font.name = 'Arial Black'
    title_font.size = Pt(44)
    title_font.color.rgb = RGBColor(255, 255, 255)

    # Subtitle
    subtitle_shape = slide.shapes.add_textbox(
        Inches(2), Inches(3.9), Inches(9.333), Inches(0.6)
    )
    subtitle_tf = subtitle_shape.text_frame
    subtitle_tf.text = subtitle_text
    subtitle_tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    subtitle_font = subtitle_tf.paragraphs[0].font
    subtitle_font.name = 'Arial'
    subtitle_font.size = Pt(16)
    subtitle_font.color.rgb = RGBColor(255, 255, 255)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# if __name__ == '__main__':
#     create_slide(
#         output_pptx_path="focal_spotlight_title.pptx",
#         title_text="对 比 原 则",
#         subtitle_text="FOUR PRINCIPLES OF TYPOGRAPHY",
#         bg_keyword="mountain,snow"
#     )
#     create_slide(
#         output_pptx_path="focal_spotlight_title_2.pptx",
#         title_text="靠 近 原 则",
#         subtitle_text="FOUR PRINCIPLES OF TYPOGRAPHY",
#         bg_keyword="ocean,wave"
#     )

```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries? (`requests`, `io`, `pptx`, `PIL`)
- [x] Does it handle the case where an image download fails (fallback)? (Yes, falls back to a solid color background)
- [x] Are all color values explicit RGB/RGBA tuples? (Yes)
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes, the core mechanism is identical)
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes)