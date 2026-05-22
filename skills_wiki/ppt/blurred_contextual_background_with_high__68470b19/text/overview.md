# Blurred Contextual Background with High-Contrast Typography

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Blurred Contextual Background with High-Contrast Typography

* **Core Visual Mechanism**: This style relies on a heavily blurred, contextual photograph acting as a deep background canvas. By applying a strong Gaussian blur and a slight darkening overlay to a standard screenshot or photo, the image is abstracted into a soft wash of thematic colors. Above this, massive, stark-white, bold typography is placed centrally, anchored by a distinct drop shadow to sever it from the background layer.

* **Why Use This Skill (Rationale)**: This technique solves a fundamental presentation problem: providing visual context without sacrificing text legibility. A raw screenshot or photo is often too "noisy" and makes text hard to read. Blurring it creates depth (simulating a camera's shallow depth of field) and removes distracting details, while retaining the overall color palette and contextual "vibe" of the topic.

* **Overall Applicability**: This is the gold standard for tutorial title slides, video thumbnails, section headers, and hero slides where a single, punchy statement needs to be made against a thematic backdrop (e.g., software tutorials, tech product launches).

* **Value Addition**: Transforms a plain text slide into a cinematic, modern title card. It feels like premium video production rather than a standard PowerPoint template.


### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background Layer**: A high-resolution image relevant to the topic, subjected to a heavy Gaussian blur (radius ~30px).
  - **Dimming Overlay**: A semi-transparent black layer (`(0, 0, 0, 75)` or ~30% opacity) covering the background to guarantee high contrast.
  - **Text Style**: Pure white `(255, 255, 255)` sans-serif font (like Arial or Helvetica), extremely large weight and size.
  - **Shadow**: A distinct outer drop shadow on the text (Black, ~60% opacity, slightly offset downward) to lift the text off the canvas.

* **Step B: Compositional Style**
  - **Title Placement**: Dead center, usually spanning 80% of the slide width, breaking into 2-3 lines if necessary.
  - **Branding**: A small, minimalist, bold text element anchored in the extreme top-right corner (mimicking the "INSIDER" watermark in the tutorial).
  - **Margin**: Generous breathing room around the central text block.

* **Step C: Dynamic Effects & Transitions**
  - Usually paired with a simple "Fade" transition. The static depth created by the blur means complex animations are unnecessary; the visual impact is immediate upon appearance.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Heavily blurred background | `PIL/Pillow` | Native PowerPoint cannot programmatically apply heavy Gaussian blurs to images via code. PIL is required to process the image and composite the dark overlay. |
| Text Placement & Formatting | `python-pptx` | Standard API is perfect for precise coordinate placement and basic font styling. |
| Text Drop Shadow | `lxml` (XML Injection) | `python-pptx` does not expose an API for adding shadows specifically to *text characters* (applying it to the shape often shadows the bounding box). Injecting `<a:outerShdw>` into the text run properties solves this. |

> **Feasibility Assessment**: 100%. The combination of PIL for the visual backdrop and lxml for the typographic finish perfectly reproduces the cinematic title slide aesthetic seen at the start of the tutorial.

#### 3b. Complete Reproduction Code

```python
import os
import io
import urllib.request
from PIL import Image, ImageFilter
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def create_slide(
    output_pptx_path: str,
    title_text: str = "How to use split\nscreen on Windows 10",
    branding_text: str = "INSIDER",
    bg_keyword: str = "windows desktop", 
    **kwargs,
) -> str:
    """
    Creates a presentation slide with a deeply blurred contextual background
    and high-contrast, drop-shadowed typography.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Helper Function: Inject Text Shadow via lxml ===
    def add_text_shadow(run, opacity=60000, blur_rad="38100", dist="38100", dir="2700000"):
        # Access the run properties XML element
        rPr = run._r.get_or_add_rPr()
        ns_main = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
        
        effectLst = etree.SubElement(rPr, f'{ns_main}effectLst')
        outerShdw = etree.SubElement(effectLst, f'{ns_main}outerShdw', 
                                     blurRad=blur_rad, dist=dist, dir=dir, algn="tl", rotWithShape="0")
        srgbClr = etree.SubElement(outerShdw, f'{ns_main}srgbClr', val="000000")
        etree.SubElement(srgbClr, f'{ns_main}alpha', val=str(opacity))

    # === Layer 1: Generate Blurred Contextual Background ===
    width_px, height_px = 1920, 1080
    bg_image_path = "temp_blurred_bg.png"
    
    # Fetch image (using picsum as a reliable fallback/placeholder for Unsplash)
    # The seed ensures a consistent image based on the keyword length/characters
    url = f"https://picsum.photos/seed/{bg_keyword.replace(' ', '')}/{width_px}/{height_px}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            base_img = Image.open(io.BytesIO(response.read())).convert("RGBA")
    except Exception:
        # Fallback to a solid tech-blue gradient-like base if download fails
        base_img = Image.new("RGBA", (width_px, height_px), (30, 60, 90, 255))

    # 1. Apply heavy Gaussian Blur
    blurred_img = base_img.filter(ImageFilter.GaussianBlur(radius=25))
    
    # 2. Apply a dark overlay (30% opacity black) to ensure white text pops
    overlay = Image.new("RGBA", (width_px, height_px), (0, 0, 0, 85))
    final_bg = Image.alpha_composite(blurred_img, overlay)
    final_bg.save(bg_image_path)

    # Insert background into slide
    slide.shapes.add_picture(bg_image_path, 0, 0, prs.slide_width, prs.slide_height)

    # === Layer 2: Main Title Typography ===
    title_left = Inches(1)
    title_top = Inches(2.5)
    title_width = prs.slide_width - Inches(2)
    title_height = Inches(2.5)
    
    title_box = slide.shapes.add_textbox(title_left, title_top, title_width, title_height)
    title_tf = title_box.text_frame
    title_tf.word_wrap = True
    title_tf.vertical_anchor = 3 # Middle
    
    p = title_tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    
    # Format Title
    run = p.runs[0]
    run.font.name = 'Arial'
    run.font.size = Pt(68)
    run.font.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255)
    
    # Inject aggressive drop shadow to match the tutorial aesthetic
    add_text_shadow(run, opacity=70000, blur_rad="50000", dist="40000")

    # === Layer 3: Top Right Branding (e.g., "INSIDER" watermark) ===
    brand_width = Inches(2.5)
    brand_left = prs.slide_width - brand_width - Inches(0.5)
    brand_top = Inches(0.4)
    brand_height = Inches(0.5)
    
    brand_box = slide.shapes.add_textbox(brand_left, brand_top, brand_width, brand_height)
    brand_p = brand_box.text_frame.paragraphs[0]
    brand_p.text = branding_text.upper()
    brand_p.alignment = PP_ALIGN.RIGHT
    
    brand_run = brand_p.runs[0]
    brand_run.font.name = 'Arial'
    brand_run.font.size = Pt(22)
    brand_run.font.bold = True
    brand_run.font.color.rgb = RGBColor(255, 255, 255)
    
    # Inject subtle drop shadow on branding
    add_text_shadow(brand_run, opacity=50000, blur_rad="20000", dist="20000")

    # Save and cleanup
    prs.save(output_pptx_path)
    if os.path.exists(bg_image_path):
        os.remove(bg_image_path)
        
    return output_pptx_path
```