# Dual Call-to-Action (CTA) Closure

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dual Call-to-Action (CTA) Closure

* **Core Visual Mechanism**: A highly directive, action-oriented layout utilizing bold, symmetrical vertical block arrows to anchor the left and right sides of the slide. These arrows act as heavy visual guides, funneling the audience's eyes directly toward explicit "next step" instructions (CTAs), while maintaining a central focus on the core brand and web link.
* **Why Use This Skill (Rationale)**: The weakest way to end a presentation is a blank slide or a generic "Questions?". A dedicated CTA slide capitalizes on the audience's peak attention at the end of a talk. By offering clear, visually directed options (e.g., "Follow Us" and "More Info"), you remove friction and clearly dictate the post-presentation user journey. 
* **Overall Applicability**: Perfect for the final slides of webinars, sales pitches, educational courses, and marketing presentations where lead generation or audience retention is the primary goal.
* **Value Addition**: Transforms a passive ending into an active funnel. The heavy geometric symmetry creates a sense of authority and finality, while the high-contrast elements ensure readability even when projected or viewed on small screens.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: A subtle, non-distracting gradient (light gray to slightly darker gray) to give depth without clashing with the content.
  - **Color Logic**: 
    - Background: Light Gray (`#F5F5F5` to `#E6E6E6`)
    - Main Title: Black/Dark Charcoal (`(0, 0, 0, 255)`)
    - Accents (Arrows & Links): Corporate Blue (`(31, 78, 121, 255)`)
  - **Text Hierarchy**: 
    - Title: Largest, bold, centered at the top.
    - URL: Medium-large, colored, centered.
    - CTA Text: Medium, bold, matching the accent color, placed explicitly at the tip of the directional arrows.

* **Step B: Compositional Style**
  - Symmetrical layout emphasizing balance.
  - Left Arrow anchored at ~20% of slide width; Right Arrow anchored at ~80% of slide width.
  - The URL occupies the negative space exactly in the center of the slide, cradled between the two large arrow shafts.
  - Generous white space ensures the CTAs are unambiguous.

* **Step C: Dynamic Effects & Transitions**
  - *Best Practice for PowerPoint*: Apply a "Wipe" (Down) animation to the arrows, followed by a "Fade" animation for the text below them to simulate the flow of information. (Achievable natively in PPTX via manual setup).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Subtle gradient background** | `PIL/Pillow` | Native python-pptx doesn't support complex, smooth background gradients easily without heavy XML manipulation; PIL allows us to generate a clean, high-quality image layer perfectly sized for the slide. |
| **Symmetrical Layout & Shapes** | `python-pptx` | The built-in `MSO_SHAPE.DOWN_ARROW` is ideal for this exact use case. Text positioning and typography are best handled natively to allow the user to edit the text later. |

> **Feasibility Assessment**: 100% — The static visual style of the reference video can be perfectly recreated using standard PPTX shapes combined with a PIL-generated gradient background.

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from PIL import Image

def create_slide(
    output_pptx_path: str,
    title_text: str = "Expert Academy",
    url_text: str = "www.expertacademy.be",
    cta_left_text: str = "FOLLOW US\nCLICK HERE",
    cta_right_text: str = "MORE INFO\nCLICK HERE",
    accent_color: tuple = (31, 78, 121),  # Corporate Blue
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Dual Call-to-Action Closure" visual effect.
    
    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # === Layer 1: Background Gradient via PIL ===
    bg_path = "temp_bg_gradient.png"
    width, height = int(13.333 * 100), int(7.5 * 100) # scale for resolution
    base = Image.new('RGB', (width, height), (250, 250, 250))
    top = Image.new('RGB', (width, height), (220, 225, 230))
    mask = Image.new('L', (width, height))
    
    # Create a vertical linear gradient mask
    mask_data = []
    for y in range(height):
        val = int(255 * (y / height))
        mask_data.extend([val] * width)
    mask.putdata(mask_data)
    
    base.paste(top, (0, 0), mask)
    base.save(bg_path)
    
    # Add background to slide
    slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)

    # === Layer 2: Main Typography ===
    
    # Title
    title_box = slide.shapes.add_textbox(Inches(1.666), Inches(1.0), Inches(10), Inches(1.2))
    tf_title = title_box.text_frame
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(54)
    p_title.font.bold = True
    p_title.font.name = "Arial"
    p_title.font.color.rgb = RGBColor(0, 0, 0)
    p_title.alignment = PP_ALIGN.CENTER

    # Center URL
    url_box = slide.shapes.add_textbox(Inches(3.666), Inches(3.2), Inches(6), Inches(1.0))
    tf_url = url_box.text_frame
    p_url = tf_url.paragraphs[0]
    p_url.text = url_text
    p_url.font.size = Pt(28)
    p_url.font.bold = True
    p_url.font.name = "Arial"
    p_url.font.color.rgb = RGBColor(*accent_color)
    p_url.font.underline = True
    p_url.alignment = PP_ALIGN.CENTER

    # === Layer 3: Visual Vectors & Arrows ===
    
    # Left Arrow
    left_arrow = slide.shapes.add_shape(
        MSO_SHAPE.DOWN_ARROW, 
        Inches(2.5), Inches(2.2), Inches(1.5), Inches(3.8)
    )
    left_arrow.fill.solid()
    left_arrow.fill.fore_color.rgb = RGBColor(*accent_color)
    left_arrow.line.color.rgb = RGBColor(*accent_color)

    # Right Arrow
    right_arrow = slide.shapes.add_shape(
        MSO_SHAPE.DOWN_ARROW, 
        Inches(9.333), Inches(2.2), Inches(1.5), Inches(3.8)
    )
    right_arrow.fill.solid()
    right_arrow.fill.fore_color.rgb = RGBColor(*accent_color)
    right_arrow.line.color.rgb = RGBColor(*accent_color)

    # === Layer 4: Action Text ===
    def add_action_text(x, y, text):
        box = slide.shapes.add_textbox(x, y, Inches(3.0), Inches(1.0))
        tf = box.text_frame
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.name = "Arial"
        p.font.color.rgb = RGBColor(*accent_color)
        p.alignment = PP_ALIGN.CENTER

    # Place text directly below the arrow tips
    add_action_text(Inches(1.75), Inches(6.2), cta_left_text)
    add_action_text(Inches(8.583), Inches(6.2), cta_right_text)

    # Save presentation
    prs.save(output_pptx_path)
    
    # Cleanup temp file
    if os.path.exists(bg_path):
        os.remove(bg_path)
        
    return output_pptx_path
```