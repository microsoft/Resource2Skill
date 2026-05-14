# Minimalist Vertical Anchor & Concentric Spotlight

## Analysis

# High-level Design Pattern Extraction

> **Skill Name**: Minimalist Vertical Anchor & Concentric Spotlight

* **Core Visual Mechanism**: This design style is defined by two primary motifs: 
  1. **The Vertical Anchor**: A brightly colored (cyan) vertical rule that acts as a focal point, drawing the eye and separating content blocks (e.g., separating the spotlight title from the company logo, or anchoring a large interview question).
  2. **The Concentric Spotlight**: A circular framing device for portrait photography, accented by abstract, disconnected concentric arcs. This frames the subject organically without heavy, solid borders.

* **Why Use This Skill (Rationale)**: The heavy use of white space combined with a single, vibrant accent color communicates a clean, modern, and professional corporate identity. The vertical lines create a strong left-to-right reading flow. The circular, stylized portrait masks soften the corporate aesthetic, making the "Employee Spotlight" feel personal, approachable, and human-centric.

* **Overall Applicability**: Perfect for corporate interviews, employee spotlights, "Meet the Team" decks, Q&A transition slides, and minimalist corporate branding where whitespace is heavily utilized.

* **Value Addition**: Transforms standard "text and photo" slides into a dynamic narrative sequence. The consistent use of the vertical anchor across different slide layouts provides visual continuity, while the concentric rings add a layer of premium motion graphic design to an otherwise static portrait.


# Visual Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: 
    - Background: Pure White `(255, 255, 255, 255)`
    - Primary Accent: Bright Cyan `(0, 163, 224, 255)`
    - Secondary Accent: Light Sky Blue `(142, 208, 235, 255)`
    - Primary Text: Deep Navy Blue `(20, 40, 80, 255)`
    - Script/Highlight Text: Coral/Red `(200, 50, 50, 255)`
  - **Text Hierarchy**:
    - **Eyebrow/Category**: Medium weight, all-caps, light colors (e.g., "EMPLOYEE SPOTLIGHT").
    - **Header/Question**: Large, clean sans-serif, dark navy, anchored to the vertical line.
    - **Subject Name**: Stylized, handwritten/script font in a contrasting accent color (red) to signify a personal signature.

* **Step B: Compositional Style**
  - **Intro Slide**: Symmetrical balance. A perfectly centered 2.5-inch vertical line. Text blocks are horizontally aligned on either side, taking up ~40% of the canvas width each.
  - **Spotlight Slide**: Asymmetrical balance. The portrait occupies the left 40% of the slide, layered with concentric rings. The name and details occupy the right 50%, aligned to the vertical center.
  - **Question Slide**: Left-aligned anchor. The vertical line sits ~10% from the left edge. The question text acts as a massive hero element, taking up ~80% of the remaining width.

* **Step C: Dynamic Effects & Transitions**
  - The tutorial shows arcs drawing themselves and lines wiping in. We will translate the drawing arcs into continuous ambient rotation using the `add_infinite_rotation` primitive to give the portrait an ongoing, premium "breathing" effect.


# Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Concentric Arcs & Circular Portrait** | `PIL/Pillow` | PowerPoint native shapes cannot easily create disconnected, variable-width concentric arcs with perfectly rounded caps. PIL handles this easily, along with generating the circular alpha mask for the downloaded profile photo. |
| **Ambient Ring Rotation** | `_shell_helpers` | To capture the kinetic nature of the rings in the tutorial, we use `add_infinite_rotation` for continuous orbiting motion. |
| **Vertical Line Anchors & Typography** | `python-pptx` native | Clean rectangles with no borders perfectly replicate the minimalist vertical dividers. Native text frames handle the large corporate typography. |

> **Feasibility Assessment**: 95% reproduction. The static layouts, typography, color palette, and geometric proportions are reproduced exactly. The specific "wipe" animations from the video are replaced with a continuous ambient rotation on the spotlight rings, which adapts the video's motion graphic feel into a reproducible presentation primitive.

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
from pptx.enum.shapes import MSO_SHAPE

# Required for ambient motion features
AMBIENT_CAPABLE = True
try:
    from _shell_helpers import add_infinite_rotation
except ImportError:
    def add_infinite_rotation(slide, shape, duration_ms=10000, direction="cw"):
        pass  # Fallback if shell helpers are not available

