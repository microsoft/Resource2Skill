# Infographic Showcase with Interactive Example Panels

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Infographic Showcase with Interactive Example Panels

*   **Core Visual Mechanism**: This design uses a central "monitor" or "stage" metaphor to present a series of detailed visual examples, such as infographics or case studies. A persistent set of labeled, colored buttons acts as a navigation menu, allowing the user to select which example is displayed in the main viewing area. The style is characterized by a clean, flat aesthetic, ample white space, and the use of a magnifying glass effect to draw attention to specific details within the displayed content.

*   **Why Use This Skill (Rationale)**: This technique excels at structuring complex information. By presenting a visual "table of contents" (the buttons), it gives the audience a clear roadmap of the content to be covered. The central stage provides a consistent focal point, preventing the cognitive load of processing entirely new slide layouts for each example. This "single-frame, multiple-states" approach feels more dynamic and engaging than a linear slide progression, mimicking the experience of an interactive dashboard or application.

*   **Overall Applicability**: This is a powerful pattern for any presentation that involves walking an audience through a portfolio or a set of distinct examples.
    *   **Portfolio Reviews**: Showcasing different design projects, ad campaigns, or architectural mockups.
    *   **Educational Tutorials**: Breaking down a topic into 5 key types, 3 common mistakes, or 7 best practices.
    *   **Software Demos**: Displaying different feature screens or UI states within a consistent application frame.
    *   **Case Study Walkthroughs**: Presenting findings from multiple research studies or business cases.

*   **Value Addition**: Instead of a simple "next slide" sequence, this pattern provides a non-linear, organized view of the subject matter. It reinforces the idea that the examples are related parts of a whole, rather than disconnected pieces of information. The interactive feel empowers the presenter and engages the audience more deeply.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    *   **Framing Device**: A stylized computer monitor serves as the primary content holder.
    *   **Navigation**: A series of brightly colored, rounded rectangular buttons, each labeled (e.g., "Example 1").
    *   **Content**: Detailed infographics or images that are displayed within the monitor's screen area.
    *   **Attention Device**: A magnifying glass overlay that zooms in on a specific portion of the infographic to highlight a call-to-action (CTA) or key detail.
    *   **Color Logic**:
        *   Background: Light, muted blue (`(240, 248, 255, 255)`) or off-white to create a clean, professional canvas.
        *   Accent Palette (Buttons/Banner): A set of distinct, saturated colors to differentiate navigation items.
            *   Banner Orange: `(243, 156, 18, 255)`
            *   Button Red: `(231, 76, 60, 255)`
            *   Button Yellow: `(241, 196, 15, 255)`
            *   Button Green: `(46, 204, 113, 255)`
    *   **Text Hierarchy**:
        *   **Banner Text**: Large, bold, all-caps sans-serif (e.g., 'Arial Black', 'Montserrat ExtraBold') for the main theme.
        *   **Button Text**: Clean, bold sans-serif (e.g., 'Arial Bold'), typically in white for high contrast.

*   **Step B: Compositional Style**
    *   **Layout**: Centered and balanced. The monitor typically occupies the central 60% of the slide width, creating a strong focal point.
    *   **Flow**: The viewer's eye is drawn from the navigation buttons (the "what") to the monitor (the "detail").
    *   **Layering**: The design uses clear visual layers: Background -> Monitor Frame -> Infographic Content -> Magnifying Glass. This creates a sense of depth and focus.

*   **Step C: Dynamic Effects & Transitions**
    *   The core dynamic is a state change: clicking a button updates the content within the monitor. In a live presentation, this is achieved with PowerPoint Triggers or slide hyperlinks.
    *   The magnifying glass is a static overlay that simulates a dynamic zoom, effectively focusing the audience's attention without complex animation.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Main layout, monitor, buttons | `python-pptx` native | These are all composed of standard shapes (rectangles, rounded rectangles) and text boxes, which `python-pptx` handles perfectly. |
| Placeholder infographic | PIL/Pillow | To demonstrate the concept without relying on external assets, a plausible-looking infographic is generated programmatically. PIL provides the canvas and drawing tools for this. |
| Magnifying glass zoom effect | PIL/Pillow + `python-pptx` | The most effective way to create the magnified "lens" is to crop a section of the source image, scale it up, apply a circular alpha mask for transparency, and save it as a PNG. This PNG is then inserted by `python-pptx` over the original image. |
| Magnifying glass handle | `python-pptx` native | The handle can be easily drawn using a thick connector or rectangle shape, which is simpler than rendering it in PIL. |

> **Feasibility Assessment**: 85%. The code fully reproduces the static visual composition of the slide, including the monitor, navigation buttons, a generated infographic, and the detailed magnifying glass effect. The remaining 15% constitutes the *interactivity* (the ability to click buttons to change the displayed infographic), which requires PowerPoint's internal trigger system and is not accessible via the `python-pptx` API. The generated slide represents a single, complete state of the interactive concept.

#### 3b. Complete Reproduction Code

This code generates a single, self-contained PPTX slide that captures the essence of the tutorial's visual style.

