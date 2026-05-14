# Corporate Color Block & Masonry Hero Slide

## Analysis

Here is the structured extraction of the design style and the corresponding reproducible Python code.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Corporate Color Block & Masonry Hero Slide

* **Core Visual Mechanism**: This style is defined by a clean, asymmetric layout balancing bold, structured typography on one side with a multi-image "masonry" (grid) collage on the other. It utilizes a subtle, geometrically patterned background (like dots or faint hexes) overlaid with distinct, floating pastel color blocks that act as accents and text anchors.
* **Why Use This Skill (Rationale)**: Breaking a single large image into a masonry grid feels more dynamic and modern than a standard full-bleed background. The soft geometric background combined with floating color blocks creates depth without clutter, cleanly separating the "information delivery" zone (text) from the "emotional/visual" zone (images).
* **Overall Applicability**: Ideal for corporate presentations, title slides, section headers, product launch introductions, and company overviews. 
* **Value Addition**: Transforms a standard title slide into a highly professional, template-grade "hero" slide. The structured image grid accommodates multiple visual concepts (e.g., team + product + office) without looking messy.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Color Logic**:
    * Background: Off-white/Light Gray `(245, 245, 245, 255)` with faint gray patterning `(230, 230, 230, 255)`.
    * Primary Accent (Coral/Salmon): `(244, 152, 140)` — used for primary headers and small icon accents.
    * Secondary Accent (Plum/Dark Purple): `(89, 50, 76)` — used as solid square blocks behind images to add depth.
    * Typography: Charcoal/Soft Black `(40, 40, 40)` for high contrast readability.
  * **Text Hierarchy**: Two-tone massive header (Top line colored, bottom line dark on a light block), followed by a thin divider line and a standard sans-serif subtitle.

* **Step B: Compositional Style**
  * **Spatial Feel**: ~45% of the left screen is dedicated to whitespace and typography. ~55% of the right screen is dedicated to tightly packed rectangular images and overlapping accent squares.
  * **Z-Index/Layering**: Background Pattern -> Accent Color Blocks -> Images -> Typography.

* **Step C: Dynamic Effects & Transitions**
  * Best paired with standard PowerPoint "Fade" or "Slide/Push" transitions. The floating blocks lend themselves well to "Fly In" animations, though this reproduction will focus on the static compositional architecture.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Subtle Geometric Background** | `PIL/Pillow` | `python-pptx` cannot natively generate repeating pattern fills easily across environments. PIL generates a high-quality seamless texture overlay. |
| **Masonry Image Collage** | `urllib` + `python-pptx` | Downloads proportionally accurate placeholder images and arranges them into a precise multi-block grid using native shape positioning. |
| **Color Blocks & Typography** | `python-pptx` native | Standard shape insertions (`add_shape`, `add_textbox`) are perfect for the rigid, blocky corporate text layout. |

