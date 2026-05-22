# Glassmorphism (Frosted Glass Panel Reveal)

## Analysis

Here is the extracted strategy and complete reproduction code based on the Glassmorphism/Frosted Glass tutorial.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Glassmorphism (Frosted Glass Panel Reveal)

* **Core Visual Mechanism**: The effect simulates looking through a pane of frosted glass. The background directly behind a specific geometric shape (usually a rounded rectangle or circle) is heavily blurred. To complete the illusion, a translucent white tint and a delicate, semi-transparent white border are applied to the shape, giving it physical presence and simulating the edge of the glass. 
* **Why Use This Skill (Rationale)**: Glassmorphism solves a major design challenge: placing readable text over complex, vibrant, or chaotic backgrounds. By blurring the specific area behind the text, you establish readability (via reduced contrast/detail) while preserving the overall color scheme, aesthetic cohesion, and depth of the background.
* **Overall Applicability**: Modern tech product presentations, UI/UX portfolio mockups, credit card / fintech showcases, modern dashboard title cards, and minimalist "zen" quote slides.
* **Value Addition**: Transforms a flat, standard presentation into an interface that feels like a premium iOS/macOS or modern web experience. It establishes strong spatial hierarchy (foreground vs. background) without completely obscuring the slide's visual context.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Background Layer**: Must be highly colorful, high-contrast, or have distinct lighting (like a photo) for the blur effect to be noticeable.
  * **Glass Panel (Shape)**:
    * **Blur**: Heavy Gaussian Blur (Radius ~20-30px).
    * **Tint**: White or Black overlay at 10% - 25% opacity (`RGBA(255, 255, 255, 40)`).
    * **Border**: 1px to 2px solid line, semi-transparent (`RGBA(255, 255, 255, 128)`).
    * **Shadow**: A soft, wide drop shadow (Opacity ~20-30%, Blur ~15pt) to detach the glass from the background.
  * **Text Hierarchy**: Super crisp, usually pure white (`#FFFFFF`) or pure black (`#000000`) placed directly on the glass panel.
* **Step B: Compositional Style**
  * Floating cards: The glass panel usually occupies 40-60% of the screen, floating centrally or aligned to one side, acting as a "content container."
* **Step C: Dynamic Effects & Transitions**
  * **Morph Transition**: Moving, resizing, or rotating the glass cards between slides with the Morph transition creates a stunning effect where the background seems to dynamically "refract" through the moving glass.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Background Blur & Intersect** | `PIL (Pillow)` | While PPT has a "Slide Background Fill" hack, setting it via python-pptx is highly fragile and depends on Master Slides. PIL mathematically calculates the exact bounding box, crops the image, applies a true Gaussian blur, and generates a precise "glass pane" PNG. |
| **Translucency & Edge Lighting** | `PIL (Pillow)` | PIL allows us to add a 15% opacity white tint and a pixel-perfect semi-transparent rounded border directly onto the mask, ensuring the asset looks perfectly like glass. |
| **Drop Shadow** | `lxml` XML Injection | Injecting OOXML into the inserted picture gives a beautiful native PowerPoint drop shadow that interacts perfectly with the PNG's transparent rounded corners. |
| **Layout & Text** | `python-pptx` native | For crisp rendering of vector text on top of the glass image. |

> **Feasibility Assessment**: **100%**. By using PIL to literally process the image exactly as light would bend through frosted glass, and composing it natively in PPTX, we achieve an identical result to the tutorial.

#### 3b. Complete Reproduction Code

