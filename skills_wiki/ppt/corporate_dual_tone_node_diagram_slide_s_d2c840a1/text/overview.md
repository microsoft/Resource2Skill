# Corporate Dual-Tone Node Diagram (Slide Science Style)

## Analysis

### 0. Clarification on the Source Material

**Crucial Note**: The provided video is a tutorial on a **PowerPoint application feature** (how to organize slides into "Sections" in the left-hand thumbnail pane to manage massive decks), rather than a tutorial on slide design or visual aesthetics. 

Because PowerPoint "Sections" are purely an authoring UI feature and do not have a visual representation on the actual slide canvas, it is impossible to write code that visually "reproduces" sections as a graphical effect. 

However, to fulfill the objective of extracting a reusable design skill, I have analyzed the **Slide Science template deck** shown *within* the video (specifically around 0:24 - 0:43). The code and breakdown below extract the core aesthetic of those templates: clean, geometric vector diagrams using a specific dual-tone corporate color palette.


---

### 1. High-level Design Pattern Extraction

> **Skill Name**: Corporate Dual-Tone Node Diagram (Slide Science Style)

* **Core Visual Mechanism**: The defining style is flat, highly structured geometric vector shapes (circles, chevrons, overlapping rings) used to build process diagrams. It relies heavily on a strict, high-contrast dual-tone color palette (a deep, dark purple paired with a vibrant, energetic magenta) set against clean white or light gray backgrounds, accented with thick white stroke borders for separation.
* **Why Use This Skill (Rationale)**: Complex processes can easily become cluttered. Using strict geometric constraints (perfect circles, symmetrical layouts) and limiting the palette to only two primary semantic colors reduces cognitive load. The vibrant magenta acts as a natural highlight against the heavier, stable purple base.
* **Overall Applicability**: Ideal for corporate template packs, standardizing process flows, strategy models, and organizational charts. It works best when you need to make dry, structural information look polished and proprietary.
* **Value Addition**: Transforms standard bullet points or default SmartArt into a custom-looking, branded vector graphic that feels like it belongs in a premium consulting deck.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Element Types**: Perfect circles (`MSO_SHAPE.OVAL`), straight line connectors, thick shape outlines.
  * **Color Logic**:
    * Background: Off-white/Light Gray `(245, 245, 247)` to make white borders pop.
    * Primary Anchor Color (Deep Purple): `(43, 22, 114)` — used for central hubs and structural lines.
    * Highlight/Action Color (Vibrant Magenta): `(216, 27, 96)` — used for surrounding steps or action nodes.
    * Separators: Pure White `(255, 255, 255)` — used as a 3pt to 4pt border on all shapes to create clean separation when objects overlap or touch.
  * **Text Hierarchy**: Bold, capitalized sans-serif text inside shapes (white text for contrast).

* **Step B: Compositional Style**
  * **Symmetry**: The layouts rely on perfect center alignment. Satellite nodes are spaced evenly around a central hub (e.g., at 0°, 90°, 180°, 270°).
  * **Proportions**: Satellite nodes are typically ~60-70% the size of the central hub to establish a clear hierarchy.

* **Step C: Dynamic Effects & Transitions**
  * Typically, template packs like this rely on static clarity. If animated, they use simple "Fade" or "Wipe" effects sequentially to reveal steps.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Geometric Process Nodes** | `python-pptx` native | The template style relies purely on standard vector geometry (circles, lines). Using native shapes ensures the text inside them remains fully editable by the final user. |
| **Color & Stroke Styling** | `python-pptx` native | We can easily set the exact RGB fill colors and thick white border lines required to match the aesthetic using standard shape properties. |

> **Feasibility Assessment**: 100% of the *slide canvas aesthetic* shown in the template deck can be reproduced via code. (As noted, the UI "Sections" feature itself cannot be coded onto a slide).

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Process Architecture",
    **kwargs
) -> str:
    """
    Creates a PPTX file featuring a dual-tone circular node diagram,
    extracting the aesthetic of the template deck shown in the tutorial.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    import math

    prs = Presentation()
    # 16:9 widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Style Palette ===
    color_bg = RGBColor(248, 248, 250)
    color_purple = RGBColor(43, 22, 114)
    color_magenta = RGBColor(216, 27, 96)
    color_white = RGBColor(255, 255, 255)

    # === Background ===
    # Set a very light gray background so the white shape borders stand out
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color_bg

    # === Title Section ===
    title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.333), Inches(1))
    tf = title_box.text_frame
    p = tf.add_paragraph()
    p.text = title_text
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = color_purple

    # === Diagram Layout Parameters ===
    center_x = Inches(13.333 / 2)
    center_y = Inches(4.2)
    orbit_radius = Inches(2.3)
    
    hub_size = Inches(2.2)
    node_size = Inches(1.5)

    # === Connectors (Lines drawn first so they sit behind shapes) ===
    # Draw simple lines radiating from the center to the 4 compass points
    angles = [0, 90, 180, 270]
    for angle in angles:
        rad = math.radians(angle)
        end_x = center_x + orbit_radius * math.cos(rad)
        end_y = center_y + orbit_radius * math.sin(rad)
        
        # 1 = msoConnectorStraight
        connector = slide.shapes.add_connector(1, center_x, center_y, end_x, end_y)
        connector.line.color.rgb = color_purple
        connector.line.width = Pt(2.5)

    # === Central Hub (Purple) ===
    hub = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, 
        center_x - hub_size/2, center_y - hub_size/2, 
        hub_size, hub_size
    )
    hub.fill.solid()
    hub.fill.fore_color.rgb = color_purple
    hub.line.color.rgb = color_white
    hub.line.width = Pt(4) # Thick white border is characteristic of this style
    
    tf_hub = hub.text_frame
    tf_hub.word_wrap = True
    p_hub = tf_hub.paragraphs[0]
    p_hub.text = "CORE\nSYSTEM"
    p_hub.alignment = PP_ALIGN.CENTER
    p_hub.font.size = Pt(18)
    p_hub.font.bold = True
    p_hub.font.color.rgb = color_white

    # === Satellite Nodes (Magenta) ===
    node_labels = ["Phase 1\nPlan", "Phase 2\nDesign", "Phase 3\nBuild", "Phase 4\nTest"]
    
    for i, angle in enumerate(angles):
        rad = math.radians(angle)
        nx = center_x + orbit_radius * math.cos(rad)
        ny = center_y + orbit_radius * math.sin(rad)
        
        node = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            nx - node_size/2, ny - node_size/2, 
            node_size, node_size
        )
        node.fill.solid()
        node.fill.fore_color.rgb = color_magenta
        node.line.color.rgb = color_white
        node.line.width = Pt(3)
        
        tf_node = node.text_frame
        tf_node.word_wrap = True
        p_node = tf_node.paragraphs[0]
        p_node.text = node_labels[i]
        p_node.alignment = PP_ALIGN.CENTER
        p_node.font.size = Pt(14)
        p_node.font.bold = True
        p_node.font.color.rgb = color_white

    prs.save(output_pptx_path)
    return output_pptx_path
```