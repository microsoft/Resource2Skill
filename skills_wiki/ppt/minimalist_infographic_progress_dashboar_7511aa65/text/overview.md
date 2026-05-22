# Minimalist Infographic Progress Dashboard

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Minimalist Infographic Progress Dashboard

* **Core Visual Mechanism**: The defining visual signature is the translation of standard bar charts into sleek, UI-inspired "progress sliders." This is achieved using layered horizontal track lines, vibrant colored fill bars, minimalist tick marks for scale (25%, 50%, 75%), and custom "pin/speech bubble" callouts indicating the final percentage. 
* **Why Use This Skill (Rationale)**: Standard PowerPoint bar charts often feel heavy and overly corporate. By disaggregating the data into distinct rows with generous white space and using UI-slider aesthetics, the information becomes much easier to scan. It leverages the psychological satisfaction of "progress bars" (completion states) to make data comparison more engaging.
* **Overall Applicability**: Ideal for project status updates, OKR (Objectives and Key Results) reviews, comparing demographic segments, or highlighting three distinct statistical points in a hero presentation.
* **Value Addition**: Transforms a dry numerical comparison into an airy, modern, infographic-style slide. It creates a strong visual hierarchy where the category name, description, and quantitative value are perfectly balanced horizontally.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: High-contrast, clean UI colors against a pure white background `(255, 255, 255)`. 
    - Text/Titles: Slate Black `(51, 51, 51)` and Medium Grey `(128, 128, 128)`.
    - Accent 1 (Task 1): Crimson Red `(214, 40, 40)`.
    - Accent 2 (Task 2): Vibrant Teal `(42, 157, 143)`.
    - Accent 3 (Task 3): Ocean Blue `(0, 119, 182)`.
    - Track Lines: Very light grey `(220, 220, 220)`.
  - **Text Hierarchy**: 
    - Main Title: Centered, all-caps, heavy weight.
    - Category Title: Left-aligned, colored to match its data bar, bold, medium size.
    - Category Description: Left-aligned, grey, small size, regular weight.
    - Data Label (Inside Pin): White, bold, distinct.

* **Step B: Compositional Style**
  - **Grid & Spacing**: The slide uses a ~25% / 75% vertical split. The left 25% contains the text metadata. The right 75% acts as the data visualization canvas. 
  - **Alignment**: The track lines anchor the visual weight. The data callouts (pins) "float" exactly at the tip of the data bar, creating a jagged, dynamic visual line down the right side of the slide depending on the percentages.

* **Step C: Dynamic Effects & Transitions**
  - *Tutorial approach*: Uses a "Motion Path (Lines)" animation for the colored bars to slide out from left to right, unmasking themselves from behind a white background rectangle. The data pins use a "Float In" animation triggered after the bar finishes sliding.
  - *Code Reproduction*: The code below will generate the static, completed infographic state (which is the primary design asset). Complex timing-based motion paths require deep XML modification and are highly specific to manual presentation pacing.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Base Layout & Text** | `python-pptx` native | Clean placement of text boxes, font color, and size management. |
| **Progress Tracks & Bars** | `python-pptx` native | Rectangle shapes layered in precise Z-order (Back track -> tick marks -> fill bar) flawlessly mimic the UI slider look. |
| **Custom Percentage "Pin"** | `python-pptx` native (Shape grouping strategy) | PowerPoint's native callouts are hard to control via API. We perfectly overlap a `ROUNDED_RECTANGLE` and an `ISOSCELES_TRIANGLE` rotated 180° to create the custom speech bubble. |

