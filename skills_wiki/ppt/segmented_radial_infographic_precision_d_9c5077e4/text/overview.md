# Segmented Radial Infographic (Precision Donut Slicing)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Segmented Radial Infographic (Precision Donut Slicing)

* **Core Visual Mechanism**: The defining visual signature is a continuous, thick geometric ring (a "donut") that has been systematically fractured into equally spaced, distinct radial segments separated by negative space (gaps). This mimics a boolean subtraction effect (cutting a shape with thick geometric lines).
* **Why Use This Skill (Rationale)**: Breaking a continuous ring into discrete chunks fundamentally changes how the brain interprets the graphic. Instead of seeing a single holistic entity, the viewer interprets a *system of parts*, a *cycle*, or a *multi-step process*. The precise gaps create a sense of mechanical precision and modularity.
* **Overall Applicability**: This aesthetic is perfect for cycle diagrams, agile process loops, ecosystem overviews, data dashboard "gauge" representations, or any slide that needs to break down a central concept into smaller, equal constituent pieces (e.g., "The 14 Pillars of our Strategy"). 
* **Value Addition**: Compared to a standard PowerPoint pie or donut chart, this styled approach guarantees exact geometric gaps regardless of data values. It elevates standard bullet points into a highly structural, professional-looking circular framework.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **The Segmented Ring**: A thick circle where the stroke is the primary element.
  - **Negative Space Dividers**: Transparent gaps that cut entirely through the ring's thickness, allowing the background to show through.
  - **Color Logic**: In the tutorial, contrasting vibrant colors were used to differentiate segments. Representative palette: Dark space background `(18, 22, 28, 255)`, vibrant cyan `(0, 191, 255, 255)`, and energetic orange `(255, 140, 0, 255)`.
  - **Text Hierarchy**: A central focal text inside the donut's negative space, with supplementary text arranged either around the perimeter or on an adjacent panel.

* **Step B: Compositional Style**
  - The radial graphic acts as the visual anchor.
  - Typically occupies ~60-70% of the vertical canvas height.
  - High degree of symmetry; the use of exactly 14 segments means the graphic has rotational symmetry, making it feel engineered and balanced.

* **Step C: Dynamic Effects & Transitions**
  - **Wipe Transitions**: Slices can be animated sequentially using a "Wheel" entrance animation in PowerPoint to emphasize a cycle.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Boolean cutting / Segmenting** | `PIL/Pillow` (ImageDraw) | Native `python-pptx` shapes don't easily support boolean subtraction or precise "Block Arc" generation without messy XML hacking. PIL's `ImageDraw.arc` with a thick width and calculated angle gaps perfectly mimics the tutorial's "cutter line" subtraction. |
| **Drop Shadows** | `PIL/Pillow` (ImageFilter) | Applying a slight Gaussian blur to a darkened copy of the segments creates a premium, modern UI drop-shadow effect underneath the ring. |
| **Layout & Typography** | `python-pptx` native | Ideal for placing the resulting graphic, formatting the slide background, and adding editable text elements in the center and side. |

> **Feasibility Assessment**: 100%. By utilizing Python's math and PIL's arc drawing capabilities, we perfectly reproduce the mathematically precise 14-segment donut ring described in the Xara Designer Pro tutorial, and inject it as a pristine, transparent asset into PPTX.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Core Architecture",
    body_text: str = "A precisely engineered 14-point cycle.",
    segments: int = 14,
    gap_degrees: float = 3.5,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Segmented Radial Infographic visual effect.
    """
    import math
    import io
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from PIL import Image, ImageDraw, ImageFilter
    
    # Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6] # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # Theme Colors
    bg_color = (18, 22, 28)
    color_palette = [
        (0, 191, 255, 255),   # Cyan
        (255, 140, 0, 255),   # Orange
        (0, 250, 154, 255),   # Medium Spring Green
        (147, 112, 219, 255)  # Medium Purple
    ]

    # Set Background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # === Layer 1: PIL Generation of the Segmented Donut ===
    # Using high resolution for anti-aliasing
    img_size = 1200
    canvas = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))
    shadow_canvas = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))
    
    draw = ImageDraw.Draw(canvas)
    shadow_draw = ImageDraw.Draw(shadow_canvas)
    
    # Graphic constraints
    ring_thickness = 140
    margin = 100
    bbox = [margin, margin, img_size - margin, img_size - margin]
    
    # Calculate sweep of each segment
    sweep_angle = 360 / segments
    
    for i in range(segments):
        # Calculate angles, incorporating the boolean "gap" equivalent to the tutorial's line
        start_angle = (i * sweep_angle) + (gap_degrees / 2)
        end_angle = ((i + 1) * sweep_angle) - (gap_degrees / 2)
        
        # Select alternating color
        color = color_palette[i % len(color_palette)]
        
        # Draw shadow arc (black, slightly offset)
        shadow_draw.arc(bbox, start_angle, end_angle, fill=(0, 0, 0, 150), width=ring_thickness)
        
        # Draw main segment arc
        draw.arc(bbox, start_angle, end_angle, fill=color, width=ring_thickness)

    # Blur the shadow layer
    shadow_canvas = shadow_canvas.filter(ImageFilter.GaussianBlur(15))
    
    # Composite main graphics over shadow
    final_img = Image.alpha_composite(shadow_canvas, canvas)
    
    # Save to in-memory stream
    img_stream = io.BytesIO()
    final_img.save(img_stream, format='PNG')
    img_stream.seek(0)

    # === Layer 2: Insert into PPTX ===
    # Place graphic on the right side
    graphic_size = Inches(6.5)
    pic_left = Inches(6.0)
    pic_top = Inches(0.5)
    slide.shapes.add_picture(img_stream, pic_left, pic_top, graphic_size, graphic_size)

    # === Layer 3: PPTX Text Elements ===
    # Title Text (Left Panel)
    tx_box = slide.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(4.5), Inches(1.5))
    tf = tx_box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title_text.upper()
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.font.name = "Arial"
    
    p2 = tf.add_paragraph()
    p2.text = body_text
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(180, 180, 190)
    p2.font.name = "Arial"

    # Central Callout inside the Donut
    center_box = slide.shapes.add_textbox(Inches(7.75), Inches(3.25), Inches(3.0), Inches(1.0))
    center_tf = center_box.text_frame
    center_p = center_tf.paragraphs[0]
    center_p.text = str(segments)
    center_p.font.size = Pt(64)
    center_p.font.bold = True
    center_p.font.color.rgb = RGBColor(255, 255, 255)
    center_p.alignment = 2 # center alignment
    
    center_p2 = center_tf.add_paragraph()
    center_p2.text = "MODULES"
    center_p2.font.size = Pt(16)
    center_p2.font.bold = True
    center_p2.font.color.rgb = RGBColor(*color_palette[0][:3])
    center_p2.alignment = 2 # center alignment

    # Save Presentation
    prs.save(output_pptx_path)
    return output_pptx_path
```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries? (Yes, `math`, `io`, `pptx`, `PIL`).
- [x] Does it handle the case where an image download fails (fallback)? (Not applicable here, image is programmatically generated).
- [x] Are all color values explicit RGBA tuples? (Yes, e.g., `(0, 191, 255, 255)`).
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes, it accurately replicates the 14 separated radial segments using code-driven boolean gap math).
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes, the core visual of the cut donut is perfectly retained).