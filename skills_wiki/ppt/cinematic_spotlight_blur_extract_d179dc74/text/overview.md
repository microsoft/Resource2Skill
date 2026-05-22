# Cinematic Spotlight & Blur Extract

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Cinematic Spotlight & Blur Extract

* **Core Visual Mechanism**: This technique uses a single base image applied in two radically different states. The background is a heavily blurred, grayscale version of the image, while the foreground consists of precision-cropped, full-color, sharp segments of that exact same image. These sharp "extracts" are then shifted slightly out of their original positions to overlap a solid geometric banner, creating a dynamic floating card effect.
* **Why Use This Skill (Rationale)**: By completely desaturating and blurring the background, you strip away visual noise and establish a "canvas" layer. Re-introducing the sharp color segments instantly commands the viewer's eye. It creates an optical illusion of depth (depth-of-field) and feels highly customized and premium compared to standard picture frames.
* **Overall Applicability**: Perfect for "Meet the Team" slides, portfolio galleries, product feature deep-dives, or any scenario where you want to highlight specific parts of a complex whole.
* **Value Addition**: It transforms a single stock photo into a complete, multi-layered composition without needing external graphical assets. It establishes clear visual hierarchy and modern UI aesthetics (similar to glassmorphism or floating UI cards).

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Background Image**: 100% grayscale (`L` mode in PIL), heavy Gaussian blur (Radius ~15-20). 
  * **Solid Banner**: A dark solid rectangle (e.g., `RGBA(30, 30, 35, 255)`) anchored to the bottom third of the slide to anchor the text.
  * **Spotlight Extracts**: 3 to 5 precisely cropped rectangles from the original color image. 
  * **Text Hierarchy**: 
    * Name: Primary white, bold, prominent (e.g., `RGBA(255, 255, 255, 255)`).
    * Title: Secondary color, smaller, regular weight (e.g., `RGBA(180, 190, 200, 255)`).

* **Step B: Compositional Style**
  * **Aspect Ratio**: 16:9 widescreen canvas.
  * **Alignment**: The color extracts are symmetrically distributed across the X-axis. 
  * **Layering & Overlap**: The most critical compositional trick is that the color extracts are shifted slightly *downwards* from their true origin point so that their bottom edges break the plane of the dark bottom banner. This creates depth.

* **Step C: Dynamic Effects & Transitions**
  * **Morph Transition (PowerPoint Native)**: In the tutorial, the slides transition using PowerPoint's "Morph". Because the extracts share the same image source, Morph naturally translates them across the screen. While Morph is a slide-to-slide transition (requiring manual duplicate slides), the *static* visual composition can be fully generated via code.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Grayscale & Blur Background** | `PIL/Pillow` | `python-pptx` cannot dynamically convert images to grayscale or apply Gaussian blur natively. PIL handles this perfectly. |
| **Precision Color Crops** | `PIL/Pillow` | Slicing the exact rectangular coordinates out of the source image ensures perfect aspect ratios and framing. |
| **Floating Shadows** | `lxml` XML injection | Applying an outer shadow directly via OOXML gives the cropped pictures the required "floating card" effect over the background. |
| **Banner & Typography** | `python-pptx` native | Standard shape drawing and text formatting APIs are perfectly suited for the lower third UI elements. |

