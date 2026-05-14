# Radial Burst Metric Visualization

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Radial Burst Metric Visualization

* **Core Visual Mechanism**: This style relies on **concentric geometric layering** combined with a **polar/radial scatter effect**. The focal point is a central metric anchored by a thick, highly saturated circular ring. Radiating outward from this center is a series of varying-length lines (like a sunburst or circular bar chart) overlaid on faint concentric wireframe circles. This mimics a sophisticated data visualization dashboard.
* **Why Use This Skill (Rationale)**: The circular, radiating nature inherently draws the viewer's eye directly to the center, making it the ultimate pattern for highlighting a single, highly important metric. The varying lengths of the radial lines create a subconscious feeling of complex data, "impact," or "reach" radiating outward.
* **Overall Applicability**: Perfect for "Hero" metric slides, global impact statistics, annual report highlights, and tech or data-centric product presentations.
* **Value Addition**: Transforms a boring "Big Number" slide into an intricate, sophisticated piece of infographic art that feels data-driven and dynamic without overwhelming the viewer.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **The Anchor**: A central circle with a thick stroke (accent color).
  - **The Metric**: Large, bold typography placed exactly at the geometric center.
  - **The Grid**: 5 to 7 faint, evenly spaced concentric circles forming a radar-like background.
  - **The Data Spokes**: Straight lines radiating outward from the center. Their outer lengths vary to simulate data points or sound waves.
  - **Color Logic**: "Dark Mode High Contrast."
    - Background: Deep Navy/Charcoal `(25, 30, 45, 255)`
    - Accent (The Ring): Vibrant Orange/Red `(232, 93, 56, 255)`
    - Wireframes & Spokes: Faint Light Blue/Gray `(150, 160, 180, 255)` with transparency.
    - Typography: Pure White `(255, 255, 255, 255)` and Faint Gray.

* **Step B: Compositional Style**
  - **Vertical Axis Symmetry**: The entire composition is perfectly center-aligned vertically.
  - **Proportions**:
    - The graphic occupies the top 60% of the slide.
    - The text block (Title, Subtitle, Body) occupies the bottom 40%.
    - The central metric circle diameter is roughly 15-20% of the slide height.

* **Step C: Dynamic Effects & Transitions**
  - *Ideal Animation*: A "Wheel" entrance animation for the radial lines and rings, paired with a "Zoom" entrance for the central number. (This must be applied natively in PowerPoint after generation).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Background & Layout** | `python-pptx` native | A full-screen rectangle provides a reliable dark canvas. |
| **Concentric Wireframes** | `python-pptx` native | Native oval shapes with no fill and thin lines scale perfectly as vectors without pixelation. |
| **Radial Burst Lines** | `python-pptx` native + Trigonometry (`math`) | While Illustrator uses a scatter brush, we can recreate this natively in PPTX by mathematically calculating start/end coordinates $(x,y)$ using $\sin$ and $\cos$ to draw individual connector lines. This ensures the output is purely vector, editable, and razor-sharp. |
| **Typography** | `python-pptx` native | Standard centered text frames for precise control over typography hierarchy. |

> **Feasibility Assessment**: 100%. Because this design relies entirely on precise geometric primitives (lines, circles, text), Python can recreate the exact aesthetic natively in PowerPoint without needing to rasterize anything into an image.

#### 3b. Complete Reproduction Code

