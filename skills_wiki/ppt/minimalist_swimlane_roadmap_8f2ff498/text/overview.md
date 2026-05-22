# Minimalist Swimlane Roadmap

## Analysis

# Agent_Skill_Distiller Report

### 1. High-level Design Pattern Extraction

> **Skill Name**: Minimalist Swimlane Roadmap

* **Core Visual Mechanism**: This technique transforms a cluttered, confusing timeline into a pristine, highly readable grid. The visual signature relies on **flat design, muted color palettes, absolute alignment, and "chart junk" elimination.** Harsh borders, 3D effects, and saturated primary colors are entirely stripped away. Instead, negative space (whitespace), extremely subtle background shading (light grey swimlanes), and thin, delicate gridlines guide the eye. 
* **Why Use This Skill (Rationale)**: Complex project plans overwhelm audiences when presented with overlapping shapes and heavy borders. By enforcing a rigid, mathematically perfectly spaced grid—where horizontal bands denote categories (swimlanes) and horizontal spans denote time—the cognitive load is drastically reduced. The brain easily tracks a task across time and department without fighting visual noise.
* **Overall Applicability**: Essential for Product Roadmaps, Strategic Timelines, Quarterly Go-To-Market Plans, and multi-departmental project tracking.
* **Value Addition**: Elevates a slide from a "messy internal working document" to an "executive-ready presentation." It demonstrates clarity of thought, professional polish, and structural organization.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Gridlines & Backgrounds**: Extremely subtle. Background swimlanes use an off-white/light grey (e.g., `RGBA(245, 245, 245, 255)`). Vertical dividers use a slightly darker grey (e.g., `RGBA(220, 220, 220, 255)`). No element has an outline/border.
  - **Color Logic**: Uses a cohesive, professional "muted" palette to denote categories. 
    - Slate Blue: `(86, 110, 145)`
    - Muted Crimson/Coral: `(198, 75, 90)`
    - Soft Teal: `(78, 155, 166)`
  - **Text Hierarchy**: 
    - Top Axis (Quarters): 14pt, slightly bolder, Slate color.
    - Sub-axis (Months): 10pt, grey, standard weight.
    - Category Labels (Marketing, Development): 12pt, bold, aligned top-left of the swimlane.
    - Task Blocks: 9pt, white, horizontally centered, word-wrapped.

* **Step B: Compositional Style**
  - The canvas is strictly divided. The left ~15% is reserved for category labels (row headers). The remaining 85% is the time axis.
  - The time axis is evenly subdivided. If showing 12 months, the 85% width is divided exactly by 12. Task block coordinates are mathematically derived from these "month units."
  - Vertical spacing ensures a small, clean gap between task blocks within the same swimlane.

* **Step C: Dynamic Effects & Transitions**
  - No dramatic animations are needed. A simple "Fade" or "Wipe from Left" for the task blocks can show sequential rollouts, but the static visual structure is the core focus.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Rigid structural grid & alignment | `python-pptx` native | A timeline is fundamentally vector geometry. By calculating exact X, Y, Width, and Height based on a 12-column grid system, `python-pptx` ensures mathematically perfect alignment that cannot be easily matched by eye. |
| Muted color palette & Flat shapes | `python-pptx` native | Standard PPTX shapes with borders disabled (`shape.line.fill.background()`) and explicit `RGBColor` assignments perfectly reproduce the flat, modern aesthetic. |

