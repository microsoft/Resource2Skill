# Unified Master Layout Branding

## Analysis

# Skill Strategy: Unified Master Layout Branding

### 1. High-level Design Pattern Extraction

> **Skill Name**: Unified Master Layout Branding

* **Core Visual Mechanism**: The core visual idea is establishing strict visual consistency across an entire deck. This is achieved by shifting from a fragmented, default aesthetic (e.g., outdated serif fonts like Times New Roman) to a clean, modern sans-serif (like Segoe UI) and anchoring brand identity using a persistent, fixed-position logo (typically bottom-right). Furthermore, visual hierarchy is controlled by layout types—specifically, title slides receive extra contextual branding (like a speaker headshot) that does not clutter standard content slides.
* **Why Use This Skill (Rationale)**: From a design psychology perspective, consistency reduces cognitive load. When the font, colors, and logo placement remain static, the audience stops processing the layout and focuses entirely on the content. A jumping logo or changing font breaks immersion. Utilizing master-level rules ensures enterprise-grade professionalism.
* **Overall Applicability**: Essential for corporate pitch decks, company overviews, branded webinars, and any presentation where adherence to brand guidelines and cohesive storytelling are required.
* **Value Addition**: Transforms a basic, default presentation into a branded, professional asset. It creates a unified "wrapper" for the content, ensuring that no matter what the specific slide says, it unmistakably belongs to the company.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Typography**: Modern, readable sans-serif. The shift from a dated serif to `Segoe UI` (or similar clean fonts like Arial/Calibri) instantly modernizes the feel.
  - **Anchored Branding**: A company logo placed consistently across all slides.
  - **Color Logic**: High-contrast text on a clean background. Typical values would be `(0, 0, 0, 255)` for text on a white `(255, 255, 255, 255)` background. Brand accent colors are contained within the anchored logo.
  - **Layout-Specific Elements**: Speaker imagery or prominent graphics reserved strictly for the Title layout.

* **Step B: Compositional Style**
  - **Spatial Feel**: Unobtrusive branding. The logo is sized to occupy roughly 10-15% of the slide width and is tucked into the bottom right corner, keeping the main canvas clear for data and text.
  - **Layering**: The logo and master elements sit on the bottom-most layout layer, ensuring they do not interfere with or overlay the active slide content.

* **Step C: Dynamic Effects & Transitions**
  - This pattern relies entirely on static consistency. The "effect" is the seamless visual continuity experienced as the presenter transitions from slide to slide.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Consistent Typography** | `python-pptx` Text Frame parsing | `python-pptx` provides access to text runs, allowing us to programmatically override fonts (mimicking a Master font update). |
| **Anchored Master Branding** | `PIL/Pillow` + `python-pptx` | PIL is used to generate dynamic dummy brand assets (Logo and Speaker avatar). `python-pptx` inserts them at exact fixed coordinates across slides. |
| **Layout-Specific Rules** | Python conditional logic | Mimics the PowerPoint Slide Master hierarchy by applying specific assets only to Title slides vs. Content slides. |

> **Feasibility Assessment**: 100% — While `python-pptx` does not easily allow deep edits to the native XML Slide Master configurations of an existing template, we can achieve the exact same 100% visual outcome by wrapping our slide generation in programmatic "master" functions that enforce font and branding rules uniformly across all generated slides.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Kevin's Cookie Company",
    body_text: str = "Automated Master Layout Demo",
    bg_palette: str = "white",
    accent_color: tuple = (210, 105, 30),  # Cookie orange/brown
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Unified Master Layout Branding effect.
    Generates a Title slide and a Content slide with programmatic master-level 
    branding (consistent font, anchored logo, and conditional title assets).
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from PIL import Image, ImageDraw
    import os

    # Initialize presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # ==========================================
    # Layer 1: Generate Master Brand Assets via PIL
    # ==========================================
    logo_path = "master_logo_temp.png"
    # Create a nice branded badge
    logo_img = Image.new('RGBA', (250, 80), (255, 255, 255, 0))
    draw_logo = ImageDraw.Draw(logo_img)
    draw_logo.rounded_rectangle([(0,0), (249, 79)], radius=15, fill=(255, 245, 230, 255), outline=accent_color, width=4)
    # Simple geometry to represent a cookie/logo icon
    draw_logo.ellipse([(15, 15), (65, 65)], fill=accent_color)
    draw_logo.ellipse([(25, 25), (35, 35)], fill=(139, 69, 19, 255)) # Choc chip
    draw_logo.ellipse([(45, 35), (55, 45)], fill=(139, 69, 19, 255)) # Choc chip
    draw_logo.text((80, 30), "BRAND LOGO", fill=(0, 0, 0, 255)) 
    logo_img.save(logo_path)

    speaker_path = "master_speaker_temp.png"
    # Create a circular speaker headshot placeholder
    speaker_img = Image.new('RGBA', (200, 200), (255, 255, 255, 0))
    draw_spk = ImageDraw.Draw(speaker_img)
    draw_spk.ellipse([(0,0), (199, 199)], fill=(100, 150, 200, 255)) # Blue background
    draw_spk.ellipse([(60, 40), (140, 120)], fill=(200, 200, 200, 255)) # Head
    draw_spk.chord([(30, 120), (170, 260)], start=180, end=0, fill=(200, 200, 200, 255)) # Shoulders
    speaker_img.save(speaker_path)

    # ==========================================
    # Layer 2: Master Formatting Helper
    # ==========================================
    def apply_master_formatting(slide, is_title_layout=False):
        """Mimics editing the Slide Master by globally updating fonts and adding locked assets."""
        # 1. Force Global Font (equivalent to changing master font to Segoe UI)
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        run.font.name = 'Segoe UI'
                        
        # 2. Add anchored Global Logo (Bottom Right)
        slide.shapes.add_picture(logo_path, Inches(10.8), Inches(6.4), width=Inches(2.2))
        
        # 3. Add Layout-Specific Elements (e.g., speaker only on Title Layout)
        if is_title_layout:
            slide.shapes.add_picture(speaker_path, Inches(11.0), Inches(4.2), width=Inches(1.8))

    # ==========================================
    # Layer 3: Slide Generation
    # ==========================================
    
    # --- Slide 1: Title Layout ---
    slide1 = prs.slides.add_slide(prs.slide_layouts[0])
    slide1.shapes.title.text = title_text
    slide1.placeholders[1].text = body_text
    
    # Apply Master Logic
    apply_master_formatting(slide1, is_title_layout=True)

    # --- Slide 2: Content Layout ---
    slide2 = prs.slides.add_slide(prs.slide_layouts[1])
    slide2.shapes.title.text = "Company Progress"
    
    tf = slide2.placeholders[1].text_frame
    tf.text = "Sales should increase exponentially."
    tf.add_paragraph().text = "Customers love our products."
    tf.add_paragraph().text = "Staff love our unified branding."
    
    # Apply Master Logic (Notice is_title_layout is False, so no speaker is added)
    apply_master_formatting(slide2, is_title_layout=False)

    # Clean up temp assets
    try:
        os.remove(logo_path)
        os.remove(speaker_path)
    except:
        pass

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
```