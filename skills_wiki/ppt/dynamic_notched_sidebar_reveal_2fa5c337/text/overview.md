# Dynamic Notched Sidebar Reveal

## Analysis

An analysis of the provided tutorial reveals a highly modern and effective presentation design pattern. The tutorial demonstrates how to build a dynamic, morphing sidebar navigation menu combined with a hub-and-spoke radial diagram. 

Here is the extraction of this design style and the code to reproduce it automatically.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic Notched Sidebar Reveal

* **Core Visual Mechanism**: A flat, vibrant background is juxtaposed against a persistent, pure white sidebar on the left. The defining feature is a smooth, Bezier-like "notch" or "cutout" scooped out of the sidebar's edge. This notch physically engulfs the active menu icon, exposing the background color beneath it. When transitioned using PowerPoint's "Morph" feature, this notch seamlessly glides up and down the sidebar like a physical track.
* **Why Use This Skill (Rationale)**: Traditional sidebars consume space and can feel detached from the content. By physically "cutting into" the sidebar, you create a Gestalt principle of continuity—the navigation and the canvas become one connected layer. It immediately anchors the viewer's eye to the current section without requiring heavy text highlights.
* **Overall Applicability**: Perfect for multi-chapter presentations, interactive dashboards, course modules, agenda slides, or product feature breakdowns. 
* **Value Addition**: Transforms a standard bullet-point list into an app-like user interface. It elevates the perceived production value of the deck, making it feel engineered rather than merely drafted.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: Solid, flat, vibrant tones. The contrast between the white sidebar and the background is crucial. Example: Magenta/Pink `(216, 68, 100, 255)`.
  - **Sidebar**: Pure white `(255, 255, 255, 255)`.
  - **Icons/Content**: Thin, minimalist line-art style. White lines on the colored background, and dark grey `(80, 80, 80)` lines for inactive items sitting on the white sidebar.
* **Step B: Compositional Style**
  - **Navigation Zone**: Occupies the left 15-20% of the horizontal real estate.
  - **Content Zone**: The remaining 80% utilizes a radial (hub-and-spoke) layout, anchoring a central "core idea" in the middle, branching out to sub-points in the four corners.
* **Step C: Dynamic Effects & Transitions**
  - The true magic happens using the **Morph transition** between consecutive slides. The cutout physically travels vertically to align with the new active item, while the background color fades to a new theme color.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Smooth Cutout Sidebar** | `PIL/Pillow` (Mask generation) | PowerPoint's native boolean shape operations (Subtract/Merge) cannot programmatically generate the mathematically perfect, smooth, C1-continuous Bezier curve needed for the notch edge via `python-pptx` natively. PIL handles this geometry flawlessly. |
| **Hub-and-Spoke Layout** | `python-pptx` native shapes | Standard shapes, text boxes, and connector lines are perfect for building the radial diagram robustly. |
| **Monochromatic Icons** | `python-pptx` native shapes | Using basic geometry (circles/rings) to simulate the clean outline aesthetic of the icons. |

> **Feasibility Assessment**: 95% of the visual layout is reproduced. The remaining 5% involves manually turning on the "Morph" transition in PowerPoint (which cannot be enabled directly via `python-pptx`, but the geometry created is perfectly structured to support it if you duplicate the generated slide).

#### 3b. Complete Reproduction Code

