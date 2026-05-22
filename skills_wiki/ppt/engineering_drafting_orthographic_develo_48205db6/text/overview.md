# Engineering Drafting & Orthographic Development

## Analysis

# Skill Extraction: Engineering Drafting & Orthographic Development

### 1. High-level Design Pattern Extraction

> **Skill Name**: Engineering Drafting & Orthographic Development

* **Core Visual Mechanism**: This design style replicates the precise, vector-based aesthetic of a technical engineering drawing (descriptive geometry). It relies on a strict visual grammar: a plain contrasting background, distinct line weights and colors separating object boundaries from construction lines, standard orthographic views (Top, Front) placed alongside a flattened "development" view, and meticulous point labeling.
* **Why Use This Skill (Rationale)**: This aesthetic inherently communicates academic rigor, precision, and logical progression. The raw, "blueprint" look strips away corporate polish in favor of raw analytical truth, making the audience feel they are looking at how something is actually built or calculated.
* **Overall Applicability**: Ideal for technical presentations, architecture or mechanical engineering pitches, academic lectures, or "deep dive" slides explaining the underlying mechanics/architecture of a product or software system. 
* **Value Addition**: Transforms simple shapes into a complex, highly credible diagram. The use of specific "cut lines" and "projections" visually proves that a solution was derived through logic rather than just placed on the screen.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: Matte off-white or light gray `(245, 245, 245)` to simulate drafting paper or a whiteboard.
  - **Line Logic & Color Palette**:
    - *Object Lines (Thick)*: Dark Slate/Black `(30, 30, 30)` for the physical edges of the pyramid.
    - *Construction/Projection Lines (Thin)*: Light Gray `(180, 180, 180)` to show relationships without cluttering.
    - *Cutting/Highlight Lines (Medium)*: Vibrant Cyan/Blue `(0, 176, 240)` to indicate modifications, planes, or the resulting truncated paths.
  - **Text Hierarchy**: 
    - *Problem Statement*: Standard sans-serif block at the top, clear and unobtrusive.
    - *Annotations*: Small, lowercase/uppercase italicized labels (a, b, c, o', p') precisely placed next to geometric vertices.

* **Step B: Compositional Style**
  - The canvas is divided logically: The top 25% is reserved for context (the problem text). The remaining space is split 40/60. The left side contains the orthogonal views anchored by a horizontal X-Y reference line. The right side is a spacious, radiating arc showing the 3D object "unrolled" into 2D space.

* **Step C: Dynamic Effects & Transitions**
  - While the reference video shows the *process* of drawing, the final output is static. In a presentation context, these lines would typically be animated using PowerPoint's native "Wipe" (from left/top) or "Draw" animations to simulate the live construction of the geometry step-by-step.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Geometric Lines & Polygons** | `python-pptx` shapes (Connectors) | Native shapes are sharp, scalable (vector), and perfect for line-art diagrams. |
| **Radial Development Math** | Python `math` module | Calculating the exact (x,y) vertices of the unfolded pyramid requires trigonometric functions to generate accurate chords. |
| **Labeling** | `python-pptx` TextBoxes | Standard text boxes with transparent backgrounds allow precise placement of vertex labels. |

> **Feasibility Assessment**: 100% reproduction of the visual style. The code mathematically plots an orthographic projection and its corresponding geometric development, perfectly capturing the aesthetic of a CAD/engineering diagram.

#### 3b. Complete Reproduction Code

