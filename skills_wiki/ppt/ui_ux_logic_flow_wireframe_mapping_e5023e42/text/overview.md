# UI/UX Logic Flow & Wireframe Mapping

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: UI/UX Logic Flow & Wireframe Mapping

* **Core Visual Mechanism**: The core visual signature is the translation of abstract user journeys into a structured, modular flowchart. It relies on nested geometric shapes (a large "Screen" rectangle containing "Page Name" and "Features" text) connected by orthogonal lines, intercepted by smaller interactive nodes (Action/Button labels) and logical operators (Decision diamonds). 
* **Why Use This Skill (Rationale)**: This style bridges the gap between pure text requirements and high-fidelity prototypes. By visualizing the layout logically, product managers and designers can identify dead ends, missing pages, or cyclical loops in the user experience before writing a single line of code or designing a final screen.
* **Overall Applicability**: Ideal for Product Requirements Documents (PRDs), app architecture overviews, user journey presentations, and system logic mapping. 
* **Value Addition**: Transforms dense bulleted lists of app features into an easy-to-read, chronological visual map. It establishes clear hierarchy (Page -> Action -> Next Page).

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Screen/Page Nodes**: Large, light-filled rectangles with prominent dark borders representing a single UI screen.
  * **Information Blocks**: Within the screen node, text is hierarchically divided into "Page ID/Name" (top) and "Key Features" (bottom).
  * **Interactive Nodes**: Smaller rounded or standard rectangles resting on connector lines, visually representing the user clicking a button or taking an action.
  * **Color Logic**:
    * Canvas/Background: Warm parchment/cream `(244, 239, 230, 255)`
    * Screen Node Fill: Cool light blue `(217, 226, 236, 255)`
    * Screen Border & Text: Deep navy `(16, 42, 67, 255)`
    * Action/Button Fill: Pale orange/peach `(255, 229, 217, 255)`
    * Action Border: Burnt orange `(217, 119, 6, 255)`
* **Step B: Compositional Style**
  * Flow generally reads left-to-right (chronological user journey).
  * Equal spacing between screen nodes to establish rhythm.
  * Orthogonal (elbow) lines connecting elements to maintain a grid-like, organized appearance.
* **Step C: Dynamic Effects & Transitions**
  * This is primarily a static layout technique. If animated, it would use simple "Wipe" or "Fade" transitions revealing the flow one node at a time from left to right.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Basic layout, Page Nodes, Decision Diamonds | `python-pptx` native shapes | The visual style relies entirely on standard vector geometry (rectangles, diamonds). |
| Text hierarchy within shapes | `python-pptx` native text frames | Paragraph formatting, font sizes, and word wrap can be natively handled. |
| Connectors & Orthogonal lines | `python-pptx` native connectors | Standard lines can be drawn to link the logical progression of the flow. |

> **Feasibility Assessment**: 95%. The code will perfectly recreate the flat, geometric, color-coded flowchart style shown in the video. The only limitation is that `python-pptx` does not natively support "dynamic snapping" of elbow connectors via high-level API in a way that reroutes automatically when shapes move, but we can geometrically calculate the static line placement to look identical to the final frame.

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN
from pptx.enum.dml import MSO_THEME_COLOR

