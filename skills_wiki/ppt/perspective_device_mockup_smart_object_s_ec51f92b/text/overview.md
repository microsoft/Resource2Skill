# Perspective Device Mockup (Smart Object Simulation)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Perspective Device Mockup (Smart Object Simulation)

* **Core Visual Mechanism**: The core visual idea is seamlessly inserting a flat 2D image (like a screenshot, UI design, or photograph) into a 3D perspective environment—specifically, onto the angled screen of a device like a laptop or phone. This creates a realistic "in-situ" mockup that simulates Photoshop's "Smart Object" perspective warp feature.
* **Why Use This Skill (Rationale)**: Flat screenshots can look dry and unengaging. Placing content inside a realistic device context immediately gives it scale, usability context, and a premium, finished feel. The perspective angle creates depth and draws the viewer's eye dynamically across the slide.
* **Overall Applicability**: Ideal for software product showcases, portfolio presentations, web design proposals, digital transformation slide decks, and any scenario where digital content needs to be presented professionally in the real world.
* **Value Addition**: Transforms a basic image insertion into a high-end graphic design asset. It elevates the perceived quality of the content and demonstrates a high level of design polish without requiring external design software.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Environment/Backdrop**: A stylized or photographic desk/office surface that provides spatial context. (e.g., gradient base from `(240, 245, 250, 255)` to `(200, 205, 215, 255)`).
  - **Device Frame (Bezel)**: The physical casing of the device, drawn with dark grays `(40, 42, 45, 255)` and metallic silver accents `(180, 185, 190, 255)` to separate the screen from the background.
  - **Warped Content Layer**: The user's image, mathematically skewed via a homography matrix to perfectly match the 4 corners of the angled device screen.
  - **Screen Glare/Reflection**: A subtle, semi-transparent white polygon `(255, 255, 255, 15)` overlaid on the screen area to mimic the physical properties of a glass display.
  - **Typography Context**: Clean, high-contrast text positioned in the negative space (typically beside the device) to anchor the visual and provide context.

* **Step B: Compositional Style**
  - **Asymmetrical Balance**: The perspective laptop dominates the left 60-70% of the canvas, angling inward. The text is neatly aligned on the remaining 30-40% on the right, balancing the heavy visual weight of the device.
  - **Depth Layering**: Background $\rightarrow$ Laptop Base $\rightarrow$ Laptop Bezel $\rightarrow$ Warped Screen Content $\rightarrow$ Screen Glare.

* **Step C: Dynamic Effects & Transitions**
  - While the final output is static, the visual *implies* depth. In PowerPoint, this pairs exceptionally well with the "Push" or "Fade" transition, letting the complex 3D mockup ground the slide while text elements fade in via standard animations.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Perspective Warp (Smart Object)** | `PIL` + `numpy` | `python-pptx` natively lacks the ability to skew an image into an arbitrary 4-point perspective polygon. PIL with a calculated homography matrix perfectly recreates Photoshop's `Ctrl+T` corner distortion. |
| **Masking & Screen Glare** | `PIL` `ImageDraw` | Needed to ensure the warped image doesn't bleed over the laptop bezel and to overlay transparent glass reflections. |
| **Typography & Slide Layout** | `python-pptx` | Best for rendering crisp vector text and positioning the final composite image as the slide backdrop. |

