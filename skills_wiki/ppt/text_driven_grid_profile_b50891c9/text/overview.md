# Text-Driven Grid Profile

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Text-Driven Grid Profile

* **Core Visual Mechanism**: Deconstructing a dense "wall of text" into semantic, visually distinct chunks using purely typographic contrast. It relies on a multi-column grid layout, varied font weights, selective accent coloring, and intentionally increased line spacing to create a clean, modern aesthetic without needing a single image or shape.
* **Why Use This Skill (Rationale)**: 
  * *Cognitive Load Reduction*: Large blocks of text intimidate readers. By separating the narrative (bio) from structured data (stats), the brain can process the information faster.
  * *Visual Breathing Room*: Increasing line spacing (1.3x - 1.5x) and avoiding pure black text (using dark grey instead) reduces eye strain and visual pressure, making the text look "high-end" and professionally typeset.
* **Overall Applicability**: Internal team introductions, speaker biographies, quick project role assignments, or resume slides where professional headshots are unavailable or unnecessary.
* **Value Addition**: Transforms a boring, default bullet-point slide into a magazine-like layout. It proves that professional design is often about *alignment, spacing, and hierarchy* rather than complex graphics.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Typography only**: The entire slide is built using 3-4 text boxes.
  * **Color Logic**:
    * Background: Pure White `(255, 255, 255, 255)`
    * Primary/Accent (Name, Data Labels): Corporate Blue `(93, 156, 227, 255)`. This draws the eye to the most critical anchor points.
    * Body Text: Dark Grey `(89, 89, 89, 255)`. *Never use pure black* for large blocks of text; dark grey looks significantly more refined.
  * **Text Hierarchy**:
    * **H1 (Name)**: 40pt+, Bold, Accent Color.
    * **Data Labels (Keys)**: 18-20pt, Bold, Accent Color.
    * **Body / Data Values**: 18-20pt, Regular weight, Dark Grey.

* **Step B: Compositional Style**
  * **Asymmetric 2-Column Grid**: 
    * The left column takes up ~60% of the canvas width, containing the Name and the Narrative Bio.
    * The right column takes up ~30% of the canvas width, containing structured key-value pairs.
  * **Alignment**: The narrative bio uses **Justified Alignment** so both left and right edges are perfectly straight, creating a neat block. The right column is strictly left-aligned. Top edges of the Bio and the Data block share the same horizontal Y-axis.

* **Step C: Dynamic Effects & Transitions**
  * None required. The power of this slide is in its static layout. Simple "Fade" transitions work best.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Multi-column layout | `python-pptx` native | Standard API is perfect for positioning distinct text boxes accurately. |
| Typographic styling (Bold, Colors) | `python-pptx` native | `Run` level formatting easily handles mixing colors within the same paragraph (for the key-value pairs). |
| Justified text & Line spacing | `python-pptx` native | `PP_ALIGN.JUSTIFY` and `paragraph.line_spacing` replicate the exact advice given in the tutorial. |

> **Feasibility Assessment**: 100%. The tutorial relies entirely on PowerPoint's native text frame manipulation, which maps perfectly to the `python-pptx` API. 

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    name: str = "Shinichi Kudo",
    bio_text: str = (
        "High school detective, originally studying in Class B, Year 2 at Teitan High School. "
        "He is the childhood friend of Ran Mouri, the only son of Yusaku Kudo and Yukiko Kudo. "
        "Possessing first-class deductive reasoning skills, he is known as the 'Savior of the Japanese Police' "
        "and the 'Sherlock Holmes of the Heisei Era'. He is also the main helper of Inspector Megure from the "
        "Tokyo Metropolitan Police Department, who highly appreciates his abilities."
    ),
    stats: dict = None,
    accent_color: tuple = (93, 156, 227),  # Soft Corporate Blue
    body_color: tuple = (89, 89, 89),      # Dark Grey (reduces visual pressure)
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Text-Driven Grid Profile" visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN

    if stats is None:
        stats = {
            "Age": "17",
            "Gender": "Male",
            "Height": "174 cm",
            "Weight": "58 kg",
            "DOB": "May 4th",
            "Nationality": "Japan"
        }

    prs = Presentation()
    # Set to 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a completely blank slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    accent_rgb = RGBColor(*accent_color)
    body_rgb = RGBColor(*body_color)

    # ==========================================
    # 1. H1 Header: Name Box (Top Left)
    # ==========================================
    name_box = slide.shapes.add_textbox(Inches(1.5), Inches(1.0), Inches(5.0), Inches(1.0))
    name_tf = name_box.text_frame
    name_tf.word_wrap = True
    
    p_name = name_tf.paragraphs[0]
    p_name.text = name
    p_name.font.size = Pt(44)
    p_name.font.bold = True
    p_name.font.name = "Arial" # Fallback clean sans-serif
    p_name.font.color.rgb = accent_rgb

    # ==========================================
    # 2. Narrative Block: Bio (Bottom Left)
    # ==========================================
    bio_box = slide.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(6.0), Inches(4.5))
    bio_tf = bio_box.text_frame
    bio_tf.word_wrap = True # Crucial for paragraph blocks
    
    p_bio = bio_tf.paragraphs[0]
    p_bio.text = bio_text
    p_bio.font.size = Pt(18)
    p_bio.font.name = "Arial"
    p_bio.font.color.rgb = body_rgb
    
    # Tutorial Key Insight: Justified alignment & 1.5 Line Spacing
    p_bio.alignment = PP_ALIGN.JUSTIFY
    p_bio.line_spacing = 1.5 

    # ==========================================
    # 3. Structured Data Block: Stats (Right)
    # ==========================================
    stats_box = slide.shapes.add_textbox(Inches(8.5), Inches(2.2), Inches(4.0), Inches(4.5))
    stats_tf = stats_box.text_frame
    stats_tf.word_wrap = True

    # Iterate through dictionary to build the key-value pairs
    first_paragraph = True
    for key, value in stats.items():
        if first_paragraph:
            p_stat = stats_tf.paragraphs[0]
            first_paragraph = False
        else:
            p_stat = stats_tf.add_paragraph()
            
        # Tutorial Key Insight: 1.5 Line Spacing for readability
        p_stat.line_spacing = 1.5
        
        # Add the Key (Bold, Accent Color)
        run_key = p_stat.add_run()
        # Add spaces for pseudo-column alignment between keys and values
        run_key.text = f"{key}    " 
        run_key.font.size = Pt(18)
        run_key.font.bold = True
        run_key.font.name = "Arial"
        run_key.font.color.rgb = accent_rgb
        
        # Add the Value (Regular, Dark Grey)
        run_val = p_stat.add_run()
        run_val.text = str(value)
        run_val.font.size = Pt(18)
        run_val.font.bold = False
        run_val.font.name = "Arial"
        run_val.font.color.rgb = body_rgb

    prs.save(output_pptx_path)
    return output_pptx_path
```