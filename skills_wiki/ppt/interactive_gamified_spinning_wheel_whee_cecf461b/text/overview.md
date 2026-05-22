# Interactive Gamified Spinning Wheel ("Wheel of Fortune")

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Interactive Gamified Spinning Wheel ("Wheel of Fortune")

* **Core Visual Mechanism**: A standard data pie chart is visually repurposed into a mechanical spinning wheel (roulette style). This is achieved by feeding the chart uniform quantitative data (so all slices are perfectly equal in size) and mapping category labels (names/items) to the pie slices. Layered over this chart are static UI elements—a center anchor button and a top directional pointer—that contextualize the chart as a physical wheel.
* **Why Use This Skill (Rationale)**: Gamification introduces an element of unpredictability and excitement. Transforming a static presentation into an interactive "game" captures audience attention, breaks monotony, and fosters active participation. 
* **Overall Applicability**: Perfect for Q&A sessions (picking a random speaker), raffles/giveaways, classroom icebreakers, or determining the order of speakers in team standup meetings.
* **Value Addition**: It elevates PowerPoint from a passive delivery medium to an interactive web-app-like tool.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **The Wheel (Pie Chart)**: A clean pie chart with no title, no legend, and no borders. 
  - **Color Logic**: Highly vibrant, distinguishable alternating colors to simulate a game show wheel. Representative RGBs: Red `(255, 89, 94)`, Yellow `(255, 202, 58)`, Green `(138, 201, 38)`, Blue `(25, 130, 196)`, Purple `(106, 76, 147)`.
  - **Text Hierarchy**: Data labels act as the primary text. They are bold, radially spaced, and placed at the outer edge of the slices. The center button text ("SPIN!") is the dominant call-to-action, styled in heavily bolded, large typography.

* **Step B: Compositional Style**
  - **Dead Center Alignment**: The wheel occupies ~80% of the slide height (`6.5` inches on a `7.5`-inch tall canvas) and is mathematically centered. 
  - **Layering**: The chart is the base layer (Z-index 0). The center button and top pointer overlap the chart (Z-index 1) to create depth and ground the "spinning" element.

* **Step C: Dynamic Effects & Transitions**
  - **The Core Animation**: A "Spin" emphasis animation is applied to the pie chart.
  - **The Trigger**: The animation is set to start *On Click* of the center "SPIN!" button, with a fast duration (e.g., 0.5s) set to repeat until the next click. 
  - *Note*: PowerPoint animation and trigger logic rely heavily on hidden `spid` (shape ID) linkages in the XML. For maximum robustness and editability, the code below constructs the complete visual apparatus, leaving the single final step of applying the Spin animation to the user.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Equal-slice Wheel** | `python-pptx` (ChartBuilder) | Using a native Pie Chart allows the end-user to easily right-click and "Edit Data" to change names in the future. The tutorial copies it as a static picture, but a native chart is functionally superior. |
| **Vibrant Slices** | `python-pptx` (Color injection) | We programmatically loop through `chart.series[0].points` to override default theme colors with a bright game-show palette. |
| **Pointer & Spin Button** | `python-pptx` (Shapes) | Native geometric shapes (Isosceles Triangle, Ovals) allow for crisp scaling and precise center-alignment mathematics. |

