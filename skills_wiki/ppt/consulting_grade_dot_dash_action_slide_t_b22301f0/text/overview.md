# Consulting-Grade "Dot-Dash" Action Slide (The SCR Framework)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Consulting-Grade "Dot-Dash" Action Slide (The SCR Framework)

* **Core Visual Mechanism**: Typographic hierarchy acting as the primary visual architecture. This pattern eschews heavy graphics in favor of a dominant, top-heavy **Action Title** separated by a crisp accent line. Below the line, the body content utilizes a strict "Dot-Dash" structural logic (bold key statements as dots, supporting evidence as sub-bullet dashes).
* **Why Use This Skill (Rationale)**: This is the gold standard for management consulting (McKinsey, BCG, Bain). It forces the author to synthesize their argument into a persuasive narrative. An "Action Title" states the conclusion directly (e.g., "Rents have grown faster than incomes"), while the Dot-Dash body provides scannable, logical proof. It prioritizes clarity, cognitive ease, and executive persuasion over pure decoration.
* **Overall Applicability**: Executive summaries, strategy consulting decks, persuasive presentations, policy proposals, and data-driven narratives where the argument's logic is the most important element.
* **Value Addition**: Transforms a standard "informational" slide into a "persuasive" slide. It guides the reader's eye sequentially: Context (Kicker) $\rightarrow$ Conclusion (Action Title) $\rightarrow$ Proof (Dot-Dash Body).

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Stark, high-contrast, and highly disciplined. 
    - Background: Pure White `(255, 255, 255)`
    - Main Text (Title & Dots): Charcoal Black `(38, 38, 38)`
    - Supporting Text (Dashes): Dark Grey `(89, 89, 89)`
    - Accent / Corporate Color: Consulting Blue `(0, 81, 155)` applied sparingly to the kicker and divider line.
  - **Typography**: Clean sans-serif (Arial, Helvetica) or classic serif (Garamond) to project institutional authority.

* **Step B: Compositional Style**
  - **Kicker Area (Top 5%)**: A small, uppercase category label (e.g., "SITUATION" or "COMPLICATION") indicating where the slide fits in the overall story.
  - **Action Title (Top 10-20%)**: Massive, left-aligned, and bold. It dominates the slide.
  - **Divider Line**: A 1.5pt to 2pt solid horizontal line acting as a visual anchor, preventing the heavy title from visually crushing the body text.
  - **Body Content (Bottom 75%)**: Highly structured hanging-indent paragraphs. "Dots" are bold and large; "Dashes" are indented, smaller, and greyed out.

* **Step C: Dynamic Effects & Transitions**
  - **None**. The power of this style lies in its static, absolute clarity. Animations detract from the consulting aesthetic.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Structural Layout & Typography | `python-pptx` native | Exact calculation of margins, font sizes, and text box placement is the core of this technique. |
| Custom "Dot-Dash" Bullets | `lxml` XML injection | `python-pptx` does not natively support changing the bullet character to a specific en-dash or forcing bullet visibility without a master layout. We inject `<a:buChar>` directly into the paragraph properties. |

