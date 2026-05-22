# Cyber-Radar Emission Composition

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Cyber-Radar Emission Composition

* **Core Visual Mechanism**: This design relies on **depth through concentric interpolation** combined with **glowing accent nodes**. By placing a subject (with a transparent background) over a series of concentric, expanding geometric shapes (waves) that fade in opacity, it creates a 3D illusion of signal emission, scanning, or technological depth. Glowing "blips" add a layer of dynamic activity.
* **Why Use This Skill (Rationale)**: Native PowerPoint often looks flat. Using interpolating shapes with alpha gradients instantly transforms a static 2D slide into a dynamic, 3D spatial environment. It directs the viewer's eye outward from the focal point (the subject) to the data points on the periphery.
* **Overall Applicability**: Perfect for high-tech product features (drones, sensors, AI, telecommunications), performance metrics, data dashboard hero slides, or cybersecurity presentations. 
* **Value Addition**: Transforms a boring bullet-point slide into an immersive "Heads Up Display" (HUD). It elevates the perceived value of the product by visually demonstrating "invisible" features like range, sensitivity, or connectivity.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Subject**: A centralized, high-quality image with the background removed (transparent PNG).
  - **Background**: Deep, untextured dark space. Value: `(10, 10, 15, 255)`.
  - **Radar Waves**: Expanding concentric ellipses (giving a slight 3D perspective tilt) originating from a point on the subject. Color: Neon Tech Green `(0, 255, 128)`. Alpha transitions from 80% near the source to 0% at the edges.
  - **Signal Blips**: Small solid circles surrounded by a larger, highly transparent "glow" halo. Color: Alert Orange `(255, 100, 0)`.
  - **Text Hierarchy**: 
    - **Title**: Large, bold, standard white/light gray.
    - **Data Highlights**: Oversized, bold numbers using a gradient or the neon wave color.
    - **Body Text**: Small, clean sans-serif, muted gray `(180, 180, 180)` to maintain contrast without overpowering.

* **Step B: Compositional Style**
  - **Asymmetric Balance**: The visual anchor (subject + radar center) is placed in the left-center quadrant (occupying ~55% of the canvas). The right 45% is dedicated to clean, left-aligned typography.
  - **Layering Logic**: Background -> Radar Waves & Blips -> Subject -> Text. The subject *must* overlap the center of the waves to ground the emission effect.

* **Step C: Dynamic Effects & Transitions**
  - In PowerPoint, the rings could be animated with a slow "Zoom" or "Grow/Shrink" effect, and the blips with a "Pulse" animation to simulate active scanning.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Concentric Radar Waves** | PIL / Pillow | Recreating the iSlide "Interpolation" tool in raw `python-pptx` XML is difficult because PPT handles line transparency poorly. A simple `for` loop in PIL drawing ellipses with decreasing RGBA alpha yields a perfect, artifact-free HUD effect. |
| **Glowing Signal Blips** | PIL / Pillow | Using `ImageFilter.GaussianBlur` on an RGBA canvas creates a true optical glow that natively blends with the dark background. |
| **Transparent Subject** | python-pptx | Inserted as a standard picture overlay over the PIL-generated background. |
| **Data Typography** | python-pptx native | Native text boxes allow for crisp rendering, easy editing, and specific font coloring (Neon accents for numbers). |

