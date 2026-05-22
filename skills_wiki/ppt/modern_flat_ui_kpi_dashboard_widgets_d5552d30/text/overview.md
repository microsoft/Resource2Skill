# Modern Flat-UI KPI Dashboard Widgets

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Modern Flat-UI KPI Dashboard Widgets

* **Core Visual Mechanism**: This design pattern translates the look of modern web-based data dashboards into presentation slides. It relies on minimalist "cards" (flat rectangular panels with subtle drop shadows) that act as containers for single data points. The defining element is the **Semi-circular Gauge Chart** with thick, clean arcs, combined with hyper-legible, oversized typography for the primary metrics. The background utilizes abstract, scattered geometric squares to provide a tech-forward, corporate aesthetic without cluttering the data.
* **Why Use This Skill (Rationale)**: Stakeholders and executives digest numbers best when they are isolated, hierarchically structured, and visually mapped to a goal. A gauge chart instantly communicates "progress vs. target" intuitively without requiring the viewer to parse axes or legends. Flat-UI cards create a mental "sandbox" for each metric, separating it from the rest of the slide.
* **Overall Applicability**: Perfect for performance reviews, quarterly business reviews (QBRs), project status updates, operational metrics (like the factory losses tracked in the video), and title/summary slides. 
* **Value Addition**: Transforms a boring bulleted list of numbers ("Losses: 104") into a piece of software-like UI that looks premium, objective, and authoritative. 

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background Pattern**: A warm off-white/cream base `(249, 249, 244, 255)` scattered with hard-edged, flat-colored squares mimicking pixel blocks or modular logic.
  - **Color Logic**:
    - Quickbase Teal (Accent/Positive): `(46, 139, 130, 255)`
    - Alert Red (Negative/Warning): `(229, 77, 77, 255)`
    - Mustard Yellow (Decorative): `(218, 165, 32, 255)`
    - Royal Purple (Decorative): `(102, 51, 153, 255)`
    - Card Background: Pure White `(255, 255, 255, 255)`
    - Typography: Dark slate `(51, 51, 51, 255)` for primary numbers, medium gray `(119, 119, 119, 255)` for labels.
  - **Text Hierarchy**: 
    1. Primary Metric: Massive, bold font (e.g., 60pt+), dead center.
    2. Widget Title: Medium, regular weight, positioned at the top of the card.
    3. Context/Delta: Small, sometimes colored (e.g., a small red "▼ 32").

* **Step B: Compositional Style**
  - **Modular Grid**: Cards are arranged in a strict grid layout, floating above the background canvas.
  - **Whitespace**: Immense internal padding within the cards. The gauge chart never touches the edges.
  - **Proportions**: The gauge path thickness is roughly 12-15% of the total radius, ensuring it looks "chunky" and modern rather than thin and fragile.

* **Step C: Dynamic Effects & Transitions**
  - While not animated in a static export, these widgets are designed to look like they could "fill up" dynamically. The design relies entirely on static visual clarity (color coding and high contrast) rather than motion.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Semi-circular Gauge Chart** | `PIL/Pillow` | Native PowerPoint arcs and donut charts are difficult to perfectly crop into a clean semicircle without axes/borders interfering. PIL provides exact, anti-aliased pixel control for a beautiful UI-style thick gauge track. |
| **Card Drop Shadows** | `lxml` XML injection | Native `python-pptx` cannot add drop shadows to shapes. Injecting `<a:outerShdw>` into the shape properties creates the authentic flat-UI floating card effect. |
| **Widget Layout & Typography** | `python-pptx` native | Perfect for precise coordinate placement of text boxes over the PIL-generated gauge images, ensuring text remains editable. |

> **Feasibility Assessment**: 95% reproduction. The code perfectly recreates the sleek web-dashboard aesthetic, the scattered geometric background, the precise arc of the gauge chart, and the floating UI cards. The only missing element is interactive tooltips, which are impossible in a static PPTX.

#### 3b. Complete Reproduction Code

