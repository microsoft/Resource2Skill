# Minimalist Architectural Grid Presentation

## Analysis

# Strategy Document: Presentation Board Design Pattern Extraction

### 1. High-level Design Pattern Extraction

> **Skill Name**: Minimalist Architectural Grid Presentation

* **Core Visual Mechanism**: The defining characteristic of this style is the **strict, visible underlying grid** and the strategic use of **negative space (whitespace)**. It relies on rigorous horizontal and vertical alignment of mixed media (text, hero images, analytical diagrams) to create a highly structured, editorial look. The aesthetic is clinical, professional, and entirely driven by layout rather than decorative elements.
* **Why Use This Skill (Rationale)**: When presenting dense, multifaceted information (like a building design, a complex data dashboard, or a multi-tiered business strategy), a rigid grid prevents cognitive overload. The hierarchy tells the viewer exactly where to look first (the Hero image), second (the title/concept), and third (the supporting analytical diagrams). Whitespace is used actively as a structural element to "let the images breathe."
* **Overall Applicability**: Perfect for architectural portfolios, product teardowns/showcases, case studies, strategic master plans, and mood boards. It excels wherever multiple distinct pieces of visual evidence must be synthesized into one cohesive narrative.
* **Value Addition**: Transforms a chaotic "scrapbook" of images and text into a curated, museum-quality exhibition board. It projects authority, precision, and organization.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: Unobtrusive and flat. Typically pure White `(255, 255, 255, 255)` or a very subtle off-white/light grey `(245, 245, 245, 255)`.
  - **Color Logic**: Monochromatic UI. The layout itself uses only greyscale—Black `(0, 0, 0, 255)` or Charcoal `(40, 40, 40, 255)` for text. Color is *only* introduced via the actual project images/diagrams, ensuring the content is the hero, not the slide template.
  - **Text Hierarchy**: 
    - **Project Title**: Large, bold, often tracked out (increased letter spacing), anchoring the top left.
    - **Subtitles/Headers**: Medium size, bold, acting as signposts for the grid sections.
    - **Body Text (Concept/Process)**: Small (10-12pt), justified or strictly left-aligned, set in a clean sans-serif (like Arial, Helvetica, or Segoe UI).

* **Step B: Compositional Style**
  - **Grid System**: The canvas is divided into strict modular columns and rows. Elements *never* float randomly; their edges align perfectly with adjacent elements.
  - **Proportions**: A classic 60/40 or 70/30 split. The primary "Hero" image (e.g., an exterior render) takes up 60% of the canvas width. The remaining 40% is subdivided into a smaller 2x2 or 1x3 grid for secondary information (plans, sections, data charts).
  - **Margins**: Generous outer margins (e.g., 0.5 to 1 inch all around) to frame the content like a printed poster.

* **Step C: Dynamic Effects & Transitions**
  - **Animation**: None. This is a print-inspired, static design. The motion is entirely guided by the viewer's eye moving through the visual hierarchy (from the largest image to the smallest details).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Strict Grid Layout** | `python-pptx` native | PPTX natively handles precise X, Y, Width, Height positioning in Inches, perfect for modular grid alignment. |
| **Architectural Visuals** | `PIL/Pillow` | To guarantee the aesthetic without relying on external image URLs (which break), PIL is used to generate sleek, minimalist "architectural diagrams" (grids, section cuts, plans) directly in memory to serve as the visual content. |
| **Typography & Hierarchy** | `python-pptx` native | Font sizes, RGB colors, and paragraph alignment can be precisely controlled via the PPTX API. |

> **Feasibility Assessment**: 100%. Because this design style relies on foundational graphic design principles (alignment, scale, typography, whitespace) rather than complex 3D rendering or proprietary PowerPoint effects, it can be perfectly reproduced using code.

#### 3b. Complete Reproduction Code

