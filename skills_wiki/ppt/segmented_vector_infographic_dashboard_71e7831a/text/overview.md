# Segmented Vector Infographic Dashboard

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Segmented Vector Infographic Dashboard

* **Core Visual Mechanism**: A clean, vector-based data visualization layout characterized by custom geometric charts (segmented radial rings, filled pyramid/triangle charts, and hollow donut rings) using a cohesive pastel-tech color palette. The contrast between a bold, solid-color title panel on the left and a clean white data canvas on the right creates a highly legible, modern dashboard aesthetic.
* **Why Use This Skill (Rationale)**: Native PowerPoint charts often look rigid, generic, or overly complex. By constructing bespoke visual representations of percentages using custom geometry (freeform shapes and segmented rings), the data is perceived not just as numbers, but as premium editorial content. The "step-by-step" filled geometric areas inherently convey progress and proportion more intuitively than standard bar charts.
* **Overall Applicability**: Perfect for data dashboard slides, executive summaries, marketing KPI reports, portfolio highlight pages, or cover slides for analytical presentations.
* **Value Addition**: Transforms dry statistics into high-end "infographic poster" quality visuals. It elevates the perceived professionalism of the deck, showing a level of design polish typically associated with Adobe Illustrator exports, while remaining entirely editable and reproducible within the presentation's code logic.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Dichotomous Layout**: 1/3 solid accent color (left), 2/3 clean white (right).
  - **Color Logic**:
    - **Primary Purple** (Left Panel & Chart Accent): `(111, 89, 209, 255)`
    - **Success Green** (Chart Accent): `(134, 197, 139, 255)`
    - **Tech Blue** (Chart Accent): `(121, 142, 229, 255)`
    - **Track Gray** (Chart Backgrounds): `(235, 235, 235, 255)`
    - **Text Color**: Dark slate `(50, 50, 60, 255)` for readability on white.
  - **Text Hierarchy**: Massive bold sans-serif titles on the left, clear numerical percentage callouts (bold) sitting inside or directly below their corresponding geometric chart.

* **Step B: Compositional Style**
  - The right panel acts as an independent canvas, divided into three horizontal zones for the three distinct chart types.
  - **Chart 1 (Top)**: Multi-layered segmented ring, dominating the upper quadrant, paired with a subtle dot legend.
  - **Chart 2 (Middle)**: Three aligned triangle pyramids, filled horizontally from the base.
  - **Chart 3 (Bottom)**: Three hollow donut rings with perfectly rounded caps and centered labels.

* **Step C: Dynamic Effects & Transitions**
  - *Setup*: The geometric progression (e.g., trapezoids scaling inside triangles) is achieved mathematically via Python logic to map data percentages to exact geometric coordinates.
  - *Animation (Manual addition)*: These elements pair perfectly with a "Wipe" from bottom (for pyramids) or "Wheel" (for circular charts).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Segmented Radial Rings** | PIL / Pillow | PPTX native arcs cannot easily be chopped into exact dashed segments with alternating gaps. PIL renders this perfectly as a crisp transparent PNG. |
| **Donut Charts with Round Caps** | PIL / Pillow | Native PPTX block arcs lack smooth rounded end-caps. Drawing paths with circular caps in PIL ensures a flawless vector-like aesthetic. |
| **Pyramid Area Charts** | `python-pptx` FreeformBuilder | Injecting custom polygon coordinates mathematically generates a perfect percentage-filled trapezoid inside a triangle. This remains natively rendering vector art in PPTX. |
| **Split Dashboard Layout** | `python-pptx` native | Standard rectangles and text boxes easily handle the 1/3 to 2/3 crisp structural divide. |

> **Feasibility Assessment**: 100% reproduction of the visual style. The code mathematically handles the geometric constraints (trapezoid slopes, arc radians) to precisely recreate the Adobe Illustrator infographic look entirely programmatically.

#### 3b. Complete Reproduction Code

