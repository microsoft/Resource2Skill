# Alternating Milestone Node Timeline

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Alternating Milestone Node Timeline

* **Core Visual Mechanism**: A horizontal chronology anchored by a central linear axis. Information branches alternatively upwards and downwards via connecting stems, terminating in geometric nodes (circles) that house numerical identifiers. Native drop shadows give these nodes a modern, tactile depth ("glassmorphism/material" hints), while pill-shaped badges highlight specific dates directly on the axis.
* **Why Use This Skill (Rationale)**: Bullet points fail to convey progression over time. This alternating layout maximizes horizontal and vertical screen real estate, preventing the "staircase effect" (text overlapping or crowding) common in sequential lists. The geometric alignment guides the viewer's eye rhythmically across the timeline.
* **Overall Applicability**: Essential for Product Launch Roadmaps, Quarterly Planning Overviews, Strategic Company Milestones, and Go-To-Market strategy slides.
* **Value Addition**: Transforms a dry chronological list into an executive-level visual dashboard. The injection of XML-based soft drop shadows elevates standard PowerPoint vectors to the level of modern UI/SaaS design assets.


### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Framework**: Light neutral gray axis and stems (`#CBD5E1` / `203, 213, 225`).
  - **Thematic Nodes & Pills**: Vibrant accent colors to segment phases.
    - *Phase 1 (Concept)*: Blue `(59, 130, 246)`
    - *Phase 2 (Develop)*: Emerald `(16, 185, 129)`
    - *Phase 3 (Beta)*: Amber `(245, 158, 11)`
    - *Phase 4 (Launch)*: Rose `(239, 68, 68)`
    - *Phase 5 (Scale)*: Purple `(139, 92, 246)`
  - **Text Hierarchy**: 
    - *Slide Title*: 28pt, Dark Navy, Bold.
    - *Node Badge*: 14pt, White, Bold (e.g., "01").
    - *Date Pill*: 10pt, White, Bold (e.g., "Q1 2024").
    - *Milestone Title*: 14pt, Color-matched to node, Bold.
    - *Milestone Body*: 11pt, Dark Gray, Regular.

* **Step B: Compositional Style**
  - **Spatial Rhythm**: Symmetrical distribution across a 13.33" widescreen. The central axis sits slightly below the vertical center (at Y=4.1 inches) to allow room for the main slide title and subtitle at the top.
  - **Alternation**: Even-indexed items extend *above* the axis; odd-indexed items extend *below* the axis.
  - **Layering**: The main horizontal axis is on the bottom layer. Connecting stems layer above it. Nodes and Date Pills sit on the very top layer, popping off the canvas using subtle drop shadows (alpha=25%).

* **Step C: Dynamic Effects & Transitions**
  - *Code-Generated*: Soft XML drop shadows on the overlapping nodes ensure depth separation without relying on image compositing, keeping the slide 100% editable.
  - *Recommended Manual Animation*: Add a "Wipe" (From Left) to the central line, followed by a sequential "Zoom" animation for each node and text group.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Base layout, Text & Lines** | `python-pptx` native | Provides exact spatial positioning while keeping text perfectly editable for the end-user. |
| **Node Depth (Drop Shadows)** | `lxml` XML injection | `python-pptx` lacks a native API for shape shadows. Injecting `<a:effectLst>` directly into the shape's XML perfectly reproduces the modern UI depth seen in the tutorial template. |
| **Geometry Alignment** | Math / Algorithm | Calculated alternating Y-coordinates ensure flush connections between stems, circles, and bounding boxes. |

> **Feasibility Assessment**: 100%. By combining native shape placement with direct XML manipulation for rendering effects (shadows, precise line endpoints), the generated slide perfectly replicates the modern corporate roadmap style.

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml import parse_xml

def add_modern_shadow(shape, alpha=25, blur=5, distance=3, angle=45):
    """
    Injects a modern, soft drop shadow into a python-pptx shape using lxml.
    alpha: percentage (0-100)
    blur: points
    distance: points
    angle: degrees
    """
    # Convert points to EMUs (1 pt = 12700 EMUs)
    dist_emu = int(distance * 12700)
    blur_emu = int(blur * 12700)
    # Convert degrees to 60000ths of a degree
    dir_angle = int(angle * 60000)
    # Convert alpha to 1000ths of a percent (e.g., 25% = 25000)
    alpha_val = int(alpha * 1000)

    shadow_xml = f"""
    <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:outerShdw blurRad="{blur_emu}" dist="{dist_emu}" dir="{dir_angle}" algn="tl" rotWithShape="0">
            <a:srgbClr val="000000">
                <a:alpha val="{alpha_val}"/>
            </a:srgbClr>
        </a:outerShdw>
    </a:effectLst>
    """
    effect_lst = parse_xml(shadow_xml)
    shape.element.spPr.append(effect_lst)

