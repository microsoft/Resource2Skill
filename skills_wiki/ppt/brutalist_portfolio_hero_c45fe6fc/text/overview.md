# Brutalist Portfolio Hero

## Analysis

# High-level Design Pattern Extraction

> **Skill Name**: Brutalist Portfolio Hero 

* **Core Visual Mechanism**: This pattern relies on extreme scale contrast (Micro vs. Macro typography) and Z-axis layering. It features precise, grid-aligned functional micro-text at the top, anchored by massive, edge-to-edge brutalist typography at the bottom. A horizontal "media reel" (with partially cropped images on the edges to imply horizontal scroll) lives in the center, and a high-contrast floating "pill" component overlaps the giant text to create a tangible sense of depth and hierarchy.
* **Why Use This Skill (Rationale)**: The juxtaposition of tiny metadata and aggressively large title text creates visual tension and high modernism (popularized by agency platforms like Awwwards). It immediately communicates a "design-first", confident, and contemporary aesthetic. The floating UI elements make the slide feel like an interactive web experience rather than a static presentation.
* **Overall Applicability**: Ideal for portfolio hero slides, creative agency introductions, product launch covers, or any scenario where brand aesthetic and bold statements are prioritized over dense information.
* **Value Addition**: Transforms a standard title slide into a premium, interactive-feeling "viewport", bringing modern web design sensibilities (glassmorphism, brutalism, spatial floating components) directly into PowerPoint.

---

# Visual Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Minimalist "Zinc" palette. 
    - Background: Off-white/Light Gray `(244, 244, 245)`
    - Primary Text/Pill Fill: Near Black `(24, 24, 27)`
    - Secondary Text (Metadata): Mid Gray `(113, 113, 122)`
    - Accent: A vivid pop color (e.g., Neon Blue or Pink) used sparingly on the primary CTA button.
  - **Typography**: Heavily bolded, oversized geometric sans-serif (e.g., Arial Black, >100pt) for the hero, and crisp, structured sans-serif (~9-10pt) for metadata.
  - **Imagery**: Abstract, modern, high-quality textures or 3D renders, styled with slightly rounded corners (pillbox geometry).

* **Step B: Compositional Style**
  - **Top Edge**: 3-column structured metadata + 1 pill-shaped Call-To-Action button.
  - **Center Canvas**: A 3-image carousel. The center image is fully framed, while the left and right images are deliberately cropped by the slide boundary to subconsciously imply a draggable scroll reel.
  - **Bottom Edge**: Giant typography acting as a foundational base, layered *underneath* a floating pill-shaped profile widget.

* **Step C: Dynamic Effects & Transitions**
  - **Web Mimicry**: The subtle drop shadow applied to the floating pill creates the illusion of a sticky web component hovering over scrolled content. 
  - *Note: While the video features actual scroll interactions, this slide replicates the "frozen moment" of that motion.*

---

# Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Pill shapes & UI Cards** | `python-pptx` native | Modifying `shape.adjustments[0] = 0.5` natively yields perfect capsule/pill shapes without complex SVG math. |
| **Media Reel & Cropping** | `python-pptx` shape placement | Placing shapes partially off-canvas naturally replicates the web "overflow-x" horizontal scroll aesthetic. |
| **Dynamic Image Fetching** | `urllib` & `PIL` (fallback) | Automatically pulls modern, high-res Unsplash imagery to match the aesthetic, with built-in PIL fallback generation if offline. |
| **Floating Z-Axis Shadows** | `lxml` XML injection | PowerPoint's native shadow APIs via `python-pptx` are limited. Lxml injection allows for precise, soft, web-style drop shadows that make the UI pills "float". |

