# Modern Dashboard Card Layout

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Modern Dashboard Card Layout

* **Core Visual Mechanism**: This design pattern transforms a standard, flat report into a modern software-like dashboard. It relies on placing content inside perfectly aligned, distinct "cards" (containers) with rounded corners and subtle drop shadows, all floating above an ambient, full-bleed gradient background. This creates a multi-layered, tactile hierarchy.
* **Why Use This Skill (Rationale)**: Cramming data onto a blank white slide creates visual fatigue. By explicitly defining "cards," you chunk information into digestible, discrete zones. The generous use of white space (gutters between cards) gives the data room to breathe, while rounded corners and shadows trigger the brain's familiarity with modern mobile and web UI (Neumorphism/Glassmorphism).
* **Overall Applicability**: Perfect for data-heavy presentations, KPI reports, executive summaries, and portfolio dashboards.
* **Value Addition**: Transforms a basic "data dump" into a premium, interactive-feeling executive dashboard, vastly increasing perceived professionalism and readability.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: An ambient, dark gradient (e.g., deep teal to dark navy `(13, 17, 28, 255)`) that sets a premium tone.
  - **Cards (Containers)**: Dark gray rectangles `(40, 44, 48, 255)` with no borders, creating low but distinct contrast against the background.
  - **Typography**: High contrast, crisp white `(255, 255, 255)` and soft gray `(180, 180, 180)` for secondary metrics.
  - **Accents**: Small pops of neon colors (cyan, lime green) for actual data elements to draw the eye.

* **Step B: Compositional Style**
  - **Alignment & Grid**: Strict column and row layouts. Example: 4 identical KPI cards across the top row, 2 or 3 larger chart cards across the bottom row.
  - **White Space (Gutters)**: Consistent padding of roughly 0.3 to 0.5 inches between every card and around the margins of the slide.
  - **Padding**: Internal padding within each card so text never touches the edges.

* **Step C: Dynamic Effects & Transitions**
  - **Rounded Corners**: ~10-15px border radius to soften the hard edges of data tables.
  - **Drop Shadows**: Soft, highly blurred, and slightly offset shadows to lift the cards off the background canvas, establishing depth (Z-axis separation).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Ambient Background** | PIL/Pillow | `python-pptx` cannot generate smooth, custom dual-color gradient backgrounds dynamically. PIL allows us to create a rich, pixel-perfect gradient. |
| **Card Drop Shadows** | lxml XML injection | `python-pptx` does not expose the shadow properties API. We must inject `<a:outerShdw>` elements directly into the shape properties (`spPr`). |
| **Rounded Corners & Layout** | `python-pptx` native | Using `MSO_SHAPE.ROUNDED_RECTANGLE` and grid math to enforce alignment and white space perfectly. |

> **Feasibility Assessment**: 95%. The code generates the exact layout, shadow effects, rounded corners, and background styling shown in the tutorial's final transformation. (Actual data charts inside the cards would require native charting implementation, which is abstracted into text placeholders here to focus on the container layout technique).

#### 3b. Complete Reproduction Code

