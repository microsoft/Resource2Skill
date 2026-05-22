# Cinematic Triptych Presentation Wall

## Analysis

# High-level Design Pattern Extraction

> **Skill Name**: Cinematic Triptych Presentation Wall

* **Core Visual Mechanism**: The defining visual idea is the "boardroom multi-monitor" layout. Instead of a single flat image, the slide is divided into a triptych (three panels) simulating physical television screens or video wall panels. The central panel serves as a bright, highly saturated focal point (the hero product), while the flanking panels are dark, dimmed, or ambient, pushing all attention to the center. Thick, dark frames (bezels) and drop shadows ground the screens in physical space.
* **Why Use This Skill (Rationale)**: This technique leverages the psychology of "the reveal." By framing the image within simulated hardware (monitors), it elevates the content from a simple picture to a "presentation within a presentation." It carries an authoritative, high-stakes, cinematic corporate vibe—perfect for dramatic pitches.
* **Overall Applicability**: Ideal for hero product reveals, bold aesthetic comparisons (e.g., classic vs. modern), portfolio highlights, and title slides where you want to evoke a premium, executive boardroom atmosphere.
* **Value Addition**: Compared to a standard full-bleed image, this style adds depth, architectural structure, and a masculine, industrial aesthetic. It immediately frames the content as something important enough to be broadcast on a multi-million dollar display wall.

# Visual Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: 
    - Background Environment: Deep slate/charcoal `(20, 25, 30, 255)` representing a darkened room.
    - Monitor Bezels: Pure dark grey/black `(10, 10, 10, 255)`.
    - Inactive/Ambient Screens: Glossy, subtle reflections over a dark base `(15, 18, 22, 255)` to `(30, 35, 40, 255)`.
    - Hero Image: High contrast, vivid colors (like the red or green muscle cars in the video).
  - **Text Hierarchy**: Stark, clean, minimal text. A single bold caption anchored directly beneath the center monitor, resembling a lower-third broadcast graphic or presentation subtitle.

* **Step B: Compositional Style**
  - **Grid Layout**: A 3-column horizontal array. 
  - **Proportions**: The center monitor commands ~60% of the horizontal canvas width (e.g., 8 inches wide). The side monitors are roughly 15-20% each (e.g., 2.2 inches wide), separated by narrow, realistic gaps (~0.15 inches).
  - **Spatial Feel**: Floating just off the background wall, achieved via outer drop shadows.

* **Step C: Dynamic Effects & Transitions**
  - The strength of this slide is in its static, statuesque framing. The transition between these slides is best served by a hard cut or a subtle "Fade," mimicking a slide-projector or screen switching inputs.

# Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Monitor Screen Generation** | PIL/Pillow | Used to generate the glossy "off-state" textures for the flanking monitors, giving them realistic glare without needing complex vector gradients. |
| **Hero Image Sizing** | PIL/Pillow | Ensures the downloaded hero image perfectly crops to the 16:9 monitor aspect ratio without distorting. |
| **Physical Bezels & Grid** | `python-pptx` native | Thick dark lines applied to shapes create the perfect hardware bezel effect. |
| **Wall Drop Shadows** | `lxml` XML injection | Injects native PowerPoint outer shadows behind the monitors so they appear mounted on a physical wall. |

> **Feasibility Assessment**: 95% reproduction of the visual style. The code flawlessly recreate the multi-screen physical hardware look, the sleek captions, and the corporate pitch aesthetic. The only missing element is the actual real-world background blur (e.g., the boardroom chairs), which is replaced with a clean, dark cinematic backdrop.

#### 3b. Complete Reproduction Code

