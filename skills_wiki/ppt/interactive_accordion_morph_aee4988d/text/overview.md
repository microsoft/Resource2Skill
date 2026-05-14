# Interactive Accordion Morph (水平手风琴平滑展开交互)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Interactive Accordion Morph (水平手风琴平滑展开交互)

* **Core Visual Mechanism**: This design uses the **Accordion Menu** metaphor. It presents content as a series of tightly packed, brightly colored vertical pillars. When a section is "activated" (via transitioning to the next slide), its pillar slides open horizontally, revealing a large background image behind it, while the other pillars compress to the sides. The magic is driven entirely by PowerPoint's **Morph (平滑)** transition seamlessly interpolating the width and X-coordinates of the layers.
* **Why Use This Skill (Rationale)**: It transforms a static bullet-point list or table of contents into an engaging, physical-feeling interactive experience. The vertical typography paired with horizontal motion creates a strong contrasting dynamic. The hidden images create a "reveal" psychological reward.
* **Overall Applicability**: Perfect for Presentation Agendas, Table of Contents (目录), Product Feature showcases, or Portfolio cover pages where 4-6 distinct core pillars need to be highlighted.
* **Value Addition**: Replaces boring list-based menus with a modern, application-like interactive UI. It immediately signals high production value and design maturity.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: A gradient-like progression of 5 solid colors. In the video, it transitions from a warm cream/beige to a dark slate/navy.
    - Cream `(230, 224, 216, 255)`
    - Khaki `(213, 196, 179, 255)`
    - Steel Blue `(118, 142, 166, 255)`
    - Navy Blue `(68, 93, 115, 255)`
    - Slate Black `(34, 46, 61, 255)`
  - **Text Hierarchy**:
    1. Giant Section Number (壹, 贰...) acting as a graphical anchor.
    2. Primary Title, set **vertically** (East Asian vertical typesetting).
    3. Secondary English Title, rotated 270 degrees running bottom-to-top.

* **Step B: Compositional Style**
  - The total accordion width spans roughly 80% of the slide width.
  - When collapsed, a panel is roughly 1-inch wide.
  - When expanded, the revealed image takes up ~45% of the slide width, flanked by the collapsed panels on either side.
  - The panels float in the center of the vertical axis, leaving negative space for a global title at the top.

* **Step C: Dynamic Effects & Transitions**
  - **Morph Transition (平滑切换)**: Matches elements by ID across slides, interpolating their X-position and width.
  - Squeezed images are hidden *behind* the colored panels and smoothly expand outward as the panels physically slide to the right.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Multi-slide layout & shapes** | `python-pptx` native | Required to ensure exact Shape IDs across slides so the Morph transition works flawlessly. |
| **Vertical Text Typesetting** | `lxml` XML injection | `python-pptx` cannot natively set East Asian vertical text flow (`<a:bodyPr vert="eaVert"/>`); XML injection makes it elegant. |
| **Morph Transition Logic** | `lxml` XML injection | The `<p:morph>` transition tag must be injected into each slide's XML definition. |
| **Images** | `urllib` / `PIL` | Downloads high-quality representative photos to make the effect visually stunning out-of-the-box. |

> **Feasibility Assessment**: **95%**. The core visual aesthetic, layout, vertical typography, and Morph transitions are fully reproduced. The only minor deviation is that the user must click space/arrow-keys to navigate between the states rather than clicking specific panels, as embedding programmatic hyperlinks to specific slides via python-pptx is highly complex, but the visual morphing effect is identical.

#### 3b. Complete Reproduction Code

