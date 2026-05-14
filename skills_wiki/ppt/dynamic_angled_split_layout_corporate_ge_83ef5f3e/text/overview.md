# Dynamic Angled Split Layout (Corporate Geometric Identity)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic Angled Split Layout (Corporate Geometric Identity)

* **Core Visual Mechanism**: The defining signature of this style is the use of **sharp, angled geometric polygons** to divide the canvas into distinct, contrasting zones. Rather than relying on standard vertical or horizontal grids, the slanted division line creates a sense of forward momentum and kinetic energy. The layout pairs a heavy, bold branding block (solid color) on one side with a lighter, structured information block on the other, bridged by a secondary dark accent shape that balances the visual weight.

* **Why Use This Skill (Rationale)**: Angled splits disrupt the inherent blockiness of a screen. They guide the viewer's eye diagonally across the layout, forcing active engagement rather than passive scanning. The strict separation of color zones creates a powerful visual hierarchy: the brand identity owns the heavy color block, while the critical data owns the clean, high-contrast whitespace. 

* **Overall Applicability**: This technique is ideal for **Title Slides**, **Contact Us pages**, **Team Member Profiles**, and **Digital Business Cards**. It fits perfectly within modern B2B, tech, and consulting contexts where a clean but assertive corporate identity is required.

* **Value Addition**: Transforms a basic list of contact details or introductory text into a striking, branded visual asset. It achieves a highly professional, bespoke agency look using purely native, lightweight vector shapes without relying on heavy external images.

---

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Flat Geometric Polygons**: Custom freeform shapes with specific angled edges.
  - **Color Logic**: A high-contrast tri-color palette.
    - Brand Accent: Bold Corporate Red `(200, 16, 46)`
    - Secondary Heavy Accent: Deep Black `(0, 0, 0)`
    - Canvas/Information Base: Crisp White `(255, 255, 255)`
  - **Iconography**: Geometric containers (hexagons or circles) utilized as bullet points to anchor contact information.
  - **Text Hierarchy**: Bold, large typography (white on dark backgrounds) for branding and names; smaller, standard-weight text (dark grey/black on white) for detailed information.

* **Step B: Compositional Style**
  - **The Split**: The canvas is split roughly 40/60. The left side (40%) anchors the branding in a heavy red block. The right side (60%) breathes with whitespace for readability.
  - **The Gap**: A calculated, uniform gap (whitespace) separates the red branding block from the black header block, enforcing the diagonal motion and keeping shapes distinct.
  - **Right-Alignment**: Contact information is right-aligned against the right-hand edge, anchoring the text to the geometric icons and balancing the heavy left side.

* **Step C: Dynamic Effects & Transitions**
  - This is fundamentally a static composition. However, "Fly In" or "Wipe" animations (from left and right respectively) can be applied natively in PowerPoint to have the heavy color blocks slide into place.

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Angled Geometric Blocks** | `python-pptx` (FreeformBuilder) | Standard shapes don't easily allow arbitrary angled polygons. `FreeformBuilder` allows us to define precise mathematical vertices for the slanted edges, ensuring perfect parallelism and a crisp vector finish that remains editable. |
| **Hexagonal Icons** | `python-pptx` native shapes | Standard `MSO_SHAPE.HEXAGON` shapes perfectly serve as the contact bullet points. |
| **Text & Layout** | `python-pptx` native | Straightforward text box placement, utilizing specific alignments (`PP_ALIGN.RIGHT`) to recreate the structured typography. |