*Feasibility Assessment: 95% reproduction of the static visual frame. The web-based scroll motion cannot be rendered natively in PPTX, but the spatial depth and visual web aesthetic are completely captured.*

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "DESIGN ENGINEER",
    body_text: str = "JASON ZUBIATE",
    bg_palette: str = "technology",
    accent_color: tuple = (0, 191, 255),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Brutalist Portfolio Hero visual effect.
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml import OxmlElement
    from pptx.oxml.ns import qn
    import os
    import urllib.request
    from PIL import Image

    # --- Helper: Robust Image Fetching ---
    def get_image(url, filename, size=(800, 600), color=(200, 200, 200)):
        if os.path.exists(filename):
            return filename
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                with open(filename, 'wb') as f:
                    f.write(response.read())
            return filename
        except Exception:
            # Fallback block generation if network fails
            img = Image.new('RGB', size, color)
            img.save(filename)
            return filename

    # --- Helper: LXML Web-Style Soft Drop Shadow ---
    def apply_shadow(shape, opacity='15000', blur='150000', dist='80000'):
        spPr = shape.element.spPr
        effectLst = spPr.find(qn('a:effectLst'))
        if effectLst is None:
            effectLst = OxmlElement('a:effectLst')
            spPr.append(effectLst)
        
        outerShdw = OxmlElement('a:outerShdw')
        outerShdw.set('blurRad', blur)       # Blur radius
        outerShdw.set('dist', dist)          # Distance
        outerShdw.set('dir', '5400000')      # 90 degrees (straight down)
        outerShdw.set('algn', 'b')
        
        srgbClr = OxmlElement('a:srgbClr')
        srgbClr.set('val', '000000')
        alpha = OxmlElement('a:alpha')
        alpha.set('val', opacity)            # Opacity percentage
        
        srgbClr.append(alpha)
        outerShdw.append(srgbClr)
        effectLst.append(outerShdw)

    # --- Presentation Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Slide Background (Off-white "Zinc")
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(244, 244, 245)

    # --- LAYER 1: Top Navigation & Metadata ---
    def add_meta(x, y, t1, t2):
        tx = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(2.5), Inches(0.8))
        tf = tx.text_frame
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        p1 = tf.paragraphs[0]
        p1.text = t1
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.name = "Arial"
        p1.font.color.rgb = RGBColor(24, 24, 27)
        
        p2 = tf.add_paragraph()
        p2.text = t2
        p2.font.size = Pt(10)
        p2.font.name = "Arial"
        p2.font.color.rgb = RGBColor(113, 113, 122)

    add_meta(0.8, 0.5, "US Based", "Working globally")
    add_meta(3.5, 0.5, "Building at", "Trackstack")
    add_meta(6.5, 0.5, "Freelance availability", "July 2025")

    # Top Nav CTA Button
    btn = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(11.0), Inches(0.5), Inches(1.5), Inches(0.4))
    btn.adjustments[0] = 0.5 # 50% adjustment makes a perfect pill shape
    btn.fill.solid()
    btn.fill.fore_color.rgb = RGBColor(*accent_color)
    btn.line.color.rgb = RGBColor(*accent_color)
    tf = btn.text_frame
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "Get in touch"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.name = "Arial"
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

    # --- LAYER 2: Horizontal Scroll Media Reel ---
    img_center = get_image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&q=80", "tmp_center.jpg", (800, 600), (200, 220, 255))
    img_left = get_image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&q=80", "tmp_left.jpg", (800, 600), (220, 255, 200))
    img_right = get_image("https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?w=800&q=80", "tmp_right.jpg", (800, 600), (255, 200, 220))

    def add_reel_img(x, y, w, h, img_path):
        shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        shp.adjustments[0] = 0.05 # Gentle modern rounded corners
        shp.fill.user_picture(img_path)
        shp.line.color.rgb = RGBColor(244, 244, 245) # Blend outline with bg
        return shp

    reel_w, reel_h, gap = 4.66, 3.5, 0.3
    cx = (13.333 - reel_w) / 2
    y_reel = 1.3

    # Left and Right images intentionally placed partially off-canvas
    add_reel_img(cx - reel_w - gap, y_reel, reel_w, reel_h, img_left)
    add_reel_img(cx + reel_w + gap, y_reel, reel_w, reel_h, img_right)
    center_shp = add_reel_img(cx, y_reel, reel_w, reel_h, img_center)
    apply_shadow(center_shp, opacity='10000', blur='300000', dist='0') # Soft ambient shadow

    # --- LAYER 3: Micro & Macro Typography ---
    def add_micro(x, y, txt, align, w=1.5):
        tx = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(0.4))
        tf = tx.text_frame
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        p = tf.paragraphs[0]
        p.text = txt
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.name = "Arial"
        p.font.color.rgb = RGBColor(161, 161, 170)
        if align == 'center': p.alignment = PP_ALIGN.CENTER
        elif align == 'right': p.alignment = PP_ALIGN.RIGHT

    y_micro = 5.0
    add_micro(0.8, y_micro, "A", 'left')
    add_micro(5.9, y_micro, "SERIOUSLY", 'center')
    add_micro(11.0, y_micro, "GOOD", 'right')

    # Massive edge-to-edge typography
    tx = slide.shapes.add_textbox(Inches(0), Inches(5.1), Inches(13.333), Inches(2.0))
    tf = tx.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.text = title_text.upper()
    p.font.size = Pt(100)
    p.font.bold = True
    p.font.name = "Arial Black" # Essential for brutalist weight
    p.font.color.rgb = RGBColor(24, 24, 27)
    p.alignment = PP_ALIGN.CENTER

    # --- LAYER 4: Floating Profile Pill Component ---
    pill_w, pill_h = 4.0, 0.8
    pill_x = (13.333 - pill_w) / 2
    pill_y = 6.4 # Overlaps the giant typography

    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(pill_x), Inches(pill_y), Inches(pill_w), Inches(pill_h))
    pill.adjustments[0] = 0.5
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(24, 24, 27)
    pill.line.color.rgb = RGBColor(24, 24, 27)
    apply_shadow(pill, opacity='25000', blur='200000', dist='100000') # Strong pop-out shadow

    # Profile Avatar
    pic_img = get_image("https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80", "tmp_profile.jpg", (400, 400), (100, 100, 100))
    pic_size = 0.6
    pic = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(pill_x + 0.1), Inches(pill_y + 0.1), Inches(pic_size), Inches(pic_size))
    pic.adjustments[0] = 0.5
    pic.fill.user_picture(pic_img)
    pic.line.color.rgb = RGBColor(24, 24, 27)

    # Widget Text
    ptx = slide.shapes.add_textbox(Inches(pill_x + 0.8), Inches(pill_y + 0.15), Inches(2.5), Inches(0.5))
    ptf = ptx.text_frame
    ptf.margin_top = ptf.margin_bottom = ptf.margin_left = ptf.margin_right = 0
    pp1 = ptf.paragraphs[0]
    pp1.text = body_text if body_text else "JASON ZUBIATE"
    pp1.font.size = Pt(11)
    pp1.font.bold = True
    pp1.font.name = "Arial"
    pp1.font.color.rgb = RGBColor(255, 255, 255)
    
    pp2 = ptf.add_paragraph()
    pp2.text = "CREATIVE DESIGN ENGINEER"
    pp2.font.size = Pt(8)
    pp2.font.name = "Arial"
    pp2.font.color.rgb = RGBColor(161, 161, 170)

    # Hamburger Menu Icon (using Unicode)
    htx = slide.shapes.add_textbox(Inches(pill_x + pill_w - 0.4), Inches(pill_y + 0.25), Inches(0.3), Inches(0.3))
    htf = htx.text_frame
    htf.margin_top = htf.margin_bottom = htf.margin_left = htf.margin_right = 0
    hp = htf.paragraphs[0]
    hp.text = "≡"
    hp.font.size = Pt(16)
    hp.font.bold = True
    hp.font.name = "Arial"
    hp.font.color.rgb = RGBColor(255, 255, 255)
    hp.alignment = PP_ALIGN.CENTER

    # --- Cleanup & Save ---
    for f in ["tmp_center.jpg", "tmp_left.jpg", "tmp_right.jpg", "tmp_profile.jpg"]:
        if os.path.exists(f):
            try: os.remove(f)
            except: pass

    prs.save(output_pptx_path)
    return output_pptx_path
```