# Horizontal Accordion Morph (Layered Folder Tabs)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Horizontal Accordion Morph (Layered Folder Tabs)

* **Core Visual Mechanism**: The presentation utilizes a horizontal accordion layout structured like a series of physical file folders. The tabs are stacked from left to right. When a tab becomes "active," its width expands significantly to reveal content, while the other inactive tabs compress tightly to the left and right edges. Drop shadows on each tab enhance the layered, physical depth. 
* **Why Use This Skill (Rationale)**: This layout provides clear wayfinding. Viewers always know exactly where they are in the presentation structure because the unselected chapters remain visible as compressed tabs. The physical overlapping metaphor grounds the information, making abstract topics feel organized and accessible.
* **Overall Applicability**: Ideal for agenda slides, chapter transitions, process steps, product feature highlights, or any content that contains 3-5 distinct, equally important categories.
* **Value Addition**: Transforms a standard bulleted agenda or section header into a highly interactive, tactile visual experience. By generating this sequentially across multiple slides, PowerPoint's native "Morph" transition will smoothly animate the expanding and collapsing of the tabs.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Shapes**: Custom-drawn polygon shapes representing a rectangle with a small protruding "tab marker" on its right edge.
  - **Color Logic**: A monochromatic gradient palette. The background is a very dark violet `(45, 18, 75)`. The tabs range from light lilac `(234, 214, 252)` on the top layer to deep violet `(97, 37, 144)` on the bottom layer.
  - **Text Hierarchy**: 
    1. A massive, highly transparent background number (e.g., "01") serving as a watermark (`70%` transparency).
    2. Bold, uppercase section titles (`24 Pt`).
    3. Standard body copy (`12 Pt`).
    4. "Chapter SLIDES" persistent global title on the extreme right canvas.

* **Step B: Compositional Style**
  - **Layout Principles**: The design acts as a shifting ratio. Out of a ~`10.0` inch active working area, `6.4` inches are allocated to the *active* tab, while the remaining `3.6` inches are distributed evenly among the *collapsed* tabs (`1.2` inches each).
  - **Layering**: To ensure the shadows cast perfectly to the right, the tabs share a common left origin (`X=0`) and are drawn from back to front (Tab 4 -> Tab 3 -> Tab 2 -> Tab 1). The top-most tab perfectly eclipses the underlying tabs' main bodies, leaving only their rightmost edges and markers exposed.

* **Step C: Dynamic Effects & Transitions**
  - The true magic of this layout happens during slide transitions. By sequentially assigning the "expanded" width to a different tab on consecutive slides, PowerPoint's native Morph transition automatically creates a buttery-smooth horizontal shifting accordion.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Custom Tab Geometry** | `python-pptx` (FreeformBuilder) | The tab shape requires a single unified body (Main area + Protruding lip) so the drop shadow outlines the whole shape seamlessly. |
| **Physical Depth (Shadows)** | `lxml` XML injection | `python-pptx` lacks a direct property for rendering sophisticated blur and transparency on Outer Shadows; XML ensures pixel-perfect fidelity. |
| **Text Watermark Opacity** | `lxml` XML injection | Standard `python-pptx` font colors cannot apply RGBA alpha values (transparency). Injecting `<a:alpha>` enables the watermark effect. |

