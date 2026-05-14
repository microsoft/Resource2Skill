# Dark Tech Blueprint (Cyber-Manual Aesthetic)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dark Tech Blueprint (Cyber-Manual Aesthetic)

* **Core Visual Mechanism**: This design style relies on a high-contrast, "dark mode" interface aesthetic inspired by digital dashboards and technical manuals. The signature look is achieved by combining a deep, moody background (charcoal/dark navy) with sharp, electric Cyan/Teal geometric elements. It utilizes UI-like structural components—thin bounding boxes, horizontal data ribbons, decorative slash separators (`/`), and micro-typography (like small "PART 01" labels) to create a highly organized, professional, and technological feel.

* **Why Use This Skill (Rationale)**: The dark background reduces eye strain while instantly conveying a premium, modern, and serious tone. The cyan accents draw immediate attention to structural hierarchy (titles, sections). The UI-style elements (brackets, lines, small badges) subconsciously signal to the viewer that the information is systematic, precise, and authoritative—perfect for a "Quality Control Manual" or a technical guide.

* **Overall Applicability**: Ideal for corporate guidelines, technical product launches, data analysis reports, software/IT presentations, and internal operating manuals where a modern, structured, and authoritative tone is required.

* **Value Addition**: Transforms a standard bullet-point document into a visual experience resembling a high-end digital product. It elevates perceived professionalism and makes dense technical or structural information feel digestible and cutting-edge.


### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**:
    - **Background Base**: Deep Charcoal/Night Blue `(26, 31, 36, 255)` to almost Black `(15, 18, 22, 255)`.
    - **Primary Accent (The "Glow")**: Electric Cyan / Teal `(44, 181, 195, 255)` or `(0, 191, 255, 255)`.
    - **Text Colors**: Pure White `(255, 255, 255, 255)` for primary focus, Light Gray `(150, 160, 170, 255)` for secondary text, and Dark Charcoal `(30, 35, 40, 255)` when overlaid on top of Cyan banners.
  - **Text Hierarchy**: Heavy, blocky Sans-Serif fonts for main titles. Secondary titles often use English translations with wide letter spacing (tracking) placed directly beneath the Chinese/primary titles. Micro-text is used for categories and labels.
  - **Decorations**: Slash marks (` / `) used as separators instead of commas. Thin rectangular borders to enclose labels. Large, faded watermark text in the background.

* **Step B: Compositional Style**
  - **Card/Ribbon Layout**: Content is often housed within distinct horizontal blocks or "ribbons" that stretch across the screen, mimicking website headers or software UI panels.
  - **Alignment**: Strong left-alignment for text within its designated block, but the main visual weight (like the title ribbons) is often perfectly center-aligned on the slide.
  - **Layering**: A distinct sense of depth: Dark background layer -> Soft cyan ambient glow layer -> Opaque structural blocks -> High contrast text.

* **Step C: Dynamic Effects & Transitions**
  - While static in this extraction, this style heavily implies sliding transitions (Pan or Push in PowerPoint) where the horizontal ribbons slide in from the left or right, mimicking digital loading states.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Ambient Tech Glow Background** | `PIL/Pillow` | PowerPoint native gradients can band and are hard to position radially off-center. PIL allows creating a high-quality dark canvas with a smooth, Gaussian-blurred cyan focal light, recreating the digital screen vibe. |
| **Tech Ribbons & Structural Boxes** | `python-pptx` native | Standard shape manipulation is perfect for the sharp, geometric rectangles, thin borders, and layout structuring required for this UI-like aesthetic. |
| **Neon/Shadow Depth** | `lxml` XML injection | To separate the cyan elements from the dark background, applying a native PowerPoint outer shadow/glow via OpenXML manipulation adds crucial depth that `python-pptx` doesn't natively support via standard API. |

> **Feasibility Assessment**: 85%. The code successfully recreates the core "Cyber-Manual" visual signature: the dark ambient background, the glowing cyan ribbon, the technical typography layout (including slash separators and UI badges), and the depth effects. Specific proprietary fonts used in the original video cannot be guaranteed, but standard sans-serif fallbacks maintain the structure perfectly.

#### 3b. Complete Reproduction Code

