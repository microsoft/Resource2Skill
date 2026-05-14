# Corporate Geometric Arc Framing

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Corporate Geometric Arc Framing

* **Core Visual Mechanism**: The defining aesthetic of this style is the use of **oversized, off-canvas overlapping circles**. By placing geometric ovals whose centers are outside the slide boundaries, the viewer only sees sweeping arcs (semi-circles and quarter-circles) encroaching on the canvas. These arcs serve dual purposes: as abstract decorative borders (using solid colors or concentric lines) and as organic, soft frames for photography.
* **Why Use This Skill (Rationale)**: Large circular arcs break the rigid, rectangular nature of standard PowerPoint slides. They introduce fluid, organic movement that naturally draws the eye inward toward the text. Layering a hero image over a bold accent color (like gold) creates dynamic tension and visual depth without cluttering the screen.
* **Overall Applicability**: Perfect for corporate title slides, human resources presentations, team performance reviews, and modern company profiles. It conveys professionalism but feels approachable and modern.
* **Value Addition**: Transforms a basic "text + square photo" slide into a bespoke, agency-quality layout. The layered geometric masking makes any generic stock photo look custom-designed for the deck.


### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**:
    - Background: Warm, light cream `(242, 239, 233)`
    - Accent: Rich Gold `(232, 185, 59)`
    - Sub-Accent (Badges): Muted Blue/Slate `(43, 87, 115)`
    - Decorative Elements: Darker Cream `(230, 225, 215)`
    - Text: Dark Navy/Black `(15, 23, 42)`
  - **Text Hierarchy**: Huge, ultra-clean sans-serif typography. The primary word is regular weight, and the secondary word is significantly larger and bolded to create contrast.

* **Step B: Compositional Style**
  - **Left Edge (60%)**: Dominated by sweeping arcs. An underlying gold circle peeks out from behind a white-bordered circular photo, both protruding from the left edge.
  - **Right Edge (40%)**: Clean space dedicated to the title. The bottom right corner features subtle, overlapping transparent arcs to balance the heavy visual weight on the left.

* **Step C: Dynamic Effects & Transitions**
  - Works beautifully with PowerPoint's native "Morph" transition, especially if the large circles smoothly slide in from the left edge upon presentation startup.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Perfect Circular Image | **PIL/Pillow** | `python-pptx` cannot natively mask an inserted picture to a perfect circle without complex OpenXML (`lxml`) manipulation. PIL allows us to create an anti-aliased cropped PNG. |
| Sweeping Color Arcs | **python-pptx native** | Native shapes (`MSO_SHAPE.OVAL`) scale infinitely without pixelation. Placing them partially off-canvas perfectly replicates the sweeping edge arcs. |
| Typography & Badges | **python-pptx native** | Standard text boxes and rounded rectangles offer precise control over fonts, weights, and layout. |

