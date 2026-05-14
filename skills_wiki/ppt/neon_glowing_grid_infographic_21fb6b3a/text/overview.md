# Neon Glowing Grid Infographic

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Neon Glowing Grid Infographic

* **Core Visual Mechanism**: A 10x10 circular matrix (bubble chart) acting as a spatial representation of a percentage, paired with massive, high-contrast typography. The design heavily utilizes a "dark mode / neon" aesthetic, featuring intense bright accents against a near-black background, further elevated by volumetric, soft-blurred "glowing orbs" floating behind the text.
* **Why Use This Skill (Rationale)**: Abstract percentages (like "75%") often fail to carry emotional weight. A 100-dot grid gives the audience a tangible, spatial sense of the proportion. The dark background mixed with neon glowing accents directs the viewer's eye exactly where it needs to go while looking ultra-modern and tech-forward. 
* **Overall Applicability**: Perfect for data visualization slides, hero metrics in pitch decks, technology & AI presentations, or dashboard-style summary slides.
* **Value Addition**: It translates a generic bullet point into a compelling visual set-piece. The layered background glows create a sense of depth (Z-axis), breaking the standard flat PowerPoint look.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Color Logic**: 
    * Background: Very Dark Olive/Near Black `(25, 34, 13)`
    * Neon Accent: Bright Lime/Cyan `(188, 255, 1)`
    * Muted Fill: Dark Green `(56, 80, 0)`
  * **Text Hierarchy**: 
    * Primary Value: Massive font (~140pt), bold. The `%` symbol has a customized treatment (dark fill with neon stroke) to visually separate it from the primary integer.
    * Subtitle: Small (~16pt), all-caps, tracking/spaced out, anchored with a heavy neon underline.
  * **Graphic Elements**: 10x10 grid of perfect circles. Filled circles represent the active percentage, while the remaining circles default to a dark fill with a neon outline.

* **Step B: Compositional Style**
  * **Layout**: ~40/60 vertical split. The left 40% holds the typographic elements, strongly left-aligned to a grid guide. The right 60% holds the matrix, vertically and horizontally centered within its own bounding box.
  * **Depth/Z-Index**: Background Layer (Solid Dark) -> Effects Layer (Fuzzy glowing blobs) -> Content Layer (Text and Grid).

* **Step C: Dynamic Effects & Transitions**
  * *Video implementation relies on cascading "Zoom" entrance animations for the dots (0.05s delay between each) and a masked "Fly In" for the text.* (Our code will generate the exact end-state composition).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Soft Glowing Background Orbs** | `PIL/Pillow` (GaussianBlur) | `python-pptx` cannot natively draw and heavy-blur radial gradients. PIL easily generates an alpha-transparent glowing sphere PNG. |
| **Percentage Value Matrix** | `python-pptx` natively | Standard shape generation (`msoShapeOval`) combined in a math loop perfectly aligns the circles. |
| **Text Outline / Stroke** | `lxml` OOXML injection | `python-pptx` lacks a Pythonic API to add line strokes to text characters. Injecting `<a:ln>` into `<a:rPr>` creates the exact hollow `%` effect. |

> **Feasibility Assessment**: 100% of the visual layout and style can be replicated in code. The 10x10 matrix math and text styling inject perfectly. The cascading animation requires PowerPoint UI tweaks, but the graphic composition will be pixel-perfect.

#### 3b. Complete Reproduction Code

