# Process Branching Flowchart with Contextual Image Overlay

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Process Branching Flowchart with Contextual Image Overlay

* **Core Visual Mechanism**: This technique transforms a standard, dry process diagram into an engaging visual by layering uniform, lightly colored flowchart nodes over a highly transparent, contextually relevant background image. The background provides thematic flavor (e.g., medical masks for health protocols) without compromising the readability of the foreground data. Thick, brightly colored connecting arrows guide the eye through the decision tree.
* **Why Use This Skill (Rationale)**: Flowcharts can often feel sterile. Adding a 10-15% opacity background image grounds the abstract logic in a real-world context. This creates an emotional or thematic anchor for the viewer, making the information more memorable. The use of consistent shape styles and thick stroke weights ensures cognitive ease when following complex branching logic.
* **Overall Applicability**: Ideal for decision trees, troubleshooting guides, medical or safety protocols, onboarding processes, and organizational structures. 
* **Value Addition**: It bridges the gap between a "data slide" and a "design slide." It elevates a basic Visio-style diagram into a presentation-ready graphic that feels custom-made and cohesive.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: A full-bleed photograph, heavily washed out (approx. 85% transparent or blended with solid white) so it reads as a subtle texture rather than a focal point.
  - **Nodes**: Rounded rectangles with a very light background fill and a solid border. 
  - **Color Logic**: 
    - Node Fill: Light Peach `(255, 235, 218)`
    - Node Border & Arrows: Vivid Orange `(237, 125, 49)`
    - Text: Dark Charcoal `(64, 64, 64)` to ensure high contrast against the light peach nodes.
  - **Connectors**: Straight lines with triangle arrowheads, weighted heavily (e.g., 2.5pt - 3pt) to clearly define the path of action.

* **Step B: Compositional Style**
  - **Hierarchy**: The layout flows strictly top-to-bottom. A single entry point (Symptoms) leads to a central hub (Call Physician), which then branches into parallel horizontal columns (Mild, Severe, Unsure) representing different outcomes.
  - **Spacing**: Generous negative space between columns ensures the branches don't feel cluttered. Nodes occupy roughly 20-25% of the slide width each.

* **Step C: Dynamic Effects & Transitions**
  - The video teases animating the flowchart. Typically, this involves using the "Wipe" animation (from Top) for arrows, and "Fade" or "Zoom" for the nodes, triggered sequentially to walk the audience through the process one step at a time.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Subtle Background Image** | `PIL/Pillow` | Native `python-pptx` cannot easily apply global alpha transparency to an inserted image. PIL allows us to blend the downloaded photo with a white background to perfectly wash it out before inserting. |
| **Connecting Arrows** | `lxml` XML injection | While `python-pptx` can create connector lines, adding the actual *arrowhead* to the end of the line requires modifying the underlying Open XML (`<a:tailEnd type="triangle"/>`). |
| **Nodes and Layout** | `python-pptx` native | `add_shape` is perfect for creating the rounded rectangles, and standard text frame properties handle the alignment and typography. |

