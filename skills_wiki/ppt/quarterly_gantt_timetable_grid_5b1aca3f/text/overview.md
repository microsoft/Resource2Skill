# Quarterly Gantt Timetable Grid

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Quarterly Gantt Timetable Grid

* **Core Visual Mechanism**: A highly structured, calendar-based grid grouped by fiscal quarters (Q1–Q4). The background structure acts as a strict modular grid (built with distinct quarter containers and row dividers), while the project timelines themselves are represented by free-floating, absolutely positioned pill shapes (Gantt bars) that dynamically span across the background grid columns.
* **Why Use This Skill (Rationale)**: This design resolves the classic problem of displaying complex project timelines on a single slide. Grouping months into Quarter containers makes the year digestible at a glance, while using floating shapes for the tasks breaks the rigidness of standard Excel-like tables, giving the slide a modern, infographic feel.
* **Overall Applicability**: Perfect for annual project planning, product roadmaps, marketing campaign schedules, and executive summary timelines.
* **Value Addition**: Transforms a standard, boring table into a highly visual, easy-to-read dashboard. The visual separation of quarters creates natural reading pauses, and the colorful month labels provide strong wayfinding for the eye.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Quarter Containers**: Tall, vertical rounded rectangles acting as backdrops. Color: Dark Slate/Navy `(38, 43, 64)`.
  * **Month Headers**: Small, vibrantly colored rectangular tabs inside each quarter. Colors: Cyan `(0, 180, 216)`, Red `(217, 4, 41)`, Orange `(244, 162, 97)`, etc.
  * **Grid Lines**: Horizontal dividing lines corresponding to each project/task. Color: Light Gray `(200, 200, 200)`.
  * **Gantt Bars**: Rounded horizontal "pill" shapes indicating start and end dates. They float freely over the grid, ignoring cell boundaries.
* **Step B: Compositional Style**
  * **Y-Axis (Left)**: ~15% of slide width dedicated to Project Names.
  * **X-Axis (Right)**: ~85% dedicated to the timeline, split evenly into 4 columns (Quarters).
  * **Layering**: Layer 1 = Quarter backdrop; Layer 2 = Month headers and grid lines; Layer 3 = Gantt bars; Layer 4 = Explanatory text boxes positioned near Gantt bars.
* **Step C: Dynamic Effects & Transitions**
  * Typically static, but can use "Wipe" (From Left) animations on the Gantt bars to simulate time progressing when presenting.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Background structure & Quarters | `python-pptx` native | Standard rounded rectangles and text boxes perfectly recreate the containers. |
| Grid & Dividing lines | `python-pptx` native | Drawing explicit horizontal connector lines guarantees perfect rendering without battling PowerPoint's complex table border XML. |
| Gantt Bars & Floating Text | `python-pptx` native | Absolute positioning of `ROUNDED_RECTANGLE` shapes across calculated X/Y coordinates precisely reproduces the span effect. |

