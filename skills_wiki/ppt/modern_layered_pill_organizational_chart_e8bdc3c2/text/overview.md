# Modern Layered-Pill Organizational Chart

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Modern Layered-Pill Organizational Chart

* **Core Visual Mechanism**: The defining visual idea is the "Color-Banded Pill Node." Instead of flat, monochrome boxes, this design uses fully rounded rectangles (pills) layered on top of one another. A wider colored pill sits behind a slightly narrower white pill, exposing a vertical band of color on the left edge. This is paired with soft drop shadows to create a modern, tactile "card" feel. A distinct, larger circular node denotes the top of the hierarchy.
* **Why Use This Skill (Rationale)**: Org charts can easily look rigid, corporate, and visually overwhelming. The pill shapes soften the aesthetic (reducing cognitive friction), while the distinct color bands provide instant visual grouping (distinguishing departments or teams) without needing heavy, saturated backgrounds that clash with text.
* **Overall Applicability**: Ideal for organizational structures, team introductions, decision trees, workflow process maps, and mind maps in modern corporate or startup decks.
* **Value Addition**: Transforms a standard SmartArt org chart into a custom, premium infographic. The layered shape technique creates depth, making the information pop off the slide, while maintaining strict, readable alignment.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Top Node (Level 0)**: Large circle with a subtle gradient fill, a distinct inner/outer border, and an avatar icon. 
  * **Subordinate Nodes (Level 1+)**: Horizontal pill shapes. They consist of a colored base layer and a white top layer to create a left-side color ribbon.
  * **Color Logic**:
    * Background: Very pale blue/gray `(235, 240, 245)` to allow white cards to pop.
    * Cards: Pure White `(255, 255, 255)` with Dark Gray text `(50, 50, 50)`.
    * Department Accents: Teal `(0, 150, 136)`, Red `(211, 47, 47)`, Blue `(25, 118, 210)`, Orange `(245, 124, 0)`, Green `(56, 142, 60)`.
  * **Text Hierarchy**: 
    * `NAME SURNAME`: Bold, slightly larger, dark gray.
    * `Job position`: Regular, smaller, lighter gray.

* **Step B: Compositional Style**
  * **Layout**: Strict top-down tree hierarchy.
  * **Proportions**: Subordinate nodes are roughly 2.5 times wider than they are tall (e.g., 2" x 0.8"). The color band takes up about 10-15% of the node's width.
  * **Connectors**: Thin gray lines linking nodes, often featuring small circular "joints" at connection points to add mechanical/structural detail.

* **Step C: Dynamic Effects & Transitions**
  * **Static Element**: The depth is static, achieved via drop shadows (`lxml` injected `outerShdw`).
  * **Animation (Optional)**: Typically, these elements fade or wipe in hierarchically from top to bottom.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Pill Shape Generation** | `python-pptx` native | Standard rounded rectangles adjusted to maximum roundness natively create perfect pill shapes. |
| **Color Band Effect** | `python-pptx` native (Layering) | Rather than complex multi-stop gradients, layering a slightly offset white shape over a colored shape perfectly reproduces the solid color band on the left. |
| **Node Drop Shadows** | `lxml` XML injection | `python-pptx` lacks native API support for applying drop shadows to shapes. Manipulating the OpenXML directly via `lxml` is required for the "floating card" aesthetic. |
| **Connector Lines & Hierarchy** | `python-pptx` native | Lines and small circles can be calculated via basic coordinate math to draw the tree structure. |

> **Feasibility Assessment**: 95%. The code accurately reproduces the layered pill cards, the color coding, the shadows, the text hierarchy, and the overall tree structure. I have substituted the video's manual use of "rotated curly braces" for standard orthogonal/straight connecting lines, as this is much more robust for dynamic algorithmic generation.

#### 3b. Complete Reproduction Code

