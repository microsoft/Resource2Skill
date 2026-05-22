# Immersive Framed Content Panel

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Immersive Framed Content Panel

* **Core Visual Mechanism**: This design pattern juxtaposes a rich, complex, darkly themed background (often representing a brand, event, or overarching concept) with a stark, high-contrast, minimalist white content card floating in the center. The background acts as an immersive "stage" or frame, while the solid white card ensures that the actual presentation content remains 100% legible. 

* **Why Use This Skill (Rationale)**: Often, presenters want to use visually striking, thematic backgrounds but struggle with text readability. By containing the text within a distinct, opaque geometric panel that leaves generous margins, you achieve the best of both worlds: the emotional or branding impact of the rich background, and the crisp, cognitive clarity of a classic document. It visually separates the "environment" from the "information."

* **Overall Applicability**: Ideal for event presentations, keynote addresses, branded corporate decks, and high-stakes pitches where a premium, produced "broadcast" feel is desired without sacrificing the clarity of the core message. 

* **Value Addition**: Transforms a basic "white slide with black text" into a premium, broadcast-quality visual experience by leveraging spatial framing and depth.


### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: A dark, textured, or complex image (e.g., a dark navy `(13, 17, 28, 255)` to deep purple `(40, 20, 60, 255)` gradient with technical/network motifs).
  - **Content Panel**: A pristine white rectangle `(255, 255, 255, 255)` with sharp or very slightly rounded corners, separated from the background by a subtle drop shadow.
  - **Text Hierarchy**: Highly contrasting typography. Titles are large, bold, and black `(0, 0, 0, 255)`. Body copy and bullet points are dark grey `(80, 80, 80, 255)` to slightly reduce eye strain against the pure white background.

* **Step B: Compositional Style**
  - **Spatial Framing**: The background acts as a passe-partout. The white panel occupies approximately 75-80% of the canvas width and height, leaving a continuous 10-15% border of the background visible on all sides.
  - **Internal Padding**: The text inside the white panel has generous internal margins, never touching the edges of the panel, maintaining a calm, uncluttered reading area.

* **Step C: Dynamic Effects & Transitions**
  - The background typically remains static across slides (like a physical stage), while the content inside the white panel changes. 
  - A subtle "Fade" transition between slides maintains the illusion of a continuous background while the content updates.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Thematic Background** | `requests` / PIL | Attempts to download a rich, thematic background. If unavailable, uses PIL to dynamically generate a dark, professional gradient fallback. |
| **Content Panel & Text** | `python-pptx` native | Standard shape and text frame generation is perfect for the clean, structural layout of the card and typography. |
| **Panel Depth (Shadow)** | `lxml` XML injection | Native `python-pptx` lacks an API for adding drop shadows. Modifying the OOXML directly allows us to create the subtle elevation that separates the card from the background. |

> **Feasibility Assessment**: 95% — This code successfully reproduces the visual architecture, background layering, clean typography, and spatial framing. The exact background image from the event is proprietary, so a programmatic fallback/public image is used instead.

#### 3b. Complete Reproduction Code

