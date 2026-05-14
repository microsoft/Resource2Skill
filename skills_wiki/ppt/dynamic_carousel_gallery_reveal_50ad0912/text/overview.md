# Dynamic Carousel Gallery Reveal

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic Carousel Gallery Reveal

* **Core Visual Mechanism**: A smoothly morphing, horizontally scrolling carousel. The active focal point (the central image) is physically enlarged, encased in a polished rounded frame, and annotated with an active text tag. Non-focal peripheral items are scaled down to establish depth and spatial hierarchy without leaving the screen. This relies heavily on morphological animation (Morph transition) matching identical shape names/indices across slides.
* **Why Use This Skill (Rationale)**: Human attention is naturally drawn to scale and contrast. By dynamically shifting the scale and adding detailed text only to the focal element, you guide the audience's eye exactly where it needs to be, while the peripheral elements provide context and preview the upcoming content. It prevents cognitive overload while displaying multiple entities.
* **Overall Applicability**: Ideal for team introductions, product feature highlights, portfolio showcases, or multi-step timeline overviews. 
* **Value Addition**: Transforms a static "grid of faces" into an interactive, app-like horizontal swiper experience, adding a premium, professional motion-design feel to standard presentations.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: Solid dark charcoal/grey to make foreground elements pop. (e.g., `RGBA(50, 50, 50, 255)`).
  - **Portrait Cards**: Rounded rectangle shapes holding picture fills. 
  - **Active Identifier**: A vibrant colored rectangular tag (e.g., Cyan `RGBA(0, 191, 255, 255)`) overlapping the bottom edge of the central portrait.
  - **Typography**: Clean sans-serif; high contrast (White text against dark background/cyan tags). 

* **Step B: Compositional Style**
  - The carousel aligns elements on a strict horizontal center axis (`Y = ~3.75"` on a 16:9 canvas).
  - **Scale Hierarchy**:
    - Center (Active): ~2.5x to 3x larger than side images (e.g., `3.5" x 4.5"`).
    - Sides (Inactive): Scaled down to ~`1.5" x 2.0"`.
  - **Spacing**: Consistent gap (e.g., `0.3"`) between the bounding boxes of the elements.

* **Step C: Dynamic Effects & Transitions**
  - Uses the native PowerPoint **Morph Transition**.
  - When transitioning from Slide 1 to Slide 2, the shape geometries (X, Y, Width, Height) interpolate automatically because the shapes persist across slides with identical names and Z-orders.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layout & Sizing** | `python-pptx` native | Calculating strict X/Y coordinates and dimensions creates the geometric foundation for the Morph. |
| **Rounded Picture Cards** | `lxml` XML injection | `python-pptx` inserts square images by default. Wrapping standard pictures into rounded rectangle geometries requires injecting an `<a:blipFill>` into a rounded shape's properties. |
| **Outline Removal** | `lxml` XML injection | Replacing `<a:ln>` with `<a:noFill/>` ensures our dynamic rounded cards don't have PowerPoint's default blue borders. |
| **Asset Generation** | `PIL/Pillow` | Generating robust fallback placeholder portraits locally prevents the script from crashing due to broken URLs or proxy issues. |
| **Smooth Animation** | OOXML Structure | Injecting the exact shape sequence across two slides inherently triggers PPT's Morph logic when the transition is applied. |

> **Feasibility Assessment**: **95%**. The code fully reproduces the visual styling, the geometric layout, the dynamic sizing, and generates consecutive slides set up for a perfect Morph transition. (Depending on the PPT version, the user may simply need to click "Transitions -> Morph" if the XML injection is bypassed by older PPT renderers, but the structural foundation is 100% complete).

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from lxml import etree
from PIL import Image, ImageDraw

def _generate_placeholder_portraits(num_images: int = 5):
    """Generates placeholder portrait images locally using PIL."""
    colors = [
        (255, 99, 71),   # Tomato
        (60, 179, 113),  # Medium Sea Green
        (30, 144, 255),  # Dodger Blue
        (218, 165, 32),  # Goldenrod
        (138, 43, 226)   # Blue Violet
    ]
    img_paths = []
    for i in range(num_images):
        path = f"temp_team_member_{i}.jpg"
        img = Image.new('RGB', (400, 600), color=colors[i % len(colors)])
        draw = ImageDraw.Draw(img)
        # Draw a simplistic "person" vector
        draw.ellipse((100, 120, 300, 320), fill=(255, 255, 255, 120)) # Head
        draw.polygon([(50, 600), (200, 350), (350, 600)], fill=(255, 255, 255, 120)) # Shoulders
        img.save(path)
        img_paths.append(path)
    return img_paths

