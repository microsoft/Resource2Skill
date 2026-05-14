# Asymmetric Masonry Color Blocking

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Asymmetric Masonry Color Blocking

* **Core Visual Mechanism**: The defining visual idea is an intersecting, masonry-style grid of rectangles. This technique interweaves solid blocks of bold color, precisely cropped photography, and rotated typography. The layout is further elevated by "offset wireframes" (thin border rectangles slightly shifted from their underlying photo blocks) to create a sense of depth and modern editorial flair.
* **Why Use This Skill (Rationale)**: By breaking the slide into distinct geometric compartments, you create natural visual boundaries that prevent information overload. The grid structure satisfies the eye's desire for order, while the asymmetry, offsets, and rotated text introduce dynamic tension, keeping the viewer engaged. 
* **Overall Applicability**: Ideal for "About Us" slides, team profiles, product highlights, and transition/title slides where you need to combine an aesthetic vibe (photos) with concrete information (text) without letting either overpower the other.
* **Value Addition**: Transforms a standard bullet-point and photo layout into a magazine-quality editorial spread. It communicates high production value, organization, and a contemporary brand identity.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: A tri-tone palette consisting of a neutral background, a deep anchoring color, and a vibrant accent. 
    - Background: Crisp Light Gray-Blue `(244, 245, 248)`
    - Anchor Block: Deep Purple/Navy `(74, 63, 107)`
    - Accent Block & Borders: Coral Pink `(240, 138, 138)`
  - **Photography**: Images are tightly cropped to fit exact rectangular aspect ratios, avoiding native distortion.
  - **Text Hierarchy**: Large, bold sans-serif titles rotated 90 degrees vertically in the anchor block, paired with clean, horizontally wrapped body copy in the accent blocks.

* **Step B: Compositional Style**
  - **Grid System**: A 3-column asymmetric layout with a 1-inch outer margin.
    - *Column 1* (~25% width): Tall solid color block containing the vertical title.
    - *Column 2* (~45% width): Large, dominant photo block wrapped in a 0.2-inch offset wireframe border.
    - *Column 3* (~30% width): Split horizontally into two smaller, equal-sized blocks (one solid color with text, one photo).
  - **Layering**: Subtle drop shadows under the filled blocks lift them off the canvas, while the offset wireframes sit flat, crossing the background and the shadow.

* **Step C: Dynamic Effects & Transitions**
  - *Code Achievable*: The exact geometric rendering, exact image cropping (via PIL), rotated text anchors, and Open XML (lxml) drop shadow injections.
  - *Manual Addition*: Applying a native PowerPoint "Push" or "Pan" transition horizontally fits this geometric style perfectly.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Image Cropping & Sizing** | `PIL` (Pillow) | `python-pptx` struggles with native image cropping without distorting or overflowing shapes. PIL pre-crops images to the exact physical aspect ratio before insertion. |
| **Drop Shadows** | `lxml` (XML Injection) | `python-pptx` natively lacks a Python API for shape drop shadows. By injecting `<a:effectLst>` directly into the shape's XML, we unlock PowerPoint's native shadow engine. |
| **Grid Layout & Text Rotation** | `python-pptx` native | Calculating center pivots allows us to perfectly overlap a rotated `-90` degree textbox over a vertical rectangle. |

> **Feasibility Assessment**: 100%. The grid proportions, exact image mapping, text rotation, offset borders, and drop shadows are fully reproducible using the combined `python-pptx`, `PIL`, and `lxml` approach.

#### 3b. Complete Reproduction Code

