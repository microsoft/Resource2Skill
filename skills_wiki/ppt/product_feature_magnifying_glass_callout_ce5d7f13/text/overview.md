# Product Feature "Magnifying Glass" Callout

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Product Feature "Magnifying Glass" Callout

* **Core Visual Mechanism**: This technique uses a macro-zoom circular cutout overlaid on a darkened version of the original image. It visually isolates and enlarges a specific detail of a product (e.g., a lens ring, a sofa armrest, or UI button) while retaining the macroscopic context in the background. A clean, high-contrast line connects the original feature location to the enlarged circular callout.
* **Why Use This Skill (Rationale)**: This solves the classic presentation dilemma of "Context vs. Detail." If you show the whole product, the audience can't see the fine craftsmanship or specific features. If you only show the macro shot, they lose a sense of scale and location. The magnifying glass effect guides the user's eye forcefully to the detail while anchoring it to the whole.
* **Overall Applicability**: Perfect for hardware product reveals, architectural detail slides, software UI feature highlights, and premium e-commerce catalogs. 
* **Value Addition**: Transforms a standard product photograph into an interactive, high-end "editorial" graphic. It demonstrates attention to detail and elevates the perceived quality of the product.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Base Background**: The original product image, slightly blurred and dimmed via a semi-transparent dark overlay (e.g., `(0, 0, 0, 150)`).
  - **Zoom Circle**: A perfectly circular crop of a specific coordinate on the original image, scaled up 1.5x to 2.5x. 
  - **Highlight Ring**: A solid border around the zoom circle (e.g., white `(255, 255, 255, 255)`) to separate it from the background.
  - **Connecting Line**: A 1pt or 2pt solid line connecting the feature's origin point to the floating zoom circle.
  - **Callout Typography**: Clean, sans-serif text aligned near the zoom circle, typically a bold title and a lighter, smaller description body.

* **Step B: Compositional Style**
  - **Contrast**: The background is pushed back (darkened), making the fully bright, opaque zoom circle pop out dramatically.
  - **Asymmetry**: The origin point is usually dictated by the product, but the zoom circle and text are deliberately offset into "negative space" (areas of the image with less clutter).
  - **Proportions**: The base image fills 100% of the canvas (16:9). The zoom circle occupies roughly 25-30% of the vertical height.

* **Step C: Dynamic Effects & Transitions**
  - *Code achievable*: The static composite of the zoom, mask, and dimming.
  - *PPT Native (Manual)*: A "Zoom" entrance animation for the circle, followed by a "Wipe" entrance for the connecting line, and a "Fade" for the text.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Darkened Base Background | PIL/Pillow | Allows precise color multiplication and alpha compositing before inserting into PPT. |
| Circular Zoom Crop | PIL/Pillow | `python-pptx` cannot natively take an arbitrary sub-region of an image, scale it, and apply a circular mask. PIL handles this perfectly via bounding boxes, resizing, and alpha masks. |
| Connecting Line & Text | `python-pptx` native | Drawing the lines and text in native PPTX allows the user to edit the text and adjust the line endpoints later if needed. |