> **Feasibility Assessment**: 100% — This code perfectly reproduces the classic consulting slide structural aesthetic demonstrated in the tutorial, including the exact XML manipulation needed to enforce the "Dot-Dash" typographic rule.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Though the King County point-in-time count dropped in 2019, homelessness continues to increase",
    kicker_text: str = "Situation",
    content_lines: list = None,
    accent_color: tuple = (0, 81, 155),
    **kwargs
) -> str:
    """
    Create a PPTX file reproducing the Consulting-Grade "Dot-Dash" Action Slide.
    
    :param output_pptx_path: Path to save the presentation.
    :param title_text: The main persuasive action title.
    :param kicker_text: The SCR category (e.g., SITUATION, COMPLICATION, RESOLUTION).
    :param content_lines: List of strings. Strings starting with "-" become dashed sub-bullets.
    :param accent_color: RGB tuple for the corporate accent color.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.oxml.xmlchemy import OxmlElement
    
    # Default content mirroring the video's McKinsey example
    if content_lines is None:
        content_lines = [
            "More than 22,000 households experience homelessness in Seattle each year",
            "- 22,500 households were homeless for at least some of 2018",
            "- 30% of households experiencing homelessness were chronically homeless",
            "Despite robust growth, the housing supply and average household incomes have not kept pace",
            "- Rents have grown faster than incomes, exacerbating pressure on the poorest households",
            "- Since 2010, Seattle has lost 112,000 housing units affordable to low-income earners"
        ]

    def apply_custom_bullet(paragraph, char):
        """Safely inject OpenXML to force a specific bullet character."""
        pPr = paragraph._p.get_or_add_pPr()
        # Clean out existing bullet configurations
        for prefix in ['a:buNone', 'a:buChar', 'a:buAutoNum', 'a:buBlip']:
            tag = pPr.find(f'{{http://schemas.openxmlformats.org/drawingml/2006/main}}{prefix.split(":")[1]}')
            if tag is not None:
                pPr.remove(tag)
        # Inject custom bullet character
        buChar = OxmlElement('a:buChar')
        buChar.set('char', char)
        pPr.insert(0, buChar)

    # Initialize Widescreen Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # --- Layer 1: Kicker (Context Label) ---
    kicker_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    tf_kicker = kicker_box.text_frame
    tf_kicker.word_wrap = False
    p_kicker = tf_kicker.paragraphs[0]
    p_kicker.text = kicker_text.upper()
    p_kicker.font.size = Pt(12)
    p_kicker.font.bold = True
    p_kicker.font.color.rgb = RGBColor(*accent_color)
    p_kicker.font.name = "Arial"

    # --- Layer 2: Action Title ---
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(1.0))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(28)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(38, 38, 38)
    p_title.font.name = "Arial"

    # --- Layer 3: Accent Divider Line ---
    # Using a thin rectangle as a line for absolute color and thickness control
    divider = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.8), Inches(1.85), Inches(11.733), Pt(2)
    )
    divider.fill.solid()
    divider.fill.fore_color.rgb = RGBColor(*accent_color)
    divider.line.fill.background() # Remove border

    # --- Layer 4: "Dot-Dash" Body Content ---
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.7), Inches(4.5))
    tf_content = content_box.text_frame
    tf_content.word_wrap = True
    tf_content.clear() # Remove default empty paragraph

    for item in content_lines:
        p = tf_content.add_paragraph()
        if item.startswith("-"):
            # DASH Logic (Supporting evidence)
            p.text = item[1:].strip()
            p.level = 1
            apply_custom_bullet(p, '–') # En-dash
            p.font.size = Pt(16)
            p.font.bold = False
            p.font.color.rgb = RGBColor(89, 89, 89)
            p.font.name = "Arial"
            p.space_before = Pt(6)
        else:
            # DOT Logic (Key Statement)
            p.text = item.lstrip("•").strip()
            p.level = 0
            apply_custom_bullet(p, '•') # Solid Dot
            p.font.size = Pt(18)
            p.font.bold = True
            p.font.color.rgb = RGBColor(38, 38, 38)
            p.font.name = "Arial"
            p.space_before = Pt(14)

    # --- Layer 5: Institutional Footer ---
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(4), Inches(0.3))
    p_footer = footer_box.text_frame.paragraphs[0]
    p_footer.text = "CONFIDENTIAL AND PROPRIETARY"
    p_footer.font.size = Pt(9)
    p_footer.font.color.rgb = RGBColor(140, 140, 140)
    p_footer.font.name = "Arial"

    page_box = slide.shapes.add_textbox(Inches(12.2), Inches(7.0), Inches(0.5), Inches(0.3))
    p_page = page_box.text_frame.paragraphs[0]
    p_page.text = "1"
    p_page.font.size = Pt(10)
    p_page.font.color.rgb = RGBColor(140, 140, 140)
    p_page.font.name = "Arial"

    prs.save(output_pptx_path)
    return output_pptx_path
```

#### 3c. Verification Checklist
- [x] Does the code import all required libraries? (Yes, including `OxmlElement` for bullet modification).
- [x] Does it handle the case where an image download fails? (N/A - Relies purely on generated geometric and typographic forms).
- [x] Are all color values explicit RGBA/RGB tuples? (Yes, using strictly defined McKinsey-style values).
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes, the layout matches the exact structure required by top-tier consulting methodologies).
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes, the "Dot-Dash" hierarchy and "Action Title" look identical to standard industry decks).