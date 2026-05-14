# 3D Isometric Book Comparison Infographic

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: 3D Isometric Book Comparison Infographic

* **Core Visual Mechanism**: This pattern simulates an open book or folder presented in a pseudo-3D isometric perspective. It relies on carefully mapped custom geometric polygons (covers and back pages) with calculated slopes. The illusion of 3D depth is enhanced by applying dynamic shading (darkening one side, lightening the background pages) and applying exact 2D rotations to overlay text to match the slope of the isometric planes.
* **Why Use This Skill (Rationale)**: Comparing "A" versus "B" is a classic presentation need. A standard side-by-side list is forgettable. Using an open book metaphor psychologically implies that both options belong to the same narrative, while structurally providing a beautiful, centralized anchor for branching callout information. 
* **Overall Applicability**: Perfect for educational content, A/B testing results, "Old Way vs. New Way" paradigms, and strategic crossroads where two paths or methodologies are being weighed. 
* **Value Addition**: Transforms flat lists into a rich, vector-based 3D scene without requiring external image assets. The shapes remain fully editable, recolorable, and mathematically precise within PowerPoint.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Geometric Construction**: The "book" consists of 4 freeform polygons: Left Page Back, Right Page Back, Left Cover, Right Cover. 
  - **Color Logic**: Utilizes a monolithic color palette based on a single accent color. 
    - Left Cover: Base Accent (e.g., Teal `(26, 188, 156)`)
    - Right Cover: Darkened by 15% `(22, 160, 133)` to simulate a light source
    - Left Pages: Lightened by 60% `(163, 228, 215)` to push them to the background
    - Right Pages: Lightened by 40% `(118, 215, 196)` 
  - **Text Hierarchy**: Massive, bold, white "A" and "B" lettering anchored inside the shapes. Surrounding callout titles are bold, with smaller, muted gray supporting text. 

* **Step B: Compositional Style**
  - **Spatial Feel**: The book acts as a central gravitational body. Symmetrical horizontal connector lines branch outward from the center, tethering floating icons and descriptive text blocks. 
  - **Proportions**: The book occupies the central 35% of the slide (X-axis 4.0" to 9.33"), leaving ample negative space on the left and right (the remaining 65%) for detailed typography.

* **Step C: Dynamic Effects & Transitions**
  - **Perspective Tilt**: The text "A" and "B" are rotated ±11 degrees. Because the polygons have a slope of `dx=2.66, dy=0.5` ($\approx 10.6^\circ$), this 2D rotation creates a startlingly convincing pseudo-3D perspective effect.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **3D Book Covers & Pages** | `python-pptx` (FreeformBuilder) | Drawing custom polygons via vertex mapping generates crisp, native, editable vector shapes. It avoids heavy image compositing and keeps file size tiny. |
| **Dynamic 3D Shading** | Python Math | By calculating darkened/lightened RGB variants of a single user-provided color, we guarantee the 3D depth effect works on *any* theme automatically. |
| **Perspective Text** | `python-pptx` (Rotation) | Matching the rotational angle of a standard text box to the trigonometric slope of the freeform polygon creates a perfect perspective illusion natively. |

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_CONNECTOR

