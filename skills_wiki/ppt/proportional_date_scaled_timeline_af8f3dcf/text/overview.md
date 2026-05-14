# Proportional Date-Scaled Timeline

## Analysis

# Skill Extraction: Proportional Date-Scaled Timeline

### 1. High-level Design Pattern Extraction

> **Skill Name**: Proportional Date-Scaled Timeline

* **Core Visual Mechanism**: A central horizontal axis where events are spaced **proportionally based on their actual calendar dates**, rather than evenly distributed. Each data point features an anchored callout box (alternating above and below the line) connected by a delicate vertical line.
* **Why Use This Skill (Rationale)**: Standard native timelines (like PowerPoint SmartArt) distribute items with equal spacing regardless of the time elapsed between them. This creates a cognitive distortion, making a gap of 10 days look identical to a gap of 6 months. A proportional timeline accurately reflects clusters, bursts of activity, and long delays, providing an honest and immediate visual understanding of project velocity.
* **Overall Applicability**: Ideal for project post-mortems, roadmap planning, historical event summaries, and legal/investigative chronologies where the actual passage of time is a critical factor.
* **Value Addition**: Transforms a standard bulleted list of dates into a truthful, spatial representation of time. It eliminates the need to hack a scatter chart manually (as shown in the tutorial) by using programmatic date-math to calculate exact positional coordinates.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Main Axis**: A prominent, thick horizontal line serving as the timeline anchor.
  - **Markers**: Small, distinct geometric shapes (usually circles) placed directly on the axis to denote exact dates.
  - **Callout Labels**: Clean, rounded rectangular boxes containing the date (bold) and event description (regular), serving as the primary information carriers.
  - **Connectors**: Thin, often dashed or lighter-colored vertical lines linking the marker to its callout box.
  - **Color Logic**: 
    - Background: Crisp White `(255, 255, 255)` for contrast.
    - Axis Line: Subdued Gray `(200, 200, 200)`.
    - Accent (Markers & Borders): Professional Cyan/Teal `(68, 172, 214)` or similar corporate brand color.
    - Text: Dark Charcoal `(50, 50, 50)` for readability.

* **Step B: Compositional Style**
  - **Layout**: Spans ~85% of the slide width (leaving margins for breathing room). 
  - **Staggering**: To prevent text overlap (especially during periods of dense activity), labels strictly alternate between occupying the space above the axis and below the axis.
  - **Information Hierarchy**: The date is visually prioritized (larger, bolder) followed by the event description.

* **Step C: Dynamic Effects & Transitions**
  - Best revealed using a "Wipe" transition from Left to Right, mimicking the forward progression of time. (Achieved manually in PPT).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Proportional Date Spacing** | Python Date Math | The tutorial hacks an XY Scatter Chart to achieve spatial scaling. Programmatically calculating the `(event_date - min_date) / total_span` is much cleaner, more accurate, and entirely avoids chart-rendering complexities. |
| **Axis, Markers, and Connectors** | `python-pptx` native shapes | Basic geometric shapes (Oval, Rounded Rectangle, Connector) are perfect for this flat, modern corporate aesthetic. They remain fully editable by the end-user. |
| **Alternating Callout Layout** | Python logic (`i % 2`) | Simple modulo logic handles the above/below alternating placement seamlessly, preventing overlapping text boxes. |

