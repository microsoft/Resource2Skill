# Custom Motion Path Animation & Visualization

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Custom Motion Path Animation & Visualization

* **Core Visual Mechanism**: Defining a tailored, non-linear trajectory (e.g., a bouncing or zigzag path) for an object, allowing it to navigate the slide with distinct motion behaviors. This moves beyond simple linear entrances, creating a sense of physical physics (like gravity or momentum).
* **Why Use This Skill (Rationale)**: Human eyes naturally track motion. A custom, multi-point path keeps the audience engaged, tells a spatial story (e.g., journey, obstacles, progress), and visually anchors physical analogies (like a bouncing ball representing market fluctuations).
* **Overall Applicability**: Perfect for process journey slides, timeline animations, physical product demonstrations, storytelling sequences, and dynamic title cards where energetic motion sets the tone.
* **Value Addition**: Transforms a static graphic into a dynamic storytelling element. By combining the animation with a dashed "ghost" line, the audience intuitively understands both the *intended* journey and the *actual* movement.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: Deep, atmospheric radial gradient simulating a spotlight or a sports field (e.g., from `(34, 139, 34)` to `(10, 30, 10)`).
  - **The Object**: A stylized item (in this case, a procedurally drawn soccer ball) acting as the focal point of the animation. 
  - **The Path Indicator**: A semi-transparent, dashed freeform line (e.g., `RGB(200, 255, 200)` with `3pt` width) that provides a visual track for the object.

* **Step B: Compositional Style**
  - **Spatial Feel**: Left-to-right progression. The object starts at `x=15%` of the slide width and travels across the canvas to `x=75%`, utilizing the horizontal space to denote forward progress.
  - **Proportions**: The object occupies about `10-15%` of the vertical height, ensuring it doesn't overwhelm the space while moving.

* **Step C: Dynamic Effects & Transitions**
  - **Animation Type**: A Custom Motion Path (`<p:animMotion>`) applied via XML injection.
  - **Physics**: The trajectory utilizes a sequence of relative coordinate shifts (Up, Down, Up) to simulate a physical bounce over a fixed `3000ms` duration.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Background & Object** | `PIL/Pillow` | Native python-pptx cannot generate radial gradients. PIL is used to procedurally draw both the gradient background and the soccer ball element ensuring the code works offline without relying on external image links. |
| **Path Visualization** | `python-pptx` (FreeformBuilder) | Used to draw the precise physical dashed line on the slide so the audience can see the trajectory path before and during the animation. |
| **Motion Path Animation** | `lxml` XML injection | `python-pptx` has zero native support for animations. We must inject a `<p:timing>` tree and an `<p:animMotion>` behavior targeting the shape's specific ID to create the custom moving effect. |

