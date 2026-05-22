# Automated Hierarchy Tree Diagram (Organizational Chart)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Automated Hierarchy Tree Diagram (Organizational Chart)

* **Core Visual Mechanism**: The core visual is a top-down, branched tree diagram. It uses discrete geometric nodes (usually rectangles) to represent entities, arranged in discrete horizontal levels denoting hierarchy, connected by orthogonal "elbow" lines to represent parent-child reporting or compositional relationships.
* **Why Use This Skill (Rationale)**: Human cognition struggles to visualize complex nested relationships from bulleted lists. A spatial hierarchy diagram instantly communicates power structures, categorization constraints, and operational dependencies through the Gestalt principles of proximity and connection.
* **Overall Applicability**: Essential for corporate organizational charts, product feature breakdown structures (WBS), decision trees, family trees, and server/architecture mapping.
* **Value Addition**: Transforms a dense, hard-to-read nested text list into a highly scannable, structurally intuitive visual map. Color coding by level further accelerates comprehension of peer-level relationships.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  *   **Nodes (Shapes)**: Standard rectangles with slight spacing.
  *   **Connectors**: Right-angled elbow lines connecting the bottom center of a parent to the top center of a child.
  *   **Color Logic (Level-based)**:
      *   Level 0 (Root): Dark Blue `(47, 85, 151)`
      *   Level 1 (Managers): Medium Blue `(91, 155, 213)`
      *   Level 2 (Departments): Light Blue `(157, 195, 230)` or Accent Color (e.g., Orange `(237, 125, 49)`)
  *   **Text Hierarchy**: All text is centrally aligned, usually white or dark gray depending on background contrast. Font size decreases slightly at lower levels.

* **Step B: Compositional Style**
  *   **Layout Principles**: Centered, balanced top-down tree. Symmetrical arrangement where possible.
  *   **Proportions**: Nodes are generally twice as wide as they are tall (e.g., 1.5" x 0.6"). Horizontal spacing between nodes must be calculated to prevent overlaps.

* **Step C: Dynamic Effects & Transitions**
  *   Typically static, though Native PowerPoint allows applying "Wipe" or "Fade" animations sequenced "By Level" so the chart builds dynamically during a presentation. (Cannot be fully coded via `python-pptx` natively, must be set in UI).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Organizational Chart Layout** | Custom Python Algorithm | `python-pptx` cannot create or manipulate native PowerPoint SmartArt. To reproduce the visual effect, we must write a tree-traversal algorithm to calculate X/Y coordinates for each node and draw them manually. |
| **Nodes and Text** | `python-pptx` native | Standard shapes, fills, and text frames handle the node rendering perfectly. |
| **Connecting Lines** | `python-pptx` native (`MSO_CONNECTOR.ELBOW`) | Native elbow connectors can be placed between calculated coordinates to draw the orthogonal linking lines. |