> **Feasibility Assessment**: 100% of the core visual mechanism (perspective content replacement) is reproduced programmatically. Instead of requiring Photoshop Smart Objects, this code mathematically generates the exact same visual composite on the fly.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Digital Ecosystem",
    body_text: str = "Seamlessly deploy your solutions across all platforms with responsive, pixel-perfect accuracy.",
    bg_palette: str = "technology",
    accent_color: tuple = (0, 191, 255),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Perspective Device Mockup (Smart Object) effect.
    Returns: path to the saved PPTX file.
    """
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter
    from pptx import Presentation
    from pptx.util import Pt, Inches
    from pptx.dml.color import RGBColor
    import urllib.request
    import io
    import os

    # 1. Setup Base Canvas
    W, H = 1280, 720
    base_img = Image.new('RGBA', (W, H), (245, 247, 250, 255))
    draw = ImageDraw.Draw(base_img)

    # 2. Draw Environment (Stylized Desk)
    # Gradient desk
    desk_start = H // 2 + 50
    for y in range(desk_start, H):
        ratio = (y - desk_start) / (H - desk_start)
        c = int(240 - ratio * 45)
        draw.line([(0, y), (W, y)], fill=(c, c+3, c+8, 255))
    
    # Subtle drop shadow for the laptop base
    draw.polygon([(100, 660), (900, 580), (1100, 680), (200, 760)], fill=(180, 185, 190, 120))

    # 3. Draw Laptop Geometry (Viewed from front-left angle)
    # Lid / Bezel Outer
    bezel_corners = [(150, 120), (800, 180), (800, 600), (150, 680)]
    draw.polygon(bezel_corners, fill=(40, 42, 45, 255))
    draw.line(bezel_corners + [bezel_corners[0]], fill=(180, 185, 190, 255), width=3)

    # Keyboard Base
    base_corners = [(150, 680), (800, 600), (1050, 680), (250, 780)]
    clipped_base = [(x, min(y, H)) for x, y in base_corners] # Clip to bottom
    draw.polygon(clipped_base, fill=(200, 205, 210, 255))
    
    # Keyboard Well (Darker inner polygon)
    kbd_corners = [(220, 680), (760, 615), (950, 650), (320, 730)]
    clipped_kbd = [(x, min(y, H)) for x, y in kbd_corners]
    draw.polygon(clipped_kbd, fill=(100, 105, 110, 255))

    # Screen Display Area (Inner corners)
    screen_corners = [(170, 145), (780, 200), (780, 580), (170, 650)]
    draw.polygon(screen_corners, fill=(10, 10, 10, 255))

    # 4. Fetch or Generate Content Image (The "Smart Object" Replacement)
    content_img = None
    try:
        url = f"https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1000&q=80"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content_img = Image.open(io.BytesIO(response.read())).convert('RGBA')
    except Exception:
        # Fallback: Create a vibrant gradient screen if network fails
        content_img = Image.new('RGBA', (1000, 600), (0, 0, 0, 255))
        cdraw = ImageDraw.Draw(content_img)
        for i in range(600):
            r = int(accent_color[0] * (i/600))
            g = int(accent_color[1] * (i/600))
            b = int(accent_color[2] + (255 - accent_color[2]) * (1 - i/600))
            cdraw.line([(0, i), (1000, i)], fill=(r, g, min(b,255), 255))

    # 5. Calculate Perspective Homography (Solving A*c = B)
    cw, ch = content_img.size
    pa = screen_corners  # Destination polygon on canvas
    pb = [(0, 0), (cw, 0), (cw, ch), (0, ch)]  # Source original corners

    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = np.matrix(matrix, dtype=np.float64)
    B = np.array(pb).reshape(8)
    # Solve linear equations for the 8 perspective coefficients
    coeffs = np.linalg.solve(A, B).reshape(8).tolist()

    # 6. Apply Perspective Warp
    warped_img = content_img.transform((W, H), Image.PERSPECTIVE, coeffs, Image.BICUBIC)

    # 7. Mask and Composite
    mask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(mask).polygon(screen_corners, fill=255)
    # Antialiasing the mask edges slightly
    mask = mask.filter(ImageFilter.GaussianBlur(0.5))
    base_img.paste(warped_img, (0, 0), mask)

    # 8. Add Glass Reflection (Gloss)
    glare = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    glare_corners = [
        screen_corners[0], 
        (450, screen_corners[1][1] - 10), 
        (450, 615), 
        screen_corners[3]
    ]
    ImageDraw.Draw(glare).polygon(glare_corners, fill=(255, 255, 255, 12))
    base_img = Image.alpha_composite(base_img, glare)

    # Save Composite Image
    img_path = "mockup_composite.png"
    base_img.save(img_path)

    # 9. Build PPTX Slide
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Insert background mockup
    slide.shapes.add_picture(img_path, Inches(0), Inches(0), Inches(13.333), Inches(7.5))

    # Add Typography on the right
    tx_box = slide.shapes.add_textbox(Inches(8.5), Inches(2.2), Inches(4.2), Inches(3.0))
    tf = tx_box.text_frame
    tf.word_wrap = True

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(38)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(30, 35, 45)
    p_title.font.name = "Arial"

    p_body = tf.add_paragraph()
    p_body.text = "\n" + body_text
    p_body.font.size = Pt(16)
    p_body.font.color.rgb = RGBColor(90, 100, 110)
    p_body.font.name = "Arial"

    # Add a sleek accent line under title
    line = slide.shapes.add_shape(
        1, # msoShapeRectangle
        Inches(8.5), Inches(3.0), Inches(0.8), Inches(0.06)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(accent_color[0], accent_color[1], accent_color[2])
    line.line.fill.background()

    prs.save(output_pptx_path)
    
    # Cleanup temp image
    if os.path.exists(img_path):
        os.remove(img_path)
        
    return output_pptx_path
```