> **Feasibility Assessment**: 100% reproduction of the visual end-state. The Python code automatically calculates the precise X-coordinates for the bars and the custom pins based on the input percentages.

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_slide(
    output_pptx_path: str,
    title_text: str = "ANIMATED COMPARISON SLIDE DESIGN",
    data_points: list = None,
    **kwargs
) -> str:
    """
    Creates a sleek, minimalist infographic progress dashboard slide.
    
    :param output_pptx_path: Path to save the presentation.
    :param title_text: Main slide title.
    :param data_points: List of dictionaries containing 'title', 'desc', 'pct', and 'color' (RGB tuple).
    """
    # Default data if none provided
    if not data_points:
        data_points = [
            {
                "title": "TASK ONE", 
                "desc": "You can write some text here\nto describe any information\nabout the heading above.", 
                "pct": 75, 
                "color": (214, 40, 40)   # Red
            },
            {
                "title": "TASK TWO", 
                "desc": "You can write some text here\nto describe any information\nabout the heading above.", 
                "pct": 50, 
                "color": (42, 157, 143)  # Teal
            },
            {
                "title": "TASK THREE", 
                "desc": "You can write some text here\nto describe any information\nabout the heading above.", 
                "pct": 25, 
                "color": (0, 119, 182)   # Blue
            }
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Constants for layout
    SLATE_BLACK = RGBColor(51, 51, 51)
    GREY_TEXT = RGBColor(128, 128, 128)
    TRACK_COLOR = RGBColor(230, 230, 230)
    TICK_COLOR = RGBColor(180, 180, 180)
    
    # 1. Main Title
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(0.5), Inches(11.333), Inches(0.8))
    tf = title_box.text_frame
    tf.text = title_text
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Montserrat" # Will fallback to Arial if not installed
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = SLATE_BLACK

    # Coordinates and dimensions for the bars
    start_y = 2.0
    spacing_y = 1.6
    
    text_x = Inches(1.0)
    text_w = Inches(3.0)
    
    track_x = Inches(4.5)
    track_w_inches = 7.5
    track_w = Inches(track_w_inches)
    track_h = Inches(0.12)
    
    # Generate the 3 tasks
    for i, data in enumerate(data_points):
        current_y = Inches(start_y + (i * spacing_y))
        accent_color = RGBColor(*data["color"])
        
        # --- Left Side: Text ---
        # Category Title
        cat_box = slide.shapes.add_textbox(text_x, current_y - Inches(0.2), text_w, Inches(0.4))
        cat_tf = cat_box.text_frame
        cat_p = cat_tf.paragraphs[0]
        cat_p.text = data["title"]
        cat_p.font.name = "Montserrat"
        cat_p.font.size = Pt(20)
        cat_p.font.bold = True
        cat_p.font.color.rgb = accent_color
        
        # Category Description
        desc_box = slide.shapes.add_textbox(text_x, current_y + Inches(0.15), text_w, Inches(0.8))
        desc_tf = desc_box.text_frame
        desc_tf.word_wrap = True
        desc_p = desc_tf.paragraphs[0]
        desc_p.text = data["desc"]
        desc_p.font.name = "Arial"
        desc_p.font.size = Pt(11)
        desc_p.font.color.rgb = GREY_TEXT
        
        # --- Right Side: The Data Track ---
        # 1. Background Track
        track = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, track_x, current_y + Inches(0.15), track_w, track_h)
        track.fill.solid()
        track.fill.fore_color.rgb = TRACK_COLOR
        track.line.color.rgb = TRACK_COLOR
        
        # 2. Tick marks (0%, 25%, 50%, 75%, 100%)
        num_segments = 4
        segment_w = track_w_inches / num_segments
        for j in range(num_segments + 1):
            tick_x = track_x + Inches(j * segment_w)
            tick = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, tick_x, current_y + Inches(0.1), Inches(0.03), Inches(0.22))
            tick.fill.solid()
            tick.fill.fore_color.rgb = TICK_COLOR
            tick.line.color.rgb = TICK_COLOR
            
        # 3. Colored Fill Bar
        fill_w = Inches(track_w_inches * (data["pct"] / 100.0))
        # Ensure it has a tiny minimum width so it renders even at 0%
        fill_w = max(fill_w, Inches(0.05))
        
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, track_x, current_y + Inches(0.15), fill_w, track_h)
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent_color
        bar.line.color.rgb = accent_color
        
        # 4. Data Label (The Custom "Pin" Callout)
        pin_x_center = track_x + fill_w
        
        # Pin Triangle (Pointer)
        tri_w = Inches(0.2)
        tri_h = Inches(0.15)
        tri = slide.shapes.add_shape(
            MSO_SHAPE.ISOSCELES_TRIANGLE, 
            pin_x_center - (tri_w/2), 
            current_y - Inches(0.02), 
            tri_w, 
            tri_h
        )
        tri.rotation = 180 # Point downwards
        tri.fill.solid()
        tri.fill.fore_color.rgb = accent_color
        tri.line.color.rgb = accent_color
        
        # Pin Rectangle (Body)
        rect_w = Inches(0.8)
        rect_h = Inches(0.4)
        rect = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, 
            pin_x_center - (rect_w/2), 
            current_y - Inches(0.4), 
            rect_w, 
            rect_h
        )
        rect.adjustments[0] = 0.2 # Slight rounding
        rect.fill.solid()
        rect.fill.fore_color.rgb = accent_color
        rect.line.color.rgb = accent_color
        
        # Text inside the Pin
        rect_tf = rect.text_frame
        rect_tf.margin_left = 0
        rect_tf.margin_right = 0
        rect_tf.margin_top = 0
        rect_tf.margin_bottom = 0
        rect_p = rect_tf.paragraphs[0]
        rect_p.alignment = PP_ALIGN.CENTER
        rect_p.text = f"{data['pct']}%"
        rect_p.font.name = "Arial"
        rect_p.font.size = Pt(12)
        rect_p.font.bold = True
        rect_p.font.color.rgb = RGBColor(255, 255, 255)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("animated_comparison_dashboard.pptx")
```