*Feasibility Assessment*: 95%. The visual structure, overlapping logic, custom geometry, and shadows are reproduced perfectly. Users will only need to apply the "Morph" transition natively in PowerPoint across the generated slides to trigger the animation. Standard native vector shapes are used in place of SVG icons.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "LOREM IPSUM DOLOR",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    **kwargs,
) -> str:
    """
    Creates a 4-slide presentation demonstrating the Horizontal Accordion Morph effect.
    Returns: path to the saved PPTX file.
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

    # Color Palette
    bg_color = RGBColor(45, 18, 75)
    tab_colors = [
        RGBColor(234, 214, 252),  # Tab 1: Light Lilac
        RGBColor(194, 142, 238),  # Tab 2: Light Purple
        RGBColor(151,  85, 203),  # Tab 3: Medium Purple
        RGBColor( 97,  37, 144)   # Tab 4: Dark Purple
    ]

    # Dimensions
    num_tabs = 4
    collapsed_w = 1.2
    expanded_w = 6.4
    canvas_height = 7.5
    marker_height = 1.2
    marker_width = 0.4
    marker_spacing = 0.3
    start_y = 0.9

    # --- XML Helpers ---
    def add_drop_shadow(shape):
        """Injects a subtle right-facing drop shadow into a shape's properties."""
        spPr = shape.element.spPr
        effectLst = etree.SubElement(spPr, "{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst")
        # dir="0" means angle 0 (pure right)
        outerShdw = etree.SubElement(effectLst, "{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw",
                                     blurRad="120000", dist="60000", dir="0", algn="tl", rotWithShape="0")
        srgbClr = etree.SubElement(outerShdw, "{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr", val="000000")
        etree.SubElement(srgbClr, "{http://schemas.openxmlformats.org/drawingml/2006/main}alpha", val="40000") # 40% opacity

    def set_run_opacity(run, alpha_percent=40):
        """Applies transparency to a text run by mutating its XML."""
        color = run.font.color
        srgbClr = color._color_format._element.find("{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr")
        if srgbClr is not None:
            alpha = etree.SubElement(srgbClr, "{http://schemas.openxmlformats.org/drawingml/2006/main}alpha")
            alpha.set("val", str(int(alpha_percent * 1000)))  # Format: 100,000ths

    # Generate 4 sequential slides to serve as Morph keyframes
    for active_idx in range(num_tabs):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # 1. Set Background
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = bg_color
        
        # 2. Add Persistent Right-Side Title
        global_title = slide.shapes.add_textbox(Inches(10.5), Inches(3.0), Inches(2.5), Inches(1.5))
        tf_gt = global_title.text_frame
        tf_gt.word_wrap = True
        p1 = tf_gt.paragraphs[0]
        p1.alignment = PP_ALIGN.CENTER
        run1 = p1.add_run()
        run1.text = "chapter\n"
        run1.font.size = Pt(32)
        run1.font.bold = True
        run1.font.italic = True
        run1.font.color.rgb = RGBColor(255, 200, 50)  # Yellow accent
        
        p2 = tf_gt.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        run2 = p2.add_run()
        run2.text = "SLIDES"
        run2.font.size = Pt(48)
        run2.font.bold = True
        run2.font.color.rgb = RGBColor(255, 255, 255)

        # 3. Calculate Tab Widths for this Keyframe
        # The trick: all tabs start at X=0. Their width determines what is visible.
        widths = []
        current_w = 0
        for j in range(num_tabs):
            step = expanded_w if j == active_idx else collapsed_w
            current_w += step
            widths.append(current_w)

        # 4. Draw Tabs from Back to Front (Z-Index ordering)
        for j in range(num_tabs - 1, -1, -1):
            W_j = widths[j]
            my_j = start_y + j * (marker_height + marker_spacing)
            color_j = tab_colors[j]

            # Build Freeform Polygon
            builder = slide.shapes.build_freeform(Inches(0), Inches(0))
            builder.add_line_segments([
                (Inches(W_j), Inches(0)),
                (Inches(W_j), Inches(my_j)),
                (Inches(W_j + marker_width - 0.1), Inches(my_j)),         # Bevel top
                (Inches(W_j + marker_width), Inches(my_j + 0.1)),
                (Inches(W_j + marker_width), Inches(my_j + marker_height - 0.1)),
                (Inches(W_j + marker_width - 0.1), Inches(my_j + marker_height)), # Bevel bottom
                (Inches(W_j), Inches(my_j + marker_height)),
                (Inches(W_j), Inches(canvas_height)),
                (Inches(0), Inches(canvas_height))
            ], close=True)
            
            tab_shape = builder.convert_to_shape()
            tab_shape.fill.solid()
            tab_shape.fill.fore_color.rgb = color_j
            tab_shape.line.fill.background()  # Remove border
            add_drop_shadow(tab_shape)

            # Add Tab Marker Number
            marker_text_box = slide.shapes.add_textbox(Inches(W_j), Inches(my_j), Inches(marker_width), Inches(marker_height))
            tf_m = marker_text_box.text_frame
            tf_m.vertical_anchor = MSO_ANCHOR.MIDDLE
            p_m = tf_m.paragraphs[0]
            p_m.alignment = PP_ALIGN.CENTER
            run_m = p_m.add_run()
            run_m.text = str(j + 1)
            run_m.font.size = Pt(24)
            run_m.font.bold = True
            # Dark text for the lightest tab, white for the rest
            run_m.font.color.rgb = RGBColor(97, 37, 144) if j == 0 else RGBColor(255, 255, 255)

            # 5. Populate Active Tab Content
            if j == active_idx:
                # Calculate visible boundaries of the active tab
                visible_left = widths[j - 1] if j > 0 else 0
                content_x = visible_left + 1.0
                content_w = expanded_w - 2.0
                
                # A. Large Watermark Number
                wm_box = slide.shapes.add_textbox(Inches(content_x), Inches(1.0), Inches(content_w), Inches(3.0))
                tf_wm = wm_box.text_frame
                p_wm = tf_wm.paragraphs[0]
                p_wm.alignment = PP_ALIGN.CENTER
                run_wm = p_wm.add_run()
                run_wm.text = f"{j + 1:02d}"
                run_wm.font.size = Pt(140)
                run_wm.font.bold = True
                run_wm.font.color.rgb = RGBColor(255, 255, 255)
                set_run_opacity(run_wm, 30)  # 70% Transparent
                
                # B. Title
                t_box = slide.shapes.add_textbox(Inches(content_x), Inches(3.5), Inches(content_w), Inches(0.8))
                p_t = t_box.text_frame.paragraphs[0]
                p_t.alignment = PP_ALIGN.CENTER
                run_t = p_t.add_run()
                run_t.text = title_text
                run_t.font.size = Pt(20)
                run_t.font.bold = True
                run_t.font.color.rgb = RGBColor(97, 37, 144) if j == 0 else RGBColor(255, 255, 255)
                
                # C. Body Text
                b_box = slide.shapes.add_textbox(Inches(content_x), Inches(4.3), Inches(content_w), Inches(1.5))
                b_box.text_frame.word_wrap = True
                p_b = b_box.text_frame.paragraphs[0]
                p_b.alignment = PP_ALIGN.CENTER
                run_b = p_b.add_run()
                run_b.text = body_text
                run_b.font.size = Pt(12)
                run_b.font.color.rgb = RGBColor(45, 18, 75) if j == 0 else RGBColor(240, 240, 240)
                
                # D. Decorative Icon Placeholder (Native Shape)
                icon_x = content_x + content_w / 2 - 0.5
                icon = slide.shapes.add_shape(MSO_SHAPE.DIAMOND, Inches(icon_x), Inches(5.6), Inches(1.0), Inches(1.0))
                icon.fill.background() # Empty center
                icon.line.color.rgb = RGBColor(97, 37, 144) if j == 0 else RGBColor(255, 255, 255)
                icon.line.width = Pt(3)

    prs.save(output_pptx_path)
    return output_pptx_path
```