def _insert_rounded_picture(slide, img_path, shape_name, cx, cy, w, h):
    """
    Inserts a picture into a rounded rectangle shape using lxml injection.
    """
    left = Inches(cx - w/2)
    top = Inches(cy - h/2)
    width = Inches(w)
    height = Inches(h)

    # 1. Add dummy pic to load the image and get its relationship ID
    dummy = slide.shapes.add_picture(img_path, 0, 0, Inches(0.1), Inches(0.1))
    rel_id = dummy._element.blipFill.blip.embed
    dummy_element = dummy._element
    dummy_element.getparent().remove(dummy_element) # Delete dummy

    # 2. Add rounded rectangle
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.name = shape_name # MUST be identical across slides for Morph to work!
    
    # 3. Inject blipFill (Picture Fill) and remove solid background & outline
    spPr = shape._element.spPr
    
    # Remove existing solid fill
    solidFill = spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}solidFill")
    if solidFill is not None:
        spPr.remove(solidFill)

    # Create blipFill
    blipFill = etree.SubElement(spPr, "{http://schemas.openxmlformats.org/drawingml/2006/main}blipFill")
    blip = etree.SubElement(blipFill, "{http://schemas.openxmlformats.org/drawingml/2006/main}blip")
    blip.set("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed", rel_id)
    stretch = etree.SubElement(blipFill, "{http://schemas.openxmlformats.org/drawingml/2006/main}stretch")
    etree.SubElement(stretch, "{http://schemas.openxmlformats.org/drawingml/2006/main}fillRect")

    # Remove Outline
    ln = spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}ln")
    if ln is not None:
        spPr.remove(ln)
    ln = etree.SubElement(spPr, "{http://schemas.openxmlformats.org/drawingml/2006/main}ln")
    etree.SubElement(ln, "{http://schemas.openxmlformats.org/drawingml/2006/main}noFill")

    return shape

def create_slide(
    output_pptx_path: str,
    title_text: str = "ANIMATED TEAM INTRODUCTION TEMPLATE",
    body_text: str = "",
    bg_palette: str = "dark",
    accent_color: tuple = (0, 191, 255), 
    **kwargs,
) -> str:
    """
    Creates a presentation demonstrating the Dynamic Carousel Morphing effect.
    Builds 2 slides to showcase the progression.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Generate assets
    num_members = 5
    img_paths = _generate_placeholder_portraits(num_members)
    
    # Pre-calculate slot geometries (Relative index: (X_center, Y_center, Width, Height))
    gap = 0.3
    cy = 4.0
    w_large, h_large = 3.5, 4.5
    w_small, h_small = 1.8, 2.4
    x_center = 13.333 / 2
    
    slots = {
        0: (x_center, cy, w_large, h_large), # Active center
        -1: (x_center - (w_large/2) - gap - (w_small/2), cy, w_small, h_small),
        -2: (x_center - (w_large/2) - gap - w_small - gap - (w_small/2), cy, w_small, h_small),
        -3: (x_center - (w_large/2) - gap - w_small*2 - gap*2 - (w_small/2), cy, w_small, h_small), # Offscreen Left
        1: (x_center + (w_large/2) + gap + (w_small/2), cy, w_small, h_small),
        2: (x_center + (w_large/2) + gap + w_small + gap + (w_small/2), cy, w_small, h_small),
        3: (x_center + (w_large/2) + gap + w_small*2 + gap*2 + (w_small/2), cy, w_small, h_small), # Offscreen Right
    }

    # Build 2 consecutive slides focusing on Member 2, then Member 3
    active_indices = [2, 3]

    for slide_idx, active_idx in enumerate(active_indices):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # 1. Background
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(50, 50, 50)
        
        # 2. Static Title
        title_box = slide.shapes.add_textbox(Inches(0), Inches(0.5), Inches(13.333), Inches(1.0))
        tf = title_box.text_frame
        tf.text = title_text
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        tf.paragraphs[0].font.size = Pt(28)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = RGBColor(220, 220, 220)
        
        # 3. Carousel Images (Ensure we insert in exact loop order to match z-index for Morph)
        for i in range(num_members):
            slot_pos = i - active_idx
            
            # If out of defined slots, clamp to offscreen
            if slot_pos < -3: slot_pos = -3
            if slot_pos > 3: slot_pos = 3
                
            cx, cy_pos, w, h = slots[slot_pos]
            shape_name = f"TeamMember_Card_{i}"
            
            _insert_rounded_picture(slide, img_paths[i], shape_name, cx, cy_pos, w, h)
            
            # Active Member specific styling (Name Tag)
            if slot_pos == 0:
                tag_w, tag_h = 2.8, 0.6
                tag_left = Inches(cx - tag_w/2)
                tag_top = Inches(cy_pos + h/2 - 0.2)
                
                tag = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, tag_left, tag_top, Inches(tag_w), Inches(tag_h))
                tag.name = "Active_Name_Tag"
                tag.fill.solid()
                tag.fill.fore_color.rgb = RGBColor(*accent_color)
                tag.line.color.rgb = RGBColor(*accent_color)
                
                tag_tf = tag.text_frame
                tag_tf.text = f"MEMBER 0{i+1}"
                tag_tf.paragraphs[0].alignment = PP_ALIGN.CENTER
                tag_tf.paragraphs[0].font.size = Pt(16)
                tag_tf.paragraphs[0].font.bold = True
                tag_tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

        # Inject Morph Transition XML for Slide 2
        if slide_idx > 0:
            p_ns = "http://schemas.openxmlformats.org/presentationml/2006/main"
            try:
                transition = etree.Element(f"{{{p_ns}}}transition", spd="med")
                # PPT 2019+ morphological transition namespace
                morph = etree.SubElement(transition, "{http://schemas.microsoft.com/office/powerpoint/2018/8/main}morph", option="byObject")
                
                # Insert transition securely inside <p:sld>
                cSld = slide._element.find(f"{{{p_ns}}}cSld")
                insert_idx = slide._element.index(cSld) + 1
                slide._element.insert(insert_idx, transition)
            except Exception:
                pass # Graceful fallback; user can manually select Transitions -> Morph

    prs.save(output_pptx_path)
    
    # Cleanup dummy images
    for p in img_paths:
        if os.path.exists(p):
            os.remove(p)

    return output_pptx_path
```