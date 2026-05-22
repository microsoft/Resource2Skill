# Dynamic Split-Diagonal End Card

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic Split-Diagonal End Card

* **Core Visual Mechanism**: This pattern relies on high-contrast, chunky geometric blocking. Two dominant diagonal "pillars" act as structural frames, drawing the eye inward toward a central focal point. Overlapping these pillars with heavy, dark rectangular placeholders creates a sense of depth (layering) and cinematic framing. The use of rotated vertical text aligned with the diagonals adds a modern, energetic tension to the layout.
* **Why Use This Skill (Rationale)**: The diagonal lines break the rigid horizontal/vertical grid typical of PowerPoint, instantly signaling dynamic motion and finality. By symmetrically framing the center, it aggressively guides the viewer's attention exactly where you want it (the final call to action or logo).
* **Overall Applicability**: This is the archetypal "YouTube Outro" screen, but in a business context, it is perfect for final "Call to Action" slides, "Next Steps" summaries, or closing portfolio slides where you want to highlight two distinct pathways (e.g., "Read the Report" vs "Watch the Demo") alongside a central brand mark.
* **Value Addition**: It transforms a mundane closing slide ("Thank You" or list of links) into a highly engaging, interactive-feeling dashboard panel. It looks engineered rather than just typed.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: High contrast tri-tone palette.
    - Background: Faint cool gray `(245, 245, 247)` to provide soft contrast.
    - Structural Diagonals: Deep, vibrant crimson `(163, 15, 35)`.
    - Placeholders: Off-black/charcoal `(22, 22, 24)` to command weight.
  - **Text Hierarchy**:
    - Hero Title: Top center, large, bold, heavily tracked (letter-spaced), matching the primary accent color.
    - Banner Accents: Vertical, uppercase, white text tracking down the red diagonals.
    - Metadata/Socials: Small, muted dark gray text anchored at the bottom center.

* **Step B: Compositional Style**
  - **Symmetrical V-Frame**: The left and right diagonal banners slope inward (top is further out, bottom is further in), creating an inverted "V" that acts as a funnel toward the center.
  - **Layering Depth**: The dark rectangles (occupying ~30% width each) are placed *on top* of the diagonal banners, with a slightly offset red rectangle behind them acting as a sharp, flat drop shadow.
  - **Center Anchor**: A perfect circle sits dead center, interrupting the empty space between the heavy left and right blocks.

* **Step C: Dynamic Effects & Transitions**
  - *Note*: While the video uses quick cuts, this layout is perfectly suited for PowerPoint's "Pan" or "Fly In" animations, where the red pillars shoot in from the top/bottom, followed by the dark rectangles stamping down onto them.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Diagonal Structural Banners** | `python-pptx` (FreeformBuilder) | Standard rectangles leave messy corners when rotated off-canvas. `FreeformBuilder` allows precise mathematical pinning of polygons to slide edges. |
| **Layered Drop Shadows** | `python-pptx` native shapes | The flat, sharp shadow aesthetic is best achieved by stacking solid shapes rather than using blurry rendering effects. |
| **Rotated Banner Text** | `python-pptx` text box rotation | Native rotation perfectly aligns text with the angle of the freeform polygons. |
| **Floating Center Icon** | `lxml` XML injection | We use `lxml` to inject a true native PowerPoint blurred outer shadow on the central circle to make it pop off the flat background elements. |

