# Split-Panel Feature Layout (Staging for Simultaneous Animations)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Split-Panel Feature Layout (Staging for Simultaneous Animations)

* **Core Visual Mechanism**: The visual signature of this slide relies on a high-contrast, dual-column composition. One side features a solid, vibrant color block containing bold, repetitive typography. The other side features an isolated, standalone subject image with a transparent background (e.g., a cutout vehicle, product, or character).
* **Why Use This Skill (Rationale)**: This clean split-screen layout provides excellent visual balance. The heavy color block anchors the eye and delivers the core message, while the transparent background of the subject image prevents the slide from feeling boxed-in or cluttered. This setup is specifically designed to be the perfect "stage" for multi-animations—allowing both the text block and the image to fly in, fade, or spin into the frame independently yet harmoniously.
* **Overall Applicability**: Ideal for product introduction slides, feature highlights, sample placeholder decks, and hero sections where a specific item needs to be contextualized next to strong copy.
* **Value Addition**: Compared to a standard bulleted list next to a square photo, isolating the subject on a transparent background and pairing it with a bold color block immediately elevates the presentation to a modern, "brochure-like" aesthetic.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: A stark white canvas `(255, 255, 255, 255)` contrasted by a bright, vibrant accent block—in this case, a bright green `(50, 205, 50, 255)`. 
  - **Typography**: Heavy, sans-serif font (e.g., Arial Black), rendered purely in white `(255, 255, 255)` to pop against the colored container. The repetition of the text ("This is a sample") creates an intentional typographic pattern rather than just acting as a sentence.
  - **Imagery**: A PNG image with an alpha channel (transparency) to ensure the subject (the airplane) blends natively into the white background.

* **Step B: Compositional Style**
  - **Spatial Feel**: ~45% of the horizontal space is dedicated to the color block, leaving ~55% for the image and negative space.
  - **Centering**: Elements are center-aligned on the vertical axis, creating a stable, grounded feel.

* **Step C: Dynamic Effects & Transitions**
  - *The tutorial focuses heavily on the UI technique for simultaneous animations:*
  - **Adding Multiple Animations**: Selecting objects, applying an initial Entrance effect, then holding `Shift` while selecting a second effect from the Animation gallery (or clicking "Add Animation") to stack them without overwriting.
  - **Synchronization**: Using the **Animation Pane** to select the secondary animation and setting it to trigger "With Previous", ensuring both the entrance and emphasis effects run concurrently.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Split-panel layout & text container** | `python-pptx` native | Flat shapes and basic typography placement are handled perfectly by the native API. |
| **Standalone subject image** | `urllib` + PIL fallback | Python-pptx requires a local image file. We download a transparent PNG, and use PIL to generate a stylized paper plane with an alpha channel if the download fails. |
| **Simultaneous Animations** | **N/A (Limitation)** | `python-pptx` does not expose an API for `<p:timing>` XML elements. Manually injecting complex concurrent animation sequences via `lxml` is highly likely to corrupt the PPTX file. |

> **Feasibility Assessment**: The static visual composition (the split layout, typography, color blocks, and transparent imagery) is **100% reproducible** via code. However, the **dynamic animation sequence** (the primary topic of the tutorial) **cannot be reproduced** programmatically in Python safely. The code below focuses strictly on staging the exact visual layout seen before the animations play.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "This is a sample",
    bg_palette: str = "technology",  # Kept for signature compatibility
    accent_color: tuple = (50, 205, 50),  # Vibrant Green
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Split-Panel Object Reveal layout.
    Provides the visual staging used for simultaneous animation tutorials.
    
    Returns: path to the saved PPTX file.
    """
    import os
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image, ImageDraw

    # Initialize presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide_layout = prs.slide_layouts[6] 
    slide = prs.slides.add_slide(slide_layout)

    # === Layer 1: Left Text Block ===
    # Draw a vibrant green container on the left side
    left_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(1.0), Inches(1.75), Inches(5.5), Inches(4.0)
    )
    left_shape.fill.solid()
    left_shape.fill.fore_color.rgb = RGBColor(*accent_color)
    left_shape.line.fill.background()  # Remove border

    tf = left_shape.text_frame
    tf.word_wrap = True
    
    # Add repeated bold text pattern as seen in the tutorial
    for i in range(3):
        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p.text = title_text
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Arial Black"
        p.font.size = Pt(40)
        p.font.color.rgb = RGBColor(255, 255, 255)

    # === Layer 2: Right Subject Image ===
    # Attempt to download a transparent PNG (airplane silhouette)
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Airplane_silhouette.svg/512px-Airplane_silhouette.svg.png"
    image_path = "temp_subject_image.png"
    
    try:
        # Request with headers to avoid basic scraping blocks
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(image_path, 'wb') as out_file:
            out_file.write(response.read())
    except Exception:
        # Fallback to PIL: Generate a stylized paper plane with a transparent background
        img = Image.new("RGBA", (600, 400), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # Main wing body
        draw.polygon([(100, 200), (500, 100), (300, 350), (250, 250)], fill=(100, 150, 255, 255))
        # Shadow/lower wing flap
        draw.polygon([(500, 100), (250, 250), (200, 300)], fill=(70, 100, 180, 255))
        img.save(image_path)

    # Insert the transparent image on the right side of the split layout
    slide.shapes.add_picture(image_path, Inches(7.5), Inches(2.0), width=Inches(4.5))

    # Clean up temporary asset
    if os.path.exists(image_path):
        os.remove(image_path)

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
```