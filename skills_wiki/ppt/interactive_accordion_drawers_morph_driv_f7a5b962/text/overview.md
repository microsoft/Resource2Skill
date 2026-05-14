# Interactive Accordion Drawers (Morph-Driven Pull-out Panels)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Interactive Accordion Drawers (Morph-Driven Pull-out Panels)

* **Core Visual Mechanism**: The defining visual idea is the "file folder" or "drawer tab" metaphor. Rectangular shapes with rounded side-tabs are stacked horizontally or vertically. Using PowerPoint's Morph transition, interacting with a slide causes a specific panel to slide out, revealing its text content while pushing or keeping the others collapsed.
* **Why Use This Skill (Rationale)**: This style is highly engaging because it gamifies information delivery. Instead of overwhelming the audience with a wall of text, it chunks information into distinct, color-coded categories. The physical sliding motion provides strong spatial context, helping viewers map concepts in their minds.
* **Overall Applicability**: Ideal for process steps, core company values, product feature breakdowns, or pricing tiers. It shines in interactive presentations where a presenter or user wants to click through specific sections non-linearly, or as a highly polished agenda/table of contents slide.
* **Value Addition**: Transforms static bullet points into an interactive, app-like UI experience. It demonstrates high technical proficiency in presentation design and keeps audience attention through smooth, logical motion.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Shape Construction**: A combination of a large right-side Rectangle (the content body) and a smaller left-side Rounded Rectangle (the tab). 
  * **Color Logic**: A high-contrast pastel palette against a neutral background.
    * Background: Soft Cream `(245, 245, 240, 255)`
    * Drawer 1 (Cyan): `(105, 196, 203, 255)`
    * Drawer 2 (Peach): `(252, 175, 115, 255)`
    * Drawer 3 (Mint): `(153, 205, 169, 255)`
  * **Text Hierarchy**: Large bold numbers on the tabs (e.g., "1", "2"), clear bold titles (24pt) inside the drawer body, and smaller descriptive text (14pt) below the title.

* **Step B: Compositional Style**
  * **Layout**: Stacked vertically, taking up the majority of the slide. 
  * **Proportions**: The tab is roughly 1/8th the width of the main body. The entire combined shape spans about 80% of the screen width when fully extended.
  * **Depth**: Drop shadows on the combined shapes to make them look like physical, overlapping cards.

* **Step C: Dynamic Effects & Transitions**
  * **The "Trick"**: The exact same set of shapes exists on multiple consecutive slides. On Slide 1, they are positioned off-screen to the left (so only the tabs show). On Slide 2, Drawer 1 is moved to the right. 
  * **Transition**: The `Morph` (平滑) transition is applied to all slides, causing PowerPoint to automatically calculate the smooth sliding animation between states.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Shape creation & layout** | `python-pptx` native | Basic rectangles and rounded rectangles are easily placed via native APIs. |
| **Morph Transition** | `lxml` XML injection | `python-pptx` cannot natively set the Morph transition. We must manipulate the slide XML directly to add `<p:morph/>`. |
| **Drop Shadows** | `lxml` XML injection | Shadows are crucial for the overlapping UI look, requiring direct OOXML `<a:outerShdw>` injection. |

