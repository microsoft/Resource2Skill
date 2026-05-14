# Radiating Branch Infographic Panel

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Radiating Branch Infographic Panel

* **Core Visual Mechanism**: A large central "hub" (usually a circle) from which multiple "arms" or "branches" radiate outwards. These arms start condensed and parallel, then fan out vertically to attach smoothly to rounded content panels. The design utilizes a monochromatic or analogous color progression (e.g., dark teal to light green) to create visual hierarchy and flow. Drop shadows on floating elements (the central hub and outer icon nodes) create depth.
* **Why Use This Skill (Rationale)**: This layout visually reinforces the concept of a central idea breaking down into constituent parts, or a single origin point distributing into multiple parallel tracks. The flowing, curved/angled arms smoothly guide the viewer's eye from the main topic to the details.
* **Overall Applicability**: Perfect for "Core Pillars", "5 Steps to Success", "Features & Benefits", or any breakdown of a central thesis into 4-6 distinct components. It serves well as a presentation hero slide or a summary infographic.
* **Value Addition**: Replaces boring bullet points with a highly professional, cohesive graphic that implies synergy and structure. The custom fanning arms give it a premium "Adobe Illustrator" feel that is rarely seen in native PowerPoint designs.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Hub**: A large white circle with a drop shadow, containing the main title.
  * **Branches (Arms)**: Custom polygons that start at a uniform narrow width behind the hub, remain parallel for a short distance (the "trunk"), and then flare out to match the height of the right-side panels.
  * **Content Panels**: Standard rounded rectangles.
  * **Nodes**: Smaller white circles sitting on the outer edge of the content panels, acting as icon containers.
  * **Color Palette** (Teal/Green progression):
    * Step 1: Dark Teal `(26, 83, 92)`
    * Step 2: Teal `(46, 129, 123)`
    * Step 3: Sea Green `(68, 181, 156)`
    * Step 4: Soft Green `(118, 200, 147)`
    * Step 5: Light Green `(153, 217, 140)`

* **Step B: Compositional Style**
  * **Layout**: Left-weighted hub (approx. 25% of slide width), middle transition zone (approx. 25%), right-weighted content stacks (approx. 50%).
  * **Spacing**: The right-side panels have consistent vertical gaps (~0.2 inches). The arms seamlessly bridge the gap without overlapping.

* **Step C: Dynamic Effects & Transitions**
  * Uses PPTX native outer drop shadows to lift the central hub and the right-side nodes off the flat canvas, creating a subtle 3D layered effect.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Radiating Arms / Branches** | `python-pptx` `FreeformBuilder` | Standard PPTX shapes cannot achieve the "fan out from a tight trunk" look. We must calculate the geometry and draw custom polygons. |
| **Drop Shadows** | `lxml` XML injection | `python-pptx` does not expose an API for adding shadows to shapes. Injecting `<a:effectLst>` directly into the shape's XML perfectly replicates the video's shadow effects. |
| **Panels & Hubs** | `python-pptx` native | Standard rounded rectangles and circles handle the layout perfectly. |

