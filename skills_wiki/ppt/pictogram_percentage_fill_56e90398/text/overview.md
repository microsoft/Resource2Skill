# Pictogram Percentage Fill

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Pictogram Percentage Fill

*   **Core Visual Mechanism**: This technique uses a universally understood icon as a data container, which is partially filled with a solid color from bottom to top to represent a percentage. The fill "level" visually communicates the data value, similar to a thermometer or a liquid-fill gauge, making the data instantly intuitive.

*   **Why Use This Skill (Rationale)**: This is a form of isotype visualization. It leverages relevant iconography to make data more engaging and memorable than abstract charts (like bars or pies). By replacing abstract shapes with meaningful symbols, it reduces the audience's cognitive load and enhances the narrative power of the data. The visual metaphor of "filling up" a container is immediately understood across cultures.

*   **Overall Applicability**: This style is excellent for:
    *   **Infographics**: Presenting key statistics in a visually dense but clear manner.
    *   **Dashboard Summaries**: Showing KPIs or project completion rates.
    *   **Single-Statistic Highlights**: Emphasizing a single, powerful data point on a slide (e.g., "80% customer satisfaction").
    *   **Comparative Stats**: Placing several pictograms side-by-side to compare metrics across different categories.

*   **Value Addition**: It transforms sterile numbers into a compelling visual story, increasing audience engagement and improving information retention. It's a powerful tool for simplifying complex data into an at-a-glance insight.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    - **Icon Base**: A simple, solid, single-color icon with a transparent background (PNG format is ideal). The tutorial uses a person icon.
    - **Background Layer**: The full icon, colorized in a neutral, desaturated tone to represent the 100% total. A common choice is light gray, e.g., `(217, 217, 217, 255)`.
    - **Fill Layer**: The same icon, but colorized with a vibrant accent color. This layer is vertically clipped from the top, so only the bottom portion corresponding to the data percentage is visible. Example fill color: Blue `(79, 129, 189, 255)`.
    - **Data Label**: A clear text box displaying the numerical percentage, typically placed next to the icon.

*   **Step B: Compositional Style**
    - **Layering**: The effect is achieved by perfectly superimposing the clipped "Fill Layer" on top of the complete "Background Layer".
    - **Alignment**: Central alignment (both horizontal and vertical) is critical. The two layers must share the same coordinates and dimensions.
    - **Fill Logic**: The fill is always vertical, rising from the bottom. A value of 75% means the bottom 75% of the icon is filled with the accent color, while the top 25% reveals the gray background icon underneath.

*   **Step C: Dynamic Effects & Transitions**
    - The tutorial shows two methods. The first, using charts, allows for dynamic data updates within PowerPoint. The second, using shape merging, is static.
    - Our code-based reproduction creates a static, finalized image. However, the *visual effect* of filling can be simulated on the slide by applying a "Wipe" animation (Direction: "From Bottom") to the generated image in PowerPoint.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Creating the partial fill effect | **PIL/Pillow** | `python-pptx` has no native functions for partial image clipping or layering with alpha transparency. The tutorial's "Merge Shapes" method is a boolean operation best replicated by creating a composite image with an alpha mask. PIL provides precise, pixel-level control to generate the final visual as a single, clean PNG. |
| Re-coloring the base icon | PIL/Pillow | PIL can efficiently take a single-color source icon and programmatically re-color it to create both the background and fill versions, making the function highly reusable. |
| Layout and text placement | **python-pptx native** | Placing the generated images and their corresponding text labels on the slide is a straightforward task perfectly suited for the standard `python-pptx` API. |