*Feasibility Assessment*: 95%. The code generates the exact layout, color scheme, masonry grid, and patterned background seen in the title slide of the video. Font rendering will depend on local system fonts, defaulting to sans-serif.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_line1: str = "New Product",
    title_line2: str = "Evaluation",
    subtitle: str = "Your Company Name",
    bg_palette: str = "business",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Corporate Color Block & Masonry Hero Slide" visual effect.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from PIL import Image, ImageDraw
    import urllib.request
    import io
    import os

    # === Setup Presentation ===
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide

    # === Colors ===
    color_coral = RGBColor(244, 152, 140)
    color_plum = RGBColor(89, 50, 76)
    color_dark = RGBColor(40, 40, 40)
    color_bg_block = RGBColor(235, 235, 235)

    # === Helper Functions ===
    def fetch_image(width_px, height_px, fallback_color):
        """Fetches an image from picsum.photos, falls back to a solid PIL image if offline."""
        url = f"https://picsum.photos/{width_px}/{height_px}?random=1"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                return io.BytesIO(response.read())
        except Exception:
            img = Image.new('RGB', (width_px, height_px), fallback_color)
            bio = io.BytesIO()
            img.save(bio, format='PNG')
            bio.seek(0)
            return bio

    def generate_pattern_bg():
        """Generates a subtle geometric plus-pattern background."""
        bg_path = "temp_bg_pattern.png"
        img = Image.new('RGBA', (1920, 1080), (245, 245, 245, 255))
        draw = ImageDraw.Draw(img)
        # Draw a subtle plus/cross grid pattern
        spacing = 40
        for x in range(0, 1920, spacing):
            for y in range(0, 1080, spacing):
                draw.line([(x-2, y), (x+2, y)], fill=(225, 225, 225, 255), width=1)
                draw.line([(x, y-2), (x, y+2)], fill=(225, 225, 225, 255), width=1)
        img.save(bg_path)
        return bg_path

    # === Layer 1: Background ===
    bg_path = generate_pattern_bg()
    slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)
    if os.path.exists(bg_path):
        os.remove(bg_path)

    # === Layer 2: Color Blocks (Accents) ===
    # Small plum square behind main image
    block1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.5), Inches(0.5), Inches(1.5), Inches(1.5))
    block1.fill.solid()
    block1.fill.fore_color.rgb = color_plum
    block1.line.fill.background()

    # Small plum square at bottom right
    block2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(12.0), Inches(6.0), Inches(1.0), Inches(1.0))
    block2.fill.solid()
    block2.fill.fore_color.rgb = color_plum
    block2.line.fill.background()

    # === Layer 3: Masonry Image Collage ===
    # Image 1 (Main Tall, Center-Right)
    img1_stream = fetch_image(400, 600, (200, 200, 200))
    slide.shapes.add_picture(img1_stream, Inches(6.0), Inches(1.0), Inches(3.5), Inches(5.5))

    # Image 2 (Top Right)
    img2_stream = fetch_image(300, 280, (180, 180, 180))
    slide.shapes.add_picture(img2_stream, Inches(9.7), Inches(1.0), Inches(2.8), Inches(2.6))

    # Image 3 (Bottom Right)
    img3_stream = fetch_image(300, 280, (160, 160, 160))
    slide.shapes.add_picture(img3_stream, Inches(9.7), Inches(3.9), Inches(2.8), Inches(2.6))

    # === Layer 4: Typography & Text Layout ===
    
    # Line 1 (Coral, Bold)
    tx_box1 = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5), Inches(1.0))
    tf1 = tx_box1.text_frame
    p1 = tf1.add_paragraph()
    p1.text = title_line1.upper()
    p1.font.size = Pt(54)
    p1.font.bold = True
    p1.font.name = "Arial"
    p1.font.color.rgb = color_coral

    # Line 2 Background Block (Light Gray block under text)
    title2_block = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.9), Inches(4.5), Inches(1.2))
    title2_block.fill.solid()
    title2_block.fill.fore_color.rgb = color_bg_block
    title2_block.line.fill.background()

    # Line 2 Text (Dark, inside the block)
    tx_box2 = slide.shapes.add_textbox(Inches(0.9), Inches(3.0), Inches(4.3), Inches(1.0))
    tf2 = tx_box2.text_frame
    p2 = tf2.add_paragraph()
    p2.text = title_line2
    p2.font.size = Pt(60)
    p2.font.bold = True
    p2.font.name = "Arial"
    p2.font.color.rgb = color_dark

    # Icon/Divider block (Simulating the small checklist icon area)
    icon_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.5), Inches(0.6), Inches(0.6))
    icon_bg.fill.solid()
    icon_bg.fill.fore_color.rgb = RGBColor(255, 255, 255)
    icon_bg.line.color.rgb = color_coral
    icon_bg.line.width = Pt(1.5)
    
    # Subtitle
    tx_box3 = slide.shapes.add_textbox(Inches(1.6), Inches(4.45), Inches(4.0), Inches(0.6))
    tf3 = tx_box3.text_frame
    tf3.vertical_anchor = MSO_ANCHOR.MIDDLE
    p3 = tf3.add_paragraph()
    p3.text = subtitle
    p3.font.size = Pt(20)
    p3.font.name = "Arial"
    p3.font.color.rgb = color_dark

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
```