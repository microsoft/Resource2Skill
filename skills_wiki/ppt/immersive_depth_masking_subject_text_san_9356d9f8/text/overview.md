# Immersive Depth Masking (Subject-Text Sandwich)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Immersive Depth Masking (Subject-Text Sandwich)

* **Core Visual Mechanism**: This technique breaks the standard 2D flat plane of a presentation slide by interleaving elements in 3D space. It uses a "sandwich" layer logic: a solid background layer, a massive typographic layer in the middle, and an isolated, background-free photographic subject layer in the front. The subject overlaps the typography, creating a striking depth-of-field effect.
* **Why Use This Skill (Rationale)**: Human eyes are drawn to depth and overlapping elements because it mimics the physical world. Hiding parts of the text behind a subject forces the brain to "complete" the word (Gestalt principle of closure), which increases cognitive engagement. It feels highly editorial, akin to high-end magazine covers (like *TIME* or *National Geographic*).
* **Overall Applicability**: Perfect for high-impact hero slides, speaker introduction slides, product showcases, or title slides. It works beautifully when introducing a single focal concept (e.g., "DOG", "LEOPARD", "INNOVATION").
* **Value Addition**: Transforms a standard title slide into a dynamic, premium visual experience. The depth created by the masking gives the slide a modern, cinematic quality without requiring embedded video.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: Solid, high-contrast flat color. Typically pitch black `(10, 10, 10, 255)` or stark white `(245, 245, 245, 255)`.
  - **Typography**: Extremely large, heavy sans-serif font (e.g., Poppins Bold, Montserrat Black). White `(255, 255, 255, 255)` text on dark backgrounds. Font size is pushed to extremes (200pt+) so it spans the entire slide.
  - **Subject (Mask)**: A high-resolution photographic subject isolated on a transparent background. 
  - **Drop Shadow**: The text uses a strong outer shadow to visually separate it from the background layer and push the text "forward."

* **Step B: Compositional Style**
  - **Center Alignment**: Text is dead-centered horizontally and vertically. 
  - **Anchoring**: The subject is usually anchored to the bottom edge of the slide, popping up to intersect the bottom 30-50% of the text.

* **Step C: Dynamic Effects & Transitions**
  - **Parallax Reveal**: In PowerPoint, this is brought to life using a "Fade" entrance combined with an "Upward Motion Path" on the text layer. Because the text is sandwiched *behind* the subject, it creates a 3D parallax illusion as it slides up. *(Note: Code implementation below provides the static layered composition; motion paths are best applied natively in PPT).*

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layered Sandwich Logic** | `python-pptx` native | PPTX natively handles object z-index stacking (first added = bottom layer). |
| **Drop Shadow on Text** | `lxml` XML injection | `python-pptx` lacks a native API to set drop shadows on text boxes. We must inject `<a:outerShdw>` into the shape properties. |
| **Isolated Foreground Subject** | `urllib` / `PIL` | To recreate the "Remove Background" effect cleanly via code, we fetch a pre-cut transparent PNG. We use PIL to generate a fallback geometric mask if the download fails, ensuring the code always executes successfully. |

> **Feasibility Assessment**: **100% reproduction of the visual static layout.** The code constructs the exact visual "sandwich" (Dark Background -> Shadowed Text -> Cutout Image) shown in the tutorial. To replicate the animation shown in part 3 of the video, a user would manually apply a motion path to the generated text box.

#### 3b. Complete Reproduction Code

```python
import os
import urllib.request
from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str = "Immersive_Depth_Masking.pptx",
    title_text: str = "DOG",
    bg_color: tuple = (10, 10, 10),
    **kwargs
) -> str:
    """
    Create a PPTX file reproducing the Immersive Depth Masking (Sandwich) effect.
    
    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Solid Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # === Layer 2: Massive Typography with Drop Shadow ===
    # Positioned perfectly centered
    tb_width = Inches(12)
    tb_height = Inches(4)
    left = (prs.slide_width - tb_width) / 2
    top = (prs.slide_height - tb_height) / 2 - Inches(0.5) # Shifted slightly up
    
    tb = slide.shapes.add_textbox(left, top, tb_width, tb_height)
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title_text.upper()
    p.alignment = PP_ALIGN.CENTER
    
    run = p.runs[0]
    run.font.name = 'Arial Black' # Heavy sans-serif fallback
    run.font.size = Pt(200)
    run.font.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255)

    # XML Injection: Add a strong drop shadow to the text box shape
    # blurRad=127000 (10pt), dist=127000 (10pt), dir=2700000 (45 degrees down-right), alpha=60%
    shadow_xml = """
    <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:outerShdw blurRad="127000" dist="127000" dir="2700000" algn="tl" rotWithShape="0">
            <a:srgbClr val="000000">
                <a:alpha val="60000"/>
            </a:srgbClr>
        </a:outerShdw>
    </a:effectLst>
    """
    spPr = tb._element.spPr
    spPr.append(parse_xml(shadow_xml))

    # === Layer 3: Foreground Subject (Mask) ===
    # We download a transparent PNG (a dog) to act as the cutout subject.
    img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Dog_transparent_background.png/1024px-Dog_transparent_background.png"
    img_path = "temp_subject_mask.png"
    
    try:
        # Download the transparent subject
        urllib.request.urlretrieve(img_url, img_path)
    except Exception as e:
        print(f"Image download failed, generating PIL fallback mask. Error: {e}")
        # Fallback: Create a gray silhouette of an animal using PIL to ensure code execution
        img = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Draw a shape resembling a head/shoulders mask
        draw.ellipse((212, 300, 812, 1100), fill=(80, 80, 80, 255)) 
        draw.ellipse((100, 200, 400, 500), fill=(80, 80, 80, 255)) # Left ear
        draw.ellipse((624, 200, 924, 500), fill=(80, 80, 80, 255)) # Right ear
        img.save(img_path)

    # Insert the transparent image over the text
    # Anchored to the bottom center to create the depth illusion
    pic_width = Inches(8)
    pic_left = (prs.slide_width - pic_width) / 2
    # Adjust top to intersect the text visually
    pic_top = Inches(2.2) 
    
    slide.shapes.add_picture(img_path, pic_left, pic_top, width=pic_width)

    # Cleanup temporary image
    if os.path.exists(img_path):
        os.remove(img_path)

    prs.save(output_pptx_path)
    return output_pptx_path

if __name__ == "__main__":
    create_slide()
```