> **Feasibility Assessment**: **95%**. The code accurately reproduces the visual layout, node styling, custom arrow connections, and the transparent background image overlay. The only minor deviation is the omission of the specific raster icons (checkmarks, phone) used in the video, which have been substituted with text/emoji equivalents for pure programmatic generation.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Do I need to get tested for COVID-19?",
    subtitle_text: str = "Are you experiencing these symptoms?",
    bg_keyword: str = "medical",
    theme_color_light: tuple = (255, 235, 218),  # Light Peach
    theme_color_dark: tuple = (237, 125, 49),   # Vivid Orange
    **kwargs,
) -> str:
    """
    Creates a PPTX file featuring a branching flowchart over a transparent background image.
    """
    import os
    import urllib.request
    from io import BytesIO
    from lxml import etree
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image

    # 1. Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # 2. Generate and Insert Transparent Background
    bg_temp_path = "temp_bg_washed.png"
    try:
        # Fetch image
        url = f"https://source.unsplash.com/random/1920x1080/?{bg_keyword}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img_data = response.read()
        
        # Open and process with PIL
        original_img = Image.open(BytesIO(img_data)).convert("RGBA")
        original_img = original_img.resize((1920, 1080), Image.Resampling.LANCZOS)
        
        # Create a solid white background
        white_bg = Image.new("RGBA", original_img.size, (255, 255, 255, 255))
        
        # Blend the image with white (15% image, 85% white)
        washed_img = Image.blend(white_bg, original_img, alpha=0.15)
        washed_img.save(bg_temp_path)
        
        # Insert as background
        slide.shapes.add_picture(bg_temp_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
    except Exception as e:
        print(f"Failed to fetch or process background image: {e}. Proceeding with plain background.")

    # 3. Add Titles
    title_box = slide.shapes.add_textbox(Inches(1), Inches(0.3), Inches(11.333), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(64, 64, 64)

    sub_box = slide.shapes.add_textbox(Inches(1), Inches(0.9), Inches(11.333), Inches(0.5))
    tf2 = sub_box.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = subtitle_text
    p2.alignment = PP_ALIGN.CENTER
    p2.font.size = Pt(20)
    p2.font.color.rgb = RGBColor(100, 100, 100)

    # 4. Helper Function: Create Flowchart Node
    nodes = {}
    
    def add_node(node_id, text, cx, cy, w, h):
        left = Inches(cx - w/2)
        top = Inches(cy - h/2)
        width = Inches(w)
        height = Inches(h)
        
        # Create Rounded Rectangle
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        
        # Styling
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*theme_color_light)
        shape.line.color.rgb = RGBColor(*theme_color_dark)
        shape.line.width = Pt(1.5)
        
        # Text
        tf = shape.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(64, 64, 64)
        
        # Store connection anchor points
        nodes[node_id] = {
            'top': (Inches(cx), Inches(cy - h/2)),
            'bottom': (Inches(cx), Inches(cy + h/2)),
            'left': (Inches(cx - w/2), Inches(cy)),
            'right': (Inches(cx + w/2), Inches(cy))
        }

    # 5. Build Flowchart Data
    # Top Level
    add_node('symptoms', "☑ Fever      ☑ Shortness of breath      ☑ Coughing", 6.66, 1.8, 7.5, 0.6)
    add_node('call', "📞 Call\nyour Physician", 6.66, 2.8, 2.5, 0.8)

    # Left Branch (Unsure)
    add_node('l1', "Doctor is not sure if there are COVID symptoms & advises you to get checked.", 2.5, 4.2, 3.5, 1.0)
    add_node('l2', "Specimen is collected via swab and send to lab to be tested.", 2.5, 5.5, 3.5, 1.0)
    add_node('l3', "Doctor should have test results within 24 hours.", 2.5, 6.8, 3.5, 0.8)

    # Center Branch (Mild)
    add_node('c1', "Doctor identifies mild symptoms & advised home isolation.", 6.66, 4.2, 3.5, 1.0)
    add_node('c2', "Isolation / stay at home.", 6.66, 5.5, 3.5, 0.8)

    # Right Branch (Severe)
    add_node('r1', "Doctor identifies severe symptoms and advises urgent medical care.", 10.8, 4.2, 3.5, 1.0)
    add_node('r2', "Go to your local hospital.", 10.8, 5.5, 3.5, 0.8)

    # 6. Helper Function: Create Connectors with Arrows via lxml
    def add_arrow(start_node, end_node, start_pos='bottom', end_pos='top'):
        s_pt = nodes[start_node][start_pos]
        e_pt = nodes[end_node][end_pos]
        
        # Add basic straight connector
        connector = slide.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT, s_pt[0], s_pt[1], e_pt[0], e_pt[1]
        )
        
        # Style the line
        connector.line.color.rgb = RGBColor(*theme_color_dark)
        connector.line.width = Pt(2.5)
        
        # Use lxml to inject arrowhead into Open XML
        ln = connector.element.spPr.ln
        if ln is not None:
            tailEnd = etree.SubElement(ln, '{http://schemas.openxmlformats.org/drawingml/2006/main}tailEnd')
            tailEnd.set('type', 'triangle')
            tailEnd.set('w', 'med')
            tailEnd.set('len', 'med')

    # 7. Draw Connections
    add_arrow('symptoms', 'call')
    add_arrow('call', 'l1')
    add_arrow('l1', 'l2')
    add_arrow('l2', 'l3')
    add_arrow('call', 'c1')
    add_arrow('c1', 'c2')
    add_arrow('call', 'r1')
    add_arrow('r1', 'r2')

    # 8. Save & Cleanup
    prs.save(output_pptx_path)
    if os.path.exists(bg_temp_path):
        os.remove(bg_temp_path)
        
    return output_pptx_path
```