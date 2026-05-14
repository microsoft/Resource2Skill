# Structured Narrative Framework

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Structured Narrative Framework

*   **Core Visual Mechanism**: This pattern establishes a clean, minimalist presentation structure that prioritizes clarity and narrative flow. It uses a professional, high-contrast color palette, strong typographic hierarchy, and generous white space to guide the audience's focus. The design is intentionally unobtrusive, serving to support the speaker's message rather than overwhelming it with visual noise.

*   **Why Use This Skill (Rationale)**: The framework is based on the principle that a presentation's primary goal is effective communication. By structuring the slides in a narrative arc—a strong opening, clearly demarcated sections, and a memorable closing—it helps the audience follow the speaker's logic. The minimalist aesthetic reduces cognitive load, ensuring the key messages and data are easily absorbed.

*   **Overall Applicability**: This is a foundational and highly versatile skill, ideal for:
    *   Corporate and business presentations (e.g., project proposals, quarterly reviews, internal training).
    *   Educational lectures and academic presentations.
    *   Any scenario where the clarity of the spoken message is paramount and the slides serve as a supporting guide.

*   **Value Addition**: Compared to a default, cluttered template, this style brings professionalism, focus, and a sense of deliberate structure. It forces the presenter to be concise and logical, directly implementing the best practices of outlining, narrative, and clarity taught in the tutorial.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    - **Elements**: The style relies on text boxes, simple lines for separation, and well-chosen fonts. Visuals like charts or images are meant to be added intentionally by the user into the provided clean canvas.
    - **Color Logic**: A high-contrast, professional palette is key.
        - Dark Background: `(34, 40, 49, 255)` — A deep, muted charcoal-navy.
        - Primary Text: `(238, 238, 238, 255)` — A soft, off-white for excellent readability.
        - Accent Color: `(0, 173, 181, 255)` — A vibrant teal for headers and key elements.
    - **Text Hierarchy**:
        - **Slide Titles/Headers**: Bold, accent-colored, and large (e.g., 32-36pt).
        - **Main Title (Title Slide)**: Very large and impactful (e.g., 48-54pt).
        - **Body Text**: Clear, legible font at a smaller size (e.g., 18-22pt) in the primary text color.
        - **Subtitle/Presenter Name**: Smallest tier, providing context without distraction (e.g., 16-18pt).

*   **Step B: Compositional Style**
    - **Layout**: The composition is clean and typically left-aligned, following natural reading patterns. White space is a critical active element, used to frame content and prevent slides from feeling crowded.
    - **Proportions**: Content rarely fills the entire slide. Headers might occupy the top 15-20% of the slide height, with body content occupying the central 50-60%, leaving ample margins.
    - **Layering**: The design is flat. A single background color layer with a text layer on top. A thin decorative line in the accent color may be placed under headers to add structure.

*   **Step C: Dynamic Effects & Transitions**
    - The tutorial does not cover animations or transitions. This skill focuses on static design principles. Simple, non-distracting transitions like "Fade" or "Push" could be applied manually in PowerPoint to enhance the flow between sections.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect                 | Method             | Why this method                                                                                                |
| ------------------------------------ | ------------------ | -------------------------------------------------------------------------------------------------------------- |
| Slide creation and layout            | `python-pptx` native | The skill is about structure, typography, and color, all of which are core strengths of the `python-pptx` library. |
| Background and color scheme          | `python-pptx` native | Solid color fills and shape/font coloring are handled directly and efficiently.                                  |
| Text hierarchy and formatting        | `python-pptx` native | Provides full control over font size, weight, color, and alignment for text boxes.                             |
| Simple decorative elements (lines)   | `python-pptx` native | Shapes like lines are easily created and styled.                                                               |

> **Feasibility Assessment**: 100%. This code fully reproduces the *design philosophy and structural recommendations* from the tutorial. The video teaches a process and a set of principles, and this code generates a template that embodies those principles perfectly.

#### 3b. Complete Reproduction Code

