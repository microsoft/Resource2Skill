# Proportional Data-Driven Timeline

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Proportional Data-Driven Timeline 

* **Core Visual Mechanism**: A mathematically accurate horizontal timeline where events are spaced proportionally according to their dates, rather than evenly distributed. It uses a strong central axis (the "spine"), circular nodes, and branching orthogonal connector lines that lead to staggered text blocks above and below the timeline.

* **Why Use This Skill (Rationale)**: Typical manual timelines cluster events inaccurately, distorting the viewer's perception of time. Plotting points proportionally (originally achieved via a scatter chart hack in the tutorial, but better achieved via programmatic calculation) creates an intuitive, honest visual representation of history or project pacing. The alternating branching layout prevents text collision even when events occur in rapid succession.

* **Overall Applicability**: Ideal for corporate histories, product development roadmaps, regulatory compliance tracking, and scientific/historical sequence overviews where the *gaps* in time are just as meaningful as the events themselves.

* **Value Addition**: Transforms a dense bulleted list of dates into a scannable, visually striking spatial diagram. The use of a single accent color (orange) against monochrome anchors the eye and directs attention instantly to the nodes and their corresponding dates.


### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **The Spine (Axis)**: A thick, heavy line spanning the width of the slide, establishing a strong foundation.
  - **Color Logic**: Minimalist high-contrast. 
    - Background: White `(255, 255, 255, 255)`
    - Axis & Body Text: Black `(0, 0, 0, 255)`
    - Highlight/Accent (Nodes, Connectors, Years): Vibrant Orange `(237, 125, 49, 255)`
  - **Text Hierarchy**: 
    - *Primary (Anchor)*: The Year (Bold, Accent Color, 14pt)
    - *Secondary (Detail)*: Event Description (Regular, Black, 11pt)

* **Step B: Compositional Style**
  - **Spine Placement**: Positioned slightly below the vertical center (e.g., at 60% of slide height) to allow taller text boxes above, or centered directly.
  - **Alternating Stagger**: Text boxes are placed on alternating "tracks" (high top, low top, low bottom, high bottom) to maximize information density without clutter.
  - **Overlap Masking**: Connectors are drawn *behind* text boxes. Text boxes are given an opaque white background, cleanly cutting off the connector line so it appears seamlessly attached to the box's edge.

* **Step C: Dynamic Effects & Transitions**
  - Best animated via a simple "Wipe" (from Left) for the central axis, followed by a "Fade" or "Zoom" for the nodes and their corresponding text branches, unfolding chronologically. *(Achieved manually in PPTX).*


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Proportional Point Spacing** | Python Math + `python-pptx` | The tutorial cleverly uses a Scatter Chart to force proportional spacing. We can completely bypass the clunky chart XML formatting by simply calculating the X-coordinates mathematically in Python and drawing native shapes. This guarantees exact pixel control and perfect reproducibility. |
| **Branching Connectors** | `python-pptx` connectors | Straight connectors drawn programmatically map perfectly to calculated X-coordinates. |
| **Overlap Masking** | `python-pptx` Z-order & Fill | Drawing lines first, then placing text boxes with `solid()` white fills over them creates the exact "edge-connected" aesthetic shown in the video. |

