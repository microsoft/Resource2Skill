# High-Contrast Oversized Number Divider

## Analysis

# Role: Agent_Skill_Distiller (PPTX Design Style & Pattern Extractor)

### 1. High-level Design Pattern Extraction

> **Skill Name**: High-Contrast Oversized Number Divider

* **Core Visual Mechanism**: This design pattern relies on **extreme scale contrast** and **stark two-tone color blocking**. It uses a vibrant vertical side-panel to house a massive, vertically-centered numeral, contrasting against a dark primary background that contains bold, multi-colored typography. The defining signature is the flat, modern, vector-based aesthetic devoid of gradients, shadows, or complex imagery.

* **Why Use This Skill (Rationale)**: The human eye is naturally drawn to high contrast and large elements. By isolating the list number at an exaggerated scale in a bright container, it visually anchors the viewer to the structure of the presentation. The two-tone typography reinforces hierarchy, allowing the presenter to emphasize key action verbs or subjects within a single continuous statement without relying on bullet points.

* **Overall Applicability**: Perfect for listicle-style presentations, agendas, key takeaways, transition slides between major topics, and "Top 10" countdowns. It shines in webinar environments, product marketing videos, and corporate pitch decks where clarity and impact are paramount.

* **Value Addition**: Transforms a standard bulleted list into a series of impactful, highly memorable standalone statements. It forces the content to be concise and creates an energetic, rhythmic pacing as the audience moves from point to point.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Color Logic**: Flat, high-contrast, complementary-adjacent colors. 
    * Primary Background (Deep Navy): `RGBA(23, 43, 61, 255)`
    * Accent Panel & Highlight Text (Vibrant Canary Yellow): `RGBA(253, 209, 39, 255)`
    * Base Text (Pure White): `RGBA(255, 255, 255, 255)`
  * **Text Hierarchy**: 
    * **The Anchor**: A gigantic numeral (e.g., 200pt+) using an ultra-bold sans-serif font.
    * **The Statement**: A large (48pt - 60pt) title statement, split across 2-3 lines, utilizing two different colors (yellow and white) to break up the sentence visually without using punctuation.

* **Step B: Compositional Style**
  * **Spatial Layout**: The slide is divided asymmetrically. The left ~25% (roughly 3.5 inches of a 13.33-inch slide) acts as a solid color column. The right 75% contains the text.
  * **Alignment**: The massive number is perfectly center-aligned both horizontally and vertically within its left panel. The main statement is left-aligned within the right panel, creating a clean, invisible vertical margin.

* **Step C: Dynamic Effects & Transitions**
  * This style thrives on simple, hard cuts or rapid horizontal "Push" transitions in PowerPoint. Because the layout is rigid and flat, pushing the slide from right-to-left creates a seamless, endless-carousel effect.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Split-screen color blocking | `python-pptx` native shapes | Flat rectangles perfectly reproduce the solid geometric background panels. |
| Oversized Typography | `python-pptx` native text boxes | Native text runs easily support extreme font sizes (200pt+) and arbitrary alignment. |
| Two-tone title text | `python-pptx` native text runs | Allows seamless application of alternating RGB colors within a single paragraph/text box. |

> **Feasibility Assessment**: 100% reproduction. Because the core visual mechanism relies purely on geometric layout, solid high-contrast colors, and bold typographic hierarchy (flat design), `python-pptx` natively excels at producing this exact result without the need for external image processing or complex XML injection.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    list_number: str = "5",
    title_part1: str = "Canva gives you access",
    title_part2: str = "to a lot more templates",
    bg_color: tuple = (23, 43, 61),      # Deep Navy
    accent_color: tuple = (253, 209, 39), # Vibrant Yellow
    text_color: tuple = (255, 255, 255),  # White
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "High-Contrast Oversized Number Divider" visual effect.
    
    Args:
        output_pptx_path: Filepath to save the .pptx file.
        list_number: The large digit/number to display in the side panel.
        title_part1: The first part of the statement (colored in accent color).
        title_part2: The second part of the statement (colored in white).
        bg_color: RGB tuple for the main dark background.
        accent_color: RGB tuple for the left panel and highlighted text.
        text_color: RGB tuple for the standard text.
        
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    
    # Initialize presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Extract color tuples to RGBColor objects
    c_bg = RGBColor(*bg_color)
    c_accent = RGBColor(*accent_color)
    c_text = RGBColor(*text_color)

    # === Layer 1: Background ===
    # Set the main slide background color
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = c_bg

    # === Layer 2: Visual Structure (The Split Panel) ===
    # Add the vertical accent panel on the left
    panel_width = Inches(3.5)
    left_panel = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        0, 0, panel_width, prs.slide_height
    )
    left_panel.fill.solid()
    left_panel.fill.fore_color.rgb = c_accent
    left_panel.line.fill.background() # Remove border

    # === Layer 3: Typography ===
    
    # 1. The Oversized Anchor Number
    num_box = slide.shapes.add_textbox(
        Inches(0), Inches(2.25), panel_width, Inches(3.0)
    )
    num_frame = num_box.text_frame
    num_frame.clear() # clear default paragraphs
    num_p = num_frame.paragraphs[0]
    num_p.alignment = PP_ALIGN.CENTER
    num_run = num_p.add_run()
    num_run.text = str(list_number)
    
    # Styling the oversized number
    font = num_run.font
    font.name = "Arial Black" # Use a widely available heavy font
    font.size = Pt(220)
    font.color.rgb = c_bg # Number inherits the dark background color for contrast

    # 2. The Main Statement (Two-Tone Text)
    # Positioned with generous left padding away from the yellow panel
    text_box = slide.shapes.add_textbox(
        Inches(4.2), Inches(2.5), Inches(8.5), Inches(3.0)
    )
    text_frame = text_box.text_frame
    text_frame.word_wrap = True
    
    p = text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    p.line_spacing = 1.1

    # Run 1: Highlighted Text (Yellow)
    run1 = p.add_run()
    run1.text = title_part1 + "\n"
    run1.font.name = "Arial Black"
    run1.font.size = Pt(54)
    run1.font.color.rgb = c_accent
    
    # Run 2: Base Text (White)
    run2 = p.add_run()
    run2.text = title_part2
    run2.font.name = "Arial Black"
    run2.font.size = Pt(54)
    run2.font.color.rgb = c_text

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
```

#### 3c. Verification Checklist
- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails? *(N/A - purely geometric/native rendering)*
- [x] Are all color values explicit RGBA/RGB tuples (not referencing undefined variables)?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?
- [x] Would someone looking at the output say "yes, that's the same technique"?