```python
import os
import urllib.request
from io import BytesIO
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw, ImageFilter

def add_native_drop_shadow(shape, blur_rad_pt=15, dist_pt=5, angle_deg=45, alpha_pct=30):
    """Injects native PowerPoint drop shadow XML to a picture shape."""
    spPr = shape.element.spPr
    effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
    
    # Convert points and degrees to EMUs and fractions
    blur_emu = int(blur_rad_pt * 12700)
    dist_emu = int(dist_pt * 12700)
    dir_emu = int(angle_deg * 60000)
    alpha_val = int(alpha_pct * 1000)
    
    outerShdw = etree.SubElement(
        effectLst, 
        '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw', 
        blurRad=str(blur_emu), dist=str(dist_emu), dir=str(dir_emu), algn="ctr", rotWithShape="0"
    )
    srgbClr = etree.SubElement(outerShdw, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr', val="000000")
    etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', val=str(alpha_val))

def create_slide(
    output_pptx_path: str,
    title_text: str = "VISA",
    body_text: str = "5412  7512  3412  3456\n\nDREAM LIU, CARDHOLDER                       VALID THRU 12/28",
    bg_theme: str = "abstract,gradient,dark",
    **kwargs,
) -> str:
    """
    Creates a slide demonstrating a Glassmorphism (Frosted Glass) effect.
    Simulates a transparent credit card or glass UI panel floating over a background.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Canvas dimensions in Pixels (Assuming 96 DPI for 1:1 mapping with PPT inches)
    W, H = 1280, 720
    
    # --- 1. Generate or Download Background ---
    bg_img = None
    try:
        url = f"https://source.unsplash.com/random/{W}x{H}/?{bg_theme}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            bg_img = Image.open(BytesIO(response.read())).convert('RGBA')
            bg_img = bg_img.resize((W, H))
    except Exception:
        # Fallback: Draw a programmatic vibrant gradient background
        bg_img = Image.new('RGBA', (W, H), (20, 20, 30, 255))
        draw = ImageDraw.Draw(bg_img)
        # Draw some colored orbs
        draw.ellipse((100, 100, 700, 700), fill=(255, 80, 0, 255))   # Orange
        draw.ellipse((600, -100, 1100, 400), fill=(138, 43, 226, 255)) # Purple
        draw.ellipse((800, 300, 1400, 900), fill=(0, 191, 255, 255))   # Cyan
        bg_img = bg_img.filter(ImageFilter.GaussianBlur(100)) # Blend them heavily

    bg_path = "temp_bg.png"
    bg_img.save(bg_path)
    
    # Insert background into PPTX
    slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)

    # --- 2. Process the Frosted Glass Panel via PIL ---
    # Define the "Glass Card" dimensions and position
    card_w, card_h = 600, 380
    cx, cy = W // 2, H // 2
    left_px = cx - card_w // 2
    top_px = cy - card_h // 2
    box = (left_px, top_px, left_px + card_w, top_px + card_h)
    
    # Step A: Crop the exact area behind the card and blur it heavily
    glass_crop = bg_img.crop(box)
    glass_crop = glass_crop.filter(ImageFilter.GaussianBlur(radius=25))
    
    # Step B: Add a white translucent tint (15% opacity) to simulate glass frosting
    tint = Image.new('RGBA', (card_w, card_h), (255, 255, 255, 35))
    glass_base = Image.alpha_composite(glass_crop, tint)
    
    # Step C: Create a rounded corner mask
    corner_radius = 24
    mask = Image.new('L', (card_w, card_h), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle((0, 0, card_w, card_h), corner_radius, fill=255)
    
    # Step D: Apply the mask to make the glass panel have rounded corners
    glass_panel = Image.new('RGBA', (card_w, card_h), (0, 0, 0, 0))
    glass_panel.paste(glass_base, (0, 0), mask)
    
    # Step E: Draw a semi-transparent white border (Edge lighting of the glass)
    draw_border = ImageDraw.Draw(glass_panel)
    draw_border.rounded_rectangle(
        (1, 1, card_w - 2, card_h - 2), 
        corner_radius, 
        outline=(255, 255, 255, 120), # ~47% opacity white
        width=2
    )
    
    glass_path = "temp_glass.png"
    glass_panel.save(glass_path)

    # --- 3. Insert Glass Panel into PPTX ---
    # Convert pixels back to inches based on 96 DPI
    pic_left = Inches(left_px / 96.0)
    pic_top = Inches(top_px / 96.0)
    pic_width = Inches(card_w / 96.0)
    pic_height = Inches(card_h / 96.0)
    
    glass_shape = slide.shapes.add_picture(glass_path, pic_left, pic_top, pic_width, pic_height)
    
    # Add native OOXML drop shadow to the glass
    add_native_drop_shadow(glass_shape, blur_rad_pt=20, dist_pt=8, angle_deg=90, alpha_pct=40)

    # --- 4. Add Crisp Foreground Text (Simulating a Credit Card) ---
    # Card Title / Brand
    title_box = slide.shapes.add_textbox(pic_left + Inches(0.4), pic_top + Inches(0.3), Inches(2), Inches(0.5))
    tf = title_box.text_frame
    p = tf.add_paragraph()
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(28)
    p.font.color.rgb = RGBColor(255, 255, 255)

    # Card Numbers & Info
    body_box = slide.shapes.add_textbox(pic_left + Inches(0.4), pic_top + Inches(2.2), pic_width - Inches(0.8), Inches(1.5))
    body_box.text_frame.word_wrap = True
    tf_body = body_box.text_frame
    
    # Card Number
    p_num = tf_body.add_paragraph()
    p_num.text = body_text.split('\n')[0]
    p_num.font.bold = True
    p_num.font.size = Pt(22)
    p_num.font.color.rgb = RGBColor(255, 255, 255)
    
    # Holder & Date
    p_info = tf_body.add_paragraph()
    p_info.text = "\n" + body_text.split('\n')[-1]
    p_info.font.size = Pt(10)
    p_info.font.color.rgb = RGBColor(220, 220, 220)

    # Cleanup temp files
    prs.save(output_pptx_path)
    if os.path.exists(bg_path): os.remove(bg_path)
    if os.path.exists(glass_path): os.remove(glass_path)
    
    return output_pptx_path

# Example execution:
# create_slide("frosted_glass_card.pptx", title_text="VISA", bg_theme="neon,gradient")
```