```python
def create_structured_narrative_deck(
    output_pptx_path: str,
    title_text: str = "Your Presentation Title",
    subtitle_text: str = "Engaging and memorable subtitle",
    presenter_name: str = "Your Name",
    opening_hook: str = "Start with a powerful question or a startling statistic to grab attention.",
    section_titles: list = ["First Key Point", "Second Key Point", "Third Key Point"],
    closing_message: str = "End with a strong, actionable take-home message.",
    **kwargs,
) -> str:
    """
    Creates a PPTX file based on the Structured Narrative Framework,
    embodying the design principles of clarity, structure, and narrative flow.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        title_text: The main title for the presentation.
        subtitle_text: The subtitle for the title slide.
        presenter_name: The name of the presenter.
        opening_hook: The text for the strong opening slide.
        section_titles: A list of strings for the main section header slides.
        closing_message: The final, memorable message for the closing slide.

    Returns:
        The path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE

    # --- Color Palette ---
    BG_COLOR = RGBColor(34, 40, 49)
    TEXT_COLOR = RGBColor(238, 238, 238)
    ACCENT_COLOR = RGBColor(0, 173, 181)

    # --- Presentation Setup ---
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    blank_layout = prs.slide_layouts[6]

    # --- Helper to set background ---
    def set_background(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = BG_COLOR
        return

    # --- Slide 1: Title Slide ---
    slide = prs.slides.add_slide(blank_layout)
    set_background(slide)

    title_box = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(14), Inches(2))
    title_p = title_box.text_frame.paragraphs[0]
    title_p.text = title_text
    title_p.font.bold = True
    title_p.font.size = Pt(54)
    title_p.font.color.rgb = TEXT_COLOR
    title_p.alignment = PP_ALIGN.CENTER

    subtitle_box = slide.shapes.add_textbox(Inches(1), Inches(4.5), Inches(14), Inches(1))
    subtitle_p = subtitle_box.text_frame.paragraphs[0]
    subtitle_p.text = subtitle_text
    subtitle_p.font.size = Pt(24)
    subtitle_p.font.color.rgb = TEXT_COLOR
    subtitle_p.alignment = PP_ALIGN.CENTER
    
    presenter_box = slide.shapes.add_textbox(Inches(1), Inches(7.5), Inches(14), Inches(1))
    presenter_p = presenter_box.text_frame.paragraphs[0]
    presenter_p.text = presenter_name
    presenter_p.font.size = Pt(18)
    presenter_p.font.color.rgb = TEXT_COLOR
    presenter_p.alignment = PP_ALIGN.CENTER

    # --- Slide 2: The Opening Hook ---
    slide = prs.slides.add_slide(blank_layout)
    set_background(slide)
    
    hook_box = slide.shapes.add_textbox(Inches(1.5), Inches(3), Inches(13), Inches(3))
    hook_p = hook_box.text_frame.paragraphs[0]
    hook_p.text = opening_hook
    hook_p.font.italic = True
    hook_p.font.size = Pt(32)
    hook_p.font.color.rgb = ACCENT_COLOR
    hook_p.alignment = PP_ALIGN.CENTER

    # --- Content Slides ---
    for title in section_titles:
        slide = prs.slides.add_slide(blank_layout)
        set_background(slide)

        header_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(14), Inches(1.0))
        header_p = header_box.text_frame.paragraphs[0]
        header_p.text = title
        header_p.font.bold = True
        header_p.font.size = Pt(36)
        header_p.font.color.rgb = ACCENT_COLOR
        
        line = slide.shapes.add_shape(MSO_SHAPE.LINE_INVERSE, Inches(1), Inches(1.5), Inches(5), Inches(0))
        line.line.color.rgb = ACCENT_COLOR
        line.line.width = Pt(2)
        
        content_box = slide.shapes.add_textbox(Inches(1), Inches(2.2), Inches(14), Inches(5.5))
        content_tf = content_box.text_frame
        content_tf.word_wrap = True
        
        p1 = content_tf.paragraphs[0]
        p1.text = "Use concise language here."
        p1.font.size = Pt(22)
        p1.font.color.rgb = TEXT_COLOR
        p1.level = 0
        
        p2 = content_tf.add_paragraph()
        p2.text = "Slides should support your message, not replace it."
        p2.font.size = Pt(20)
        p2.font.color.rgb = TEXT_COLOR
        p2.level = 1

    # --- Slide N: The Closing Message ---
    slide = prs.slides.add_slide(blank_layout)
    set_background(slide)
    
    closing_box = slide.shapes.add_textbox(Inches(1.5), Inches(3), Inches(13), Inches(3))
    closing_p = closing_box.text_frame.paragraphs[0]
    closing_p.text = closing_message
    closing_p.font.bold = True
    closing_p.font.size = Pt(32)
    closing_p.font.color.rgb = TEXT_COLOR
    closing_p.alignment = PP_ALIGN.CENTER
    
    # --- Final Slide: Thank You / Q&A ---
    slide = prs.slides.add_slide(blank_layout)
    set_background(slide)
    
    ty_box = slide.shapes.add_textbox(Inches(1.5), Inches(3.5), Inches(13), Inches(2))
    ty_p = ty_box.text_frame.paragraphs[0]
    ty_p.text = "Thank You"
    ty_p.font.bold = True
    ty_p.font.size = Pt(48)
    ty_p.font.color.rgb = ACCENT_COLOR
    ty_p.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx_path)
    return output_pptx_path

```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback)? (N/A - no images used)
- [x] Are all color values explicit RGB tuples (not referencing undefined variables)?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes, it reproduces the *principles* taught)
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes, in terms of structure and design philosophy)