def create_slide(
    output_pptx_path: str,
    title_text: str = "COMPARISON INFOGRAPHIC",
    body_text: str = "",
    bg_palette: str = "education",  
    accent_color: tuple = (26, 188, 156),  # Default: Vibrant Teal
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 3D Isometric Book Comparison effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # --- Helper: Dynamic Color Generator for 3D Shading ---
    def adjust_color(color: tuple, factor: float) -> tuple:
        """Lightens (factor > 0) or darkens (factor < 0) an RGB tuple."""
        r, g, b = color
        if factor > 0:
            r = int(r + (255 - r) * factor)
            g = int(g + (255 - g) * factor)
            b = int(b + (255 - b) * factor)
        else:
            r = int(r * (1 + factor))
            g = int(g * (1 + factor))
            b = int(b * (1 + factor))
        return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

    left_cover_color = accent_color
    right_cover_color = adjust_color(accent_color, -0.15) # Darker
    left_pages_color = adjust_color(accent_color, 0.6)    # Lighter
    right_pages_color = adjust_color(accent_color, 0.4)   # Slightly less light

    # --- Helper: Freeform Polygon Drawer ---
    def add_polygon(slide, points: list, color: tuple):
        ff = slide.shapes.build_freeform(Inches(points[0][0]), Inches(points[0][1]))
        ff.add_line_segments([(Inches(x), Inches(y)) for x, y in points[1:]], close=True)
        shape = ff.convert_to_shape()
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*color)
        shape.line.fill.solid()
        shape.line.fill.fore_color.rgb = RGBColor(*color)
        return shape

    # ==========================================
    # LAYER 1: Isometric Book Construction
    # ==========================================
    
    # 1. Back Pages (Drawn first to sit behind covers)
    # The spine apex for the pages is at (6.66, 2.7)
    left_pages = [(4.0, 2.5), (4.2, 2.3), (6.66, 2.8), (6.66, 3.0)]
    add_polygon(slide, left_pages, left_pages_color)

    right_pages = [(9.33, 2.5), (9.13, 2.3), (6.66, 2.8), (6.66, 3.0)]
    add_polygon(slide, right_pages, right_pages_color)

    # 2. Front Covers
    # The spine center for the covers is at (6.66, 3.0) and bottom is (6.66, 6.0)
    left_cover = [(4.0, 2.5), (6.66, 3.0), (6.66, 6.0), (4.0, 5.5)]
    add_polygon(slide, left_cover, left_cover_color)

    right_cover = [(6.66, 3.0), (9.33, 2.5), (9.33, 5.5), (6.66, 6.0)]
    add_polygon(slide, right_cover, right_cover_color)

    # ==========================================
    # LAYER 2: Pseudo-3D Perspective Text
    # ==========================================
    # The slope angle is approx 10.6 degrees. We rotate the text to match it.

    # Left 'A'
    tx_a = slide.shapes.add_textbox(Inches(4.6), Inches(3.7), Inches(1.5), Inches(1.5))
    tx_a.rotation = 11.0 # Rotates clockwise to match the downward slope
    p = tx_a.text_frame.paragraphs[0]
    p.text = "A"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(88)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # Right 'B'
    tx_b = slide.shapes.add_textbox(Inches(7.2), Inches(3.7), Inches(1.5), Inches(1.5))
    tx_b.rotation = -11.0 # Rotates counter-clockwise to match the upward slope
    p = tx_b.text_frame.paragraphs[0]
    p.text = "B"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(88)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # Center Top Icon (Pop-out effect)
    tx_icon = slide.shapes.add_textbox(Inches(6.0), Inches(1.7), Inches(1.33), Inches(1.0))
    p = tx_icon.text_frame.paragraphs[0]
    p.text = "👥"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(44)

    # ==========================================
    # LAYER 3: Callouts & Infographic Layout
    # ==========================================

    def add_callout(slide, side: str, y_center: float, title: str, desc: str, icon: str):
        line_y = y_center
        if side == "left":
            # Connector
            line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(2.2), Inches(line_y), Inches(3.8), Inches(line_y))
            line.line.color.rgb = RGBColor(180, 180, 180)
            line.line.width = Pt(1.5)
            
            # Icon (Right-aligned against the line)
            tx_i = slide.shapes.add_textbox(Inches(3.3), Inches(line_y - 0.4), Inches(0.8), Inches(0.8))
            tx_i.text_frame.text = icon
            tx_i.text_frame.paragraphs[0].font.size = Pt(24)
            
            # Text Box
            tx_t = slide.shapes.add_textbox(Inches(0.5), Inches(line_y - 0.6), Inches(2.0), Inches(1.5))
            tf = tx_t.text_frame
            tf.word_wrap = True
            p1 = tf.paragraphs[0]
            p1.text = title
            p1.font.bold = True
            p1.font.size = Pt(13)
            p1.alignment = PP_ALIGN.RIGHT
            p2 = tf.add_paragraph()
            p2.text = desc
            p2.font.size = Pt(10)
            p2.font.color.rgb = RGBColor(120, 120, 120)
            p2.alignment = PP_ALIGN.RIGHT
        else:
            # Connector
            line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(9.5), Inches(line_y), Inches(11.1), Inches(line_y))
            line.line.color.rgb = RGBColor(180, 180, 180)
            line.line.width = Pt(1.5)
            
            # Icon (Left-aligned against the line)
            tx_i = slide.shapes.add_textbox(Inches(9.2), Inches(line_y - 0.4), Inches(0.8), Inches(0.8))
            tx_i.text_frame.text = icon
            tx_i.text_frame.paragraphs[0].font.size = Pt(24)
            
            # Text Box
            tx_t = slide.shapes.add_textbox(Inches(10.8), Inches(line_y - 0.6), Inches(2.0), Inches(1.5))
            tf = tx_t.text_frame
            tf.word_wrap = True
            p1 = tf.paragraphs[0]
            p1.text = title
            p1.font.bold = True
            p1.font.size = Pt(13)
            p1.alignment = PP_ALIGN.LEFT
            p2 = tf.add_paragraph()
            p2.text = desc
            p2.font.size = Pt(10)
            p2.font.color.rgb = RGBColor(120, 120, 120)
            p2.alignment = PP_ALIGN.LEFT

    # Add 4 balanced callouts
    add_callout(slide, "left", 3.2, "ACHIEVEMENTS", "Highlights of path A performance, focus areas, and overall success.", "🏆")
    add_callout(slide, "left", 4.8, "MILESTONES", "Key educational checkpoints and certifications completed.", "🎓")
    add_callout(slide, "right", 3.2, "CULTURE", "Events and team-building strategies implemented for path B.", "💡")
    add_callout(slide, "right", 4.8, "EVENTS", "Upcoming celebrations and major milestones for the year.", "🚀")

    # ==========================================
    # LAYER 4: Overall Slide Titles
    # ==========================================
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(0.4), Inches(11.333), Inches(1.0))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text.upper()
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = adjust_color(accent_color, -0.3)
    p.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx_path)
    return output_pptx_path
```