def create_slide(
    output_pptx_path: str,
    title_text: str = "Product Launch Roadmap",
    subtitle_text: str = "Strategic timeline and core milestones for go-to-market execution.",
    milestones: list = None,
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing an alternating milestone node timeline.
    """
    if milestones is None:
        milestones = [
            {"date": "Q1 2024", "title": "Concept & Strategy", "desc": "Market research, competitive analysis, and core product ideation phase.", "color": (59, 130, 246)},
            {"date": "Q2 2024", "title": "Prototyping", "desc": "Develop initial wireframes, UI/UX flows, and scalable architecture.", "color": (16, 185, 129)},
            {"date": "Q3 2024", "title": "Beta Release", "desc": "Closed beta testing with key stakeholders to gather critical feedback.", "color": (245, 158, 11)},
            {"date": "Q4 2024", "title": "Launch Prep", "desc": "Finalize marketing materials, sales enablement, and final QA testing.", "color": (239, 68, 68)},
            {"date": "Q1 2025", "title": "Public Launch", "desc": "Global product rollout, PR campaign, and initial user acquisition.", "color": (139, 92, 246)},
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Base Colors
    text_dark = RGBColor(15, 23, 42)
    text_gray = RGBColor(71, 85, 105)
    line_gray = RGBColor(203, 213, 225)

    # === 1. Slide Title & Subtitle ===
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(0.4), Inches(11.333), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = 'Arial'
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = text_dark

    sub_p = tf.add_paragraph()
    sub_p.text = subtitle_text
    sub_p.font.name = 'Arial'
    sub_p.font.size = Pt(14)
    sub_p.font.color.rgb = text_gray

    # === 2. Layout Mathematics ===
    num_items = len(milestones)
    start_x = 1.5
    end_x = 11.833
    axis_y = 4.1  # Central horizontal line position

    # Spacing between items
    spacing = (end_x - start_x) / (num_items - 1) if num_items > 1 else 0

    # === 3. Draw Central Axis ===
    axis_line = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT, Inches(0.8), Inches(axis_y), Inches(12.5), Inches(axis_y)
    )
    axis_line.line.color.rgb = line_gray
    axis_line.line.width = Pt(3)

    # === 4. Render Milestones ===
    stem_len = 1.0        # Length of vertical line
    circle_r = 0.35       # Radius of the node circle
    date_w, date_h = 1.2, 0.35  # Dimensions of the date pill
    text_w = 2.2          # Width of the text box
    
    for i, m in enumerate(milestones):
        x = start_x + (i * spacing)
        is_top = (i % 2 == 0)
        dir_mult = -1 if is_top else 1
        
        node_color = RGBColor(*m['color'])

        # -- A. Stem Line --
        stem_start_y = axis_y
        stem_end_y = axis_y + (stem_len * dir_mult)
        stem = slide.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(stem_start_y), Inches(x), Inches(stem_end_y)
        )
        stem.line.color.rgb = line_gray
        stem.line.width = Pt(2)

        # -- B. Node Circle --
        # Align circle perfectly flush with the end of the stem
        circle_cy = stem_end_y + (circle_r * dir_mult)
        circle_top = circle_cy - circle_r
        circle_left = x - circle_r

        node = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, Inches(circle_left), Inches(circle_top), Inches(circle_r*2), Inches(circle_r*2)
        )
        node.fill.solid()
        node.fill.fore_color.rgb = node_color
        node.line.color.rgb = RGBColor(255, 255, 255)
        node.line.width = Pt(2)
        add_modern_shadow(node, alpha=25, blur=6, distance=3, angle=90)

        # Node Text (01, 02, etc.)
        node_tf = node.text_frame
        node_tf.margin_left = node_tf.margin_right = node_tf.margin_top = node_tf.margin_bottom = 0
        node_p = node_tf.paragraphs[0]
        node_p.text = f"{i+1:02d}"
        node_p.alignment = PP_ALIGN.CENTER
        node_p.font.name = 'Arial'
        node_p.font.size = Pt(14)
        node_p.font.bold = True
        node_p.font.color.rgb = RGBColor(255, 255, 255)

        # -- C. Date Pill (on the axis) --
        pill_left = x - (date_w / 2)
        pill_top = axis_y - (date_h / 2)
        pill = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(pill_left), Inches(pill_top), Inches(date_w), Inches(date_h)
        )
        pill.fill.solid()
        pill.fill.fore_color.rgb = node_color
        pill.line.fill.background() # No line
        add_modern_shadow(pill, alpha=15, blur=3, distance=2, angle=90)

        pill_tf = pill.text_frame
        pill_tf.margin_left = pill_tf.margin_right = pill_tf.margin_top = pill_tf.margin_bottom = 0
        pill_p = pill_tf.paragraphs[0]
        pill_p.text = m['date']
        pill_p.alignment = PP_ALIGN.CENTER
        pill_p.font.name = 'Arial'
        pill_p.font.size = Pt(10)
        pill_p.font.bold = True
        pill_p.font.color.rgb = RGBColor(255, 255, 255)

        # -- D. Text Content Box --
        text_left = x - (text_w / 2)
        if is_top:
            text_top = circle_top - 1.4  # Place above the top circle
        else:
            text_top = circle_top + (circle_r * 2) + 0.2  # Place below the bottom circle

        content_box = slide.shapes.add_textbox(Inches(text_left), Inches(text_top), Inches(text_w), Inches(1.2))
        c_tf = content_box.text_frame
        c_tf.word_wrap = True
        
        # Title
        title_p = c_tf.paragraphs[0]
        title_p.text = m['title']
        title_p.alignment = PP_ALIGN.CENTER
        title_p.font.name = 'Arial'
        title_p.font.size = Pt(12)
        title_p.font.bold = True
        title_p.font.color.rgb = node_color

        # Description
        desc_p = c_tf.add_paragraph()
        desc_p.text = m['desc']
        desc_p.alignment = PP_ALIGN.CENTER
        desc_p.font.name = 'Arial'
        desc_p.font.size = Pt(10)
        desc_p.font.color.rgb = text_gray
        # Add a little spacing before the description
        desc_p.space_before = Pt(4)

    prs.save(output_pptx_path)
    return output_pptx_path
```