# Structured Page Flow Mapping (UI/UX Logic Diagrams)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Structured Page Flow Mapping (UI/UX Logic Diagrams)

* **Core Visual Mechanism**: The core style relies on nested geometric container logic. A "Page" is visually represented as a distinct bounding box containing a standardized header (Page Number + Title) and body (Key Content + Functions). User interactions ("Actions" or "Conditions") are represented as distinct, highly contrasting secondary shapes (rounded rectangles or diamonds) floating on the connective pathways between pages. 
* **Why Use This Skill (Rationale)**: Abstract user journeys and software architecture can be overwhelming. By enforcing a rigid visual syntax (Pages = Big Rectangles, Actions = Small Coloured Badges, Logic = Diamonds), cognitive load is drastically reduced. It visually separates "States" (where the user is) from "Triggers" (what moves the user to the next state).
* **Overall Applicability**: Ideal for Product Requirements Documents (PRDs), UX/UI wireframing presentations, system architecture design reviews, and onboarding materials for development teams.
* **Value Addition**: Transforms a textual list of requirements into a scannable, spatial blueprint. It allows stakeholders to instantly identify dead-ends, circular loops, or missing steps in a digital product's user experience.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Page Nodes (State Containers)**: Structured as cards. 
    - Outer Box: Light grayish-blue fill `(240, 244, 248, 255)`, dark border `(44, 62, 80, 255)`.
    - Header Region: Solid dark fill `(44, 62, 80, 255)` with white bold text.
    - Body Text: Bulleted lists indicating key content, dark gray text `(52, 73, 94, 255)`.
  - **Action Nodes (Triggers)**: Smaller, pill-shaped or rounded rectangles. High contrast colors like Coral/Orange `(231, 76, 60, 255)` with white text to indicate interactivity.
  - **Decision Nodes (Logic)**: Diamond shapes `(243, 156, 18, 255)` indicating a system check (e.g., "Is user logged in?").
  - **Connectors**: Straight or elbow lines `(127, 140, 141, 255)` with definitive end arrows pointing to the resulting state.

* **Step B: Compositional Style**
  - **Grid Alignment**: strict vertical and horizontal alignment is mandatory. Pages must snap to an invisible grid to look professional.
  - **Spacing**: Generous whitespace between page blocks to allow room for action nodes and connector lines without clutter. 
  - **Proportions**: Page nodes typically occupy an aspect ratio of 4:3 or square. Action nodes are roughly 1/4 the width of a Page node.

* **Step C: Dynamic Effects & Transitions**
  - Generally presented statically. If animated, it uses a simple "Wipe" animation sequence (Page -> Connector -> Action -> Connector -> Next Page) to simulate the user walking through the journey.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Page Containers (Cards with headers) | `python-pptx` native | Standard shape grouping (rectangles + text boxes) is highly stable and editable in PPTX. |
| Action & Decision Nodes | `python-pptx` native | `MSO_SHAPE.ROUNDED_RECTANGLE` and `MSO_SHAPE.DIAMOND` provide the exact semantic shapes needed. |
| Connector Lines | `python-pptx` native | Straight connectors with end-arrows mathematically calculated between shape boundaries ensure clean routing. |

