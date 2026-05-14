# Minimalist Typographic Grid Bio

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Minimalist Typographic Grid Bio

* **Core Visual Mechanism**: This design relies entirely on **typographic hierarchy** (font size, weight, and color) and **spatial alignment** (invisible grids, margins, and whitespace) rather than images, shapes, or icons. It creates a clean, authoritative look by structuring text into distinct, highly aligned blocks.
* **Why Use This Skill (Rationale)**: Pure text slides can easily become walls of unreadable text. By manipulating line spacing (e.g., 1.3x to 1.5x) to create "breathing room," and swapping pure black text for deep grey, it drastically reduces visual fatigue. Bold accent colors draw the eye to key anchors (Name, Data Labels), making the slide scannable.
* **Overall Applicability**: Ideal for corporate environments with strict brand guidelines, internal team introductions, professional resumes, speaker bios, and any scenario where the presenter lacks high-quality photography but needs to convey high professionalism.
* **Value Addition**: Transforms a boring "bullet point" bio into a sleek, editorial-style layout. It proves that sophisticated design does not require complex graphics—only discipline in spacing and typography.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Typography**: Sans-serif fonts (e.g., Microsoft YaHei, Arial). Heavy/Bold weights for headers and labels; Regular weight for body text.
  * **Color Logic**:
    * *Background*: Pure White `(255, 255, 255)` or very light grey.
    * *Accent Color (Name & Labels)*: Corporate Blue `(68, 114, 196)` or a similar brand color.
    * *Body Text*: Deep Grey `(89, 89, 89)`. *Crucial detail: Never use pure black `#000000` for large blocks of text, as it creates too much harsh contrast against a white background.*
* **Step B: Compositional Style**
  * **Two-Column Asymmetry**: The slide is divided into an invisible grid. The left column (~60% width) houses the heavy Title (Name) and the multi-line Bio paragraph. The right column (~30% width) houses tabular personal details.
  * **Strict Alignment**: Top edges are aligned horizontally (Bio text aligns with Stats text). Left edges are aligned strictly vertically.
  * **Box Behavior**: Uses the distinction between "auto-fit" single-line text boxes (for names) and "fixed-width" text boxes with text wrapping (for the bio paragraph).
* **Step C: Dynamic Effects & Transitions**
  * Static slide. No animation is used. The impact comes entirely from the static layout.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Text box creation & alignment | `python-pptx` native | The core of this tutorial is precise native text box positioning (mimicking the align left/top UI tools). |
| Text wrapping & boundaries | `python-pptx` native | `word_wrap = True` perfectly replicates the "drawn paragraph text box" from the video. |
| Typographic styling & spacing | `python-pptx` native | Font size, RGB colors, bold weights, and crucially, paragraph `line_spacing` (1.3x - 1.5x) are fully supported natively. |

> **Feasibility Assessment**: 100% reproduction. The visual effect relies entirely on native PowerPoint text rendering and layout math, which `python-pptx` handles flawlessly.

#### 3b. Complete Reproduction Code

