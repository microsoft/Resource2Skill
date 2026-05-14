# Aspect-Perfect Shape Masks

## Analysis

# Agent Skill: Aspect-Perfect Shape Masks

### 1. High-level Design Pattern Extraction

> **Skill Name**: Aspect-Perfect Shape Masks

* **Core Visual Mechanism**: Placing photographs inside non-rectangular geometric shapes (circles, hexagons, diamonds) **without aspect ratio distortion**. The image maintains its natural proportions while perfectly filling the custom boundary.
* **Why Use This Skill (Rationale)**: Native PowerPoint "Picture Fill" often aggressively stretches or squashes images to fit the bounding box of a shape. This makes portraits look unnatural. By pre-cropping the image to match the bounding box aspect ratio (typically 1:1 for circles and regular polygons), the image sits naturally inside the shape, instantly elevating the professionalism of the design.
* **Overall Applicability**: Essential for "Meet the Team" slides (headshots in circles), testimonial avatars, portfolio highlights, and creative title slide collages where standard rectangular photos feel too rigid.
* **Value Addition**: Transforms standard photos into stylized, modern design elements while completely avoiding the amateurish "stretched face" look. Furthermore, because the fill is anchored to a native shape, the shape itself can be dynamically changed later (e.g., from circle to hexagon) while retaining the perfect crop.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Subject Image**: High-quality portrait or focal-point image.
  - **Container Shape**: Native geometric shapes (Oval, Hexagon, Diamond).
  - **Color Logic**: Often accompanied by clean, thin borders (e.g., White `(255, 255, 255, 255)` or matching theme colors) to define the edge against the background.
* **Step B: Compositional Style**
  - Grid or inline alignment of multiple masked shapes.
  - Container shapes are typically sized symmetrically (1:1 bounding box, e.g., 3x3 inches) to maintain regular geometry.
* **Step C: Dynamic Effects & Transitions**
  - Because these are native PowerPoint shapes with picture fills, they natively support the "Change Shape" feature in PPTX, seamlessly morphing the mask boundary without altering the picture data.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Preventing image distortion** | `PIL/Pillow` (Center Crop) | `python-pptx` `user_picture()` fill naturally stretches images to bounding boxes. To prevent distortion, we use PIL to pre-crop the image to a perfect 1:1 aspect ratio *before* injecting it. |
| **Shape masking** | `python-pptx` native (`user_picture`) | Applying the 1:1 cropped image as a picture fill to a 1:1 shape (like a 3x3 inch Oval) natively masks the image without any stretching, perfectly replicating the tutorial's final result. |

> **Feasibility Assessment**: 100% — This hybrid programmatic approach perfectly bypasses the PowerPoint distortion issue highlighted in the tutorial, producing flawless, changeable shape-masked images.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Meet The Team",
    body_text: str = "",
    bg_palette: str = "portrait", 
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Aspect-Perfect Shape Masks visual effect.
    Demonstrates how to put pictures into shapes without aspect ratio distortion.
    
    Returns: path to the saved PPTX file.
    """
    import os
    import urllib.request
    from PIL import Image, ImageDraw
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.dml.color import RGBColor

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank layout and add custom title
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Add Title
    title_box = slide.shapes.add_textbox(Inches(1), Inches(0.8), Inches(11), Inches(1))
    title_tf = title_box.text_frame
    title_p = title_tf.paragraphs[0]
    title_p.text = title_text
    title_p.font.size = Pt(44)
    title_p.font.bold = True
    title_p.font.color.rgb = RGBColor(40, 40, 40)

    # Add Subtitle explaining the effect
    sub_box = slide.shapes.add_textbox(Inches(1), Inches(1.5), Inches(11), Inches(0.5))
    sub_tf = sub_box.text_frame
    sub_p = sub_tf.paragraphs[0]
    sub_p.text = "Images are perfectly masked without stretching or aspect ratio distortion."
    sub_p.font.size = Pt(18)
    sub_p.font.color.rgb = RGBColor(100, 100, 100)

    # === Image Acquisition & Pre-processing (The Anti-Distortion Step) ===
    # Download a sample portrait
    img_url = "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=800&auto=format&fit=crop"
    temp_img = "temp_portrait_raw.jpg"
    temp_cropped = "temp_portrait_1x1.jpg"
    
    try:
        # Download image
        req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(temp_img, 'wb') as out_file:
            out_file.write(response.read())
            
        # Crop image to 1:1 aspect ratio using PIL
        # This is the programmatic equivalent of the tutorial's manual crop adjustment
        img = Image.open(temp_img)
        width, height = img.size
        min_dim = min(width, height)
        
        # Calculate center crop box
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = (width + min_dim) / 2
        bottom = (height + min_dim) / 2
        
        img_cropped = img.crop((left, top, right, bottom))
        img_cropped.save(temp_cropped)
        
    except Exception as e:
        # Fallback if download fails: Create a 1:1 placeholder image using PIL
        img_fallback = Image.new('RGB', (800, 800), color=(70, 130, 180))
        draw = ImageDraw.Draw(img_fallback)
        draw.line((0,0, 800,800), fill=(100, 160, 210), width=10)
        draw.line((0,800, 800,0), fill=(100, 160, 210), width=10)
        img_fallback.save(temp_cropped)

    # === Shape Generation & Injection ===
    # We will map the 1:1 image onto shapes that have 1:1 bounding boxes.
    # Because both ratios match perfectly, pptx's native stretch fill results in NO distortion.
    
    shape_configs = [
        {"type": MSO_SHAPE.OVAL, "x": 1.5, "y": 3.0, "label": "Circle Mask"},
        {"type": MSO_SHAPE.HEXAGON, "x": 5.16, "y": 3.0, "label": "Hexagon Mask"},
        {"type": MSO_SHAPE.DIAMOND, "x": 8.83, "y": 3.0, "label": "Diamond Mask"}
    ]
    
    shape_size = 3.0 # 3x3 inches ensures a 1:1 bounding box

    for config in shape_configs:
        # Add the geometry shape
        shape = slide.shapes.add_shape(
            config["type"], 
            Inches(config["x"]), 
            Inches(config["y"]), 
            Inches(shape_size), 
            Inches(shape_size)
        )
        
        # Apply the pre-cropped 1:1 picture fill
        shape.fill.user_picture(temp_cropped)
        
        # Apply a clean border to frame it nicely
        shape.line.color.rgb = RGBColor(220, 220, 220)
        shape.line.width = Pt(2)
        
        # Add a small label underneath
        lbl_box = slide.shapes.add_textbox(
            Inches(config["x"]), 
            Inches(config["y"] + shape_size + 0.2), 
            Inches(shape_size), 
            Inches(0.5)
        )
        lbl_p = lbl_box.text_frame.paragraphs[0]
        lbl_p.text = config["label"]
        lbl_p.font.size = Pt(14)
        lbl_p.font.color.rgb = RGBColor(120, 120, 120)
        lbl_p.alignment = 2 # center (PP_ALIGN.CENTER equivalent)

    prs.save(output_pptx_path)
    
    # Cleanup temporary image files
    for temp_file in [temp_img, temp_cropped]:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
                
    return output_pptx_path
```