*Feasibility Assessment*: 95%. The code mathematically calculates the custom geometric arm shapes drawn by hand in Adobe Illustrator in the video, producing a nearly identical radiating vector graphic natively in PowerPoint.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "HEADING\nHERE",
    body_text: str = "",
    bg_palette: str = "business",  
    accent_color: tuple = (0, 191, 255),  
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Radiating Branch Infographic Panel' visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from lxml import etree

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Color Palette from Dark Teal to Light Green
    colors = [
        RGBColor(26, 83, 92),
        RGBColor(46, 129, 123),
        RGBColor(68, 181, 156),
        RGBColor(118, 200, 147),
        RGBColor(153, 217, 140)
    ]

    # --- Helper Function: Add Shadow via lxml ---
    def add_drop_shadow(shape, blur_rad="150000", dist="50000", dir_ang="2700000", alpha="40000"):
        spPr = shape.element.spPr
        effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
        outerShdw = etree.SubElement(effectLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw', 
                                     blurRad=blur_rad, dist=dist, dir=dir_ang, algn="ctr", rotWithShape="0")
        srgbClr = etree.SubElement(outerShdw, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr', val="000000")
        etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', val=alpha)

    # --- Geometric Layout Variables ---
    num_steps = 5
    
    # Hub variables
    hub_cx = Inches(3.5)
    hub_cy = Inches(3.75)
    hub_r = Inches(1.8)
    
    # Right panel variables
    rect_w = Inches(4.5)
    rect_h = Inches(0.85)
    rect_x = Inches(7.0) # Left edge of rectangles
    spacing = Inches(0.2)
    total_h = (num_steps * rect_h) + ((num_steps - 1) * spacing)
    start_y = hub_cy - (total_h / 2)
    
    # Trunk variables (the narrow part of the arms behind the hub)
    trunk_h = Inches(0.25)
    trunk_gap = Inches(0.05)
    total_trunk_h = (num_steps * trunk_h) + ((num_steps - 1) * trunk_gap)
    trunk_start_y = hub_cy - (total_trunk_h / 2)
    trunk_x0 = hub_cx - Inches(0.5) # Start inside the hub
    trunk_x1 = hub_cx + Inches(1.8) # Point where they start fanning out
    
    # --- Layer 1: Draw the Radiating Arms and Panels ---
    for i in range(num_steps):
        color = colors[i]
        
        # 1. Calculate Arm Vertices
        t_top = trunk_start_y + i * (trunk_h + trunk_gap)
        t_bottom = t_top + trunk_h
        
        r_top = start_y + i * (rect_h + spacing)
        r_bottom = r_top + rect_h
        
        arm_x2 = rect_x + Inches(0.1) # Overlap slightly with rectangle to avoid seams
        
        # 2. Draw Freeform Arm
        builder = slide.shapes.build_freeform(trunk_x0, t_top)
        builder.add_line_segments([
            (trunk_x1, t_top),   # Top flat edge of trunk
            (arm_x2, r_top),     # Top angled edge
            (arm_x2, r_bottom),  # Right flat edge (hidden by rect)
            (trunk_x1, t_bottom),# Bottom angled edge
            (trunk_x0, t_bottom),# Bottom flat edge of trunk
            (trunk_x0, t_top)    # Close shape
        ])
        arm = builder.convert_to_shape()
        arm.fill.solid()
        arm.fill.fore_color.rgb = color
        arm.line.fill.background() # No outline
        
        # 3. Draw Rounded Rectangle Panel
        rect = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rect_x, r_top, rect_w, rect_h)
        rect.fill.solid()
        rect.fill.fore_color.rgb = color
        rect.line.fill.background()
        
        # Adjust rounded corner radius (lxml manipulation for adjust values)
        adjLst = rect.element.xpath('.//a:adjLst')
        if adjLst:
            for adj in adjLst[0]:
                if adj.get('name') == 'adj':
                    adj.set('fmla', 'val 50000') # Make corners very rounded
                    
        # 4. Add Text to Panel
        txBox = slide.shapes.add_textbox(rect_x + Inches(0.2), r_top, rect_w - Inches(1.0), rect_h)
        tf = txBox.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = f"HEADING HERE {i+1}"
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.font.size = Pt(14)
        
        p2 = tf.add_paragraph()
        p2.text = "Insert your detailed description text here. Explain the step."
        p2.font.color.rgb = RGBColor(255, 255, 255)
        p2.font.size = Pt(10)
        
        # 5. Draw Outer Node Circle
        node_r = Inches(0.4)
        node_cx = rect_x + rect_w - Inches(0.1)
        node_cy = r_top + (rect_h / 2)
        node = slide.shapes.add_shape(MSO_SHAPE.OVAL, node_cx - node_r, node_cy - node_r, node_r * 2, node_r * 2)
        node.fill.solid()
        node.fill.fore_color.rgb = RGBColor(255, 255, 255)
        node.line.color.rgb = color
        node.line.width = Pt(3)
        add_drop_shadow(node, blur_rad="80000", dist="30000", alpha="30000")

    # --- Layer 2: Draw the Central Hub (drawn last so it sits on top of the arms) ---
    hub = slide.shapes.add_shape(MSO_SHAPE.OVAL, hub_cx - hub_r, hub_cy - hub_r, hub_r * 2, hub_r * 2)
    hub.fill.solid()
    hub.fill.fore_color.rgb = RGBColor(255, 255, 255)
    hub.line.fill.background()
    add_drop_shadow(hub, blur_rad="250000", dist="0", dir_ang="0", alpha="25000") # Center glow/shadow
    
    # Hub Text
    hub_tx = slide.shapes.add_textbox(hub_cx - hub_r, hub_cy - Inches(0.5), hub_r * 2, Inches(1))
    htf = hub_tx.text_frame
    htf.word_wrap = True
    hp = htf.paragraphs[0]
    hp.alignment = PP_ALIGN.CENTER
    hp.text = title_text
    hp.font.bold = True
    hp.font.size = Pt(20)
    hp.font.color.rgb = RGBColor(50, 50, 50)

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
```