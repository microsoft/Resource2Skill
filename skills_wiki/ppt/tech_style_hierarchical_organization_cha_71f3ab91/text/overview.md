# Tech-Style Hierarchical Organization Chart

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Tech-Style Hierarchical Organization Chart

* **Core Visual Mechanism**: The defining visual idea is the transformation of default, rigid organizational charts into a **modern, futuristic "Tech/Corporate" dashboard style**. This is achieved by abandoning default solid blocks in favor of dark-themed, rounded-corner rectangles (`Round Rectangle`), highlighted by neon/cyan glowing borders, orthogonal (elbow) branching connector lines, and a deep ambient background.
* **Why Use This Skill (Rationale)**: Traditional organizational charts often look bureaucratic and visually heavy. By utilizing a dark mode palette with high-contrast accent borders (cyan/neon), the information hierarchy becomes clear while conveying a sense of innovation, agility, and premium branding. The rounded corners soften the psychological rigidity of corporate hierarchies.
* **Overall Applicability**: Ideal for corporate profiles, tech company pitch decks, project kick-offs, department introductions, and dashboard overview slides.
* **Value Addition**: Transforms a mandatory, often boring administrative slide into a visually striking asset that aligns with modern SaaS, Tech, or high-end consulting brand identities.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Background**: Deep ambient navy/dark blue gradient. Represents a "screen" or "blueprint" feel. (e.g., Top `(9, 13, 23)` to Bottom `(24, 34, 59)`).
  * **Nodes (Shapes)**: Rounded rectangles. 
    * Fill: Dark translucent blue `(18, 30, 60)`.
    * Border: Bright Cyan `(0, 191, 255)` with a 1.5pt to 2pt weight.
  * **Lines (Connectors)**: Orthogonal (stepped) lines, color-matched to the shape borders `(0, 191, 255)` to create a seamless "circuit" or "flow" visual.
  * **Text Hierarchy**: White `(255, 255, 255)`. Higher-level nodes (e.g., "General Manager") use bolder or slightly larger typography compared to leaf nodes.

* **Step B: Compositional Style**
  * **Layout Principle**: Strict top-down tree hierarchy. 
  * **Spatial Feel**: Symmetrical balancing. The root node is dead center at the top. Sub-departments spread evenly across the horizontal axis to utilize the 16:9 widescreen format efficiently. 
  * **Proportions**: Nodes should not exceed ~1.5 inches in width to allow 4-6 departments to fit comfortably on a single row without overlapping.

* **Step C: Dynamic Effects & Transitions**
  * **Animation (Manual Setup)**: Typically revealed using a "Wipe" (From Top) on the lines, and "Fade" or "Zoom" on the nodes, cascading down the hierarchy level by level.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Background Gradient** | `PIL/Pillow` | `python-pptx` lacks a simple, robust API for smooth radial/linear background gradients. PIL creates a perfect high-res background image. |
| **Org Chart Logic & Nodes** | Python Algorithm + `python-pptx` | `python-pptx` cannot natively edit or create SmartArt. We must implement a mathematical tree-layout algorithm to calculate X/Y coordinates and draw the nodes using standard `MSO_SHAPE.ROUNDED_RECTANGLE`. |
| **Orthogonal Lines** | `python-pptx` straight connectors | Native elbow connectors auto-route unpredictably via API. Calculating exact mid-points and drawing exact vertical/horizontal lines mathematically guarantees a perfect SmartArt-like look. |

> **Feasibility Assessment**: 95%. Since `python-pptx` cannot interact with PowerPoint's proprietary SmartArt engine, the code bypasses SmartArt entirely and generates standard, perfectly aligned shapes and lines. This is actually *better* for future API manipulation, though it acts as grouped shapes rather than a SmartArt object. The visual result is nearly identical to a highly styled SmartArt chart.

#### 3b. Complete Reproduction Code

