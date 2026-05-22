# Panoramic Chevron Reveal Slide

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Panoramic Chevron Reveal Slide

* **Core Visual Mechanism**: The design relies on a series of nested, forward-pointing geometric shapes (chevrons/pentagons) that stretch from the left edge of the screen and terminate in dynamic, parallel sharp angles. A large picture fill acts as the central anchor, flanked by vibrant solid-color accent bands on the leading edge and a contrasting solid block on the trailing edge. 
* **Why Use This Skill (Rationale)**: The forward-pointing chevron geometry inherently implies momentum, progress, and future-thinking. Stacking these shapes with distinct visual weights (dark neutral, bright accent, rich photography, stark white) creates a strong sense of depth and visual hierarchy without cluttering the canvas.
* **Overall Applicability**: Perfect for high-impact title slides, executive summaries, strategic roadmaps, or chapter intro dividers. It excels in scenarios where a "visionary" or "forward-moving" tone is required.
* **Value Addition**: Transforms a standard photo-and-text slide into a branded, editorial-quality layout. The layered bands provide structural framing for the image, while the solid white overlay ensures the text remains highly readable regardless of the background photo's complexity.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Geometric Masks**: Full-height freeform polygons that feature a flat left edge and a pointed right edge.
  - **Color Logic (Modern Enterprise Palette)**:
    - Base Background: Deep Navy `(15, 23, 42, 255)`
    - Depth Band: Dark Slate `(30, 41, 59, 255)`
    - Accent Band: Vibrant Yellow `(250, 204, 21, 255)`
    - Overlay Block: Crisp White `(255, 255, 255, 255)`
    - Hero Arrow: Sky Blue `(14, 165, 233, 255)`
  - **Text Hierarchy**: Massive, bold, capitalized title text anchored tightly inside the hero arrow, paired with a smaller, tracked-out subtitle.

* **Step B: Compositional Style**
  - **Mathematical Parallelism**: The slanted lines of every layer (grey, yellow, picture, white, blue) share the exact same slope, creating a unified directional flow.
  - **Layering & Shadows**: Each geometric band overlaps the one beneath it, reinforced by subtle directional drop shadows that cast rightward, giving the illusion of folded physical ribbons.

* **Step C: Dynamic Effects & Transitions**
  - *Tutorial context*: The shapes are animated to "Fly In" from the left sequentially with a slight delay (staggered cascade), culminating in the text appearing.
  - *Code context*: We will generate the fully resolved, layered final state with LXML-injected shadows to emulate the depth.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Precise Chevron Geometries** | `python-pptx` `FreeformBuilder` | Standard chevron shapes distort their point angles when stretched to full height. Building custom polygons ensures mathematically parallel slopes. |
| **Image Masking inside Polygon** | `python-pptx` `user_picture()` | Natively binds an image inside the custom freeform path while maintaining vector editability. |
| **Image Sizing / Cropping** | `PIL/Pillow` | Pre-crops the downloaded image to perfectly match the polygon's bounding box ratio so it doesn't stretch when injected into PPTX. |
| **Layer Depth / Drop Shadows** | `lxml` XML injection | `python-pptx` lacks a native API for drop shadows. Modifying the underlying OOXML (`<a:outerShdw>`) perfectly recreates the layered 3D aesthetic. |

