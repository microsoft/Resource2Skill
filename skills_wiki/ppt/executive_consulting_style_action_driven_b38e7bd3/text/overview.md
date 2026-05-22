# Executive Consulting Style: Action-Driven Data Layout

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Executive Consulting Style: Action-Driven Data Layout

* **Core Visual Mechanism**: The defining characteristic of this style is the **"Action Title"** (or declarative title). Instead of topical titles (e.g., "Homelessness Statistics"), the slide uses a full, sentence-case statement summarizing the key takeaway (e.g., "Though the count dropped in 2019, homelessness continues to increase"). This is paired with minimalist, highly legible data visualizations that serve purely as supporting evidence for the title's claim. The typography often contrasts an authoritative Serif font for the title with a clean Sans-Serif for the body/data.
* **Why Use This Skill (Rationale)**: This structure enforces the "Slide Skeleton" logic (Horizontal and Vertical Flow). By reading only the titles across a deck, the audience gets the complete "Storyline" (Horizontal Flow). When looking at a single slide, the data visually proves the title's claim (Vertical Flow). It reduces cognitive load by telling the audience exactly what they should conclude before they even look at the data.
* **Overall Applicability**: Essential for corporate strategy, management consulting (McKinsey, BCG, Bain style), board-level reporting, and data-heavy analytical presentations where synthesizing insights is more important than just displaying raw data.
* **Value Addition**: Transforms a presentation from a "data dump" into a persuasive narrative. It forces the author to distill the "So What?" and creates a highly professional, trustworthy, and noise-free visual aesthetic.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Typography Hierarchy**:
    - **Action Title**: Dominant, top-aligned, sentence case. Often uses a classic Serif font (e.g., Georgia, Times New Roman, Garamond) to project authority. Size ~24-28pt.
    - **Body/Chart Text**: Clean Sans-Serif (e.g., Arial, Calibri, Helvetica). Size ~12-14pt for labels, ~10pt for footnotes.
  - **Color Logic**: Muted, professional palettes with high contrast.
    - Background: Pure White `(255, 255, 255)`
    - Primary Text: Dark Charcoal `(38, 38, 38)`
    - Accent/Brand Data Color: Deep Navy `(0, 45, 114)` or Muted Teal `(43, 114, 129)`
    - Context/Secondary Data Color: Light Grey `(217, 217, 217)`
  - **Structural Separators**: A very subtle, thin horizontal line separating the header block from the body block is common.

* **Step B: Compositional Style**
  - **Layout Ratios**:
    - Top 15-20%: Action Title (Left-aligned, ample breathing room above and below).
    - Middle 70%: Slide Body (Charts, tables, or structural graphics centered in this space).
    - Bottom 10%: Source citations, footnotes, and slide numbers (Left-aligned, tiny font).
  - **Data Visualization Principle**: Zero "chart-junk". No 3D effects, no unnecessary gridlines, no heavy borders, direct labeling on data points instead of separate legends when possible.

* **Step C: Dynamic Effects & Transitions**
  - **Zero Animation**: Top-tier consulting decks almost never use animations. The transition is instantaneous (Cut). The narrative momentum is carried by the storyline structure (the "Horizontal Flow"), not by moving shapes.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layout & Typography** | `python-pptx` native | Standard shape and text formatting is perfectly suited for exact typographic control (Serif vs Sans, specific Pt sizes, line spacing). |
| **Data Visualization** | `python-pptx` native charts | Consulting slides rely on editable, clean data charts. Using native PPTX charts ensures the output is professional, crisp, and natively editable. |
| **Chart Styling (De-junking)** | `python-pptx` native | We use the library's API to strip away gridlines, legends, and axis lines to achieve the minimalist consulting aesthetic. |