```python
import os
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def add_shadow_to_shape(shape):
    """
    Injects a soft outer shadow into a shape's XML using lxml.
    """
    spPr = shape.element.spPr
    # Check if effectLst exists, if not create it
    effectLst = spPr.find('.//a:effectLst', namespaces=spPr.nsmap)
    if effectLst is None:
        effectLst = etree.SubElement(spPr, '{%s}effectLst' % spPr.nsmap['a'])
    
    # Define shadow parameters (distance, blur, angle, color/opacity)
    shadow_xml = """
        <a:outerShdw blurRad="50800" dist="38100" dir="5400000" algn="ctr" rotWithShape="0" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:srgbClr val="000000">
                <a:alpha val="15000"/>
            </a:srgbClr>
        </a:outerShdw>
    """
    outerShdw = etree.fromstring(shadow_xml)
    effectLst.append(outerShdw)

def draw_pill_node(slide, x, y, width, height, accent_color, name="NAME SURNAME", role="Job Position"):
    """
    Draws a single 'Pill' org chart node with a colored left edge and shadow.
    """
    # 1. Base shape (The accent color band)
    base_shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, x, y, width, height
    )
    base_shape.fill.solid()
    base_shape.fill.fore_color.rgb = accent_color
    base_shape.line.fill.background() # No line
    base_shape.adjustments[0] = 1.0 # Fully rounded (Pill)
    add_shadow_to_shape(base_shape)

    # 2. Top shape (The white card body)
    # Offset slightly to the right to leave the colored band exposed on the left
    band_width = width * 0.12
    top_shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, 
        x + band_width, y, 
        width - band_width, height
    )
    top_shape.fill.solid()
    top_shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
    top_shape.line.fill.background()
    top_shape.adjustments[0] = 1.0 # Fully rounded

    # 3. Avatar Placeholder (Circle)
    avatar_size = height * 0.6
    avatar_x = x + band_width + (height * 0.2)
    avatar_y = y + (height * 0.2)
    avatar = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, avatar_x, avatar_y, avatar_size, avatar_size
    )
    avatar.fill.solid()
    avatar.fill.fore_color.rgb = RGBColor(220, 220, 220)
    avatar.line.fill.background()

    # 4. Text Content
    text_box = slide.shapes.add_textbox(
        avatar_x + avatar_size + Inches(0.05), y, 
        width - band_width - avatar_size - Inches(0.1), height
    )
    tf = text_box.text_frame
    tf.word_wrap = True
    tf.margin_top = Pt(5)
    
    # Name Paragraph
    p_name = tf.paragraphs[0]
    p_name.text = name
    p_name.font.bold = True
    p_name.font.size = Pt(9)
    p_name.font.name = "Montserrat"
    p_name.font.color.rgb = RGBColor(50, 50, 50)
    
    # Role Paragraph
    p_role = tf.add_paragraph()
    p_role.text = role
    p_role.font.size = Pt(7)
    p_role.font.name = "Montserrat"
    p_role.font.color.rgb = RGBColor(120, 120, 120)

    return {"top_x": x + width/2, "top_y": y, "bottom_x": x + width/2, "bottom_y": y + height}

def draw_top_node(slide, x, y, size, accent_color, name="CEO NAME", role="Executive"):
    """
    Draws the circular top node of the hierarchy.
    """
    # Main Circle
    circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, x - size/2, y, size, size
    )
    circle.fill.solid()
    circle.fill.fore_color.rgb = RGBColor(245, 250, 255)
    circle.line.color.rgb = accent_color
    circle.line.width = Pt(3)
    add_shadow_to_shape(circle)

    # Avatar
    avatar_size = size * 0.4
    avatar = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, x - avatar_size/2, y + size*0.1, avatar_size, avatar_size
    )
    avatar.fill.solid()
    avatar.fill.fore_color.rgb = accent_color
    avatar.line.fill.background()

    # Text Box
    text_box = slide.shapes.add_textbox(
        x - size/2, y + size*0.5, size, size*0.5
    )
    tf = text_box.text_frame
    tf.word_wrap = True
    
    p_name = tf.paragraphs[0]
    p_name.text = name
    p_name.font.bold = True
    p_name.font.size = Pt(10)
    p_name.font.color.rgb = RGBColor(50, 50, 50)
    p_name.alignment = PP_ALIGN.CENTER
    
    p_role = tf.add_paragraph()
    p_role.text = role
    p_role.font.size = Pt(8)
    p_role.font.color.rgb = RGBColor(120, 120, 120)
    p_role.alignment = PP_ALIGN.CENTER

    return {"bottom_x": x, "bottom_y": y + size}

def draw_connection(slide, start_pos, end_pos):
    """Draws a line with a small anchor circle connecting two points."""
    line = slide.shapes.add_connector(
        MSO_SHAPE.LINE_INVERSE, 
        start_pos[0], start_pos[1], end_pos[0], end_pos[1]
    )
    line.line.color.rgb = RGBColor(180, 180, 180)
    line.line.width = Pt(1.5)

    # Add small joint circle
    joint_size = Inches(0.1)
    joint = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, end_pos[0] - joint_size/2, end_pos[1] - joint_size/2, joint_size, joint_size
    )
    joint.fill.solid()
    joint.fill.fore_color.rgb = RGBColor(180, 180, 180)
    joint.line.fill.background()


def create_slide(
    output_pptx_path: str,
    title_text: str = "Organizational Chart",
    body_text: str = "",
    bg_palette: str = "light", 
    accent_color: tuple = (0, 150, 136),  # Not strictly used as departments have their own
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Modern Layered-Pill Organizational Chart visual effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Background ===
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(235, 240, 245) # Soft pale blue/gray
    bg.line.fill.background()

    # === Layer 2: Visual Effect (Org Chart Nodes) ===
    
    # Chart Parameters
    center_x = prs.slide_width / 2
    top_y = Inches(1.0)
    tier_2_y = Inches(3.5)
    tier_3_y = Inches(5.0)
    node_w = Inches(2.2)
    node_h = Inches(0.8)
    
    # Department Colors
    colors = [
        RGBColor(0, 150, 136),   # Teal
        RGBColor(211, 47, 47),   # Red
        RGBColor(25, 118, 210),  # Blue
        RGBColor(245, 124, 0),   # Orange
        RGBColor(56, 142, 60)    # Green
    ]

    # Draw Top Node
    ceo_node = draw_top_node(slide, center_x, top_y, Inches(1.6), colors[2], "MARK JOHNSON", "Chief Executive")

    # Draw Tier 2 Nodes (Managers)
    tier_2_x_positions = [
        center_x - Inches(3),
        center_x,
        center_x + Inches(3)
    ]
    
    t2_nodes = []
    for i, x in enumerate(tier_2_x_positions):
        c_idx = i * 2 # Pick alternating colors
        node_pts = draw_pill_node(slide, x - node_w/2, tier_2_y, node_w, node_h, colors[c_idx], "NAME SURNAME", "Manager")
        t2_nodes.append(node_pts)
        # Connect to CEO
        draw_connection(slide, (ceo_node["bottom_x"], ceo_node["bottom_y"]), (node_pts["top_x"], node_pts["top_y"]))

    # Draw Tier 3 Nodes (Subordinates under first manager)
    tier_3_x_positions = [
        tier_2_x_positions[0] - Inches(1.2),
        tier_2_x_positions[0] + Inches(1.2)
    ]
    
    for i, x in enumerate(tier_3_x_positions):
        node_pts = draw_pill_node(slide, x - node_w/2, tier_3_y, node_w, node_h, colors[0], "NAME SURNAME", "Specialist")
        # Connect to Manager 1
        draw_connection(slide, (t2_nodes[0]["bottom_x"], t2_nodes[0]["bottom_y"]), (node_pts["top_x"], node_pts["top_y"]))

    # Draw Tier 3 Nodes (Subordinates under third manager)
    tier_3_x_positions_right = [
        tier_2_x_positions[2] - Inches(1.2),
        tier_2_x_positions[2] + Inches(1.2)
    ]
    
    for i, x in enumerate(tier_3_x_positions_right):
        node_pts = draw_pill_node(slide, x - node_w/2, tier_3_y, node_w, node_h, colors[4], "NAME SURNAME", "Specialist")
        # Connect to Manager 3
        draw_connection(slide, (t2_nodes[2]["bottom_x"], t2_nodes[2]["bottom_y"]), (node_pts["top_x"], node_pts["top_y"]))

    # === Layer 3: Text & Title ===
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(5), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(24)
    p.font.name = "Montserrat"
    p.font.color.rgb = RGBColor(50, 50, 50)

    prs.save(output_pptx_path)
    return output_pptx_path
```

#### 3c. Verification Checklist
- [x] Does the code import all required libraries? (Yes, `pptx`, `lxml.etree`).
- [x] Does it handle the case where an image download fails (fallback)? (N/A, uses native shapes entirely).
- [x] Are all color values explicit RGBA/RGB tuples? (Yes, heavily uses explicit `RGBColor` constants to match video).
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes, the layered pills, distinct colors, and drop shadows create the exact aesthetic).
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes, the color band mechanism is faithfully reproduced).