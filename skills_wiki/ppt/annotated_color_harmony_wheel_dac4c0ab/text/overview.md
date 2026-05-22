# Annotated Color Harmony Wheel

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Annotated Color Harmony Wheel

*   **Core Visual Mechanism**: This design pattern uses a segmented color wheel as a visual anchor to explain color theory concepts. Key color relationships (like monochromatic, analogous, complementary) are visually highlighted using geometric annotations such as lines, arcs, and wedges directly on the wheel, accompanied by clear text labels.

*   **Why Use This Skill (Rationale)**: The technique works by translating abstract color theory terminology into a concrete, intuitive visual model. It provides an immediate, easy-to-understand reference that grounds the audience's understanding of color harmony. By visualizing the mathematical relationships between hues on a circle, it makes concepts like "180 degrees apart" (complementary) tangible and memorable.

*   **Overall Applicability**: This skill is highly effective in educational or strategic contexts where justifying design choices is necessary.
    *   **Design/Branding Presentations**: Explaining the logic behind a new color palette.
    *   **Educational Workshops**: Teaching fundamentals of art, graphic design, or UI/UX.
    *   **Marketing & Sales Pitches**: Demonstrating a deep understanding of visual psychology to a client.
    *   **Internal Team Meetings**: Aligning team members on a visual style guide.

*   **Value Addition**: It elevates a presentation from simply *showing* colors to *explaining* them. It adds a layer of professionalism and analytical rigor, demonstrating that color choices are deliberate and based on established principles, not just subjective preference.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    - **Color Wheel**: A 24-segment "donut" style color wheel, programmatically generated to cover the full hue spectrum (360 degrees).
    - **Annotation Graphics**: Simple geometric shapes like lines, wedges (pie slices), and circles are used to highlight specific segments or relationships.
    - **Text Labels**: A primary label identifies the concept (e.g., "Analogous Colors"), and a sub-label provides a concise definition (e.g., "Colors within 60° of each other").
    - **Color Logic**:
        - **Background**: A clean, neutral white `(255, 255, 255, 255)` or off-white.
        - **Color Wheel**: Generated using the HSL color model, with saturation at 100% and lightness at 50% for maximum vibrancy.
        - **Annotation Elements**: A neutral but strong color like dark grey `(80, 80, 80, 255)` for lines and wedges to ensure they are visible but don't clash with the wheel.
        - **Text**: A primary, bold font for the title in a dark grey `(80, 80, 80, 255)` and a lighter, regular font for the description. A small red accent box `(211, 84, 0, 255)` is used for the title block as seen in the tutorial.

*   **Step B: Compositional Style**
    - The slide uses a clean, two-column layout.
    - The right side is dedicated to the visual element: the annotated color wheel. It typically occupies about 40-45% of the slide's width.
    - The left side is for the textual explanation, creating a clear separation between concept and visualization. This balanced asymmetry guides the viewer's eye from the definition to the example.

*   **Step C: Dynamic Effects & Transitions**
    - The tutorial implies a "Fade" or "Appear" animation for each slide or element as it's introduced. This is best applied manually in PowerPoint. The code focuses on generating the static visual assets for each concept on a separate slide.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Segmented Color Wheel** | PIL/Pillow | `python-pptx` lacks the ability to draw segmented circular shapes or gradients. PIL's `ImageDraw.pieslice` is ideal for programmatically constructing a color wheel with precise control over each hue segment. |
| **Annotation Graphics (lines, wedges)** | PIL/Pillow | Drawing annotations directly onto the same PIL image as the wheel ensures perfect alignment and sizing. It's far simpler and more robust than trying to overlay `python-pptx` shapes. |
| **Slide Layout and Text** | `python-pptx` native | `python-pptx` is the most straightforward tool for creating slides, placing images, and adding formatted text boxes. |

> **Feasibility Assessment**: 100%. The combination of PIL for generating the complex visual asset (the annotated wheel) and `python-pptx` for assembling the final slide can fully reproduce the core educational diagrams shown in the tutorial.

#### 3b. Complete Reproduction Code

