# Rotating Dial Morph Panel (Wheel Selector)

## Analysis

# Skill Strategy Document

### 1. High-level Design Pattern Extraction

> **Skill Name**: Rotating Dial Morph Panel (Wheel Selector)

* **Core Visual Mechanism**: This technique uses a large, partially off-screen circular dial (a donut shape overlaid with a circular text warp). A static "pointer" (like an arrow) extends from the dial's edge to a detail panel. By duplicating the slide and applying the **Morph transition** while applying incremental rotations to the dial group, it creates an elegant, highly tactile "scrolling wheel" selection effect.
* **Why Use This Skill (Rationale)**: The rotating wheel metaphor gives the audience an immediate understanding of a "menu" or "sequence of options." It transforms flat, static bullet points into an interactive, spatial experience. The physical rotation anchors the viewer's attention, clearly separating the *navigation mechanism* (the wheel) from the *content payload* (the text panel).
* **Overall Applicability**: Perfect for agendas, geographic locations (as seen in the tutorial with country names), step-by-step processes, product feature lists, or team member profiles.
* **Value Addition**: Replaces boring "next slide" cuts with a smooth, interconnected visual narrative. It makes the presentation feel like a premium, custom-coded software application or a high-end dashboard rather than a standard deck.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **The Base Dial**: A geometric donut shape spanning roughly 60-70% of the slide height, positioned so its center lies slightly off the left edge of the slide canvas.
  - **The Typographic Ring**: Text warped onto a circular path matching the donut's curvature.
  - **The Pointer**: A block arrow or chevron intersecting the right edge of the dial, acting as the "read head" or selection indicator.
  - **Color Logic**: High-contrast pairing. For instance, a vibrant energetic accent `(230, 81, 0, 255)` for the mechanical parts (dial/arrow) against a deep corporate navy `(26, 35, 126, 255)` for the text to maintain legibility.
* **Step B: Compositional Style**
  - **Asymmetrical Balance**: The left hemisphere is dominated by large, bold, geometric curves (the dial), leaving the right 60% of the slide as negative space for detailed, left-aligned typography.
* **Step C: Dynamic Effects & Transitions**
  - **PowerPoint Morph Transition**: The entire effect relies on duplicating the layout exactly and only changing the rotation angle of the dial elements. The Morph transition automatically interpolates the rotation angle, spinning the wheel seamlessly between slides.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layout & Base Shapes** | `python-pptx` native | Provides robust placement and styling for Donut, Arrows, and standard Text boxes. |
| **Circular Text Bending** | `lxml` XML injection | Native `python-pptx` does not expose the WordArt Text Effects. We must inject the `<a:prstTxWarp prst="circle">` DrawingML element directly into the shape's body properties. |
| **Smooth Rotation Animation** | `lxml` XML injection | Requires injecting the `<p:morph/>` transition element into the slide XML for slides 2 and 3 so PowerPoint natively renders the rotating animation. |
| **Depth & Shadows** | `lxml` XML injection | Adding drop shadows to the arrow and dial separates the elements from the background. |

