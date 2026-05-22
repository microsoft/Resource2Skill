# Rule of Thirds Data Highlight Composition

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Rule of Thirds Data Highlight Composition

* **Core Visual Mechanism**: This design style applies an asymmetric 1:2 split based on the **Rule of Thirds**. The left third (or right third) is anchored by a high-quality, perfectly cropped photographic asset. The remaining two-thirds utilize aggressive **white space** and feature a minimalist, custom-built data visualization (such as a highlighted horizontal bar chart) that replaces traditional bullet points. 
* **Why Use This Skill (Rationale)**: Drawing directly from the tutorial, human eyes are naturally drawn to grid intersections (Rule of Thirds). Placing a human face or strong visual on the 1/3 line grabs attention, while the vast white space on the 2/3 side lowers cognitive load. By converting a list of percentages into a sorted bar chart with a single contrasting accent color, you guide the viewer's eye exactly to the most critical data point instantly.
* **Overall Applicability**: Ideal for survey results, executive summaries, pitch deck key metrics, or user persona slides where you need to combine a human/real-world element with hard data.
* **Value Addition**: Transforms a dull, cluttered list of statistics into a magazine-quality infographic. It forces brevity, creates breathing room, and ensures the core message is grasped in under 3 seconds.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Photography**: A single image cropped precisely to cover exactly 33.3% of the slide width. 
  - **Typography**: Sans-serif, highly legible text. A clear hierarchy with a large bold title, a brief descriptive subtitle, and clean data labels.
  - **Data Visualization**: Flat, scalable vector rectangles representing data. No axes, no gridlines.
  - **Color Logic**:
    - Background: Clean White `(255, 255, 255, 255)`
    - Primary Text: Dark Slate `(40, 40, 40, 255)`
    - Highlight Accent (Data Focus): Vibrant Teal `(81, 196, 171, 255)`
    - Secondary Data (De-emphasized): Light Gray `(220, 220, 220, 255)`

* **Step B: Compositional Style**
  - **Grid System**: 3x3 Rule of Thirds. Left vertical divider sits exactly at 33% (X = 4.44 inches).
  - **Layout**: Image occupies `0% to 33%` horizontally. Text and data occupy `40% to 90%`, leaving generous 10% margins for breathing room (implementing the "Use White Space" tip).
  - **Bar Proportions**: Bars have a fixed height (e.g., 0.4 inches) and dynamic widths scaled to the maximum available space, creating a crisp, scalable vector graphic look.

* **Step C: Dynamic Effects & Transitions**
  - Best paired with a **Wipe** transition from the left (matching the visual flow).
  - Data bars can be animated with a native PowerPoint "Wipe" from Left to Right, appearing sequentially to build the story.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Rule of Thirds Image Cropping | PIL/Pillow | Powerpoint's native picture insertion doesn't easily auto-crop to an exact aspect ratio (1:3 slide width) without distortion. PIL perfectly scales and crops the image before insertion. |
| Clean Typography & White Space | `python-pptx` native | Standard text frames are perfectly suited for grid-aligned, crisp typography. |
| Minimalist Bar Chart | `python-pptx` native shapes | To achieve the "scalable vector graphics" and "visualize data" tips, building the chart out of native vector rectangles ensures absolute crispness, perfect color control, and avoids the clunky default Excel chart UI. |

> **Feasibility Assessment**: 100% reproducible. The code directly translates the core principles of the tutorial—Rule of Thirds, White Space, and Visualized Highlighted Data—into a dynamically generated, precise layout.

#### 3b. Complete Reproduction Code

