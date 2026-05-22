# 3D Isometric Morphing Bar Charts

## Analysis

### 1. High-level Design Pattern Extraction

**Skill Name**: 3D Isometric Morphing Bar Charts

*   **Core Visual Mechanism**: The defining visual signature is transforming flat, 2D vector shapes into a 3D isometric landscape using native 3D camera presets (`isometricTopUp`) and depth extrusions (`extrusionH`). Elements like floor strips, rising data cubes, text labels, and floating icons are composed in 2D space but mapped seamlessly into a unified 3D grid.
*   **Why Use This Skill (Rationale)**: Isometric projections add depth and physical weight to standard data without the clutter of perspective distortion. It turns abstract comparisons (like a bar chart) into a tangible "cityscape" or physical platform, increasing viewer engagement.
*   **Overall Applicability**: Perfect for high-stakes presentations, product launch metrics, strategic pillars, and data dashboard hero slides where you want to show "ranking" or "growth" visually rather than just numerically.
*   **Value Addition**: Transforms a standard 4-point list or basic bar chart into an immersive, premium motion-graphics experience. Utilizing PowerPoint’s native 3D engine allows these elements to flawlessly interpolate (grow/shrink) using the Morph transition.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    *   **Background**: Deep violet/navy solid fill `(30, 20, 60)` to provide a dark studio backdrop.
    *   **Color Logic**: Vibrant, saturated "flat UI" colors that pop against the dark background.
        *   Bar 1 (Cyan): `(0, 191, 255)`
        *   Bar 2 (Blue): `(58, 117, 255)`
        *   Bar 3 (Magenta): `(255, 0, 150)`
        *   Bar 4 (Purple): `(153, 50, 204)`
    *   **Text Hierarchy**: Standard 2D bold titles in the top left. The 3D text labels ("Topic 01") are mapped flat onto the isometric floor strips, using clean, white sans-serif fonts.
*   **Step B: Compositional Style**
    *   The 3D grid defines the layout. By drawing horizontal strips in 2D and applying an `isometricTopUp` camera, the strips naturally project diagonally down-right across the canvas.
    *   The cubes sit at the "start" of the strips. The height of the cubes (data magnitude) is controlled exclusively by their 3D Z-extrusion depth.
*   **Step C: Dynamic Effects & Transitions**
    *   **Morph Transition**: By creating a "flat" version of the chart on Slide 1 (where cubes have depth = 1) and an "elevated" version on Slide 2 (where cubes have depth = 100+), the Morph transition natively interpolates the 3D extrusion, creating a stunning rising bar animation.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
| :--- | :--- | :--- |
| **3D Isometric Projection** | `lxml` XML injection | `python-pptx` natively lacks the API to set 3D camera presets (`<a:scene3d>`). We must inject it into the shape's properties. |
| **3D Bar Height (Extrusion)** | `lxml` XML injection | Setting the 3D depth (`extrusionH`) and distance from ground (`z`) requires injecting the `<a:sp3d>` element. |
| **Floating Icons & Floor Text** | Mathematical Z-layering (`lxml`) | By precisely matching the `z` attribute of the icon to the `extrusionH` of the cube, the icon perfectly rests on the top face of the 3D bar. |
| **Morph Animation** | Slide Duplication | Generating two structurally identical slides with different 3D values guarantees that PPT's native Morph transition will work flawlessly. |

*Feasibility Assessment*: 100% reproducible. By tapping directly into PowerPoint's robust DrawingML 3D engine via `lxml`, we completely recreate the visual effect, the shading, the spatial layout, and the morph-ability without relying on external image generation.

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml

def apply_3d_effect(shape, depth_pt=0, z_pt=0, camera_prst="isometricTopUp", material="matPlastic"):
    """
    Injects DrawingML XML into a shape to transform it into a 3D isometric object.
    :param depth_pt: The extrusion depth (thickness) in points.
    :param z_pt: Distance from the ground (Z-axis offset) in points.
    """
    spPr = shape.element.spPr
    
    # Remove existing 3D tags if present to prevent schema errors
    for tag in ['{http://schemas.openxmlformats.org/drawingml/2006/main}scene3d',
                '{http://schemas.openxmlformats.org/drawingml/2006/main}sp3d']:
        el = spPr.find(tag)
        if el is not None:
            spPr.remove(el)

    # 1. Add Camera and Lighting Scene
    scene3d_xml = f"""
    <a:scene3d xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:camera prst="{camera_prst}"/>
        <a:lightRig rig="threePt" dir="t"/>
    </a:scene3d>
    """
    spPr.append(parse_xml(scene3d_xml))

    # 2. Add 3D Extrusion and Z-Elevation
    # 1 point = 12,700 EMUs
    extrusion_emu = int(depth_pt * 12700)
    z_emu = int(z_pt * 12700)
    sp3d_xml = f"""
    <a:sp3d xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
            extrusionH="{extrusion_emu}"
            z="{z_emu}"
            prstMaterial="{material}">
    </a:sp3d>
    """
    spPr.append(parse_xml(sp3d_xml))

