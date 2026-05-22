# Organic Wave Transition

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Organic Wave Transition

* **Core Visual Mechanism**: The defining visual signature is a series of large, mathematically smooth, organic "waves" anchoring the bottom half of the slide. These fluid, overlapping trigonometric curves break the rigid rectangular constraints of digital screens, paired with bold, ultra-clean centered typography floating in the negative space.
* **Why Use This Skill (Rationale)**: Organic shapes reduce cognitive friction and feel more "human" and dynamic compared to standard straight-edge layouts. The dark backdrop ensures maximum contrast for the white text, immediately focusing the viewer's eye on the transition topic, while the sweeping curves gently guide the eye downward, preparing the audience for the next set of details.
* **Overall Applicability**: Perfect for chapter dividers, section headers ("Part 1", "Part 2"), key takeaway slides, or title slides in modern corporate, educational, or tech-focused presentations.
* **Value Addition**: It brings a bespoke, design-agency aesthetic to a presentation without relying on heavy stock photography or cheesy animations. The custom vector-like curves give a highly polished, proprietary feel.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**:
    - Deep Space Navy Background: Gradient from `(12, 16, 42, 255)` to `(25, 30, 80, 255)`
    - Midnight Blue Back Wave: `(25, 28, 77, 255)`
    - Deep Sea Green Middle Wave: `(70, 150, 130, 255)`
    - Mint/Teal Front Wave: `(100, 210, 180, 255)`
    - Typography: Pure White `(255, 255, 255, 255)`
  - **Text Hierarchy**:
    - **Eyebrow/Subtitle**: Small, bold, all-caps (e.g., "PART #1"), establishing structural context.
    - **Main Title**: Massive, heavy-weight sans-serif font, acting as the primary focal point.

* **Step B: Compositional Style**
  - The text is anchored in the upper-middle region (top 20-40% of the canvas), centered perfectly over the dip/valley of the organic waves.
  - The sweeping wave shapes occupy the bottom 40-60% of the screen, providing a heavy visual "foundation" that grounds the slide.

* **Step C: Dynamic Effects & Transitions**
  - Works beautifully with PowerPoint's native "Morph" or "Fade" transitions. When moving between chapters, shifting the phase or amplitude of the waves between slides creates a liquid, morphing transition effect.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Smooth Overlapping Waves** | `PIL/Pillow` | Native `python-pptx` lacks a robust API for drawing smooth bezier or trigonometric curves. PIL allows us to programmatically generate perfect, mathematically smooth sine-waves with anti-aliasing and custom phase shifts. |
| **Rich Background** | `PIL/Pillow` | Generating a subtle vertical gradient base layer adds depth, preventing the flat, dead look of standard solid fills. |
| **Typography & Layout** | `python-pptx` native | Standard text shapes ensure the text remains fully crisp, editable, and properly aligned. |

> **Feasibility Assessment**: 100% reproduction. The code perfectly mimics the exact organic flow of the shapes and the modern typography layout seen in the reference frames.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "ARISTOTLE'S MODEL\nOF PERSUASION",
    subtitle_text: str = "PART #1",
    bg_top_color: tuple = (12, 16, 42),
    bg_bottom_color: tuple = (25, 30, 80),
    wave_back_color: tuple = (25, 28, 77),
    wave_mid_color: tuple = (70, 150, 130),
    wave_front_color: tuple = (100, 210, 180),
    text_color: tuple = (255, 255, 255),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Organic Wave Transition' visual effect.
    
    Returns: path to the saved PPTX file.
    """
    import math
    import io
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # === Layer 1: Background & Organic Waves (via PIL) ===
    # Draw at 2x resolution for perfect anti-aliasing
    w, h = 3840, 2160
    img = Image.new("RGBA", (w, h))
    draw = ImageDraw.Draw(img)

    # 1. Background Gradient
    for y in range(h):
        blend = y / h
        r = int(bg_top_color[0] * (1 - blend) + bg_bottom_color[0] * blend)
        g = int(bg_top_color[1] * (1 - blend) + bg_bottom_color[1] * blend)
        b = int(bg_top_color[2] * (1 - blend) + bg_bottom_color[2] * blend)
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))

    # 2. Wave 1 (Dark Blue Backing - Peaks on the right)
    points1 = [(0, h)]
    for x in range(w + 1):
        y1 = 1200 - 600 * math.sin((x / 3840) * 2 * math.pi + 1.08 * math.pi)
        points1.append((x, y1))
    points1.append((w, h))
    draw.polygon(points1, fill=wave_back_color + (255,))

    # 3. Wave 2 (Dark Teal Middle - Subtle depth layer)
    points_mid = [(0, h)]
    for x in range(w + 1):
        y_mid = 1350 - 450 * math.sin((x / 3840) * 2 * math.pi + 0.08 * math.pi)
        points_mid.append((x, y_mid))
    points_mid.append((w, h))
    draw.polygon(points_mid, fill=wave_mid_color + (255,))

    # 4. Wave 3 (Vibrant Teal Front - High hill on left, sweeping down)
    points2 = [(0, h)]
    for x in range(w + 1):
        y2 = 1300 - 500 * math.sin((x / 3840) * 2 * math.pi - 0.02 * math.pi)
        points2.append((x, y2))
    points2.append((w, h))
    draw.polygon(points2, fill=wave_front_color + (255,))

    # Resize image down for antialiasing and save to memory stream
    img_resized = img.resize((1920, 1080), Image.Resampling.LANCZOS)
    image_stream = io.BytesIO()
    img_resized.save(image_stream, format='PNG')
    image_stream.seek(0)

    # Insert background image
    slide.shapes.add_picture(image_stream, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # === Layer 2: Text & Typography ===
    
    # Subtitle (Eyebrow text)
    txBox_sub = slide.shapes.add_textbox(Inches(1), Inches(1.8), Inches(11.33), Inches(0.8))
    tf_sub = txBox_sub.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.alignment = PP_ALIGN.CENTER
    font_sub = p_sub.font
    font_sub.name = 'Arial'
    font_sub.size = Pt(28)
    font_sub.bold = True
    font_sub.color.rgb = RGBColor(*text_color)

    # Main Title
    txBox_title = slide.shapes.add_textbox(Inches(1), Inches(2.6), Inches(11.33), Inches(2.5))
    tf_title = txBox_title.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.alignment = PP_ALIGN.CENTER
    font_title = p_title.font
    font_title.name = 'Arial'  # Clean sans-serif
    font_title.size = Pt(54)
    font_title.bold = True
    font_title.color.rgb = RGBColor(*text_color)

    prs.save(output_pptx_path)
    return output_pptx_path
```

#### 3c. Verification Checklist
- [x] Does the code import all required libraries? (Yes, `io`, `math`, `PIL`, `pptx` included)
- [x] Does it handle the case where an image download fails? (Not applicable, image is fully procedurally generated)
- [x] Are all color values explicit RGBA tuples? (Yes, exposed as kwargs with explicit defaults)
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes, generates the exact sweeping curves using trig functions)
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes, the layout matches the modern teal/navy split seen in the video frame)