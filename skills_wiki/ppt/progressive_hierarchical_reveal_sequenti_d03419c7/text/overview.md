# Progressive Hierarchical Reveal (Sequential Builds)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Progressive Hierarchical Reveal (Sequential Builds)

* **Core Visual Mechanism**: The defining characteristic is the **sequential introduction of information**. Instead of presenting a dense wall of text, bullet points and their corresponding sub-bullets are revealed step-by-step (typically synchronized with the speaker's narrative). Visually, the style maintains a consistent spatial anchor—the text does not shift around; new lines simply "appear" in their pre-designated geometric slots.
* **Why Use This Skill (Rationale)**: This is a fundamental cognitive load management technique. If a slide contains five complex points, displaying them simultaneously encourages the audience to read ahead, splitting their attention and causing them to ignore the speaker. Progressive reveals force the audience to focus linearly on the current topic. 
* **Overall Applicability**: Essential for instructional content, step-by-step methodology breakdowns, complex technical explanations, and high-stakes pitch decks where narrative pacing is critical.
* **Value Addition**: Transforms a static reference document into a dynamic pacing tool. It creates a sense of momentum and keeps the presenter in absolute control of the information flow.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Typography & Hierarchy**: 
    - Title: Large, bold, anchored at the top or side.
    - Main Bullets (Level 1): Medium-large text (e.g., 24-28pt), high contrast color (e.g., White `(255, 255, 255)`).
    - Sub-bullets (Level 2): Smaller text (e.g., 18-20pt), slightly muted color (e.g., Light Grey `(180, 180, 180)`), indented horizontally.
  - **Color Logic**: A high-contrast theme works best for progressive reveals. 
    - Background: Deep slate/navy `(20, 25, 35)`.
    - Accent (Bullets): Bright Cyan `(0, 191, 255)`.
* **Step B: Compositional Style**
  - **Spatial Feel**: Structured and vertically aligned. A common modern layout places the slide title on the left 30% of the slide, while the bullet points occupy the right 70%, creating an asymmetrical, magazine-like balance.
  - **Vertical Rhythm**: Consistent padding between Level 1 points (e.g., 0.5 inches) and tighter padding between Level 2 points (e.g., 0.2 inches).
* **Step C: Dynamic Effects & Transitions**
  - **Animation Type**: "Appear" or "Fade".
  - **Sequencing**: "By Paragraph" (Level 1) or "By 2nd Level Paragraphs" (Level 2).
  - *Programmatic Note*: PowerPoint's native animation XML is incredibly volatile and difficult to generate safely via external code. The programmatic industry standard for this effect is **"Slide Builds"** (Stop-Motion slides)—generating a sequence of identical slides where each subsequent slide contains one additional bullet point. In Presentation mode, navigating through these slides perfectly simulates the "Click to Reveal" animation without risking file corruption.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Sequential Text Reveal | python-pptx (Slide Builds) | Injecting `<p:timing>` XML for paragraph-level animations is undocumented, highly fragile, and frequently causes PowerPoint to crash or corrupt files. Generating sequential slides (Builds) is the 100% robust programmatic standard for this effect. |
| Modern List Formatting | python-pptx native | Standard PPT text frames allow for `.level` attributes on paragraphs to handle indentation natively. |
| Layout & Colors | python-pptx native | `RGBColor` and shape manipulation handle the dark theme and accent styling easily. |

> **Feasibility Assessment**: 100% of the *presentation experience* is reproduced. When the user enters Slideshow mode and clicks "Next", the bullets will appear one by one exactly as they do in the tutorial. The only difference is that the file contains multiple static slides instead of one animated slide.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Key Deliverables",
    bullets_data: list = None,
    bg_color: tuple = (20, 25, 35),      # Deep slate
    text_color: tuple = (255, 255, 255), # White
    sub_color: tuple = (180, 180, 180),  # Light Grey
    accent_color: tuple = (0, 191, 255), # Cyan
    **kwargs,
) -> str:
    """
    Creates a PPTX file replicating the progressive bullet reveal effect using "Slide Builds".
    It generates a sequence of slides, adding one bullet/sub-bullet per slide.
    
    bullets_data should be a list of tuples: (level, text)
    e.g., [(0, "Main Point 1"), (1, "Sub Point 1"), (1, "Sub Point 2"), (0, "Main Point 2")]
    """
    from pptx import Presentation
    from pptx.util import Pt, Inches
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    
    if not bullets_data:
        bullets_data = [
            (0, "Phase 1: Market Research"),
            (1, "Competitor analysis"),
            (1, "Customer demographic surveys"),
            (0, "Phase 2: Product Development"),
            (1, "Initial prototyping"),
            (1, "Iterative QA testing"),
            (1, "Final design lock"),
            (0, "Phase 3: Go-to-Market Strategy"),
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank layout
    
    # We will generate one slide for each progressive step
    for step in range(1, len(bullets_data) + 1):
        slide = prs.slides.add_slide(blank_layout)
        
        # 1. Background
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(*bg_color)
        
        # 2. Side Accent Bar
        accent_bar = slide.shapes.add_shape(
            1, # Rectangle
            Inches(0), Inches(0), Inches(0.15), prs.slide_height
        )
        accent_bar.fill.solid()
        accent_bar.fill.fore_color.rgb = RGBColor(*accent_color)
        accent_bar.line.fill.background()
        
        # 3. Static Title (Left aligned, vertically centered-ish)
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(1), Inches(4), Inches(2))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.add_paragraph()
        p.text = title_text
        p.font.size = Pt(44)
        p.font.bold = True
        p.font.color.rgb = RGBColor(*text_color)
        p.font.name = "Arial"
        
        # Optional: Add a subtle divider line under title
        divider = slide.shapes.add_shape(
            1, Inches(0.8), Inches(2.2), Inches(1.5), Inches(0.05)
        )
        divider.fill.solid()
        divider.fill.fore_color.rgb = RGBColor(*accent_color)
        divider.line.fill.background()

        # 4. Bullet Points Container (Right side)
        # We draw only up to the current 'step'
        content_box = slide.shapes.add_textbox(Inches(5.5), Inches(1), Inches(7), Inches(5.5))
        content_tf = content_box.text_frame
        content_tf.word_wrap = True
        
        current_items = bullets_data[:step]
        
        for idx, (level, text) in enumerate(current_items):
            # First item modifies the default paragraph, subsequent ones add new
            p = content_tf.paragraphs[0] if idx == 0 else content_tf.add_paragraph()
            p.text = text
            p.level = level
            p.font.name = "Arial"
            
            # Styling based on level
            if level == 0:
                p.font.size = Pt(28)
                p.font.bold = True
                p.font.color.rgb = RGBColor(*text_color)
                # Adding some space before new main points (except the first)
                if idx > 0:
                    p.space_before = Pt(20)
            else:
                p.font.size = Pt(20)
                p.font.bold = False
                p.font.color.rgb = RGBColor(*sub_color)
                p.space_before = Pt(8)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("progressive_reveal.pptx")
```