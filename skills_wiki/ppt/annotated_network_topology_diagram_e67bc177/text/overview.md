# Annotated Network Topology Diagram

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Annotated Network Topology Diagram

*   **Core Visual Mechanism**: The design uses a clean, two-dimensional layout of standardized iconography to represent a computer network's physical or logical topology. The core principle is clarity through simplification, where complex hardware is reduced to simple geometric shapes (circles for routers, squares for switches) and connections are represented by clean, straight lines. The key "effect" is the use of numbered, high-contrast labels overlaid on connection paths or segments to enumerate distinct subnets or broadcast domains, turning a static diagram into a teaching tool.

*   **Why Use This Skill (Rationale)**: This style is effective because it leverages universal conventions in technical diagramming. By abstracting complex technology into simple symbols, it reduces cognitive load and allows the audience to focus on the network's structure and relationships. The numbered annotations act as visual signposts, guiding the viewer's attention sequentially and breaking down a complex system into digestible parts, which is ideal for educational or explanatory content.

*   **Overall Applicability**: This pattern is highly applicable for:
    *   **IT and Networking Education**: Explaining concepts like subnets, routing, and broadcast domains.
    *   **System Architecture Proposals**: Clearly communicating a proposed network design to stakeholders.
    *   **Technical Documentation**: Visually documenting existing network infrastructure.
    *   **Cybersecurity Briefings**: Illustrating network vulnerabilities or data flow paths.

*   **Value Addition**: Compared to a purely textual description or a cluttered, realistic diagram, this style provides immediate clarity and an intuitive understanding of connectivity. It transforms an abstract list of components into a coherent map, making the information more memorable and easier to reference.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    - **Icons**: Simple, solid-color geometric shapes are used to represent network devices.
        - **Router**: A blue circle.
        - **Switch**: A blue square or rectangle.
        - **End Device (Computer/Server)**: A smaller, grey or green-grey rectangle.
    - **Connectors**: Thin, solid black lines representing data links.
    - **Annotations**: Small, white squares with a thin black border, containing a bold, black, centered number.
    - **Color Logic**:
        - Background: White `(255, 255, 255, 255)`
        - Core Network Devices (Routers, Switches): A professional, medium blue `(79, 129, 189, 255)`.
        - End Devices: A neutral dark grey `(128, 128, 128, 255)`.
        - Connectors: Black `(0, 0, 0, 255)`.
        - Annotation Fill: White `(255, 255, 255, 255)`.
        - Annotation Border & Text: Black `(0, 0, 0, 255)`.
    - **Text Hierarchy**: The only text is the numeric annotation, which is given high prominence through its contrast and placement. Device labels are omitted for simplicity, but could be added as small text below each icon.

*   **Step B: Compositional Style**
    - **Layout**: The diagram uses a non-overlapping, node-and-link layout. Devices are distributed across the canvas with ample white space to ensure connection lines are clearly visible and easy to follow.
    - **Proportions**: Core network devices (routers, switches) are larger than end devices (computers) to create a visual hierarchy. Annotation boxes are small enough not to obscure the diagram but large enough to be easily legible.
    - **Layering**: The composition is two-layered. The base layer contains all devices and connectors. The top layer contains all the numbered annotations, which sit visually "above" the network topology.

*   **Step C: Dynamic Effects & Transitions**
    - The source video uses simple "appear" animations to introduce the annotations one by one. This is a presentation-time effect. The core skill is the generation of the final, fully annotated static slide. The sequential reveal can be achieved in code by generating multiple slides, each adding one more annotation.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Network device icons | `python-pptx` native shapes | Standard shapes like `OVAL` and `RECTANGLE` are universally understood symbols for routers and switches, making the diagram clear and the code simple and robust. |
| Device layout & connections | `python-pptx` native shapes & connectors | The `add_shape` and `add_connector` methods are the standard and most efficient way to build this type of diagram, allowing for precise placement and linking. |
| Numbered annotations | `python-pptx` `add_textbox` | A textbox is the ideal element for creating the numbered labels, as it allows for precise control over fill, border, text formatting, and alignment. |
| Overall composition | `python-pptx` native | The entire visual is composed of vector shapes, lines, and text, which is the core strength of `python-pptx`. No external libraries are needed. |

> **Feasibility Assessment**: 100%. The visual style is based on fundamental vector shapes and text, which can be fully and accurately reproduced using the `python-pptx` library.

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.enum.text import PP_ALIGN