```python
import os
import urllib.request
from io import BytesIO
from lxml import etree
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn

def _create_fallback_gradient(filepath: str, width: int = 1920, height: int = 1080):
    """Creates a dark tech-themed gradient background if image download fails."""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    color_top = (13, 17, 28)    # Dark Navy
    color_bottom = (40, 20, 60) # Deep Purple
    
    for y in range(height):
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * y / height)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * y / height)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    img.save(filepath)

def _add_drop_shadow(shape):
    """Injects OOXML to add a subtle drop shadow to a shape."""
    spPr = shape.element.spPr
    effectLst = etree.SubElement(spPr, qn('a:effectLst'))
    outerShdw = etree.SubElement(effectLst, qn('a:outerShdw'))
    
    # Shadow parameters
    outerShdw.set('blurRad', '400000')  # Blur radius
    outerShdw.set('dist', '350000')     # Distance
    outerShdw.set('dir', '2700000')     # Angle (45 degrees)
    outerShdw.set('algn', 'tl')         # Alignment
    outerShdw.set('rotWithShape', '0')
    
    srgbClr = etree.SubElement(outerShdw, qn('a:srgbClr'))
    srgbClr.set('val', '000000')        # Black shadow
    alpha = etree.SubElement(srgbClr, qn('a:alpha'))
    alpha.set('val', '40000')           # 40% Opacity

def create_slide(
    output_pptx_path: str,
    title_text: str = "Common Elements of a Pitch",
    body_text: str = "• What do you do?\n• Team\n• Traction\n• Unique Insights\n• Market Size\n• Ask",
    bg_keyword: str = "technology,network,dark",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Immersive Framed Content Panel effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Thematic Background ===
    bg_img_path = "temp_bg_framed_panel.jpg"
    bg_url = f"https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1920&auto=format&fit=crop"
    
    try:
        req = urllib.request.Request(bg_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(bg_img_path, 'wb') as out_file:
                out_file.write(response.read())
    except Exception as e:
        print(f"Background download failed, using PIL gradient fallback. Error: {e}")
        _create_fallback_gradient(bg_img_path)

    # Insert background covering the entire slide
    slide.shapes.add_picture(bg_img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # === Layer 2: The White Content Panel ===
    # Create the card leaving a generous margin to frame it with the background
    card_width = Inches(10.0)
    card_height = Inches(6.0)
    card_left = (prs.slide_width - card_width) / 2
    card_top = (prs.slide_height - card_height) / 2
    
    card = slide.shapes.add_shape(
        1,  # MSO_SHAPE.RECTANGLE
        card_left, card_top, card_width, card_height
    )
    
    # Style the card: pure white, no outline, with shadow
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(255, 255, 255)
    card.line.fill.background() # No line
    
    _add_drop_shadow(card)

    # === Layer 3: Typography ===
    # Title Box
    title_box = slide.shapes.add_textbox(
        card_left + Inches(0.8), 
        card_top + Inches(0.6), 
        card_width - Inches(1.6), 
        Inches(1.0)
    )
    title_frame = title_box.text_frame
    title_frame.word_wrap = True
    p_title = title_frame.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = 'Arial'
    p_title.font.size = Pt(40)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(0, 0, 0) # Stark Black

    # Body / Bullets Box
    body_box = slide.shapes.add_textbox(
        card_left + Inches(0.8), 
        card_top + Inches(1.8), 
        card_width - Inches(1.6), 
        card_height - Inches(2.4)
    )
    body_frame = body_box.text_frame
    body_frame.word_wrap = True
    
    for i, line in enumerate(body_text.split('\n')):
        p = body_frame.paragraphs[i] if i == 0 else body_frame.add_paragraph()
        p.text = line.replace('• ', '') # Remove manual bullet if exists to apply formatting
        p.font.name = 'Arial'
        p.font.size = Pt(28)
        p.font.color.rgb = RGBColor(80, 80, 80) # Dark Grey for readability
        p.space_after = Pt(14)
        p.level = 0
        
        # Add XML for native bullet points
        pPr = p._pPr
        buFont = etree.SubElement(pPr, qn('a:buFont'))
        buFont.set('typeface', 'Arial')
        buChar = etree.SubElement(pPr, qn('a:buChar'))
        buChar.set('char', '•')

    # Save and clean up
    prs.save(output_pptx_path)
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)
        
    return output_pptx_path
```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback)? *(Yes, PIL gradient fallback is included)*
- [x] Are all color values explicit RGBA/RGB tuples?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? *(Yes, creates the framed content panel with drop shadow)*
- [x] Would someone looking at the output say "yes, that's the same technique"? *(Yes, captures the core aesthetic of presenting clear white cards on top of a rich event backdrop)*