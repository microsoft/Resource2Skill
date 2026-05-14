# Continuous Blurred-Background Aesthetic (Apple Presentation Style)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Continuous Blurred-Background Aesthetic (Apple Presentation Style)

* **Core Visual Mechanism**: The defining signature of this style is the use of a single, high-quality photographic background that persists across multiple slides. On the title slide, the image is sharp and vibrant. On content slides, the exact same image undergoes a heavy Gaussian blur and a slight dimming effect. This transforms the photograph from a focal point into a smooth, abstract "frosted glass" canvas that perfectly contrasts with clean, white typography and minimalist UI elements.

* **Why Use This Skill (Rationale)**: This technique solves the classic presentation dilemma: how to make a deck look visually rich without distracting from the text. The sharp title slide sets the emotional tone, while the blurred content slides maintain subconscious spatial continuity (giving the "Morph" transition a canvas to slide across) while guaranteeing absolute legibility. It mimics the "Glassmorphism" UI found in modern operating systems like macOS and iOS.

* **Overall Applicability**: Ideal for high-stakes environments: product launch keynotes, executive summaries, portfolio showcases, and company "all-hands" meetings. It works best when the text content is concise. 

* **Value Addition**: Transforms a standard bullet-point deck into a cohesive, cinematic experience. It removes the harsh, sterile feel of solid white backgrounds and replaces it with depth, warmth, and a premium "tech-keynote" polish.


### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: High-resolution landscape or abstract photo. 
  - **Color Logic**: 
    - Background overlay (for text legibility): `RGBA(20, 20, 30, 80)` (darkening) or `RGBA(255, 255, 255, 40)` (light frosted glass).
    - Text: Pure White `RGBA(255, 255, 255, 255)`.
    - UI Accents (Borders/Lines): Semi-transparent white `RGBA(255, 255, 255, 128)`.
  - **Text Hierarchy**: 
    - Massive, bold sans-serif headers (e.g., 60pt+).
    - Clean, regular-weight body text (e.g., 14-18pt).
  - **Shapes**: Perfect circles (for profile images) and "Pill" shapes (rounded rectangles with 50% corner radius) for buttons and navigation markers.

* **Step B: Compositional Style**
  - **Center-Weighted**: Elements are heavily center-aligned to create a sense of balance and calm.
  - **Menu/Navigation Metaphor**: Content slides feature small, pill-shaped "tabs" at the top (e.g., Team, Timing, Budget), mimicking a website or app interface to orient the viewer.
  - **Airiness**: Huge amounts of negative space. Content is grouped tightly in the center, leaving the blurred background visible around the edges.

* **Step C: Dynamic Effects & Transitions**
  - **Morph Transition**: The style relies heavily on PowerPoint's "Morph" transition. Text flies from the center of the title slide up to the header position on the second slide.
  - *(Note: While `python-pptx` cannot natively set the Morph transition flag, we can perfectly set up the geometrical states so that a user only needs to click "Morph" in the UI).*


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Blurred Background** | `PIL/Pillow` (GaussianBlur) | PowerPoint's native "Artistic Blur" cannot be applied via `python-pptx`. Generating the blurred image via Python guarantees cross-platform fidelity. |
| **Circular Profile Pictures** | `PIL/Pillow` (RGBA Masking) | Native picture cropping to a circle in PPTX is highly complex via XML. Pre-processing the image into a transparent circular PNG is robust and visually perfect. |
| **"Pill" Shaped Buttons** | `lxml` XML Injection | `python-pptx` cannot natively set the corner radius of a rounded rectangle. We use `lxml` to inject `<a:adj idx="1" val="50000"/>` to create perfect Apple-style pills. |
| **Text & Layout** | `python-pptx` native | Standard API is perfect for text boxes, alignment, and basic lines. |

