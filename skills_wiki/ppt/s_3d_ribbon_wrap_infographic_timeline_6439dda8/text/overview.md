# 3D Ribbon Wrap Infographic Timeline

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: 3D Ribbon Wrap Infographic Timeline

* **Core Visual Mechanism**: The defining aesthetic is the **simulated 3D depth achieved through 2.5D overlapping**. Flat, brightly colored ribbons appear to wrap around a central neutral-colored structural "pillar." This illusion is created using precise layer sequencing (Z-ordering): a darker ribbon piece is placed behind the pillar, the pillar is drawn over it, and the bright main ribbon is placed over the front of the pillar. Strategic drop shadows separate these flat layers, selling the illusion of volume.
* **Why Use This Skill (Rationale)**: Traditional timelines often feel flat and monotonous. Introducing a central "anchor" (the pillar) and wrapping the chronological events around it breaks up the linear visual flow, creating a dynamic, spatial hierarchy. The bright ribbon colors instantly guide the eye, while the staggered lengths add organic rhythm to the layout.
* **Overall Applicability**: Perfect for corporate milestones, product roadmaps, historical company timelines, and step-by-step process flows.
* **Value Addition**: Transforms a standard bulleted list of dates into a premium, engaging infographic. It elevates the perceived production value of the deck without requiring actual 3D rendering tools.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: Soft radial gradient (white center fading to light grey) to give a studio-lighting feel that accentuates the 3D pillar.
  - **The Pillar**: A tall, light grey vertical rectangle serving as the anchor.
  - **Ribbons**: Vivid, saturated colors against the neutral background. Left edge is completely rounded (semi-circle), right edge is flat where it "folds" around the pillar.
  - **Color Logic**:
    - Pillar: Light Grey `(240, 240, 240)`
    - Ribbon 1: Pink/Magenta `(217, 22, 111)`
    - Ribbon 2: Orange `(242, 142, 43)`
    - Ribbon 3: Teal `(0, 168, 143)`
    - Ribbon 4: Purple `(137, 76, 174)`
  - **Text Hierarchy**: Large, bold year indicators (accent colored), followed by dark grey subtitles.

* **Step B: Compositional Style**
  - The pillar is heavily right-weighted (occupying the ~80% horizontal mark).
  - Ribbons extend right-to-left, utilizing the abundant negative space on the left side of the slide for text.
  - Ribbons are staggered in width (alternating shorter and longer) to avoid visual blockiness.

* **Step C: Dynamic Effects & Transitions**
  - *Native PPT Option*: A simple "Wipe" animation from Right to Left for each ribbon group sequentially reveals the timeline timeline, following the logical flow of the ribbon unwrapping.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Soft Radial Background** | `PIL/Pillow` | Native python-pptx radial gradients require verbose XML injection and are hard to center perfectly; PIL renders a flawless, studio-quality gradient image instantly. |
| **3D Drop Shadows** | `lxml` XML Injection | Deep, blurred drop shadows are critical to separate the overlapping shapes and sell the "wrap" illusion. Python-pptx lacks a native API for shadow effects. |
| **Ribbon Geometry** | `python-pptx` native | Using overlapping standard shapes (a rectangle + a circle on the end) is a highly reliable way to construct the flat-right, rounded-left ribbon geometry seamlessly. |

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml
from PIL import Image, ImageDraw

def _create_radial_gradient_bg(filename: str):
    """Generates a soft, studio-style radial gradient background using PIL."""
    base_size = 1000
    img = Image.new('RGB', (base_size, base_size))
    draw = ImageDraw.Draw(img)
    
    center_color = (255, 255, 255)
    edge_color = (220, 225, 232) # Cool light grey
    
    cx, cy = base_size / 2, base_size / 2
    max_radius = base_size / 1.2
    
    for radius in range(int(max_radius), 0, -2):
        ratio = radius / max_radius
        r = int(center_color[0] * (1 - ratio) + edge_color[0] * ratio)
        g = int(center_color[1] * (1 - ratio) + edge_color[1] * ratio)
        b = int(center_color[2] * (1 - ratio) + edge_color[2] * ratio)
        draw.ellipse(
            (cx - radius, cy - radius, cx + radius, cy + radius),
            fill=(r, g, b)
        )
    
    # Resize to standard 16:9 aspect ratio and save
    img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
    img.save(filename)
    return filename

def _add_shadow(shape, blur_pt=5, dist_pt=4, alpha_pct=30):
    """Injects openxml drop shadow to a shape for 3D separation."""
    blur_emu = int(blur_pt * 12700)
    dist_emu = int(dist_pt * 12700)
    alpha_val = int(alpha_pct * 1000)
    
    shadow_xml = f"""
    <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:outerShdw blurRad="{blur_emu}" dist="{dist_emu}" dir="2700000" algn="tl">
            <a:srgbClr val="000000">
                <a:alpha val="{alpha_val}"/>
            </a:srgbClr>
        </a:outerShdw>
    </a:effectLst>
    """
    effectLst = parse_xml(shadow_xml)
    shape.element.spPr.append(effectLst)

def _darken_color(rgb_tuple, factor=0.7):
    """Returns a darker version of a given RGB tuple for shadow/wrap effects."""
    return RGBColor(
        int(rgb_tuple[0] * factor),
        int(rgb_tuple[1] * factor),
        int(rgb_tuple[2] * factor)
    )