```python
import os
import tempfile
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.oxml import OxmlElement
from PIL import Image, ImageDraw, ImageFilter

def _create_glow_orb(color_rgba, radius=150, blur_amount=80):
    """Generates a soft, glowing spherical PNG with alpha transparency."""
    # Create an image with padding to avoid clipping the blur
    size = (radius * 2) + (blur_amount * 4)
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center = size // 2
    # Draw solid circle
    draw.ellipse(
        [center - radius, center - radius, center + radius, center + radius],
        fill=color_rgba
    )
    # Apply heavy blur to create the fuzzy glow effect
    img = img.filter(ImageFilter.GaussianBlur(blur_amount))
    
    temp_path = tempfile.mktemp(suffix=".png")
    img.save(temp_path, format="PNG")
    return temp_path

def _add_text_outline(run, hex_color="BCFF01", width_pt=1.5):
    """Injects OOXML to add a stroke (outline) to a specific text run."""
    rPr = run._r.get_or_add_rPr()
    
    # Create outline element <a:ln>
    ln = OxmlElement('a:ln')
    ln.set('w', str(int(width_pt * 12700))) # Convert Pt to EMUs (1 pt = 12700 EMUs)
    
    # Set outline solid fill
    solidFill = OxmlElement('a:solidFill')
    srgbClr = OxmlElement('a:srgbClr')
    srgbClr.set('val', hex_color)
    solidFill.append(srgbClr)
    ln.append(solidFill)
    
    # Add to run properties
    rPr.append(ln)

def create_slide(
    output_pptx_path: str,
    title_text: str = "PERCENTAGE CHART",
    percentage: int = 75,
    bg_color: tuple = (25, 34, 13),      # Very dark green
    accent_color: tuple = (188, 255, 1), # Neon lime
    dark_fill: tuple = (56, 80, 0),      # Dark muted green
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Neon Glowing Grid Infographic.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank slide layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # === Layer 1: Background ===
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # === Layer 2: Glowing Atmospheric Orbs ===
    rgba_accent = (accent_color[0], accent_color[1], accent_color[2], 120)
    
    orb1_path = _create_glow_orb(rgba_accent, radius=180, blur_amount=90)
    orb2_path = _create_glow_orb(rgba_accent, radius=100, blur_amount=60)
    
    # Position orbs subtly behind the main focus areas
    slide.shapes.add_picture(orb1_path, Inches(1.0), Inches(4.5), Inches(5), Inches(5))
    slide.shapes.add_picture(orb2_path, Inches(3.5), Inches(1.0), Inches(3), Inches(3))

    # === Layer 3: Typography & Lines ===
    
    # 1. Subtitle Text
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(4), Inches(0.5))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(*accent_color)
    
    # 2. Subtitle Accent Line
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.85), Inches(1.7), Inches(2.5), Inches(0.04)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(*accent_color)
    line.line.fill.background()

    # 3. Main Percentage Value
    val_box = slide.shapes.add_textbox(Inches(0.6), Inches(2.8), Inches(4.5), Inches(2.5))
    val_tf = val_box.text_frame
    p_val = val_tf.paragraphs[0]
    
    # Integer part
    run_int = p_val.add_run()
    run_int.text = str(percentage)
    run_int.font.name = "Arial Black"
    run_int.font.size = Pt(130)
    run_int.font.bold = True
    run_int.font.color.rgb = RGBColor(*accent_color)
    
    # Percentage symbol part (Hollow / Neon Stroke)
    run_sym = p_val.add_run()
    run_sym.text = "%"
    run_sym.font.name = "Arial Black"
    run_sym.font.size = Pt(130)
    run_sym.font.bold = True
    run_sym.font.color.rgb = RGBColor(*dark_fill)
    
    # Apply custom XML to outline the % sign
    accent_hex = f"{accent_color[0]:02X}{accent_color[1]:02X}{accent_color[2]:02X}"
    _add_text_outline(run_sym, hex_color=accent_hex, width_pt=1.5)

    # === Layer 4: The 10x10 Grid Infographic ===
    
    grid_start_x = Inches(6.5)
    grid_start_y = Inches(1.25)
    dot_spacing = Inches(0.55)
    dot_size = Inches(0.42)
    
    # Ensure percentage is clamped between 0 and 100
    safe_percent = max(0, min(100, percentage))
    
    for row in range(10):
        for col in range(10):
            idx = (row * 10) + col
            
            x = grid_start_x + (col * dot_spacing)
            y = grid_start_y + (row * dot_spacing)
            
            oval = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, dot_size, dot_size)
            
            # Decide if circle is "filled" or "empty"
            if idx < safe_percent:
                # Active circle
                oval.fill.solid()
                oval.fill.fore_color.rgb = RGBColor(*accent_color)
                oval.line.fill.background() # No line
            else:
                # Inactive circle
                oval.fill.solid()
                oval.fill.fore_color.rgb = RGBColor(*dark_fill)
                oval.line.color.rgb = RGBColor(*accent_color)
                oval.line.width = Pt(1.5)

    # Cleanup temp image files
    try:
        os.remove(orb1_path)
        os.remove(orb2_path)
    except:
        pass

    prs.save(output_pptx_path)
    return output_pptx_path
```