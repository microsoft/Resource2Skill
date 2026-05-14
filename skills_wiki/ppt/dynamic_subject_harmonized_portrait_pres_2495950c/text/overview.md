# Dynamic Subject-Harmonized Portrait Presentation

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic Subject-Harmonized Portrait Presentation

* **Core Visual Mechanism**: The defining visual idea is **Subject-Background Color Harmony combined with Asymmetric Geometric Tension**. The background is no longer a separate environment; it is explicitly tied to the subject by extracting the dominant color from their attire. The addition of diagonal/slanted background shapes breaks the static grid, creating a sense of movement and modern editorial elegance. The subject is a cutout (no native background), allowing them to overlap these diagonal shapes, creating depth.

* **Why Use This Skill (Rationale)**: 
  * *Color extraction* creates immediate psychological unity. The viewer perceives the person and the slide as a single cohesive brand.
  * *Removing the background* brings the person forward, making eye contact and facial expressions more engaging.
  * *Diagonal elements* disrupt the expected horizontal/vertical reading patterns, injecting energy (rhythm and motion) into an otherwise static block of text.
  * *Strong text contrast* (mixing very dark and pure white text) naturally guides the eye through the hierarchy (Name -> Role -> Details).

* **Overall Applicability**: Ideal for executive profiles, speaker introductions, portfolio "About Me" pages, team rosters, and key character/persona slides in product marketing. 

* **Value Addition**: Transforms a standard "ID badge" layout into a high-end magazine editorial spread. It elevates the perceived status and professionalism of the person being introduced.

---

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **The Cutout Subject**: High-resolution person with a transparent background.
  - **Harmonized Color Palette**: 
    - Base Background: Dominant soft color from attire (e.g., Mauve/Pink `(226, 169, 184, 255)`).
    - Accent Geometric Shapes: Slightly darker/more saturated variant of the base `(205, 137, 153, 255)`.
  - **Text Hierarchy & Contrast**:
    - Primary (Name): Large, bold, very dark gray `(50, 50, 50, 255)` for heavy anchoring.
    - Secondary (Role/English Name): Medium/Small, pure white `(255, 255, 255, 255)` or lighter gray, often with increased letter spacing (tracking).
    - Tertiary (Details): Standard reading size, dark gray matching the name.
  - **Micro-interactions (Decorations)**: Fine lines and small circular bullets to organize detail text without adding bulk.

* **Step B: Compositional Style**
  - **Spatial Layout**: Asymmetrical two-column. The subject occupies the left 40-50% of the screen, anchoring the bottom edge. Text occupies the right 50%, aligned cleanly to a vertical grid.
  - **Depth Layering (Z-index)**: 
    1. Base solid color
    2. Slanted geometric color blocks
    3. The cutout person (overlapping the blocks)
    4. Typography and decorative lines

* **Step C: Dynamic Effects & Transitions**
  - The tutorial focuses on static layout optimization. However, this layout perfectly sets up a "Morph" transition (e.g., the subject sliding in from the left, while the diagonal blocks slide down from the top right).

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layered transparent cutout** | PIL/Pillow | To guarantee the code runs without relying on broken image URLs or complex ML background removal APIs, PIL generates a high-quality stylized RGBA (transparent) silhouette placeholder. |
| **Diagonal background blocks** | `python-pptx` native shapes | Parallelogram shapes with rotation easily reproduce the geometric "slanted" tension described in the video. |
| **Text hierarchy & coloring** | `python-pptx` native | Standard text boxes with specific font sizes, weight, and RGB colors perfectly achieve the contrast requirements. |

> **Feasibility Assessment**: 95%. The code fully recreates the layout logic, color harmony, geometric tension, and typographic hierarchy. The only abstraction is the use of a generated transparent silhouette instead of a real photograph of a person, ensuring 100% code execution reliability while perfectly demonstrating the layering effect.

#### 3b. Complete Reproduction Code

