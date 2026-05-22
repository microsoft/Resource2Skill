# Interlocking Chevron Progress Agenda

## Analysis

# 1. High-level Design Pattern Extraction

> **Skill Name**: Interlocking Chevron Progress Agenda

* **Core Visual Mechanism**: The design relies on constructing a composite ribbon shape that points forward (left-to-right flow). Visually, each row consists of a colored "main body" (featuring a sharp, inward chevron-cut on the left and a smooth rounded edge on the right) and a disconnected, lighter-colored "arrow tip" on the far left. A distinct, uniform gap between the tip and the body creates a sophisticated interlocking or "origami fold" aesthetic.
* **Why Use This Skill (Rationale)**: This layout breaks the monotony of vertical bullet points. The forward-pointing chevron geometry inherently implies progression, steps, or sequential agenda items. The distinct, disconnected tip serves as an excellent visual anchor for numbering, drawing the eye directly to the sequence.
* **Overall Applicability**: Ideal for Agenda slides, Table of Contents, process visualizations (Steps 1-4), or detailing chronological project phases. 
* **Value Addition**: Transforms a standard text list into a structured, highly professional infographic. The dual-tone effect and curved/sharp contrast add a modern, polished aesthetic that looks custom-made rather than relying on default SmartArt.

# 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Main Ribbon**: A custom compound shape. Left side is sharply pointed; right side is rounded.
  - **Tip Anchor**: A chevron-shaped polygon that fits perfectly into the left point of the main ribbon, separated by a precise visual gap.
  - **Typography**: Large, bold sans-serif numbering ("01", "02"). White text inside the colored ribbons for high contrast. Large, dominant title text on the left pane.
  - **Color Logic**: A neutral light gray for the arrow tips `(166, 166, 166)`, paired with a vibrant, distinct color for each row body to separate information.
    - Row 1 (Blue): `(47, 53, 144)`
    - Row 2 (Burgundy/Magenta): `(104, 14, 52)`
    - Row 3 (Emerald): `(43, 142, 29)`
    - Row 4 (Violet): `(87, 6, 140)`

* **Step B: Compositional Style**
  - Widescreen 16:9 canvas.
  - Left pane (~35% width) is reserved for the macro-level context (Title, Subtitle).
  - Right pane (~65% width) houses the staggered rows.
  - Rows span horizontally from near the center to the right edge. Height is substantial enough (~0.9 inches) to comfortably house two lines of text and an icon.

* **Step C: Dynamic Effects & Transitions**
  - Sequential "Wipe" entrance from the right for the main ribbons.
  - "Zoom" effect for the numbering and text.
  - *Note: Animations require native GUI setup; the code will focus on perfectly recreating the static geometric layout.*

# 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| "Merge Shapes" Union | `FreeformBuilder` (python-pptx) | `python-pptx` does not support shape boolean operations (Union/Subtract). We recreate the complex custom shape by programmatically plotting an exact polygon that covers the left side of a standard rounded rectangle. |
| Interlocking Chevron Gap | Polygon Math Math | Calculating precise X/Y offsets for a custom gray chevron polygon guarantees a pixel-perfect, uniform gap separating the tip from the main body, ensuring a flawless vector output without anti-aliasing artifacts. |
| Icons | Unicode Text Elements | Bypasses the need for external image assets while maintaining clean, scalable vector symbols that respect text color overrides. |

> **Feasibility Assessment**: 95% reproduction. The code perfectly recreates the complex interlocking geometry, layout, and styling. The only omission is the native PowerPoint slide entrance animations, which are extremely brittle to script via XML injection and better applied globally in the PowerPoint GUI.

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR
from pptx.enum.shape import MSO_SHAPE