> **Feasibility Assessment**: 95% reproduction of the visual style. The staggered entry animation from the video cannot be robustly coded via standard libraries without complex timing node XML, but the core spatial geometry, masking, and shadow aesthetics are reproduced perfectly.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "2024",
    body_text: str = "GLOBAL VISION & STRATEGY",
    bg_palette: str = "cityscape, modern architecture",
    accent_color: tuple = (14, 165, 233), 
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Panoramic Chevron Reveal visual effect.
    """
    import os
    import urllib.request
    import urllib.parse
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from lxml import etree
    from PIL import Image, ImageDraw

    # Initialize Presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Helper 1: Setup Base Background ===
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor(15, 23, 42)

    # === Helper 2: Convert Inches to EMUs for FreeformBuilder ===
    def to_emu(val):
        return int(Inches(val))

    # === Helper 3: Inject Drop Shadow via LXML ===
    def apply_shadow(shape, alpha="40000", blur="200000", dist="100000"):
        spPr = shape.element.spPr
        effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
        outerShdw = etree.SubElement(effectLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw', 
                                     blurRad=blur, dist=dist, dir="2700000", algn="ctr", rotWithShape="0")
        srgbClr = etree.SubElement(outerShdw, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr', val="000000")
        etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', val=alpha)

    # === Helper 4: Build Full-Height Pointed Geometry ===
    # dx is the horizontal length of the point. y_mid is vertically centered.
    def add_full_pointed_rect(pt_x, color_rgb=None, picture_path=None):
        dx = 3.0
        ffb = slide.shapes.build_freeform(to_emu(-0.5), to_emu(0))
        ffb.add_line_segments([
            (to_emu(pt_x - dx), to_emu(0)),
            (to_emu(pt_x), to_emu(3.75)),
            (to_emu(pt_x - dx), to_emu(7.5)),
            (to_emu(-0.5), to_emu(7.5)),
            (to_emu(-0.5), to_emu(0))
        ], close=True)
        shape = ffb.convert_to_shape()
        shape.line.fill.background() # Remove border
        
        if picture_path:
            shape.fill.user_picture(picture_path)
        elif color_rgb:
            shape.fill.solid()
            shape.fill.fore_color.rgb = RGBColor(*color_rgb)
            
        return shape

    # === Acquire Image (AI Gen / Unsplash fallback / Gradiant fallback) ===
    img_path = "temp_chevron_bg.jpg"
    try:
        prompt = urllib.parse.quote(f"{bg_palette} high quality photography")
        url = f"https://image.pollinations.ai/prompt/{prompt}?width=1200&height=800&nologo=true"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(img_path, 'wb') as f:
                f.write(response.read())
        
        # Crop image perfectly to polygon bounding box ratio (12.5 / 7.5)
        img = Image.open(img_path)
        target_ratio = 12.5 / 7.5
        img_ratio = img.width / img.height
        if img_ratio > target_ratio:
            new_w = int(img.height * target_ratio)
            left = (img.width - new_w) // 2
            img = img.crop((left, 0, left + new_w, img.height))
        else:
            new_h = int(img.width / target_ratio)
            top = (img.height - new_h) // 2
            img = img.crop((0, top, img.width, top + new_h))
        img.save(img_path)
    except Exception:
        # Fallback Gradient
        img = Image.new('RGB', (1250, 750))
        draw = ImageDraw.Draw(img)
        for y in range(750):
            draw.line([(0, y), (1250, y)], fill=(int(20 + 30*y/750), int(30 + 40*y/750), int(60 + 60*y/750)))
        img.save(img_path)

    # === Construct Layers Back-to-Front ===
    
    # Layer 1: Dark Slate Band (Touches right edge)
    dark_band = add_full_pointed_rect(pt_x=13.3, color_rgb=(30, 41, 59))
    apply_shadow(dark_band)

    # Layer 2: Vibrant Yellow Band
    yellow_band = add_full_pointed_rect(pt_x=12.6, color_rgb=(250, 204, 21))
    apply_shadow(yellow_band)

    # Layer 3: Hero Picture Area
    pic_band = add_full_pointed_rect(pt_x=12.0, picture_path=img_path)
    apply_shadow(pic_band)

    # Layer 4: White Contrast Overlay
    white_overlay = add_full_pointed_rect(pt_x=8.0, color_rgb=(255, 255, 255))
    apply_shadow(white_overlay, alpha="25000", blur="300000") # Softer shadow

    # Layer 5: Nested Accent Blue Arrow (Mathematically matched parallel slope)
    # Full geometry dx = 3.0, dy = 3.75 (Slope = 0.8 width/height)
    # Arrow head dy = 2.5, so dx must = 2.5 * 0.8 = 2.0 to maintain parallel angle
    ffb_arrow = slide.shapes.build_freeform(to_emu(-0.5), to_emu(2.25))
    ffb_arrow.add_line_segments([
        (to_emu(5.5), to_emu(2.25)),   # Stem top right
        (to_emu(5.5), to_emu(1.25)),   # Arrow head top right
        (to_emu(7.5), to_emu(3.75)),   # Arrow point (Matched to dx=2.0)
        (to_emu(5.5), to_emu(6.25)),   # Arrow head bottom right
        (to_emu(5.5), to_emu(5.25)),   # Stem bottom right
        (to_emu(-0.5), to_emu(5.25)),  # Stem bottom left
        (to_emu(-0.5), to_emu(2.25))   # Close
    ], close=True)
    blue_arrow = ffb_arrow.convert_to_shape()
    blue_arrow.line.fill.background()
    blue_arrow.fill.solid()
    blue_arrow.fill.fore_color.rgb = RGBColor(*accent_color)
    apply_shadow(blue_arrow, dist="150000")

    # === Add Typography ===
    
    # Title Text (Inside Blue Arrow Stem)
    tx_title = slide.shapes.add_textbox(to_emu(0.5), to_emu(2.7), to_emu(4.8), to_emu(1.0))
    tf_title = tx_title.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(64)
    p_title.font.bold = True
    p_title.font.name = "Arial"
    p_title.font.color.rgb = RGBColor(255, 255, 255)

    # Subtitle Text
    tx_sub = slide.shapes.add_textbox(to_emu(0.5), to_emu(3.9), to_emu(4.8), to_emu(0.8))
    tf_sub = tx_sub.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.add_paragraph()
    p_sub.text = body_text.upper()
    p_sub.font.size = Pt(18)
    p_sub.font.bold = True
    p_sub.font.name = "Arial"
    p_sub.font.color.rgb = RGBColor(224, 242, 254) # Pale blue

    # Cleanup
    if os.path.exists(img_path):
        os.remove(img_path)

    prs.save(output_pptx_path)
    return output_pptx_path
```