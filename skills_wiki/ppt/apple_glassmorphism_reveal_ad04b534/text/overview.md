# Apple Glassmorphism Reveal

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Apple Glassmorphism Reveal

* **Core Visual Mechanism**: The defining visual signature is **frosted glass depth mapping**. It uses a highly textured, vibrant background (like leaves or colorful gradients) overlaid with translucent geometric shapes. The area *inside* the shapes displays a heavily blurred version of the background, mimicking the light refraction and depth of frosted glass. It is finished with a semi-transparent specular border (beveled edge) and a subtle drop shadow to create physical separation.
* **Why Use This Skill (Rationale)**: Glassmorphism solves a common presentation problem: how to maintain a beautiful, complex background without sacrificing text legibility. By blurring the area behind the text, it creates a dedicated, high-contrast focal plane while retaining the atmospheric color palette of the slide.
* **Overall Applicability**: Ideal for premium brand presentations, product reveals (especially software or tech hardware), portfolio title slides, or highlighting key quotes/metrics against lifestyle imagery.
* **Value Addition**: Transforms a standard "image + text box" slide into a sophisticated, modern UI experience. It communicates a high-end, contemporary brand identity reminiscent of macOS and iOS design languages.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **The Environment**: A vibrant, high-frequency background image (e.g., foliage, macro photography, abstract fluid art). Representative average color: Lush Green `(13, 115, 50, 255)`.
  * **The Glass Panels**: Geometric shapes (perfect circles or pill-shaped rectangles) acting as lenses.
    * *Refraction:* Heavy Gaussian blur applied to the background.
    * *Tint/Opacity:* A subtle white wash `(255, 255, 255, 40)` applied over the blurred area to boost text contrast.
    * *Specular Edge (Border):* A 2px to 4px semi-transparent white stroke `(255, 255, 255, 180)` simulating light hitting the edge of the glass.
  * **Text Hierarchy**: Center-aligned, crisp white text `(255, 255, 255, 255)` using modern sans-serif geometric fonts (like Poppins, Montserrat, or SF Pro), utilizing heavy weights for titles and lighter weights for subtitles.

* **Step B: Compositional Style**
  * **Spatial Feel**: Layered and floating. The design relies on the Z-axis (depth) rather than just X/Y placement.
  * **Proportions**: The glass shapes occupy roughly 30% to 45% of the total canvas. They are kept relatively small to allow the unblurred background to frame them. The circle radius is typically ~15-20% of the screen width.

* **Step C: Dynamic Effects & Transitions**
  * **In PowerPoint (Manual)**: By setting a shape's fill to "Slide Background Fill", dragging the shape dynamically updates the blur.
  * **In Code (Automated)**: Since PPTX API doesn't fully expose background mapping logic reliably across all templates, the exact visual result is achieved by pre-rendering a full-slide transparent composite layer. This guarantees a perfect 1:1 visual match for automated generation.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Background Blur & Frosted Lens | `PIL/Pillow` (ImageOps & Filter) | `python-pptx` cannot dynamically blur background regions. PIL allows us to create a mathematically perfect full-screen transparent overlay containing the blurred glass shapes. |
| Glass Edge & Drop Shadow | `PIL` ImageDraw / Composite | Generating the shadow and semi-transparent stroke inside the PIL PNG ensures pixel-perfect alignment and blending, avoiding PPTX rendering inconsistencies. |
| Text Placement | `python-pptx` native | Standard text frames are best for content so it remains editable for the user after the script runs. |