```python
import math
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw

def _make_radial_segmented_img(vals, colors, size=800):
    """Generates a PIL image of segmented concentric rings."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    center = (size // 2, size // 2)
    radii = [320, 250, 180]  # Outer, Mid, Inner
    width = 45
    
    # Draw background tracks
    for r in radii:
        bbox = [center[0] - r, center[1] - r, center[0] + r, center[1] + r]
        draw.arc(bbox, 0, 360, fill=(235, 235, 235, 255), width=width)
        
    # Draw value arcs
    for i, (val, color) in enumerate(zip(vals, colors)):
        r = radii[i]
        bbox = [center[0] - r, center[1] - r, center[0] + r, center[1] + r]
        # Angles in PIL: 0 is 3 o'clock, 90 is 6 o'clock. We want to start at top (270)
        start_angle = 270
        end_angle = 270 + (val * 360)
        draw.arc(bbox, start_angle, end_angle, fill=color, width=width)
        
    # Cut segments with transparent/white lines originating from center
    for angle in range(0, 360, 8):
        rad = math.radians(angle)
        x1 = center[0] + 100 * math.cos(rad)
        y1 = center[1] + 100 * math.sin(rad)
        x2 = center[0] + 400 * math.cos(rad)
        y2 = center[1] + 400 * math.sin(rad)
        draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 255, 255), width=8)
        
    return img

def _make_donut_img(val, color, size=400):
    """Generates a PIL image of a donut chart with rounded caps."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    center = (size // 2, size // 2)
    r = 150
    width = 35
    bbox = [center[0] - r, center[1] - r, center[0] + r, center[1] + r]
    
    # Background track
    draw.arc(bbox, 0, 360, fill=(235, 235, 235, 255), width=width)
    
    # Value arc
    start_angle = 270
    end_angle = 270 + (val * 360)
    draw.arc(bbox, start_angle, end_angle, fill=color, width=width)
    
    # Draw rounded caps
    def draw_cap(angle_deg):
        rad = math.radians(angle_deg)
        cx = center[0] + r * math.cos(rad)
        cy = center[1] + r * math.sin(rad)
        draw.ellipse([cx - width/2, cy - width/2, cx + width/2, cy + width/2], fill=color)
        
    draw_cap(start_angle)
    draw_cap(end_angle)
    
    return img

def _draw_filled_triangle(shapes, x, y, w, h, p, color_rgb):
    """Uses pptx FreeformBuilder to draw a background triangle and a percentage-filled foreground trapezoid."""
    bg_color = (235, 235, 235)
    
    # Emu conversion is required for exact Freeform points to avoid float issues
    def to_int(val): return int(val)
    
    # 1. Background Triangle
    bg_builder = shapes.build_freeform(to_int(x), to_int(y + h))
    bg_builder.add_line_segments([
        (to_int(x + w), to_int(y + h)),
        (to_int(x + w / 2), to_int(y)),
        (to_int(x), to_int(y + h))
    ])
    bg_shape = bg_builder.convert_to_shape()
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RGBColor(*bg_color)
    bg_shape.line.fill.solid()
    bg_shape.line.fill.fore_color.rgb = RGBColor(*bg_color)

    # 2. Foreground Trapezoid (Filled percentage from bottom)
    # The height scales linearly. The top width shrinks linearly.
    fg_builder = shapes.build_freeform(to_int(x), to_int(y + h))
    fg_builder.add_line_segments([
        (to_int(x + w), to_int(y + h)),
        (to_int(x + w - w * (1-p) / 2), to_int(y + h - p * h)),
        (to_int(x + w * (1-p) / 2), to_int(y + h - p * h)),
        (to_int(x), to_int(y + h))
    ])
    fg_shape = fg_builder.convert_to_shape()
    fg_shape.fill.solid()
    fg_shape.fill.fore_color.rgb = RGBColor(*color_rgb)
    fg_shape.line.fill.solid()
    fg_shape.line.fill.fore_color.rgb = RGBColor(*color_rgb)

def create_slide(
    output_pptx_path: str,
    title_text: str = "DATA\nVISUALIZATION",
    body_text: str = "Adobe Illustrator Tutorial\nVector Infographic Style",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Segmented Vector Infographic Dashboard style.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Core Palette
    COLOR_PANEL_BG = (111, 89, 209)
    COLOR_BLUE = (121, 142, 229, 255)
    COLOR_PURPLE = (156, 128, 230, 255)
    COLOR_GREEN = (134, 197, 139, 255)
    TEXT_DARK = RGBColor(50, 50, 60)
    
    # === Layer 1: Split Layout Background ===
    left_panel = slide.shapes.add_shape(
        1,  # msoShapeRectangle
        0, 0, Inches(4.5), prs.slide_height
    )
    left_panel.fill.solid()
    left_panel.fill.fore_color.rgb = RGBColor(*COLOR_PANEL_BG)
    left_panel.line.fill.background()

    # Title Text (Left Panel)
    tx_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.0), Inches(3.5), Inches(3))
    tf = tx_box.text_frame
    
    p = tf.add_paragraph()
    p.text = "STEP-BY-STEP"
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    p2 = tf.add_paragraph()
    p2.text = title_text
    p2.font.size = Pt(44)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(255, 255, 255)
    
    p3 = tf.add_paragraph()
    p3.text = "\n" + body_text
    p3.font.size = Pt(16)
    p3.font.color.rgb = RGBColor(220, 220, 235)


    # === Layer 2: Segmented Radial Chart (Top Right) ===
    # Colors mapped inside-out: Green, Purple, Blue
    r_img = _make_radial_segmented_img([0.45, 0.31, 0.15], [COLOR_GREEN, COLOR_PURPLE, COLOR_BLUE])
    stream_r = BytesIO()
    r_img.save(stream_r, format="PNG")
    stream_r.seek(0)
    
    slide.shapes.add_picture(stream_r, Inches(6.0), Inches(0.5), width=Inches(2.5), height=Inches(2.5))
    
    # Legend for Radial Chart
    leg_x, leg_y = Inches(8.7), Inches(1.0)
    leg_vals = ["15%", "31%", "45%"]
    leg_colors = [COLOR_BLUE, COLOR_PURPLE, COLOR_GREEN]
    for i, (val, clr) in enumerate(zip(leg_vals, leg_colors)):
        # Legend dot
        dot = slide.shapes.add_shape(9, leg_x, leg_y + Inches(i*0.4), Inches(0.15), Inches(0.15))
        dot.fill.solid()
        dot.fill.fore_color.rgb = RGBColor(clr[0], clr[1], clr[2])
        dot.line.fill.background()
        # Legend text
        tb = slide.shapes.add_textbox(leg_x + Inches(0.2), leg_y - Inches(0.05) + Inches(i*0.4), Inches(1), Inches(0.3))
        tb.text_frame.text = val
        tb.text_frame.paragraphs[0].font.size = Pt(14)
        tb.text_frame.paragraphs[0].font.bold = True
        tb.text_frame.paragraphs[0].font.color.rgb = TEXT_DARK


    # === Layer 3: Pyramid Area Charts (Middle Right) ===
    pyr_x_starts = [Inches(5.3), Inches(7.8), Inches(10.3)]
    pyr_y = Inches(3.2)
    pyr_w = Inches(1.6)
    pyr_h = Inches(1.4)
    pyr_vals = [0.70, 0.45, 0.80]
    pyr_colors = [(COLOR_PURPLE[0], COLOR_PURPLE[1], COLOR_PURPLE[2]), 
                  (COLOR_GREEN[0], COLOR_GREEN[1], COLOR_GREEN[2]), 
                  (COLOR_BLUE[0], COLOR_BLUE[1], COLOR_BLUE[2])]
    
    for i in range(3):
        # Draw Pyramid
        _draw_filled_triangle(slide.shapes, pyr_x_starts[i], pyr_y, pyr_w, pyr_h, pyr_vals[i], pyr_colors[i])
        
        # Draw Text below
        tb = slide.shapes.add_textbox(pyr_x_starts[i], pyr_y + pyr_h + Inches(0.1), pyr_w, Inches(0.4))
        p = tb.text_frame.add_paragraph()
        p.text = f"{int(pyr_vals[i]*100)}%"
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK


    # === Layer 4: Donut Charts (Bottom Right) ===
    don_y = Inches(5.4)
    don_vals = [0.35, 0.10, 0.20]
    
    for i in range(3):
        d_img = _make_donut_img(don_vals[i], pyr_colors[i] + (255,))
        stream_d = BytesIO()
        d_img.save(stream_d, format="PNG")
        stream_d.seek(0)
        
        # Center image horizontally with the pyramid above it
        don_x = pyr_x_starts[i] + (pyr_w / 2) - (Inches(1.5) / 2)
        slide.shapes.add_picture(stream_d, don_x, don_y, width=Inches(1.5), height=Inches(1.5))
        
        # Add center text
        tb = slide.shapes.add_textbox(don_x, don_y + Inches(0.45), Inches(1.5), Inches(0.5))
        p = tb.text_frame.add_paragraph()
        p.text = f"{int(don_vals[i]*100)}%"
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK

    prs.save(output_pptx_path)
    return output_pptx_path
```