def create_slide(
    output_pptx_path: str,
    title_text: str = "INFOGRAPHIC TIMELINE",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    **kwargs
) -> str:
    """
    Creates a presentation with the 3D Ribbon Wrap Timeline.
    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide
    
    # --- Layer 0: Background ---
    bg_img_path = "temp_bg_gradient.png"
    _create_radial_gradient_bg(bg_img_path)
    slide.shapes.add_picture(bg_img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)
        
    # Title Setup
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(8), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(28)
    p.font.color.rgb = RGBColor(80, 80, 80)

    # Theme Configuration
    ribbon_colors = [
        (217, 22, 111),  # Magenta
        (242, 142, 43),  # Orange
        (0, 168, 143),   # Teal
        (137, 76, 174)   # Purple
    ]
    years = ["2015", "2018", "2020", "2024"]
    y_levels = [1.8, 3.2, 4.6, 6.0]
    start_xs = [5.5, 4.2, 5.5, 4.2] # Staggered effect
    
    pillar_x = 10.0
    pillar_w = 0.8
    ribbon_h = 0.6
    
    # --- Layer 1: Wrap Behind Shapes (Z-Order 1) ---
    # These are drawn first so they sit behind the pillar
    for i in range(4):
        wrap_x = pillar_x + pillar_w - 0.2
        wrap_w = 0.8
        wrap_y = y_levels[i] + 0.3 # Offset downward to simulate angle
        
        wrap_shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 
            Inches(wrap_x), Inches(wrap_y), 
            Inches(wrap_w), Inches(ribbon_h * 0.8)
        )
        wrap_shape.fill.solid()
        wrap_shape.fill.fore_color.rgb = _darken_color(ribbon_colors[i], 0.6)
        wrap_shape.line.fill.background()
        
    # --- Layer 2: The Anchor Pillar (Z-Order 2) ---
    # Drawn over the back wraps
    pillar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(pillar_x), Inches(1.0),
        Inches(pillar_w), Inches(6.0)
    )
    pillar.fill.solid()
    pillar.fill.fore_color.rgb = RGBColor(245, 245, 245)
    pillar.line.fill.background()
    _add_shadow(pillar, blur_pt=10, dist_pt=2, alpha_pct=15) # Soft drop shadow
    
    # --- Layer 3: Main Front Ribbons & Text (Z-Order 3) ---
    for i in range(4):
        c_rgb = RGBColor(*ribbon_colors[i])
        y = y_levels[i]
        start_x = start_xs[i]
        
        # 1. Main Ribbon Body (Overlaps the Pillar exactly to the right edge)
        body_w = (pillar_x + pillar_w) - start_x
        main_ribbon = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(start_x), Inches(y),
            Inches(body_w), Inches(ribbon_h)
        )
        main_ribbon.fill.solid()
        main_ribbon.fill.fore_color.rgb = c_rgb
        main_ribbon.line.fill.solid()
        main_ribbon.line.fill.fore_color.rgb = c_rgb
        _add_shadow(main_ribbon, blur_pt=6, dist_pt=3, alpha_pct=35) # Crucial for depth

        # 2. Rounded Left Cap (Seamlessly merges with main ribbon body)
        cap_size = ribbon_h
        cap = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(start_x - (cap_size/2)), Inches(y),
            Inches(cap_size), Inches(cap_size)
        )
        cap.fill.solid()
        cap.fill.fore_color.rgb = c_rgb
        cap.line.fill.solid()
        cap.line.fill.fore_color.rgb = c_rgb
        
        # 3. Node Outer Diamond
        node_size = 0.9
        node = slide.shapes.add_shape(
            MSO_SHAPE.DIAMOND,
            Inches(start_x - (node_size/2)), Inches(y - 0.15),
            Inches(node_size), Inches(node_size)
        )
        node.fill.solid()
        node.fill.fore_color.rgb = RGBColor(255, 255, 255)
        node.line.color.rgb = c_rgb
        node.line.width = Pt(4)
        _add_shadow(node, blur_pt=4, dist_pt=2, alpha_pct=20)
        
        # 4. Node Inner Diamond (Accent)
        inner_size = 0.35
        inner_node = slide.shapes.add_shape(
            MSO_SHAPE.DIAMOND,
            Inches(start_x - (inner_size/2)), Inches(y + 0.125),
            Inches(inner_size), Inches(inner_size)
        )
        inner_node.fill.solid()
        inner_node.fill.fore_color.rgb = c_rgb
        inner_node.line.fill.background()
        
        # 5. Connective Tracker Line (to Text)
        line = slide.shapes.add_shape(
            MSO_SHAPE.LINE,
            Inches(start_x - 1.5), Inches(y + ribbon_h/2),
            Inches(start_x - 0.5), Inches(y + ribbon_h/2)
        )
        line.line.color.rgb = c_rgb
        line.line.width = Pt(1.5)

        # 6. Year Box
        year_box = slide.shapes.add_textbox(
            Inches(start_x - 3.2), Inches(y - 0.3), 
            Inches(1.6), Inches(0.6)
        )
        p_yr = year_box.text_frame.paragraphs[0]
        p_yr.text = years[i]
        p_yr.font.bold = True
        p_yr.font.size = Pt(28)
        p_yr.font.color.rgb = c_rgb
        p_yr.alignment = PP_ALIGN.RIGHT
        
        # 7. Subtitle / Body Box
        text_box = slide.shapes.add_textbox(
            Inches(start_x - 3.2), Inches(y + 0.35), 
            Inches(1.6), Inches(0.8)
        )
        p_sub = text_box.text_frame.paragraphs[0]
        p_sub.text = body_text
        p_sub.font.size = Pt(10)
        p_sub.font.color.rgb = RGBColor(100, 100, 100)
        p_sub.alignment = PP_ALIGN.RIGHT
        
    prs.save(output_pptx_path)
    return output_pptx_path
```