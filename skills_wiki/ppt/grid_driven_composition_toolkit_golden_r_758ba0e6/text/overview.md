# Grid-Driven Composition Toolkit (Golden Ratio, Rule of Thirds, Symmetry)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Grid-Driven Composition Toolkit (Golden Ratio, Rule of Thirds, Symmetry)

* **Core Visual Mechanism**: Using strict geometric and mathematical grids to dictate the placement of images, text, and visual weight. Rather than arbitrary placement, elements are snapped to specific proportional lines: 
  1. **Golden Ratio (1:1.618)** for organic, highly balanced asymmetry.
  2. **Rule of Thirds (3x3 Grid)** for dynamic tension and perfect focal points.
  3. **Symmetry (1:1)** for formal, authoritative, and structured presentation.
* **Why Use This Skill (Rationale)**: The human brain intuitively finds geometric order pleasing. Grids eliminate "floating" elements, reducing cognitive load and guiding the viewer’s eye seamlessly from the dominant visual (anchor) to the core message (text).
* **Overall Applicability**: 
  - **Golden Ratio**: Premium product showcases, editorial-style photo slides, and portfolio pieces.
  - **Rule of Thirds**: Full-bleed background images with vast "negative space" (skies, oceans, minimalist textures) where text needs a distinct resting place.
  - **Symmetry**: Comparison slides, pros/cons, balanced dashboards, and classic title slides.
* **Value Addition**: Transforms a standard PowerPoint slide into an editorial, magazine-quality layout. It provides a foolproof framework for layout decisions, ensuring every slide feels intentionally designed.

---

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Imagery**: High-quality, context-relevant photos that inherently possess negative space.
  - **Grid Guides (Educational/Aesthetic)**: Sometimes rendered as ultra-thin, low-opacity lines (e.g., `(255, 255, 255, 100)`) to add a "technical" or "blueprint" aesthetic to the slide.
  - **Color Logic**: Minimalist backgrounds to support the grids. E.g., Charcoal background `(28, 30, 33, 255)` with clean White `(255, 255, 255, 255)` text, or a warm Gold accent `(212, 175, 55, 255)`.

