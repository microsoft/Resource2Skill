# Dark Mode Arc Diagram (Node-Link Sequence)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dark Mode Arc Diagram (Node-Link Sequence)

* **Core Visual Mechanism**: The core visual identity of this skill is the **horizontal axis paired with overlapping semicircular paths (arcs)** above and below the baseline. By bending the connecting lines into smooth curves with varying heights, complex intersecting relationships between sequential points can be mapped out cleanly without the visual clutter of intersecting straight lines. 

* **Why Use This Skill (Rationale)**: This layout excels at showing non-linear jumps in a linear sequence. Instead of a standard flowchart that implies strict Step 1 → Step 2 logic, the arc diagram visually explains how early stages directly impact much later stages (e.g., Data 1 directly linking to Data 3 or 5). The dark mode aesthetic paired with thin, translucent-looking arc lines makes the diagram feel highly technical, modern, and data-driven.

* **Overall Applicability**: 
  - **System Architecture**: Showing data telemetry, API calls, or server-to-server communications.
  - **Process Maps**: Illustrating supply chains or multi-stage workflows where items bypass certain steps.
  - **User Journeys**: Visualizing conversion funnels where users jump back and forth between touchpoints.

* **Value Addition**: Transforms a standard left-to-right process slide into a sophisticated network visualization. The arcs naturally guide the eye up and down, making the slide feel dynamic even when static.


### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: Solid black `(0, 0, 0)` to allow the thin lines to "glow".
  - **Nodes**: Small white circular checkpoints along the horizontal axis. 
  - **Axis**: A subtle, straight horizontal baseline connecting the nodes.
  - **Arcs (Edges)**: Thin, elegant gray paths `(150, 150, 150)` curving between nodes. 
  - **Text Hierarchy**: 
    - Title: Bold, upper-case, centered, prominent white `(255, 255, 255)`.
    - Node Labels: Small, clean, positioned directly below the nodes.
    - Weights/Percentages: Placed precisely at the peak (apex) of each arc to indicate volume or importance.

* **Step B: Compositional Style**
  - The diagram is strictly constrained to the horizontal center of the slide.
  - **Proportions**: The axis sits slightly below the vertical center (e.g., ~60% down the slide) to leave ample room for the higher, overlapping top arcs. 
  - Arcs scale their height proportionally based on the distance between the two connected nodes, ensuring nesting rather than tangling.

* **Step C: Dynamic Effects & Transitions**
  - *Tutorial Implementation*: The video uses PowerPoint's animation engine (specifically Motion Paths like "Arc Down" / "Arc Up") to make white dots travel along the curves, simulating "data flow". 
  - *Code Constraints*: While `python-pptx` can generate the perfect static geometric structure of the arc diagram, complex motion paths require manual UI setup or deep XML injection. The code below provides the exact static structural base, allowing a user to easily add motion paths later if desired.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Background & Nodes** | `python-pptx` native | Simple shapes and solid fills easily handle standard node placement. |
| **Connecting Arcs** | `python-pptx` `FreeformBuilder` | Native arc shapes are notoriously difficult to align perfectly to two arbitrary points. Using `FreeformBuilder` to generate a mathematically calculated sine-wave curve ensures perfect, scalable connections between any two nodes. |
| **Typography & Weights** | `python-pptx` native | Standard text boxes with Center alignment easily handle node labels and percentage markers at the arc apices. |

> **Feasibility Assessment**: 90% visual reproduction. The code perfectly mathematically recreates the entire visual structure, the elegant intersecting arcs, and the text hierarchy. The only missing 10% is the animated "moving dots", which requires native PowerPoint animation triggers.

#### 3b. Complete Reproduction Code

