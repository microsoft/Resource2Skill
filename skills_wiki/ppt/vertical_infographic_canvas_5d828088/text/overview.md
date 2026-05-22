# Vertical Infographic Canvas

## Analysis

# Agent_Skill_Distiller Strategy Document

### 1. High-level Design Pattern Extraction

> **Skill Name**: Vertical Infographic Canvas

* **Core Visual Mechanism**: Extending the slide height significantly beyond standard landscape ratios (e.g., making the slide 13.333 inches wide by 26.666 inches tall). The canvas is then divided into full-width horizontal bands of alternating colors to create a continuous vertical scrolling experience.
* **Why Use This Skill (Rationale)**: Humans are intrinsically accustomed to scrolling vertically on web pages and mobile devices. A vertical format allows for a continuous narrative flow (like a process, timeline, or listicle) without the cognitive interruption of slide transitions. Grouping information into colored bands helps parse the narrative into digestible chunks.
* **Overall Applicability**: Perfect for "Top 10" listicles, step-by-step process flows, visual manifestos, company timelines, and data summaries intended to be exported as PDFs or embedded directly into web pages/emails. 
* **Value Addition**: Transforms a standard presentation tool (PowerPoint) into a lightweight desktop publishing tool. It breaks the "presentation" mold, delivering an asset that feels like a professional graphic design poster rather than a pitch deck.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Custom Slide Geometry**: The defining characteristic. Width remains standard (13.33 inches) but Height is multiplied (e.g., 26.66 inches, a 1:2 vertical ratio).
  - **Color Logic (Flat Design)**: The tutorial uses a muted, mid-century modern or "flat design" palette. 
    - Header/Dark Accent: Slate/Navy `(84, 106, 123)`
    - Primary Band: Steel Blue `(115, 153, 172)`
    - Secondary Band: Muted Sand/Orange `(226, 192, 143)`
    - Tertiary Band: Light Gray/Blue `(204, 214, 217)`
  - **Typography**: Bold, uppercase sans-serif or slab-serif headers for section numbers/titles. 
  - **Iconography**: Minimalist flat icons (vectors) placed centrally or aligned left to anchor each text block.
  - **Framing**: The main title is often framed inside a thick-bordered rectangle to draw the eye.

* **Step B: Compositional Style**
  - **Spatial Feel**: Segmented and modular.
  - **Proportions**: 
    - Header occupies the top ~15-20% of the canvas.
    - Remaining space is divided equally among the narrative sections (e.g., 5 sections occupying ~16% height each).
    - Text and content are constrained within a central safe zone (leaving ~10-15% margin on the left and right).

* **Step C: Dynamic Effects & Transitions**
  - Not applicable. Infographics are static and meant to be consumed at the user's scrolling pace (often exported to PDF).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Vertical Canvas Sizing** | `python-pptx` native | Modifying `prs.slide_width` and `prs.slide_height` directly manipulates the presentation canvas XML perfectly. |
| **Color Blocking (Bands)** | `python-pptx` native | Standard rectangles drawn across the full width, iterating through a color palette. |
| **Text & Outlines** | `python-pptx` native | Flat design typography and thick borders can be fully replicated using native shape format APIs without needing PIL. |

