# Organic Grid Reveal Sequence

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Organic Grid Reveal Sequence

* **Core Visual Mechanism**: A structured 2x2 grid layout presenting a numbered list or "Table of Contents," set against a soft, organic "botanical" background featuring abstract blobs and dotted textures. The defining functional mechanism is the **sequential reveal**—items appear one by one to guide audience focus.
* **Why Use This Skill (Rationale)**: Presenting all information at once can overwhelm the audience. By combining a soothing organic aesthetic with a step-by-step reveal (achieved via animations in PowerPoint, or via sequential slides programmatically), you control the narrative pacing and keep the audience engaged with the current point.
* **Overall Applicability**: Perfect for agendas, table of contents, core competency summaries (e.g., resumes, as seen in the video), or multi-step process overviews.
* **Value Addition**: Transforms a basic bulleted list into a highly visual, structured, and paced narrative element. The organic shapes soften the rigidity of a standard grid.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Background Aesthetic**: "Sage Botanical" theme. 
    * Base Canvas: Light Sage `(212, 217, 205, 255)`
    * Abstract Blobs: Muted Pine `(100, 124, 106, 255)` and Dark Forest `(47, 62, 51, 255)`
    * Textures: Clusters of small dots to add depth without clutter.
  * **Badges**: Circular number indicators in Mid-Sage `(161, 178, 154, 255)`.
  * **Typography**: Bold serif fonts for titles (elegance), clean sans-serif for body text (readability). Dark text color `(48, 59, 51)` ties into the green theme.

* **Step B: Compositional Style**
  * **Header**: Anchored top-left, large and bold.
  * **Grid**: 2 columns x 2 rows. Items are spaced generously. 
  * **Micro-layout**: Within each item, the numbered badge is positioned to the left. The item title and description are vertically stacked to the right of the badge.

* **Step C: Dynamic Effects & Transitions**
  * **Tutorial Approach**: Native PowerPoint "Appear" or "Fade" entrance animations set to "On Click".
  * **Code Reproduction Strategy**: Because `python-pptx` does not natively support writing complex animation timing XML, the most robust way to programmatically generate a "reveal" effect is via **Slide Sequencing** (generating a series of slides, adding one new item per slide). When presented, advancing the slide creates the exact same visual "appear" effect as an animation, with 100% compatibility across all PDF and presentation viewers.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Organic Background Blobs & Textures** | `PIL/Pillow` | Native PPTX shapes are hard to make beautifully abstract and organic. PIL allows precise drawing of smooth overlapping ellipses, slices, and dot patterns saved as a flat background layer. |