def create_slide(
    output_pptx_path: str = "network_diagram.pptx",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with an annotated network topology diagram.

    This function reproduces the visual style of explaining network segments
    by overlaying numbered labels on a clean, symbolic network map.

    Returns:
        str: The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)

    # Define colors
    BG_COLOR = RGBColor(255, 255, 255)
    DEVICE_BLUE = RGBColor(79, 129, 189)
    END_DEVICE_GREY = RGBColor(128, 128, 128)
    LINE_COLOR = RGBColor(0, 0, 0)
    
    # Set background color
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

    # --- Device Definitions ---
    # {name: (shape_type, left, top, width, height, color, text)}
    devices = {
        'R1': (MSO_SHAPE.OVAL, Inches(2), Inches(1), Inches(1), Inches(1), DEVICE_BLUE, 'R1'),
        'R2': (MSO_SHAPE.OVAL, Inches(10), Inches(1), Inches(1), Inches(1), DEVICE_BLUE, 'R2'),
        'R3': (MSO_SHAPE.OVAL, Inches(3.5), Inches(3), Inches(1), Inches(1), DEVICE_BLUE, 'R3'),
        'R4': (MSO_SHAPE.OVAL, Inches(8.5), Inches(4), Inches(1), Inches(1), DEVICE_BLUE, 'R4'),
        'S1': (MSO_SHAPE.RECTANGLE, Inches(4.5), Inches(5.5), Inches(1), Inches(0.75), DEVICE_BLUE, 'S1'),
        'S2': (MSO_SHAPE.RECTANGLE, Inches(11), Inches(3), Inches(1), Inches(0.75), DEVICE_BLUE, 'S2'),
        'PC1': (MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.125), Inches(0.75), Inches(0.5), END_DEVICE_GREY, 'PC1'),
        'PC2': (MSO_SHAPE.RECTANGLE, Inches(12), Inches(1.125), Inches(0.75), Inches(0.5), END_DEVICE_GREY, 'PC2'),
        'PC3': (MSO_SHAPE.RECTANGLE, Inches(12), Inches(4.125), Inches(0.75), Inches(0.5), END_DEVICE_GREY, 'PC3'),
        'PC4': (MSO_SHAPE.RECTANGLE, Inches(2.5), Inches(6.5), Inches(0.75), Inches(0.5), END_DEVICE_GREY, 'PC4'),
        'PC5': (MSO_SHAPE.RECTANGLE, Inches(4.75), Inches(6.5), Inches(0.75), Inches(0.5), END_DEVICE_GREY, 'PC5'),
        'PC6': (MSO_SHAPE.RECTANGLE, Inches(7), Inches(6.5), Inches(0.75), Inches(0.5), END_DEVICE_GREY, 'PC6'),
    }

    device_shapes = {}
    for name, (shape_type, left, top, width, height, color, text) in devices.items():
        shape = slide.shapes.add_shape(shape_type, left, top, width, height)
        shape.text = text
        p = shape.text_frame.paragraphs[0]
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER

        fill = shape.fill
        fill.solid()
        fill.fore_color.rgb = color
        
        line = shape.line
        line.fill.background() # No line
        
        device_shapes[name] = shape

    # --- Connection Definitions ---
    # (start_device, end_device)
    connections = [
        ('PC1', 'R1'), ('R1', 'R2'), ('PC2', 'R2'), ('R1', 'R3'),
        ('R2', 'R3'), ('R3', 'R4'), ('R2', 'S2'), ('R4', 'S2'),
        ('S2', 'PC3'), ('R3', 'S1'), ('R4', 'S1'), ('S1', 'PC4'),
        ('S1', 'PC5'), ('S1', 'PC6')
    ]

    for start_name, end_name in connections:
        start_shape = device_shapes[start_name]
        end_shape = device_shapes[end_name]
        connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, 0, 0, 0, 0)
        
        # Connect the shapes
        connector.begin_x = start_shape.left + start_shape.width // 2
        connector.begin_y = start_shape.top + start_shape.height // 2
        connector.end_x = end_shape.left + end_shape.width // 2
        connector.end_y = end_shape.top + end_shape.height // 2

        # Style connector line
        line = connector.line
        line.color.rgb = LINE_COLOR
        line.width = Pt(1.5)

    # --- Annotation Definitions ---
    # (number, left, top)
    annotations = [
        ('1', Inches(1.4), Inches(0.7)),
        ('2', Inches(6), Inches(0.7)),
        ('3', Inches(11.1), Inches(0.7)),
        ('4', Inches(2.9), Inches(2.2)),
        ('5', Inches(7), Inches(2.2)),
        ('6', Inches(11.2), Inches(2.2)),
        ('7', Inches(6.25), Inches(3.7)),
        ('8', Inches(3.5), Inches(4.7)),
    ]
    
    label_size = Inches(0.3)
    for num, left, top in annotations:
        textbox = slide.shapes.add_textbox(left, top, label_size, label_size)
        
        # Style textbox fill and line
        fill = textbox.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(255, 255, 255)
        line = textbox.line
        line.color.rgb = RGBColor(0, 0, 0)
        line.width = Pt(1)

        # Style text
        tf = textbox.text_frame
        tf.clear() # remove default paragraph
        p = tf.paragraphs[0]
        p.text = num
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = RGBColor(0, 0, 0)
        p.alignment = PP_ALIGN.CENTER
        tf.margin_bottom = 0
        tf.margin_top = 0
        tf.margin_left = 0
        tf.margin_right = 0

    prs.save(output_pptx_path)
    return output_pptx_path

# Example of how to run the function
if __name__ == '__main__':
    file_path = create_slide()
    print(f"Presentation saved to: {file_path}")
    # To open the file on Windows
    if os.name == 'nt':
        os.startfile(file_path)
```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback)? (N/A - no images used)
- [x] Are all color values explicit RGBA tuples (not referencing undefined variables)?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?
- [x] Would someone looking at the output say "yes, that's the same technique"?