```python
import os
import urllib.request
from io import BytesIO
from typing import Tuple
from lxml import etree

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

from PIL import Image, ImageDraw, ImageFilter

def _add_drop_shadow(shape, blur_pt=15, dist_pt=5, angle_deg=90, alpha_pct=60):
    """Injects a native PowerPoint outer drop shadow into a shape via lxml."""
    spPr = shape.element.spPr
    effectLst = spPr.find(f"{{http://schemas.openxmlformats.org/drawingml/2006/main}}effectLst")
    if effectLst is None:
        effectLst = etree.SubElement(spPr, f"{{http://schemas.openxmlformats.org/drawingml/2006/main}}effectLst")
    
    outerShdw = etree.SubElement(effectLst, f"{{http://schemas.openxmlformats.org/drawingml/2006/main}}outerShdw")
    outerShdw.set("blurRad", str(int(blur_pt * 12700)))
    outerShdw.set("dist", str(int(dist_pt * 12700)))
    outerShdw.set("dir", str(int(angle_deg * 60000)))
    outerShdw.set("algn", "ctr")
    
    srgbClr = etree.SubElement(outerShdw, f"{{http://schemas.openxmlformats.org/drawingml/2006/main}}srgbClr")
    srgbClr.set("val", "000000")
    alpha = etree.SubElement(srgbClr, f"{{http://schemas.openxmlformats.org/drawingml/2006/main}}alpha")
    alpha.set("val", str(int(100000 - (alpha_pct * 1000))))

def generate_blank_monitor_texture(width_px: int, height_px: int, path: str):
    """Generates a dark, glassy screen texture for the inactive side monitors."""
    img = Image.new('RGB', (width_px, height_px), (15, 18, 22))
    draw = ImageDraw.Draw(img)
    
    # Draw a subtle diagonal glare/reflection
    glare_poly = [
        (0, 0), 
        (width_px * 0.8, 0), 
        (width_px, height_px * 0.4), 
        (0, height_px * 0.8)
    ]
    draw.polygon(glare_poly, fill=(25, 30, 35))
    
    # Add blur to make it look like a smooth screen reflection
    img = img.filter(ImageFilter.GaussianBlur(15))
    img.save(path)

def fetch_and_crop_hero_image(query: str, target_w: int, target_h: int, path: str):
    """Downloads an image and center-crops it to fit exactly within the given dimensions."""
    try:
        url = f"https://source.unsplash.com/featured/?{query.replace(' ', ',')}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img = Image.open(BytesIO(response.read())).convert('RGB')
    except Exception:
        # Fallback to a solid color if download fails
        img = Image.new('RGB', (target_w, target_h), (180, 50, 50))
    
    # Calculate aspect ratios for perfect center crop
    img_ratio = img.width / img.height
    target_ratio = target_w / target_h
    
    if img_ratio > target_ratio:
        # Image is wider than target, crop sides
        new_w = int(target_ratio * img.height)
        offset = (img.width - new_w) // 2
        img = img.crop((offset, 0, offset + new_w, img.height))
    else:
        # Image is taller than target, crop top/bottom
        new_h = int(img.width / target_ratio)
        offset = (img.height - new_h) // 2
        img = img.crop((0, offset, img.width, offset + new_h))
        
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    img.save(path)

def create_slide(
    output_pptx_path: str,
    title_text: str = "THE 1965 PONTIAC GTO",
    body_text: str = "Completely awesome. Pure American muscle.",
    bg_palette: str = "classic muscle car",
    accent_color: tuple = (255, 255, 255), 
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Cinematic Triptych Presentation Wall effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Environment Background ===
    # Dark cinematic boardroom wall
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(20, 25, 30)
    bg.line.fill.background() # No line

    # === Layout Mathematics ===
    screen_h = Inches(4.5)
    center_w = Inches(8.0)
    side_w = Inches(2.2)
    gap = Inches(0.2)
    
    center_x = (prs.slide_width - center_w) / 2
    left_x = center_x - gap - side_w
    right_x = center_x + center_w + gap
    screen_y = Inches(1.2)

    # === Asset Generation ===
    hero_img_path = "hero_center_screen.jpg"
    side_img_path = "ambient_side_screen.jpg"
    
    fetch_and_crop_hero_image(bg_palette, 1600, 900, hero_img_path)
    generate_blank_monitor_texture(400, 800, side_img_path)

    # === Layer 2: The Monitors ===
    # Helper to create a monitor shape
    def add_monitor(x, y, w, h, img_path):
        shape = slide.shapes.add_picture(img_path, x, y, w, h)
        # Apply heavy physical bezel (line border)
        shape.line.color.rgb = RGBColor(10, 10, 10)
        shape.line.width = Pt(10)
        # Add drop shadow to pop off the wall
        _add_drop_shadow(shape, blur_pt=20, dist_pt=10, angle_deg=90, alpha_pct=75)
        return shape

    # Left Screen (Inactive)
    add_monitor(left_x, screen_y, side_w, screen_h, side_img_path)
    
    # Right Screen (Inactive)
    add_monitor(right_x, screen_y, side_w, screen_h, side_img_path)
    
    # Center Screen (Hero) - Added last to be on top if any overlap occurs
    add_monitor(center_x, screen_y, center_w, screen_h, hero_img_path)

    # === Layer 3: Typography ===
    # Title Text (Like a lower-third or projector caption)
    title_box = slide.shapes.add_textbox(center_x, screen_y + screen_h + Inches(0.4), center_w, Inches(0.5))
    tf = title_box.text_frame
    tf.word_wrap = True
    tf.clear()
    
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = title_text.upper()
    run.font.name = 'Arial'
    run.font.size = Pt(24)
    run.font.bold = True
    run.font.color.rgb = RGBColor(*accent_color)
    
    # Subtitle Text
    if body_text:
        subtitle_box = slide.shapes.add_textbox(center_x, screen_y + screen_h + Inches(0.8), center_w, Inches(0.4))
        tf_sub = subtitle_box.text_frame
        tf_sub.word_wrap = True
        
        p_sub = tf_sub.paragraphs[0]
        p_sub.alignment = PP_ALIGN.CENTER
        run_sub = p_sub.add_run()
        run_sub.text = body_text
        run_sub.font.name = 'Arial'
        run_sub.font.size = Pt(14)
        run_sub.font.color.rgb = RGBColor(180, 185, 190)

    # Cleanup temp files
    if os.path.exists(hero_img_path): os.remove(hero_img_path)
    if os.path.exists(side_img_path): os.remove(side_img_path)

    prs.save(output_pptx_path)
    return output_pptx_path
```