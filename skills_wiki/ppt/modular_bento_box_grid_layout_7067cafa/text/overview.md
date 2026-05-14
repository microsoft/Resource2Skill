# Modular Bento Box Grid Layout

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Modular Bento Box Grid Layout

* **Core Visual Mechanism**: Inspired by traditional Japanese lunchboxes, this design style uses an asymmetrical but perfectly aligned grid of rounded rectangles (cards or "cells"). The defining characteristic is the strict adherence to a uniform gutter (gap) between all elements, with varying block sizes (spanning different columns and rows) to create a visual hierarchy.
* **Why Use This Skill (Rationale)**: The Bento Box layout excels at organizing complex, disparate information into highly digestible, bite-sized visual chunks. By strictly containing different types of content (text, charts, images, icons) inside distinct, rounded modules, it dramatically lowers the cognitive load for the viewer.
* **Overall Applicability**: Perfect for dashboard slides, product feature highlight pages, portfolio overviews, table of contents/agenda slides, and summary slides where multiple distinct points need to be conveyed on a single screen without feeling cluttered.
* **Value Addition**: Transforms a standard bullet-point or scattered multi-image slide into a highly modern, sleek UI-inspired experience. It brings a "tech-forward" aesthetic (heavily popularized by Apple) to standard presentation design.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Shapes**: Exclusively rounded rectangles. Sharp corners are avoided to maintain the soft, modern aesthetic.
  - **Color Logic**: Highly effective in "Dark Mode". 
    - Background: Deep Dark Navy/Black `(13, 17, 28, 255)`.
    - Cards: Lighter elevated grays `(26, 32, 44, 255)` or vibrant accent colors for hero blocks `(88, 101, 242, 255)`.
  - **Text Hierarchy**: Bold, sans-serif typography. Content is nested with strict internal margins within each card. Top-left or centered alignment inside cells is standard.

* **Step B: Compositional Style**
  - **The Grid**: The layout relies on an invisible fractional grid (e.g., 4 columns by 3 rows, or 6x4).
  - **Spanning**: Cards take up fractional space (e.g., a "Hero" card might span 2 columns and 2 rows, while secondary metrics only span 1 column and 1 row).
  - **Spacing**: A strict, unvarying gap (e.g., 15-20 pixels) separates every single card, both horizontally and vertically. 

* **Step C: Dynamic Effects & Transitions**
  - While web Bento grids feature hover effects, in PowerPoint, this layout pairs beautifully with the **Morph transition**. Duplicating the slide and enlarging a single Bento cell to full-screen while shrinking the others creates an incredibly professional "drill-down" effect.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Grid Math & Layout** | Python Native Math | CSS Grid doesn't exist in PPTX. We must calculate exact X, Y, Width, and Height coordinates mathematically to simulate CSS fractional units (`fr`) and gap spacing. |
| **Bento Cells (Cards)** | `python-pptx` Shapes | PPTX's native `ROUNDED_RECTANGLE` is perfect for this. It allows for crisp rendering, adjustable corner radii, and embedded text. |
| **Card Content** | `python-pptx` TextFrames | Native text handling allows for proper internal padding (margins) within the shapes, ensuring text doesn't hit the edges. |

> **Feasibility Assessment**: **100% reproduction.** While we cannot use web-based CSS tools, math allows us to perfectly replicate a multi-span layout grid in PowerPoint. The output will look identical to a static web Bento Box.

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.text import MSO_ANCHOR

