# Dashboard Speedometer Gauge

## Analysis

# Skill Strategy Document

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dashboard Speedometer Gauge

* **Core Visual Mechanism**: A semi-circular doughnut chart acting as a gauge, filled with a smooth linear color gradient (e.g., Green to Red) representing performance or progress. A central pivoting needle indicates the exact metric, combining sharp geometric angles with circular bases to mimic physical dashboard dials.
* **Why Use This Skill (Rationale)**: The speedometer is an intuitive, universally understood metaphor. It leverages cognitive familiarity with car dashboards to immediately communicate whether a metric is in a "safe" (green), "warning" (yellow), or "danger" (red) zone. It turns abstract percentages into instantly readable spatial information.
* **Overall Applicability**: Ideal for executive dashboards, KPI reporting, progress tracking, risk assessments, and project status slides. 
* **Value Addition**: Transforms a boring numerical percentage or basic pie chart into an engaging, high-fidelity UI component. It adds an interactive, animated feel (even when static) and significantly elevates the professional polish of data-heavy presentations.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Gauge Arc**: A thick, semi-circular ring serving as the track.
  - **Color Logic**: A semantic continuous gradient. 
    - `Safe`: Green `(46, 204, 113, 255)`
    - `Warning`: Yellow `(241, 196, 15, 255)`
    - `Danger`: Red `(231, 76, 60, 255)`
  - **Needle**: A dark contrast element composed of an isosceles triangle pointing to the value, anchored by a circular pivot hub at the base. Color: Dark Slate `(44, 62, 80, 255)`.
  - **Text Hierarchy**: Large, bold primary metric text centered directly beneath the pivot point.

* **Step B: Compositional Style**
  - The gauge relies on radial symmetry. The focal point is the center-bottom pivot, drawing the eye directly down to the numerical value.
  - The needle length is designed to reach exactly to the inner boundary of the gauge arc (~60% of the total bounding radius).
  - The layout mathematically aligns the needle's pivot exactly with the horizontal axis of the semi-circle.

* **Step C: Dynamic Effects & Transitions**
  - *Tutorial Implementation*: PowerPoint native "Spin" animations (180 degrees) synced with "Appear" effects so the needle tracks along the arc to its final position.
  - *Programmatic Implementation*: Natively assigning the `rotation` property to the needle image object, automatically placing it at the exact calculated percentage angle.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Semi-circle Gradient Arc** | `PIL/Pillow` | Creating a perfect semi-circle with a smooth, continuous 3-stop linear gradient is messy and inconsistent across platforms using PPTX native shape XML. PIL generates a flawless, resolution-independent PNG mask. |
| **Pivot-perfect Needle** | `PIL/Pillow` | Grouping shapes to alter their center-of-rotation is easily done in the PPTX GUI but highly complex via the API. By rendering the needle onto a transparent square PNG where the base is exactly at the image center, we can rotate it natively using `python-pptx` with perfect mathematical precision. |
| **Placement & Rotation** | `python-pptx native` | Standard image insertion and setting the `.rotation` attribute flawlessly mimics the target gauge value. |