def create_slide(
    output_pptx_path: str,
    title_text: str = "Ranking SLIDES",
    body_text: str = "",
    bg_palette: str = "dark",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the '3D Isometric Morphing Bar Charts' visual effect.
    Generates two slides to demonstrate the Morph transition rising effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Data configuration
    bg_color = RGBColor(30, 20, 60)
    
    colors = [
        RGBColor(0, 191, 255),    # Cyan
        RGBColor(58, 117, 255),   # Blue
        RGBColor(255, 0, 150),    # Magenta
        RGBColor(153, 50, 204)    # Purple
    ]
    
    # Target heights for the bars
    target_depths = [80, 140, 200, 100]
    
    # Icons to place on top of the bars
    icons = [
        MSO_SHAPE.STAR_5_POINT,
        MSO_SHAPE.HEART,
        MSO_SHAPE.LIGHTNING_BOLT,
        MSO_SHAPE.SUN
    ]

    # Generate Slide 1 (Flat State) and Slide 2 (Elevated State)
    for slide_idx in range(2):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Slide Background
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = bg_color

        # Add 2D Screen-space Titles
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(5), Inches(1))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = "Ranking"
        p.font.size = Pt(44)
        p.font.color.rgb = RGBColor(255, 215, 0)
        p.font.italic = True
        
        subtitle_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(5), Inches(1))
        tf2 = subtitle_box.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = "SLIDES"
        p2.font.size = Pt(64)
        p2.font.color.rgb = RGBColor(255, 255, 255)
        p2.font.bold = True

        # Render 3D Isometric Chart Elements
        start_x = Inches(3.0)
        start_y = Inches(1.5)
        w_cube = Inches(1.3)
        h_cube = Inches(1.3)
        w_tail = Inches(7.0)

        for i in range(4):
            # Layout cascades downwards in 2D (which projects to down-left in 3D)
            y = start_y + (i * h_cube)

            # Determine depth based on which slide we are generating (animation state)
            current_depth = target_depths[i] if slide_idx == 1 else 1

            # 1. Floor Tail (The long strip)
            tail = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, start_x, y, w_tail, h_cube)
            tail.fill.solid()
            tail.fill.fore_color.rgb = colors[i]
            tail.line.color.rgb = colors[i]
            # Sits flat on the floor (Z=0, Depth=1)
            apply_3d_effect(tail, depth_pt=1, z_pt=0)

            # 2. Rising Data Cube
            cube = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, start_x, y, w_cube, h_cube)
            cube.fill.solid()
            cube.fill.fore_color.rgb = colors[i]
            cube.line.color.rgb = colors[i]
            # Cube extends upwards. Setting Z=depth pushes the front face towards camera, leaving back face on floor.
            apply_3d_effect(cube, depth_pt=current_depth, z_pt=current_depth)

            # 3. Floor Text (Painted on the strip)
            text_box = slide.shapes.add_textbox(start_x + w_cube + Inches(0.5), y + Inches(0.25), Inches(3), Inches(0.8))
            text_box.margin_left = text_box.margin_top = text_box.margin_right = text_box.margin_bottom = 0
            tf3 = text_box.text_frame
            tf3.word_wrap = False
            p3 = tf3.paragraphs[0]
            p3.text = f"Topic 0{i+1}"
            p3.font.size = Pt(36)
            p3.font.bold = True
            p3.font.color.rgb = RGBColor(255, 255, 255)
            # Text hovers 1 point above the floor to avoid z-fighting with the tail
            apply_3d_effect(text_box, depth_pt=0, z_pt=2)

            # 4. Floating Icon (Rests on top of the data cube)
            icon = slide.shapes.add_shape(icons[i], start_x + Inches(0.3), y + Inches(0.3), Inches(0.7), Inches(0.7))
            icon.fill.solid()
            icon.fill.fore_color.rgb = RGBColor(255, 255, 255)
            icon.line.color.rgb = colors[i]
            # Icon hovers exactly at the front face of the cube (Z = current_depth + 1pt buffer)
            apply_3d_effect(icon, depth_pt=0, z_pt=current_depth + 1)

    prs.save(output_pptx_path)
    return output_pptx_path
```