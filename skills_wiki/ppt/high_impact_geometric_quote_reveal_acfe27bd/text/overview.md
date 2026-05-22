# High-Impact Geometric Quote Reveal

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: High-Impact Geometric Quote Reveal

* **Core Visual Mechanism**: A stark, high-contrast composition that juxtaposes a black-and-white portrait against a vibrant, solid-color geometric container (a perfect circle or skewed rectangle). Set against a dark background, this aesthetic uses oversized, watermarked quotation marks and selective text highlighting (matching the geometric shape's color) to create visual harmony between the graphic and the text.

* **Why Use This Skill (Rationale)**: Converting the portrait to black and white removes distracting background colors and grants the subject a sense of historical weight, authority, or timelessness. The vibrant geometric shape injects modern energy and draws the eye immediately to the subject. The selective coloring of one or two keywords in the quote acts as a cognitive anchor, ensuring the audience remembers the core message. 

* **Overall Applicability**: Ideal for keynote addresses, core company values, leadership quotes, customer testimonials, and transition slides in high-stakes corporate presentations.

* **Value Addition**: Transforms a standard "text and picture" slide into a premium, poster-like composition. It forces brevity (as the text must be large) and creates an emotional connection through the stylized portraiture.


### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: Dark, sophisticated slate/navy or dark radial gradient. (e.g., `(24, 26, 30)`).
  - **Portrait**: High-quality headshot, strictly converted to Grayscale/B&W.
  - **Container Shape**: A distinct geometric primitive (Circle, Parallelogram, or split-rectangle) using a vibrant, high-contrast accent color:
    - Yellow: `(255, 204, 0)`
    - Mint Green: `(92, 225, 166)`
    - Cyan: `(0, 229, 255)`
  - **Typography**: Heavy, modern sans-serif (e.g., Montserrat Bold or Bebas Neue). White text with specific keywords colored to match the container shape.
  - **Decorative Accents**: Oversized quotation marks (`"`) placed in the background as a subtle watermark or in a light gray `(70, 75, 80)` to add textural depth without overwhelming the text.

* **Step B: Compositional Style**
  - **Layout**: Asymmetrical balance. Typically, the text occupies the left 50-60% of the slide, left-aligned. The portrait and geometric container occupy the right 40%.
  - **Layering**: Bottom to Top -> Dark Background -> Oversized Quote Mark -> Accent Geometric Shape -> B&W Portrait -> Quote Text -> Attribution text.
  - **Alignment**: Strong horizontal axis connecting the visual center of the portrait with the vertical center of the text block.

* **Step C: Dynamic Effects & Transitions**
  - **Transitions**: The tutorial explicitly uses the "Push" transition (from bottom or side) to introduce the slide cleanly. 
  - **Animation (Optional)**: A simple fade-in for the text while the image flies in from the right.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **B&W Image & Circular Crop** | `PIL/Pillow` | Native `python-pptx` lacks simple APIs for applying B&W picture formatting *and* exact circular alpha masking simultaneously. PIL processes the image perfectly before insertion. |
| **Vibrant Geometric Container** | `python-pptx` native | Standard shape generation (Oval/Circle) allows for crisp vector edges and easy recoloring. |
| **Multi-color Text (Highlights)** | `python-pptx` native | Iterating through paragraph `runs` allows us to apply the accent color to specific target words in the quote natively. |
| **Watermark Quote Marks** | `python-pptx` native | Large font size with a dark gray color simulates the transparency/watermark effect without needing complex XML injection. |

> **Feasibility Assessment**: 95% reproduction. The code successfully recreates the dark theme, the B&W circular masked portrait, the vibrant background shape, the oversized quote marks, and the selectively highlighted typography. 

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    quote_text: str = "BE THE CHANGE THAT YOU WISH TO SEE IN THE WORLD.",
    author_text: str = "- Mahatma Gandhi",
    image_url: str = "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=800&auto=format&fit=crop",
    accent_color: tuple = (255, 204, 0),  # Vibrant Yellow
    highlight_words: list = ["CHANGE", "WORLD."], # Words to color in the quote
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the 'High-Impact Geometric Quote Reveal' effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image, ImageDraw
    import urllib.request
    from io import BytesIO
    import os

    # 1. Initialize Presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # 2. Set Dark Background
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(24, 26, 30)
    bg.line.fill.background()

    # 3. Add Watermark Oversized Quote Marks
    qm_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(3), Inches(3))
    qm_tf = qm_box.text_frame
    qm_p = qm_tf.add_paragraph()
    qm_p.text = "“"
    qm_p.font.name = "Arial Black"
    qm_p.font.size = Pt(250)
    qm_p.font.color.rgb = RGBColor(45, 48, 55) # Dark gray simulating watermark

    # 4. Prepare B&W Circular Image using PIL
    img_stream = BytesIO()
    try:
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img = Image.open(BytesIO(response.read())).convert("RGBA")
            
        # Crop to square
        size = min(img.size)
        left = (img.size[0] - size) / 2
        top = (img.size[1] - size) / 2
        img = img.crop((left, top, left + size, top + size))
        
        # Convert to Grayscale, then back to RGBA for masking
        img = img.convert("L").convert("RGBA")
        
        # Create circular alpha mask
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        img.putalpha(mask)
        img.save(img_stream, format="PNG")
        img_stream.seek(0)
    except Exception as e:
        print(f"Image download/processing failed: {e}. Using a solid gray circle instead.")
        # Fallback to a gray circle if download fails
        img = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, 800, 800), fill=(100, 100, 100, 255))
        img.save(img_stream, format="PNG")
        img_stream.seek(0)

    # 5. Place Accent Geometric Container (Yellow Circle)
    circle_size = Inches(5.2)
    circle_left = Inches(7.2)
    circle_top = Inches(1.15)
    
    accent_circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, circle_left, circle_top, circle_size, circle_size
    )
    accent_circle.fill.solid()
    accent_circle.fill.fore_color.rgb = RGBColor(*accent_color)
    accent_circle.line.fill.background() # No line

    # 6. Insert B&W Processed Image over the container (slightly offset)
    img_size = Inches(5.0)
    img_left = Inches(7.3)
    img_top = Inches(1.25)
    slide.shapes.add_picture(img_stream, img_left, img_top, img_size, img_size)

    # 7. Add Typography (The Quote)
    text_box = slide.shapes.add_textbox(Inches(1.5), Inches(2.8), Inches(5.0), Inches(2.5))
    text_frame = text_box.text_frame
    text_frame.word_wrap = True
    
    p = text_frame.add_paragraph()
    p.alignment = PP_ALIGN.LEFT
    p.line_spacing = 1.1
    
    # Process text for highlighting specific words
    words = quote_text.split()
    for word in words:
        run = p.add_run()
        run.text = word + " "
        run.font.name = "Montserrat"
        run.font.size = Pt(36)
        run.font.bold = True
        
        # Color highlight check
        clean_word = word.strip('.,;!?')
        if any(hw.upper() == clean_word.upper() or hw.upper() == word.upper() for hw in highlight_words):
            run.font.color.rgb = RGBColor(*accent_color)
        else:
            run.font.color.rgb = RGBColor(255, 255, 255)

    # 8. Add Attribution/Author
    p_author = text_frame.add_paragraph()
    p_author.alignment = PP_ALIGN.LEFT
    run_author = p_author.add_run()
    run_author.text = f"\n{author_text}"
    run_author.font.name = "Montserrat"
    run_author.font.size = Pt(20)
    run_author.font.color.rgb = RGBColor(200, 200, 200) # Light gray

    # Save
    prs.save(output_pptx_path)
    return output_pptx_path
```

#### 3c. Verification Checklist
- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback)?
- [x] Are all color values explicit RGBA/RGB tuples (not referencing undefined variables)?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?
- [x] Would someone looking at the output say "yes, that's the same technique"?