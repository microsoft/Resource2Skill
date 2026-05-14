# Dual-Phase Split Roadmap (Traction & Vision)

## Analysis

Based on the transcript provided by the venture capitalist discussing the perfect 8-slide pitch deck, one of the most vividly described and highly effective visual mechanisms is the **Slide 5: Traction Timeline**. 

The speaker specifically highlights showing a timeline split into two distinct eras: **"In 9 Months" (Past Execution) vs. "Next 9 Months" (Future Roadmap)**, peppered with monetary milestones and partner logos. This creates a powerful narrative of momentum.

Here is the extraction of this design pattern and the complete Python code to reproduce it.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dual-Phase Split Roadmap (Traction & Vision)

* **Core Visual Mechanism**: The slide is split exactly 50/50 down the middle using two highly contrasting background colors. A continuous horizontal axis runs across both halves. The left half maps past achievements (Traction), while the right half maps future projections (Roadmap). Nodes mark key milestones with alternating top/bottom text layouts.
* **Why Use This Skill (Rationale)**: Psychologically, this layout immediately establishes the startup's core pitch: *"We execute on our promises (left side), therefore you should believe our future projections (right side)."* The continuous line visually links past momentum to future growth, while the color split clearly delineates proven facts from ambitious goals.
* **Overall Applicability**: Pitch decks (Traction/Roadmap slide), Quarterly Business Reviews (Last Q vs. Next Q), Product Launch timelines, and Strategic Planning updates.
* **Value Addition**: Compared to a standard bulleted list or a generic single-color timeline, this split layout creates an immediate sense of scale and momentum. It prevents the audience from confusing past achievements with future goals while making the data highly scannable.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background Split**: Two massive rectangles. Left (Past) uses a deep, grounding color like Dark Navy `(15, 23, 42)`. Right (Future) uses a vibrant, forward-looking accent color like Vibrant Coral `(255, 107, 107)` or Cyan.
  - **The Axis**: A thick, continuous line spanning 90% of the slide width, bridging the two color zones.
  - **The Nodes**: Crisp white circular markers.
  - **Text Hierarchy**: 
    - *Era Titles*: Massive, bold, ultra-light text at the top of each zone (e.g., "PAST 9 MONTHS").
    - *Metrics*: Large, bold numbers (e.g., "€150K", "1.2M Users").
    - *Dates/Descriptions*: Smaller, muted secondary text.

* **Step B: Compositional Style**
  - **Spatial Feel**: Balanced but dynamic. The 50/50 split commands attention. 
  - **Rhythm**: Alternating data points (above the line, below the line) to prevent visual clustering and allow for large typography.
  - **Depth**: Soft drop shadows applied to the timeline nodes to make them float above the flat color block background.

* **Step C: Dynamic Effects & Transitions**
  - *In Presentation*: A standard "Wipe" or "Push" transition from the left works best here. You can also use "Fade" animations to reveal the past milestones sequentially, followed by the future milestones.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **50/50 Split Background** | `python-pptx` native shapes | Standard rectangles easily achieve the sharp vertical color boundary. |
| **Timeline Elements & Text** | `python-pptx` native shapes | Standard lines, circles, and text boxes are perfect for crisp vector rendering of timelines. |
| **Node Depth (Floating circles)** | `lxml` XML injection | Native `python-pptx` lacks a direct API for drop shadows. We inject `<a:outerShdw>` into the shape's XML to make the nodes pop off the flat background. |

> **Feasibility Assessment**: 100% reproduction. The code below constructs a pixel-perfect, highly professional dual-phase timeline entirely via Python, matching the aesthetic of top-tier venture capital pitch decks.

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement

def add_drop_shadow(shape):
    """
    Injects OpenXML to add a professional drop shadow to a python-pptx shape.
    """
    spPr = shape.element.spPr
    effectLst = OxmlElement('a:effectLst')
    outerShdw = OxmlElement('a:outerShdw')
    
    # Shadow properties: blur radius, distance, direction, angle
    outerShdw.set('blurRad', str(Emu(Pt(5))))
    outerShdw.set('dist', str(Emu(Pt(3))))
    outerShdw.set('dir', '2700000') # 45 degrees
    outerShdw.set('algn', 'ctr')
    
    # Shadow color (Black with 40% opacity)
    srgbClr = OxmlElement('a:srgbClr')
    srgbClr.set('val', '000000')
    alpha = OxmlElement('a:alpha')
    alpha.set('val', '40000') # 40% opacity
    srgbClr.append(alpha)
    
    outerShdw.append(srgbClr)
    effectLst.append(outerShdw)
    spPr.append(effectLst)