> **Feasibility Assessment**: 100%. By replacing the manual PowerPoint scatter-chart hack with programmatic spatial mapping, we achieve the exact same aesthetic result but with significantly higher reusability and stability.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Historical Milestone Timeline",
    body_text: str = "",
    bg_palette: str = "white",
    accent_color: tuple = (237, 125, 49),  # Office Orange
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Proportional Data-Driven Timeline visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
    from pptx.dml.color import RGBColor

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Blank slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Default data representing the tutorial's events
    events = [
        {"year": 1974, "desc": "Discovery that CFCs could destroy ozone in the stratosphere (Molina and Rowland)"},
        {"year": 1978, "desc": "United States, Canada, Sweden and Norway ban CFCs in aerosols"},
        {"year": 1984, "desc": "Ozone hole in Antarctica discovered (Chubachi)"},
        {"year": 1985, "desc": "Vienna Convention for the Protection of the Ozone Layer"},
        {"year": 1987, "desc": "Montreal Protocol on Substances that Deplete the Ozone Layer"},
        {"year": 1989, "desc": "Montreal Protocol entered into force"},
        {"year": 1990, "desc": "The London Amendment - Phase out CFCs & Halons"},
        {"year": 1992, "desc": "The Copenhagen Amendment - Tighter controls for HCFCs"},
        {"year": 1997, "desc": "The Montreal Amendment - New licensing system"},
        {"year": 1999, "desc": "The Beijing Amendment - Tighter controls for HCFCs"},
        {"year": 2015, "desc": "The Montreal Protocol became the first universally ratified treaty"},
        {"year": 2016, "desc": "The Kigali Amendment - HFCs added"},
    ]

    # Theme Colors
    COLOR_ACCENT = RGBColor(*accent_color)
    COLOR_BLACK = RGBColor(0, 0, 0)
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_GRAY = RGBColor(100, 100, 100)

    # Slide Dimensions & Timeline Configuration
    margin_x = Inches(1.0)
    axis_y = Inches(4.0)
    timeline_width = prs.slide_width - (margin_x * 2)
    
    start_year = 1970
    end_year = 2020
    year_range = end_year - start_year

    def get_x_pos(year):
        """Map a year to a physical X coordinate on the slide."""
        percentage = (year - start_year) / year_range
        return margin_x + (percentage * timeline_width)

    # === Layer 1: Connectors (Drawn first so they sit behind nodes and text boxes) ===
    
    # Track configurations to prevent text box overlaps
    # [High Top, Low Bottom, Low Top, High Bottom]
    track_y_positions = [
        axis_y - Inches(2.2),  # Top High
        axis_y + Inches(0.5),  # Bottom Low
        axis_y - Inches(1.1),  # Top Low
        axis_y + Inches(1.6),  # Bottom High
    ]
    
    box_width = Inches(1.8)
    box_height = Inches(0.8)

    # Draw event connectors
    for i, event in enumerate(events):
        x = get_x_pos(event["year"])
        track_idx = i % 4
        ty = track_y_positions[track_idx]
        
        # Determine anchor point for the line depending on if it's above or below axis
        is_above = ty < axis_y
        line_target_y = ty + box_height if is_above else ty
        
        # Draw vertical connector line
        connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x, axis_y, x, line_target_y)
        connector.line.color.rgb = COLOR_ACCENT
        connector.line.width = Pt(1.5)

    # === Layer 2: The Timeline Axis ===
    
    # Main horizontal axis
    axis = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, margin_x, axis_y, margin_x + timeline_width, axis_y)
    axis.line.color.rgb = COLOR_BLACK
    axis.line.width = Pt(2.5)

    # Axis tick marks and labels (every 5 years)
    for yr in range(start_year, end_year + 1, 5):
        x = get_x_pos(yr)
        
        # Tick mark
        tick = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x, axis_y - Pt(4), x, axis_y + Pt(4))
        tick.line.color.rgb = COLOR_BLACK
        tick.line.width = Pt(1.5)
        
        # Tick Label
        lbl_box = slide.shapes.add_textbox(x - Inches(0.4), axis_y + Pt(5), Inches(0.8), Inches(0.4))
        lbl_tf = lbl_box.text_frame
        lbl_tf.word_wrap = False
        lbl_p = lbl_tf.paragraphs[0]
        lbl_p.text = str(yr)
        lbl_p.font.bold = True
        lbl_p.font.size = Pt(10)
        lbl_p.font.color.rgb = COLOR_GRAY
        lbl_p.alignment = 2  # Center align

    # === Layer 3: Nodes and Text Boxes ===

    for i, event in enumerate(events):
        x = get_x_pos(event["year"])
        track_idx = i % 4
        ty = track_y_positions[track_idx]
        
        # Draw Circular Marker (Node)
        node_size = Pt(12)
        node = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            x - (node_size / 2), 
            axis_y - (node_size / 2), 
            node_size, 
            node_size
        )
        node.fill.solid()
        node.fill.fore_color.rgb = COLOR_ACCENT
        node.line.fill.background() # No line

        # Draw Text Box
        # We add a solid white fill so it masks the connector line perfectly
        tx_box = slide.shapes.add_textbox(x - (box_width / 2), ty, box_width, box_height)
        tx_box.fill.solid()
        tx_box.fill.fore_color.rgb = COLOR_WHITE
        tx_box.line.color.rgb = COLOR_ACCENT
        tx_box.line.width = Pt(1)
        
        tf = tx_box.text_frame
        tf.word_wrap = True
        
        # Paragraph 1: Year
        p1 = tf.paragraphs[0]
        p1.text = str(event["year"])
        p1.font.bold = True
        p1.font.size = Pt(12)
        p1.font.color.rgb = COLOR_ACCENT
        
        # Paragraph 2: Description
        p2 = tf.add_paragraph()
        p2.text = event["desc"]
        p2.font.bold = False
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_BLACK

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(10), Inches(1))
    title_p = title_box.text_frame.paragraphs[0]
    title_p.text = title_text
    title_p.font.bold = True
    title_p.font.size = Pt(28)
    title_p.font.color.rgb = COLOR_BLACK

    prs.save(output_pptx_path)
    return output_pptx_path
```