> **Feasibility Assessment**: 100% reproducible. The mathematical alignment of floating shapes over a drawn grid ensures a pixel-perfect, native PowerPoint layout that the user can click and edit later.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "PROJECT TIMETABLE",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Quarterly Gantt Timetable Grid effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.enum.shapes import MSO_SHAPE

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # === Colors ===
    bg_color = RGBColor(250, 250, 250)
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = bg_color

    dark_navy = RGBColor(40, 45, 68)
    line_gray = RGBColor(220, 220, 220)
    text_dark = RGBColor(50, 50, 50)
    text_gray = RGBColor(120, 120, 120)

    # Distinct vibrant colors for the 12 months
    month_colors = [
        RGBColor(72, 202, 228), RGBColor(144, 224, 239), RGBColor(0, 119, 182),    # Q1: Blues
        RGBColor(0, 150, 199), RGBColor(72, 190, 220), RGBColor(10, 100, 160),     # Q2: Deep Blues
        RGBColor(230, 57, 70), RGBColor(244, 162, 97), RGBColor(233, 196, 106),    # Q3: Warm
        RGBColor(155, 34, 38), RGBColor(202, 103, 2), RGBColor(187, 62, 3)         # Q4: Dark Warm
    ]
    months_labels = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    projects = ["PROJECT A", "PROJECT B", "PROJECT C", "PROJECT D", "PROJECT E", "PROJECT F"]

    # === Dimensions & Layout Math ===
    start_x = Inches(2.5)       # Left margin for grid
    start_y = Inches(1.8)       # Top margin for grid
    q_width = Inches(2.5)       # Width of one Quarter column
    gap_x = Inches(0.15)        # Gap between quarters
    month_width = q_width / 3.0 # Width of a single month column
    row_height = Inches(0.7)    # Height of a project row
    num_rows = len(projects)
    grid_height = num_rows * row_height
    q_box_height = grid_height + Inches(0.9) # Header area + grid height

    # 1. Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(12), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = dark_navy
    p.alignment = PP_ALIGN.CENTER

    # 2. Draw Project Y-Axis Labels
    for i, proj in enumerate(projects):
        y = start_y + Inches(0.9) + (i * row_height)
        tb = slide.shapes.add_textbox(Inches(0.5), y, Inches(1.8), row_height)
        tf = tb.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = proj
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = text_dark
        p.alignment = PP_ALIGN.LEFT

    # 3. Draw Quarter Backgrounds & Headers
    for q in range(4):
        qx = start_x + q * (q_width + gap_x)
        
        # Quarter Base Box (Dark Header part)
        q_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, qx, start_y, q_width, q_box_height)
        q_box.fill.solid()
        q_box.fill.fore_color.rgb = bg_color # Main area is slide color (transparent-like)
        q_box.line.color.rgb = line_gray
        q_box.line.width = Pt(1)
        # Hack to make a two-tone box: add a dark rectangle at the top
        header_bg = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, qx, start_y, q_width, Inches(0.9)
        )
        header_bg.fill.solid()
        header_bg.fill.fore_color.rgb = dark_navy
        header_bg.line.fill.background()
        
        # Q1/Q2/Q3/Q4 Text
        q_tb = slide.shapes.add_textbox(qx, start_y + Inches(0.1), q_width, Inches(0.4))
        p = q_tb.text_frame.paragraphs[0]
        p.text = f"Q{q+1}"
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER

        # Month Labels
        for m in range(3):
            mx = qx + (m * month_width)
            m_idx = (q * 3) + m
            
            # Month color tab
            m_tab = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, mx + Inches(0.05), start_y + Inches(0.55), month_width - Inches(0.1), Inches(0.25)
            )
            m_tab.fill.solid()
            m_tab.fill.fore_color.rgb = month_colors[m_idx]
            m_tab.line.fill.background()
            
            # Month Text
            mtb = slide.shapes.add_textbox(mx, start_y + Inches(0.5), month_width, Inches(0.3))
            mp = mtb.text_frame.paragraphs[0]
            mp.text = months_labels[m_idx]
            mp.font.size = Pt(10)
            mp.font.bold = True
            mp.font.color.rgb = RGBColor(255, 255, 255)
            mp.alignment = PP_ALIGN.CENTER
            
            # Draw vertical divider line for month (skip first month line inside box)
            if m > 0:
                vline = slide.shapes.add_connector(
                    1, mx, start_y + Inches(0.9), mx, start_y + q_box_height
                )
                vline.line.color.rgb = line_gray
                vline.line.width = Pt(0.75)

    # 4. Draw Row Grid Lines
    for r in range(1, num_rows):
        ry = start_y + Inches(0.9) + (r * row_height)
        # Line spans across all quarters
        line_start = start_x
        line_end = start_x + (4 * q_width) + (3 * gap_x)
        hline = slide.shapes.add_connector(1, line_start, ry, line_end, ry)
        hline.line.color.rgb = line_gray
        hline.line.width = Pt(1)

    # 5. Gantt Bars Data (Dynamic overlays)
    # Start and duration are in "months" (0.0 to 12.0)
    tasks = [
        {"row": 0, "start_m": 0.5, "dur_m": 2.0, "color": RGBColor(72, 202, 228), "desc": "Lorem ipsum dolor sit amet."},
        {"row": 1, "start_m": 2.0, "dur_m": 2.5, "color": RGBColor(0, 119, 182), "desc": "Research and development phase."},
        {"row": 2, "start_m": 4.5, "dur_m": 1.5, "color": RGBColor(244, 162, 97), "desc": "Prototyping & Alpha testing."},
        {"row": 3, "start_m": 5.5, "dur_m": 3.0, "color": RGBColor(230, 57, 70), "desc": "Marketing campaign planning."},
        {"row": 4, "start_m": 8.5, "dur_m": 2.0, "color": RGBColor(202, 103, 2), "desc": "Beta release and QA cycle."},
        {"row": 5, "start_m": 10.0, "dur_m": 1.5, "color": RGBColor(155, 34, 38), "desc": "Final launch execution."}
    ]

    def get_x_for_month_float(month_float: float) -> int:
        """Calculate exact X coordinate considering gaps between quarters."""
        q_idx = int(month_float // 3)
        if q_idx > 3: q_idx = 3 # cap
        m_remainder = month_float % 3
        # Absolute x is start + full quarters widths + gaps + remaining month portion
        return start_x + (q_idx * (q_width + gap_x)) + (m_remainder * month_width)

    # 6. Draw Gantt Bars
    for task in tasks:
        x0 = get_x_for_month_float(task["start_m"])
        x1 = get_x_for_month_float(task["start_m"] + task["dur_m"])
        w = x1 - x0
        
        # Center the bar vertically in the row
        bar_h = Inches(0.15)
        row_top = start_y + Inches(0.9) + (task["row"] * row_height)
        bar_y = row_top + (row_height / 2) - (bar_h / 2)
        
        # Add Pill Shape
        bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x0, bar_y, w, bar_h)
        bar.fill.solid()
        bar.fill.fore_color.rgb = task["color"]
        bar.line.fill.background()
        
        # Add Explanatory Text near the bar
        txt_w = Inches(2.5)
        txt_x = x0
        # alternate text position slightly above or below bar based on row to prevent overlaps
        txt_y = bar_y - Inches(0.25)
        
        dtb = slide.shapes.add_textbox(txt_x, txt_y, txt_w, Inches(0.3))
        dtf = dtb.text_frame
        dtf.word_wrap = False
        dp = dtf.paragraphs[0]
        dp.text = task["desc"]
        dp.font.size = Pt(8)
        dp.font.color.rgb = text_gray

    prs.save(output_pptx_path)
    return output_pptx_path
```