def create_slide(
    output_pptx_path: str,
    title_text: str = "Product Ecosystem",
    body_text: str = "Bento Grid Layout",
    bg_color: tuple = (13, 17, 28),         # Deep Navy/Black
    card_color_primary: tuple = (30, 35, 48), # Elevated Gray
    card_color_accent: tuple = (79, 70, 229), # Indigo/Purple Accent
    text_color_main: tuple = (255, 255, 255), # White
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Modular Bento Box Grid Layout.
    Calculates exact coordinates to simulate a CSS Grid layout with gaps.
    """
    prs = Presentation()
    # 16:9 widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # === Grid Configuration ===
    # We will simulate a 4 column x 3 row grid
    COLS = 4
    ROWS = 3
    MARGIN = Inches(0.6)   # Outer padding of the slide
    GAP = Inches(0.15)     # Gap between bento boxes

    # Calculate individual baseline cell dimensions
    usable_width = prs.slide_width - (2 * MARGIN) - (GAP * (COLS - 1))
    usable_height = prs.slide_height - (2 * MARGIN) - (GAP * (ROWS - 1))
    
    cell_w = usable_width / COLS
    cell_h = usable_height / ROWS

    # Helper function to calculate exact shape dimensions based on grid spans
    def get_bbox(col, row, col_span=1, row_span=1):
        x = MARGIN + (col * (cell_w + GAP))
        y = MARGIN + (row * (cell_h + GAP))
        w = (col_span * cell_w) + ((col_span - 1) * GAP)
        h = (row_span * cell_h) + ((row_span - 1) * GAP)
        return x, y, w, h

    # Helper function to create a Bento Card
    def add_bento_card(col, row, col_span, row_span, bg_rgb, title, desc, is_accent=False):
        x, y, w, h = get_bbox(col, row, col_span, row_span)
        
        # Add rounded rectangle
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        
        # Adjust corner rounding (lower number = less rounded, crisp modern look)
        shape.adjustments[0] = 0.08 if max(col_span, row_span) > 1 else 0.15
        
        # Styling the shape
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*bg_rgb)
        shape.line.fill.background() # No outline
        
        # Configure text box properties
        text_frame = shape.text_frame
        text_frame.word_wrap = True
        text_frame.vertical_anchor = MSO_ANCHOR.TOP
        
        # Internal padding (Bento boxes need breathing room)
        text_frame.margin_left = Inches(0.3)
        text_frame.margin_top = Inches(0.3)
        text_frame.margin_right = Inches(0.3)
        text_frame.margin_bottom = Inches(0.3)

        # Add Title
        p_title = text_frame.paragraphs[0]
        p_title.text = title
        p_title.font.bold = True
        p_title.font.size = Pt(24) if is_accent else Pt(18)
        p_title.font.color.rgb = RGBColor(*text_color_main)
        p_title.alignment = PP_ALIGN.LEFT
        
        # Add Description
        if desc:
            p_desc = text_frame.add_paragraph()
            p_desc.text = desc
            p_desc.font.size = Pt(14)
            # Make description slightly transparent/grayer based on background
            if is_accent:
                p_desc.font.color.rgb = RGBColor(200, 200, 255)
            else:
                p_desc.font.color.rgb = RGBColor(150, 160, 180)
            p_desc.alignment = PP_ALIGN.LEFT
            p_desc.space_before = Pt(8)

        return shape

    # === Layer 2: Visual Effect (The Bento Grid Placement) ===
    
    # Card 1: Hero Block (Top Left, spans 2 cols, 2 rows)
    add_bento_card(col=0, row=0, col_span=2, row_span=2, 
                   bg_rgb=card_color_accent, 
                   title=title_text, 
                   desc="A modular, highly responsive grid system that adapts perfectly to complex data visualization and content chunking.", 
                   is_accent=True)
    
    # Card 2: Top Right Wide (spans 2 cols, 1 row)
    add_bento_card(col=2, row=0, col_span=2, row_span=1, 
                   bg_rgb=card_color_primary, 
                   title="Seamless Integration", 
                   desc="Connects to 80 million data points instantly.")
    
    # Card 3: Mid Right Small (1x1)
    add_bento_card(col=2, row=1, col_span=1, row_span=1, 
                   bg_rgb=card_color_primary, 
                   title="99.9%", 
                   desc="Uptime SLA")
    
    # Card 4: Mid Far Right Small (1x1)
    add_bento_card(col=3, row=1, col_span=1, row_span=1, 
                   bg_rgb=card_color_primary, 
                   title="24/7", 
                   desc="Global Support")
    
    # Card 5: Bottom Left Small (1x1)
    add_bento_card(col=0, row=2, col_span=1, row_span=1, 
                   bg_rgb=card_color_primary, 
                   title="Secure", 
                   desc="End-to-end encrytion")

    # Card 6: Bottom Mid Small (1x1)
    add_bento_card(col=1, row=2, col_span=1, row_span=1, 
                   bg_rgb=card_color_primary, 
                   title="Fast", 
                   desc="<10ms latency")
    
    # Card 7: Bottom Right Wide (2x1)
    add_bento_card(col=2, row=2, col_span=2, row_span=1, 
                   bg_rgb=card_color_primary, 
                   title="Let's Manage Everything Together", 
                   desc="Access the full suite of smart tools right from the dashboard.")

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path

```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries? (Yes, `pptx` modules imported correctly).
- [x] Does it handle the case where an image download fails (fallback)? (Not applicable here; relies entirely on robust native vector math and shapes to build the grid, ensuring 100% reliability).
- [x] Are all color values explicit RGBA/RGB tuples? (Yes, explicit tuples defined in the function signature).
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes, it accurately calculates CSS-style fractional grid placements with exact gaps, forming a clean Bento Box UI).
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes, it visually captures the modern UI card trend highlighted in the video).