```python
import os
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from lxml import etree
from PIL import Image, ImageDraw

def ensure_image(idx, url):
    """Download image or generate a fallback if download fails."""
    filename = f"accordion_img_{idx}.jpg"
    if not os.path.exists(filename):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                with open(filename, 'wb') as f:
                    f.write(response.read())
        except Exception:
            # Generate dummy image fallback
            img = Image.new('RGB', (800, 600), (40 + idx*15, 50 + idx*15, 60 + idx*15))
            draw = ImageDraw.Draw(img)
            draw.line((0, 0, 800, 600), fill=(200, 200, 200), width=3)
            img.save(filename)
    return filename

def set_vertical_text(text_frame):
    """Inject XML to set East Asian Vertical Text direction."""
    try:
        bodyPr = text_frame._element.find('.//a:bodyPr', namespaces=text_frame._element.nsmap)
        if bodyPr is not None:
            bodyPr.set('vert', 'eaVert')
    except Exception as e:
        pass

def add_morph_transition(slide):
    """Inject XML to add a Morph transition to the slide."""
    try:
        sld_xml = slide._element
        # Remove any existing transition
        transition_list = sld_xml.findall('.//{http://schemas.openxmlformats.org/presentationml/2006/main}transition')
        for t in transition_list:
            sld_xml.remove(t)
        
        # Add Morph transition
        transition = etree.SubElement(sld_xml, '{http://schemas.openxmlformats.org/presentationml/2006/main}transition')
        transition.set('spd', 'slow')
        morph = etree.SubElement(transition, '{http://schemas.microsoft.com/office/powerpoint/2015/09/main}morph')
        morph.set('option', 'byObject')
    except Exception:
        pass

def create_slide(output_pptx_path: str = "Accordion_Morph_Menu.pptx", **kwargs) -> str:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Define Content Data
    panels_data = [
        {"num": "壹", "title": "汽车外观设计", "en": "Automotive exterior design", "bg_color": (230, 224, 216), "text_color": (30, 30, 30), "url": "https://images.unsplash.com/photo-1503376760367-111c1d763321?auto=format&fit=crop&w=800&q=80"},
        {"num": "贰", "title": "汽车功能特点", "en": "Car features", "bg_color": (213, 196, 179), "text_color": (30, 30, 30), "url": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?auto=format&fit=crop&w=800&q=80"},
        {"num": "叁", "title": "产品创新理念", "en": "Product innovation ideas", "bg_color": (118, 142, 166), "text_color": (240, 240, 240), "url": "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=800&q=80"},
        {"num": "肆", "title": "外部宣传渠道", "en": "Communication channels", "bg_color": (68, 93, 115), "text_color": (240, 240, 240), "url": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=800&q=80"},
        {"num": "伍", "title": "相关售后保障", "en": "Relevant after-sales guarantee", "bg_color": (34, 46, 61), "text_color": (240, 240, 240), "url": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=800&q=80"},
    ]
    
    N = len(panels_data)
    
    # Pre-download images
    images = [ensure_image(i, p["url"]) for i, p in enumerate(panels_data)]
    
    # Layout Proportions
    W_acc = 11.0 # Total width of the accordion mechanism
    H_acc = 5.5 # Height of panels and images
    X_offset = (13.333 - W_acc) / 2 # Center horizontally
    Y_offset = 1.2 # Top margin for accordion
    
    w_col = 1.0 # Width of a collapsed panel
    W_exp = W_acc - (N * w_col) # Width of the expanded image (~6 inches)

    # Generate 5 slides, each representing the "Expanded" state of one section
    for active_idx in range(N):
        slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
        add_morph_transition(slide)
        
        # Slide Background (Dark Grey)
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = RGBColor(25, 25, 25)
        
        # Global Title (Static)
        tx_main = slide.shapes.add_textbox(Inches(X_offset), Inches(0.4), Inches(W_acc), Inches(0.6))
        p = tx_main.text_frame.paragraphs[0]
        p.text = "目录 CONTENTS"
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = RGBColor(240, 240, 240)
        
        # 1. ADD IMAGES (Ensuring exactly identical creation order on every slide for Morph)
        for i in range(N):
            # Calculate position based on active state
            if i == active_idx:
                img_left = X_offset + ((i + 1) * w_col)
                img_width = W_exp
            elif i < active_idx:
                img_left = X_offset + (i * w_col)
                img_width = w_col
            else:
                img_left = X_offset + W_acc - ((N - i) * w_col)
                img_width = w_col
                
            # Insert Image (images squashed underneath panels when not active)
            pic = slide.shapes.add_picture(images[i], Inches(img_left), Inches(Y_offset), Inches(img_width), Inches(H_acc))

        # 2. ADD PANELS & TEXT (Identical order)
        for i in range(N):
            # Calculate Panel Position
            if i <= active_idx:
                panel_left = X_offset + (i * w_col)
            else:
                panel_left = X_offset + W_acc - ((N - i) * w_col)
                
            data = panels_data[i]
            r, g, b = data["bg_color"]
            tr, tg, tb = data["text_color"]
            
            # Draw solid color pillar
            rect = slide.shapes.add_shape(
                1, # MSO_SHAPE.RECTANGLE
                Inches(panel_left), Inches(Y_offset), Inches(w_col), Inches(H_acc)
            )
            rect.fill.solid()
            rect.fill.fore_color.rgb = RGBColor(r, g, b)
            rect.line.fill.background() # No line
            
            # --- Text 1: Giant Number ---
            tx_num = slide.shapes.add_textbox(Inches(panel_left), Inches(Y_offset + 0.1), Inches(w_col), Inches(1.0))
            p_num = tx_num.text_frame.paragraphs[0]
            p_num.text = data["num"]
            p_num.alignment = PP_ALIGN.CENTER
            p_num.font.size = Pt(44)
            p_num.font.bold = True
            p_num.font.name = "SimSun"
            p_num.font.color.rgb = RGBColor(tr, tg, tb)
            tx_num.text_frame.margin_left = 0
            tx_num.text_frame.margin_right = 0
            
            # --- Text 2: Vertical Title ---
            tx_title = slide.shapes.add_textbox(Inches(panel_left), Inches(Y_offset + 1.2), Inches(w_col), Inches(2.2))
            p_title = tx_title.text_frame.paragraphs[0]
            p_title.text = data["title"]
            p_title.alignment = PP_ALIGN.CENTER
            p_title.font.size = Pt(16)
            p_title.font.bold = True
            p_title.font.color.rgb = RGBColor(tr, tg, tb)
            set_vertical_text(tx_title.text_frame) # Apply XML hack
            
            # --- Text 3: Rotated English Subtitle ---
            # Create a box wider than the pillar to allow text to fit before rotation
            tx_en = slide.shapes.add_textbox(Inches(panel_left - 0.5), Inches(Y_offset + H_acc - 1.5), Inches(2.0), Inches(0.5))
            tx_en.rotation = 270 # Rotate bottom-to-top
            p_en = tx_en.text_frame.paragraphs[0]
            p_en.text = data["en"]
            p_en.alignment = PP_ALIGN.CENTER
            p_en.font.size = Pt(10)
            p_en.font.color.rgb = RGBColor(tr, tg, tb)

    prs.save(output_pptx_path)
    return output_pptx_path
```