> **Feasibility Assessment**: 95%. The code generates the exact visual aesthetic (dark mode, fading neon radar rings, glowing blips, and structured data text). Because fetching perfectly cutout transparent PNGs via URL is unreliable, the script includes a fallback that generates a sleek "tech core" subject if a drone image isn't available, ensuring the visual effect works out of the box.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "高性能雷达探测\nHIGH-PERFORMANCE RADAR DETECTION",
    bg_palette: str = "dark",
    accent_color_waves: tuple = (0, 255, 128),  # Neon Green
    accent_color_blips: tuple = (255, 100, 0),  # Orange
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Cyber-Radar Emission effect.
    Uses PIL to calculate and draw an alpha-interpolated radar background,
    layered under text and subject imagery.
    """
    import os
    import urllib.request
    from io import BytesIO
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw, ImageFilter
    
    prs = Presentation()
    # 16:9 widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # blank layout

    # === Layer 1: Dark Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(15, 15, 20)

    # === Layer 2: Generate Radar Waves & Blips via PIL ===
    # Canvas size matching 1080p for good resolution
    canvas_w, canvas_h = 1920, 1080
    radar_img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(radar_img)

    # Radar emission origin (Left-center, where the subject will be placed)
    origin_x, origin_y = int(canvas_w * 0.35), int(canvas_h * 0.6)
    
    # 1. Draw Concentric Interpolated Waves
    num_rings = 35
    max_radius_x = 1200
    max_radius_y = 900 # Slightly elliptical to simulate 3D perspective
    
    r, g, b = accent_color_waves
    for i in range(num_rings):
        progress = i / (num_rings - 1) # 0.0 to 1.0
        # Ease-out progression for ring spacing (looks more natural)
        ease_progress = 1 - (1 - progress)**2 
        
        rad_x = 50 + (max_radius_x * ease_progress)
        rad_y = 50 + (max_radius_y * ease_progress)
        
        # Alpha fades out as rings get larger
        alpha = int(200 * (1 - progress)**1.5)
        
        bbox = [origin_x - rad_x, origin_y - rad_y, origin_x + rad_x, origin_y + rad_y]
        draw.ellipse(bbox, outline=(r, g, b, alpha), width=3)

    # 2. Add Glowing Blips
    blip_positions = [
        (origin_x - 300, origin_y + 100),
        (origin_x + 150, origin_y + 250),
        (origin_x - 100, origin_y + 350)
    ]
    
    br, bg, bb = accent_color_blips
    for bx, by in blip_positions:
        # Draw outer glow
        glow_radius = 40
        glow_bbox = [bx - glow_radius, by - glow_radius, bx + glow_radius, by + glow_radius]
        draw.ellipse(glow_bbox, fill=(br, bg, bb, 40))
        # Draw solid inner core
        core_radius = 12
        core_bbox = [bx - core_radius, by - core_radius, bx + core_radius, by + core_radius]
        draw.ellipse(core_bbox, fill=(br, bg, bb, 255))
        
    # Apply a slight blur to the whole radar layer to make it feel like light/HUD
    radar_img = radar_img.filter(ImageFilter.GaussianBlur(radius=1))
    
    # Save temp radar image
    radar_path = "temp_radar.png"
    radar_img.save(radar_path)
    
    # Insert radar image into slide
    slide.shapes.add_picture(radar_path, Inches(0), Inches(0), width=prs.slide_width, height=prs.slide_height)

    # === Layer 3: The Subject (Transparent PNG) ===
    # Attempt to download a transparent drone/camera image
    subject_img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/DJI_Inspire_1_in_flight.png/640px-DJI_Inspire_1_in_flight.png"
    temp_subject = "temp_subject.png"
    
    try:
        req = urllib.request.Request(subject_img_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(temp_subject, 'wb') as f:
                f.write(response.read())
        # Insert Subject
        pic = slide.shapes.add_picture(temp_subject, Inches(0.5), Inches(1.5), width=Inches(6.5))
    except Exception as e:
        # Fallback: Draw a sleek vector tech-core if download fails
        fallback_img = Image.new('RGBA', (800, 800), (0, 0, 0, 0))
        f_draw = ImageDraw.Draw(fallback_img)
        f_draw.ellipse([100, 100, 700, 700], fill=(40, 40, 45, 255), outline=(150, 150, 150, 255), width=8)
        f_draw.ellipse([300, 300, 500, 500], fill=(200, 200, 200, 255))
        f_draw.line([400, 0, 400, 800], fill=(150, 150, 150, 255), width=4)
        f_draw.line([0, 400, 800, 400], fill=(150, 150, 150, 255), width=4)
        fallback_img.save(temp_subject)
        pic = slide.shapes.add_picture(temp_subject, Inches(1), Inches(1.5), width=Inches(5))

    # === Layer 4: Typography & Layout ===
    
    # Main Title
    title_box = slide.shapes.add_textbox(Inches(7.5), Inches(0.8), Inches(5), Inches(1))
    tf = title_box.text_frame
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    p1.text = title_text.split('\n')[0]
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)
    
    if "\n" in title_text:
        p2 = tf.add_paragraph()
        p2.text = title_text.split('\n')[1]
        p2.font.size = Pt(14)
        p2.font.color.rgb = RGBColor(120, 120, 120)

    # Helper function to add data blocks
    def add_data_block(slide, top_inch, title, value_str, desc=""):
        # Divider line
        line = slide.shapes.add_shape(
            1, # line
            Inches(7.5), Inches(top_inch), Inches(5), Inches(0)
        )
        line.line.color.rgb = RGBColor(50, 50, 60)
        
        tb = slide.shapes.add_textbox(Inches(7.5), Inches(top_inch + 0.1), Inches(5), Inches(1.5))
        t_frame = tb.text_frame
        t_frame.word_wrap = True
        
        # Data Title
        p_title = t_frame.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(16)
        p_title.font.bold = True
        p_title.font.color.rgb = RGBColor(200, 200, 200)
        
        # Massive Value (Accent Color)
        p_val = t_frame.add_paragraph()
        p_val.text = value_str
        p_val.font.size = Pt(40)
        p_val.font.bold = True
        p_val.font.color.rgb = RGBColor(accent_color_waves[0], accent_color_waves[1], accent_color_waves[2])
        
        # Description
        if desc:
            p_desc = t_frame.add_paragraph()
            p_desc.text = desc
            p_desc.font.size = Pt(12)
            p_desc.font.color.rgb = RGBColor(150, 150, 150)

    # Insert Data Blocks
    add_data_block(slide, 2.2, "系统流畅度提升", "20% - 27%")
    add_data_block(slide, 4.0, "雷达探测灵敏度提升", "53% - 67%")
    add_data_block(slide, 5.8, "硬件升级概述", "", "应用最新一代雷达传感器，软件系统\n全面升级流畅度大幅提升。")

    # Clean up temp files
    try:
        os.remove(radar_path)
        os.remove(temp_subject)
    except:
        pass

    prs.save(output_pptx_path)
    return output_pptx_path
```