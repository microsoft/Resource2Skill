# Clean Corporate Software Demo Slide

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Clean Corporate Software Demo Slide

* **Core Visual Mechanism**: A structured, asymmetrical split layout (text on the left, technical hero graphic on the right) that presents technical value propositions clearly, anchored by a persistent, tripartite branded footer.
* **Why Use This Skill (Rationale)**: In software demos, IT architecture presentations, or training videos, viewers need to quickly understand the *what* and *why* before the actual demonstration begins. This layout avoids clutter, cleanly separating the narrative context from the visual evidence, which minimizes cognitive overload.
* **Overall Applicability**: Title slides and closing slides for screencasts, technical webinars, product training videos, and corporate IT utility showcases.
* **Value Addition**: Elevates standard bullet-point slides into a professional corporate format, establishing authority and maintaining brand presence without distracting from the main technical message.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: Minimalist solid white `(255, 255, 255, 255)`.
  - **Typography**: Clean sans-serif hierarchy. Title in bold black `(0, 0, 0)`, body text in dark grey `(51, 51, 51)` to reduce contrast fatigue, and metadata/presenter info in lighter grey `(85, 85, 85)`.
  - **Graphic**: Right-aligned technical diagram (e.g., a network topology) utilizing corporate accent colors like blue `(52, 152, 219)`.
  - **Footer**: A consistent tripartite footer containing legal/trademark text on the left, a URL in the center, and a company logo on the right.

* **Step B: Compositional Style**
  - The canvas uses a roughly 55/45 horizontal split.
  - The left content block maintains a strict 1.0-inch margin, creating a strong vertical reading line.
  - The footer forms a stable visual base occupying the bottom 10% of the slide height, aligned cleanly along a horizontal axis.

* **Step C: Dynamic Effects & Transitions**
  - Static layout designed for high legibility during a video introduction or conclusion. In practice, a subtle "Fade" transition is often applied when moving into the live demo screen.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Text layout and typography | `python-pptx` native | Provides precise positioning, word wrapping, and font styling for corporate text blocks. |
| Technical diagram mock | `PIL/Pillow` | Can procedurally generate a placeholder network topology diagram with nodes and edges that fits the technical theme. |
| Footer logo mock | `PIL/Pillow` | Can dynamically draw a stylized corporate logo placeholder. |

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw, ImageFont

def _generate_network_diagram(path: str):
    """Generates a mock network topology diagram using PIL."""
    img = Image.new('RGBA', (800, 600), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Define network nodes (x, y)
    nodes = {
        'Core1': (400, 100),
        'Dist1': (200, 300),
        'Dist2': (600, 300),
        'Access1': (300, 500),
        'Access2': (500, 500)
    }
    # Define links between nodes
    edges = [('Core1', 'Dist1'), ('Core1', 'Dist2'), 
             ('Dist1', 'Access1'), ('Dist1', 'Access2'), 
             ('Dist2', 'Access2')]
    
    # Draw links
    for u, v in edges:
        draw.line([nodes[u], nodes[v]], fill=(180, 180, 180, 255), width=4)
        
    # Draw stylized switch icons (blue box with a star/asterisk inside)
    for name, (x, y) in nodes.items():
        draw.rectangle([x-50, y-40, x+50, y+40], fill=(52, 152, 219, 255), outline=(41, 128, 185, 255), width=3)
        # Draw asterisk to represent a network switch
        draw.line([x-25, y-15, x+25, y+15], fill=(255, 255, 255, 255), width=3)
        draw.line([x-25, y+15, x+25, y-15], fill=(255, 255, 255, 255), width=3)
        draw.line([x, y-25, x, y+25], fill=(255, 255, 255, 255), width=3)
        draw.line([x-25, y, x+25, y], fill=(255, 255, 255, 255), width=3)
        
    img.save(path)

def _generate_logo(path: str):
    """Generates a simple corporate logo mock using PIL."""
    img = Image.new('RGBA', (300, 100), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw geometric icon
    draw.rectangle([10, 10, 90, 90], fill=(52, 152, 219, 255), outline=(41, 128, 185, 255), width=4)
    draw.rectangle([30, 30, 70, 70], fill=(255, 255, 255, 255))
    
    # Draw text
    try:
        font = ImageFont.truetype("arialbd.ttf", 36)
    except IOError:
        font = ImageFont.load_default()
        
    draw.text((110, 15), "SQUARE", fill=(0, 0, 0, 255), font=font)
    draw.text((110, 55), "MILE", fill=(0, 0, 0, 255), font=font)
    img.save(path)

def create_slide(
    output_pptx_path: str,
    title_text: str = "Intelligent Network Connector",
    body_text: str = "This video shows you how\nthe intelligent network\nconnector Visio shape\nmakes network diagrams\nmuch quicker and easier.",
    presenter_name: str = "Robert Cowham",
    presenter_title: str = "Services Director",
    company_url: str = "www.squaremilesystems.com",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Clean Corporate Software Demo Slide layout.
    
    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # === Layer 1: Background ===
    # Using default white slide background.

    # === Layer 2: Left Pane Text Block ===
    # Title
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(5.5), Inches(1.0))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.name = "Arial"
    p.font.color.rgb = RGBColor(0, 0, 0)

    # Body Subtitle/Value Proposition
    body_box = slide.shapes.add_textbox(Inches(1.0), Inches(2.8), Inches(5.5), Inches(2.0))
    tf = body_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = body_text
    p.font.size = Pt(24)
    p.font.name = "Arial"
    p.font.color.rgb = RGBColor(51, 51, 51)
    
    # Presenter Information
    pres_box = slide.shapes.add_textbox(Inches(1.0), Inches(5.2), Inches(5.5), Inches(1.0))
    tf = pres_box.text_frame
    p1 = tf.paragraphs[0]
    p1.text = presenter_name
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.name = "Arial"
    p1.font.color.rgb = RGBColor(0, 0, 0)
    
    p2 = tf.add_paragraph()
    p2.text = presenter_title
    p2.font.size = Pt(16)
    p2.font.name = "Arial"
    p2.font.color.rgb = RGBColor(85, 85, 85)

    # === Layer 3: Right Pane Hero Graphic ===
    img_path = "temp_network_diagram.png"
    _generate_network_diagram(img_path)
    # Position in the right half of the slide
    slide.shapes.add_picture(img_path, Inches(7.0), Inches(1.5), width=Inches(5.0))
    if os.path.exists(img_path):
        os.remove(img_path)

    # === Layer 4: Tripartite Footer ===
    # Left: Trademark/Legal text
    foot_left = slide.shapes.add_textbox(Inches(1.0), Inches(7.0), Inches(3.0), Inches(0.4))
    p = foot_left.text_frame.paragraphs[0]
    p.text = "All trademarks acknowledged"
    p.font.size = Pt(10)
    p.font.name = "Arial"
    p.font.color.rgb = RGBColor(119, 119, 119)

    # Center: URL
    foot_center = slide.shapes.add_textbox(Inches(4.5), Inches(7.0), Inches(4.33), Inches(0.4))
    p = foot_center.text_frame.paragraphs[0]
    p.text = company_url
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(14)
    p.font.name = "Arial"
    p.font.color.rgb = RGBColor(0, 0, 0)

    # Right: Company Logo
    logo_path = "temp_logo.png"
    _generate_logo(logo_path)
    slide.shapes.add_picture(logo_path, Inches(10.5), Inches(6.8), height=Inches(0.5))
    if os.path.exists(logo_path):
        os.remove(logo_path)

    prs.save(output_pptx_path)
    return output_pptx_path
```