def create_slide(
    output_pptx_path: str,
    title_text: str = "User Login & Dashboard Flow",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the UI/UX Page Flowchart effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Colors
    bg_color = RGBColor(244, 239, 230)
    screen_fill = RGBColor(217, 226, 236)
    screen_border = RGBColor(16, 42, 67)
    action_fill = RGBColor(255, 229, 217)
    action_border = RGBColor(217, 119, 6)
    text_color = RGBColor(16, 42, 67)

    # Set Background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = bg_color

    # Helper function to create a "Screen Node"
    def add_screen_node(x, y, page_id, page_name, features):
        w, h = Inches(2.2), Inches(2.5)
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = screen_fill
        shape.line.color.rgb = screen_border
        shape.line.width = Pt(1.5)
        
        # Clear default text margin and text
        tf = shape.text_frame
        tf.clear()
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = Pt(10)
        
        # Add Page ID / Name
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = f"{page_id} {page_name}"
        run.font.bold = True
        run.font.size = Pt(14)
        run.font.color.rgb = text_color
        
        # Separator Line simulation (using dashes)
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        run2 = p2.add_run()
        run2.text = "-------------------"
        run2.font.size = Pt(12)
        run2.font.color.rgb = screen_border
        
        # Add Features
        p3 = tf.add_paragraph()
        p3.alignment = PP_ALIGN.LEFT
        p3.space_before = Pt(5)
        run3 = p3.add_run()
        run3.text = features
        run3.font.size = Pt(11)
        run3.font.color.rgb = text_color
        
        return shape

    # Helper function to create an "Action/Button Node"
    def add_action_node(x, y, action_name):
        w, h = Inches(1.2), Inches(0.5)
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = action_fill
        shape.line.color.rgb = action_border
        shape.line.width = Pt(1)
        
        tf = shape.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = action_name
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = action_border
        return shape

    # Helper function to create a "Decision Diamond"
    def add_decision_node(x, y, text):
        w, h = Inches(1.5), Inches(1.5)
        shape = slide.shapes.add_shape(MSO_SHAPE.DIAMOND, x, y, w, h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = screen_border
        shape.line.width = Pt(1.5)
        
        tf = shape.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = text
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = text_color
        return shape

    # Helper to draw straight connection line
    def draw_line(start_x, start_y, end_x, end_y):
        connector = slide.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT, start_x, start_y, end_x, end_y
        )
        connector.line.color.rgb = screen_border
        connector.line.width = Pt(1.5)
        return connector

    # --- Constructing the Flowchart ---
    
    # 1. Main Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(10), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = title_text
    run.font.size = Pt(24)
    run.font.bold = True
    run.font.color.rgb = RGBColor(176, 26, 26) # Dark red title matching video branding

    # Coordinates
    y_center = Inches(3.5)
    
    # Node 1: Login Screen
    node1 = add_screen_node(Inches(1.0), Inches(2.25), "01", "Login", "1. Username Input\n2. Password Input\n3. Login Button\n4. Forgot Password")
    
    # Action 1: Click Login
    act1 = add_action_node(Inches(3.5), Inches(3.25), "Click Login")
    
    # Decision: Valid?
    dec1 = add_decision_node(Inches(5.0), Inches(2.75), "Valid\nCredentials?")
    
    # Node 2: Dashboard (Success)
    node2 = add_screen_node(Inches(8.5), Inches(0.8), "02", "Dashboard", "1. User Profile\n2. Data Charts\n3. Settings Link\n4. Logout")
    
    # Action 2: Pass
    act2 = add_action_node(Inches(6.8), Inches(1.3), "Yes")
    
    # Node 3: Error Page (Fail)
    node3 = add_screen_node(Inches(8.5), Inches(4.0), "03", "Error Prompt", "1. Error Message\n2. Retry Button\n3. Contact Support")
    
    # Action 3: Fail
    act3 = add_action_node(Inches(6.8), Inches(5.0), "No")

    # --- Draw Lines (Order is back-to-front so shapes sit on top of lines) ---
    
    # Line: Node 1 to Action 1 to Decision
    draw_line(Inches(3.2), Inches(3.5), Inches(5.0), Inches(3.5))
    
    # Line: Decision to Node 2 (Elbow simulation)
    draw_line(Inches(5.75), Inches(2.75), Inches(5.75), Inches(1.55)) # Up
    draw_line(Inches(5.75), Inches(1.55), Inches(8.5), Inches(1.55))  # Right
    
    # Line: Decision to Node 3 (Elbow simulation)
    draw_line(Inches(5.75), Inches(4.25), Inches(5.75), Inches(5.25)) # Down
    draw_line(Inches(5.75), Inches(5.25), Inches(8.5), Inches(5.25))  # Right

    # Bring actions to front (PPTX adds shapes in order, so lines drawn last are on top. 
    # We must re-add/adjust z-order or just place them strategically. 
    # Since we can't easily change Z-order in pure python-pptx without XML, 
    # we redraw the Action Nodes over the lines).
    slide.shapes.element.remove(act1.element)
    slide.shapes.element.remove(act2.element)
    slide.shapes.element.remove(act3.element)
    
    add_action_node(Inches(3.5), Inches(3.25), "Click Login")
    add_action_node(Inches(6.8), Inches(1.3), "Yes")
    add_action_node(Inches(6.8), Inches(5.0), "No")

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path

if __name__ == "__main__":
    create_slide("ui_ux_flowchart.pptx")
```