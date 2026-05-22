# Neon-Accented Asymmetric Geometric Layout

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Neon-Accented Asymmetric Geometric Layout

* **Core Visual Mechanism**: The defining signature of this style is the stark contrast between a deep, dark canvas and vibrant, high-luminance neon accents (specifically lime green and cyan). Structurally, it relies on **asymmetric rounded shapes** (e.g., rectangles where only the top-left and bottom-right corners are heavily rounded while others remain perfectly sharp). These custom geometries are used both as solid color blocks and as clipping masks for photography.

* **Why Use This Skill (Rationale)**: The asymmetric shapes break the rigid, predictable grid of traditional corporate slides, introducing a sense of forward momentum and innovation. The neon-on-dark color scheme mimics the UI of modern developer environments and tech dashboards, instantly signaling "high-tech," "software," or "cyber-security" to the audience without needing to explain it. 

* **Overall Applicability**: Perfect for IT product presentations, SaaS company pitch decks, cybersecurity reports, data analytics dashboards, and modern B2B tech portfolios. 

* **Value Addition**: Transforms a standard bullet-point slide into a highly engaging, brand-defining hero visual. It establishes immediate authority and modern aesthetic appeal, proving that the company's design standards match their technical innovation.

---

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**:
    - Background: Deep Slate/Navy `(44, 45, 53, 255)`
    - Accent 1 (Primary Neon): Lime Green `(196, 240, 66, 255)`
    - Accent 2 (Secondary): Cyan/Teal `(0, 208, 197, 255)`
    - Typography: Pure White `(255, 255, 255, 255)` for primary text, Light Grey `(180, 180, 180, 255)` for secondary text.
  - **Shape Language**: The "Round 2 Diagonal Rectangle" (rounded top-left and bottom-right) is the hero element. Overlapping shapes create depth without using drop shadows (flat design layered approach).
  - **Text Hierarchy**: Massive, bold, left-aligned sans-serif typography. Often, words are split across lines with alternating colors (White -> Grey) to emphasize specific terms.

* **Step B: Compositional Style**
  - **Spatial Feel**: A 50/50 horizontal split. The left hemisphere acts as the negative space anchor containing the typography. The right hemisphere acts as the "visual playground" with overlapping geometric intersections and the masked hero image.
  - **Proportions**: The main image block occupies ~40% of the canvas width on the right, slightly offset from the background color blocks to create an architectural, layered feel.

* **Step C: Dynamic Effects & Transitions**
  - Morph transitions and smooth push-ins complement this style perfectly, though the core visual impact comes entirely from the static geometric composition.

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Asymmetric Geometry Masks** | `python-pptx` `auto_shape_type` mapping | Standard `Picture` objects in `python-pptx` natively support mapping to `MSO_SHAPE` enums (like `ROUND_2_DIAG_RECT`), creating perfect "crop-to-shape" masks without complex XML injection. |
| **Overlapping Layout** | `python-pptx` Z-order via insertion order | Drawing background geometric accents first, then the image, then foreground accents accurately mimics the flat-layering depth of the tutorial. |
| **Fallback Image Generation** | `PIL/Pillow` | Ensures the code executes perfectly and produces a recognizable layout even if the external Unsplash image URL blocks the download. |

> **Feasibility Assessment**: 95%. The code reproduces the exact color palette, geometric masks, layout composition, and typographic hierarchy seen at the `0:02` mark of the tutorial. The slight default radius difference of PowerPoint's native auto-shapes is the only minor variance.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "IT PRODUCT\nPRESENTATION",
    bg_theme: str = "technology,code", 
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Neon-Accented Asymmetric Geometric Layout' 
    visual effect, complete with custom shape masking and overlapping neon accents.
    """
    import os
    import urllib.request
    from io import BytesIO
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image, ImageDraw

    # Initialize presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Color Palette ===
    COLOR_BG = RGBColor(44, 45, 53)
    COLOR_NEON_GREEN = RGBColor(196, 240, 66)
    COLOR_CYAN = RGBColor(0, 208, 197)
    COLOR_TEXT_WHITE = RGBColor(255, 255, 255)
    COLOR_TEXT_GREY = RGBColor(180, 180, 180)

    # === Layer 1: Background ===
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = COLOR_BG
    bg_shape.line.fill.background() # Remove border

    # === Layer 2: Background Geometric Accents ===
    # Neon Green accent block (Behind Image)
    accent_bg = slide.shapes.add_shape(
        MSO_SHAPE.ROUND_2_DIAG_RECT, 
        Inches(7.5), Inches(0.8), Inches(4.5), Inches(3.5)
    )
    accent_bg.fill.solid()
    accent_bg.fill.fore_color.rgb = COLOR_NEON_GREEN
    accent_bg.line.fill.background()
    # Increase corner rounding if supported by the shape
    try:
        accent_bg.adjustments[0] = 0.25 
    except:
        pass

    # === Layer 3: Image Fetch & Masking ===
    image_stream = BytesIO()
    try:
        # Attempt to fetch a relevant high-quality image
        url = f"https://images.unsplash.com/featured/800x600/?{bg_theme}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            image_stream.write(response.read())
    except Exception:
        # Fallback to PIL generated placeholder if offline or blocked
        img = Image.new('RGB', (800, 600), color=(60, 65, 80))
        draw = ImageDraw.Draw(img)
        draw.line([(0,0), (800,600)], fill=(80, 85, 100), width=5)
        draw.line([(0,600), (800,0)], fill=(80, 85, 100), width=5)
        img.save(image_stream, format='PNG')
    
    image_stream.seek(0)

    # Add Picture and apply Asymmetric Crop (The core visual trick)
    pic = slide.shapes.add_picture(
        image_stream, 
        Inches(6.2), Inches(1.8), Inches(5.0), Inches(3.8)
    )
    # Apply the signature top-left/bottom-right rounded shape
    pic.auto_shape_type = MSO_SHAPE.ROUND_2_DIAG_RECT


    # === Layer 4: Foreground Geometric Accents ===
    # Bottom Right Cyan Donut intersection
    donut = slide.shapes.add_shape(
        MSO_SHAPE.DONUT, 
        Inches(5.0), Inches(4.5), Inches(2.2), Inches(2.2)
    )
    donut.fill.solid()
    donut.fill.fore_color.rgb = COLOR_CYAN
    donut.line.fill.background()
    try:
        donut.adjustments[0] = 0.35 # Make the ring thicker
    except:
        pass

    # Small Top Left Green Logo/Accent block
    logo_accent = slide.shapes.add_shape(
        MSO_SHAPE.CHEVRON, 
        Inches(1.0), Inches(0.8), Inches(0.4), Inches(0.6)
    )
    logo_accent.fill.solid()
    logo_accent.fill.fore_color.rgb = COLOR_NEON_GREEN
    logo_accent.line.fill.background()


    # === Layer 5: Typography ===
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(5.0), Inches(2.0))
    tf = title_box.text_frame
    tf.clear() # Clear default paragraph
    
    lines = title_text.split('\n')
    
    # Line 1 (White, bold)
    p1 = tf.paragraphs[0]
    p1.text = lines[0] if len(lines) > 0 else "IT PRODUCT"
    p1.font.name = 'Arial' # Standard fallback for clean sans-serif
    p1.font.size = Pt(56)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_WHITE

    # Line 2 (Grey, bold)
    if len(lines) > 1:
        p2 = tf.add_paragraph()
        p2.text = lines[1]
        p2.font.name = 'Arial'
        p2.font.size = Pt(56)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT_GREY

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("neon_tech_layout.pptx", title_text="IT PRODUCT\nPRESENTATION")
```