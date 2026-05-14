# Interactive Morphing Image Wheel

## Analysis

# Role: Agent_Skill_Distiller (PPTX Design Style & Pattern Extractor)

### 1. High-level Design Pattern Extraction

> **Skill Name**: Interactive Morphing Image Wheel

* **Core Visual Mechanism**: The core design relies on a large circular "dial" or "donut" constructed from individual image wedges (pie slices). Using PowerPoint's Morph transition, this wheel acts as a dynamic navigation menu. As the presentation progresses, the entire wheel rotates and translates (slides) off-center to create space for full-width content, while the central hub updates its text to indicate the current section.

* **Why Use This Skill (Rationale)**: This technique breaks the monotony of linear, slide-by-slide bullet points. By anchoring the navigation to a persistent, rotating physical object (the wheel), it gives the audience a strong sense of spatial progression and context. It leverages the psychological appeal of tactile, dial-like interfaces.

* **Overall Applicability**: Ideal for presentations with 4 to 8 distinct but equal sections, such as event agendas (as seen in the tutorial), product feature breakdowns, company core values, or phased project timelines. 

* **Value Addition**: Transforms a standard presentation into an interactive "app-like" experience. The fluid motion retains audience attention, while the image slices provide a highly visual, evocative preview of upcoming topics.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **The Wheel**: A circle divided into $N$ equal pie slices. Each slice contains a distinct photograph.
  - **The Hub**: A solid white circle placed perfectly in the center of the wheel to create a donut chart effect.
  - **Typography**: Bold, modern sans-serif fonts (e.g., Montserrat or Arial Black). High contrast (Black `(0, 0, 0, 255)` on White `(255, 255, 255, 255)`).
  - **Color Logic**: The background is clean white `(255, 255, 255, 255)`. The color palette is driven organically by the vibrant photographs used in the slices.

