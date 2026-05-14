# Vector Geometric Data Dashboard (Segmented Donuts & Filled Pyramids)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Vector Geometric Data Dashboard (Segmented Donuts & Filled Pyramids)

* **Core Visual Mechanism**: The design replaces standard, clunky Excel charts with sleek, geometric vector graphics. It relies on two primary visual metaphors:
  1. **Concentric Progress**: Using nested polar coordinates (donut charts) where the outermost ring is segmented (dashed) to represent tick marks or scale, while inner rings are solid progress bars.
  2. **Volumetric Fill**: Using isosceles triangles (pyramids) where the "fill" level visually corresponds to a percentage, acting as an area-based progress bar. 

* **Why Use This Skill (Rationale)**: Native PowerPoint charts often look overly corporate and uninspired. By constructing data visualizations out of raw geometric shapes (custom polygons and polar plots), the slide instantly feels like it was designed in Adobe Illustrator. The use of whitespace, strict alignment, and vibrant accents against a split-tone background creates high visual hierarchy and cognitive ease.

* **Overall Applicability**: Perfect for high-end corporate presentations, KPI dashboards, executive summaries, or product launch slides where data needs to look like a bespoke infographic rather than a pasted spreadsheet.

* **Value Addition**: Transforms dry numerical data into a visually stimulating poster-style infographic. It elevates the perceived production value of the deck, making the information feel curated, modern, and highly digestible.

---

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Color Logic**: 
    * Split Background: Deep Indigo `(122, 96, 224)` on the left, Pure White `(255, 255, 255)` on the right.
    * Data Palette: Vibrant but muted pastels. Pink-Red `(232, 139, 140)`, Mint Green `(121, 204, 158)`, Lavender Blue `(139, 122, 228)`, Deep Navy `(89, 101, 163)`.
    * Track/Background Colors for charts: Light Gray `(229, 229, 229)`.
  * **Text Hierarchy**: Massive, bold display typography for the title block (White). Large, bold geometric sans-serif numbers for the data points, with small subtle gray labels.
  * **Shapes**: Custom segmented arcs, smooth solid arcs, and geometrically clipped triangles.

* **Step B: Compositional Style**
  * **Layout**: 1/3 to 2/3 Vertical Split Layout. The dark left third acts as an anchor and title area. The white right two-thirds acts as a bright, clean canvas for the data.
  * **Spatial Balance**: The data is clustered into distinct "zones" (top right, middle, bottom row), providing a clear reading path from the complex nested donut down to the simple individual metrics.

* **Step C: Dynamic Effects & Transitions**
  * *Code capability*: The geometry is static but highly precise.
  * *Manual addition*: Adding PowerPoint's "Wipe" (from bottom) to the triangles and "Wheel" animation to the donut charts would beautifully complete the infographic reveal.

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

To achieve the "Illustrator" aesthetic without manual drawing, we combine native PPTX shapes with Python's premier plotting library:

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Segmented & Nested Donut Charts** | `matplotlib` rendered to transparent PNG | Natively calculating and perfectly spacing 24 dashed segments as individual PPTX shapes is prone to rendering glitches. `matplotlib` polar bar charts handle this mathematically perfectly and inject cleanly as transparent overlays. |
| **Filled Triangles (Pyramids)** | `python-pptx` `FreeformBuilder` | We can mathematically calculate the exact vertices of a trapezoid (representing the filled percentage of a triangle) and draw it natively. This keeps the shape as a crisp, editable vector inside PowerPoint. |
| **Split Background & Typography** | `python-pptx` native shapes | Standard rectangles and text boxes provide the perfect structural layout. |

> **Feasibility Assessment**: 100% reproduction of the visual aesthetic. The combination of Matplotlib for complex polar geometry and Freeform polygon math for the pyramids perfectly mimics the Adobe Illustrator workflow shown in the tutorial.

#### 3b. Complete Reproduction Code

