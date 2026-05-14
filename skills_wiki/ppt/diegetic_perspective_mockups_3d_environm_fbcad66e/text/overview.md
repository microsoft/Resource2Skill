# Diegetic Perspective Mockups (3D & Environment Integration)

## Analysis

# Skill Extraction Strategy Document

### 1. High-level Design Pattern Extraction

> **Skill Name**: Diegetic Perspective Mockups (3D & Environment Integration)

* **Core Visual Mechanism**: Embedding raw 2D digital content (screenshots, photos, text) into realistic photographic environments or native 3D spaces using perspective warping, spatial depth, and lighting. Rather than pasting flat images onto a slide, this pattern transforms them into "physical" objects (like floating isometric tablets, angled laptop screens, or integrated paper notes).
* **Why Use This Skill (Rationale)**: Flat screenshots create a visual disconnect and signal low effort. By warping elements into 3D perspective or pasting them into environmental contexts (like a billboard or notebook), you ground the content in reality. It immediately increases the perceived production value and gives the audience a visceral sense of scale and application.
* **Overall Applicability**: Essential for product showcases, UI/UX portfolio decks, software launch presentations, and any scenario where digital features need to feel tangible, premium, and "real."
* **Value Addition**: Transforms a standard 2D grid layout into a dynamic spatial composition. It captures attention through realism and depth, breaking the monotonous "title + bullet points + flat image" convention.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Diegetic Containers**: Devices (phones/laptops), print media (notebooks), or physical structures (billboards) acting as frames.
  - **3D Extrusions & Bezels**: Simulated physical thickness (e.g., an aluminum edge catching the light) to sell the illusion of depth.
  - **Environment Shadows**: Soft, detached drop shadows that ground floating elements in the 3D space.
  - **Color Logic**: Often relies on high-contrast foreground-background relationships. For example, a dark environment (`#0F141E`) paired with a bright, luminous mock-up screen to simulate a glowing display.

* **Step B: Compositional Style**
  - **Asymmetrical Spatial Layout**: The angled, isometric nature of the mockups allows them to occupy one half of the slide dynamically, leading the eye naturally to the text on the opposite side.
  - **Layering**: Overlapping physical elements (e.g., a notebook stacked over a floating tablet) to reinforce the Z-axis depth.

* **Step C: Dynamic Effects & Transitions**
  - **Morphing Across Perspectives**: The "Morph" transition combined with 3D rotation allows the mockup to seamlessly swivel from a flat view to an angled isometric view across slides.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Procedural UI Generation** | `PIL/Pillow` | Generates a crisp, abstract UI graphic on the fly so the code runs standalone without requiring external image downloads. |
| **3D Isometric Warp & Bezel** | `lxml` (XML Injection) | `python-pptx` cannot natively apply 3D camera rotations or extrusions. Injecting `<a:scene3d>` and `<a:sp3d>` utilizes PowerPoint's native hardware-accelerated 3D engine, keeping the asset crisp and perfectly mapped without destructive pixel-warping. |
| **Drop Shadows** | `lxml` (XML Injection) | Injects `<a:effectLst>` to add realistic, decoupled shadows that don't rotate with the shape, grounding the floating mockup. |

