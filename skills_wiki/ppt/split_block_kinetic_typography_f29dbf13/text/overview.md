# Split-Block Kinetic Typography

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Split-Block Kinetic Typography

* **Core Visual Mechanism**: High-contrast, massive geometric sans-serif text split across multiple distinct, tightly aligned text blocks. The visual tension is created by placing two text boxes side-by-side with opposing text alignments (Right-align vs Left-align) hugging a central axis. This creates a cohesive "single block" illusion that is perfectly primed for opposing directional entrance animations (e.g., flying in from opposite sides).
* **Why Use This Skill (Rationale)**: Large, flat typography creates immediate visual impact. Breaking a phrase into modular, contrasting blocks allows for dynamic motion and rhythm in presentation design. It forces the audience to read the statement piece-by-piece, enhancing retention.
* **Overall Applicability**: Ideal for high-energy intro slides, bold quote slides, transitional chapters, and promotional/manifesto video sequences. 
* **Value Addition**: Transforms a static, boring phrase into a punchy, modern graphic element. It elevates text from mere "content" to the primary visual feature of the slide.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: High contrast is mandatory. A deeply dark, matte background pushes the text forward. 
    - Background: Deep Charcoal `(20, 20, 22, 255)`
    - Primary Text: Pure White `(255, 255, 255, 255)`
    - Accent Text: Vibrant Punchy Red `(255, 42, 68, 255)`
  - **Text Hierarchy**: Exceptionally large font sizes (110pt+), aggressively bolded, using geometric sans-serif typefaces like *Futura*, *Impact*, or *Arial Black*. Line spacing is tighter than default to make multiline text look like a solid brick.

* **Step B: Compositional Style**
  - **The Split-Axis Trick**: The canvas is split exactly at 50%. 
    - The Left text box occupies `0% to 50%` of the width. Its text is **Right-aligned**, pushing it flush against the center line.
    - The Right text box occupies `50% to 100%` of the width. Its text is **Left-aligned**, pushing it flush against the center line from the other side.
  - A tiny gap (~0.2 inches) is maintained in the dead center so the blocks don't physically touch, creating an incredibly clean seam regardless of how long the text is.

* **Step C: Dynamic Effects & Transitions**
  - **Kinetic Motion**: The left block flies in from the left edge; the right block flies in from the right edge.
  - *Note*: Natively generating PowerPoint entrance timing `<p:timing>` trees from scratch in Python is highly unstable and prone to file corruption. The provided code automatically constructs the perfect structural and spatial prerequisites (the separated, color-coded, center-snapping blocks) so the user can simply select them and click "Fly In" in PowerPoint.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Typographic Blocks & Layout** | `python-pptx` native | Standard text shapes are required here so the final text remains editable and hookable for native PowerPoint entrance animations. |
| **Split-Axis Alignment** | `python-pptx` anchors | Using `PP_ALIGN.RIGHT` and `PP_ALIGN.LEFT` bounded by mathematically calculated bounding boxes guarantees a perfect center seam without needing to measure text pixel widths. |

> **Feasibility Assessment**: 85% — The distinct layout, exact typography scale, center-seam alignment logic, and color separation are fully and dynamically reproduced. The PowerPoint 'Fly-In' entrance animation relies on the UI, as programmatic injection of entrance timing nodes without a pre-existing template file is dangerous to the PPTX schema. The script perfectly sets up the independent shape blocks required for the kinetic effect.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Default Title", # Ignored, using phrases instead
    body_text: str = "",
    phrases: list = ["WORK\nHARD", "PLAY\nHARD"],
    bg_color: tuple = (20, 20, 22),
    colors: list = [(255, 255, 255), (255, 42, 68)],
    font_name: str = "Futura",
    font_size: int = 120,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Split-Block Kinetic Typography effect.
    The script perfectly aligns multiple text blocks along a central axis
    using opposing text alignments to create a seamless kinetic typography setup.

    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.dml.color import RGBColor

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # === Layer 2: Kinetic Typography Layout ===
    # A small gap forces the blocks to stay slightly separated at the seam
    gap = Inches(0.2)
    center_x = prs.slide_width / 2

    # Layout calculation
    if len(phrases) == 2:
        # The dual-split kinetic layout (as seen in the tutorial):
        # Left box right-aligns text, Right box left-aligns text.
        alignments = [PP_ALIGN.RIGHT, PP_ALIGN.LEFT]
        lefts = [0, center_x + gap / 2]
        widths = [center_x - gap / 2, center_x - gap / 2]
    else:
        # Generic fallback if the user passes more than 2 phrases
        col_w = prs.slide_width / len(phrases)
        alignments = [PP_ALIGN.CENTER] * len(phrases)
        lefts = [i * col_w for i in range(len(phrases))]
        widths = [col_w] * len(phrases)

    # Generate the typography blocks
    for i, phrase in enumerate(phrases):
        # Create full-height text boxes
        txBox = slide.shapes.add_textbox(lefts[i], 0, widths[i], prs.slide_height)
        tf = txBox.text_frame
        tf.word_wrap = True
        
        # Vertically center the text within the slide height
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE

        # Clear default paragraphs before adding customized lines
        tf.clear()
        
        # Split phrase by newline to ensure tight line spacing is applied uniformly
        lines = phrase.split('\n')
        for j, line in enumerate(lines):
            # Use the existing first paragraph or append new ones
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.text = line
            p.alignment = alignments[i]
            
            # Compress line spacing to create a 'solid brick' kinetic look
            p.line_spacing = 0.85
            
            # Apply heavy font styling
            for run in p.runs:
                run.font.name = font_name
                run.font.size = Pt(font_size)
                run.font.bold = True
                
                # Alternate colors based on the text block index
                color_idx = i % len(colors)
                run.font.color.rgb = RGBColor(*colors[color_idx])

    prs.save(output_pptx_path)
    return output_pptx_path
```