```python
import io
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.dml import MSO_THEME_COLOR
from PIL import Image, ImageDraw, ImageFont

def create_placeholder_infographic(width: int, height: int) -> io.BytesIO:
    """Generates a simple, visually plausible infographic placeholder."""
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    font_path = "Arial.ttf"
    try:
        title_font = ImageFont.truetype(font_path, 40)
        large_font = ImageFont.truetype(font_path, 80)
        small_font = ImageFont.truetype(font_path, 24)
    except IOError:
        title_font, large_font, small_font = (ImageFont.load_default(),) * 3

    draw.text((30, 20), "VOLUNTEER TO COLLECT", fill=(243, 156, 18), font=title_font)
    draw.text((30, 80), "$100", fill=(52, 73, 94), font=large_font)

    icon_colors = [(60, 120, 180), (230, 126, 34), (46, 204, 113), (231, 76, 60)]
    icon_texts = ["Help with\nhomework", "Toys and\nSchool", "Help with\nsocial skills", "Hot meals\nand treats"]
    
    for i, (color, text) in enumerate(zip(icon_colors, icon_texts)):
        x = 50 + i * 200
        y = 250
        draw.ellipse([(x, y), (x + 80, y + 80)], fill=color)
        draw.multiline_text((x + 40, y + 90), text, fill=(80, 80, 80), font=small_font, anchor="ms")

    draw.text((30, 450), "FOR CHILDREN WHO REALLY NEED THEM", fill=(100, 100, 100), font=small_font)
    draw.line([(30, 480), (width - 30, 480)], fill=(200, 200, 200), width=2)
    
    draw.rectangle([(30, 550), (width - 30, 600)], fill=(231, 76, 60))
    draw.text((50, 565), "SIGN UP NOW AT WWW.EXAMPLEHOPE.COM", fill=(255, 255, 255), font=small_font)

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

def create_magnifying_glass_image(source_image_bytes: io.BytesIO, crop_box: tuple, zoom_factor: float = 1.5) -> io.BytesIO:
    """Creates a magnified, circular view of a part of an image with a transparent background."""
    source_image = Image.open(source_image_bytes).convert("RGBA")
    
    cropped = source_image.crop(crop_box)
    magnified_size = (int(cropped.width * zoom_factor), int(cropped.height * zoom_factor))
    magnified = cropped.resize(magnified_size, Image.LANCZOS)

    mask = Image.new('L', magnified.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0) + magnified.size, fill=255)

    result = Image.new('RGBA', magnified.size, (0, 0, 0, 0))
    result.paste(magnified, (0, 0), mask)
    
    draw_result = ImageDraw.Draw(result)
    draw_result.ellipse((0, 0) + magnified.size, outline=(80, 80, 80), width=10)

    img_byte_arr = io.BytesIO()
    result.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

def create_slide(
    output_pptx_path: str,
    title_text: str = "CALL-TO-ACTION",
    bg_color: tuple = (240, 248, 255),
    **kwargs
) -> str:
    """
    Creates a PPTX slide showcasing infographic CTA examples in a monitor frame.

    This function reproduces the static visual of one example being highlighted with a
    magnifying glass, as seen in the tutorial video.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # === Layer 2: Monitor and Static Elements ===
    base = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.66), Inches(6.7), Inches(2), Inches(0.15))
    base.fill.solid(); base.fill.fore_color.rgb = RGBColor(58, 87, 124); base.line.fill.background()
    stand = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.16), Inches(6.5), Inches(1), Inches(0.2))
    stand.fill.solid(); stand.fill.fore_color.rgb = RGBColor(58, 87, 124); stand.line.fill.background()
    
    bezel = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(2.5), Inches(1.5), Inches(8.33), Inches(5))
    bezel.fill.solid(); bezel.fill.fore_color.rgb = RGBColor(235, 235, 235)
    bezel.line.fill.solid(); bezel.line.fill.fore_color.rgb = RGBColor(180, 180, 180)
    
    screen_left, screen_top, screen_width, screen_height = (Inches(2.6), Inches(1.6), Inches(8.13), Inches(4.8))

    banner = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.5), Inches(0.5), Inches(4.33), Inches(0.7))
    banner.fill.solid(); banner.fill.fore_color.rgb = RGBColor(243, 156, 18); banner.line.fill.background()
    banner.text_frame.text = title_text
    p = banner.text_frame.paragraphs[0]; p.font.name = 'Arial Black'; p.font.size = Pt(24); p.font.color.rgb = RGBColor(255, 255, 255)

    button_data = [
        {"text": "EXAMPLE 1", "color": (231, 76, 60)},
        {"text": "EXAMPLE 2", "color": (241, 196, 15)},
        {"text": "EXAMPLE 3", "color": (46, 204, 113)},
        {"text": "EXAMPLE 4", "color": (52, 73, 94)},
        {"text": "EXAMPLE 5", "color": (230, 126, 34)},
    ]
    
    for i, data in enumerate(button_data):
        btn = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(11), Inches(1.5 + i * 0.7), Inches(1.8), Inches(0.5))
        btn.fill.solid(); btn.fill.fore_color.rgb = RGBColor(*data['color']); btn.line.fill.background()
        btn.text_frame.text = data['text']
        p = btn.text_frame.paragraphs[0]; p.font.bold = True; p.font.color.rgb = RGBColor(255, 255, 255); p.font.size = Pt(12)

    # === Layer 3: Infographic and Magnifying Glass ===
    infographic_bytes = create_placeholder_infographic(800, 600)
    slide.shapes.add_picture(infographic_bytes, screen_left, screen_top, width=screen_width, height=screen_height)
    infographic_bytes.seek(0) 

    # Area on the 800x600 infographic to magnify
    crop_area = (25, 540, 600, 610)
    magnified_lens_bytes = create_magnifying_glass_image(infographic_bytes, crop_area, zoom_factor=2.0)
    
    lens_size = Inches(2.8)
    lens_left = Inches(7)
    lens_top = Inches(4)
    slide.shapes.add_picture(magnified_lens_bytes, lens_left, lens_top, height=lens_size)

    handle_left = lens_left + lens_size - Inches(0.4)
    handle_top = lens_top + lens_size - Inches(0.4)
    connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, handle_left, handle_top, handle_left + Inches(1), handle_top + Inches(1))
    line = connector.line; line.color.rgb = RGBColor(80, 80, 80); line.width = Pt(12)
    
    prs.save(output_pptx_path)
    return output_pptx_path
```