# Diagonal Duotone Split (Magazine Cover Style)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Diagonal Duotone Split (Magazine Cover Style)

* **Core Visual Mechanism**: The slide background consists of a single photographic image, but it is diagonally split. One side of the split retains the original, full-color photograph, while the other side is converted to a monochrome/duotone tint (e.g., dark navy blue). This tinted geometric slice acts as an integrated, high-contrast backdrop for typography.
* **Why Use This Skill (Rationale)**: Overlaying text on full photographs often causes readability issues due to varying contrasts. Using a solid shape overlay feels disjointed. This technique solves the problem by keeping the texture and context of the photograph visible through the dark tint, bridging the gap between optimal text readability and striking visual aesthetics. The diagonal line adds a dynamic, modern energy.
* **Overall Applicability**: Ideal for magazine-style title slides, portfolio covers, impactful quotes, or chapter dividers where you want a premium, "editorial" aesthetic.
* **Value Addition**: Transforms a basic "text-over-image" slide into a sophisticated, multi-layered composition. It guides the viewer's eye directly to the text while maintaining the emotional impact of the photography.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: High-quality, context-relevant photograph.
  - **Tinted Overlay**: A geometric slice (typically a right triangle or angled polygon) of the same photograph, desaturated and tinted (e.g., Navy Blue `(20, 40, 70, 255)`).
  - **Text Hierarchy**: 
    - **Masthead**: Top center, large, sans-serif (e.g., Century Gothic), white `(255, 255, 255, 255)`.
    - **Feature Title**: Placed inside the tinted zone (bottom left), medium-large, white.
    - **Highlight Element**: A specific word or year in the title is highlighted in a vibrant contrasting color like Yellow `(255, 204, 0, 255)` to draw attention.

* **Step B: Compositional Style**
  - **Spatial Layout**: The slide is divided diagonally. The tinted portion usually occupies the bottom-left or bottom-half, creating a heavy, grounded area for the main feature text, while the top/right remains open and airy.
  - **Alignment**: Masthead is center-aligned; feature text is heavily left-aligned or aligned to follow the invisible grid created by the diagonal.

* **Step C: Dynamic Effects & Transitions**
  - In a slide environment, the overlay can be animated to "Slide In" from the bottom left, followed by a "Fade" for the text, emphasizing the layered construction. (Recreated via static layers in code for base template).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Image Tinting & Duotone | `PIL/Pillow` | `python-pptx` lacks native ability to apply artistic color filters/duotone effects to images programmatically. |
| Diagonal Image Slicing | `PIL/Pillow` | Using a polygon alpha mask in PIL ensures perfect pixel alignment and transparency without relying on complex PPTX shape intersections that often fail via API. |
| Typography Layout | `python-pptx` native | Best for maintaining editable text boxes with specific font sizes and color highlighting (like the yellow accent text). |

> **Feasibility Assessment**: 100%. By using `PIL` to pre-composite the duotone diagonal overlay as a transparent PNG, we perfectly replicate the visual effect while leaving the layout fully editable in PowerPoint.

#### 3b. Complete Reproduction Code