> **Feasibility Assessment**: 100%. Because this design relies on bold, crisp geometric blocking rather than complex raster effects or image masking, native `python-pptx` (augmented with `lxml` for the shadow) can reproduce the aesthetic perfectly, resulting in a lightweight, fully editable vector slide.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "SUBSCRIBE",
    left_banner_text: str = "L A T E S T",
    right_banner_text: str = "P O P U L A R",
    accent_color: tuple = (163, 15, 35),  # Deep Crimson
    dark_color: tuple = (22, 22, 24),     # Charcoal/Off-Black
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Dynamic Split-Diagonal End Card visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.enum.shapes import MSO_SHAPE
    from lxml import etree

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Convert tuples to RGBColor
    COLOR_ACCENT = RGBColor(*accent_color)
    COLOR_DARK = RGBColor(*dark_color)
    COLOR_BG = RGBColor(245, 245, 247)
    COLOR_WHITE = RGBColor(255, 255, 255)

    # Helper: Add Text Box
    def add_text(left, top, width, height, text, size, bold=False, color=COLOR_DARK, align=PP_ALIGN.CENTER):
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = text
        p.alignment = align
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = color
        p.font.name = "Arial"
        return txBox

    # Helper: Inject Native Shadow
    def apply_shadow(shape):
        spPr = shape.element.spPr
        effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
        outerShdw = etree.SubElement(effectLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw')
        outerShdw.set('blurRad', '150000')  # Blur radius
        outerShdw.set('dist', '40000')      # Distance
        outerShdw.set('dir', '2700000')     # Angle (bottom)
        srgbClr = etree.SubElement(outerShdw, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
        srgbClr.set('val', '000000')
        alpha = etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha')
        alpha.set('val', '25000')           # 25% opacity

    # === Layer 1: Background ===
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_BG
    bg.line.fill.background()

    # === Layer 2: Diagonal Structural Banners (V-Shape framing) ===
    # Left Banner (slopes inward to the right)
    points_left = [(Inches(1.5), 0), (Inches(2.8), 0), (Inches(4.3), Inches(7.5)), (Inches(3.0), Inches(7.5))]
    builder_l = slide.shapes.build_freeform()
    builder_l.add_line_segments(points_left, close=True)
    shape_left = builder_l.convert_to_shape()
    shape_left.fill.solid(); shape_left.fill.fore_color.rgb = COLOR_ACCENT
    shape_left.line.fill.background()

    # Right Banner (slopes inward to the left)
    points_right = [(Inches(10.53), 0), (Inches(11.83), 0), (Inches(10.33), Inches(7.5)), (Inches(9.03), Inches(7.5))]
    builder_r = slide.shapes.build_freeform()
    builder_r.add_line_segments(points_right, close=True)
    shape_right = builder_r.convert_to_shape()
    shape_right.fill.solid(); shape_right.fill.fore_color.rgb = COLOR_ACCENT
    shape_right.line.fill.background()

    # === Layer 3: Placeholders with Flat Accent Shadows ===
    # Left Content Block
    s1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(2.9), Inches(3.6), Inches(2.2))
    s1.fill.solid(); s1.fill.fore_color.rgb = COLOR_ACCENT; s1.line.fill.background()
    m1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(2.8), Inches(3.6), Inches(2.2))
    m1.fill.solid(); m1.fill.fore_color.rgb = COLOR_DARK; m1.line.fill.background()
    add_text(Inches(0.5), Inches(3.65), Inches(3.6), Inches(0.5), "Video / Content", 18, color=COLOR_WHITE)

    # Right Content Block
    s2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.33), Inches(2.9), Inches(3.6), Inches(2.2))
    s2.fill.solid(); s2.fill.fore_color.rgb = COLOR_ACCENT; s2.line.fill.background()
    m2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.23), Inches(2.8), Inches(3.6), Inches(2.2))
    m2.fill.solid(); m2.fill.fore_color.rgb = COLOR_DARK; m2.line.fill.background()
    add_text(Inches(9.23), Inches(3.65), Inches(3.6), Inches(0.5), "Video / Content", 18, color=COLOR_WHITE)

    # === Layer 4: Central Floating Anchor ===
    # Outer accent ring
    ring = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(5.66), Inches(2.75), Inches(2.0), Inches(2.0))
    ring.fill.solid(); ring.fill.fore_color.rgb = COLOR_ACCENT; ring.line.fill.background()
    apply_shadow(ring)
    # Inner white circle (creating a logo/profile placeholder)
    inner = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(5.81), Inches(2.90), Inches(1.7), Inches(1.7))
    inner.fill.solid(); inner.fill.fore_color.rgb = COLOR_WHITE; inner.line.fill.background()

    # === Layer 5: Typography & Decals ===
    # Hero Title
    add_text(Inches(3.66), Inches(0.8), Inches(6.0), Inches(1.0), title_text.upper(), 44, bold=True, color=COLOR_ACCENT)

    # Vertical Banner Texts
    # Center points geometrically calculated to sit perfectly inside the sloping pillars
    tb1 = add_text(Inches(1.15), Inches(5.0), Inches(4.0), Inches(0.5), left_banner_text, 24, bold=True, color=COLOR_WHITE)
    tb1.rotation = -90.0

    tb2 = add_text(Inches(8.18), Inches(5.0), Inches(4.0), Inches(0.5), right_banner_text, 24, bold=True, color=COLOR_WHITE)
    tb2.rotation = 90.0

    # Socials / Footer links
    add_text(Inches(4.66), Inches(5.2), Inches(4.0), Inches(0.5), "@your_handle_here", 14, color=RGBColor(80,80,80))
    add_text(Inches(4.66), Inches(5.5), Inches(4.0), Inches(0.5), "website.com/link", 14, color=RGBColor(80,80,80))

    prs.save(output_pptx_path)
    return output_pptx_path
```