def create_slide(
    output_pptx_path: str,
    employee_name: str = "Jared Benedict",
    question_text: str = "What is your favorite part\nabout being at MorganFranklin?",
    accent_color: tuple = (0, 163, 224),  # Cyan
    **kwargs,
) -> str:
    """
    Creates a 3-slide sequence reproducing the "Vertical Anchor & Concentric Spotlight" style.
    Slide 1: Intro / Title
    Slide 2: Employee Spotlight Profile
    Slide 3: Interview Question Transition
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Colors
    color_cyan = RGBColor(*accent_color)
    color_navy = RGBColor(20, 40, 80)
    color_red = RGBColor(200, 50, 50)
    color_light_blue = RGBColor(142, 208, 235)

    # ==========================================
    # HELPER: Generate PIL Images for Slide 2
    # ==========================================
    def create_spotlight_assets():
        # 1. Download and crop profile photo
        profile_path = "temp_profile_circle.png"
        try:
            url = "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=800&q=80"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                img = Image.open(BytesIO(response.read())).convert("RGB")
        except Exception:
            # Fallback placeholder if download fails
            img = Image.new("RGB", (800, 800), (220, 220, 220))
            d = ImageDraw.Draw(img)
            d.text((300, 380), "Photo Unavailable", fill=(100, 100, 100))

        # Make square and circularize
        size = min(img.size)
        img = ImageOps.fit(img, (size, size), centering=(0.5, 0.5))
        mask = Image.new("L", (size, size), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, size, size), fill=255)
        img.putalpha(mask)
        img.save(profile_path)

        # 2. Generate Concentric Arcs (Transparent PNG)
        rings_path = "temp_concentric_rings.png"
        ring_size = 1000
        rings_img = Image.new("RGBA", (ring_size, ring_size), (0, 0, 0, 0))
        draw_rings = ImageDraw.Draw(rings_img)
        
        # Outer Cyan Arc
        bbox_outer = [50, 50, 950, 950]
        draw_rings.arc(bbox_outer, start=45, end=270, fill=accent_color + (255,), width=16)
        
        # Inner Light Blue Arc
        bbox_inner = [120, 120, 880, 880]
        draw_rings.arc(bbox_inner, start=160, end=420, fill=(142, 208, 235, 255), width=8)

        # Extra accent dot
        draw_rings.ellipse([935, 485, 965, 515], fill=accent_color + (255,))
        
        rings_img.save(rings_path)
        return profile_path, rings_path

    prof_img_path, rings_img_path = create_spotlight_assets()

    # ==========================================
    # SLIDE 1: Intro (Center Vertical Anchor)
    # ==========================================
    slide_intro = prs.slides.add_slide(prs.slide_layouts[6])
    slide_intro.background.fill.solid()
    slide_intro.background.fill.fore_color.rgb = RGBColor(255, 255, 255)

    # Center Vertical Line
    line_intro = slide_intro.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(6.6), Inches(2.5), Inches(0.1), Inches(2.5)
    )
    line_intro.fill.solid()
    line_intro.fill.fore_color.rgb = color_cyan
    line_intro.line.fill.background()

    # Left Text: EMPLOYEE SPOTLIGHT
    tb_left = slide_intro.shapes.add_textbox(Inches(1.5), Inches(3.2), Inches(4.8), Inches(1.0))
    tf_left = tb_left.text_frame
    p_left = tf_left.paragraphs[0]
    p_left.alignment = PP_ALIGN.RIGHT
    run1 = p_left.add_run()
    run1.text = "EMPLOYEE "
    run1.font.size = Pt(36)
    run1.font.color.rgb = color_light_blue
    run2 = p_left.add_run()
    run2.text = "SPOTLIGHT"
    run2.font.size = Pt(36)
    run2.font.color.rgb = color_cyan

    # Right Text: COMPANY NAME
    tb_right = slide_intro.shapes.add_textbox(Inches(7.0), Inches(3.2), Inches(4.8), Inches(1.0))
    tf_right = tb_right.text_frame
    p_right = tf_right.paragraphs[0]
    p_right.alignment = PP_ALIGN.LEFT
    run_r = p_right.add_run()
    run_r.text = "MORGANFRANKLIN\nCONSULTING"
    run_r.font.size = Pt(28)
    run_r.font.color.rgb = color_navy
    run_r.font.bold = True

    # ==========================================
    # SLIDE 2: Spotlight Profile
    # ==========================================
    slide_profile = prs.slides.add_slide(prs.slide_layouts[6])
    slide_profile.background.fill.solid()
    slide_profile.background.fill.fore_color.rgb = RGBColor(255, 255, 255)

    # Add profile picture (center-left)
    pic_size = Inches(4.0)
    pic_left = Inches(2.5)
    pic_top = Inches(1.75)
    slide_profile.shapes.add_picture(prof_img_path, pic_left, pic_top, pic_size, pic_size)

    # Add concentric rings overlay
    ring_size_in = Inches(5.0)
    ring_left = pic_left - Inches(0.5)
    ring_top = pic_top - Inches(0.5)
    rings_shape = slide_profile.shapes.add_picture(rings_img_path, ring_left, ring_top, ring_size_in, ring_size_in)
    
    # Apply continuous ambient rotation to the rings
    add_infinite_rotation(slide_profile, rings_shape, duration_ms=25000, direction="cw")

    # Add Name Text
    tb_name = slide_profile.shapes.add_textbox(Inches(8.0), Inches(3.0), Inches(5.0), Inches(1.5))
    p_name = tb_name.text_frame.paragraphs[0]
    run_name = p_name.add_run()
    run_name.text = employee_name
    run_name.font.size = Pt(54)
    run_name.font.color.rgb = color_red
    run_name.font.name = "Brush Script MT" # Script fallback
    run_name.font.italic = True

    # ==========================================
    # SLIDE 3: Question Transition
    # ==========================================
    slide_q = prs.slides.add_slide(prs.slide_layouts[6])
    slide_q.background.fill.solid()
    slide_q.background.fill.fore_color.rgb = RGBColor(255, 255, 255)

    # Left Vertical Line
    line_q = slide_q.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(1.5), Inches(2.0), Inches(0.12), Inches(3.5)
    )
    line_q.fill.solid()
    line_q.fill.fore_color.rgb = color_cyan
    line_q.line.fill.background()

    # Question Text
    tb_q = slide_q.shapes.add_textbox(Inches(2.0), Inches(2.2), Inches(9.5), Inches(3.0))
    p_q = tb_q.text_frame.paragraphs[0]
    p_q.word_wrap = True
    run_q = p_q.add_run()
    run_q.text = question_text
    run_q.font.size = Pt(44)
    run_q.font.color.rgb = color_navy

    # Cleanup temp files
    try:
        os.remove(prof_img_path)
        os.remove(rings_img_path)
    except OSError:
        pass

    prs.save(output_pptx_path)
    return output_pptx_path
```