> **Feasibility Assessment**: 95%. The visual output will look virtually identical to a SmartArt org chart. The only difference is that it will be composed of individual editable shapes rather than a single locked SmartArt object container.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Company Organizational Structure",
    body_text: str = "",
    bg_palette: str = "corporate", 
    accent_color: tuple = (0, 191, 255), 
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing an Automated Hierarchy Tree Diagram (Org Chart).
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    
    # 1. Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide
    
    # Add Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.333), Inches(0.8))
    tf = title_box.text_frame
    p = tf.add_paragraph()
    p.text = title_text
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(64, 64, 64)
    p.alignment = PP_ALIGN.CENTER

    # 2. Define the Hierarchy Data (Replicating the video's structure)
    org_data = {
        "name": "General Manager",
        "children": [
            {
                "name": "GM Assistant",
                "children": []
            },
            {
                "name": "R&D Dept",
                "children": [
                    {"name": "R&D 1"},
                    {"name": "R&D 2"}
                ]
            },
            {
                "name": "Sales Dept",
                "children": [
                    {"name": "Sales 1"},
                    {"name": "Sales 2"},
                    {"name": "Sales 3"}
                ]
            },
            {
                "name": "Logistics",
                "children": []
            },
            {
                "name": "Production",
                "children": [
                    {"name": "Plant 1"},
                    {"name": "Plant 2"},
                    {"name": "Plant 3"}
                ]
            }
        ]
    }

    # 3. Tree Layout Algorithm
    class TreeNode:
        def __init__(self, name, level=0):
            self.name = name
            self.children = []
            self.level = level
            self.x = 0.0
            self.y = 0.0

    def build_tree(data, level=0):
        node = TreeNode(data['name'], level)
        for child_data in data.get('children', []):
            node.children.append(build_tree(child_data, level + 1))
        return node

    def assign_coordinates(node, current_x=0.0, x_spacing=1.8, y_start=1.5, y_spacing=1.2):
        node.y = y_start + (node.level * y_spacing)
        
        if not node.children:
            node.x = current_x
            return current_x + x_spacing

        child_x = current_x
        for child in node.children:
            child_x = assign_coordinates(child, child_x, x_spacing, y_start, y_spacing)

        # Center parent above children
        node.x = (node.children[0].x + node.children[-1].x) / 2
        return child_x

    def get_bounds(node, bounds=None):
        if bounds is None:
            bounds = {"min_x": float('inf'), "max_x": float('-inf')}
        bounds["min_x"] = min(bounds["min_x"], node.x)
        bounds["max_x"] = max(bounds["max_x"], node.x)
        for child in node.children:
            get_bounds(child, bounds)
        return bounds

    # Build and calculate layout
    root = build_tree(org_data)
    assign_coordinates(root, current_x=0.0, x_spacing=1.6, y_start=1.5, y_spacing=1.4)
    
    # Center the tree on the slide
    bounds = get_bounds(root)
    tree_width = bounds["max_x"] - bounds["min_x"]
    slide_center_x = 13.333 / 2
    offset_x = slide_center_x - (tree_width / 2) - bounds["min_x"]

    def shift_tree(node, offset):
        node.x += offset
        for child in node.children:
            shift_tree(child, offset)
            
    shift_tree(root, offset_x)

    # 4. Drawing the Shapes and Connectors
    node_w = 1.4
    node_h = 0.6
    
    # Color palette based on depth level
    level_colors = {
        0: RGBColor(47, 85, 151),    # Dark Blue
        1: RGBColor(91, 155, 213),   # Medium Blue
        2: RGBColor(237, 125, 49)    # Orange (Accent)
    }

    def draw_tree(node):
        # Determine color
        bg_color = level_colors.get(node.level, RGBColor(165, 165, 165))
        
        # Draw connections to children FIRST (so they are under the shapes)
        for child in node.children:
            start_x = Inches(node.x + node_w / 2)
            start_y = Inches(node.y + node_h)
            end_x = Inches(child.x + node_w / 2)
            end_y = Inches(child.y)
            
            connector = slide.shapes.add_connector(
                MSO_CONNECTOR.ELBOW, start_x, start_y, end_x, end_y
            )
            connector.line.color.rgb = RGBColor(150, 150, 150)
            connector.line.width = Pt(1.5)
            
            # Recursive call to draw child and its subtree
            draw_tree(child)

        # Draw Node Shape
        shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(node.x), Inches(node.y),
            Inches(node_w), Inches(node_h)
        )
        
        # Format Shape
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = RGBColor(255, 255, 255) # White border
        shape.line.width = Pt(1)
        
        # Format Text
        tf = shape.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = node.name
        p.font.size = Pt(14 if node.level < 2 else 12)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER
        
        # Center text vertically (requires accessing shape text frame properties)
        tf.vertical_anchor = 3 # Middle

    # Execute drawing
    draw_tree(root)

    # Save output
    prs.save(output_pptx_path)
    return output_pptx_path
```