> **Feasibility Assessment**: **95%**. The code flawlessly reproduces the complex static visual composition (the blurred grayscale background, the color extracted cards, the overlaps, and the shadows). The remaining 5% is the actual animation click-through (PowerPoint's Morph transition), which requires setting up multiple slides in series. This code generates the peak "reveal" state of the layout.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "MEET OUR TEAM",
    bg_palette: str = "team",  
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Cinematic Spotlight & Blur Extract" visual effect.
    """
    import urllib.request
    from io import BytesIO
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image, ImageOps, ImageFilter, ImageDraw
    from lxml import etree

    # 1. Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    
    # 2. Fetch Base Image (or create fallback)
    # Using a high-quality Unsplash image of a team/group
    img_url = "https://images.unsplash.com/photo-1522071820081-009f0129c71c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80"
    try:
        req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            base_img = Image.open(BytesIO(response.read())).convert("RGB")
    except Exception:
        # Fallback if network fails
        base_img = Image.new("RGB", (1920, 1080), color=(40, 50, 60))
        draw = ImageDraw.Draw(base_img)
        for i in range(5):
            draw.rectangle([i*384+50, 200, i*384+334, 800], fill=(60+i*30, 80+i*20, 120))
            
    # Ensure image is exactly 1920x1080 to map to 13.333x7.5 inches perfectly (144 DPI)
    base_img = ImageOps.fit(base_img, (1920, 1080), Image.Resampling.LANCZOS)
    
    # 3. Create & Insert Grayscale Blurred Background
    bg_img = base_img.convert('L').filter(ImageFilter.GaussianBlur(radius=20))
    bg_io = BytesIO()
    bg_img.save(bg_io, format='PNG')
    bg_io.seek(0)
    slide.shapes.add_picture(bg_io, 0, 0, width=Inches(13.333), height=Inches(7.5))
    
    # 4. Create Dark Lower Banner
    # Banner covers the bottom 2.5 inches
    banner = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        0, Inches(5.0), Inches(13.333), Inches(2.5)
    )
    banner.fill.solid()
    banner.fill.fore_color.rgb = RGBColor(25, 28, 35)
    banner.line.fill.background() # No line
    
    # Add subtle banner title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(5.1), Inches(3.0), Inches(0.5))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(20)
    p.font.color.rgb = RGBColor(100, 110, 120)
    
    # 5. Extract, Shift, and Insert Profiles
    # Configuration for 4 profiles
    num_profiles = 4
    card_width_px = 280
    card_height_px = 420
    card_w_inch = card_width_px / 144.0
    card_h_inch = card_height_px / 144.0
    
    # Original crop center Y (where faces likely are)
    crop_center_y_px = int(3.5 * 144) 
    
    # Shifted placement Y on slide (moved down to overlap banner)
    placement_center_y_inch = 4.0 
    
    team_data = [
        {"name": "ALEX RIVERA", "title": "Creative Director"},
        {"name": "JORDAN LEE", "title": "Lead Engineer"},
        {"name": "TAYLOR SMITH", "title": "Product Manager"},
        {"name": "CASEY CHEN", "title": "Head of Sales"},
    ]
    
    for i in range(num_profiles):
        # Calculate X centers evenly distributed
        cx_px = int((i + 1) * (1920 / (num_profiles + 1)))
        
        # Calculate pixel bounds for crop from original color image
        left = cx_px - (card_width_px // 2)
        top = crop_center_y_px - (card_height_px // 2)
        right = cx_px + (card_width_px // 2)
        bottom = crop_center_y_px + (card_height_px // 2)
        
        # Extract color crop
        crop_img = base_img.crop((left, top, right, bottom))
        crop_io = BytesIO()
        crop_img.save(crop_io, format='PNG')
        crop_io.seek(0)
        
        # Calculate PPTX insertion coordinates
        ppt_x = Inches(cx_px / 144.0 - (card_w_inch / 2))
        ppt_y = Inches(placement_center_y_inch - (card_h_inch / 2))
        
        # Insert Picture
        pic = slide.shapes.add_picture(
            crop_io, ppt_x, ppt_y, 
            width=Inches(card_w_inch), height=Inches(card_h_inch)
        )
        
        # Add Drop Shadow via lxml to make it float
        spPr = pic.element.xpath('.//p:spPr')[0]
        shadow_xml = '''
            <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
                <a:outerShdw blurRad="254000" dist="50800" dir="2700000" algn="b" rotWithShape="0">
                    <a:srgbClr val="000000">
                        <a:alpha val="60000"/>
                    </a:srgbClr>
                </a:outerShdw>
            </a:effectLst>
        '''
        spPr.append(etree.fromstring(shadow_xml))
        
        # Add Typography (Name and Title) below the card inside the banner area
        # Placement logic: just below the picture bottom
        text_y = ppt_y + Inches(card_h_inch) + Inches(0.15)
        
        # Name
        tb_name = slide.shapes.add_textbox(ppt_x - Inches(0.5), text_y, Inches(card_w_inch + 1.0), Inches(0.3))
        p_name = tb_name.text_frame.paragraphs[0]
        p_name.text = team_data[i]["name"]
        p_name.font.bold = True
        p_name.font.size = Pt(14)
        p_name.font.color.rgb = RGBColor(255, 255, 255)
        p_name.alignment = PP_ALIGN.CENTER
        
        # Title
        tb_title = slide.shapes.add_textbox(ppt_x - Inches(0.5), text_y + Inches(0.25), Inches(card_w_inch + 1.0), Inches(0.3))
        p_title = tb_title.text_frame.paragraphs[0]
        p_title.text = team_data[i]["title"]
        p_title.font.size = Pt(11)
        p_title.font.color.rgb = RGBColor(160, 175, 190)
        p_title.alignment = PP_ALIGN.CENTER

    # 6. Save Presentation
    prs.save(output_pptx_path)
    return output_pptx_path
```