> **Feasibility Assessment**: 100% — The fundamental layout and aesthetic of the infographic demonstrated in the tutorial can be perfectly mapped to `python-pptx` vector objects. 

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "TIPS FOR WORKING\nFROM HOME",
    body_text: str = "As many people adapt to a work-from-home lifestyle, it is important to integrate key routines. Here are tips and techniques to ensure you are productive.",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Vertical Infographic Canvas' visual effect.
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE

    prs = Presentation()
    
    # 1. SET CUSTOM VERTICAL SLIDE DIMENSIONS (Core mechanism from tutorial)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(26.666)  # 1:2 ratio (Double standard height)
    
    # Use a blank slide layout
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)

    # --- Color Palette (Extracted from video style) ---
    c_header_bg = RGBColor(84, 106, 123)     # Slate Navy
    c_text_light = RGBColor(255, 255, 255)
    c_text_dark = RGBColor(40, 40, 40)
    
    # Alternating band colors
    band_colors = [
        RGBColor(115, 153, 172),  # Steel Blue
        RGBColor(226, 192, 143),  # Sand/Orange
        RGBColor(204, 214, 217),  # Light Gray
        RGBColor(115, 153, 172),  # Steel Blue (repeat)
        RGBColor(226, 192, 143),  # Sand/Orange (repeat)
    ]

    # Content for the infographic sections
    sections = [
        {"num": "1", "title": "ESTABLISH A ROUTINE", "icon": MSO_SHAPE.MATH_PLUS},
        {"num": "2", "title": "SCHEDULE BREAKS", "icon": MSO_SHAPE.MATH_MINUS},
        {"num": "3", "title": "EYE EXERCISES", "icon": MSO_SHAPE.OVAL},
        {"num": "4", "title": "CREATE A WORKSPACE", "icon": MSO_SHAPE.RECTANGLE},
        {"num": "5", "title": "AVOID DISTRACTIONS", "icon": MSO_SHAPE.MATH_MULTIPLY},
    ]

    # --- LAYOUT CALCULATIONS ---
    header_height = Inches(5.5)
    footer_height = Inches(3.0)
    available_section_height = prs.slide_height - header_height - footer_height
    section_height = available_section_height / len(sections)

    # === LAYER 1: Header Background ===
    header_bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, header_height
    )
    header_bg.fill.solid()
    header_bg.fill.fore_color.rgb = c_header_bg
    header_bg.line.fill.background() # No border

    # === LAYER 2: Header Content (Thick framed title box) ===
    # Frame Box
    frame_width = Inches(10)
    frame_height = Inches(3)
    frame_left = (prs.slide_width - frame_width) / 2
    frame_top = Inches(0.8)
    
    title_frame = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, frame_left, frame_top, frame_width, frame_height
    )
    title_frame.fill.solid()
    title_frame.fill.fore_color.rgb = RGBColor(245, 245, 245)
    title_frame.line.color.rgb = c_header_bg
    title_frame.line.width = Pt(8)

    tf = title_frame.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.name = 'Arial Black'
    p.font.size = Pt(64)
    p.font.color.rgb = c_header_bg

    # Header Subtext / Intro paragraph
    intro_box = slide.shapes.add_textbox(
        Inches(1.5), frame_top + frame_height + Inches(0.2), 
        Inches(10.333), Inches(1.5)
    )
    intro_tf = intro_box.text_frame
    intro_tf.word_wrap = True
    intro_p = intro_tf.paragraphs[0]
    intro_p.text = body_text
    intro_p.alignment = PP_ALIGN.CENTER
    intro_p.font.name = 'Arial'
    intro_p.font.size = Pt(22)
    intro_p.font.color.rgb = c_text_light

    # === LAYER 3: Dynamic Infographic Sections ===
    current_top = header_height

    for i, section in enumerate(sections):
        bg_color = band_colors[i % len(band_colors)]
        
        # 1. Band Background
        band = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, current_top, prs.slide_width, section_height
        )
        band.fill.solid()
        band.fill.fore_color.rgb = bg_color
        band.line.fill.background()

        # 2. Section Number (Large watermark style or bold text)
        num_box = slide.shapes.add_textbox(
            Inches(1.5), current_top + Inches(0.5), Inches(2), Inches(1)
        )
        num_p = num_box.text_frame.paragraphs[0]
        num_p.text = section["num"]
        num_p.font.name = 'Arial Black'
        num_p.font.size = Pt(60)
        num_p.font.color.rgb = c_text_dark

        # 3. Section Title
        title_box = slide.shapes.add_textbox(
            Inches(2.5), current_top + Inches(0.6), Inches(8), Inches(1)
        )
        title_p = title_box.text_frame.paragraphs[0]
        title_p.text = section["title"]
        title_p.font.name = 'Arial Black'
        title_p.font.size = Pt(44)
        title_p.font.color.rgb = c_text_dark
        
        # 4. Icon Placeholder (Using basic shape as placeholder for visual weight)
        icon_size = Inches(1.2)
        icon = slide.shapes.add_shape(
            section["icon"], 
            (prs.slide_width - icon_size) / 2, # Centered horizontally
            current_top + Inches(1.8),         # Placed below text
            icon_size, icon_size
        )
        icon.fill.solid()
        icon.fill.fore_color.rgb = c_header_bg
        icon.line.fill.background()

        current_top += section_height

    # === LAYER 4: Footer ===
    footer_bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, current_top, prs.slide_width, footer_height
    )
    footer_bg.fill.solid()
    footer_bg.fill.fore_color.rgb = c_header_bg
    footer_bg.line.fill.background()
    
    footer_box = slide.shapes.add_textbox(
        Inches(1.5), current_top + Inches(1), Inches(10.333), Inches(1)
    )
    footer_p = footer_box.text_frame.paragraphs[0]
    footer_p.text = "Save this presentation as a PDF to distribute as a scrolling infographic."
    footer_p.alignment = PP_ALIGN.CENTER
    footer_p.font.name = 'Arial'
    footer_p.font.size = Pt(24)
    footer_p.font.color.rgb = c_text_light

    prs.save(output_pptx_path)
    return output_pptx_path
```