> **Feasibility Assessment**: 100% reproducible. By translating the underlying logic of the tutorial's "Time Scale Perfect" technique into mathematical coordinate mapping, the generated slide perfectly mimics the visual outcome without the tedious manual labor of deleting chart axes and adjusting individual nodes.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Project Roadmap & Key Milestones",
    events: list = None,
    accent_color: tuple = (68, 172, 214),  # Cyan/Teal
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide featuring a proportionally spaced, date-scaled timeline.
    """
    import datetime
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN

    # Default data if none provided
    if not events:
        events = [
            {"date": "2023-06-01", "title": "Project Conception"},
            {"date": "2023-07-15", "title": "Core Team Assembled"},
            {"date": "2023-07-25", "title": "Scope & Budget Approved"},
            {"date": "2023-09-01", "title": "Execution Phase Begins"},
            {"date": "2024-03-15", "title": "Final Deployment"},
            {"date": "2024-04-10", "title": "Project Wrap-up & Retrospective"}
        ]

    # Parse and sort dates
    parsed_events = []
    for e in events:
        d = datetime.datetime.strptime(e["date"], "%Y-%m-%d")
        parsed_events.append({"dt": d, "title": e["title"]})
    
    parsed_events.sort(key=lambda x: x["dt"])

    # Initialize presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Apply background color
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(250, 251, 252) # Very light cool gray

    # Add Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(12.333), Inches(0.8))
    tf_title = title_box.text_frame
    p = tf_title.paragraphs[0]
    p.text = title_text.upper()
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(40, 45, 50)
    p.font.name = "Arial"

    # Timeline Layout Metrics
    start_x = Inches(1.5)
    end_x = Inches(11.8)
    axis_y = Inches(4.0)  # Center vertically
    
    # Draw Main Timeline Axis
    axis = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x - Inches(0.2), axis_y - Inches(0.04), (end_x - start_x) + Inches(0.4), Inches(0.08))
    axis.fill.solid()
    axis.fill.fore_color.rgb = RGBColor(200, 205, 210)
    axis.line.fill.background()

    # Time Scaling Math
    min_date = parsed_events[0]["dt"]
    max_date = parsed_events[-1]["dt"]
    total_days = (max_date - min_date).days
    if total_days == 0: 
        total_days = 1  # Prevent division by zero

    # Plot events
    for i, ev in enumerate(parsed_events):
        # Calculate proportional X position
        ratio = (ev["dt"] - min_date).days / total_days
        x_pos = start_x + (end_x - start_x) * ratio

        # 1. Draw Marker on Axis
        marker_size = Inches(0.2)
        marker = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            x_pos - marker_size/2, 
            axis_y - marker_size/2, 
            marker_size, 
            marker_size
        )
        marker.fill.solid()
        marker.fill.fore_color.rgb = RGBColor(*accent_color)
        marker.line.color.rgb = RGBColor(255, 255, 255)
        marker.line.width = Pt(1.5)

        # Alternating Layout Logic (Top / Bottom)
        is_top = (i % 2 == 0)
        box_width = Inches(2.0)
        box_height = Inches(0.85)
        box_x = x_pos - box_width / 2

        if is_top:
            box_y = axis_y - Inches(1.8)
            conn_start_y = box_y + box_height
            conn_end_y = axis_y - marker_size/2
        else:
            box_y = axis_y + Inches(0.95)
            conn_start_y = box_y
            conn_end_y = axis_y + marker_size/2

        # 2. Draw Connector Line
        conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x_pos, conn_start_y, x_pos, conn_end_y)
        conn.line.color.rgb = RGBColor(*accent_color)
        conn.line.width = Pt(1.5)
        # Try setting dash pattern if supported by current python-pptx version, otherwise standard solid line
        try:
            from pptx.enum.dml import MSO_LINE_DASH_STYLE
            conn.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        except ImportError:
            pass

        # 3. Draw Callout Box
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, box_x, box_y, box_width, box_height)
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(255, 255, 255)
        box.line.color.rgb = RGBColor(*accent_color)
        box.line.width = Pt(1.5)

        # Format Callout Text
        tf = box.text_frame
        tf.clear()
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.08)

        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        
        # Date Run
        run_date = p.add_run()
        run_date.text = ev["dt"].strftime("%b %d, %Y") + "\n"
        run_date.font.name = "Arial"
        run_date.font.size = Pt(11)
        run_date.font.bold = True
        run_date.font.color.rgb = RGBColor(*accent_color)

        # Title Run
        run_title = p.add_run()
        run_title.text = ev["title"]
        run_title.font.name = "Arial"
        run_title.font.size = Pt(10)
        run_title.font.bold = False
        run_title.font.color.rgb = RGBColor(70, 70, 70)

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
```