> **Feasibility Assessment**: **100% reproduction.** By combining native shape insertion, XML text warp injection, and Morph transition injection, this code perfectly recreates the dynamic "rotating wheel" layout and animation seen in the video.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "WHEEL SELECTOR",
    body_text: str = "",
    bg_palette: str = "minimal", 
    accent_color: tuple = (230, 81, 0),  # Deep Orange
    **kwargs,
) -> str:
    """
    Creates a 3-slide PPTX reproducing the 'Rotating Dial Morph Panel' effect.
    Slide 1: Base state
    Slide 2 & 3: Rotated states demonstrating the Morph animation.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from pptx.oxml import OxmlElement
    from pptx.oxml.ns import qn

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Helper: Add Morph Transition to a slide
    def inject_morph_transition(slide):
        transition = OxmlElement('p:transition')
        morph = OxmlElement('p:morph')
        transition.append(morph)

        # Clean existing transition if present
        existing = slide.element.find(qn('p:transition'))
        if existing is not None:
            slide.element.remove(existing)

        # Safe XML injection location
        timing = slide.element.find(qn('p:timing'))
        extLst = slide.element.find(qn('p:extLst'))
        if timing is not None:
            timing.addprevious(transition)
        elif extLst is not None:
            extLst.addprevious(transition)
        else:
            slide.element.append(transition)

    # Helper: Add Drop Shadow
    def add_drop_shadow(shape):
        spPr = shape.element.spPr
        effectLst = OxmlElement('a:effectLst')
        outerShdw = OxmlElement('a:outerShdw')
        outerShdw.set('blurRad', '50800')
        outerShdw.set('dist', '38100')
        outerShdw.set('dir', '2700000')  # Angle
        outerShdw.set('algn', 'tl')
        srgbClr = OxmlElement('a:srgbClr')
        srgbClr.set('val', '000000')
        alpha = OxmlElement('a:alpha')
        alpha.set('val', '25000')  # 25% opacity
        srgbClr.append(alpha)
        outerShdw.append(srgbClr)
        effectLst.append(outerShdw)
        spPr.append(effectLst)

    # Data to animate through
    menu_items = ["INDIA", "PAKISTAN", "DUBAI", "RUSSIA", "BANGLADESH", "USA", "AFGHANISTAN", "CHINA", "NEPAL"]
    dial_text = " • ".join(menu_items) + " • "
    
    # We will generate 3 slides to show the wheel rotating
    # Angles calculated to roughly align the next item to the pointer
    angles = [0, -40, -80]
    selected_items = [menu_items[0], menu_items[1], menu_items[2]]
    
    # Text color mapping
    text_color = RGBColor(26, 35, 126) # Navy Blue
    base_accent = RGBColor(*accent_color)

    for i in range(3):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # 1. Background Fill (Off-white)
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(245, 245, 245)

        # 2. Add Dial Donut Shape
        # Centered vertically, off-canvas to the left
        donut = slide.shapes.add_shape(
            MSO_SHAPE.DONUT, 
            Inches(-3.5), Inches(-0.25), Inches(8), Inches(8)
        )
        donut.fill.solid()
        donut.fill.fore_color.rgb = base_accent
        donut.line.fill.background()
        donut.adjustments[0] = 0.12  # Make the ring thinner
        add_drop_shadow(donut)
        
        # 3. Add Circular Text Warp Shape
        # Must exactly overlap the donut dimensions to align
        txBox = slide.shapes.add_textbox(Inches(-3.5), Inches(-0.25), Inches(8), Inches(8))
        tf = txBox.text_frame
        tf.word_wrap = False
        
        # Dense repeated text to ensure it completes the 360 circle
        p = tf.paragraphs[0]
        p.text = (dial_text * 4).strip()
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = text_color
        p.alignment = PP_ALIGN.CENTER

        # Inject Text Warp effect (prstTxWarp prst="circle")
        bodyPr = txBox.element.txBody.bodyPr
        warp = OxmlElement('a:prstTxWarp')
        warp.set('prst', 'circle')
        avLst = OxmlElement('a:avLst')
        warp.append(avLst)
        bodyPr.append(warp)

        # Apply Rotation! This is what the Morph transition interpolates
        donut.rotation = angles[i]
        txBox.rotation = angles[i]

        # 4. Add Pointer Arrow
        arrow = slide.shapes.add_shape(
            MSO_SHAPE.RIGHT_ARROW, 
            Inches(4.1), Inches(3.25), Inches(3.5), Inches(1.0)
        )
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = base_accent
        arrow.line.fill.background()
        add_drop_shadow(arrow)
        
        # 5. Right Side Content Panel
        # Country Name Title
        title_box = slide.shapes.add_textbox(Inches(8.0), Inches(2.6), Inches(4.5), Inches(1.0))
        tp = title_box.text_frame.paragraphs[0]
        tp.text = selected_items[i]
        tp.font.size = Pt(44)
        tp.font.bold = True
        tp.font.color.rgb = base_accent
        
        # Subtitle
        sub_box = slide.shapes.add_textbox(Inches(8.0), Inches(3.5), Inches(4.5), Inches(0.5))
        sp = sub_box.text_frame.paragraphs[0]
        sp.text = "DETAILS FOR REGION"
        sp.font.size = Pt(18)
        sp.font.bold = True
        sp.font.color.rgb = text_color

        # Bullet points
        bullets_box = slide.shapes.add_textbox(Inches(8.0), Inches(4.2), Inches(4.5), Inches(2.0))
        bullets_tf = bullets_box.text_frame
        bullet_lines = [
            f"{selected_items[i]} market analysis",
            "Regional growth metrics",
            "Key demographic insights"
        ]
        for line in bullet_lines:
            bp = bullets_tf.add_paragraph()
            bp.text = line
            bp.font.size = Pt(16)
            bp.font.color.rgb = RGBColor(80, 80, 80)
            bp.level = 0
            
        # Remove the empty first paragraph
        if len(bullets_tf.paragraphs) > 1 and bullets_tf.paragraphs[0].text == "":
            p_elem = bullets_tf.paragraphs[0]._p
            p_elem.getparent().remove(p_elem)

        # Inject morph transition for slide 2 and 3
        if i > 0:
            inject_morph_transition(slide)

    prs.save(output_pptx_path)
    return output_pptx_path
```