```python
import os
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from PIL import Image, ImageDraw, ImageFilter

def add_shadow_via_lxml(shape, color_hex="000000", blur_rad=100000, dist=50000, dir=2700000, alpha=50000):
    """
    Injects an Outer Shadow effect into a shape using lxml.
    Blur/Dist are in EMUs (1 pt = 12700 EMUs).
    Alpha is in thousandths of a percent (50000 = 50%).
    """
    spPr = shape.element.spPr
    effectLst = etree.SubElement(spPr, "{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst")
    outerShdw = etree.SubElement(effectLst, "{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw")
    outerShdw.set("blurRad", str(blur_rad))
    outerShdw.set("dist", str(dist))
    outerShdw.set("dir", str(dir))
    outerShdw.set("algn", "ctr")
    
    srgbClr = etree.SubElement(outerShdw, "{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr")
    srgbClr.set("val", color_hex)
    etree.SubElement(srgbClr, "{http://schemas.openxmlformats.org/drawingml/2006/main}alpha").set("val", str(alpha))

def create_slide(
    output_pptx_path: str,
    title_text: str = "准 备 规 范",
    subtitle_text: str = "P R E P A R I N G   S P E C I F I C A T I O N",
    tech_tags: list = ["防", "御", "打", "造", "完", "美", "幻", "灯", "片"],
    bg_color: tuple = (20, 24, 28),
    accent_color: tuple = (44, 181, 195), # Cyber Cyan
    **kwargs,
) -> str:
    """
    Creates a PPTX slide recreating the 'Dark Tech Blueprint' cyber-manual aesthetic.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Generate & Apply Ambient Glow Background via PIL ===
    bg_img_path = "temp_cyber_bg.png"
    img_w, img_h = 1920, 1080
    bg_img = Image.new('RGB', (img_w, img_h), bg_color)
    draw = ImageDraw.Draw(bg_img)
    
    # Draw a soft cyan glow in the center-bottom
    glow_radius = 600
    glow_color = accent_color
    draw.ellipse(
        [img_w/2 - glow_radius, img_h*0.7 - glow_radius, 
         img_w/2 + glow_radius, img_h*0.7 + glow_radius],
        fill=glow_color
    )
    # Apply heavy blur to create ambient light
    bg_img = bg_img.filter(ImageFilter.GaussianBlur(radius=250))
    # Darken it slightly by blending with base color
    dark_overlay = Image.new('RGB', (img_w, img_h), bg_color)
    bg_img = Image.blend(bg_img, dark_overlay, alpha=0.6)
    
    bg_img.save(bg_img_path)
    slide.shapes.add_picture(bg_img_path, 0, 0, prs.slide_width, prs.slide_height)

    # === Layer 2: Tech UI Elements & Structural Ribbons ===
    
    # Top-Left "Manual" UI Badge
    badge_l, badge_t, badge_w, badge_h = Inches(1), Inches(0.8), Inches(2.2), Inches(0.4)
    badge = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, badge_l, badge_t, badge_w, badge_h)
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(255, 255, 255)
    badge.line.color.rgb = RGBColor(*accent_color)
    badge.line.width = Pt(1.5)
    
    tf_badge = badge.text_frame
    tf_badge.text = "工作型PPT // 品控手册"
    tf_badge.paragraphs[0].font.size = Pt(12)
    tf_badge.paragraphs[0].font.bold = True
    tf_badge.paragraphs[0].font.color.rgb = RGBColor(*bg_color) # Dark text
    tf_badge.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Main Cyan Center Ribbon
    ribbon_w = Inches(10)
    ribbon_h = Inches(1.8)
    ribbon_l = (prs.slide_width - ribbon_w) / 2
    ribbon_t = Inches(2.8)
    
    ribbon = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, ribbon_l, ribbon_t, ribbon_w, ribbon_h)
    ribbon.fill.solid()
    ribbon.fill.fore_color.rgb = RGBColor(*accent_color)
    ribbon.line.fill.background() # No line
    # Add shadow via lxml to make it pop from the background
    add_shadow_via_lxml(ribbon, color_hex="000000", blur_rad=250000, dist=80000, alpha=60000)

    # Sub-ribbon (Dark frame underneath/around)
    frame_w = Inches(10.2)
    frame_h = Inches(2.4)
    frame_l = (prs.slide_width - frame_w) / 2
    frame_t = Inches(2.5)
    frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, frame_l, frame_t, frame_w, frame_h)
    frame.fill.background() # Transparent
    frame.line.color.rgb = RGBColor(*accent_color)
    frame.line.width = Pt(1)
    # Move frame to back, then ribbon to back, then bg to back to fix Z-order
    # But since we just added them linearly: bg -> badge -> ribbon -> frame. 
    # We want frame BEHIND ribbon. We can just re-insert or sort Z-order. 
    # Let's adjust order via code: frame is transparent so it can sit on top of ribbon slightly.

    # === Layer 3: Typography ===
    
    # Main Title on the Ribbon
    title_box = slide.shapes.add_textbox(ribbon_l, ribbon_t + Inches(0.2), ribbon_w, Inches(1))
    tf_title = title_box.text_frame
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(64)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(20, 24, 28) # Dark text on cyan
    p_title.alignment = PP_ALIGN.CENTER

    # Subtitle on the Ribbon
    sub_box = slide.shapes.add_textbox(ribbon_l, ribbon_t + Inches(1.2), ribbon_w, Inches(0.5))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = RGBColor(20, 24, 28)
    p_sub.alignment = PP_ALIGN.CENTER
    
    # Bottom Tech Tags (Slash Separated)
    tag_string = "  /  ".join(tech_tags)
    tag_box = slide.shapes.add_textbox(0, frame_t + frame_h + Inches(0.3), prs.slide_width, Inches(0.5))
    tf_tag = tag_box.text_frame
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = tag_string
    p_tag.font.size = Pt(12)
    p_tag.font.color.rgb = RGBColor(*accent_color)
    p_tag.alignment = PP_ALIGN.CENTER
    
    # Large Watermark Text (Bottom Right)
    wm_box = slide.shapes.add_textbox(Inches(8), Inches(5.5), Inches(4.5), Inches(1.5))
    tf_wm = wm_box.text_frame
    p_wm = tf_wm.paragraphs[0]
    p_wm.text = "FPT"
    p_wm.font.size = Pt(120)
    p_wm.font.bold = True
    # Semi-transparent pure cyan for watermark
    p_wm.font.color.rgb = RGBColor(*accent_color)
    # LXML trick: To make text transparent in python-pptx natively is hard, so we fake it with very dark cyan
    p_wm.font.color.rgb = RGBColor(20, 60, 65) 
    p_wm.alignment = PP_ALIGN.RIGHT

    # Cleanup temp file
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("cyber_manual.pptx")
```