> **Feasibility Assessment**: 100%. The code will perfectly recreate the compositional, color, and geometric logic of the tutorial's title slide.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Performance\nTeam",
    body_text: str = "Collection of 10+ PowerPoint Templates",
    bg_palette: str = "business team meeting",
    accent_color: tuple = (232, 185, 59),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Corporate Geometric Arc Framing" visual effect.
    """
    import os
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image, ImageDraw

    # 1. Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # 2. Setup Background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(242, 239, 233)  # Warm cream

    # 3. Add Bottom-Right Decorative Arcs (Background Layer)
    # By placing centers at (13.3, 7.5), we create quarter-circles in the corner.
    decor1 = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(8.333), Inches(2.5), Inches(10), Inches(10)
    )
    decor1.fill.solid()
    decor1.fill.fore_color.rgb = RGBColor(230, 225, 215)
    decor1.line.fill.background()

    decor2 = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(7.333), Inches(1.5), Inches(12), Inches(12)
    )
    decor2.fill.background()
    decor2.line.color.rgb = RGBColor(230, 225, 215)
    decor2.line.width = Pt(2)

    # 4. Add Left Edge Gold Accent Arc
    gold_arc = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, -Inches(7.5), -Inches(4), Inches(12), Inches(12)
    )
    gold_arc.fill.solid()
    gold_arc.fill.fore_color.rgb = RGBColor(*accent_color)
    gold_arc.line.fill.background()

    # 5. Add Left Edge White Rim (behind the photo)
    white_rim = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, -Inches(6.5), -Inches(1.5), Inches(11), Inches(11)
    )
    white_rim.fill.solid()
    white_rim.fill.fore_color.rgb = RGBColor(255, 255, 255)
    white_rim.line.fill.background()

    # 6. Fetch and Process Hero Image
    img_path = "temp_hero.jpg"
    masked_img_path = "temp_hero_circle.png"
    
    try:
        url = f"https://source.unsplash.com/random/1200x1200/?{bg_palette.replace(' ', ',')}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(img_path, 'wb') as f:
                f.write(response.read())
        img = Image.open(img_path).convert("RGBA")
    except Exception:
        # Fallback to a solid gray image if download fails
        img = Image.new("RGBA", (1200, 1200), (150, 150, 150, 255))

    # Crop to perfect square
    min_dim = min(img.size)
    left_crop = (img.size[0] - min_dim) / 2
    top_crop = (img.size[1] - min_dim) / 2
    img = img.crop((left_crop, top_crop, left_crop + min_dim, top_crop + min_dim))

    # Create anti-aliased circular mask
    scale = 4  # Supersampling for smooth edges
    mask = Image.new("L", (min_dim * scale, min_dim * scale), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, min_dim * scale, min_dim * scale), fill=255)
    mask = mask.resize((min_dim, min_dim), Image.Resampling.LANCZOS)

    # Apply mask and save
    circle_img = Image.new("RGBA", (min_dim, min_dim), (0, 0, 0, 0))
    circle_img.paste(img, (0, 0), mask)
    circle_img.save(masked_img_path, format="PNG")

    # 7. Insert Circular Image into PPTX
    # Placed exactly over the white rim, but slightly smaller to leave a border
    slide.shapes.add_picture(
        masked_img_path, -Inches(6.3), -Inches(1.3), Inches(10.6), Inches(10.6)
    )

    # 8. Add Typography & Text
    # Parse title (handles exactly two lines gracefully, or falls back to one)
    lines = title_text.split('\n')
    line1 = lines[0] if len(lines) > 0 else "Performance"
    line2 = lines[1] if len(lines) > 1 else "Team"

    text_box = slide.shapes.add_textbox(Inches(5.5), Inches(2.2), Inches(7), Inches(3))
    tf = text_box.text_frame
    tf.clear()

    # First word (Regular weight)
    p1 = tf.paragraphs[0]
    p1.text = line1
    p1.font.size = Pt(64)
    p1.font.name = "Segoe UI"
    p1.font.color.rgb = RGBColor(15, 23, 42)

    # Second word (Bold, larger)
    p2 = tf.add_paragraph()
    p2.text = line2
    p2.font.size = Pt(88)
    p2.font.bold = True
    p2.font.name = "Segoe UI"
    p2.font.color.rgb = RGBColor(15, 23, 42)
    # Tighten line spacing
    p2.line_spacing = Pt(90) 

    # 9. Add Subtitle Badge (Pill shape)
    pill = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.6), Inches(5.0), Inches(4.5), Inches(0.4)
    )
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(43, 87, 115)  # Muted corporate blue
    pill.line.fill.background()
    
    # Adjust pill text
    pill_tf = pill.text_frame
    pill_tf.text = body_text
    pill_tf.paragraphs[0].font.size = Pt(13)
    pill_tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

    # 10. Save and Cleanup
    prs.save(output_pptx_path)
    
    if os.path.exists(img_path):
        os.remove(img_path)
    if os.path.exists(masked_img_path):
        os.remove(masked_img_path)

    return output_pptx_path
```