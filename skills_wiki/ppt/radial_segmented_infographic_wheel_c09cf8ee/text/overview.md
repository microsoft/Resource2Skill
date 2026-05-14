# Radial Segmented Infographic Wheel

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Radial Segmented Infographic Wheel

* **Core Visual Mechanism**: A thick, continuous wheel divided into equal fragments (segments) radiating from a central core. The structural foundation relies on a doughnut-chart aesthetic, where each wedge is color-coded and serves as an anchor for floating, spatially-aligned text boxes and icons. White stroke borders between the segments create a clean, "fragmented" puzzle-piece look.
* **Why Use This Skill (Rationale)**: Radial designs inherently draw the viewer’s eye to the center (the core concept) while giving equal visual weight to surrounding elements. This avoids the implicit hierarchy of a top-down list. The distinct colors and physical segmentation make complex, multi-part concepts easily digestible.
* **Overall Applicability**: Ideal for illustrating cyclic processes, component breakdowns (e.g., "7 Pillars of our Strategy"), product feature sets, or organizational values. It is highly effective for title slides or executive summary dashboards.
* **Value Addition**: Transforms a standard bulleted list into a structured, engaging visual anchor. It makes the slide feel like a custom-designed vector graphic rather than a standard PowerPoint template.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **The Wheel**: 7 equal segments forming a thick ring.
  - **Colors**: A vibrant, distinct 7-color palette (e.g., Coral Red `(234, 84, 85)`, Warm Orange `(240, 123, 63)`, Yellow `(246, 192, 101)`, Blue `(66, 133, 244)`, Navy `(45, 62, 80)`, Purple `(155, 89, 182)`, and Pink/Magenta `(200, 75, 100)`).
  - **The Core**: A white circular hub with a subtle border, containing the primary title.
  - **Text Hierarchy**: Large bold numbers/icons inside the colored wedges (White, to pop against the background); Title in the center (Dark Gray); Segment labels outside the wheel (Bold, matching segment color); Body text (Small, Light Gray).

* **Step B: Compositional Style**
  - **Spatial Alignment**: The wheel occupies the exact center of the slide (approx 45% of the slide height). Text elements orbit the wheel, dynamically aligning right or left depending on which hemisphere of the wheel they sit on, keeping the layout balanced and flush against the invisible circular boundary.

* **Step C: Dynamic Effects & Transitions**
  - Elements typically animate in sequentially in a clockwise pattern (e.g., "Wipe" or "Float In"), emphasizing the step-by-step nature of the infographic.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Perfect Circular Wedges | `python-pptx` (Doughnut Chart) | Calculating complex SVG/Freeform arcs natively is error-prone. A Doughnut chart with equal values natively renders perfect, editable vector arcs with zero math. |
| Thick Doughnut Ring | `lxml` XML Injection | The default `python-pptx` doughnut hole is 75% (too thin). Modifying the `c:holeSize` attribute via Open XML ensures the thick, bold aesthetic from the video. |
| Circular Layout Engine | Python Trigonometry | Text boxes and icons must orbit perfectly around the wheel. Standard `sin()` and `cos()` calculations convert polar coordinates into exact X/Y offsets. |