```python
import os
import io
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml import parse_xml
from pptx.oxml.xmlchemy import OxmlElement
from PIL import Image, ImageDraw

def add_drop_shadow(shape, blur_rad_pt=15, dist_pt=5, dir_deg=90, alpha_pct=30):
    """
    Injects OpenXML to add a subtle drop shadow to a python-pptx shape.
    """
    spPr = shape.element.spPr
    
    # Calculate PPTX EMU/Angle values
    blurRad = int(blur_rad_pt * 12700)
    dist = int(dist_pt * 12700)
    dir_val = int(dir_deg * 60000)
    alpha_val = int(alpha_pct * 1000)

    effectLst = OxmlElement('a:effectLst')
    outerShdw = OxmlElement('a:outerShdw')
    outerShdw.set('blurRad', str(blurRad))
    outerShdw.set('dist', str(dist))
    outerShdw.set('dir', str(dir_val))
    outerShdw.set('algn', 'tl')
    outerShdw.set('rotWithShape', '0')

    srgbClr = OxmlElement('a:srgbClr')
    srgbClr.set('val', '000000')  # Black shadow
    
    alpha = OxmlElement('a:alpha')
    alpha.set('val', str(alpha_val))
    
    srgbClr.append(alpha)
    outerShdw.append(srgbClr)
    effectLst.append(outerShdw)
    spPr.append(effectLst)

def create_gradient_background(width_px=1920, height_px=1080):
    """
    Generates a dark, ambient modern gradient using PIL.
    """
    img = Image.new('RGB', (width_px, height_px))
    draw = ImageDraw.Draw(img)
    
    # Dark teal (top-left) to deep navy (bottom-right)
    color1 = (20, 150, 120)
    color2 = (15, 20, 30)
    
    for y in range(height_px):
        for x in range(width_px):
            # Diagonal gradient math
            factor = (x + y) / (width_px + height_px)
            r = int(color1[0] * (1 - factor) + color2[0] * factor)
            g = int(color1[1] * (1 - factor) + color2[1] * factor)
            b = int(color1[2] * (1 - factor) + color2[2] * factor)
            draw.point((x, y), fill=(r, g, b))
            
    return img

def create_slide(
    output_pptx_path: str,
    title_text: str = "Performance Tracking 2024",
    bg_palette: str = "dark_dashboard", 
    accent_color: tuple = (0, 255, 150),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Modern Dashboard Card Layout visual effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Background ===
    # Generate and insert PIL gradient
    bg_img = create_gradient_background(1920, 1080)
    bg_stream = io.BytesIO()
    bg_img.save(bg_stream, format='PNG')
    bg_stream.seek(0)
    slide.shapes.add_picture(bg_stream, 0, 0, prs.slide_width, prs.slide_height)

    # === Main Title ===
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(5), Inches(0.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # === Design Pattern Setup: Alignment, Gutters, White Space ===
    gutter = 0.3
    margin_x = 0.5
    margin_y = 1.0
    
    card_color = RGBColor(40, 44, 48)  # Modern dark gray container

    # --- Top Row: 4 KPI Cards ---
    kpi_count = 4
    kpi_height = 1.3
    kpi_width = (13.333 - (2 * margin_x) - ((kpi_count - 1) * gutter)) / kpi_count
    
    kpis = [
        {"title": "Total Sales", "value": "$95M"},
        {"title": "Total Insured", "value": "1,535"},
        {"title": "Total Uninsured", "value": "1,481"},
        {"title": "Average Age", "value": "46 Years"}
    ]

    for i in range(kpi_count):
        x = margin_x + i * (kpi_width + gutter)
        y = margin_y
        
        # Create Card
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, 
            Inches(x), Inches(y), Inches(kpi_width), Inches(kpi_height)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = card_color
        shape.line.fill.background() # Remove border
        shape.adjustments[0] = 0.1 # Rounded corners
        
        # Add LXML Drop Shadow
        add_drop_shadow(shape, blur_rad_pt=20, dist_pt=6, dir_deg=90, alpha_pct=35)
        
        # Add KPI Text
        tf = shape.text_frame
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.2)
        tf.vertical_anchor = MSO_ANCHOR.TOP
        
        p1 = tf.paragraphs[0]
        p1.text = kpis[i]["value"]
        p1.font.size = Pt(32)
        p1.font.bold = True
        p1.font.color.rgb = RGBColor(accent_color[0], accent_color[1], accent_color[2])
        
        p2 = tf.add_paragraph()
        p2.text = kpis[i]["title"]
        p2.font.size = Pt(14)
        p2.font.color.rgb = RGBColor(180, 180, 180)

    # --- Bottom Row: 2 Large Chart/Data Cards ---
    chart_count = 2
    chart_y = margin_y + kpi_height + gutter
    chart_height = 7.5 - chart_y - margin_x  # Fill remaining height minus bottom margin
    chart_width = (13.333 - (2 * margin_x) - ((chart_count - 1) * gutter)) / chart_count

    chart_titles = ["Sales by Car Type & Model", "Customer Demographics Matrix"]

    for i in range(chart_count):
        x = margin_x + i * (chart_width + gutter)
        
        # Create Card
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, 
            Inches(x), Inches(chart_y), Inches(chart_width), Inches(chart_height)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = card_color
        shape.line.fill.background()
        shape.adjustments[0] = 0.05  # Smaller adjustment for larger shape to keep corner radius consistent
        
        # Add LXML Drop Shadow
        add_drop_shadow(shape, blur_rad_pt=25, dist_pt=8, dir_deg=90, alpha_pct=40)

        # Add Chart Title
        tf = shape.text_frame
        tf.margin_left = Inches(0.3)
        tf.margin_top = Inches(0.3)
        tf.vertical_anchor = MSO_ANCHOR.TOP
        
        p1 = tf.paragraphs[0]
        p1.text = chart_titles[i]
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = RGBColor(255, 255, 255)
        
        p2 = tf.add_paragraph()
        p2.text = "\n[ Chart / Data Table Placeholder ]\n\n- White space strictly enforced\n- Shadow creates depth\n- Alignment is pixel-perfect"
        p2.font.size = Pt(14)
        p2.font.color.rgb = RGBColor(120, 120, 120)

    prs.save(output_pptx_path)
    return output_pptx_path

# To run and generate the slide:
# create_slide("dashboard_layout.pptx")
```