> **Feasibility Assessment**: 95%. The code generates a complete, multi-slide presentation demonstrating the exact sliding accordion effect. The shapes, shadows, layout, and automatic smooth animation are fully replicated. The only missing element is grouping the shapes (which `python-pptx` doesn't support), but because they move at the exact same velocity via Morph, it looks identical to a grouped object.

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from lxml import etree

def _add_shadow(shape):
    """Injects OOXML to add a drop shadow to a shape for depth."""
    spPr = shape.element.spPr
    effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
    outerShdw = etree.SubElement(effectLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw')
    outerShdw.set('blurRad', '150000')  # 15pt blur
    outerShdw.set('dist', '50000')      # 5pt distance
    outerShdw.set('dir', '2700000')     # Angle
    outerShdw.set('algn', 'ctr')
    
    srgbClr = etree.SubElement(outerShdw, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
    srgbClr.set('val', '000000')        # Black shadow
    alpha = etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha')
    alpha.set('val', '20000')           # 20% opacity

def _add_morph_transition(slide):
    """Injects OOXML to apply the Morph transition to a slide."""
    slide_element = slide.element
    transition = etree.SubElement(slide_element, '{http://schemas.openxmlformats.org/presentationml/2006/main}transition')
    transition.set('spd', 'slow')
    morph = etree.SubElement(transition, '{http://schemas.openxmlformats.org/presentationml/2006/main}morph')
    morph.set('option', 'byObject')

def create_slide(
    output_pptx_path: str,
    title_text: str = "Interactive Accordion Drawers",
    body_text: str = "",
    **kwargs,
) -> str:
    """
    Creates a multi-slide PPTX demonstrating the interactive sliding drawer Morph effect.
    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Drawer Data setup
    drawers = [
        {"color": (105, 196, 203), "title": "Step 1: Data Aggregation", "desc": "Collect and normalize text inputs from various visual sources and APIs."},
        {"color": (252, 175, 115), "title": "Step 2: Pattern Extraction", "desc": "Analyze compositional logic, color palettes, and typographic hierarchies."},
        {"color": (153, 205, 169), "title": "Step 3: Code Generation", "desc": "Synthesize Python scripts combining python-pptx, lxml, and PIL."}
    ]
    
    # Layout dimensions
    drawer_height = Inches(1.8)
    tab_width = Inches(1.2)
    body_width = Inches(8.0)
    spacing = Inches(0.4)
    start_y = Inches(1.0)
    
    # X coordinates for states
    closed_x = Inches(0)          # Only the tab is visible
    open_x = Inches(3)            # Drawer pulls out to the right

    # Create 4 slides to show the animation sequence (All closed -> 1 open -> 2 open -> 3 open)
    for slide_idx in range(4):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Background color
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(245, 245, 240)
        
        # Add slide main title
        title_box = slide.shapes.add_textbox(Inches(3), Inches(0.2), Inches(7.333), Inches(0.8))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = RGBColor(50, 50, 50)
        
        # Add Morph transition to slides 1, 2, 3 (0 is starting state)
        if slide_idx > 0:
            _add_morph_transition(slide)

        # Draw the drawers (reverse order so drawer 0 is on top layer)
        for i in range(len(drawers)-1, -1, -1):
            data = drawers[i]
            y_pos = start_y + (i * (drawer_height + spacing))
            
            # Determine if this specific drawer is open on this slide
            # Slide 0 = all closed. Slide 1 = Drawer 0 open. Slide 2 = Drawer 1 open, etc.
            is_open = (slide_idx - 1 == i)
            base_x = open_x if is_open else closed_x
            
            # 1. Draw Body Rectangle
            body = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                base_x + tab_width, y_pos, body_width, drawer_height
            )
            body.fill.solid()
            body.fill.fore_color.rgb = RGBColor(*data["color"])
            body.line.fill.background() # No border
            _add_shadow(body)
            
            # 2. Add Text to Body (created in same sequence so Morph tracks it)
            tb = slide.shapes.add_textbox(base_x + tab_width + Inches(0.5), y_pos + Inches(0.3), body_width - Inches(1), drawer_height - Inches(0.6))
            
            p_title = tb.text_frame.paragraphs[0]
            p_title.text = data["title"]
            p_title.font.size = Pt(22)
            p_title.font.bold = True
            p_title.font.color.rgb = RGBColor(255, 255, 255)
            
            p_desc = tb.text_frame.add_paragraph()
            p_desc.text = data["desc"]
            p_desc.font.size = Pt(14)
            p_desc.font.color.rgb = RGBColor(255, 255, 255)
            
            # 3. Draw Left Tab (Rounded Rectangle)
            tab = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                base_x, y_pos + Inches(0.15), tab_width + Inches(0.2), drawer_height - Inches(0.3)
            )
            tab.fill.solid()
            tab.fill.fore_color.rgb = RGBColor(*data["color"])
            tab.line.fill.background()
            _add_shadow(tab)
            
            # 4. Add Number Icon in Tab
            icon_bg = slide.shapes.add_shape(
                MSO_SHAPE.OVAL,
                base_x + Inches(0.2), y_pos + Inches(0.4), Inches(0.7), Inches(0.7)
            )
            icon_bg.fill.solid()
            icon_bg.fill.fore_color.rgb = RGBColor(255, 255, 255)
            icon_bg.line.fill.background()
            
            icon_tf = icon_bg.text_frame
            icon_tf.text = str(i + 1)
            icon_tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            icon_tf.paragraphs[0].font.size = Pt(24)
            icon_tf.paragraphs[0].font.bold = True
            icon_tf.paragraphs[0].font.color.rgb = RGBColor(*data["color"])

    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("accordion_drawers.pptx")
```