> **Feasibility Assessment**: 100%. Because this design relies entirely on flat vector geometry and structured typography, the provided `python-pptx` code will natively and perfectly reproduce the exact aesthetic, layout, and visual weight of the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    brand_name: str = "MY BUSINESS",
    person_name: str = "JOHN DOE",
    person_title: str = "Business Owner",
    brand_color: tuple = (200, 16, 46),  # Bold Red
    accent_color: tuple = (0, 0, 0),     # Black
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Dynamic Angled Split Layout effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank slide layout
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)

    # ======================================================
    # Layer 1: Left Branding Block (Angled Red Polygon)
    # ======================================================
    # Geometry: Starts at x=0, goes to x=4.0 at top, slants to x=5.5 at bottom
    ff_red = slide.shapes.build_freeform(0, 0)
    ff_red.add_line_segments([
        (Inches(4.0), 0),
        (Inches(5.5), Inches(7.5)),
        (0, Inches(7.5)),
        (0, 0)
    ])
    red_shape = ff_red.convert_to_shape()
    red_shape.fill.solid()
    red_shape.fill.fore_color.rgb = RGBColor(*brand_color)
    red_shape.line.fill.background() # Remove border

    # ======================================================
    # Layer 2: Top Right Header Block (Angled Black Polygon)
    # ======================================================
    # Geometry: Parallel to the red shape, creating a 0.2 inch visual gap.
    # Red edge equation: x = 4.0 + (1.5/7.5)*y = 4.0 + 0.2*y
    # Black edge start: x = 4.2 + 0.2*y
    # At y=0, x=4.2. At y=2.5, x=4.2 + 0.5 = 4.7
    ff_black = slide.shapes.build_freeform(Inches(4.2), 0)
    ff_black.add_line_segments([
        (Inches(13.333), 0),
        (Inches(13.333), Inches(2.5)),
        (Inches(4.7), Inches(2.5)),
        (Inches(4.2), 0)
    ])
    black_shape = ff_black.convert_to_shape()
    black_shape.fill.solid()
    black_shape.fill.fore_color.rgb = RGBColor(*accent_color)
    black_shape.line.fill.background()

    # ======================================================
    # Layer 3: Branding & Logo (Left Side)
    # ======================================================
    # Logo Placeholder
    logo = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(1.5), Inches(1.5), Inches(1.5), Inches(1.5)
    )
    logo.fill.solid()
    logo.fill.fore_color.rgb = RGBColor(255, 255, 255)
    logo.line.fill.background()
    logo.text_frame.text = "LOGO"
    logo.text_frame.paragraphs[0].font.color.rgb = RGBColor(*brand_color)
    logo.text_frame.paragraphs[0].font.bold = True
    logo.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    logo.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE

    # Brand Name Text
    tb_brand = slide.shapes.add_textbox(Inches(0.5), Inches(3.2), Inches(3.5), Inches(1.5))
    p_brand = tb_brand.text_frame.paragraphs[0]
    p_brand.text = brand_name
    p_brand.font.bold = True
    p_brand.font.size = Pt(40)
    p_brand.font.color.rgb = RGBColor(255, 255, 255)
    p_brand.alignment = PP_ALIGN.CENTER

    # ======================================================
    # Layer 4: Personal / Section Info (Top Right)
    # ======================================================
    tb_name = slide.shapes.add_textbox(Inches(6.0), Inches(0.5), Inches(6.8), Inches(1.5))
    
    p_name = tb_name.text_frame.paragraphs[0]
    p_name.text = person_name
    p_name.font.bold = True
    p_name.font.size = Pt(36)
    p_name.font.color.rgb = RGBColor(255, 255, 255)
    p_name.alignment = PP_ALIGN.RIGHT

    p_title = tb_name.text_frame.add_paragraph()
    p_title.text = person_title
    p_title.font.size = Pt(20)
    p_title.font.color.rgb = RGBColor(200, 200, 200)
    p_title.alignment = PP_ALIGN.RIGHT

    # ======================================================
    # Layer 5: Contact Information List (Bottom Right)
    # ======================================================
    contact_data = [
        ("123 Business Road, Corporate District, 90210", "A"), # Address
        ("+1 (555) 123-4567", "P"),                           # Phone
        ("contact@mybusiness.com", "E"),                      # Email
        ("www.mybusiness.com", "W")                           # Web
    ]
    
    start_y = 3.2
    spacing = 0.85
    
    for i, (text, icon) in enumerate(contact_data):
        y_pos = Inches(start_y + (i * spacing))
        
        # Hexagon Icon Container
        hex_shape = slide.shapes.add_shape(
            MSO_SHAPE.HEXAGON, Inches(12.0), y_pos, Inches(0.6), Inches(0.6)
        )
        hex_shape.fill.solid()
        hex_shape.fill.fore_color.rgb = RGBColor(*brand_color)
        hex_shape.line.fill.background()
        
        # Simple text acting as icon placeholder inside Hexagon
        tf = hex_shape.text_frame
        tf.text = icon
        p_icon = tf.paragraphs[0]
        p_icon.font.color.rgb = RGBColor(255, 255, 255)
        p_icon.font.bold = True
        p_icon.font.size = Pt(14)
        p_icon.alignment = PP_ALIGN.CENTER
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE

        # Contact Details Text Box (Right aligned next to hexagon)
        tb_contact = slide.shapes.add_textbox(Inches(5.5), y_pos + Inches(0.05), Inches(6.3), Inches(0.5))
        p_contact = tb_contact.text_frame.paragraphs[0]
        p_contact.text = text
        p_contact.font.size = Pt(18)
        p_contact.font.color.rgb = RGBColor(40, 40, 40)
        p_contact.alignment = PP_ALIGN.RIGHT

    prs.save(output_pptx_path)
    return output_pptx_path
```

#### 3c. Verification Checklist
- [x] Does the code import all required libraries? (Includes `FreeformBuilder` logic, `PP_ALIGN`, `MSO_ANCHOR`)
- [x] Does it handle the case where an image download fails? (Not applicable here; relies entirely on pure native vector generation).
- [x] Are all color values explicit RGBA/RGB tuples? (Yes, explicitly defined as `(200, 16, 46)`, `(0, 0, 0)`, etc.).
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes, it accurately calculates the diagonal gap and split layout).
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes, the defining visual trait—the angled colored polygons and structured right-aligned data—is fully reproduced).