```python
import io
import numpy as np
import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def _create_nested_donut_image(val_mid, val_inn, color_out, color_mid, color_inn):
    """Generates a transparent PNG of the nested donut chart using Matplotlib"""
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.axis('off')

    # Outer ring: 24 dashed segments
    segments = 24
    theta = np.linspace(0, 2*np.pi, segments, endpoint=False)
    # 60% fill, 40% gap per segment
    width_out = (2*np.pi) / segments * 0.6 
    ax.bar(theta, [0.15]*segments, width=width_out, bottom=0.85, color=color_out, align='edge')

    # Middle solid ring
    ax.bar(0, [0.15], width=2*np.pi*val_mid, bottom=0.65, color=color_mid, align='edge')
    # Inner solid ring
    ax.bar(0, [0.15], width=2*np.pi*val_inn, bottom=0.45, color=color_inn, align='edge')

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True, dpi=300)
    plt.close(fig)
    buf.seek(0)
    return buf

def _create_single_donut_image(val, color, bg_color='#E5E5E5'):
    """Generates a simple percentage donut chart"""
    fig, ax = plt.subplots(figsize=(2, 2), subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.axis('off')

    # Gray background track
    ax.bar(0, [0.2], width=2*np.pi, bottom=0.8, color=bg_color, align='edge')
    # Colored value track
    ax.bar(0, [0.2], width=2*np.pi*val, bottom=0.8, color=color, align='edge')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True, dpi=300)
    plt.close(fig)
    buf.seek(0)
    return buf

def create_slide(
    output_pptx_path: str,
    title_text: str = "信息图表", # Information Chart
    subtitle_text: str = "Adobe Illustrator Tutorial\nStep by step teach you to use AI",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Illustrator-style vector dashboard.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide

    # --- Colors ---
    c_bg_left = RGBColor(122, 96, 224)    # Deep Indigo
    c_white = RGBColor(255, 255, 255)
    c_dark_txt = RGBColor(50, 50, 50)
    
    # Palette matching the tutorial
    hex_pink = '#E88B8C'
    hex_green = '#79CC9E'
    hex_purple = '#8B7AE4'
    hex_navy = '#5965A3'
    hex_gray = '#E5E5E5'

    rgb_pink = RGBColor(232, 139, 140)
    rgb_green = RGBColor(121, 204, 158)
    rgb_purple = RGBColor(139, 122, 228)
    rgb_gray = RGBColor(229, 229, 229)

    # --- 1. Background Layout ---
    # Left Dark Panel
    left_panel = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, Inches(4.5), Inches(7.5)
    )
    left_panel.fill.solid()
    left_panel.fill.fore_color.rgb = c_bg_left
    left_panel.line.fill.background()

    # --- 2. Typography (Left Panel) ---
    tx_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(3.5), Inches(2))
    tf = tx_box.text_frame
    tf.word_wrap = True
    
    p = tf.add_paragraph()
    p.text = subtitle_text
    p.font.size = Pt(20)
    p.font.color.rgb = c_white
    p.font.bold = True
    
    p2 = tf.add_paragraph()
    p2.text = title_text
    p2.font.size = Pt(54)
    p2.font.color.rgb = c_white
    p2.font.bold = True

    # --- 3. Top Right: Nested Segmented Donut ---
    donut_stream = _create_nested_donut_image(
        val_mid=0.51, val_inn=0.45, 
        color_out=hex_purple, color_mid=hex_green, color_inn=hex_navy
    )
    slide.shapes.add_picture(donut_stream, Inches(7.5), Inches(0.2), Inches(3.5), Inches(3.5))

    # --- 4. Middle Row: Filled Triangles (Pyramids) ---
    triangles_data = [
        {"x": 5.5, "val": 0.70, "color": rgb_pink},
        {"x": 8.0, "val": 0.45, "color": rgb_green},
        {"x": 10.5, "val": 0.80, "color": rgb_purple}
    ]
    
    y_tri = Inches(3.8)
    w_tri = Inches(1.8)
    h_tri = Inches(1.8)

    for data in triangles_data:
        # Base Gray Triangle
        bg_tri = slide.shapes.add_shape(
            MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(data["x"]), y_tri, w_tri, h_tri
        )
        bg_tri.fill.solid()
        bg_tri.fill.fore_color.rgb = rgb_gray
        bg_tri.line.fill.background()

        # Calculate math for the filled trapezoid
        p = data["val"]
        x_base = Inches(data["x"])
        
        # Coordinates for Freeform Builder
        bottom_y = y_tri + h_tri
        top_y = y_tri + h_tri * (1 - p)
        
        # Width of the triangle at the fill line (similar triangles)
        w_top = w_tri * p
        x_top_left = x_base + (w_tri / 2) - (w_top / 2)
        x_top_right = x_base + (w_tri / 2) + (w_top / 2)

        # Build the trapezoid using FreeformBuilder
        ffb = slide.shapes.build_freeform(x_base, bottom_y)
        ffb.add_line_segments([
            (x_top_left, top_y),
            (x_top_right, top_y),
            (x_base + w_tri, bottom_y)
        ], close=True)
        
        fill_shape = ffb.convert_to_shape()
        fill_shape.fill.solid()
        fill_shape.fill.fore_color.rgb = data["color"]
        fill_shape.line.fill.background()

        # Add Percentage Text below
        tb = slide.shapes.add_textbox(Inches(data["x"]), y_tri + h_tri, w_tri, Inches(0.5))
        tf = tb.text_frame
        p_txt = tf.paragraphs[0]
        p_txt.text = f"{int(data['val']*100)}%"
        p_txt.alignment = PP_ALIGN.CENTER
        p_txt.font.size = Pt(20)
        p_txt.font.color.rgb = c_dark_txt
        p_txt.font.bold = True

    # --- 5. Bottom Row: Simple Donut Charts ---
    donuts_data = [
        {"x": 5.5, "val": 0.35, "color": hex_pink},
        {"x": 8.0, "val": 0.10, "color": hex_green},
        {"x": 10.5, "val": 0.20, "color": hex_purple}
    ]
    
    y_donut = Inches(5.8)
    w_donut = Inches(1.6)

    for data in donuts_data:
        stream = _create_single_donut_image(data["val"], data["color"], hex_gray)
        # Shift X slightly to center the 1.6" image within the 1.8" column grid
        pic_x = Inches(data["x"]) + (w_tri - w_donut) / 2
        slide.shapes.add_picture(stream, pic_x, y_donut, w_donut, w_donut)

        # Center Text inside Donut
        tb = slide.shapes.add_textbox(pic_x, y_donut + Inches(0.5), w_donut, Inches(0.6))
        tf = tb.text_frame
        p_txt = tf.paragraphs[0]
        p_txt.text = f"{int(data['val']*100)}%"
        p_txt.alignment = PP_ALIGN.CENTER
        p_txt.font.size = Pt(18)
        p_txt.font.color.rgb = c_dark_txt

    prs.save(output_pptx_path)
    return output_pptx_path
```