```python
import os
import math
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN

def create_slide(
    output_pptx_path: str = "Notched_Sidebar_Layout.pptx",
    bg_color: tuple = (216, 68, 100), # Vibrant Pink/Magenta
    active_index: int = 1,            # 0 to 3 (which menu item is currently selected)
) -> str:
    """
    Creates a PPTX file reproducing the 'Dynamic Notched Sidebar' visual effect.
    """
    prs = Presentation()
    # Set 16:9 Aspect Ratio
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide

    # === Layer 1: Solid Background ===
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # === Layer 2: Generate Notched Sidebar via PIL ===
    # Math to create a perfectly smooth, bell-shaped curved notch
    dpi = 120
    img_h = int(7.5 * dpi)
    img_w = int(2.0 * dpi) # 2 inches wide
    
    notch_depth = int(0.5 * dpi)
    notch_height = int(1.6 * dpi)
    base_w = img_w - notch_depth
    
    # Calculate Y positions for 4 menu items
    menu_spacing = img_h / 5
    active_y = int((active_index + 1) * menu_spacing)

    # Create PIL Image
    sidebar_img = Image.new('RGBA', (img_w, img_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(sidebar_img)
    points = [(0, 0)]
    
    # Generate smooth edge curve
    for y in range(img_h):
        if abs(y - active_y) <= notch_height / 2:
            # Normalized theta from -pi to pi
            theta = (y - active_y) / (notch_height / 2) * math.pi
            # Smooth cosine interpolation (derivative is 0 at both center and edges)
            offset = notch_depth * (1 + math.cos(theta)) / 2
            x = base_w - offset
        else:
            x = base_w
        points.append((x, y))
        
    points.append((0, img_h))
    draw.polygon(points, fill=(255, 255, 255, 255))
    
    # Save and Insert Sidebar
    temp_sidebar = "temp_sidebar_mask.png"
    sidebar_img.save(temp_sidebar)
    slide.shapes.add_picture(temp_sidebar, 0, 0, width=Inches(2.0), height=Inches(7.5))
    os.remove(temp_sidebar)

    # === Layer 3: Navigation Menu Icons ===
    for i in range(4):
        item_y = (i + 1) * (7.5 / 5)
        is_active = (i == active_index)
        
        # Icon position (X shifts slightly right if active to sit inside the notch)
        icon_x = 1.3 if is_active else 0.75
        icon_size = 0.5
        
        # Draw placeholder circle for icon
        icon = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            Inches(icon_x - icon_size/2), Inches(item_y - icon_size/2), 
            Inches(icon_size), Inches(icon_size)
        )
        icon.fill.background() if is_active else icon.fill.solid()
        if not is_active:
            icon.fill.fore_color.rgb = RGBColor(240, 240, 240)
            
        icon.line.color.rgb = RGBColor(255, 255, 255) if is_active else RGBColor(150, 150, 150)
        icon.line.width = Pt(2.5)

    # === Layer 4: Content Layout (Hub and Spoke) ===
    content_center_x = 2.0 + (13.333 - 2.0) / 2  # Center of remaining space
    content_center_y = 3.75

    # Main Slide Title
    title_box = slide.shapes.add_textbox(Inches(content_center_x - 3), Inches(0.5), Inches(6), Inches(1))
    tf = title_box.text_frame
    tf.text = "BUSINESS IDEA"
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(40)
    tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

    # Central Hub
    hub_size = 2.8
    hub = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, 
        Inches(content_center_x - hub_size/2), Inches(content_center_y - hub_size/2), 
        Inches(hub_size), Inches(hub_size)
    )
    hub.fill.background()
    hub.line.color.rgb = RGBColor(255, 255, 255)
    hub.line.width = Pt(4)
    
    # Hub Text
    hub_tf = hub.text_frame
    hub_tf.text = "CORE\nCONCEPT"
    hub_tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    hub_tf.paragraphs[0].font.bold = True
    hub_tf.paragraphs[0].font.size = Pt(24)
    hub_tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

    # Spokes (Corners)
    spoke_coords = [
        (4.5, 2.0, "IDEA 1"),
        (10.8, 2.0, "IDEA 3"),
        (4.5, 6.0, "IDEA 2"),
        (10.8, 6.0, "IDEA 4")
    ]

    for sx, sy, title in spoke_coords:
        # Spoke Icon Placeholder
        spoke_icon = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            Inches(sx - 0.4), Inches(sy - 0.4), 
            Inches(0.8), Inches(0.8)
        )
        spoke_icon.fill.background()
        spoke_icon.line.color.rgb = RGBColor(255, 255, 255)
        spoke_icon.line.width = Pt(2)

        # Connector Line
        connector = slide.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT, 
            Inches(content_center_x), Inches(content_center_y), 
            Inches(sx), Inches(sy)
        )
        connector.line.color.rgb = RGBColor(255, 255, 255)
        connector.line.width = Pt(1.5)
        # Send connector to back so it sits behind the circles
        slide.shapes._spTree.insert(2, connector._element)

        # Spoke Text
        tb = slide.shapes.add_textbox(Inches(sx - 1.5), Inches(sy + 0.5), Inches(3), Inches(1))
        tf = tb.text_frame
        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.bold = True
        p1.font.size = Pt(18)
        p1.font.color.rgb = RGBColor(255, 255, 255)
        p1.alignment = PP_ALIGN.CENTER
        
        p2 = tf.add_paragraph()
        p2.text = "Insert secondary\ndetails here"
        p2.font.size = Pt(12)
        p2.font.color.rgb = RGBColor(255, 255, 255)
        p2.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx_path)
    return output_pptx_path

if __name__ == "__main__":
    create_slide()
```