> **Feasibility Assessment**: 100%. The visual style demonstrated in the tutorial relies entirely on standard geometric shapes, color logic, and layout discipline, all of which can be perfectly replicated and parameterized using the native `python-pptx` library.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "User Authentication Page Flow",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Structured Page Flow Mapping' visual effect.
    Builds a wireframe-style diagram showing Page -> Action -> Decision -> Pages.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.shapes import MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN
    
    # Initialize presentation (Widescreen)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Colors
    COLOR_BG = RGBColor(250, 250, 250)
    COLOR_PAGE_BORDER = RGBColor(44, 62, 80)
    COLOR_PAGE_BG = RGBColor(240, 244, 248)
    COLOR_HEADER_BG = RGBColor(44, 62, 80)
    COLOR_TEXT_LIGHT = RGBColor(255, 255, 255)
    COLOR_TEXT_DARK = RGBColor(52, 73, 94)
    COLOR_ACTION = RGBColor(231, 76, 60)
    COLOR_DECISION = RGBColor(243, 156, 18)
    COLOR_LINE = RGBColor(127, 140, 141)

    # Set background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG

    # Add main title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.333), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = COLOR_PAGE_BORDER

    # --- Helper Function: Draw a Page Node ---
    def draw_page(x, y, w, h, page_id, page_title, content_list):
        # Outer Page Box
        page_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
        page_box.fill.solid()
        page_box.fill.fore_color.rgb = COLOR_PAGE_BG
        page_box.line.color.rgb = COLOR_PAGE_BORDER
        page_box.line.width = Pt(1.5)
        
        # Header Box
        header_h = Inches(0.4)
        header = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, header_h)
        header.fill.solid()
        header.fill.fore_color.rgb = COLOR_HEADER_BG
        header.line.color.rgb = COLOR_PAGE_BORDER
        
        # Header Text
        htf = header.text_frame
        htf.clear()
        hp = htf.paragraphs[0]
        hp.text = f"{page_id} | {page_title}"
        hp.font.size = Pt(12)
        hp.font.bold = True
        hp.font.color.rgb = COLOR_TEXT_LIGHT
        hp.alignment = PP_ALIGN.CENTER
        
        # Body Text
        body_box = slide.shapes.add_textbox(x + Inches(0.1), y + header_h, w - Inches(0.2), h - header_h)
        btf = body_box.text_frame
        btf.word_wrap = True
        bp = btf.paragraphs[0]
        bp.text = "Key Contents / Functions:"
        bp.font.size = Pt(11)
        bp.font.bold = True
        bp.font.color.rgb = COLOR_TEXT_DARK
        
        for item in content_list:
            p = btf.add_paragraph()
            p.text = f"• {item}"
            p.font.size = Pt(10)
            p.font.color.rgb = COLOR_TEXT_DARK

    # --- Helper Function: Draw an Action Node ---
    def draw_action(x, y, w, h, text, is_decision=False):
        shape_type = MSO_SHAPE.DIAMOND if is_decision else MSO_SHAPE.ROUNDED_RECTANGLE
        bg_color = COLOR_DECISION if is_decision else COLOR_ACTION
        
        action = slide.shapes.add_shape(shape_type, x, y, w, h)
        action.fill.solid()
        action.fill.fore_color.rgb = bg_color
        action.line.color.rgb = COLOR_BG # White-ish stroke for pop
        action.line.width = Pt(1.5)
        
        tf = action.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_LIGHT
        p.alignment = PP_ALIGN.CENTER

    # --- Helper Function: Draw Connector Line ---
    def draw_arrow(start_x, start_y, end_x, end_y):
        connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, start_x, start_y, end_x, end_y)
        connector.line.color.rgb = COLOR_LINE
        connector.line.width = Pt(2)
        # Add an arrow head via XML manipulation since python-pptx doesn't have a direct property for it
        line_format = connector.line
        # We wrap in a try-except to safely apply end arrow using native element access
        try:
            headEnd = connector.element.spPr.ln.find('{http://schemas.openxmlformats.org/drawingml/2006/main}headEnd')
            if headEnd is None:
                ln = connector.element.spPr.ln
                tailEnd = ln.makeelement('{http://schemas.openxmlformats.org/drawingml/2006/main}tailEnd')
                tailEnd.set('type', 'triangle')
                ln.append(tailEnd)
        except:
            pass # Fallback to standard line if XML structure varies

    # ==========================================
    # Compose the Scene (Layout coordinates)
    # ==========================================
    
    # 1. Start Page (Top Center)
    draw_page(Inches(5.15), Inches(1.2), Inches(3.0), Inches(1.8), 
              "P1.0", "Login Page", ["Account Input", "Password Input", "Forgot Password Link"])
    
    # Line down to Action
    draw_arrow(Inches(6.65), Inches(3.0), Inches(6.65), Inches(3.5))
    
    # 2. Action Trigger (Center)
    draw_action(Inches(6.0), Inches(3.5), Inches(1.3), Inches(0.4), "Click 'Login'")
    
    # Line down to Decision
    draw_arrow(Inches(6.65), Inches(3.9), Inches(6.65), Inches(4.3))
    
    # 3. Decision Node (Center)
    draw_action(Inches(5.9), Inches(4.3), Inches(1.5), Inches(0.8), "Auth Valid?", is_decision=True)
    
    # Lines routing from Decision to End Pages
    # Yes -> Left
    draw_arrow(Inches(5.9), Inches(4.7), Inches(4.5), Inches(4.7))
    draw_arrow(Inches(4.5), Inches(4.7), Inches(4.5), Inches(5.0))
    # No -> Right
    draw_arrow(Inches(7.4), Inches(4.7), Inches(8.8), Inches(4.7))
    draw_arrow(Inches(8.8), Inches(4.7), Inches(8.8), Inches(5.0))
    
    # Labels for Decision branches
    yes_lbl = slide.shapes.add_textbox(Inches(5.0), Inches(4.4), Inches(0.8), Inches(0.4))
    yes_lbl.text_frame.text = "Yes"
    yes_lbl.text_frame.paragraphs[0].font.size = Pt(10)
    
    no_lbl = slide.shapes.add_textbox(Inches(7.5), Inches(4.4), Inches(0.8), Inches(0.4))
    no_lbl.text_frame.text = "No"
    no_lbl.text_frame.paragraphs[0].font.size = Pt(10)
    
    # 4. Result Page A (Bottom Left)
    draw_page(Inches(2.5), Inches(5.0), Inches(3.0), Inches(1.8), 
              "P2.0", "User Dashboard", ["Welcome Message", "Data Overview", "Profile Settings"])
              
    # 5. Result Page B (Bottom Right)
    draw_page(Inches(7.8), Inches(5.0), Inches(3.0), Inches(1.8), 
              "P3.0", "Error Recovery", ["Error Message", "Reset Password Btn", "Contact Support"])

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
```