> **Feasibility Assessment**: 100%. The aesthetic of top-tier consulting firms relies entirely on strict adherence to native PowerPoint layout rules, typography, and clean chart formatting. This script fully reproduces that structural and visual logic.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Though the point-in-time count dropped slightly in 2019, the long-term trend of homelessness continues to increase steadily.",
    footer_text: str = "Source: Regional Point-in-Time Count Data; Comprehensive Homeless Management Information System.",
    **kwargs,
) -> str:
    """
    Creates a presentation slide mimicking a top-tier management consulting layout 
    (Action Title + Clean Evidence Chart).
    """
    import os
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.chart.data import CategoryChartData
    from pptx.enum.chart import XL_CHART_TYPE, XL_TICK_MARK, XL_DATA_LABEL_POSITION

    # 1. Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide_layout = prs.slide_layouts[6] 
    slide = prs.slides.add_slide(slide_layout)

    # Consulting Color Palette
    COLOR_TEXT_MAIN = RGBColor(38, 38, 38)     # Dark Charcoal
    COLOR_TEXT_MUTED = RGBColor(115, 115, 115) # Medium Grey
    COLOR_LINE = RGBColor(200, 200, 200)       # Light Grey
    COLOR_BAR_MAIN = RGBColor(0, 45, 114)      # Deep Navy
    COLOR_BAR_MUTED = RGBColor(217, 217, 217)  # Very Light Grey

    # === Layer 1: Action Title Block ===
    # Text box for the declarative statement
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(12.333), Inches(1.2))
    title_tf = title_box.text_frame
    title_tf.word_wrap = True
    title_tf.vertical_anchor = MSO_ANCHOR.TOP
    
    p = title_tf.paragraphs[0]
    p.text = title_text
    # Use a classic Serif font for authority (mimicking McKinsey/Bain style)
    p.font.name = 'Georgia' 
    p.font.size = Pt(26)
    p.font.color.rgb = COLOR_TEXT_MAIN
    p.font.bold = False
    p.line_spacing = 1.1

    # Subtle horizontal separator line
    line = slide.shapes.add_connector(
        1, Inches(0.5), Inches(1.7), Inches(12.833), Inches(1.7)
    )
    line.line.color.rgb = COLOR_LINE
    line.line.width = Pt(1)

    # === Layer 2: Slide Body (The Evidence) ===
    # Create clean chart data
    chart_data = CategoryChartData()
    chart_data.categories = ['2016', '2017', '2018', '2019', '2020 (Est.)']
    # Adding a dummy series showing a drop then an increase
    chart_data.add_series('Population', [10.2, 11.6, 12.1, 11.2, 13.5])

    # Add Column Chart
    x, y, cx, cy = Inches(1.5), Inches(2.2), Inches(10.333), Inches(4.5)
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
    ).chart

    # --- Apply Consulting "De-junking" Style to Chart ---
    chart.has_legend = False
    
    # Format the single series
    series = chart.series[0]
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = COLOR_BAR_MAIN
    
    # Add data labels directly to bars
    series.has_data_labels = True
    for dl in series.data_labels:
        dl.font.name = 'Arial'
        dl.font.size = Pt(14)
        dl.font.color.rgb = COLOR_TEXT_MAIN
        dl.position = XL_DATA_LABEL_POSITION.OUTSIDE_END
        dl.number_format = '0.0"k"' # Format as thousands

    # Clean up Value Axis (Y-axis)
    val_axis = chart.value_axis
    val_axis.visible = False # Hide Y axis completely for absolute cleanliness
    val_axis.has_major_gridlines = False
    val_axis.has_minor_gridlines = False

    # Clean up Category Axis (X-axis)
    cat_axis = chart.category_axis
    cat_axis.format.line.color.rgb = COLOR_LINE
    cat_axis.format.line.width = Pt(1)
    cat_axis.major_tick_mark = XL_TICK_MARK.NONE
    cat_axis.tick_labels.font.name = 'Arial'
    cat_axis.tick_labels.font.size = Pt(12)
    cat_axis.tick_labels.font.color.rgb = COLOR_TEXT_MUTED

    # Add a subtitle/lead-in for the chart (the "Dash" in Dot-Dash)
    chart_title_box = slide.shapes.add_textbox(Inches(1.5), Inches(1.9), Inches(5.0), Inches(0.4))
    ctf = chart_title_box.text_frame
    cp = ctf.paragraphs[0]
    cp.text = "Estimated homeless population by year (Thousands)"
    cp.font.name = 'Arial'
    cp.font.size = Pt(12)
    cp.font.color.rgb = COLOR_TEXT_MUTED
    cp.font.italic = True

    # === Layer 3: Footer ===
    # Source / Footnote box
    footer_box = slide.shapes.add_textbox(Inches(0.5), Inches(6.9), Inches(10.0), Inches(0.4))
    ftf = footer_box.text_frame
    fp = ftf.paragraphs[0]
    fp.text = footer_text
    fp.font.name = 'Arial'
    fp.font.size = Pt(9)
    fp.font.color.rgb = COLOR_TEXT_MUTED
    
    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path

```