def create_slide(
    output_pptx_path: str,
    title_text: str = "Traction & Roadmap",
    past_title: str = "PAST 9 MONTHS",
    future_title: str = "NEXT 9 MONTHS",
    color_past: tuple = (15, 23, 42),      # Dark Navy
    color_future: tuple = (255, 107, 107), # Vibrant Coral
    **kwargs
) -> str:
    """
    Creates a Dual-Phase Split Timeline slide typical in VC pitch decks.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Split Background ===
    # Left Half (Past)
    left_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(6.6665), Inches(7.5))
    left_bg.fill.solid()
    left_bg.fill.fore_color.rgb = RGBColor(*color_past)
    left_bg.line.fill.background()

    # Right Half (Future)
    right_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.6665), 0, Inches(6.6665), Inches(7.5))
    right_bg.fill.solid()
    right_bg.fill.fore_color.rgb = RGBColor(*color_future)
    right_bg.line.fill.background()

    # === Layer 2: Main Axis Line ===
    # Horizontal line crossing both halves
    axis_y = Inches(4.2)
    axis = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        Inches(1.0), axis_y - Pt(2), Inches(11.333), Pt(4)
    )
    axis.fill.solid()
    axis.fill.fore_color.rgb = RGBColor(255, 255, 255)
    axis.line.fill.background()

    # Center Marker ("TODAY")
    center_y = axis_y - Inches(0.4)
    today_box = slide.shapes.add_textbox(Inches(6.0), center_y, Inches(1.333), Inches(0.5))
    tf = today_box.text_frame
    tf.text = "TODAY"
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    center_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.65), axis_y - Inches(0.2), Pt(3), Inches(0.4))
    center_line.fill.solid()
    center_line.fill.fore_color.rgb = RGBColor(255, 255, 255)
    center_line.line.fill.background()

    # === Layer 3: Section Headers ===
    def add_header(text, x, y, width, align):
        tb = slide.shapes.add_textbox(x, y, width, Inches(1.0))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = text
        p.alignment = align
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
    
    add_header(past_title, Inches(1.0), Inches(0.5), Inches(5.0), PP_ALIGN.LEFT)
    add_header(future_title, Inches(7.333), Inches(0.5), Inches(5.0), PP_ALIGN.RIGHT)

    # Main Slide Title (Optional, subtle in top left)
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.2), Inches(5.0), Inches(0.5))
    title_p = title_box.text_frame.paragraphs[0]
    title_p.text = title_text.upper()
    title_p.font.size = Pt(12)
    title_p.font.color.rgb = RGBColor(150, 160, 180) # Muted text
    title_p.font.bold = True

    # === Layer 4: Timeline Milestones ===
    milestones = [
        # Past (Left Side)
        {"date": "Sep '18", "metric": "€150K", "desc": "Seed Round", "x": 1.5, "is_top": True},
        {"date": "Jan '19", "metric": "€80K", "desc": "Monthly MRR", "x": 3.2, "is_top": False},
        {"date": "Jun '19", "metric": "1.2M", "desc": "Active Users", "x": 4.9, "is_top": True},
        # Future (Right Side)
        {"date": "Mar '20", "metric": "€1M", "desc": "Series A Target", "x": 8.0, "is_top": False},
        {"date": "Dec '20", "metric": "Microsoft", "desc": "B2B Partnership", "x": 10.0, "is_top": True},
        {"date": "Q4 '21", "metric": "5.0M", "desc": "Global Users", "x": 11.7, "is_top": False},
    ]

    node_radius = Inches(0.15)

    for i, ms in enumerate(milestones):
        # Draw Circular Node
        node = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            Inches(ms['x']) - node_radius, 
            axis_y - node_radius, 
            node_radius * 2, 
            node_radius * 2
        )
        node.fill.solid()
        node.fill.fore_color.rgb = RGBColor(255, 255, 255)
        node.line.color.rgb = RGBColor(*color_past) if ms['x'] < 6.6 else RGBColor(*color_future)
        node.line.width = Pt(3)
        add_drop_shadow(node) # Add depth

        # Calculate Text Y positions
        box_width = Inches(2.0)
        box_x = Inches(ms['x']) - (box_width / 2)
        
        if ms['is_top']:
            tb_y = axis_y - Inches(1.8)
        else:
            tb_y = axis_y + Inches(0.4)

        # Draw Milestone Text Box
        tb = slide.shapes.add_textbox(box_x, tb_y, box_width, Inches(1.5))
        tf = tb.text_frame
        tf.clear()
        
        # Paragraph 1: Metric (Huge, Bold)
        p1 = tf.paragraphs[0]
        p1.text = ms['metric']
        p1.alignment = PP_ALIGN.CENTER
        p1.font.size = Pt(28)
        p1.font.bold = True
        p1.font.color.rgb = RGBColor(255, 255, 255)
        
        # Paragraph 2: Description
        p2 = tf.add_paragraph()
        p2.text = ms['desc']
        p2.alignment = PP_ALIGN.CENTER
        p2.font.size = Pt(14)
        p2.font.bold = True
        p2.font.color.rgb = RGBColor(255, 255, 255)
        
        # Paragraph 3: Date
        p3 = tf.add_paragraph()
        p3.text = ms['date']
        p3.alignment = PP_ALIGN.CENTER
        p3.font.size = Pt(12)
        p3.font.color.rgb = RGBColor(200, 200, 200) if ms['x'] < 6.6 else RGBColor(255, 200, 200)

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
```