```python
import os
import urllib.request
from io import BytesIO
from PIL import Image, ImageDraw, ImageOps
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def create_slide(
    output_pptx_path: str,
    masthead_text: str = "Photo Magz",
    main_title: str = "Office\nIn Nature",
    highlight_year: str = "2024",
    bg_palette: str = "nature,office",
    tint_color: tuple = (15, 35, 60),  # Dark navy blue
    accent_color: tuple = (255, 204, 0) # Yellow highlight
) -> str:
    """
    Creates a PPTX file reproducing the 'Diagonal Duotone Split' magazine cover style.
    """
    # 1. Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    width_px, height_px = 1920, 1080

    # 2. Fetch or Generate Background Image
    try:
        url = f"https://source.unsplash.com/random/{width_px}x{height_px}/?{bg_palette}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            base_img = Image.open(BytesIO(response.read())).convert("RGBA")
            base_img = base_img.resize((width_px, height_px), Image.Resampling.LANCZOS)
    except Exception:
        # Fallback if download fails
        base_img = Image.new("RGBA", (width_px, height_px), (100, 120, 110, 255))
        draw = ImageDraw.Draw(base_img)
        draw.line([(0,0), (width_px, height_px)], fill=(120, 140, 130), width=10)

    # Save the base image
    base_img_path = "temp_base_bg.png"
    base_img.convert("RGB").save(base_img_path)

    # 3. Create the Duotone/Tinted Overlay Image
    # Convert to grayscale, then colorize with the tint color
    gray_img = base_img.convert("L")
    tinted_img = ImageOps.colorize(gray_img, black="black", white=tint_color).convert("RGBA")

    # 4. Create the Diagonal Mask
    # Triangle covering the bottom left
    mask = Image.new("L", (width_px, height_px), 0)
    mask_draw = ImageDraw.Draw(mask)
    # Define a polygon: from middle-left, down to bottom-left, across to bottom-right
    polygon_points = [
        (0, height_px * 0.25),   # Start a bit down from top left
        (0, height_px),          # Bottom left
        (width_px, height_px),   # Bottom right
        (width_px, height_px * 0.8) # Slight angle up on the right
    ]
    mask_draw.polygon(polygon_points, fill=255)

    # Apply the mask as alpha channel to the tinted image
    tinted_img.putalpha(mask)
    
    overlay_img_path = "temp_overlay_bg.png"
    tinted_img.save(overlay_img_path)

    # 5. Insert Images into PowerPoint
    # Insert Base Full-Color Image
    slide.shapes.add_picture(base_img_path, 0, 0, prs.slide_width, prs.slide_height)
    
    # Insert Tinted Overlay Image exactly on top
    slide.shapes.add_picture(overlay_img_path, 0, 0, prs.slide_width, prs.slide_height)

    # 6. Add Typography
    # Masthead (Top Center)
    tx_box_masthead = slide.shapes.add_textbox(Inches(0), Inches(0.5), prs.slide_width, Inches(1.5))
    tf_masthead = tx_box_masthead.text_frame
    tf_masthead.text = masthead_text
    p_masthead = tf_masthead.paragraphs[0]
    p_masthead.alignment = PP_ALIGN.CENTER
    p_masthead.font.name = "Century Gothic"
    p_masthead.font.size = Pt(64)
    p_masthead.font.bold = True
    p_masthead.font.color.rgb = RGBColor(255, 255, 255)

    # Feature Title (Bottom Left, over the tinted area)
    tx_box_title = slide.shapes.add_textbox(Inches(1.5), Inches(4.5), Inches(8), Inches(2))
    tf_title = tx_box_title.text_frame
    
    # Main Title Lines
    p_title = tf_title.paragraphs[0]
    p_title.text = main_title
    p_title.font.name = "Century Gothic"
    p_title.font.size = Pt(44)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255)
    
    # Highlight Year Line
    p_year = tf_title.add_paragraph()
    p_year.text = highlight_year
    p_year.font.name = "Century Gothic"
    p_year.font.size = Pt(44)
    p_year.font.bold = True
    p_year.font.color.rgb = RGBColor(accent_color[0], accent_color[1], accent_color[2])

    # Footer/Author (Bottom Center/Left)
    tx_box_footer = slide.shapes.add_textbox(Inches(1.5), Inches(6.8), Inches(5), Inches(0.5))
    tf_footer = tx_box_footer.text_frame
    tf_footer.text = "Citizen Photography / Design Issue"
    p_footer = tf_footer.paragraphs[0]
    p_footer.font.name = "Century Gothic"
    p_footer.font.size = Pt(14)
    p_footer.font.color.rgb = RGBColor(200, 200, 200)

    # Clean up temp files
    try:
        os.remove(base_img_path)
        os.remove(overlay_img_path)
    except OSError:
        pass

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# create_slide("magazine_cover_slide.pptx")
```