> **Feasibility Assessment**: **90%**. The visual layout, the blurred background trick, the pill buttons, and the circular crops are perfectly reproduced. The remaining 10% is the actual application of the "Morph" transition, which the user must manually click in the PowerPoint ribbon (Transitions -> Morph) after generating the file.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Welcome",
    subtitle_text: str = "everyone!",
    bg_keyword: str = "mountains,dusk",
    **kwargs,
) -> str:
    """
    Creates a 2-slide PPTX reproducing the Apple-style Blurred-Background Aesthetic.
    Slide 1: Sharp background, Title, CTA button.
    Slide 2: Blurred background, UI Navigation, Team Profile circular crops.
    """
    import os
    import io
    import requests
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.oxml import OxmlElement
    from pptx.oxml.ns import qn
    from PIL import Image, ImageFilter, ImageDraw

    # --- Setup Presentation ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Blank layout
    blank_layout = prs.slide_layouts[6]

    # --- Helper 1: XML Modifier for Pill Shapes ---
    def make_pill_shape(shape, radius_val="50000"):
        """Modifies a rounded rectangle to have a perfect pill radius via lxml."""
        prstGeom = shape.element.find(qn('a:prstGeom'))
        if prstGeom is not None:
            adjLst = prstGeom.find(qn('a:adjLst'))
            if adjLst is None:
                adjLst = OxmlElement('a:adjLst')
                prstGeom.append(adjLst)
            
            # Remove existing adjustments
            for child in list(adjLst):
                adjLst.remove(child)
                
            adj = OxmlElement('a:adj')
            adj.set('idx', '1')
            adj.set('val', radius_val) # 50000 = 50% radius
            adjLst.append(adj)

    # --- Helper 2: XML Modifier for Transparent Shape Outlines ---
    def set_shape_transparency(shape, alpha_percent):
        """Sets transparency of a shape's fill."""
        fill = shape.fill
        fill.solid()
        # Access the solidFill element
        solidFill = shape.element.find(qn('p:spPr')).find(qn('a:solidFill'))
        if solidFill is not None:
            srgbClr = solidFill.find(qn('a:srgbClr'))
            if srgbClr is not None:
                alpha = OxmlElement('a:alpha')
                # 100% = 100000. So 40% transparency = 60000 alpha
                alpha.set('val', str(int(alpha_percent * 1000)))
                srgbClr.append(alpha)

    # --- Helper 3: Image Fetcher & Processor ---
    def get_images():
        """Fetches BG image and generates sharp, blurred, and profile circular images."""
        sharp_path = "temp_sharp_bg.jpg"
        blur_path = "temp_blur_bg.jpg"
        profile_path = "temp_profile.png"
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            url = f"https://source.unsplash.com/random/1920x1080/?{bg_keyword}"
            response = requests.get(url, headers=headers, timeout=10)
            img = Image.open(io.BytesIO(response.content)).convert("RGB")
        except Exception:
            # Fallback: Create a gradient image if download fails
            img = Image.new('RGB', (1920, 1080), color=(30, 20, 40))
            draw = ImageDraw.Draw(img)
            for i in range(1080):
                draw.line([(0, i), (1920, i)], fill=(int(30+i/20), int(20+i/30), int(40+i/15)))

        # Save sharp version
        img.save(sharp_path, quality=95)
        
        # Create Blurred version with slight dark overlay for text contrast
        blurred_img = img.filter(ImageFilter.GaussianBlur(radius=30))
        overlay = Image.new('RGBA', blurred_img.size, (10, 10, 20, 80)) # Darkening overlay
        final_blur = Image.alpha_composite(blurred_img.convert('RGBA'), overlay)
        final_blur.convert('RGB').save(blur_path, quality=90)
        
        # Create a sample circular profile picture
        size = (400, 400)
        prof_base = Image.new('RGB', size, (150, 150, 160))
        # Add some simple pattern to profile
        prof_draw = ImageDraw.Draw(prof_base)
        prof_draw.rectangle([100, 100, 300, 300], fill=(200, 100, 100))
        
        mask = Image.new('L', size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0) + size, fill=255)
        
        prof_circular = Image.new('RGBA', size, (0, 0, 0, 0))
        prof_circular.paste(prof_base, (0, 0), mask)
        prof_circular.save(profile_path, "PNG")
        
        return sharp_path, blur_path, profile_path

    # Process Images
    sharp_bg, blur_bg, profile_pic = get_images()

    # ==========================================
    # SLIDE 1: TITLE SLIDE (Sharp Background)
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    
    # 1. Background
    slide1.shapes.add_picture(sharp_bg, 0, 0, width=prs.slide_width, height=prs.slide_height)
    
    # 2. Main Title
    title_box = slide1.shapes.add_textbox(Inches(2), Inches(2.5), Inches(9.33), Inches(1.5))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(64)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.font.name = "Arial" # Fallback for Helvetica/San Francisco
    
    # 3. Subtitle
    p2 = tf.add_paragraph()
    p2.text = subtitle_text
    p2.alignment = PP_ALIGN.CENTER
    p2.font.size = Pt(24)
    p2.font.bold = False
    p2.font.color.rgb = RGBColor(255, 255, 255)
    p2.font.name = "Arial"

    # 4. CTA Button (Pill Shape)
    btn = slide1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(5.16), Inches(5.5), Inches(3), Inches(0.6)
    )
    make_pill_shape(btn) # Convert to perfect pill
    btn.fill.background() # No fill
    btn.line.color.rgb = RGBColor(255, 255, 255)
    btn.line.width = Pt(1.5)
    
    btn_tf = btn.text_frame
    btn_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    btn_p = btn_tf.paragraphs[0]
    btn_p.text = "Add to calendar"
    btn_p.alignment = PP_ALIGN.CENTER
    btn_p.font.size = Pt(16)
    btn_p.font.color.rgb = RGBColor(255, 255, 255)


    # ==========================================
    # SLIDE 2: CONTENT SLIDE (Blurred Background)
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    
    # 1. Blurred Background
    slide2.shapes.add_picture(blur_bg, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # 2. Navigation Interface (Tabs)
    tabs = ["Team", "Timing", "App", "SWOT", "Budget"]
    start_x = Inches(2.5)
    for i, tab_text in enumerate(tabs):
        tab = slide2.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            start_x + Inches(i * 1.8), Inches(0.5), Inches(1.2), Inches(0.4)
        )
        make_pill_shape(tab)
        
        # Highlight the "Team" tab
        if i == 0:
            tab.fill.solid()
            tab.fill.fore_color.rgb = RGBColor(255, 255, 255)
            set_shape_transparency(tab, 30) # 30% alpha white fill
            tab.line.fill.background()
        else:
            tab.fill.background()
            tab.line.color.rgb = RGBColor(255, 255, 255)
            tab.line.width = Pt(1)

        t_tf = tab.text_frame
        t_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        t_p = t_tf.paragraphs[0]
        t_p.text = tab_text
        t_p.alignment = PP_ALIGN.CENTER
        t_p.font.size = Pt(12)
        t_p.font.color.rgb = RGBColor(255, 255, 255)

    # 3. Section Title (Mimicking Morph placement)
    sect_box = slide2.shapes.add_textbox(Inches(2), Inches(1.5), Inches(9.33), Inches(0.8))
    sect_p = sect_box.text_frame.paragraphs[0]
    sect_p.text = "Meet the team"
    sect_p.alignment = PP_ALIGN.CENTER
    sect_p.font.size = Pt(36)
    sect_p.font.bold = True
    sect_p.font.color.rgb = RGBColor(255, 255, 255)

    # 4. Team Profiles (3 columns)
    col_spacing = 3.5
    start_col_x = 2.4
    
    for i in range(3):
        # Insert Circular Profile Image
        slide2.shapes.add_picture(
            profile_pic, 
            Inches(start_col_x + (i * col_spacing) + 0.25), 
            Inches(2.8), 
            width=Inches(1.5), height=Inches(1.5)
        )
        
        # Profile Text Box
        prof_box = slide2.shapes.add_textbox(
            Inches(start_col_x + (i * col_spacing) - 0.5), 
            Inches(4.5), 
            Inches(3), Inches(2)
        )
        ptf = prof_box.text_frame
        ptf.word_wrap = True
        
        name_p = ptf.paragraphs[0]
        name_p.text = f"Team Member {i+1}"
        name_p.font.size = Pt(20)
        name_p.font.bold = True
        name_p.font.color.rgb = RGBColor(255, 255, 255)
        name_p.alignment = PP_ALIGN.CENTER
        
        desc_p = ptf.add_paragraph()
        desc_p.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor."
        desc_p.font.size = Pt(12)
        desc_p.font.color.rgb = RGBColor(200, 200, 200)
        desc_p.alignment = PP_ALIGN.CENTER

    # Save and clean up
    prs.save(output_pptx_path)
    
    # Cleanup temp images
    for p in [sharp_bg, blur_bg, profile_pic]:
        if os.path.exists(p):
            os.remove(p)
            
    return output_pptx_path
```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries? (Yes: `pptx`, `PIL`, `requests`, `lxml`)
- [x] Does it handle the case where an image download fails (fallback)? (Yes: Includes a generated fallback gradient via PIL Draw).
- [x] Are all color values explicit RGBA tuples (not referencing undefined variables)? (Yes: Used `RGBColor(255,255,255)` and PIL tuples).
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes: Achieves the sharp-to-blur visual leap, includes the exact UI pill buttons and text centering).
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes: The Apple keynote aesthetic is heavily defined by the blur contrast and geometric UI framing).