```python
import math
import io
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw, ImageFont, ImageColor

def create_color_theory_slides(output_pptx_path: str, **kwargs) -> str:
    """
    Creates a multi-slide PPTX presentation explaining color theory concepts
    using an annotated color wheel, as seen in the tutorial.

    Each slide demonstrates a different color harmony principle.

    Returns:
        str: The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # --- Data for each slide ---
    harmonies = {
        "同色系 (Monochromatic)": {
            "description": "同一色相调整明度和饱和度\n(Adjusting brightness and saturation of a single hue)",
            "type": "monochromatic",
            "angle": 0,
        },
        "类似色 (Analogous)": {
            "description": "相差60°以内的色彩\n(Colors within a 60° arc)",
            "type": "arc",
            "angle": 60,
        },
        "邻近色 (Adjacent)": {
            "description": "间隔60-90°以内的色彩\n(Colors within a 90° arc)",
            "type": "arc",
            "angle": 90,
        },
        "对比色 (Triadic)": {
            "description": "相互之间角度为120°的色彩\n(Colors 120° apart from each other)",
            "type": "triadic",
            "angle": 120,
        },
        "互补色 (Complementary)": {
            "description": "相互之间角度为180°的色彩\n(Colors 180° apart from each other)",
            "type": "complementary",
            "angle": 180,
        },
    }

    # --- Helper function to generate the wheel image ---
    def _generate_harmony_wheel_image(harmony_type: str, angle: int, size: int = 1000) -> io.BytesIO:
        img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        center = size / 2
        radius = size / 2 * 0.9
        inner_radius_ratio = 0.4
        
        # 1. Draw the color wheel (24 segments)
        num_segments = 24
        angle_step = 360 / num_segments
        for i in range(num_segments):
            start_angle = i * angle_step
            end_angle = (i + 1) * angle_step
            hue = int(start_angle)
            
            fill_color = ImageColor.getrgb(f"hsl({hue}, 100%, 50%)")
            draw.pieslice(
                [center - radius, center - radius, center + radius, center + radius],
                start_angle - 90,
                end_angle - 90,
                fill=fill_color,
            )
            
        # 2. Draw the inner white circle to create a donut
        inner_radius = radius * inner_radius_ratio
        draw.ellipse(
            [center - inner_radius, center - inner_radius, center + inner_radius, center + inner_radius],
            fill=(255, 255, 255, 255),
        )
        
        # 3. Draw annotations based on harmony type
        # Rotate all angles by -90 to align 0 degrees with the right horizontal axis
        rotation = -90 
        annotation_color = (80, 80, 80)
        
        if harmony_type == "monochromatic":
            # Point to the red color and show variations
            base_hue = 0
            for i in range(4):
                lightness = 30 + i * 15
                sat = 100 - i * 5
                color = ImageColor.getrgb(f"hsl({base_hue}, {sat}%, {lightness}%)")
                r_offset = inner_radius + (radius - inner_radius) * (0.2 + 0.2 * i)
                x = center + r_offset * math.cos(math.radians(base_hue + rotation))
                y = center + r_offset * math.sin(math.radians(base_hue + rotation))
                draw.ellipse([x-20, y-20, x+20, y+20], fill=color, outline=annotation_color, width=2)

        elif harmony_type == "arc":
            start, end = 0, angle
            draw.pieslice([0, 0, size, size], start + rotation, end + rotation,
                          outline=annotation_color, width=5)
            
        elif harmony_type == "triadic":
            for i in range(3):
                a = (i * angle) + rotation
                x_end = center + radius * math.cos(math.radians(a))
                y_end = center + radius * math.sin(math.radians(a))
                draw.line([center, center, x_end, y_end], fill=annotation_color, width=5)
                
        elif harmony_type == "complementary":
            start_angle_rad = math.radians(0 + rotation)
            end_angle_rad = math.radians(180 + rotation)
            x1 = center + inner_radius * math.cos(start_angle_rad)
            y1 = center + inner_radius * math.sin(start_angle_rad)
            x2 = center + radius * math.cos(start_angle_rad)
            y2 = center + radius * math.sin(start_angle_rad)
            draw.line([x1, y1, x2, y2], fill=annotation_color, width=5)
            
            x3 = center + inner_radius * math.cos(end_angle_rad)
            y3 = center + inner_radius * math.sin(end_angle_rad)
            x4 = center + radius * math.cos(end_angle_rad)
            y4 = center + radius * math.sin(end_angle_rad)
            draw.line([x3, y3, x4, y4], fill=annotation_color, width=5)


        image_stream = io.BytesIO()
        img.save(image_stream, format="PNG")
        image_stream.seek(0)
        return image_stream

    # --- Loop through harmonies and create a slide for each ---
    for title, data in harmonies.items():
        slide_layout = prs.slide_layouts[6]  # Blank layout
        slide = prs.slides.add_slide(slide_layout)
        
        # Set a plain white background
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(255, 255, 255)

        # Generate and add the wheel image
        image_stream = _generate_harmony_wheel_image(data["type"], data["angle"])
        slide.shapes.add_picture(image_stream, Inches(7), Inches(1), height=Inches(5.5))

        # Add title and description text
        # Title box with red accent
        title_shape = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(5), Inches(1))
        title_frame = title_shape.text_frame
        p = title_frame.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(28)
        p.font.color.rgb = RGBColor(80, 80, 80)

        accent_box = slide.shapes.add_shape(1, Inches(1), Inches(2.1), Inches(1.5), Inches(0.4))
        accent_fill = accent_box.fill
        accent_fill.solid()
        accent_fill.fore_color.rgb = RGBColor(211, 84, 0)
        line = accent_box.line
        line.fill.background() # No outline

        # Move accent box behind title text
        accent_xml = accent_box._element
        accent_xml.getparent().remove(accent_xml)
        title_shape._element.getparent().insert(0, accent_xml)
        
        # Description box
        desc_shape = slide.shapes.add_textbox(Inches(1.2), Inches(3.2), Inches(5), Inches(1.5))
        desc_frame = desc_shape.text_frame
        desc_frame.word_wrap = True
        p_desc = desc_frame.paragraphs[0]
        p_desc.text = data["description"]
        p_desc.font.size = Pt(18)
        p_desc.font.color.rgb = RGBColor(128, 128, 128)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_color_theory_slides("color_theory_presentation.pptx")
```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback)? (N/A - images are generated programmatically)
- [x] Are all color values explicit RGBA/RGB tuples?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?
- [x] Would someone looking at the output say "yes, that's the same technique"?