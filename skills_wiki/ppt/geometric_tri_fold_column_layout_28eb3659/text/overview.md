# Geometric Tri-Fold Column Layout

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Geometric Tri-Fold Column Layout

* **Core Visual Mechanism**: The slide mimics a physical tri-fold brochure by dividing a widescreen canvas (16:9) into three distinct white vertical panels against a subtle light gray background. The strict verticality of the columns is broken by overlapping, angled geometric ribbons (parallelograms and trapezoids) placed at the header and footer, creating a dynamic, layered paper effect.
* **Why Use This Skill (Rationale)**: Breaking a slide into three columns reduces the line length of text, making dense information much easier to read (similar to newspaper columns). The angled geometric accents draw the eye horizontally, tying the three independent columns back together into a unified composition. 
* **Overall Applicability**: Ideal for corporate overviews, product feature sheets, agenda slides, executive summaries, or printed leave-behinds. 
* **Value Addition**: Transforms a standard text-heavy bullet-point slide into a highly structured, professional document that feels like a bespoke desktop-published brochure.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Columns**: Three identical white rectangles `(255, 255, 255)` acting as text containers.
  * **Background**: Very light gray `(242, 242, 242)` to provide subtle contrast for the white columns.
  * **Color Palette (Corporate Modern)**:
    * Navy Blue: `(32, 56, 100)` — Anchors the design, used for primary headers and outer shapes.
    * Vibrant Teal: `(0, 176, 155)` — Secondary accent, used for subheadings and middle overlapping shapes.
    * Mustard Yellow: `(255, 192, 0)` — Tertiary pop color, used to add warmth and contrast in the geometric ribbons.
  * **Typography**: Clean sans-serif, utilizing strong size contrast (e.g., 28pt bold Navy for titles, 14pt Teal for subtitles, 10pt gray for body text).