```python
import math
import random
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN

def create_slide(
    output_pptx_path: str,
    main_number: str = "3.9",
    metric_label: str = "MILLION",
    title_text: str = "Educational Pull",
    subtitle_text: str = "Knowledge for Global Impact",
    body_text: str = "Education participants from 88 different countries travel 3.9 million miles annually to receive the knowledge that can amplify their leadership potential and fuel their impact on the world.",
    bg_color: tuple = (25, 30, 45),
    accent_color: tuple = (232, 93, 56),
    line_color: tuple = (100, 110, 130)
) -> str:
    """
    Create a PPTX file reproducing the Radial Burst Metric Visualization.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Dark Background ===
    bg_shape = slide.shapes.add_shape(
        1, # MSO_SHAPE.RECTANGLE
        0, 0, prs.slide_width, prs.slide_height
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RGBColor(*bg_color)
    bg_shape.line.fill.background()

    # Define Center Point for Graphic (Top 55% of the slide)
    cx = prs.slide_width / 2
    cy = prs.slide_height * 0.42

    # === Layer 2: Concentric Radar Wireframes ===
    num_circles = 6
    max_radius = Inches(2.8)
    radius_step = max_radius / num_circles

    for i in range(1, num_circles + 1):
        r = radius_step * i
        circle = slide.shapes.add_shape(
            9, # MSO_SHAPE.OVAL
            cx - r, cy - r, r * 2, r * 2
        )
        circle.fill.background() # No fill
        circle.line.color.rgb = RGBColor(*line_color)
        circle.line.width = Pt(0.5)

    # === Layer 3: Radial Data Spokes ===
    # Using trigonometry to draw lines radiating from an inner ring to a variable outer ring
    num_spokes = 90 # Density of the burst
    inner_radius = Inches(1.0)
    base_outer_radius = Inches(1.5)
    
    for i in range(num_spokes):
        angle_deg = i * (360 / num_spokes)
        angle_rad = math.radians(angle_deg)
        
        # Calculate start point (on the inner circle)
        start_x = cx + inner_radius * math.cos(angle_rad)
        start_y = cy + inner_radius * math.sin(angle_rad)
        
        # Calculate dynamic end point (creating the data visualization feel)
        # Combine a sine wave for pattern + random noise for organic variation
        wave_variation = math.sin(angle_rad * 4) * Inches(0.4) 
        noise = random.uniform(0, Inches(0.8))
        dynamic_outer_radius = base_outer_radius + wave_variation + noise
        
        # Cap the max radius so it doesn't break the outer concentric circle
        dynamic_outer_radius = min(dynamic_outer_radius, max_radius - Inches(0.1))
        
        end_x = cx + dynamic_outer_radius * math.cos(angle_rad)
        end_y = cy + dynamic_outer_radius * math.sin(angle_rad)
        
        # Draw the line
        line = slide.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT, start_x, start_y, end_x, end_y
        )
        line.line.color.rgb = RGBColor(*line_color)
        line.line.width = Pt(1.0)

    # === Layer 4: Central Focal Anchor ===
    # 1. Inner dark mask circle to ensure lines don't overlap inside
    mask_radius = Inches(1.0)
    mask_circle = slide.shapes.add_shape(
        9, cx - mask_radius, cy - mask_radius, mask_radius * 2, mask_radius * 2
    )
    mask_circle.fill.solid()
    mask_circle.fill.fore_color.rgb = RGBColor(*bg_color)
    mask_circle.line.fill.background()

    # 2. Thick Accent Ring
    accent_radius = Inches(1.1)
    accent_ring = slide.shapes.add_shape(
        9, cx - accent_radius, cy - accent_radius, accent_radius * 2, accent_radius * 2
    )
    accent_ring.fill.background()
    accent_ring.line.color.rgb = RGBColor(*accent_color)
    accent_ring.line.width = Pt(4.5) # Thick stroke

    # === Layer 5: Typography ===
    # 1. Central Metric Number
    metric_box = slide.shapes.add_textbox(cx - Inches(1.5), cy - Inches(0.6), Inches(3), Inches(1))
    tf = metric_box.text_frame
    tf.text = main_number
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].runs[0].font.size = Pt(44)
    tf.paragraphs[0].runs[0].font.bold = True
    tf.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    # 2. Central Metric Label
    label_box = slide.shapes.add_textbox(cx - Inches(1.5), cy + Inches(0.1), Inches(3), Inches(0.5))
    tf2 = label_box.text_frame
    tf2.text = metric_label
    tf2.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf2.paragraphs[0].runs[0].font.size = Pt(12)
    tf2.paragraphs[0].runs[0].font.bold = True
    tf2.paragraphs[0].runs[0].font.color.rgb = RGBColor(*accent_color)

    # 3. Main Title (Below Graphic)
    text_y_start = prs.slide_height * 0.75
    title_box = slide.shapes.add_textbox(cx - Inches(4), text_y_start, Inches(8), Inches(0.5))
    tf3 = title_box.text_frame
    tf3.text = title_text
    tf3.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf3.paragraphs[0].runs[0].font.size = Pt(28)
    tf3.paragraphs[0].runs[0].font.bold = True
    tf3.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    # 4. Subtitle
    sub_box = slide.shapes.add_textbox(cx - Inches(4), text_y_start + Inches(0.5), Inches(8), Inches(0.4))
    tf4 = sub_box.text_frame
    tf4.text = subtitle_text
    tf4.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf4.paragraphs[0].runs[0].font.size = Pt(16)
    tf4.paragraphs[0].runs[0].font.color.rgb = RGBColor(*line_color) # use same gray as lines

    # 5. Body Text
    body_box = slide.shapes.add_textbox(cx - Inches(4), text_y_start + Inches(1.0), Inches(8), Inches(1.0))
    tf5 = body_box.text_frame
    tf5.text = body_text
    tf5.word_wrap = True
    tf5.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf5.paragraphs[0].runs[0].font.size = Pt(11)
    tf5.paragraphs[0].runs[0].font.color.rgb = RGBColor(180, 180, 190)

    prs.save(output_pptx_path)
    return output_pptx_path
```