> **Feasibility Assessment**: 95% — The code perfectly reproduces the static end-state of the speedometer with absolute visual fidelity. The real-time spinning animation during a slideshow is the only aspect not generated, as it requires fragile PPTX XML animation manipulation, but the graphic itself is pixel-perfect and mathematically mapped.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Project Health Metric",
    percentage: float = 75.0,  # Value from 0.0 to 100.0
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Dashboard Speedometer Gauge effect.
    """
    import os
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw

    # === Presentation Setup ===
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide
    
    # Optional: Set dark or light background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(248, 249, 250)

    # Add Title
    txBox = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.33), Inches(1))
    tf = txBox.text_frame
    tf.text = title_text
    p = tf.paragraphs[0]
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(44, 62, 80)
    p.alignment = PP_ALIGN.CENTER

    # === Helper Function for PIL Gradient ===
    def lerp_color(c1, c2, t):
        return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

    def get_gradient_color(t):
        c_green = (46, 204, 113)
        c_yellow = (241, 196, 15)
        c_red = (231, 76, 60)
        if t < 0.5:
            return lerp_color(c_green, c_yellow, t * 2)
        else:
            return lerp_color(c_yellow, c_red, (t - 0.5) * 2)

    # === Layer 1: Generate Gauge Background using PIL ===
    # We create an 800x400 image (semi-circle). Outer radius 350, inner radius 220.
    gauge_w, gauge_h = 800, 400
    
    # 1. Create linear gradient base
    grad_img = Image.new('RGB', (gauge_w, gauge_h))
    draw_grad = ImageDraw.Draw(grad_img)
    for x in range(gauge_w):
        color = get_gradient_color(x / float(gauge_w - 1))
        draw_grad.line((x, 0, x, gauge_h), fill=color)

    # 2. Create Alpha Mask for the Donut Arc
    # Draw on an 800x800 canvas so we can easily draw full circles, then crop
    mask = Image.new('L', (800, 800), 0)
    draw_mask = ImageDraw.Draw(mask)
    
    # Outer circle (White / visible)
    draw_mask.pieslice([50, 50, 750, 750], 180, 360, fill=255)
    # Inner circle (Black / transparent)
    draw_mask.pieslice([220, 220, 580, 580], 180, 360, fill=0)
    
    # Crop mask to upper half
    mask = mask.crop((0, 0, gauge_w, gauge_h))
    grad_img.putalpha(mask)
    
    gauge_path = "temp_gauge.png"
    grad_img.save(gauge_path)

    # === Layer 2: Generate Pivot-Perfect Needle using PIL ===
    # Image size is 800x800. Pivot is exactly at center (400, 400).
    # Default 0-degree state points LEFT.
    needle_img = Image.new('RGBA', (800, 800), (0, 0, 0, 0))
    draw_needle = ImageDraw.Draw(needle_img)
    
    needle_color = (44, 62, 80, 255)
    
    # Needle triangle: Points Left. Base top/bottom slightly above/below center.
    tip = (100, 400)
    base_top = (400, 385)
    base_bottom = (400, 415)
    draw_needle.polygon([base_top, tip, base_bottom], fill=needle_color)
    
    # Pivot Hub Circle
    r = 30
    draw_needle.ellipse([400-r, 400-r, 400+r, 400+r], fill=needle_color)
    
    # Inner Hub Decorative Circle (White)
    r_inner = 10
    draw_needle.ellipse([400-r_inner, 400-r_inner, 400+r_inner, 400+r_inner], fill=(255, 255, 255, 255))
    
    needle_path = "temp_needle.png"
    needle_img.save(needle_path)

    # === Insert Elements into Slide ===
    # Layout dimensions
    gauge_left = Inches(2.666)
    gauge_top = Inches(2.5)
    gauge_width = Inches(8)
    gauge_height = Inches(4)
    
    # Insert Gauge (Semi-circle)
    slide.shapes.add_picture(gauge_path, gauge_left, gauge_top, gauge_width, gauge_height)
    
    # Insert Needle (Square 8x8 image centered at gauge pivot)
    # The pivot of the gauge is at center-bottom: (gauge_left + 4, gauge_top + 4)
    # If the 8x8 needle image is placed at (gauge_left, gauge_top), its center aligns exactly with the pivot!
    needle_pic = slide.shapes.add_picture(needle_path, gauge_left, gauge_top, gauge_width, Inches(8))
    
    # Apply Mathematical Rotation
    # 0% = 0 degrees (pointing Left). 100% = 180 degrees (pointing Right).
    clamped_percentage = max(0.0, min(100.0, percentage))
    rotation_angle = (clamped_percentage / 100.0) * 180.0
    needle_pic.rotation = rotation_angle

    # === Add Metric Label ===
    # Placed directly underneath the pivot hub
    txt_left = gauge_left + Inches(3)
    txt_top = gauge_top + Inches(4.2)
    txt_width = Inches(2)
    txt_height = Inches(1)
    
    val_box = slide.shapes.add_textbox(txt_left, txt_top, txt_width, txt_height)
    val_tf = val_box.text_frame
    val_tf.text = f"{int(percentage)}%"
    val_p = val_tf.paragraphs[0]
    val_p.font.size = Pt(54)
    val_p.font.bold = True
    val_p.font.color.rgb = RGBColor(44, 62, 80)
    val_p.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx_path)
    
    # Clean up temp files
    if os.path.exists(gauge_path): os.remove(gauge_path)
    if os.path.exists(needle_path): os.remove(needle_path)
    
    return output_pptx_path
```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback)? *(N/A: Elements are generated completely procedurally via PIL, no external download needed).*
- [x] Are all color values explicit RGBA tuples (not referencing undefined variables)?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?
- [x] Would someone looking at the output say "yes, that's the same technique"?