> **Feasibility Assessment**: 95%. The code fully reproduces the core visual mechanism (the darkened background, the zoomed circular cutout, the border, the connecting line, and the text layout). Only manual animations are omitted.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Precision Craftsmanship",
    body_text: str = "The knurled focus ring is machined from a single block of aerospace-grade aluminum, providing unmatched tactile feedback.",
    bg_keyword: str = "camera lens dark",
    accent_color: tuple = (255, 255, 255),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Magnifying Glass" Product Detail Callout effect.
    Returns: path to the saved PPTX file.
    """
    import os
    import urllib.request
    from io import BytesIO
    from pptx import Presentation
    from pptx.util import Pt, Inches
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw, ImageFilter

    # --- PPTX Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Canvas dimensions in pixels (using 96 DPI as base)
    W_px, H_px = 1280, 720
    
    # --- PIL Image Generation ---
    try:
        # Attempt to fetch a relevant product image
        url = f"https://source.unsplash.com/random/{W_px}x{H_px}/?{urllib.parse.quote(bg_keyword)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            base_img = Image.open(BytesIO(response.read())).convert("RGBA")
    except Exception:
        # Fallback: Create a gradient dummy product background
        base_img = Image.new('RGBA', (W_px, H_px), (30, 30, 40, 255))
        draw = ImageDraw.Draw(base_img)
        # Draw some dummy geometry to act as the "product"
        draw.ellipse((400, 160, 800, 560), fill=(50, 50, 60, 255), outline=(100, 100, 120, 255), width=10)
        draw.ellipse((500, 260, 700, 460), fill=(20, 20, 30, 255))
        for i in range(0, 360, 10):
            draw.pieslice((450, 210, 750, 510), i, i+5, fill=(80, 80, 90, 255))

    # Ensure correct size
    base_img = base_img.resize((W_px, H_px), Image.Resampling.LANCZOS)
    
    # Define focus point on the original image (e.g., center-left) and target placement
    focus_x, focus_y = int(W_px * 0.4), int(H_px * 0.5)
    target_x, target_y = int(W_px * 0.75), int(H_px * 0.4)  # Center of the placed circle
    
    # Extract the crop area before dimming
    crop_radius = 120 # How much of the original image to capture
    zoom_factor = 1.8 # How much to enlarge it
    final_radius = int(crop_radius * zoom_factor)
    
    box = (focus_x - crop_radius, focus_y - crop_radius, focus_x + crop_radius, focus_y + crop_radius)
    zoom_crop = base_img.crop(box)
    zoom_crop = zoom_crop.resize((final_radius * 2, final_radius * 2), Image.Resampling.LANCZOS)
    
    # Create the dimming layer for the background
    dim_layer = Image.new("RGBA", (W_px, H_px), (0, 0, 0, 160)) # Darken 60%
    bg_dimmed = Image.alpha_composite(base_img, dim_layer)
    
    # Apply circular mask to the zoomed crop
    mask = Image.new("L", (final_radius * 2, final_radius * 2), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, final_radius * 2, final_radius * 2), fill=255)
    zoom_crop.putalpha(mask)
    
    # Draw a clean border ring around the zoom circle
    zoom_draw = ImageDraw.Draw(zoom_crop)
    border_width = 6
    zoom_draw.ellipse((border_width//2, border_width//2, 
                       final_radius*2 - border_width//2, final_radius*2 - border_width//2), 
                      outline=accent_color + (255,), width=border_width)
    
    # Composite the zoom circle onto the dimmed background
    # Note: target_x/y is the center, so calculate top-left for pasting
    paste_x = target_x - final_radius
    paste_y = target_y - final_radius
    bg_dimmed.paste(zoom_crop, (paste_x, paste_y), mask=zoom_crop)
    
    # Save composite image
    composite_path = "temp_zoom_bg.png"
    bg_dimmed.save(composite_path)
    
    # --- PPTX Element Assembly ---
    # 1. Add Background
    slide.shapes.add_picture(composite_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
    
    # Conversion factor from PIL pixels to PPTX Inches
    def px_to_inches(px):
        return Inches((px / W_px) * 13.333)
        
    def py_to_inches(py):
        return Inches((py / H_px) * 7.5)

    # 2. Draw Connecting Line (from focus point to edge of zoom circle)
    # Calculate intersection point on the circle edge for a cleaner line
    import math
    angle = math.atan2(target_y - focus_y, target_x - focus_x)
    edge_x = target_x - final_radius * math.cos(angle)
    edge_y = target_y - final_radius * math.sin(angle)

    line = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT, 
        px_to_inches(focus_x), py_to_inches(focus_y),
        px_to_inches(edge_x), py_to_inches(edge_y)
    )
    line.line.color.rgb = RGBColor(accent_color[0], accent_color[1], accent_color[2])
    line.line.width = Pt(1.5)
    # Add a small dot at the origin
    dot_radius = 6
    origin_dot = slide.shapes.add_shape(
        1, # Oval
        px_to_inches(focus_x - dot_radius), py_to_inches(focus_y - dot_radius),
        px_to_inches(dot_radius*2), py_to_inches(dot_radius*2)
    )
    origin_dot.fill.solid()
    origin_dot.fill.fore_color.rgb = RGBColor(accent_color[0], accent_color[1], accent_color[2])
    origin_dot.line.fill.background()

    # 3. Add Typography
    # Place text below the circle
    text_x = px_to_inches(target_x - final_radius)
    text_y = py_to_inches(target_y + final_radius + 20)
    text_w = px_to_inches(final_radius * 2.5)
    text_h = Inches(1.5)
    
    tb = slide.shapes.add_textbox(text_x, text_y, text_w, text_h)
    tf = tb.text_frame
    tf.word_wrap = True
    
    # Title
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Arial"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = RGBColor(accent_color[0], accent_color[1], accent_color[2])
    
    # Body
    p2 = tf.add_paragraph()
    p2.text = body_text
    p2.font.name = "Arial"
    p2.font.size = Pt(12)
    p2.font.color.rgb = RGBColor(200, 200, 200) # Light grey for readability
    p2.space_before = Pt(8)

    prs.save(output_pptx_path)
    
    # Cleanup temp image
    if os.path.exists(composite_path):
        os.remove(composite_path)
        
    return output_pptx_path
```