> **Feasibility Assessment**: 100% reproducible. By combining a "hacked" Doughnut chart (legend hidden, border formatted) with trigonometric positioning, we achieve a perfectly editable, natively rendered PowerPoint infographic that perfectly matches the video's aesthetic.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "7 OPTION\nINFOGRAPHIC",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Radial Segmented Infographic Wheel.
    """
    import math
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.chart import XL_CHART_TYPE
    from pptx.chart.data import ChartData
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from pptx.oxml import parse_xml

    prs = Presentation()
    # Ensure standard widescreen 16:9
    prs.slide_width = int(Inches(13.333))
    prs.slide_height = int(Inches(7.5))
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # The 7-color palette extracted from visual style
    colors = [
        RGBColor(234, 84, 85),   # Coral Red
        RGBColor(240, 123, 63),  # Warm Orange
        RGBColor(246, 192, 101), # Yellow
        RGBColor(66, 133, 244),  # Tech Blue
        RGBColor(45, 62, 80),    # Navy
        RGBColor(155, 89, 182),  # Purple
        RGBColor(200, 75, 100)   # Magenta
    ]

    # Overall Geometry setup
    cx = cy = Inches(5.5) # Chart bounding box size
    Xc, Yc = prs.slide_width / 2, prs.slide_height / 2

    # === Layer 1: The Infographic Wheel (via Doughnut Chart) ===
    chart_data = ChartData()
    chart_data.categories = [f"Item {i}" for i in range(7)]
    chart_data.add_series('Series', [1] * 7) # Equal values force equal slice angles

    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.DOUGHNUT, Xc - cx/2, Yc - cy/2, cx, cy, chart_data
    ).chart
    chart.has_legend = False

    # LXML Injection: Make the doughnut ring thicker by reducing the hole size to 50%
    plotArea = chart._element.chart.plotArea
    doughnutCharts = plotArea.xpath('./c:doughnutChart')
    if doughnutCharts:
        doughnutChart = doughnutCharts[0]
        holeSizes = doughnutChart.xpath('./c:holeSize')
        if holeSizes:
            holeSizes[0].set('val', '50')
        else:
            hs = parse_xml('<c:holeSize xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" val="50"/>')
            doughnutChart.append(hs)

    # Format the wheel slices (Colors and White Gaps)
    for i, point in enumerate(chart.series[0].points):
        point.format.fill.solid()
        point.format.fill.fore_color.rgb = colors[i]
        # Create the "Fragmented" puzzle look
        point.format.line.color.rgb = RGBColor(255, 255, 255)
        point.format.line.width = Pt(3)

    # === Layer 2: The Core / Hub ===
    r_center = Inches(1.2)
    # The gap between wheel (inner r = 1.375") and core (r = 1.2") creates breathing room
    circle = slide.shapes.add_shape(1, Xc - r_center, Yc - r_center, r_center*2, r_center*2)
    circle.fill.solid()
    circle.fill.fore_color.rgb = RGBColor(255, 255, 255)
    circle.line.color.rgb = RGBColor(230, 230, 230)
    circle.line.width = Pt(1)

    tf = circle.text_frame
    tf.text = title_text
    for p in tf.paragraphs:
        p.alignment = PP_ALIGN.CENTER
        p.font.bold = True
        p.font.size = Pt(16)
        p.font.color.rgb = RGBColor(40, 40, 40)

    # === Layer 3: Orbiting Text and Inner Segment Numbers ===
    # R_mid: Radius exactly in the middle of the thick colored wedge
    R_mid = (cx / 2) * 0.75 
    # R_text: Orbit radius for the outer text boxes
    R_text = (cx / 2) + Inches(0.4) 
    
    tw, th = Inches(2.2), Inches(1) # Text box dimensions
    icon_size = Inches(0.6)

    for i in range(7):
        # Calculate angle (Doughnut charts start slice 0 at 12 o'clock, moving clockwise)
        angle_deg = (i * (360 / 7)) + (360 / 14) # Offset by half a slice to reach the center point
        rad = math.radians(angle_deg)

        # 1. Inner Segment Identifier (Number/Icon inside the slice)
        ix = Xc + R_mid * math.sin(rad)
        iy = Yc - R_mid * math.cos(rad) # Y goes down in PPT coordinates
        
        num_box = slide.shapes.add_textbox(int(ix - icon_size/2), int(iy - icon_size/2), int(icon_size), int(icon_size))
        tf_num = num_box.text_frame
        tf_num.text = f"0{i+1}"
        p = tf_num.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

        # 2. Outer Text Labels
        tx = Xc + R_text * math.sin(rad)
        ty = Yc - R_text * math.cos(rad)
        
        # Dynamic alignment: Text on left side aligns right; text on right side aligns left
        if tx < Xc:
            left, align = tx - tw, PP_ALIGN.RIGHT
        else:
            left, align = tx, PP_ALIGN.LEFT

        top = ty - th / 2
        text_box = slide.shapes.add_textbox(int(left), int(top), int(tw), int(th))
        tf = text_box.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f"Option {i+1}"
        p1.font.bold = True
        p1.font.size = Pt(14)
        p1.font.color.rgb = colors[i]
        p1.alignment = align

        p2 = tf.add_paragraph()
        p2.text = "Add a brief description or key detail about this segment here."
        p2.font.size = Pt(10)
        p2.font.color.rgb = RGBColor(120, 120, 120)
        p2.alignment = align

    prs.save(output_pptx_path)
    return output_pptx_path
```