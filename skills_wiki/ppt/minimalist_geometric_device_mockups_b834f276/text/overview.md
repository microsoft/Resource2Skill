# Minimalist Geometric Device Mockups

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Minimalist Geometric Device Mockups

* **Core Visual Mechanism**: Constructing recognizable technology devices (tablets, laptops, phones) entirely out of layered native vector primitives (rounded rectangles, standard rectangles, and circles). It relies heavily on absolute symmetry, high-contrast borders/fills, and nested shapes to simulate hardware bezels and screens.
* **Why Use This Skill (Rationale)**: Using native vector mockups instead of imported PNG/SVG images ensures the slides remain lightweight, infinitely scalable without pixelation, and fully editable. It allows presenters to customize the device colors to match their brand, safely drop screen-recordings or images directly into the "screen" rectangles, and avoids the messy white-background issues common with downloaded clip art. 
* **Overall Applicability**: Perfect for SaaS product showcases, portfolio presentations, mobile app UI/UX design reviews, and modern, flat-design corporate slide decks.
* **Value Addition**: Transforms a standard screenshot into a contextual, professional product showcase. It provides a "frame" that immediately tells the audience *how* the software/website is consumed.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Device Chassis**: Defined by Rounded Rectangles. Color is typically stark white `(255, 255, 255, 255)` with no outline, or a subtle gray outline to separate it from white backgrounds.
  * **Screens**: Standard sharp-cornered Rectangles. Color is pure black `(0, 0, 0, 255)` to represent an off screen, or used as a placeholder for a picture/video fill.
  * **Hardware Details**: Small circles for cameras and home buttons. Small rounded rectangles for laptop trackpad cutouts or lid lips. Colors use medium grays `(127, 127, 127, 255)` to light silver `(217, 217, 217, 255)`.
  * **Background**: A high-contrast, flat solid color (like the video's bright green `(112, 173, 71, 255)`) to make the white mockups "pop."

* **Step B: Compositional Style**
  * **Symmetry**: 100% horizontal center alignment between the nested components (Chassis -> Screen -> Camera -> Button).
  * **Proportions**: Mimics real-world aspect ratios. The tablet screen is roughly 3:4 or 9:16. The laptop screen is 16:9. Bezels are kept uniform (e.g., equidistant top, left, and right borders).
  * **Layering**: Strictly layered back-to-front: Chassis (Back) -> Screen (Middle) -> Buttons/Cameras (Front).

* **Step C: Dynamic Effects & Transitions**
  * Because these are native shapes, placing a tablet on Slide 1 and a laptop on Slide 2 allows PowerPoint's "Morph" transition to fluidly animate the hardware transforming from a mobile device to a desktop device. 

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Shape Creation & Composition** | `python-pptx` native | The core of the tutorial is building devices via native PowerPoint shape primitives. Native shapes are fully editable, perfectly scalable, and natively support the required nesting. |
| **Colors & Fills** | `python-pptx` native | Standard `RGBColor` application perfectly replicates the flat UI style of the tutorial without needing image processing. |

> **Feasibility Assessment**: 100% — This code reproduces the exact technique shown in the video, generating native PowerPoint vectors that mimic a tablet and a laptop on a colored background.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Device Mockups",
    body_text: str = "",
    bg_palette: str = "technology",  
    accent_color: tuple = (0, 191, 255),  
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Minimalist Geometric Device Mockups visual effect.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.dml.color import RGBColor
    
    prs = Presentation()
    # Use standard widescreen 16:9 
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Helper function to style shapes ===
    def style_shape(shape, fill_rgb, line_rgb=None):
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_rgb
        if line_rgb:
            shape.line.color.rgb = line_rgb
            shape.line.width = Pt(1.5)
        else:
            shape.line.fill.background() # No line

    # === Layer 1: Background ===
    # Create the bright green background shown in the tutorial
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        Inches(0), Inches(0), 
        prs.slide_width, prs.slide_height
    )
    style_shape(bg, RGBColor(112, 173, 71)) # Video's green

    # Add Title
    title = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11), Inches(1))
    tf = title.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # === Layer 2: Tablet (iPad) Mockup ===
    # Tablet coordinates and dimensions
    t_w, t_h = 3.0, 4.5
    t_l, t_t = 2.0, 2.0
    
    # Tablet Chassis (White Rounded Rectangle)
    tablet_body = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(t_l), Inches(t_t), Inches(t_w), Inches(t_h))
    style_shape(tablet_body, RGBColor(255, 255, 255))
    
    # Tablet Screen (Black Rectangle)
    s_w, s_h = 2.6, 3.5
    s_l = t_l + ((t_w - s_w) / 2) # Centered horizontally
    s_t = t_t + 0.4
    tablet_screen = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(s_l), Inches(s_t), Inches(s_w), Inches(s_h))
    style_shape(tablet_screen, RGBColor(0, 0, 0))
    
    # Tablet Camera (Black Circle)
    c_d = 0.1
    c_l = t_l + ((t_w - c_d) / 2)
    c_t = t_t + 0.15
    tablet_cam = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(c_l), Inches(c_t), Inches(c_d), Inches(c_d))
    style_shape(tablet_cam, RGBColor(0, 0, 0))
    
    # Tablet Home Button (White Circle with Gray Outline)
    b_d = 0.3
    b_l = t_l + ((t_w - b_d) / 2)
    b_t = t_t + 4.05 # Bottom bezel
    tablet_btn = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(b_l), Inches(b_t), Inches(b_d), Inches(b_d))
    style_shape(tablet_btn, RGBColor(255, 255, 255), RGBColor(180, 180, 180))


    # === Layer 3: Laptop (MacBook style) Mockup ===
    # Laptop Monitor coordinates
    l_w, l_h = 5.5, 3.5
    l_l, l_t = 6.5, 2.3
    
    # Monitor Chassis (White Rounded Rectangle)
    lap_monitor = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l_l), Inches(l_t), Inches(l_w), Inches(l_h))
    style_shape(lap_monitor, RGBColor(255, 255, 255))
    
    # Monitor Screen (Black Rectangle)
    ls_w, ls_h = 5.1, 2.9
    ls_l = l_l + ((l_w - ls_w) / 2)
    ls_t = l_t + 0.2
    lap_screen = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(ls_l), Inches(ls_t), Inches(ls_w), Inches(ls_h))
    style_shape(lap_screen, RGBColor(0, 0, 0))
    
    # Monitor Camera (Black Circle)
    lc_d = 0.08
    lc_l = l_l + ((l_w - lc_d) / 2)
    lc_t = l_t + 0.06
    lap_cam = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(lc_l), Inches(lc_t), Inches(lc_d), Inches(lc_d))
    style_shape(lap_cam, RGBColor(100, 100, 100))
    
    # Laptop Base (Silver Rounded Rectangle)
    base_w, base_h = 6.5, 0.4
    base_l = l_l - ((base_w - l_w) / 2)
    base_t = l_t + l_h - 0.1 # slightly overlapping monitor
    lap_base = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(base_l), Inches(base_t), Inches(base_w), Inches(base_h))
    style_shape(lap_base, RGBColor(217, 217, 217))
    
    # Laptop Lid Notch/Lip (Dark Gray Rounded Rectangle)
    lip_w, lip_h = 1.0, 0.1
    lip_l = l_l + ((l_w - lip_w) / 2)
    lip_t = base_t
    lap_lip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(lip_l), Inches(lip_t), Inches(lip_w), Inches(lip_h))
    style_shape(lap_lip, RGBColor(127, 127, 127))

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries? (Yes, `pptx`, `MSO_SHAPE`, `RGBColor`, `Pt`, `Inches` included).
- [x] Does it handle the case where an image download fails (fallback)? (Not applicable; this effect strictly uses code-generated vector shapes, avoiding external dependencies entirely).
- [x] Are all color values explicit RGBA/RGB tuples? (Yes, explicit `RGBColor` constants used for Green, White, Black, Silver, and Gray).
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes, it accurately calculates center-alignment math to generate perfectly symmetrical flat mockups of a tablet and a laptop).
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes, it uses the exact combination of nested `ROUNDED_RECTANGLE`, `RECTANGLE`, and `OVAL` primitives demonstrated in the tutorial).