```python
import os
import io
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw

def _generate_arch_placeholder(width_in, height_in, diagram_type="hero"):
    """
    Generates a minimalist, architectural-style diagram using PIL.
    Ensures the code works perfectly offline and matches the domain aesthetic.
    """
    dpi = 150
    w_px = int(width_in * dpi)
    h_px = int(height_in * dpi)
    
    img = Image.new('RGBA', (w_px, h_px), (245, 245, 245, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw border
    border_color = (200, 200, 200, 255)
    draw.rectangle([0, 0, w_px-1, h_px-1], outline=border_color, width=2)
    
    if diagram_type == "hero":
        # Create a subtle perspective/isometric grid feel
        grid_color = (230, 230, 230, 255)
        for i in range(0, w_px, 40):
            draw.line([(i, 0), (i, h_px)], fill=grid_color, width=1)
        for i in range(0, h_px, 40):
            draw.line([(0, i), (w_px, i)], fill=grid_color, width=1)
            
        # Draw a "massing model" geometric shape
        accent = (80, 100, 120, 255)
        draw.polygon([(w_px*0.2, h_px*0.8), (w_px*0.5, h_px*0.3), (w_px*0.8, h_px*0.6), (w_px*0.8, h_px*0.9), (w_px*0.2, h_px*0.9)], fill=accent)
        draw.polygon([(w_px*0.2, h_px*0.8), (w_px*0.5, h_px*0.3), (w_px*0.4, h_px*0.8)], fill=(60, 80, 100, 255))

    elif diagram_type == "plan":
        # Top-down floor plan look
        wall_color = (50, 50, 50, 255)
        room_color = (220, 220, 220, 255)
        draw.rectangle([w_px*0.1, h_px*0.1, w_px*0.9, h_px*0.9], outline=wall_color, width=6, fill=room_color)
        draw.rectangle([w_px*0.1, h_px*0.4, w_px*0.5, h_px*0.4], outline=wall_color, width=4) # Inner wall
        draw.rectangle([w_px*0.6, h_px*0.1, w_px*0.6, h_px*0.6], outline=wall_color, width=4) # Inner wall

    elif diagram_type == "section":
        # Section cut look
        earth_color = (180, 180, 180, 255)
        structure_color = (30, 30, 30, 255)
        # Ground line
        draw.rectangle([0, h_px*0.7, w_px, h_px], fill=earth_color)
        # Building section
        draw.rectangle([w_px*0.25, h_px*0.3, w_px*0.75, h_px*0.7], outline=structure_color, width=5)
        # Roof
        draw.line([(w_px*0.2, h_px*0.3), (w_px*0.8, h_px*0.3)], fill=structure_color, width=8)

    img_stream = io.BytesIO()
    img.save(img_stream, format='PNG')
    img_stream.seek(0)
    return img_stream

def create_slide(
    output_pptx_path: str,
    title_text: str = "URBAN RENEWAL PAVILION",
    body_text: str = "The concept explores the intersection of brutalist massing and permeable public spaces. By elevating the primary structure, the ground plane is liberated for community interaction, while the strict geometric grid organizes the analytical programmatic spaces above. The design prioritizes natural light, material honesty, and clear structural hierarchy.",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Minimalist Architectural Grid Presentation effect.
    """
    prs = Presentation()
    # Use standard widescreen but treat it like a landscape presentation board
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Colors
    charcoal = RGBColor(40, 40, 40)
    light_grey = RGBColor(120, 120, 120)

    # ==========================================
    # GRID DEFINITION (Measurements in Inches)
    # ==========================================
    margin = 0.5
    gutter = 0.3 # Space between grid elements
    
    # Left Column (Hero)
    left_col_x = margin
    left_col_w = 7.5
    
    # Right Column (Analytical)
    right_col_x = left_col_x + left_col_w + gutter
    right_col_w = prs.slide_width.inches - right_col_x - margin

    # ==========================================
    # LAYER 1: TYPOGRAPHY & TEXT HIERARCHY
    # ==========================================
    # Title Box
    title_y = margin
    title_h = 1.2
    title_box = slide.shapes.add_textbox(Inches(left_col_x), Inches(title_y), Inches(left_col_w), Inches(title_h))
    tf = title_box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title_text.upper()
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.name = 'Arial'
    p.font.color.rgb = charcoal

    p2 = tf.add_paragraph()
    p2.text = "PROCESS & ANALYTICAL DIAGRAMS"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.name = 'Arial'
    p2.font.color.rgb = light_grey

    # Right Column Text Box (Concept Statement)
    concept_y = margin
    concept_h = 1.8
    concept_box = slide.shapes.add_textbox(Inches(right_col_x), Inches(concept_y), Inches(right_col_w), Inches(concept_h))
    ctf = concept_box.text_frame
    ctf.word_wrap = True
    
    cp1 = ctf.paragraphs[0]
    cp1.text = "CONCEPTUAL FRAMEWORK"
    cp1.font.size = Pt(12)
    cp1.font.bold = True
    cp1.font.color.rgb = charcoal
    
    cp2 = ctf.add_paragraph()
    cp2.text = body_text
    cp2.font.size = Pt(10)
    cp2.font.color.rgb = charcoal
    cp2.alignment = PP_ALIGN.JUSTIFY

    # ==========================================
    # LAYER 2: GRIDDED IMAGERY
    # ==========================================
    # Hero Image (Left Column)
    hero_y = title_y + title_h + gutter
    hero_h = prs.slide_height.inches - hero_y - margin
    hero_img_stream = _generate_arch_placeholder(left_col_w, hero_h, "hero")
    slide.shapes.add_picture(hero_img_stream, Inches(left_col_x), Inches(hero_y), Inches(left_col_w), Inches(hero_h))

    # Analytical Image 1 (Right Column, Top)
    img1_y = concept_y + concept_h + gutter
    img_h = (prs.slide_height.inches - img1_y - margin - gutter) / 2
    img1_stream = _generate_arch_placeholder(right_col_w, img_h, "plan")
    slide.shapes.add_picture(img1_stream, Inches(right_col_x), Inches(img1_y), Inches(right_col_w), Inches(img_h))
    
    # Add subtle caption for Image 1
    cap1 = slide.shapes.add_textbox(Inches(right_col_x), Inches(img1_y - 0.25), Inches(right_col_w), Inches(0.25))
    cap1.text_frame.text = "FIG 1: GROUND FLOOR PLAN"
    cap1.text_frame.paragraphs[0].font.size = Pt(8)
    cap1.text_frame.paragraphs[0].font.color.rgb = light_grey

    # Analytical Image 2 (Right Column, Bottom)
    img2_y = img1_y + img_h + gutter
    img2_stream = _generate_arch_placeholder(right_col_w, img_h, "section")
    slide.shapes.add_picture(img2_stream, Inches(right_col_x), Inches(img2_y), Inches(right_col_w), Inches(img_h))
    
    # Add subtle caption for Image 2
    cap2 = slide.shapes.add_textbox(Inches(right_col_x), Inches(img2_y - 0.25), Inches(right_col_w), Inches(0.25))
    cap2.text_frame.text = "FIG 2: TRANSVERSE SECTION"
    cap2.text_frame.paragraphs[0].font.size = Pt(8)
    cap2.text_frame.paragraphs[0].font.color.rgb = light_grey

    prs.save(output_pptx_path)
    return output_pptx_path
```