```python
import os
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Pt, Inches, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

def create_slide(
    output_pptx_path: str,
    title_text: str = "Company Organization Chart",
    accent_color: tuple = (0, 191, 255),  # Cyan
    node_fill_color: tuple = (18, 30, 60), # Dark Blue
    **kwargs,
) -> str:
    """
    Creates a Tech-Style Hierarchical Organization Chart using a mathematical tree layout.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # ==========================================
    # Layer 1: Generate & Apply Tech Background
    # ==========================================
    bg_img_path = "tech_bg_temp.png"
    width, height = int(13.333 * 100), int(7.5 * 100)
    bg_img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(bg_img)
    
    # Linear gradient from dark navy to slightly lighter navy
    color_top = (9, 13, 23)
    color_bottom = (24, 34, 59)
    for y in range(height):
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * y / height)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * y / height)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    bg_img.save(bg_img_path)

    # Insert background
    slide.shapes.add_picture(bg_img_path, 0, 0, prs.slide_width, prs.slide_height)

    # ==========================================
    # Layer 2: Title
    # ==========================================
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.333), Inches(0.8))
    tf = title_box.text_frame
    tf.text = title_text
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].font.size = Pt(32)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

    # ==========================================
    # Layer 3: Org Chart Data & Layout Algorithm
    # ==========================================
    # Default organization data structure
    org_data = {
        "name": "General Manager",
        "children": [
            {
                "name": "Marketing Dept",
                "children": [{"name": "Sales Group 1"}, {"name": "Sales Group 2"}]
            },
            {
                "name": "Production Dept",
                "children": [{"name": "Raw Materials"}, {"name": "Assembly"}]
            },
            {
                "name": "R&D Dept",
                "children": [{"name": "Dev Group 1"}, {"name": "Dev Group 2"}]
            },
            {
                "name": "HR Dept",
                "children": [{"name": "Recruitment"}, {"name": "Admin"}]
            }
        ]
    }

    # Configuration for nodes
    NODE_W = Inches(1.6)
    NODE_H = Inches(0.6)
    GAP_Y = Inches(0.8) # Vertical gap between levels
    START_Y = Inches(1.5)
    
    # Calculate total leaves to determine horizontal spacing
    def get_leaves_count(node):
        if not node.get("children"):
            return 1
        return sum(get_leaves_count(c) for c in node["children"])
    
    total_leaves = get_leaves_count(org_data)
    # Distribute leaves evenly across the slide width (with margins)
    margin_x = Inches(1.0)
    available_width = prs.slide_width - (margin_x * 2)
    spacing_x = available_width / (total_leaves - 1) if total_leaves > 1 else 0

    # Recursive layout function (Post-order traversal)
    def calculate_positions(node, depth, leaf_counter):
        if not node.get("children"):
            # Leaf node gets an absolute X position
            x = margin_x + leaf_counter[0] * spacing_x
            y = START_Y + depth * (NODE_H + GAP_Y)
            leaf_counter[0] += 1
            node["pos"] = (x, y)
            return x
        else:
            # Parent node X is the average of its children's X
            child_x_list = []
            for child in node["children"]:
                cx = calculate_positions(child, depth + 1, leaf_counter)
                child_x_list.append(cx)
            x = sum(child_x_list) / len(child_x_list)
            y = START_Y + depth * (NODE_H + GAP_Y)
            node["pos"] = (x, y)
            return x

    # Run layout algorithm
    leaf_counter = [0]
    calculate_positions(org_data, 0, leaf_counter)

    # ==========================================
    # Layer 4: Draw Connectors & Nodes
    # ==========================================
    shapes = slide.shapes

    def draw_line(x1, y1, x2, y2):
        """Helper to draw styled orthogonal line segments."""
        line = shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
        line.line.color.rgb = RGBColor(*accent_color)
        line.line.width = Pt(1.5)

    def draw_tree(node):
        # Draw connections to children FIRST (so they are under the shapes)
        if node.get("children"):
            px, py = node["pos"]
            p_bottom_y = py + NODE_H / 2
            mid_y = p_bottom_y + GAP_Y / 2 # Midpoint for the horizontal branching line

            # 1. Vertical line from parent bottom to mid-y
            draw_line(px, p_bottom_y, px, mid_y)

            # 2. Horizontal line spanning all children
            first_child_x = node["children"][0]["pos"][0]
            last_child_x = node["children"][-1]["pos"][0]
            if first_child_x != last_child_x:
                draw_line(first_child_x, mid_y, last_child_x, mid_y)

            # 3. Vertical lines from mid-y down to each child
            for child in node["children"]:
                cx, cy = child["pos"]
                c_top_y = cy - NODE_H / 2
                draw_line(cx, mid_y, cx, c_top_y)
                
                # Recursively draw child's tree
                draw_tree(child)

        # Draw Node Shape
        cx, cy = node["pos"]
        left = int(cx - NODE_W / 2)
        top = int(cy - NODE_H / 2)
        
        # Add Rounded Rectangle
        rect = shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, NODE_W, NODE_H)
        
        # Style Shape
        rect.fill.solid()
        rect.fill.fore_color.rgb = RGBColor(*node_fill_color)
        rect.line.color.rgb = RGBColor(*accent_color)
        rect.line.width = Pt(1.5)
        
        # Add Text
        tf = rect.text_frame
        tf.text = node["name"]
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(255, 255, 255)
        if not node.get("children"):
            # Leaf nodes slightly dimmer/smaller if desired, keeping consistent for now
            p.font.size = Pt(11)
        else:
            p.font.bold = True

    # Execute drawing
    draw_tree(org_data)

    # Cleanup temporary image
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)

    prs.save(output_pptx_path)
    return output_pptx_path
```