```python
import os
import io
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.oxml.xmlchemy import OxmlElement
from PIL import Image, ImageDraw

def add_drop_shadow(shape, blur_rad=100000, dist=30000, angle=5400000, alpha=15000):
    """
    Injects an OpenXML drop shadow into a python-pptx shape.
    Used to create the modern "floating card" UI effect.
    """
    spPr = shape.element.spPr
    effectLst = OxmlElement('a:effectLst')
    outerShdw = OxmlElement('a:outerShdw')
    
    outerShdw.set('blurRad', str(blur_rad))  # 10pt
    outerShdw.set('dist', str(dist))         # 3pt
    outerShdw.set('dir', str(angle))         # 90 degrees (bottom)
    outerShdw.set('algn', 'b')
    
    srgbClr = OxmlElement('a:srgbClr')
    srgbClr.set('val', '000000') # Black shadow
    
    alpha_xml = OxmlElement('a:alpha')
    alpha_xml.set('val', str(alpha)) # Default 15% opacity
    
    srgbClr.append(alpha_xml)
    outerShdw.append(srgbClr)
    effectLst.append(outerShdw)
    spPr.append(effectLst)

def create_pil_gauge(value, max_value, active_color_rgb):
    """
    Generates a high-quality, anti-aliased semi-circular gauge chart using PIL.
    Returns a BytesIO stream of the image.
    """
    # Create a large image and downsample for high-quality anti-aliasing
    scale = 4
    width = 400 * scale
    height = 220 * scale
    thickness = 40 * scale
    
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Bounding box for the full circle
    bbox = [
        thickness, 
        thickness, 
        width - thickness, 
        (height - thickness) * 2
    ]
    
    # Draw background track (light gray)
    draw.arc(bbox, start=180, end=360, fill=(235, 235, 235, 255), width=thickness)
    
    # Calculate progress angle
    percentage = min(value / max_value, 1.0)
    progress_end = 180 + int(percentage * 180)
    
    # Draw active progress track
    draw.arc(bbox, start=180, end=progress_end, fill=active_color_rgb + (255,), width=thickness)
    
    # Resize back down
    img = img.resize((width // scale, height // scale), Image.Resampling.LANCZOS)
    
    img_stream = io.BytesIO()
    img.save(img_stream, format='PNG')
    img_stream.seek(0)
    return img_stream

def create_slide(
    output_pptx_path: str,
    title_text: str = "Quality Control Management",
    gauge_value: int = 104,
    gauge_max: int = 500,
    gauge_label: str = "Number of Kaizens Created",
    kpi_value: str = "1.5K",
    kpi_label: str = "Total Losses",
    **kwargs,
) -> str:
    """
    Creates a presentation slide mimicking a modern flat-UI data dashboard.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide_layout = prs.slide_layouts[6] 
    slide = prs.slides.add_slide(slide_layout)
    
    # Color Palette
    bg_color = RGBColor(249, 249, 244)
    teal = RGBColor(46, 139, 130)
    red = RGBColor(229, 77, 77)
    yellow = RGBColor(218, 165, 32)
    purple = RGBColor(102, 51, 153)
    text_dark = RGBColor(51, 51, 51)
    text_gray = RGBColor(119, 119, 119)

    # === Layer 1: Background & Decorative Blocks ===
    bg = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height) # msoShapeRectangle
    bg.fill.solid()
    bg.fill.fore_color.rgb = bg_color
    bg.line.fill.background()
    
    # Decorative scatter blocks (mimicking Quickbase intro style)
    blocks = [
        (Inches(0.5), Inches(0.5), Inches(0.8), teal),
        (Inches(6.5), Inches(0.0), Inches(0.6), yellow),
        (Inches(6.0), Inches(0.6), Inches(0.6), yellow),
        (Inches(9.0), Inches(1.5), Inches(0.7), teal),
        (Inches(10.5), Inches(5.0), Inches(0.8), purple),
        (Inches(11.3), Inches(5.8), Inches(1.2), purple),
        (Inches(-0.2), Inches(6.0), Inches(1.5), red),
        (Inches(12.5), Inches(2.5), Inches(1.5), teal),
    ]
    
    for x, y, size, color in blocks:
        sq = slide.shapes.add_shape(1, x, y, size, size)
        sq.fill.solid()
        sq.fill.fore_color.rgb = color
        sq.line.fill.background()

    # Title Text
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(5), Inches(1))
    tf = title_box.text_frame
    p = tf.add_paragraph()
    p.text = "Building KPI\nwidgets"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = text_dark
    p.font.name = "Georgia"

    # === Layer 2: KPI Widget 1 (Gauge Chart Card) ===
    card1_left = Inches(5.5)
    card1_top = Inches(2.5)
    card1_width = Inches(4.5)
    card1_height = Inches(4.0)
    
    # Card Base
    card1 = slide.shapes.add_shape(1, card1_left, card1_top, card1_width, card1_height)
    card1.fill.solid()
    card1.fill.fore_color.rgb = RGBColor(255, 255, 255)
    card1.line.fill.background()
    add_drop_shadow(card1, blur_rad=150000, alpha=8000) # Soft shadow
    
    # Card Title
    c1_title = slide.shapes.add_textbox(card1_left, card1_top + Inches(0.2), card1_width, Inches(0.5))
    c1_tf = c1_title.text_frame
    c1_p = c1_tf.add_paragraph()
    c1_p.text = gauge_label
    c1_p.alignment = PP_ALIGN.CENTER
    c1_p.font.size = Pt(14)
    c1_p.font.color.rgb = text_gray
    c1_p.font.name = "Arial"
    
    # Generate and Insert PIL Gauge Image
    # Determine color based on threshold
    gauge_color = (229, 77, 77) if gauge_value < (gauge_max * 0.3) else (46, 139, 130)
    gauge_img_stream = create_pil_gauge(gauge_value, gauge_max, gauge_color)
    
    gauge_img_width = Inches(3.5)
    gauge_img_height = Inches(1.925)
    slide.shapes.add_picture(
        gauge_img_stream, 
        card1_left + Inches(0.5), 
        card1_top + Inches(1.2), 
        width=gauge_img_width, 
        height=gauge_img_height
    )
    
    # Gauge Center Value
    c1_val = slide.shapes.add_textbox(card1_left, card1_top + Inches(1.8), card1_width, Inches(1))
    c1_val_tf = c1_val.text_frame
    c1_val_p = c1_val_tf.add_paragraph()
    c1_val_p.text = str(gauge_value)
    c1_val_p.alignment = PP_ALIGN.CENTER
    c1_val_p.font.size = Pt(64)
    c1_val_p.font.bold = True
    c1_val_p.font.color.rgb = text_dark
    c1_val_p.font.name = "Arial"

    # Gauge Min/Max Labels
    c1_min = slide.shapes.add_textbox(card1_left + Inches(0.3), card1_top + Inches(3.1), Inches(1), Inches(0.5))
    c1_min.text_frame.text = "0"
    c1_min.text_frame.paragraphs[0].font.size = Pt(12)
    c1_min.text_frame.paragraphs[0].font.color.rgb = text_gray
    
    c1_max = slide.shapes.add_textbox(card1_left + Inches(3.2), card1_top + Inches(3.1), Inches(1), Inches(0.5))
    c1_max.text_frame.text = str(gauge_max)
    c1_max.text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT
    c1_max.text_frame.paragraphs[0].font.size = Pt(12)
    c1_max.text_frame.paragraphs[0].font.color.rgb = text_gray

    # === Layer 3: KPI Widget 2 (Solid Stat Card) ===
    card2_left = Inches(10.5)
    card2_top = Inches(2.5)
    card2_width = Inches(2.3)
    card2_height = Inches(2.5)
    
    # Card Base
    card2 = slide.shapes.add_shape(1, card2_left, card2_top, card2_width, card2_height)
    card2.fill.solid()
    card2.fill.fore_color.rgb = teal
    card2.line.fill.background()
    add_drop_shadow(card2, blur_rad=120000, alpha=15000)
    
    # Card 2 Title
    c2_title = slide.shapes.add_textbox(card2_left, card2_top + Inches(0.1), card2_width, Inches(0.5))
    c2_p = c2_title.text_frame.add_paragraph()
    c2_p.text = kpi_label
    c2_p.alignment = PP_ALIGN.CENTER
    c2_p.font.size = Pt(12)
    c2_p.font.color.rgb = RGBColor(255, 255, 255)
    c2_p.font.name = "Arial"
    
    # Card 2 Value
    c2_val = slide.shapes.add_textbox(card2_left, card2_top + Inches(0.7), card2_width, Inches(1))
    c2_val_p = c2_val.text_frame.add_paragraph()
    c2_val_p.text = str(kpi_value)
    c2_val_p.alignment = PP_ALIGN.CENTER
    c2_val_p.font.size = Pt(56)
    c2_val_p.font.bold = True
    c2_val_p.font.color.rgb = RGBColor(255, 255, 255)
    c2_val_p.font.name = "Arial"
    
    # Card 2 Delta indicator
    c2_delta = slide.shapes.add_textbox(card2_left, card2_top + Inches(1.9), card2_width, Inches(0.5))
    c2_delta_p = c2_delta.text_frame.add_paragraph()
    c2_delta_p.text = "▼ 32"
    c2_delta_p.alignment = PP_ALIGN.CENTER
    c2_delta_p.font.size = Pt(12)
    c2_delta_p.font.color.rgb = red
    c2_delta_p.font.name = "Arial"

    prs.save(output_pptx_path)
    return output_pptx_path
```