# Modern Diagonal Split Hero Layout

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Modern Diagonal Split Hero Layout

* **Core Visual Mechanism**: The defining visual idea is a sharp, dynamic diagonal division of the slide's background space. Instead of a standard solid color or horizontal/vertical split, a dark, heavy geometric polygon covers the left ~70% of the screen, slicing downwards to reveal a lighter contrasting background on the right. This serves as a high-contrast canvas for bold, stacked, white typography.
* **Why Use This Skill (Rationale)**: Diagonal lines inherently convey motion, energy, and progression, breaking the rigid, predictable horizontal/vertical grid of standard presentations. The dark background area creates a natural "safe zone" for high-contrast text readability, while the lighter exposed area adds visual interest without distracting from the core message.
* **Overall Applicability**: Perfect for title slides, chapter breakers, transition slides, or "hero" statements where you need to deliver a short, punchy message with high visual impact. 
* **Value Addition**: It elevates a basic text slide into a modern, professionally designed composition. When paired with a "Wipe" animation (as shown in the tutorial), the diagonal edge naturally leads the viewer's eye along the path of the text reveal.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Color Logic**: 
    * Dominant Left Polygon (Dark Gray): `RGBA(45, 45, 45, 255)`
    * Exposed Background (Medium Gray): `RGBA(125, 125, 125, 255)`
    * Typography (Pure White): `RGBA(255, 255, 255, 255)`
  * **Text Hierarchy**: Large, bold, sans-serif text tightly stacked. All text carries equal weight in this specific hero execution, relying on line breaks for pacing.

* **Step B: Compositional Style**
  * The dark polygon anchors the top-left at coordinates `(0,0)`, extends rightwards to approximately 75% of the slide width at the top edge, and angles sharply back to about 50% of the slide width at the bottom edge.
  * Text is strictly left-aligned and horizontally constrained entirely within the dark polygon to maintain maximum contrast.

* **Step C: Dynamic Effects & Transitions**
  * **Animation**: The tutorial specifically focuses on an "Entrance: Wipe" animation.
  * **Effect Options**: Direction is set to "From Left", and the Sequence is set to animate text "By word" with a 10% delay between words.
  * *Limitation Note*: Slide animations (manipulating the `<p:timing>` and `<p:animEffect>` XML nodes) are overwhelmingly complex and practically unsupported by `python-pptx`. Generating dynamic timelines via code often corrupts the file. Therefore, the code below strictly generates the **visual composition** required for this effect. The animation must be applied manually in the UI.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Diagonal Background Split | `python-pptx` (FreeformBuilder) | A standard rectangle cannot achieve the angled edge. The `FreeformBuilder` allows us to draw an exact custom polygon via coordinate mapping. |
| Typography & Layout | `python-pptx` native | Standard text frame APIs are perfect for placing and styling the left-aligned bold text. |
| Wipe Animation | *Not implemented in code* | `python-pptx` lacks an API for the `<p:timing>` animation sequence. XML injection for sequential word-by-word animation is brittle and prone to file corruption. The script delivers the complete visual layout. |

> **Feasibility Assessment**: **70%**. The code produces a 100% accurate reproduction of the visual style, layout, custom diagonal shapes, and text formatting. The 30% missing is the actual playback of the "Wipe by Word" animation, which must be clicked manually in the PowerPoint Animation pane.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Welcome back to\nmy YouTube channel",
    dark_color: tuple = (45, 45, 45),    # RGB for the main polygon
    light_color: tuple = (125, 125, 125),  # RGB for the background slice
    text_color: tuple = (255, 255, 255),   # RGB for the text
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Modern Diagonal Split Hero Layout" visual effect.
    This generates the custom freeform geometry and typographic layout.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN

    # Initialize presentation with standard 16:9 widescreen dimensions
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a completely blank slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background (Light Gray Base) ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*light_color)

    # === Layer 2: Visual Effect (Diagonal Dark Polygon) ===
    # Draw a custom polygon that covers the left side and cuts diagonally on the right
    ff_builder = slide.shapes.build_freeform()
    ff_builder.add_line_segments([
        (Inches(0), Inches(0)),         # Top Left
        (Inches(10.5), Inches(0)),      # Top Right (extends ~78% across)
        (Inches(7.0), Inches(7.5)),       # Bottom Right (angles back to ~52% across)
        (Inches(0), Inches(7.5)),       # Bottom Left
        (Inches(0), Inches(0))          # Close path back to Top Left
    ])
    
    diagonal_shape = ff_builder.convert_to_shape()
    
    # Style the polygon
    diagonal_shape.fill.solid()
    diagonal_shape.fill.fore_color.rgb = RGBColor(*dark_color)
    # Remove the border line to keep it clean
    diagonal_shape.line.fill.solid()
    diagonal_shape.line.fill.fore_color.rgb = RGBColor(*dark_color)

    # === Layer 3: Text & Content ===
    # Place text within the "safe zone" of the dark polygon
    left_margin = Inches(1.5)
    top_margin = Inches(2.5)
    width = Inches(7.0)
    height = Inches(2.5)

    txBox = slide.shapes.add_textbox(left_margin, top_margin, width, height)
    text_frame = txBox.text_frame
    text_frame.word_wrap = True
    
    p = text_frame.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.LEFT
    
    # Style the text to be bold, white, and highly legible
    font = p.font
    font.name = 'Arial'
    font.size = Pt(48)
    font.bold = True
    font.color.rgb = RGBColor(*text_color)

    # Note: To fully match the video, open the resulting PPTX, select the text box,
    # go to Animations -> Wipe -> From Left -> Effect Options -> Animate Text: By Word (10% delay).

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
```