```python
import math
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_LINE_DASH_STYLE
from pptx.enum.text import MSO_ANCHOR

def create_slide(
    output_pptx_path: str,
    title_text: str = "A square pyramid of side 45 mm and height 65 mm stands with its base on HP...",
    bg_color: tuple = (250, 250, 250), # Light grey/white paper feel
    line_dark: tuple = (30, 30, 30),
    line_light: tuple = (200, 200, 200),
    line_accent: tuple = (0, 112, 192), # Blue highlight for cuts
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Engineering Drafting visual pattern.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # Set background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # --- Helper Functions ---
    def add_line(x1, y1, x2, y2, color, width_pt, dash=None):
        connector = slide.shapes.add_connector(
            1, Inches(x1), Inches(y1), Inches(x2), Inches(y2)
        )
        line = connector.line
        line.color.rgb = RGBColor(*color)
        line.width = Pt(width_pt)
        if dash:
            line.dash_style = dash
        return connector

    def add_label(text, x, y, size=12, italic=False):
        txBox = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(0.5), Inches(0.5))
        tf = txBox.text_frame
        tf.text = text
        tf.paragraphs[0].font.size = Pt(size)
        tf.paragraphs[0].font.name = "Segoe UI"
        tf.paragraphs[0].font.italic = italic
        tf.paragraphs[0].font.color.rgb = RGBColor(100, 100, 100)
        
    # --- 1. Top Problem Statement Text ---
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.3), Inches(1.0))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "A square pyramid of side 45 mm and height 65 mm stands with its base on HP such that two edges of the base are parallel to VP. It is cut by a plane perpendicular to VP and inclined at 45° to HP and passing through a point on the axis, 35 mm above the base. Draw the development of the lateral surfaces of the truncated pyramid."
    p.font.size = Pt(16)
    p.font.name = "Segoe UI"
    p.font.color.rgb = RGBColor(50, 50, 50)

    # --- 2. Orthographic Projections (Left Side) ---
    
    # X-Y Reference Line
    xy_y = 5.0
    add_line(1.0, xy_y, 6.0, xy_y, line_dark, 1.5)
    add_label("X", 0.8, xy_y - 0.2)
    add_label("Y", 6.0, xy_y - 0.2)

    # TOP VIEW (Square + Diagonals)
    cx, cy = 2.5, 6.2 # Center of Top View
    sl = 0.8 # half side length
    # Outline
    add_line(cx-sl, cy-sl, cx+sl, cy-sl, line_dark, 1.5) # Top
    add_line(cx+sl, cy-sl, cx+sl, cy+sl, line_dark, 1.5) # Right
    add_line(cx+sl, cy+sl, cx-sl, cy+sl, line_dark, 1.5) # Bottom
    add_line(cx-sl, cy+sl, cx-sl, cy-sl, line_dark, 1.5) # Left
    # Diagonals
    add_line(cx-sl, cy-sl, cx+sl, cy+sl, line_dark, 1.0)
    add_line(cx-sl, cy+sl, cx+sl, cy-sl, line_dark, 1.0)
    
    # Top View Labels
    add_label("d", cx-sl-0.2, cy-sl-0.2, italic=True)
    add_label("c", cx+sl+0.1, cy-sl-0.2, italic=True)
    add_label("a", cx-sl-0.2, cy+sl+0.1, italic=True)
    add_label("b", cx+sl+0.1, cy+sl+0.1, italic=True)
    add_label("o", cx-0.1, cy-0.1, italic=True)

    # FRONT VIEW (Triangle)
    vx, vy = cx, 2.0 # Apex of Front View (o')
    add_line(cx-sl, xy_y, cx+sl, xy_y, line_dark, 2.0) # Base on XY
    add_line(cx-sl, xy_y, vx, vy, line_dark, 1.5) # Left slant
    add_line(cx+sl, xy_y, vx, vy, line_dark, 1.5) # Right slant
    add_line(cx, xy_y, vx, vy, line_dark, 1.5) # Center axis
    
    # Front View Labels
    add_label("a'(d')", cx-sl-0.4, xy_y, italic=True)
    add_label("b'(c')", cx+sl+0.1, xy_y, italic=True)
    add_label("o'", vx-0.1, vy-0.3, italic=True)

    # CONSTRUCTION LINES (Connecting Top and Front)
    add_line(cx-sl, cy-sl, cx-sl, xy_y, line_light, 1.0, MSO_LINE_DASH_STYLE.DASH)
    add_line(cx+sl, cy-sl, cx+sl, xy_y, line_light, 1.0, MSO_LINE_DASH_STYLE.DASH)
    add_line(cx, cy, cx, vy, line_light, 1.0, MSO_LINE_DASH_STYLE.DASH_DOT) # Center axis

    # CUTTING PLANE
    cut_y = xy_y - 1.2 # 35mm above base
    # Line at 45 degrees passing through (cx, cut_y)
    dx = 1.8
    add_line(cx - dx, cut_y + dx, cx + dx, cut_y - dx, line_accent, 2.5, MSO_LINE_DASH_STYLE.LONG_DASH_DOT)
    
    # Mark cut points on front view
    p_left_y = cut_y + sl
    p_right_y = cut_y - sl
    add_label("p'", cx-sl-0.3, p_left_y-0.1, italic=True)
    add_label("q'", cx+sl+0.1, p_right_y-0.1, italic=True)


    # --- 3. True Development (Right Side) ---
    
    ox, oy = 8.0, 1.8 # Focus point of development
    R = math.hypot(sl, xy_y - vy) * 1.5 # Radius (scaled up slightly for visibility)
    
    num_segments = 4
    start_angle = math.radians(35)
    angle_step = math.radians(22)
    
    dev_points = []
    cut_points = []
    
    # Ratios for where the cut plane hits the slants (simulated for visual)
    cut_ratios = [0.4, 0.6, 0.8, 0.6, 0.4] 

    # Generate points for the unrolled base
    for i in range(num_segments + 1):
        theta = start_angle + i * angle_step
        px = ox + R * math.cos(theta)
        py = oy + R * math.sin(theta)
        dev_points.append((px, py))
        
        # Calculate truncated cut points
        cx_cut = ox + (R * cut_ratios[i]) * math.cos(theta)
        cy_cut = oy + (R * cut_ratios[i]) * math.sin(theta)
        cut_points.append((cx_cut, cy_cut))

    # Draw radial lines (creases)
    for i, (px, py) in enumerate(dev_points):
        # Draw full construction ray
        add_line(ox, oy, px, py, line_light, 1.0)
        
        # Draw retained bold portion (from cut point to base)
        cx_cut, cy_cut = cut_points[i]
        add_line(cx_cut, cy_cut, px, py, line_dark, 2.0)
        
        # Labels
        lbls = ["A", "B", "C", "D", "A"]
        add_label(lbls[i], px + 0.1, py + 0.1)

    # Draw base chords (outer edge of development)
    for i in range(num_segments):
        add_line(dev_points[i][0], dev_points[i][1], 
                 dev_points[i+1][0], dev_points[i+1][1], 
                 line_dark, 2.0)

    # Draw the bold cut path (inner connected shape)
    for i in range(num_segments):
        add_line(cut_points[i][0], cut_points[i][1], 
                 cut_points[i+1][0], cut_points[i+1][1], 
                 line_accent, 2.5)
        
        # Draw projection line simulating taking height from front view
        add_line(cx + sl, p_right_y, cut_points[2][0], cut_points[2][1], line_light, 1.0, MSO_LINE_DASH_STYLE.DASH)

    # Center label for Development
    add_label("O", ox-0.1, oy-0.3)

    prs.save(output_pptx_path)
    return output_pptx_path
```