| **Grid Layout & Number Badges** | `python-pptx` native | Standard shape (OVAL) and text frame positioning are perfect for the structured grid content. |
| **Sequential "Appear" Effect** | Algorithmic (Slide Sequence) | `python-pptx` lacks API support for slide animations. Generating a sequence of slides where elements build up iteratively accurately reproduces the *visual experience* of clicking to reveal. |

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    main_title: str = "Table of contents",
    animate_via_slides: bool = True
) -> str:
    """
    Create a presentation reproducing the 'Organic Grid Reveal Sequence'.
    
    :param animate_via_slides: If True, generates a sequence of 5 slides to simulate 
                               the "appear one-by-one" animation. If False, generates 1 complete slide.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- Color Palette ---
    COLOR_BG = (212, 217, 205)
    COLOR_BLOB_LIGHT = (100, 124, 106)
    COLOR_BLOB_DARK = (47, 62, 51)
    COLOR_BADGE = (161, 178, 154)
    COLOR_TEXT = (48, 59, 51)
    
    # --- Generate Organic Background using PIL ---
    bg_path = "temp_organic_bg.png"
    img_width, img_height = int(13.333 * 100), int(7.5 * 100)
    bg_img = Image.new('RGBA', (img_width, img_height), COLOR_BG + (255,))
    draw = ImageDraw.Draw(bg_img)
    
    # Top right organic shape (simulated with overlapping circles)
    draw.ellipse((img_width - 400, -200, img_width + 300, 500), fill=COLOR_BLOB_LIGHT + (255,))
    draw.ellipse((img_width - 200, 100, img_width + 400, 700), fill=COLOR_BLOB_LIGHT + (255,))
    
    # Bottom left geometric/organic shape
    draw.pieslice((-200, img_height - 300, 300, img_height + 200), 270, 360, fill=COLOR_BLOB_DARK + (255,))
    draw.pieslice((-100, img_height - 400, 400, img_height + 100), 180, 270, fill=COLOR_BLOB_DARK + (255,))
    
    # Dot pattern top left
    for row in range(4):
        for col in range(5):
            x = 800 + col * 20
            y = 150 + row * 20
            draw.ellipse((x, y, x+4, y+4), fill=COLOR_TEXT + (255,))
            
    # Dot pattern bottom left
    for row in range(5):
        for col in range(3):
            x = 150 + col * 20
            y = 550 + row * 20
            draw.ellipse((x, y, x+4, y+4), fill=COLOR_TEXT + (255,))
            
    bg_img.save(bg_path)

    # --- Content Data ---
    items = [
        {"num": "01", "title": "Experience", "desc": "You can describe the topic of\nthe section here"},
        {"num": "02", "title": "Education", "desc": "You can describe the topic of\nthe section here"},
        {"num": "03", "title": "Skills", "desc": "You can describe the topic of\nthe section here"},
        {"num": "04", "title": "Interests/hobbies", "desc": "You can describe the topic of\nthe section here"}
    ]

    # Grid coordinates
    col_x = [Inches(3.5), Inches(8.0)]
    row_y = [Inches(3.0), Inches(5.0)]

    # --- Slide Generation Logic ---
    total_steps = len(items) if animate_via_slides else 0
    
    for step in range(total_steps + 1):
        slide = prs.slides.add_slide(blank_layout)
        
        # 1. Add Background
        slide.shapes.add_picture(bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
        
        # 2. Add Main Title
        title_box = slide.shapes.add_textbox(Inches(1.5), Inches(1.0), Inches(8), Inches(1))
        tf = title_box.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = main_title
        p.font.size = Pt(44)
        p.font.bold = True
        p.font.name = "Georgia"
        p.font.color.rgb = RGBColor(*COLOR_TEXT)
        
        # 3. Reveal Grid Items based on the current step
        items_to_show = step if animate_via_slides else len(items)
        
        for i in range(items_to_show):
            item = items[i]
            c_idx = i % 2
            r_idx = i // 2
            
            x_base = col_x[c_idx]
            y_base = row_y[r_idx]
            
            # Draw Badge (Circle)
            badge_size = Inches(1.1)
            badge = slide.shapes.add_shape(
                MSO_SHAPE.OVAL, 
                x_base, y_base, 
                badge_size, badge_size
            )
            badge.fill.solid()
            badge.fill.fore_color.rgb = RGBColor(*COLOR_BADGE)
            badge.line.fill.background() # No outline
            
            # Badge Text
            btf = badge.text_frame
            btf.text = item["num"]
            btf.paragraphs[0].alignment = PP_ALIGN.CENTER
            btf.paragraphs[0].font.size = Pt(28)
            btf.paragraphs[0].font.bold = True
            btf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255) # White text on badge
            # Adjust vertical alignment
            badge.text_frame.margin_top = Inches(0.25)
            
            # Item Title
            t_box = slide.shapes.add_textbox(x_base + Inches(1.3), y_base - Inches(0.1), Inches(3.5), Inches(0.5))
            ttf = t_box.text_frame
            ttf.word_wrap = True
            tp = ttf.paragraphs[0]
            tp.text = item["title"]
            tp.font.size = Pt(24)
            tp.font.bold = True
            tp.font.name = "Georgia"
            tp.font.color.rgb = RGBColor(*COLOR_TEXT)
            
            # Item Description
            d_box = slide.shapes.add_textbox(x_base + Inches(1.3), y_base + Inches(0.35), Inches(3.5), Inches(0.8))
            dtf = d_box.text_frame
            dtf.word_wrap = True
            dp = dtf.paragraphs[0]
            dp.text = item["desc"]
            dp.font.size = Pt(14)
            dp.font.name = "Arial"
            dp.font.color.rgb = RGBColor(*COLOR_TEXT)

    prs.save(output_pptx_path)
    
    # Cleanup temp file
    if os.path.exists(bg_path):
        os.remove(bg_path)
        
    return output_pptx_path
```