def create_slide(
    output_pptx_path: str,
    title_text: str = "AGENDA SLIDE",
    subtitle_text: str = "Not everyone falls into\nsuccess with their first try.",
    row_data: list = None,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Interlocking Chevron Progress Agenda effect.
    """
    if row_data is None:
        row_data = [
            {"num": "01", "text": "The quick brown fox jumps over the lazy dog. A continuous process.", "icon": "🚀", "color": (47, 53, 144)},
            {"num": "02", "text": "A seamless pipeline ensures higher quality and reduced friction.", "icon": "🎯", "color": (104, 14, 52)},
            {"num": "03", "text": "Deploying the infrastructure securely across all environments.", "icon": "📊", "color": (43, 142, 29)},
            {"num": "04", "text": "Final review and retrospective analysis for constant improvement.", "icon": "💡", "color": (87, 6, 140)}
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    # === Left Context Pane (Title & Subtitle) ===
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.2), Inches(3.5), Inches(1.0))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text.upper()
    p.font.name = "Arial Black"
    p.font.size = Pt(44)
    p.font.color.rgb = RGBColor(42, 54, 79)

    sub_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.3), Inches(3.5), Inches(1.5))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = RGBColor(100, 100, 100)

    # === Layout Parameters for the Agenda Rows ===
    num_rows = len(row_data)
    row_h = 1.0          # Height of each ribbon
    spacing = 0.25       # Vertical gap between ribbons
    start_y = 1.3        # Starting Y position
    
    # X-coordinates for the complex geometry
    x_body_point = 4.2   # Where the point of the colored body sits
    x_body_flat = 4.7    # Where the angled cut flattens out into the rectangle
    x_right_edge = 12.8  # Right edge of the screen
    
    gap = 0.08           # Spatial gap between the gray tip and colored body
    tip_w = 0.8          # Width of the gray tip
    gray_color = RGBColor(166, 166, 166)

    # === Build Rows ===
    for idx, item in enumerate(row_data):
        y = start_y + idx * (row_h + spacing)
        color_rgb = RGBColor(*item["color"])

        # --- Shape 1: Main Body (Rounded Right Side) ---
        # We use a built-in Rounded Rectangle. Its left rounded corners will be hidden 
        # by our custom overlapping Freeform point.
        rect = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, 
            Inches(x_body_flat), Inches(y), 
            Inches(x_right_edge - x_body_flat), Inches(row_h)
        )
        rect.fill.solid()
        rect.fill.fore_color.rgb = color_rgb
        rect.line.color.rgb = color_rgb # Match line to fill to prevent antialiasing seams
        
        # --- Shape 2: Main Body (Sharp Left Point) ---
        # We draw a polygon that seamlessly extends the rectangle into a left-pointing arrow.
        # It overlaps the rectangle slightly (x_body_flat to x_body_flat+0.5) to hide the left rounded corners.
        pts_body_point = [
            (Inches(x_body_point), Inches(y + row_h/2)),
            (Inches(x_body_flat), Inches(y)),
            (Inches(x_body_flat + 0.5), Inches(y)),
            (Inches(x_body_flat + 0.5), Inches(y + row_h)),
            (Inches(x_body_flat), Inches(y + row_h))
        ]
        builder_bp = slide.shapes.build_freeform()
        builder_bp.add_line_segments(pts_body_point, close=True)
        shape_bp = builder_bp.convert_to_shape()
        shape_bp.fill.solid()
        shape_bp.fill.fore_color.rgb = color_rgb
        shape_bp.line.color.rgb = color_rgb

        # --- Shape 3: Disconnected Gray Chevron Tip ---
        # Calculated to perfectly shadow the Main Body's left cut, shifted left by 'gap'
        pts_tip = [
            (Inches(x_body_point - gap - tip_w), Inches(y + row_h/2)),   # Front Tip
            (Inches(x_body_flat - gap - tip_w), Inches(y)),              # Front Top
            (Inches(x_body_flat - gap), Inches(y)),                      # Back Top
            (Inches(x_body_point - gap), Inches(y + row_h/2)),           # Back Inner V-cut (matches body point)
            (Inches(x_body_flat - gap), Inches(y + row_h)),              # Back Bottom
            (Inches(x_body_flat - gap - tip_w), Inches(y + row_h))       # Front Bottom
        ]
        builder_tip = slide.shapes.build_freeform()
        builder_tip.add_line_segments(pts_tip, close=True)
        shape_tip = builder_tip.convert_to_shape()
        shape_tip.fill.solid()
        shape_tip.fill.fore_color.rgb = gray_color
        shape_tip.line.color.rgb = gray_color

        # --- Content: Number ---
        num_box = slide.shapes.add_textbox(Inches(x_body_flat - 0.2), Inches(y), Inches(1.0), Inches(row_h))
        num_box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_num = num_box.text_frame.paragraphs[0]
        p_num.text = item["num"]
        p_num.font.name = "Arial Black"
        p_num.font.size = Pt(28)
        p_num.font.color.rgb = RGBColor(255, 255, 255)

        # --- Content: Text ---
        text_box = slide.shapes.add_textbox(Inches(x_body_flat + 0.8), Inches(y + 0.1), Inches(6.0), Inches(row_h - 0.2))
        text_box.text_frame.word_wrap = True
        text_box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_text = text_box.text_frame.paragraphs[0]
        p_text.text = item["text"]
        p_text.font.name = "Arial"
        p_text.font.size = Pt(13)
        p_text.font.color.rgb = RGBColor(255, 255, 255)
        
        # --- Content: Icon (Simulated via Unicode) ---
        icon_box = slide.shapes.add_textbox(Inches(11.8), Inches(y), Inches(0.8), Inches(row_h))
        icon_box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_icon = icon_box.text_frame.paragraphs[0]
        p_icon.text = item["icon"]
        p_icon.font.name = "Segoe UI Emoji"
        p_icon.font.size = Pt(24)
        p_icon.font.color.rgb = RGBColor(255, 255, 255)

    prs.save(output_pptx_path)
    return output_pptx_path
```