* **Step B: Compositional Style**
  * **Layout**: Three equal-width columns. With a 13.33" width canvas, each column is ~4.18" wide with a ~0.2" gap.
  * **Angles**: The top geometric ribbon leans to the right (`/ /`), while the bottom geometric ribbon leans to the left (`\ \`). This opposition creates visual balance and tension.
  * **Layering**: Shapes are layered back-to-front (e.g., Yellow in the back, Teal in the middle, Navy in the front) to create depth without using drop shadows.

* **Step C: Dynamic Effects & Transitions**
  * *In Code*: Static rendering of precise polygons to create the layered aesthetic.
  * *In PPT (Manual)*: This layout pairs perfectly with a "Wipe" (From Top/Bottom) or "Fade" transition, revealing the columns sequentially.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Background & Columns | `python-pptx` native shapes | Basic rectangles are perfectly suited for the column base layout. |
| Angled Geometric Ribbons | `python-pptx` FreeformBuilder | Standard PPT shapes (like `MSO_SHAPE.PARALLELOGRAM`) rely on unpredictable adjustment values. Building custom polygons via `FreeformBuilder` guarantees exact angles and overlapping points. |
| Text Styling & Hierarchy | `python-pptx` text frames | Provides granular control over font sizes, colors, and line spacing within the generated columns. |

> **Feasibility Assessment**: 100% reproduction. The layout, geometric exactness, color scheme, and typographic hierarchy shown in the tutorial can be perfectly recreated using programmatic freeform polygons and text frames.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "INNOVATION\nAND DESIGN",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas porttitor congue massa. Fusce posuere, magna sed pulvinar ultricies, purus lectus malesuada libero.",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Geometric Tri-Fold Column Layout" visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    
    # 1. Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Color Palette
    COLOR_BG = RGBColor(242, 242, 242)
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_NAVY = RGBColor(32, 56, 100)
    COLOR_TEAL = RGBColor(0, 176, 155)
    COLOR_YELLOW = RGBColor(255, 192, 0)
    COLOR_GRAY = RGBColor(217, 217, 217)
    COLOR_TEXT_DARK = RGBColor(89, 89, 89)

    # 2. Draw Background
    bg = slide.shapes.add_shape(1, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_BG
    bg.line.fill.background()

    # 3. Draw 3 Columns (White Rectangles)
    col_width = 4.18
    col_height = 7.1
    y_offset = 0.2
    
    cols = []
    for i in range(3):
        x_offset = 0.2 + (col_width + 0.2) * i
        col = slide.shapes.add_shape(1, Inches(x_offset), Inches(y_offset), Inches(col_width), Inches(col_height))
        col.fill.solid()
        col.fill.fore_color.rgb = COLOR_WHITE
        col.line.fill.background()
        cols.append(x_offset) # Save X coordinates for text alignment

    # Helper function to draw exact polygons
    def draw_polygon(slide, vertices_inches, color):
        ffb = slide.shapes.build_freeform(Inches(vertices_inches[0][0]), Inches(vertices_inches[0][1]))
        vertices_pt = [(Inches(x), Inches(y)) for x, y in vertices_inches[1:]]
        ffb.add_line_segments(vertices_pt, close=True)
        shape = ffb.convert_to_shape()
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        shape.line.color.rgb = color # Hide border by matching fill
        return shape

    # 4. Draw Top Geometric Ribbon (Leans Right / /)
    # Layer 1: Yellow (Back)
    draw_polygon(slide, [(6.0, 0.2), (7.5, 0.2), (7.0, 0.9), (5.5, 0.9)], COLOR_YELLOW)
    # Layer 2: Teal (Middle)
    draw_polygon(slide, [(3.5, 0.2), (6.5, 0.2), (6.0, 0.9), (3.0, 0.9)], COLOR_TEAL)
    # Layer 3: Navy (Front)
    draw_polygon(slide, [(0.2, 0.2), (4.0, 0.2), (3.5, 0.9), (0.2, 0.9)], COLOR_NAVY)

    # 5. Draw Bottom Geometric Ribbon (Leans Left \ \)
    # Layer 1: Gray (Back Right)
    draw_polygon(slide, [(8.5, 6.6), (13.13, 6.6), (13.13, 7.3), (9.5, 7.3)], COLOR_GRAY)
    # Layer 2: Yellow (Back)
    draw_polygon(slide, [(6.0, 6.6), (9.0, 6.6), (8.0, 7.3), (5.0, 7.3)], COLOR_YELLOW)
    # Layer 3: Teal (Middle)
    draw_polygon(slide, [(2.0, 6.6), (6.5, 6.6), (5.5, 7.3), (1.0, 7.3)], COLOR_TEAL)
    # Layer 4: Navy (Front)
    draw_polygon(slide, [(0.2, 6.6), (2.5, 6.6), (1.5, 7.3), (0.2, 7.3)], COLOR_NAVY)

    # Helper function for text boxes
    def add_text_box(slide, x, y, w, h, text, color, size, bold=False, align=PP_ALIGN.LEFT):
        txBox = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.alignment = align
        p.font.name = 'Calibri'
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = color
        return txBox

    # 6. Populate Column 1 (Title & Intro)
    add_text_box(slide, cols[0] + 0.3, 1.2, 3.5, 1.0, title_text, COLOR_NAVY, 28, bold=True)
    add_text_box(slide, cols[0] + 0.3, 2.3, 3.5, 0.5, "YOUR SUBTITLE HERE", COLOR_TEAL, 12, bold=True)
    
    # Simple line separator
    line = slide.shapes.add_shape(9, Inches(cols[0] + 0.3), Inches(2.7), Inches(1.5), Inches(0))
    line.line.color.rgb = COLOR_GRAY

    add_text_box(slide, cols[0] + 0.3, 3.0, 3.5, 2.0, f"1.   {body_text}", COLOR_TEXT_DARK, 10)
    add_text_box(slide, cols[0] + 0.3, 4.5, 3.5, 2.0, f"2.   {body_text}", COLOR_TEXT_DARK, 10)

    # 7. Populate Column 2 (Content & Infographics)
    add_text_box(slide, cols[1] + 0.3, 0.5, 3.5, 0.5, "YOUR SUBTITLE HERE", COLOR_YELLOW, 12, bold=True)
    add_text_box(slide, cols[1] + 0.3, 0.8, 3.5, 1.5, body_text, COLOR_TEXT_DARK, 10)
    
    for i in range(3):
        # Add small circles to mimic infographics
        y_pos = 2.5 + (i * 1.2)
        circle = slide.shapes.add_shape(9, Inches(cols[1] + 0.3), Inches(y_pos), Inches(0.4), Inches(0.4))
        circle.fill.solid()
        circle.fill.fore_color.rgb = COLOR_WHITE
        circle.line.color.rgb = COLOR_TEAL
        circle.line.width = Pt(1.5)
        # Add accompanying text
        add_text_box(slide, cols[1] + 0.8, y_pos - 0.1, 3.0, 1.0, "Short descriptive text detailing the specific point.", COLOR_TEXT_DARK, 10)

    # 8. Populate Column 3 (Header & Branding)
    # Add top-right small placeholder icons
    for i in range(3):
        circle = slide.shapes.add_shape(9, Inches(cols[2] + 2.5 + (i*0.5)), Inches(0.4), Inches(0.3), Inches(0.3))
        circle.fill.solid()
        circle.fill.fore_color.rgb = COLOR_WHITE
        circle.line.color.rgb = COLOR_GRAY

    add_text_box(slide, cols[2] + 0.3, 1.5, 3.5, 1.5, "INNOVATION\nAND DESIGN\nMANAGEMENT", COLOR_NAVY, 24, bold=True, align=PP_ALIGN.RIGHT)
    add_text_box(slide, cols[2] + 0.3, 6.0, 3.5, 0.5, "COMPANY NAME", COLOR_NAVY, 14, bold=True, align=PP_ALIGN.RIGHT)
    add_text_box(slide, cols[2] + 0.3, 6.3, 3.5, 0.5, "www.website.com", COLOR_TEAL, 10, bold=False, align=PP_ALIGN.RIGHT)

    prs.save(output_pptx_path)
    return output_pptx_path
```