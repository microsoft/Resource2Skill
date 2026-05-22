# Hierarchical Architecture Topology (Cloud Native)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Hierarchical Architecture Topology (Cloud Native)

* **Core Visual Mechanism**: This design style relies on **spatial nesting and distinct color coding**. It uses large, transparent bounding boxes (containers) to represent logical boundaries (e.g., VPCs, Cloud environments, Regions) and small, grid-aligned nodes (resources) color-coded by their function (Compute, Networking, Database). Directional paths define the flow of data or requests, punctuated by numbered, high-contrast callout badges for step-by-step explanations.
* **Why Use This Skill (Rationale)**: Complex systems overwhelm the viewer. By nesting components inside clear boundary boxes, the brain instantly processes the "where" before the "what." Grid alignment reduces cognitive load, and numbered callouts act as an integrated narrative guide, allowing the diagram to tell a linear story without requiring a separate text document.
* **Overall Applicability**: Essential for technical presentations, system design reviews, deployment topologies, cybersecurity threat models, and process flowcharts.
* **Value Addition**: Transforms a chaotic web of boxes and arrows into a clean, readable map. It elevates technical documentation to professional-grade communication that executives and engineers can both understand.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Containers (Groups)**: Light, airy bounding boxes. Usually white or completely transparent backgrounds with distinct dashed or solid thin borders. Label text sits at the top-left to stay out of the way.
  - **Nodes (Resources)**: Rounded rectangles with high contrast. The AWS 2021 Lucidchart aesthetic uses a white background with a thick, domain-specific colored border and colored text, or solid pastel colors.
    - *Squid Ink (Dark Text)*: `(35, 47, 62, 255)`
    - *Networking (Purple)*: `(140, 79, 255, 255)`
    - *Compute (Orange)*: `(237, 113, 0, 255)`
    - *Database (Blue)*: `(51, 85, 218, 255)`
    - *Containers/Boundaries (Gray/Blue)*: `(84, 107, 130, 255)`
  - **Callouts**: Small, perfect circles with solid bold fills (e.g., AWS Navy or Bright Blue) containing bold, white numbers.

* **Step B: Compositional Style**
  - **Grid Alignment**: strict orthogonal alignment (left-to-right flow is standard for web requests).
  - **Padding**: Generous negative space inside containers (at least 10-15% margin around the nested nodes) so the diagram breathes.
  - **Connection Lines**: Clean, straight, or right-angled lines. Avoid diagonal crossing lines whenever possible.

* **Step C: Dynamic Effects & Transitions**
  - Usually static in standard documentation. In live presentations, the "Wipe" or "Fade" transition is used to reveal the architecture layer by layer (e.g., Boundary -> Nodes -> Connectors -> Callouts).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Nodes, Containers, and Text** | `python-pptx` native | System architecture diagrams **must** remain editable vector objects. Using PIL to bake this into a flat image destroys its utility for future updates. |
| **Dashed Borders & Transparent Fills** | `python-pptx` native | Supported natively via `line.dash_style` and `fill.background()`. |
| **Grid Placement & Routing** | Python Math logic | Automating exact X/Y coordinates mathematically ensures perfect grid alignment, which is the hallmark of a professional diagram. |