> **Feasibility Assessment**: 100%. By manipulating PowerPoint's underlying DrawingML via `lxml`, we can perfectly recreate the angled/3D mockups demonstrated in the tutorial using native, scalable vector properties.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Beyond Flat Screens",
    body_text: str = "Elevate your designs with diegetic, 3D perspective mockups that bring digital concepts into the physical world.",
    **kwargs,
) -> str:
    """
    Creates a PPTX demonstrating the 'Diegetic Perspective Mockups' skill.
    Generates a placeholder UI image, maps it onto an isometric 3D floating tablet,
    and composites it with a layered physical "notebook" element.
    """
    import os
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.dml.color import RGBColor
    from pptx.oxml import parse_xml
    from PIL import Image, ImageDraw

    # ==========================================
    # 1. Procedurally Generate the "UI Screen"
    # ==========================================
    ui_path = "temp_mockup_ui.png"
    ui_img = Image.new('RGB', (800, 1200), color=(240, 244, 248))
    draw = ImageDraw.Draw(ui_img)
    
    # Header bar
    draw.rectangle([0, 0, 800, 120], fill=(255, 255, 255))
    draw.ellipse([40, 40, 80, 80], fill=(200, 205, 210)) # Avatar
    draw.rectangle([110, 50, 400, 70], fill=(200, 205, 210)) # Skeleton text
    
    # Hero chart area
    draw.rounded_rectangle([40, 160, 760, 560], radius=30, fill=(255, 255, 255))
    draw.line([(80, 480), (200, 350), (350, 400), (500, 250), (700, 200)], fill=(0, 120, 212), width=15, joint="curve")
    
    # Bottom cards
    draw.rounded_rectangle([40, 600, 380, 900], radius=30, fill=(255, 255, 255))
    draw.rounded_rectangle([420, 600, 760, 900], radius=30, fill=(255, 255, 255))
    
    # Action button
    draw.rounded_rectangle([40, 950, 760, 1050], radius=20, fill=(0, 120, 212))
    ui_img.save(ui_path)

    # ==========================================
    # 2. Setup Presentation & Background
    # ==========================================
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide

    # Rich dark background
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(18, 22, 31)

    # ==========================================
    # 3. Create Isometric Floating 3D Device
    # ==========================================
    # Add base rounded rectangle
    device = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, 
        Inches(1.5), Inches(1.5), Inches(4.0), Inches(5.5)
    )
    
    # Set the procedural UI as the picture fill
    device.fill.user_picture(ui_path)
    device.line.color.rgb = RGBColor(180, 180, 185)
    device.line.width = Pt(1.5)

    spPr = device._element.spPr
    
    # XML: Drop Shadow
    shadow_xml = """
    <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:outerShdw blurRad="400000" dist="500000" dir="2700000" algn="bl" rotWithShape="0">
            <a:srgbClr val="000000">
                <a:alpha val="60000"/>
            </a:srgbClr>
        </a:outerShdw>
    </a:effectLst>
    """
    
    # XML: 3D Camera (Isometric Right Up)
    scene3d_xml = """
    <a:scene3d xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:camera prst="isometricRightUp"/>
        <a:lightRig rig="threePt" dir="t"/>
    </a:scene3d>
    """
    
    # XML: 3D Extrusion (Simulating device thickness)
    sp3d_xml = """
    <a:sp3d extrusionH="120000" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:bevelT w="12700" h="12700" prst="circle"/>
        <a:extrusionClr>
            <a:srgbClr val="B0B0B5"/>
        </a:extrusionClr>
    </a:sp3d>
    """
    
    # Inject 3D effects into shape (Order matters for OpenXML validation)
    spPr.append(parse_xml(shadow_xml))
    spPr.append(parse_xml(scene3d_xml))
    spPr.append(parse_xml(sp3d_xml))

    # ==========================================
    # 4. Layered Physical Element (Notebook Effect)
    # ==========================================
    note = slide.shapes.add_shape(
        MSO_SHAPE.FOLDED_CORNER, 
        Inches(4.8), Inches(4.5), Inches(2.2), Inches(2.2)
    )
    note.fill.solid()
    note.fill.fore_color.rgb = RGBColor(255, 240, 150)
    note.line.fill.background()
    note.rotation = 6 # Slight casual rotation
    
    tf = note.text_frame
    tf.text = "Diegetic\nIntegration!"
    p = tf.paragraphs[0]
    p.font.name = "Comic Sans MS" # Safe fallback for handwritten style
    p.font.size = Pt(22)
    p.font.color.rgb = RGBColor(70, 70, 70) # Simulating ink opacity
    tf.paragraphs[1].font.name = "Comic Sans MS"
    tf.paragraphs[1].font.size = Pt(22)
    tf.paragraphs[1].font.color.rgb = RGBColor(70, 70, 70)

    # Note Shadow
    note_spPr = note._element.spPr
    note_shadow = """
    <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:outerShdw blurRad="150000" dist="150000" dir="2700000" algn="bl">
            <a:srgbClr val="000000">
                <a:alpha val="40000"/>
            </a:srgbClr>
        </a:outerShdw>
    </a:effectLst>
    """
    note_spPr.append(parse_xml(note_shadow))

    # ==========================================
    # 5. Typography Layout
    # ==========================================
    txt_box = slide.shapes.add_textbox(Inches(7.5), Inches(2.5), Inches(5.0), Inches(3.0))
    tf = txt_box.text_frame
    tf.word_wrap = True
    
    p_title = tf.paragraphs[0]
    p_title.text = title_text.upper()
    p_title.font.name = "Arial"
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255)
    
    p_body = tf.add_paragraph()
    p_body.text = f"\n{body_text}"
    p_body.font.name = "Arial"
    p_body.font.size = Pt(18)
    p_body.font.color.rgb = RGBColor(180, 190, 205)

    # Cleanup temporary image
    if os.path.exists(ui_path):
        os.remove(ui_path)

    prs.save(output_pptx_path)
    return output_pptx_path
```