```python
import os
import io
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    title_text: str = "Availability Most Important Topic",
    subtitle_text: str = "Survey results show users prioritize product availability above all other factors when deciding to purchase.",
    image_keyword: str = "business,portrait",
    accent_color: tuple = (81, 196, 171),  # Vibrant Teal
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide implementing the "Rule of Thirds Data Highlight" pattern.
    Features a 1/3 cropped image on the left, and a clean, minimalist data visualization on the right.
    """
    # 1. Initialize Presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # Theme Colors
    bg_color = RGBColor(255, 255, 255)
    text_dark = RGBColor(40, 40, 40)
    text_gray = RGBColor(120, 120, 120)
    bar_bg_color = RGBColor(230, 230, 230)
    highlight_color = RGBColor(accent_color[0], accent_color[1], accent_color[2])

    # Slide Dimensions & Rule of Thirds calculation
    total_width = 13.333
    total_height = 7.5
    one_third_width = total_width / 3.0  # ~4.444 inches

    # === Layer 1: Rule of Thirds Photographic Asset ===
    # Fetch an image and crop it exactly to the 1/3 ratio
    target_width_px = int(one_third_width * 300) # 300 dpi approx
    target_height_px = int(total_height * 300)
    
    img_url = f"https://source.unsplash.com/featured/{target_width_px}x{target_height_px}/?{image_keyword}"
    
    try:
        req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            img_data = response.read()
            img = Image.open(io.BytesIO(img_data)).convert("RGB")
    except Exception as e:
        # Fallback: Create a sleek gradient placeholder if download fails
        img = Image.new("RGB", (target_width_px, target_height_px), color=(200, 200, 200))
        draw = ImageDraw.Draw(img)
        for y in range(target_height_px):
            r = int(240 - (240 - accent_color[0]) * (y / target_height_px))
            g = int(240 - (240 - accent_color[1]) * (y / target_height_px))
            b = int(240 - (240 - accent_color[2]) * (y / target_height_px))
            draw.line([(0, y), (target_width_px, y)], fill=(r, g, b))

    # Calculate exact crop to fit aspect ratio without stretching
    img_w, img_h = img.size
    target_ratio = target_width_px / target_height_px
    img_ratio = img_w / img_h

    if img_ratio > target_ratio:
        # Image is wider, crop sides
        new_w = int(img_h * target_ratio)
        left = (img_w - new_w) / 2
        img = img.crop((left, 0, left + new_w, img_h))
    else:
        # Image is taller, crop top/bottom
        new_h = int(img_w / target_ratio)
        top = (img_h - new_h) / 2
        img = img.crop((0, top, img_w, top + new_h))

    # Save to buffer and insert
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    
    slide.shapes.add_picture(img_buffer, Inches(0), Inches(0), width=Inches(one_third_width), height=Inches(total_height))

    # === Layer 2: Typography & White Space ===
    # Using the remaining 2/3 of the slide with generous margins
    margin_left = one_third_width + 0.8
    
    # Title
    title_box = slide.shapes.add_textbox(Inches(margin_left), Inches(0.8), Inches(7.5), Inches(1.0))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = text_dark
    p.font.name = "Arial"

    # Subtitle / Insight
    sub_box = slide.shapes.add_textbox(Inches(margin_left), Inches(1.6), Inches(7.5), Inches(0.8))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = text_gray
    p_sub.font.name = "Arial"

    # === Layer 3: Scalable Vector Data Visualization ===
    # Recreating the "Visualize Your Data" bar chart natively
    
    data_points = [
        ("Availability", 84),
        ("Price", 70),
        ("Service", 63),
        ("Online Shop", 33),
        ("Tech Support", 25)
    ]
    
    chart_start_y = 2.8
    bar_spacing = 0.7
    bar_height = 0.4
    label_width = 1.8
    max_bar_width = 5.5

    for i, (label, value) in enumerate(data_points):
        current_y = chart_start_y + (i * bar_spacing)
        
        # 1. Text Label
        lbl_box = slide.shapes.add_textbox(Inches(margin_left), Inches(current_y - 0.05), Inches(label_width), Inches(bar_height))
        tf_lbl = lbl_box.text_frame
        p_lbl = tf_lbl.paragraphs[0]
        p_lbl.text = label
        p_lbl.font.size = Pt(16)
        p_lbl.font.color.rgb = text_dark
        p_lbl.font.name = "Arial"
        p_lbl.alignment = PP_ALIGN.LEFT

        # 2. Vector Bar Shape
        # Is this the top/most important metric? Apply accent color.
        is_highlight = (i == 0) 
        fill_color = highlight_color if is_highlight else bar_bg_color
        
        calculated_width = max_bar_width * (value / 100.0)
        bar_x = margin_left + label_width
        
        bar_shape = slide.shapes.add_shape(
            1, # msoShapeRectangle
            Inches(bar_x), Inches(current_y), Inches(calculated_width), Inches(bar_height)
        )
        bar_shape.fill.solid()
        bar_shape.fill.fore_color.rgb = fill_color
        bar_shape.line.fill.background() # No outline

        # 3. Data Value Label inside/next to bar
        # For the highlight, make text white inside the bar. For others, make text dark outside the bar if it's small.
        # To keep it simple and clean, place it right-aligned inside the bar box if it's large enough, or just next to it.
        val_x = bar_x + 0.1 if is_highlight else bar_x + calculated_width + 0.1
        val_box = slide.shapes.add_textbox(Inches(val_x), Inches(current_y - 0.05), Inches(1.0), Inches(bar_height))
        tf_val = val_box.text_frame
        p_val = tf_val.paragraphs[0]
        p_val.text = f"{value}%"
        p_val.font.size = Pt(14)
        p_val.font.bold = True
        p_val.font.color.rgb = RGBColor(255,255,255) if is_highlight else text_dark
        p_val.font.name = "Arial"

    # Save Presentation
    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("rule_of_thirds_data_slide.pptx")
```