* **Step B: Compositional Style**
  - **Golden Ratio Layout**: The slide width (13.33") is divided by 1.618. The dominant side takes ~8.24 inches (61.8%), the subordinate side takes ~5.09 inches (38.2%).
  - **Rule of Thirds Layout**: Canvas is divided into 9 equal rectangles. Key elements (titles, product icons) are centered exactly on one of the 4 interior intersecting nodes.
  - **Symmetric Layout**: Perfect 50/50 split down the middle (6.66" per side). Equal padding and text alignment on both halves.

* **Step C: Dynamic Effects & Transitions**
  - **Animation**: Elements usually fade in or slide in *along* the grid lines (e.g., text wiping in from the exact Rule of Thirds vertical boundary).

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Precise Spatial Splitting** | `python-pptx` natively | Standard API `Inches` allows for mathematically perfect absolute positioning based on Phi (1.618) and Thirds. |
| **Grid Overlays** | `python-pptx` connectors | `add_connector` is the perfect tool for rendering the technical "blueprint" grid lines shown in the video. |
| **Image Handling** | `PIL/Pillow` & `urllib` | Dynamically generating fallback images if downloads fail, and handling exact crop dimensions. |

> **Feasibility Assessment**: 100% — Grid mathematics are perfectly reproducible in code using absolute coordinates. The script below will generate a 3-slide presentation, demonstrating exactly how to execute all three grids with structural wireframes visible.

#### 3b. Complete Reproduction Code

```python
import os
import urllib.request
import io
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_CONNECTOR

def create_slide(
    output_pptx_path: str,
    title_text: str = "Grid Systems",
    body_text: str = "Upgrade your layouts using geometric grids.",
    **kwargs
) -> str:
    """
    Create a PPTX file reproducing 3 Grid Layout Styles: Golden Ratio, Rule of Thirds, and Symmetry.
    Includes visual grid overlay lines to demonstrate the aesthetic.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Golden Ratio Constant
    PHI = 1.61803398875
    W = 13.333
    H = 7.5

    def get_image(width_px, height_px, seed_id):
        """Helper to fetch an image or generate a solid fallback via PIL."""
        url = f"https://picsum.photos/seed/{seed_id}/{int(width_px)}/{int(height_px)}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                image_data = response.read()
            return io.BytesIO(image_data)
        except Exception:
            # Fallback: create a grey image with PIL
            img = Image.new('RGB', (int(width_px), int(height_px)), color=(100, 110, 120))
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            return img_byte_arr

    def add_gridline(slide, x1, y1, x2, y2):
        """Helper to draw thin white architectural grid lines."""
        connector = slide.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2)
        )
        connector.line.color.rgb = RGBColor(255, 255, 255)
        connector.line.width = Pt(0.75)
        # We can't do native transparency on lines easily without lxml, so we rely on thinness

    def format_text(shape, font_size=44, bold=True):
        for paragraph in shape.text_frame.paragraphs:
            for run in paragraph.runs:
                run.font.size = Pt(font_size)
                run.font.bold = bold
                run.font.color.rgb = RGBColor(41, 50, 65) # Dark Charcoal

    # ========================================================
    # SLIDE 1: GOLDEN RATIO (61.8% / 38.2% Split)
    # ========================================================
    slide_golden = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Calculate widths based on Golden Ratio
    w_golden_large = W / PHI       # ~8.24 inches
    w_golden_small = W - w_golden_large # ~5.09 inches
    
    # Add Image on the left (the 61.8% chunk)
    img_stream = get_image(w_golden_large * 100, H * 100, "golden")
    slide_golden.shapes.add_picture(img_stream, 0, 0, Inches(w_golden_large), Inches(H))
    
    # Add Text on the right (the 38.2% chunk)
    tx_box = slide_golden.shapes.add_textbox(
        Inches(w_golden_large + 0.5), Inches(2.5), Inches(w_golden_small - 1), Inches(3)
    )
    tf = tx_box.text_frame
    tf.word_wrap = True
    p = tf.add_paragraph()
    p.text = "01. Golden Ratio"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor(28, 30, 33)
    
    p2 = tf.add_paragraph()
    p2.text = "Applied the 1:1.618 ratio to dictate the boundary between imagery and typography, ensuring organic visual harmony."
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(100, 100, 100)
    
    # Draw Gridline
    add_gridline(slide_golden, w_golden_large, 0, w_golden_large, H)

    # ========================================================
    # SLIDE 2: RULE OF THIRDS (3x3 Grid)
    # ========================================================
    slide_thirds = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Background Image (Full slide)
    img_stream2 = get_image(W * 100, H * 100, "thirds")
    slide_thirds.shapes.add_picture(img_stream2, 0, 0, Inches(W), Inches(H))
    
    # Grid lines for aesthetic/blueprint look
    w_third = W / 3.0
    h_third = H / 3.0
    add_gridline(slide_thirds, w_third, 0, w_third, H)
    add_gridline(slide_thirds, w_third * 2, 0, w_third * 2, H)
    add_gridline(slide_thirds, 0, h_third, W, h_third)
    add_gridline(slide_thirds, 0, h_third * 2, W, h_third * 2)
    
    # Text Box positioned EXACTLY at the Top-Left focal node
    # W/3 is 4.44, H/3 is 2.5
    tx_box2 = slide_thirds.shapes.add_textbox(
        Inches(w_third + 0.2), Inches(h_third - 1.0), Inches(w_third * 2), Inches(1.5)
    )
    tf2 = tx_box2.text_frame
    p3 = tf2.add_paragraph()
    p3.text = "02. Rule of Thirds"
    p3.font.size = Pt(48)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(255, 255, 255) # White over image
    
    p4 = tf2.add_paragraph()
    p4.text = "Placing key elements at the intersection of a 3x3 grid creates dynamic tension."
    p4.font.size = Pt(18)
    p4.font.color.rgb = RGBColor(240, 240, 240)


    # ========================================================
    # SLIDE 3: SYMMETRY (1:1 Split)
    # ========================================================
    slide_sym = prs.slides.add_slide(prs.slide_layouts[6])
    
    w_half = W / 2.0
    
    # Left Half: Solid Color or Image
    img_stream3 = get_image(w_half * 100, H * 100, "sym")
    slide_sym.shapes.add_picture(img_stream3, 0, 0, Inches(w_half), Inches(H))
    
    # Right Half: Symmetrical Text
    tx_box3 = slide_sym.shapes.add_textbox(
        Inches(w_half + 0.5), Inches(3.0), Inches(w_half - 1.0), Inches(2.0)
    )
    tf3 = tx_box3.text_frame
    tf3.word_wrap = True
    
    p5 = tf3.add_paragraph()
    p5.alignment = PP_ALIGN.CENTER
    p5.text = "03. Symmetry"
    p5.font.size = Pt(40)
    p5.font.bold = True
    p5.font.color.rgb = RGBColor(28, 30, 33)
    
    p6 = tf3.add_paragraph()
    p6.alignment = PP_ALIGN.CENTER
    p6.text = "A perfect 50/50 split projects authority, stability, and extreme structural balance."
    p6.font.size = Pt(16)
    p6.font.color.rgb = RGBColor(100, 100, 100)
    
    # Draw Gridline straight down the middle
    add_gridline(slide_sym, w_half, 0, w_half, H)
    add_gridline(slide_sym, w_half - 0.2, H/2.0, w_half + 0.2, H/2.0) # Mini crosshair

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
```