> **Feasibility Assessment**: 95% visual reproduction. The visual output will look virtually identical to the tutorial. The only difference is that the generated glass shapes are baked into a full-slide transparent PNG overlay, meaning if the user manually drags the shape in PowerPoint later, the background blur will not dynamically update as it does via PPT's manual UI trick. For automated slide generation, this is the most robust and accurate method.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "",
    body_text: str = "Apple Glass Effect",
    bg_keyword: str = "leaves,nature", 
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Apple Glassmorphism effect.
    Uses PIL to composite a perfect frosted glass overlay.
    """
    import os
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from PIL import Image, ImageDraw, ImageFilter, ImageOps

    # --- Configuration ---
    CANVAS_W, CANVAS_H = 1920, 1080
    bg_path = "temp_bg.jpg"
    overlay_path = "temp_overlay.png"

    # --- 1. Fetch Background Image ---
    try:
        url = f"https://source.unsplash.com/random/{CANVAS_W}x{CANVAS_H}/?{bg_keyword}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(bg_path, 'wb') as f:
                f.write(response.read())
        bg_img = Image.open(bg_path).convert("RGBA")
    except Exception as e:
        print(f"Image download failed, using fallback gradient. Error: {e}")
        # Fallback: Dark Green Gradient
        bg_img = Image.new("RGBA", (CANVAS_W, CANVAS_H))
        draw = ImageDraw.Draw(bg_img)
        for y in range(CANVAS_H):
            r = int(10 + (y / CANVAS_H) * 10)
            g = int(40 + (y / CANVAS_H) * 80)
            b = int(20 + (y / CANVAS_H) * 30)
            draw.line([(0, y), (CANVAS_W, y)], fill=(r, g, b, 255))
        bg_img.save(bg_path, "JPEG")

    # Ensure background is exactly the canvas size
    bg_img = ImageOps.fit(bg_img, (CANVAS_W, CANVAS_H), Image.Resampling.LANCZOS)
    
    # --- 2. Generate Glassmorphism Overlay via PIL ---
    # Create the heavily blurred version of the background
    blurred_bg = bg_img.filter(ImageFilter.GaussianBlur(radius=35))
    
    # Define Shape Geometries
    # Circle (Top Center)
    cx, cy, r = 960, 420, 200
    circle_bbox = [cx - r, cy - r, cx + r, cy + r]
    
    # Rounded Rectangle (Bottom Center)
    rect_w, rect_h = 1000, 200
    rx1, ry1 = 960 - (rect_w // 2), 700
    rx2, ry2 = 960 + (rect_w // 2), 700 + rect_h
    corner_radius = 50
    rect_bbox = [rx1, ry1, rx2, ry2]

    # Create Mask for the glass shapes
    glass_mask = Image.new("L", (CANVAS_W, CANVAS_H), 0)
    draw_mask = ImageDraw.Draw(glass_mask)
    draw_mask.ellipse(circle_bbox, fill=255)
    draw_mask.rounded_rectangle(rect_bbox, radius=corner_radius, fill=255)

    # Extract the blurred background only inside the shapes
    glass_layer = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    glass_layer.paste(blurred_bg, (0, 0), mask=glass_mask)

    # Add frosted white tint (opacity 40)
    tint_layer = Image.new("RGBA", (CANVAS_W, CANVAS_H), (255, 255, 255, 40))
    glass_layer.paste(tint_layer, (0, 0), mask=glass_mask)

    # Create Drop Shadows
    shadow_layer = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    draw_shadow = ImageDraw.Draw(shadow_layer)
    shadow_offset = 15
    # Draw black shapes, then blur them to create shadow
    draw_shadow.ellipse([x + shadow_offset for x in circle_bbox], fill=(0, 0, 0, 120))
    draw_shadow.rounded_rectangle([rx1 + shadow_offset, ry1 + shadow_offset, 
                                   rx2 + shadow_offset, ry2 + shadow_offset], 
                                  radius=corner_radius, fill=(0, 0, 0, 120))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=20))

    # Add Specular Edges (Borders)
    border_layer = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    draw_border = ImageDraw.Draw(border_layer)
    draw_border.ellipse(circle_bbox, outline=(255, 255, 255, 180), width=4)
    draw_border.rounded_rectangle(rect_bbox, radius=corner_radius, outline=(255, 255, 255, 180), width=4)

    # Composite Layers: Shadow -> Glass -> Borders
    final_overlay = Image.alpha_composite(shadow_layer, glass_layer)
    final_overlay = Image.alpha_composite(final_overlay, border_layer)
    final_overlay.save(overlay_path, "PNG")

    # --- 3. Construct the PPTX ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Layer 0: The crisp background image
    slide.shapes.add_picture(bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # Layer 1: The Glassmorphism Overlay (perfectly aligned)
    slide.shapes.add_picture(overlay_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # Layer 2: Text inside the Circle
    # Convert pixels to Inches for PPTX placement (1920x1080 -> 13.333x7.5 means 144 DPI mapping)
    dpi = 144
    circ_tb = slide.shapes.add_textbox(Inches(cx / dpi - 1), Inches(cy / dpi - 1), Inches(2), Inches(2))
    circ_tf = circ_tb.text_frame
    circ_tf.text = title_text
    circ_tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    circ_tf.paragraphs[0].font.size = Pt(80)
    circ_tf.paragraphs[0].font.bold = True
    circ_tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

    # Layer 3: Text inside the Rounded Rectangle
    rect_tb = slide.shapes.add_textbox(Inches(rx1 / dpi), Inches(ry1 / dpi + 0.35), Inches(rect_w / dpi), Inches(1))
    rect_tf = rect_tb.text_frame
    rect_tf.text = body_text
    rect_tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    rect_tf.paragraphs[0].font.size = Pt(44)
    rect_tf.paragraphs[0].font.bold = True
    rect_tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

    # Save and clean up
    prs.save(output_pptx_path)
    if os.path.exists(bg_path): os.remove(bg_path)
    if os.path.exists(overlay_path): os.remove(overlay_path)

    return output_pptx_path
```