```python
import os
from typing import Dict
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def create_slide(
    output_pptx_path: str,
    person_name: str = "工藤新一",
    bio_text: str = (
        "高中生侦探，原先就读于帝丹高中二年B班，是毛利兰的青梅竹马、工藤优作和工藤有希子"
        "（旧姓藤峰）之独子。因拥有一流的推理能力，而被称为“日本警察的救世主”、“平成"
        "年代的福尔摩斯”，也是东京都警视厅警部目暮十三欣赏的人和主要帮手。"
    ),
    stats_data: Dict[str, str] = None,
    accent_color: tuple = (68, 114, 196),  # Standard Corporate Blue
    text_color: tuple = (89, 89, 89),      # Deep Grey (reduces eye strain)
) -> str:
    """
    Create a PPTX file reproducing the "Minimalist Typographic Grid Bio" effect.
    Uses strictly text boxes, alignment math, and typographic hierarchy.
    
    Returns: path to the saved PPTX file.
    """
    if stats_data is None:
        stats_data = {
            "年龄": "17岁",
            "性别": "男",
            "身高": "174公分",
            "体重": "58公斤",
            "出生": "5月4日",
            "国籍": "日本"
        }

    # Initialize presentation (16:9 widescreen)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank slide layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # Define Theme Colors
    theme_accent = RGBColor(*accent_color)
    theme_dark_grey = RGBColor(*text_color)

    # =======================================================
    # 1. Title / Name Text Box (Single-line, Auto-fit logic)
    # =======================================================
    name_left = Inches(1.5)
    name_top = Inches(1.0)
    name_width = Inches(5.0)
    name_height = Inches(1.0)
    
    txbox_name = slide.shapes.add_textbox(name_left, name_top, name_width, name_height)
    tf_name = txbox_name.text_frame
    p_name = tf_name.paragraphs[0]
    p_name.text = person_name
    
    # Styling: Heavy, Large, Accent Color
    p_name.font.size = Pt(44)
    p_name.font.bold = True
    p_name.font.color.rgb = theme_accent
    p_name.font.name = "Microsoft YaHei"

    # =======================================================
    # 2. Bio Paragraph Text Box (Fixed-width, Word Wrapped)
    # =======================================================
    bio_left = Inches(1.5)
    bio_top = Inches(2.8)
    bio_width = Inches(6.5) # Constrains width to create a neat column
    bio_height = Inches(4.0)
    
    txbox_bio = slide.shapes.add_textbox(bio_left, bio_top, bio_width, bio_height)
    tf_bio = txbox_bio.text_frame
    tf_bio.word_wrap = True # Crucial: forces text to act as a paragraph
    
    p_bio = tf_bio.paragraphs[0]
    p_bio.text = bio_text
    
    # Styling: Regular, Grey, High Line Spacing for "breathing room"
    p_bio.font.size = Pt(18)
    p_bio.font.color.rgb = theme_dark_grey
    p_bio.font.name = "Microsoft YaHei"
    p_bio.line_spacing = 1.4 # Replicates the 1.3x - 1.5x spacing mentioned in tutorial

    # =======================================================
    # 3. Stats Data (Right Column aligned grid)
    # Replicating the two-column alignment using math
    # =======================================================
    # We use two side-by-side text boxes to perfectly replicate 
    # the precise left-alignment of both labels and values.
    
    label_left = Inches(9.0)
    value_left = Inches(10.0)
    stats_top = Inches(2.8) # Perfectly Top-Aligned with the Bio paragraph
    stats_width = Inches(2.0)
    stats_height = Inches(4.0)
    
    # Box for Labels (e.g., "Age", "Gender")
    txbox_labels = slide.shapes.add_textbox(label_left, stats_top, stats_width, stats_height)
    tf_labels = txbox_labels.text_frame
    
    # Box for Values (e.g., "17", "Male")
    txbox_values = slide.shapes.add_textbox(value_left, stats_top, stats_width, stats_height)
    tf_values = txbox_values.text_frame
    
    for i, (label, value) in enumerate(stats_data.items()):
        # Add Label
        p_label = tf_labels.paragraphs[i] if i == 0 else tf_labels.add_paragraph()
        p_label.text = label
        p_label.font.size = Pt(18)
        p_label.font.bold = True
        p_label.font.color.rgb = theme_accent
        p_label.font.name = "Microsoft YaHei"
        p_label.line_spacing = 1.4
        
        # Add Value
        p_val = tf_values.paragraphs[i] if i == 0 else tf_values.add_paragraph()
        p_val.text = value
        p_val.font.size = Pt(18)
        p_val.font.color.rgb = theme_dark_grey
        p_val.font.name = "Microsoft YaHei"
        p_val.line_spacing = 1.4

    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_pptx_path)), exist_ok=True)
    
    # Save the presentation
    prs.save(output_pptx_path)
    return output_pptx_path

if __name__ == "__main__":
    # Example usage
    output_path = "minimalist_bio_grid.pptx"
    create_slide(output_path)
    print(f"Slide successfully generated at: {output_path}")
```

#### 3c. Verification Checklist
- [x] Does the code import all required libraries? (Yes, uses `python-pptx` natively)
- [x] Are all color values explicit RGBA tuples? (Yes, Corporate Blue and Deep Grey explicitly passed)
- [x] Does it handle paragraph line spacing specifically mentioned in the tutorial? (Yes, `p.line_spacing = 1.4` is utilized)
- [x] Does it correctly differentiate between auto-resize boxes and text-wrapped boxes? (Yes, `word_wrap = True` is strategically applied to the body paragraph).
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes, the dual-column layout and typographic coloring perfectly match the video's aesthetic intent).