```python
import io
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def create_transparent_silhouette() -> io.BytesIO:
    """
    Generates a stylized RGBA image of a person (silhouette) with a transparent background.
    This simulates the "cutout" image effect without relying on external URLs.
    """
    img = Image.new("RGBA", (800, 1000), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a stylized person (head and shoulders/blazer)
    # Blazer color to represent the "clothing" that dictates the slide theme
    blazer_color = (200, 100, 120, 255) 
    skin_color = (240, 210, 190, 255)
    
    # Body / Blazer (Slanted shoulders)
    draw.polygon([(100, 1000), (300, 500), (500, 500), (700, 1000)], fill=blazer_color)
    # Head/Neck
    draw.rectangle([(360, 400), (440, 550)], fill=skin_color)
    draw.ellipse([(300, 200), (500, 450)], fill=skin_color)
    
    # Hair style
    draw.ellipse([(280, 180), (520, 350)], fill=(220, 180, 120, 255))
    
    # Shadow/Fold on blazer for depth
    draw.polygon([(300, 500), (400, 800), (500, 500)], fill=(180, 80, 100, 255))

    image_stream = io.BytesIO()
    img.save(image_stream, format='PNG')
    image_stream.seek(0)
    return image_stream

def create_slide(
    output_pptx_path: str = "Dynamic_Portrait_Profile.pptx",
    name_text: str = "Jenny Davis",
    role_text: str = "CREATIVE DIRECTOR",
    base_color: tuple = (226, 169, 184),   # Soft Mauve/Pink
    accent_shape_color: tuple = (205, 137, 153), # Darker Mauve
    text_dark: tuple = (50, 50, 50),
    text_light: tuple = (255, 255, 255),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Dynamic Subject-Harmonized Portrait" visual effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Solid Harmonized Background ===
    bg_rect = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg_rect.fill.solid()
    bg_rect.fill.fore_color.rgb = RGBColor(*base_color)
    bg_rect.line.fill.background() # No line

    # === Layer 2: Dynamic Diagonal Shapes ===
    # Adds visual rhythm and motion behind the subject
    diag1 = slide.shapes.add_shape(
        MSO_SHAPE.PARALLELOGRAM, Inches(4), Inches(-1), Inches(4), Inches(10)
    )
    diag1.rotation = 15
    diag1.fill.solid()
    diag1.fill.fore_color.rgb = RGBColor(*accent_shape_color)
    diag1.line.fill.background()

    diag2 = slide.shapes.add_shape(
        MSO_SHAPE.PARALLELOGRAM, Inches(7), Inches(-1), Inches(1), Inches(10)
    )
    diag2.rotation = 15
    diag2.fill.solid()
    diag2.fill.fore_color.rgb = RGBColor(*accent_shape_color)
    diag2.line.fill.background()

    # === Layer 3: Subject Image (Transparent Cutout) ===
    # Simulating the background removal by inserting an RGBA PNG
    img_stream = create_transparent_silhouette()
    slide.shapes.add_picture(
        img_stream, Inches(0.5), Inches(1.5), width=Inches(4.5)
    )

    # === Layer 4: Typography and Details ===
    
    # Name (Strong Contrast)
    name_box = slide.shapes.add_textbox(Inches(6.0), Inches(1.2), Inches(5), Inches(1))
    tf_name = name_box.text_frame
    p = tf_name.paragraphs[0]
    p.text = name_text
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(*text_dark)

    # Role (Weak Contrast / Secondary)
    role_box = slide.shapes.add_textbox(Inches(6.05), Inches(1.9), Inches(5), Inches(0.5))
    tf_role = role_box.text_frame
    p2 = tf_role.paragraphs[0]
    p2.text = role_text
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(*text_light)

    # Decorative Line
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(6.05), Inches(2.5), Inches(4), Inches(0.02)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(*text_light)
    line.line.fill.background()

    # Detail List (Bullet points with custom circles)
    details = [
        "Graduated from Columbia University",
        "Winner of IF Design Gold Award",
        "Served 50+ Fortune 500 companies",
        "Published multiple personal design portfolios"
    ]
    
    start_y = 3.0
    for i, detail in enumerate(details):
        y_pos = start_y + (i * 0.6)
        
        # Custom concentric circle bullet
        outer = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(6.05), Inches(y_pos + 0.05), Inches(0.15), Inches(0.15))
        outer.fill.background() # transparent
        outer.line.color.rgb = RGBColor(*text_light)
        outer.line.width = Pt(1)
        
        inner = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(6.08), Inches(y_pos + 0.08), Inches(0.09), Inches(0.09))
        inner.fill.solid()
        inner.fill.fore_color.rgb = RGBColor(*text_light)
        inner.line.fill.background()

        # Text
        det_box = slide.shapes.add_textbox(Inches(6.3), Inches(y_pos - 0.05), Inches(6), Inches(0.4))
        p_det = det_box.text_frame.paragraphs[0]
        p_det.text = detail
        p_det.font.size = Pt(14)
        p_det.font.color.rgb = RGBColor(*text_dark)
        
    # Logo Placeholder Top Right
    logo = slide.shapes.add_shape(MSO_SHAPE.DONUT, Inches(12.0), Inches(0.5), Inches(0.4), Inches(0.4))
    logo.fill.solid()
    logo.fill.fore_color.rgb = RGBColor(*text_dark)
    logo.line.fill.background()

    prs.save(output_pptx_path)
    return output_pptx_path

if __name__ == "__main__":
    create_slide()
```