*Feasibility Assessment*: 95%. The core visual aesthetic and the exact bouncing motion path are perfectly reproduced. The only minor deviation is using linear segments (zig-zags) instead of perfectly smooth Bezier curves, as `FreeformBuilder` in python-pptx currently only maps line segments easily, but the visual result is nearly identical to the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Custom Bouncing Motion Path",
    duration_ms: int = 3000,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Custom Motion Path Animation effect.
    
    Returns: path to the saved PPTX file.
    """
    import os
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from lxml import etree
    from PIL import Image, ImageDraw

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    # Using blank layout to manage z-order perfectly from bottom-up
    slide = prs.slides.add_slide(prs.slide_layouts[6])  
    
    # === Layer 1: Background ===
    bg_path = "temp_gradient_bg.png"
    img_bg = Image.new('RGBA', (1920, 1080))
    draw_bg = ImageDraw.Draw(img_bg)
    # Draw radial gradient (spotlight effect)
    for r in range(1200, 0, -20):
        ratio = r / 1200
        # Dark forest green to near black
        c = (
            int(34 * (1-ratio) + 10 * ratio),
            int(139 * (1-ratio) + 30 * ratio),
            int(34 * (1-ratio) + 10 * ratio),
            255
        )
        draw_bg.ellipse((960-r, 540-r, 960+r, 540+r), fill=c)
    img_bg.save(bg_path)
    slide.shapes.add_picture(bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
    
    # === Layer 2: Text Box ===
    tx_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12), Inches(1))
    tf = tx_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    # === Layer 3: Visual Path Construction ===
    w_inches = 13.333
    h_inches = 7.5
    start_x_inches = w_inches * 0.15
    start_y_inches = h_inches * 0.6
    
    # Relative path points for motion (x_rel, y_rel) - represents a double bounce
    # Note: in PPTX, +Y is downwards, -Y is upwards
    rel_pts = [
        (0.15, -0.30),  # Bounce Up & Right
        (0.30, 0.00),   # Fall Down & Right
        (0.45, 0.30),   # Fall Further Down & Right
        (0.60, 0.00)    # Bounce Back Up & Right
    ]
    
    # Draw dashed visualization line
    builder = slide.shapes.build_freeform(Inches(start_x_inches), Inches(start_y_inches))
    abs_pts = [(Inches(start_x_inches + x*w_inches), Inches(start_y_inches + y*h_inches)) for x, y in rel_pts]
    builder.add_line_segments(abs_pts, close=False)
    path_shape = builder.convert_to_shape()
    path_shape.line.color.rgb = RGBColor(200, 255, 200)
    path_shape.line.dash_style = 7  # MSO_LINE_DASH_STYLE.DASH
    path_shape.line.width = Pt(3)
    
    # === Layer 4: Procedural Object (Soccer Ball) ===
    ball_path = "temp_soccer_ball.png"
    b_size = 200
    b_img = Image.new('RGBA', (b_size, b_size), (0,0,0,0))
    b_draw = ImageDraw.Draw(b_img)
    # Drop shadow
    b_draw.ellipse((15, 20, 185, 190), fill=(0,0,0,100))
    # Main white sphere
    b_draw.ellipse((10, 10, 190, 190), fill=(255,255,255,255), outline=(0,0,0,255), width=5)
    # Hexagon pattern lines
    b_draw.polygon([(100, 45), (135, 75), (120, 120), (80, 120), (65, 75)], fill=(0,0,0,255))
    b_draw.line([(100,45), (100,10)], fill=(0,0,0,255), width=5)
    b_draw.line([(135,75), (185,65)], fill=(0,0,0,255), width=5)
    b_draw.line([(120,120), (155,175)], fill=(0,0,0,255), width=5)
    b_draw.line([(80,120), (45,175)], fill=(0,0,0,255), width=5)
    b_draw.line([(65,75), (15,65)], fill=(0,0,0,255), width=5)
    b_img.save(ball_path)
    
    # Insert object centered on the start coordinates
    ball_size = Inches(1.5)
    left = Inches(start_x_inches) - ball_size/2
    top = Inches(start_y_inches) - ball_size/2
    ball_pic = slide.shapes.add_picture(ball_path, left, top, width=ball_size, height=ball_size)
    
    # === Layer 5: Animation XML Injection ===
    # Convert points to PPTX SVG-like path string
    path_str = "M 0 0 "
    for x, y in rel_pts:
        path_str += f"L {x:.3f} {y:.3f} "
        
    nsmap = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
    
    # Root timing tree wrapper (safely injecting into a new slide)
    timing_xml = """
    <p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
        <p:tnLst>
            <p:par>
                <p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
                    <p:childTnLst>
                        <p:seq concurrent="1" nextAc="seek">
                            <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
                                <p:childTnLst>
                                    <p:par>
                                        <p:cTn id="3" fill="hold">
                                            <p:stCondLst>
                                                <p:cond delay="0"/>
                                            </p:stCondLst>
                                            <p:childTnLst/>
                                        </p:cTn>
                                    </p:par>
                                </p:childTnLst>
                            </p:cTn>
                        </p:seq>
                    </p:childTnLst>
                </p:cTn>
            </p:par>
        </p:tnLst>
    </p:timing>
    """
    slide.element.append(etree.fromstring(timing_xml))
    
    # Target the deepest child node
    target_lst = slide.element.xpath('.//p:seq/p:cTn/p:childTnLst/p:par/p:cTn/p:childTnLst', namespaces=nsmap)[0]
    
    # Inject actual motion path behavior targeting the ball picture ID
    anim_xml = f'''
    <p:par xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
        <p:cTn id="4" presetID="14" presetClass="path" presetSubtype="0" fill="hold" nodeType="withEffect">
            <p:stCondLst>
                <p:cond delay="0"/>
            </p:stCondLst>
            <p:childTnLst>
                <p:animMotion path="{path_str}" pathEditMode="relative" rAng="0">
                    <p:cBhvr>
                        <p:cTn id="5" dur="{duration_ms}" fill="hold"/>
                        <p:tgtEl>
                            <p:spTgt spid="{ball_pic.shape_id}"/>
                        </p:tgtEl>
                        <p:attrNameLst>
                            <p:attrName>ppt_x</p:attrName>
                            <p:attrName>ppt_y</p:attrName>
                        </p:attrNameLst>
                    </p:cBhvr>
                </p:animMotion>
            </p:childTnLst>
        </p:cTn>
    </p:par>
    '''
    target_lst.append(etree.fromstring(anim_xml))
    
    prs.save(output_pptx_path)
    
    # Cleanup temporary local assets
    if os.path.exists(bg_path): os.remove(bg_path)
    if os.path.exists(ball_path): os.remove(ball_path)
        
    return output_pptx_path
```