> **Feasibility Assessment**: **100%**. This entire technique relies on native presentation shapes styled correctly. Because we are enforcing a layout algorithm, the programmatic output is actually cleaner and more accurate than the manual dragging and dropping demonstrated in the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Simple Product Roadmap",
    **kwargs
) -> str:
    """
    Creates a PPTX file reproducing the Minimalist Swimlane Roadmap effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE

    # Initialize presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # --- Color Palette ---
    COLOR_BG_LANE = RGBColor(245, 245, 245)
    COLOR_GRIDLINE = RGBColor(215, 215, 215)
    COLOR_TEXT_MAIN = RGBColor(80, 80, 80)
    COLOR_SLATE_BLUE = RGBColor(86, 110, 145)
    COLOR_MUTED_RED = RGBColor(198, 75, 90)
    COLOR_SOFT_TEAL = RGBColor(78, 155, 166)

    # --- Grid Layout Parameters ---
    LEFT_MARGIN = Inches(0.5)
    LANE_LABEL_WIDTH = Inches(1.5)
    TIMELINE_START_X = LEFT_MARGIN + LANE_LABEL_WIDTH + Inches(0.2)
    TIMELINE_WIDTH = prs.slide_width - TIMELINE_START_X - Inches(0.5)
    
    MONTHS_TOTAL = 12
    MONTH_WIDTH = TIMELINE_WIDTH / MONTHS_TOTAL
    
    LANE_START_Y = Inches(2.0)
    LANE_HEIGHT = Inches(1.5)
    LANE_GAP = Inches(0.2)

    # --- 1. Add Title ---
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(10), Inches(0.8))
    tf = title_box.text_frame
    p = tf.add_paragraph()
    p.text = title_text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MAIN

    # --- 2. Draw Top Timeline Axis ---
    axis_y = Inches(1.2)
    quarters = ["Q1 2018", "Q2 2018", "Q3 2018", "Q4 2018"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    for i in range(MONTHS_TOTAL):
        x = TIMELINE_START_X + (i * MONTH_WIDTH)
        
        # Add Quarter labels
        if i % 3 == 0:
            q_idx = i // 3
            q_box = slide.shapes.add_textbox(x, axis_y, MONTH_WIDTH * 3, Inches(0.4))
            q_tf = q_box.text_frame
            q_p = q_tf.paragraphs[0]
            q_p.text = quarters[q_idx]
            q_p.font.size = Pt(14)
            q_p.font.bold = True
            q_p.font.color.rgb = COLOR_TEXT_MAIN
            
            # Vertical drop line for quarters
            line = slide.shapes.add_connector(
                MSO_SHAPE.LINE_INVERSE, 
                x, axis_y + Inches(0.4), 
                x, prs.slide_height - Inches(0.5)
            )
            line.line.color.rgb = COLOR_GRIDLINE
            line.line.width = Pt(1)

        # Add Month labels
        m_box = slide.shapes.add_textbox(x, axis_y + Inches(0.4), MONTH_WIDTH, Inches(0.3))
        m_tf = m_box.text_frame
        m_p = m_tf.paragraphs[0]
        m_p.text = months[i]
        m_p.font.size = Pt(10)
        m_p.font.color.rgb = COLOR_TEXT_MAIN
        m_tf.margin_left = m_tf.margin_right = 0

    # --- 3. Draw Swimlanes ---
    categories = ["Marketing", "Development", "KPI"]
    
    for idx, cat in enumerate(categories):
        current_y = LANE_START_Y + (idx * (LANE_HEIGHT + LANE_GAP))
        
        # Background grey box for the lane
        lane_bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 
            TIMELINE_START_X, current_y, 
            TIMELINE_WIDTH, LANE_HEIGHT
        )
        lane_bg.fill.solid()
        lane_bg.fill.fore_color.rgb = COLOR_BG_LANE
        lane_bg.line.fill.background() # No border
        
        # Category Label
        lbl_box = slide.shapes.add_textbox(LEFT_MARGIN, current_y, LANE_LABEL_WIDTH, Inches(0.5))
        lbl_tf = lbl_box.text_frame
        lbl_p = lbl_tf.paragraphs[0]
        lbl_p.text = cat
        lbl_p.font.size = Pt(12)
        lbl_p.font.bold = True
        lbl_p.font.color.rgb = COLOR_TEXT_MAIN

    # --- 4. Add Task Blocks (The Data Overlay) ---
    # Data structure: (lane_index, start_month_index, span_months, "Task Name", Color)
    # lane_index: 0=Marketing, 1=Development, 2=KPI
    tasks = [
        (0, 0, 1.5, "Press\nLaunch", COLOR_SOFT_TEAL, 0),
        (0, 1.5, 2.5, "Media\nCampaign", COLOR_SLATE_BLUE, 0),
        (0, 4, 3, "Celebrity\nPartnerships", COLOR_SLATE_BLUE, 0),
        (0, 7, 5, "Ongoing\nMarketing", COLOR_MUTED_RED, 0),
        
        (1, 0, 3, "Mobile\nWeb v1", COLOR_SLATE_BLUE, 0),
        (1, 3, 4, "Platform\nArchitecture", COLOR_SLATE_BLUE, 0),
        (1, 7, 5, "Ongoing\nReleases", COLOR_MUTED_RED, 0),
        
        (1, 1, 2, "Backend v1", COLOR_SOFT_TEAL, 1),
        (1, 4, 3, "Mobile Web v2", COLOR_SLATE_BLUE, 1),
        (1, 8, 4, "HTML5 Apps", COLOR_MUTED_RED, 1),

        (2, 0, 4, "Budget Setup", COLOR_SOFT_TEAL, 0),
        (2, 5, 7, "User Growth Target (1M)", COLOR_MUTED_RED, 0),
    ]

    TASK_HEIGHT = Inches(0.4)
    TASK_Y_SPACING = Inches(0.05)
    
    for lane_idx, start_m, span, text, color, sub_row in tasks:
        lane_base_y = LANE_START_Y + (lane_idx * (LANE_HEIGHT + LANE_GAP)) + Inches(0.1)
        
        task_x = TIMELINE_START_X + (start_m * MONTH_WIDTH)
        task_y = lane_base_y + (sub_row * (TASK_HEIGHT + TASK_Y_SPACING))
        task_w = (span * MONTH_WIDTH) - Inches(0.05) # slight gap between sequential tasks
        
        # Add flat colored block
        task_shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 
            task_x, task_y, task_w, TASK_HEIGHT
        )
        task_shape.fill.solid()
        task_shape.fill.fore_color.rgb = color
        task_shape.line.fill.background() # No border
        
        # Format text inside block
        tf = task_shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.05)
        tf.margin_right = Inches(0.05)
        tf.margin_top = Inches(0.05)
        tf.margin_bottom = Inches(0.05)
        
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255) # White text
        p.alignment = PP_ALIGN.LEFT

    # Save output
    prs.save(output_pptx_path)
    return output_pptx_path
```