> **Feasibility Assessment**: **95%**. The code perfectly reproduces the final static visual appearance of the pictogram fill effect. The small gap is that it produces a non-editable image rather than a dynamic, data-linked PowerPoint chart (as shown in the tutorial's first method). The chart-based method is exceedingly complex and brittle to automate via code and is not reliably supported across PowerPoint versions. For the purpose of generating a visually identical slide, this PIL-based approach is superior in reliability and quality.

#### 3b. Complete Reproduction Code

This code provides a helper function to generate a single filled icon and a main function to create a slide with three pictograms, as seen in the tutorial's title card.

```python
import io
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageOps, ImageDraw

def create_filled_icon_image(
    icon_data: bytes,
    percentage: float,
    size: tuple = (300, 300),
    bg_color: tuple = (217, 217, 217),
    fill_color: tuple = (79, 129, 189)
) -> io.BytesIO:
    """
    Creates a partially filled icon image using PIL.

    Args:
        icon_data: The byte data of the source icon (PNG with transparency).
        percentage: The fill percentage (0.0 to 1.0).
        size: The output size of the icon.
        bg_color: RGB tuple for the background (100% total) part of the icon.
        fill_color: RGB tuple for the filled part of the icon.

    Returns:
        A BytesIO object containing the generated PNG image.
    """
    # 1. Load the base icon and ensure it has an alpha channel
    icon = Image.open(io.BytesIO(icon_data)).convert("RGBA").resize(size, Image.LANCZOS)
    
    # 2. Create the background (gray) version
    bg_icon = Image.new("RGBA", icon.size, bg_color)
    bg_icon.putalpha(icon.getchannel('A'))

    # 3. Create the fill (colored) version
    fill_icon_layer = Image.new("RGBA", icon.size, fill_color)
    fill_icon_layer.putalpha(icon.getchannel('A'))

    # 4. Calculate the crop height based on the percentage
    # We want to keep the bottom part of the image, so we calculate the top cutoff point
    height = icon.size[1]
    cutoff_y = int(height * (1 - percentage))

    # 5. Create a mask to clip the top portion of the fill icon
    mask = Image.new("L", icon.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle([(0, cutoff_y), (icon.size[0], height)], fill=255)

    # 6. Composite the final image
    # Start with the background icon, then paste the masked fill icon on top
    final_image = bg_icon.copy()
    final_image.paste(fill_icon_layer, (0, 0), mask)

    # 7. Save to a byte buffer
    img_buffer = io.BytesIO()
    final_image.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    return img_buffer

def create_slide(
    output_pptx_path: str,
    title_text: str = "Image Percentage Fill Chart",
    data: list = None,
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with Pictogram Percentage Fill charts.

    Returns: path to the saved PPTX file.
    """
    if data is None:
        data = [
            {"label": "Metric A", "value": 0.80, "color": (247, 150, 70)},
            {"label": "Metric B", "value": 0.65, "color": (79, 129, 189)},
            {"label": "Metric C", "value": 0.52, "color": (155, 187, 89)},
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Set a light gray background for contrast
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(240, 240, 240)

    # Add a title
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12.33), Inches(1))
    title_tf = title_shape.text_frame
    title_tf.text = title_text
    p = title_tf.paragraphs[0]
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(89, 89, 89)
    p.alignment = PP_ALIGN.CENTER
    
    # Download a default icon (human silhouette)
    try:
        icon_url = "https://www.flaticon.com/download/icon/3135715?format=png&size=512"
        # Flaticon requires a proper User-Agent header
        req = urllib.request.Request(icon_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            icon_data = response.read()
    except Exception as e:
        print(f"Failed to download icon, using a placeholder. Error: {e}")
        # Create a simple circle as a fallback
        img = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((10, 10, 502, 502), fill=(128, 128, 128, 255))
        fallback_buffer = io.BytesIO()
        img.save(fallback_buffer, format='PNG')
        fallback_buffer.seek(0)
        icon_data = fallback_buffer.read()

    # --- Create and place pictograms ---
    total_items = len(data)
    total_width = Inches(12)
    item_width = total_width / total_items
    start_left = (prs.slide_width - total_width) / 2
    
    for i, item in enumerate(data):
        # Generate the filled icon image
        filled_icon_buffer = create_filled_icon_image(
            icon_data=icon_data,
            percentage=item["value"],
            fill_color=item["color"],
            bg_color=(220, 220, 220)
        )
        
        # Add the image to the slide
        icon_size = Inches(2.5)
        left_pos = start_left + (i * item_width) + (item_width - icon_size) / 2
        top_pos = Inches(2.5)
        slide.shapes.add_picture(filled_icon_buffer, left_pos, top_pos, height=icon_size)

        # Add the percentage label
        label_box = slide.shapes.add_textbox(left_pos, top_pos + icon_size + Inches(0.2), icon_size, Inches(0.5))
        label_tf = label_box.text_frame
        label_tf.text = f'{item["value"]:.0%}'
        p_label = label_tf.paragraphs[0]
        p_label.font.size = Pt(32)
        p_label.font.bold = True
        p_label.font.color.rgb = RGBColor.from_string("595959")
        p_label.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx_path)
    return output_pptx_path
```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback to a gray circle)?
- [x] Are all color values explicit RGB tuples?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes, for the final visual result).