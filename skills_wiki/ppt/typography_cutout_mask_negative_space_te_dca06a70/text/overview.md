# Typography Cutout Mask (Negative Space Text Reveal)

## Analysis

# Role: Agent_Skill_Distiller (PPTX Design Style & Pattern Extractor)

### 1. High-level Design Pattern Extraction

> **Skill Name**: Typography Cutout Mask (Negative Space Text Reveal)

* **Core Visual Mechanism**: The defining visual idea is **negative space typography**. Instead of text sitting *on top* of a background, the text acts as a transparent window (a "cutout" or "hole") punched through a solid-color foreground, revealing a rich, full-bleed photograph or video beneath it.
* **Why Use This Skill (Rationale)**: This technique solves the classic design problem of placing text over busy images. By using the image *only* inside the thick text characters, you retain absolute legibility for the rest of the slide (which is a solid color). It creates a highly editorial, modern, and premium aesthetic, often seen in high-end magazines or Apple-style keynotes.
* **Overall Applicability**: Perfect for high-impact moments with very few words: Title slides, Section Headers, Hero statements, and "Thank You" / Closing slides. It works best with single words or very short phrases.
* **Value Addition**: Transforms a standard "text over picture" slide into a sophisticated graphic design composition. It commands attention and makes standard fonts look custom-designed.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Foreground Layer**: A solid color plane (e.g., light grey `RGBA(230, 230, 230, 255)` or dark navy) covering the entire slide.
  * **The Cutout (Mask)**: Heavy, ultra-thick typography (like *Impact*, *Arial Black*, or *Montserrat Black*). The thickness is crucial—thin fonts won't reveal enough of the underlying image to be recognizable.
  * **Background Layer**: A high-contrast, vibrant photograph (e.g., a sunset or cityscape).
  * **Accent Elements**: Thin intersecting geometry, such as a vertical line intersecting the main text, breaking the grid and adding a sense of motion or structure.
  * **Secondary Text**: High contrast, widely tracked (letter-spaced) sans-serif text placed cleanly on the solid foreground.

* **Step B: Compositional Style**
  * **Spatial Feel**: Centered, monolithic, and heavy. The main text dominates the center ~70% of the slide.
  * **Text Hierarchy**: 
    1. Primary (Cutout): Massive, heavy font, uppercase.
    2. Secondary (Standard): Small, clean, widely spaced uppercase font (e.g., 20pt with wide character spacing).

* **Step C: Dynamic Effects & Transitions**
  * The tutorial pairs this with a slow, horizontal moving vertical line and a slide transition that swaps the background image. The most critical dynamic effect here is the visual interaction between the foreground mask and whatever sits behind it.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Text Cutout (Subtract Shape) | **PIL/Pillow** | `python-pptx` cannot perform boolean shape operations (`Merge Shapes -> Subtract`). By using PIL, we can programmatically generate an alpha-transparent mask (a PNG) where the text acts as a transparent window in a solid colored block, perfectly mimicking the tutorial's core effect. |
| Background Image | **python-pptx native** | Simple full-bleed image insertion behind the PIL mask. |
| Secondary Text & Accents | **python-pptx native** | Standard shapes and text boxes perfectly handle the clean secondary text and intersecting vertical line. |

> **Feasibility Assessment**: 95%. The core visual effect (text acting as a window to a background image) is perfectly reproduced. The secondary text and layout are fully accurate. The exact PowerPoint "Morph/Line Wipe" animation shown at the end requires manual UI transition setup, but the layout structure prepared by the code makes it animation-ready.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "THANK YOU",
    sub_text: str = "DO YOU HAVE ANY QUESTIONS?",
    bg_keyword: str = "sunset,landscape",
    mask_color: tuple = (230, 230, 230, 255), # Light grey
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Typography Cutout Mask effect.
    Uses PIL to generate a solid layer with a transparent text hole.
    """
    import os
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw, ImageFont

    # --- Setup Presentation ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # --- Helper: Download Background Image ---
    bg_img_path = "temp_bg.jpg"
    try:
        url = f"https://source.unsplash.com/1920x1080/?{bg_keyword}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(bg_img_path, 'wb') as out_file:
            out_file.write(response.read())
    except Exception as e:
        print(f"Image download failed, generating fallback: {e}")
        fallback = Image.new('RGB', (1920, 1080), color=(50, 100, 150))
        fallback.save(bg_img_path)

    # --- Helper: Download Thick Font for Mask ---
    font_path = "Montserrat-Black.ttf"
    if not os.path.exists(font_path):
        try:
            # Download a heavy font to ensure the cutout effect works well
            font_url = "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Black.ttf"
            urllib.request.urlretrieve(font_url, font_path)
        except Exception:
            pass # Will fallback to default in PIL if download fails

    # --- Create the PIL Mask (The Core Effect) ---
    mask_img_path = "temp_mask.png"
    width, height = 1920, 1080
    
    # Create the solid foreground image
    img = Image.new('RGBA', (width, height), color=mask_color)
    
    # Create an alpha mask (255 = opaque foreground, 0 = transparent text hole)
    alpha_mask = Image.new('L', (width, height), color=255)
    draw = ImageDraw.Draw(alpha_mask)
    
    try:
        font = ImageFont.truetype(font_path, 360)
    except IOError:
        font = ImageFont.load_default()

    # Calculate text position (Centered)
    title_text = title_text.upper()
    try:
        bbox = draw.textbbox((0, 0), title_text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
    except AttributeError:
        # Fallback for older PIL versions
        text_w, text_h = draw.textsize(title_text, font=font)
        
    x = (width - text_w) / 2
    y = (height - text_h) / 2 - 50 # Slightly above true center
    
    # Draw text in black (0) on the alpha mask. This creates the "hole"
    draw.text((x, y), title_text, fill=0, font=font)
    
    # Apply the alpha mask to the solid image
    img.putalpha(alpha_mask)
    img.save(mask_img_path)

    # --- Assemble the Slide ---
    
    # 1. Background Image (Bottom Layer)
    slide.shapes.add_picture(bg_img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
    
    # 2. Text Cutout Mask (Middle Layer)
    slide.shapes.add_picture(mask_img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # 3. Accents and Secondary Text (Top Layer)
    
    # Intersecting Vertical Line
    line_x = prs.slide_width / 2 - Inches(3) # Offset to the left
    line_y = Inches(1.5)
    line_h = Inches(4.5)
    line_w = Inches(0.06)
    shape_line = slide.shapes.add_shape(
        1, # msoShapeRectangle
        line_x, line_y, line_w, line_h
    )
    shape_line.fill.solid()
    shape_line.fill.fore_color.rgb = RGBColor(20, 20, 20)
    shape_line.line.color.rgb = RGBColor(255, 255, 255)
    shape_line.line.width = Pt(1.5)

    # Secondary Text
    sub_text_box = slide.shapes.add_textbox(
        Inches(1), Inches(5.2), Inches(11.333), Inches(1)
    )
    tf = sub_text_box.text_frame
    tf.word_wrap = True
    p = tf.add_paragraph()
    p.text = sub_text.upper()
    p.alignment = PP_ALIGN.CENTER
    
    # Format Subtext
    p.font.name = "Arial"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = RGBColor(60, 60, 60)
    
    # Note: python-pptx doesn't natively support letter spacing/tracking
    # We simulate it by adding spaces between characters for the subtext
    spaced_sub_text = "  ".join(list(sub_text.upper()))
    p.text = spaced_sub_text

    # --- Save and Cleanup ---
    prs.save(output_pptx_path)
    
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)
    if os.path.exists(mask_img_path):
        os.remove(mask_img_path)

    return output_pptx_path
```