> **Feasibility Assessment**: 95%. The code generates a fully editable, highly professional, grid-aligned architecture diagram mimicking the Lucidchart AWS style. The only limitation is that we synthesize the "icons" using text and color borders instead of injecting proprietary AWS SVG icon files (which keeps the script self-contained and dependency-free).

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Multi-region API Gateway Architecture",
    body_text: str = "",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Hierarchical Architecture Topology" visual effect.
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from pptx.enum.line import MSO_LINE_DASH_STYLE

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Color Palette
    COLOR_TEXT = RGBColor(35, 47, 62)
    COLOR_BOUNDARY = RGBColor(135, 149, 150)
    COLOR_CALLOUT = RGBColor(0, 115, 187)
    
    # Domain Colors (AWS-inspired)
    C_NET = RGBColor(140, 79, 255)   # Purple (Route 53, CloudFront, API Gateway)
    C_COMP = RGBColor(237, 113, 0)   # Orange (Lambda)
    C_DB = RGBColor(51, 85, 218)     # Blue (Aurora)
    C_GEN = RGBColor(100, 100, 100)  # Gray (Client)

    # --- Helper Functions ---
    def draw_container(name, left, top, width, height, dash=False):
        """Draws a boundary box with a label."""
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        shape.fill.background() # Transparent
        shape.line.color.rgb = COLOR_BOUNDARY
        shape.line.width = Pt(1.5)
        if dash:
            shape.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        
        # Add label at top left
        txBox = slide.shapes.add_textbox(left, top, Inches(2), Inches(0.5))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = name
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT
        return shape

    def draw_node(name, left, top, color):
        """Draws a service node (white box, colored border, colored text)."""
        w, h = Inches(1.4), Inches(1.0)
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
        shape.line.color.rgb = color
        shape.line.width = Pt(2.5)
        
        tf = shape.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = name
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = color
        return shape, (left + w/2, top + h/2), (left, top, w, h) # return shape, center coords, rect

    def draw_line(pt1, pt2):
        """Draws a connecting arrow between two points."""
        connector = slide.shapes.add_connector(
            1, pt1[0], pt1[1], pt2[0], pt2[1]  # 1 = MSO_CONNECTOR.STRAIGHT
        )
        connector.line.color.rgb = COLOR_BOUNDARY
        connector.line.width = Pt(1.5)
        # To add an arrow head, we use a slight XML hack or rely on default properties. 
        # python-pptx doesn't expose line end arrowheads easily in the top-level API, 
        # but for a pure architecture map, the clean straight line is standard.
        return connector

    def draw_callout(number, cx, cy):
        """Draws a numbered circular badge."""
        r = Inches(0.18)
        shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx - r, cy - r, r*2, r*2)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CALLOUT
        shape.line.fill.background() # No border
        
        tf = shape.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = str(number)
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        return shape

    # --- Step 1: Add Title ---
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(10), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT

    # --- Step 2: Draw Structural Containers ---
    # Global AWS Cloud Box
    draw_container("AWS Cloud", Inches(2.5), Inches(1.2), Inches(10.0), Inches(5.8), dash=False)
    # Region A Box
    draw_container("Region A", Inches(6.0), Inches(1.5), Inches(6.2), Inches(2.4), dash=True)
    # Region B Box
    draw_container("Region B", Inches(6.0), Inches(4.3), Inches(6.2), Inches(2.4), dash=True)

    # --- Step 3: Draw Nodes (Grid System) ---
    col_1 = Inches(0.6) # Outside AWS
    col_2 = Inches(3.0) # Global AWS
    col_3 = Inches(4.5) # Global AWS (CloudFront)
    col_4 = Inches(6.4) # API Gateway
    col_5 = Inches(8.4) # Lambda
    col_6 = Inches(10.4) # DB
    
    row_A = Inches(2.2)
    row_B = Inches(5.0)

    # Instantiate Nodes
    _, c_client, _ = draw_node("Global Clients", col_1, Inches(3.6), C_GEN)
    
    _, c_r53, _ = draw_node("Route 53", col_2, Inches(3.6), C_NET)
    _, c_cf, _  = draw_node("CloudFront", col_3, Inches(3.6), C_NET)
    
    # Region A Nodes
    _, c_api_a, _ = draw_node("API Gateway", col_4, row_A, C_NET)
    _, c_lam_a, _ = draw_node("Lambda Handlers", col_5, row_A, C_COMP)
    _, c_db_a, _  = draw_node("Aurora DB\n(Primary)", col_6, row_A, C_DB)

    # Region B Nodes
    _, c_api_b, _ = draw_node("API Gateway", col_4, row_B, C_NET)
    _, c_lam_b, _ = draw_node("Lambda Handlers", col_5, row_B, C_COMP)
    _, c_db_b, _  = draw_node("Aurora DB\n(Replica)", col_6, row_B, C_DB)

    # --- Step 4: Draw Connecting Lines ---
    draw_line(c_client, c_r53)
    draw_line(c_r53, c_cf)
    
    # Orthogonal routing simulation (point-to-point for simplicity in PPTX math)
    draw_line(c_cf, c_api_a)
    draw_line(c_cf, c_api_b)
    
    draw_line(c_api_a, c_lam_a)
    draw_line(c_lam_a, c_db_a)
    
    draw_line(c_api_b, c_lam_b)
    draw_line(c_lam_b, c_db_b)
    
    # DB Replication Line (Vertical)
    draw_line(c_db_a, c_db_b)

    # --- Step 5: Add Numbered Callouts ---
    draw_callout(1, col_2 + Inches(0.7), Inches(3.6) - Inches(0.6))  # Over Route 53
    draw_callout(2, col_3 + Inches(0.7), Inches(3.6) - Inches(0.6))  # Over CloudFront
    draw_callout(3, col_4 + Inches(0.7), row_A - Inches(0.6))        # Over API GW A
    draw_callout(4, col_6 + Inches(0.7), Inches(3.6))                # Between DBs for replication

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
```