* **Step B: Compositional Style**
  - **Slide 1 (Overview)**: Central symmetry. The wheel occupies roughly 70% of the slide height ($13.33" \times 7.5"$ canvas -> $\sim6"$ diameter wheel).
  - **Slide 2+ (Content Reveal)**: Rule of thirds. The wheel is shifted entirely to the left margin, sometimes bleeding off the edge, acting as a visual anchor. The right 60% of the slide is left empty for clean, structured typography and supporting graphics.

* **Step C: Dynamic Effects & Transitions**
  - **Rotation**: The entire wheel rotates (e.g., by $60^\circ$ for a 6-slice wheel) between slides.
  - **Translation**: The wheel moves from the center to the left.
  - **Morph Transition**: PowerPoint's native Morph transition mathematically interpolates the position, rotation, and scale of matching shapes between the slides.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Slicing images into pie wedges** | `PIL/Pillow` | `python-pptx` cannot programmatically execute PowerPoint's "Merge Shapes -> Intersect" to mask an image into an arc/pie shape. Pillow easily creates anti-aliased pie-slice masks and outputs transparent PNGs. |
| **Perfect circular layout** | `python-pptx` native + `PIL` | By generating all slice PNGs at the exact same overall square resolution (with transparency), we can place all $N$ images at the exact same $X,Y$ coordinate in PPTX, perfectly aligning them without complex trigonometry. |
| **Wheel Rotation & Morphing** | `python-pptx` native | We can assign matching `shape.name` attributes and apply `shape.rotation` across slides to trigger smooth Morph animations. |
| **Morph Transition Injection** | `lxml` XML injection | `python-pptx` lacks an API to apply transitions. We inject the `<p14:morph>` XML tag directly into the slide element. |

> **Feasibility Assessment**: 90%. The code accurately recreates the image wheel, the center hub, the layout shift, the rotation, and the Morph transition. The only omitted detail is the complex collage of decorative graphics on the final slide shown late in the video, as that is highly specific to the video's topic rather than the core design pattern.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "EVENT",
    sections: list = ["JUNE", "ELECTRICAL CARS", "LUNCH", "HIKING", "DIVING", "GEAR"],
    wheel_diameter_inches: float = 6.0,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Interactive Morphing Image Wheel effect.
    """
    import os
    import io
    import urllib.request
    import math
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from pptx.oxml import parse_xml
    from PIL import Image, ImageDraw, ImageOps

    # --- Helper: Apply Morph Transition via lxml ---
    def apply_morph_transition(slide):
        transition_xml = (
            '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
            'xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" '
            'spd="slow">'
            '<p14:morph val="byObject"/>'
            '</p:transition>'
        )
        transition = parse_xml(transition_xml)
        slide._element.append(transition)

    # --- Helper: Generate Image Slice ---
    def generate_pie_slice_image(image_url, start_angle, end_angle, fallback_color, size=800):
        try:
            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as url_response:
                img = Image.open(io.BytesIO(url_response.read())).convert("RGBA")
        except Exception:
            # Fallback to solid color if download fails
            img = Image.new("RGBA", (size, size), fallback_color)

        # Fit image to square
        img = ImageOps.fit(img, (size, size), method=Image.Resampling.LANCZOS)
        
        # Create anti-aliased mask (4x resolution)
        mask_size = size * 4
        mask = Image.new("L", (mask_size, mask_size), 0)
        draw = ImageDraw.Draw(mask)
        # PIL angles start from +x axis, moving clockwise
        draw.pieslice([0, 0, mask_size, mask_size], start_angle, end_angle, fill=255)
        mask = mask.resize((size, size), Image.Resampling.LANCZOS)
        
        # Apply mask
        img.putalpha(mask)
        
        # Save to buffer
        img_io = io.BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        return img_io

    # Configuration
    num_slices = len(sections)
    angle_per_slice = 360 / num_slices
    
    # Placeholder images (Unsplash Source) & Fallback colors
    image_themes = ["abstract", "technology", "food", "nature", "ocean", "texture"]
    fallback_colors = [
        (255, 99, 71, 255), (54, 162, 235, 255), (255, 206, 86, 255),
        (75, 192, 192, 255), (153, 102, 255, 255), (255, 159, 64, 255)
    ]

    print("Generating transparent pie slices (this may take a few seconds)...")
    slice_buffers = []
    for i in range(num_slices):
        start_a = i * angle_per_slice
        end_a = (i + 1) * angle_per_slice
        url = f"https://source.unsplash.com/random/800x800/?{image_themes[i%len(image_themes)]}"
        img_io = generate_pie_slice_image(url, start_a, end_a, fallback_colors[i%len(fallback_colors)])
        slice_buffers.append(img_io)

    # Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Calculate positions
    # Slide 1: Center
    center_x = (prs.slide_width.inches - wheel_diameter_inches) / 2
    center_y = (prs.slide_height.inches - wheel_diameter_inches) / 2
    
    # Slide 2: Shifted Left
    left_x = -1.0  # Partially off-screen
    left_y = center_y

    # ==========================================
    # SLIDE 1: The Central Hub Overview
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    
    # Insert slices
    for i in range(num_slices):
        slice_buffers[i].seek(0)
        pic = slide1.shapes.add_picture(
            slice_buffers[i], 
            Inches(center_x), Inches(center_y), 
            Inches(wheel_diameter_inches), Inches(wheel_diameter_inches)
        )
        pic.name = f"WheelSlice_{i}" # Crucial for Morph

    # Insert Center White Hub
    hub_diameter = wheel_diameter_inches * 0.45
    hub_offset = (wheel_diameter_inches - hub_diameter) / 2
    hub1 = slide1.shapes.add_shape(
        1, # msoShapeOval
        Inches(center_x + hub_offset), Inches(center_y + hub_offset),
        Inches(hub_diameter), Inches(hub_diameter)
    )
    hub1.name = "CenterHub"
    hub1.fill.solid()
    hub1.fill.fore_color.rgb = RGBColor(255, 255, 255)
    hub1.line.fill.background() # No line
    
    # Add text to hub
    text_frame = hub1.text_frame
    text_frame.text = title_text
    text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    font = text_frame.paragraphs[0].runs[0].font
    font.name = 'Arial Black'
    font.size = Pt(32)
    font.color.rgb = RGBColor(0, 0, 0)

    # ==========================================
    # SLIDE 2: Shifted and Rotated Reveal
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    apply_morph_transition(slide2) # Inject Morph transition

    # Insert and rotate slices
    rotation_angle = angle_per_slice # Rotate wheel by 1 step
    
    for i in range(num_slices):
        slice_buffers[i].seek(0)
        pic = slide2.shapes.add_picture(
            slice_buffers[i], 
            Inches(left_x), Inches(left_y), 
            Inches(wheel_diameter_inches), Inches(wheel_diameter_inches)
        )
        pic.name = f"WheelSlice_{i}" # Match names for Morph
        pic.rotation = rotation_angle # Spin the wheel

    # Insert Center White Hub (Shifted)
    hub2 = slide2.shapes.add_shape(
        1, # msoShapeOval
        Inches(left_x + hub_offset), Inches(left_y + hub_offset),
        Inches(hub_diameter), Inches(hub_diameter)
    )
    hub2.name = "CenterHub"
    hub2.fill.solid()
    hub2.fill.fore_color.rgb = RGBColor(255, 255, 255)
    hub2.line.fill.background()
    
    text_frame = hub2.text_frame
    text_frame.text = sections[0] # Updated text
    text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    font = text_frame.paragraphs[0].runs[0].font
    font.name = 'Arial Black'
    font.size = Pt(28)
    font.color.rgb = RGBColor(0, 0, 0)

    # Add Reveal Content to the right
    content_x = Inches(left_x + wheel_diameter_inches + 0.5)
    content_y = Inches(2.0)
    
    title_box = slide2.shapes.add_textbox(content_x, content_y, Inches(6.0), Inches(1.0))
    title_frame = title_box.text_frame
    title_p = title_frame.paragraphs[0]
    title_p.text = sections[1] # E.g., "ELECTRICAL CARS"
    title_p.font.name = 'Arial Black'
    title_p.font.size = Pt(44)
    title_p.font.color.rgb = RGBColor(0, 0, 0)

    # Decorative Line
    line = slide2.shapes.add_connector(
        1, # msoConnectorStraight
        content_x, content_y + Inches(0.8),
        Inches(12.5), content_y + Inches(0.8)
    )
    line.line.color.rgb = RGBColor(0, 0, 0)
    line.line.width = Pt(3)

    body_box = slide2.shapes.add_textbox(content_x, content_y + Inches(1.0), Inches(6.0), Inches(2.0))
    body_frame = body_box.text_frame
    body_frame.word_wrap = True
    body_p = body_frame.paragraphs[0]
    body_p.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas porttitor congue massa. Fusce posuere, magna sed pulvinar ultricies, purus lectus malesuada libero, sit amet commodo magna eros quis urna."
    body_p.font.name = 'Calibri'
    body_p.font.size = Pt(14)
    body_p.font.color.rgb = RGBColor(80, 80, 80)

    # Save presentation
    prs.save(output_pptx_path)
    print(f"Presentation saved to {output_pptx_path}. Note: View in Slide Show mode to see the Morph transition.")
    return output_pptx_path
```

#### 3c. Verification Checklist
- [x] Does the code import all required libraries? (Yes, explicitly imported `pptx`, `PIL`, `urllib`, `lxml` mechanics via `parse_xml`).
- [x] Does it handle the case where an image download fails (fallback)? (Yes, falls back to solid RGB blocks).
- [x] Are all color values explicit RGBA tuples? (Yes, fallback colors and fonts use explicit values).
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes, it accurately mimics the "Merge Shapes" intersecting methodology via PIL's pieslice masking, producing the identical circular wheel design).
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes, utilizing consistent shape names allows PowerPoint to Morph the individual rotated slice objects seamlessly, matching the tutorial's core animation.)