*Feasibility Assessment*: **90%**. The code perfectly recreates the visual layout, colorization, UI elements, and data integration. The final 10% (the actual interactive Spin animation and Click Trigger) must be applied natively in PowerPoint, as `python-pptx` does not expose an API for `<p:timing>` node interactive animation sequences.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Who's Next?",
    names: list = None,
    **kwargs,
) -> str:
    """
    Creates a PPTX file featuring a visual 'Spinning Wheel of Names' setup.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.chart import XL_CHART_TYPE
    from pptx.chart.data import CategoryChartData
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    
    if names is None:
        names = ["Liam", "Olivia", "Noah", "Emma", "Oliver", "Ava", 
                 "Elijah", "Sophia", "James", "Isabella", "William", "Mia"]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Constants for layout
    cx = prs.slide_width / 2
    cy = prs.slide_height / 2
    wheel_diameter = Inches(6.0)

    # === Layer 1: The Pie Chart (The Wheel) ===
    chart_data = CategoryChartData()
    chart_data.categories = names
    # Provide an equal value (1.0) for every slice so they are uniform
    chart_data.add_series('Names', [1.0] * len(names))

    x = cx - (wheel_diameter / 2)
    y = cy - (wheel_diameter / 2)
    
    graphic_frame = slide.shapes.add_chart(
        XL_CHART_TYPE.PIE, x, y, wheel_diameter, wheel_diameter, chart_data
    )
    chart = graphic_frame.chart

    # Clean up chart UI
    chart.has_legend = False
    chart.has_title = False

    # Format Data Labels
    plot = chart.plots[0]
    plot.has_data_labels = True
    data_labels = plot.data_labels
    data_labels.show_category_name = True
    data_labels.show_value = False
    data_labels.show_percentage = False
    data_labels.font.size = Pt(14)
    data_labels.font.bold = True
    data_labels.font.color.rgb = RGBColor(0, 0, 0)

    # Vibrant Game-Show Color Palette
    palette = [
        RGBColor(255, 89, 94),   # Bright Red
        RGBColor(255, 202, 58),  # Sun Yellow
        RGBColor(138, 201, 38),  # Lime Green
        RGBColor(25, 130, 196),  # Vivid Blue
        RGBColor(106, 76, 147),  # Royal Purple
        RGBColor(255, 146, 76),  # Orange
        RGBColor(50, 205, 50),   # Bright Green
        RGBColor(0, 191, 255),   # Deep Sky Blue
    ]

    # Apply colors to individual slices
    for i, point in enumerate(chart.series[0].points):
        fill = point.format.fill
        fill.solid()
        fill.fore_color.rgb = palette[i % len(palette)]

    # === Layer 2: UI Elements (Pointer and Button) ===

    # Center Spin Button (Circle)
    btn_diameter = Inches(1.2)
    btn_x = cx - (btn_diameter / 2)
    btn_y = cy - (btn_diameter / 2)
    
    btn = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, btn_x, btn_y, btn_diameter, btn_diameter
    )
    btn.fill.solid()
    btn.fill.fore_color.rgb = RGBColor(255, 255, 255)  # White fill
    btn.line.color.rgb = RGBColor(50, 50, 50)          # Dark border
    btn.line.width = Pt(3)
    
    btn_tf = btn.text_frame
    btn_tf.text = "SPIN!"
    btn_p = btn_tf.paragraphs[0]
    btn_p.alignment = PP_ALIGN.CENTER
    btn_p.font.bold = True
    btn_p.font.size = Pt(20)
    btn_p.font.color.rgb = RGBColor(0, 0, 0)
    btn_tf.vertical_anchor = MSO_ANCHOR.MIDDLE

    # Top Pointer (Triangle)
    tri_width = Inches(0.5)
    tri_height = Inches(0.7)
    tri_x = cx - (tri_width / 2)
    # Positioned slightly overlapping the top of the wheel
    tri_y = y - Inches(0.2) 
    
    pointer = slide.shapes.add_shape(
        MSO_SHAPE.ISOSCELES_TRIANGLE, tri_x, tri_y, tri_width, tri_height
    )
    pointer.rotation = 180  # Point downward
    pointer.fill.solid()
    pointer.fill.fore_color.rgb = RGBColor(220, 20, 60) # Crimson Red
    pointer.line.color.rgb = RGBColor(255, 255, 255)
    pointer.line.width = Pt(1.5)

    # Optional: Top Pointer Anchor (Small Circle over the triangle base)
    anchor_diam = Inches(0.3)
    anchor_x = cx - (anchor_diam / 2)
    anchor_y = tri_y - (anchor_diam / 2) + Inches(0.05)
    
    anchor = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, anchor_x, anchor_y, anchor_diam, anchor_diam
    )
    anchor.fill.solid()
    anchor.fill.fore_color.rgb = RGBColor(50, 50, 50)
    anchor.line.color.rgb = RGBColor(255, 255, 255)
    anchor.line.width = Pt(1)

    # Add a title at the top left
    tx_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(4), Inches(1))
    tf = tx_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.name = "Arial"
    
    p2 = tf.add_paragraph()
    p2.text = "Click the wheel in PPT and add 'Spin' Animation!"
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(120, 120, 120)

    prs.save(output_pptx_path)
    return output_pptx_path
```