```python
import io
import urllib.request
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.xmlchemy import OxmlElement

def add_drop_shadow(shape, blur_pt=8, dist_pt=4, alpha_pct=25):
    """Injects OOXML to add a drop shadow to a standard python-pptx shape."""
    spPr = shape.element.spPr
    effectLst = OxmlElement('a:effectLst')
    outerShdw = OxmlElement('a:outerShdw')
    # Convert points to EMUs (1 pt = 12700 EMUs)
    outerShdw.set('blurRad', str(int(blur_pt * 12700)))
    outerShdw.set('dist', str(int(dist_pt * 12700)))
    outerShdw.set('dir', "2700000") # 45 degrees (down and right)
    outerShdw.set('algn', "tl")
    outerShdw.set('rotWithShape', "0")
    
    srgbClr = OxmlElement('a:srgbClr')
    srgbClr.set('val', "000000")
    alpha = OxmlElement('a:alpha')
    alpha.set('val', str(int(alpha_pct * 1000))) # 25% = 25000
    
    srgbClr.append(alpha)
    outerShdw.append(srgbClr)
    effectLst.append(outerShdw)
    spPr.append(effectLst)

def create_gradient_image(w_in, h_in, color1, color2):
    """Creates a smooth diagonal gradient fallback image using PIL."""
    dpi = 150
    w, h = int(w_in * dpi), int(h_in * dpi)
    img = Image.new('RGB', (w, h))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        r = int(color1[0] + (color2[0] - color1[0]) * y / h)
        g = int(color1[1] + (color2[1] - color1[1]) * y / h)
        b = int(color1[2] + (color2[2] - color1[2]) * y / h)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

def get_cropped_image(url, w_in, h_in, fallback_color1, fallback_color2):
    """Downloads an image and crops it to the exact aspect ratio needed, with fallback."""
    dpi = 150
    target_w, target_h = int(w_in * dpi), int(h_in * dpi)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            img = Image.open(io.BytesIO(response.read())).convert('RGB')
            img_aspect = img.width / img.height
            target_aspect = target_w / target_h
            
            if img_aspect > target_aspect:
                # Crop width
                new_w = int(target_aspect * img.height)
                left = (img.width - new_w) // 2
                img = img.crop((left, 0, left + new_w, img.height))
            else:
                # Crop height
                new_h = int(img.width / target_aspect)
                top = (img.height - new_h) // 2
                img = img.crop((0, top, img.width, top + new_h))
                
            img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            out = io.BytesIO()
            img.save(out, format='PNG')
            out.seek(0)
            return out
    except Exception:
        # Fallback to gradient if network fails
        return create_gradient_image(w_in, h_in, fallback_color1, fallback_color2)

def create_slide(
    output_pptx_path: str,
    title_text: str = "CREATIVE\nBLOCKS",
    body_text: str = "Presenting concepts through structured geometric layers and bold visual contrasts.",
    **kwargs
) -> str:
    """
    Creates a PPTX file reproducing the 'Asymmetric Masonry Color Blocking' effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Color Palette
    bg_color = RGBColor(244, 245, 248) # F4F5F8
    purple = RGBColor(74, 63, 107)     # 4A3F6B
    coral = RGBColor(240, 138, 138)    # F08A8A
    
    # 1. Slide Background
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = bg_color

    # --- Column 1: Anchor Color Block with Rotated Text ---
    # Coordinates for the physical shape
    left1, top1 = 0.866, 1.0
    w1, h1 = 3.0, 5.5
    
    shape1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left1), Inches(top1), Inches(w1), Inches(h1))
    shape1.fill.solid()
    shape1.fill.fore_color.rgb = purple
    shape1.line.fill.background()
    add_drop_shadow(shape1)

    # To perfectly align rotated text, we calculate the pivot center of the shape
    # Center X = left + (width/2) = 0.866 + 1.5 = 2.366
    # Center Y = top + (height/2) = 1.0 + 2.75 = 3.75
    # Since text is rotated -90, unrotated Width = 5.5, Height = 3.0
    # Unrotated Left = CenterX - (UnrotatedWidth/2) = 2.366 - 2.75 = -0.384
    # Unrotated Top = CenterY - (UnrotatedHeight/2) = 3.75 - 1.5 = 2.25
    tb1 = slide.shapes.add_textbox(Inches(-0.384), Inches(2.25), Inches(5.5), Inches(3.0))
    tb1.rotation = -90.0
    tf1 = tb1.text_frame
    tf1.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf1.text = title_text
    p1 = tf1.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.font.size = Pt(48)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)

    # --- Column 2: Large Photo Block with Offset Wireframe ---
    left2 = left1 + w1 + 0.3  # 0.3 inch gap
    top2 = 1.0
    w2, h2 = 4.5, 5.5

    # Wireframe Accent (Added first so it sits behind the photo slightly)
    offset = 0.2
    frame = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        Inches(left2 + offset), Inches(top2 + offset), 
        Inches(w2), Inches(h2)
    )
    frame.fill.background() # Simulates transparency against slide bg
    frame.line.color.rgb = coral
    frame.line.width = Pt(4)

    # Photo Block
    img1_url = "https://images.unsplash.com/photo-1558655146-d09347e92766?q=80&w=800"
    img1_stream = get_cropped_image(img1_url, w2, h2, (100, 100, 150), (50, 50, 80))
    pic1 = slide.shapes.add_picture(img1_stream, Inches(left2), Inches(top2), Inches(w2), Inches(h2))
    add_drop_shadow(pic1)

    # --- Column 3: Stacked Blocks ---
    left3 = left2 + w2 + 0.3
    w3 = 3.5
    h3 = 2.6 # (5.5 total height - 0.3 gap) / 2 = 2.6

    # Row 1: Solid Accent Block
    top3_1 = 1.0
    shape3 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left3), Inches(top3_1), Inches(w3), Inches(h3))
    shape3.fill.solid()
    shape3.fill.fore_color.rgb = coral
    shape3.line.fill.background()
    add_drop_shadow(shape3)

    # Text inside Row 1
    tb3 = slide.shapes.add_textbox(Inches(left3 + 0.2), Inches(top3_1 + 0.2), Inches(w3 - 0.4), Inches(h3 - 0.4))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p3 = tf3.paragraphs[0]
    p3.text = body_text
    p3.font.size = Pt(16)
    p3.font.color.rgb = RGBColor(255, 255, 255)

    # Row 2: Secondary Photo Block
    top3_2 = top3_1 + h3 + 0.3
    img2_url = "https://images.unsplash.com/photo-1513694203232-719a280e022f?q=80&w=800"
    img2_stream = get_cropped_image(img2_url, w3, h3, (200, 150, 150), (240, 200, 200))
    pic2 = slide.shapes.add_picture(img2_stream, Inches(left3), Inches(top3_2), Inches(w3), Inches(h3))
    add_drop_shadow(pic2)

    # --- Aesthetic Accents ---
    # Small floating square in top-left
    sq = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.866), Inches(0.5), Inches(0.2), Inches(0.2))
    sq.fill.solid()
    sq.fill.fore_color.rgb = coral
    sq.line.fill.background()

    # Small structural 'plus' icon acting as a masonry tie between cols 1 and 2
    cross_cx = left2 - 0.15
    cross_cy = 1.0 + (h1 / 2)
    c1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cross_cx - 0.02), Inches(cross_cy - 0.1), Inches(0.04), Inches(0.2))
    c1.fill.solid(); c1.fill.fore_color.rgb = purple; c1.line.fill.background()
    c2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cross_cx - 0.1), Inches(cross_cy - 0.02), Inches(0.2), Inches(0.04))
    c2.fill.solid(); c2.fill.fore_color.rgb = purple; c2.line.fill.background()

    prs.save(output_pptx_path)
    return output_pptx_path
```