```python
import math
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_slide(
    output_pptx_path: str,
    title_text: str = "DATA FLOW DIAGRAM",
    nodes: list = None,
    connections: list = None,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Dark Mode Arc Diagram effect.
    """
    if nodes is None:
        nodes = ["Data 1", "Data 2", "Data 3", "Data 4", "Data 5", "Data 6", "Data 7"]
        
    if connections is None:
        # Tuple format: (Start_Index, End_Index, Label, Is_Top_Arc)
        connections = [
            (0, 2, "10%", True),
            (1, 5, "20%", True),
            (2, 4, "25%", True),
            (3, 5, "18%", True),
            (0, 3, "75%", False),
            (2, 5, "60%", False),
            (4, 6, "40%", False)
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(0, 0, 0) # Pitch black

    # === Layer 2: Main Title ===
    title_box = slide.shapes.add_textbox(Inches(0), Inches(0.5), Inches(13.333), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Arial"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # === Layout Calculation ===
    num_nodes = len(nodes)
    node_spacing = Inches(1.6)
    total_width = (num_nodes - 1) * node_spacing
    start_x = (Inches(13.333) - total_width) / 2.0
    axis_y = Inches(4.5)  # Positioned slightly below center for top arc room

    # Calculate coordinates for each node
    node_coords = []
    for i in range(num_nodes):
        nx = start_x + i * node_spacing
        node_coords.append((nx, axis_y))

    # === Layer 3: Central Axis Line ===
    axis_line = slide.shapes.add_connector(
        MSO_SHAPE.LINE_CALLOUT_1, 
        int(node_coords[0][0]), int(axis_y), 
        int(node_coords[-1][0]), int(axis_y)
    )
    axis_line.line.color.rgb = RGBColor(150, 150, 150)
    axis_line.line.width = Pt(1.5)

    # === Layer 4: Arcs and Weights ===
    for start_idx, end_idx, weight_text, is_top in connections:
        x1, y1 = node_coords[start_idx]
        x2, y2 = node_coords[end_idx]
        
        distance = abs(x2 - x1)
        # Height scales with distance, but tapers off for very long connections
        height = distance * 0.4 
        # Capping height to avoid running off slide
        max_height = Inches(3.0) if is_top else Inches(1.5)
        height = min(height, max_height)
        
        direction = -1 if is_top else 1 # -1 moves UP (y decreases), 1 moves DOWN

        # Generate points for a smooth sine wave arc
        points = []
        num_steps = 40  # Resolution of the curve
        for i in range(num_steps + 1):
            t = i / num_steps
            px = x1 + t * (x2 - x1)
            py = y1 + direction * height * math.sin(t * math.pi)
            points.append((int(px), int(py)))

        # Draw the Freeform curve
        ff_builder = slide.shapes.build_freeform(points[0][0], points[0][1])
        for p in points[1:]:
            ff_builder.add_line_segments([p])
        
        arc_shape = ff_builder.convert_to_shape()
        arc_shape.line.color.rgb = RGBColor(180, 180, 180)
        arc_shape.line.width = Pt(1.2)

        # Place Percentage Label at the apex of the curve
        peak_x = x1 + 0.5 * (x2 - x1)
        peak_y = y1 + direction * height * math.sin(0.5 * math.pi)
        
        lbl_width = Inches(1.0)
        lbl_height = Inches(0.4)
        
        # Adjust Y offset so text sits neatly above or below the line
        y_offset = Inches(0.2)
        lbl_y = peak_y - lbl_height if is_top else peak_y
        
        weight_box = slide.shapes.add_textbox(
            int(peak_x - lbl_width/2), 
            int(lbl_y), 
            int(lbl_width), int(lbl_height)
        )
        tf_w = weight_box.text_frame
        p_w = tf_w.paragraphs[0]
        p_w.text = weight_text
        p_w.alignment = PP_ALIGN.CENTER
        p_w.font.name = "Arial"
        p_w.font.size = Pt(12)
        p_w.font.color.rgb = RGBColor(220, 220, 220)
        
        # Optional: Add a small decorative "data dot" randomly on the first top arc to mimic the video
        if is_top and start_idx == 0:
            dot_t = 0.35  # 35% along the path
            dot_x = x1 + dot_t * (x2 - x1)
            dot_y = y1 + direction * height * math.sin(dot_t * math.pi)
            dot_radius = Inches(0.06)
            data_dot = slide.shapes.add_shape(
                MSO_SHAPE.OVAL, 
                int(dot_x - dot_radius), int(dot_y - dot_radius), 
                int(dot_radius*2), int(dot_radius*2)
            )
            data_dot.fill.solid()
            data_dot.fill.fore_color.rgb = RGBColor(255, 255, 255)
            data_dot.line.fill.background()

    # === Layer 5: Nodes and Node Labels ===
    node_radius = Inches(0.08)
    
    for i, name in enumerate(nodes):
        nx, ny = node_coords[i]
        
        # Add Node Circle
        node_shape = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            int(nx - node_radius), int(ny - node_radius), 
            int(node_radius * 2), int(node_radius * 2)
        )
        node_shape.fill.solid()
        node_shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
        node_shape.line.fill.background() # No border

        # Add Node Label Text
        lbl_width = Inches(1.2)
        lbl_height = Inches(0.5)
        label_box = slide.shapes.add_textbox(
            int(nx - lbl_width / 2), 
            int(ny + Inches(0.1)), 
            int(lbl_width), int(lbl_height)
        )
        tf_l = label_box.text_frame
        p_l = tf_l.paragraphs[0]
        p_l.text = name
        p_l.alignment = PP_ALIGN.CENTER
        p_l.font.name = "Arial"
        p_l.font.size = Pt(14)
        p_l.font.bold = True
        p_l.font.color.rgb = RGBColor(255, 255, 255)

    prs.save(output_pptx_path)
    return output_pptx_path
```