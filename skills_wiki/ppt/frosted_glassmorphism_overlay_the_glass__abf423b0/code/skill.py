import os
import urllib.request
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from PIL import Image, ImageDraw, ImageFilter

def create_fallback_background(width=1920, height=1080):
    """Generates a vibrant abstract background if image download fails."""
    bg = Image.new('RGB', (width, height), (13, 17, 28))
    draw = ImageDraw.Draw(bg)
    # Draw vibrant blurred orbs to make the glass effect visible
    draw.ellipse((-200, -200, 800, 800), fill=(138, 43, 226))   # Purple
    draw.ellipse((1200, 400, 2200, 1400), fill=(0, 191, 255))   # Cyan
    draw.ellipse((600, 800, 1400, 1600), fill=(255, 105, 180))  # Pink
    return bg.filter(ImageFilter.GaussianBlur(radius=150))

def create_slide(
    output_pptx_path: str,
    title_text: str = "The Stunning\nGlass Effect",
    body_text: str = "This dynamic, professional look is what we're aiming for. It subdues the background while maintaining context.",
    bg_keyword: str = "abstract,gradient,fluid",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Glassmorphism Reveal Pane effect.
    """
    # 1. Setup Presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.3333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    DPI = 144
    WIDTH_PX = int(13.3333 * DPI) # ~1920
    HEIGHT_PX = int(7.5 * DPI)    # ~1080

    # 2. Fetch or Generate Background
    img_url = f"https://source.unsplash.com/featured/{WIDTH_PX}x{HEIGHT_PX}?{bg_keyword}"
    try:
        req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            bg_image = Image.open(BytesIO(response.read())).convert('RGB')
            bg_image = bg_image.resize((WIDTH_PX, HEIGHT_PX), Image.Resampling.LANCZOS)
    except Exception as e:
        print(f"Could not download image: {e}. Using generated fallback.")
        bg_image = create_fallback_background(WIDTH_PX, HEIGHT_PX)

    bg_path = "temp_bg.jpg"
    bg_image.save(bg_path, format="JPEG", quality=90)

    # 3. Create the Glass Pane using PIL (The Core Technique)
    # Define the coordinates for the glass pane (Center-Right alignment)
    pane_left, pane_top = int(WIDTH_PX * 0.35), int(HEIGHT_PX * 0.15)
    pane_right, pane_bottom = int(WIDTH_PX * 0.90), int(HEIGHT_PX * 0.85)
    pane_width = pane_right - pane_left
    pane_height = pane_bottom - pane_top

    # Step A: Crop the exact background area
    pane = bg_image.crop((pane_left, pane_top, pane_right, pane_bottom))
    
    # Step B: Apply heavy Gaussian blur
    pane = pane.filter(ImageFilter.GaussianBlur(radius=30))
    pane = pane.convert('RGBA')

    # Step C: Brighten/Milk it with a semi-transparent white overlay
    overlay = Image.new('RGBA', pane.size, (255, 255, 255, 45)) # 45/255 alpha
    pane = Image.alpha_composite(pane, overlay)

    # Step D: Apply rounded rectangle mask (Crop to Shape)
    corner_radius = 40
    mask = Image.new('L', pane.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle((0, 0, pane_width, pane_height), radius=corner_radius, fill=255)
    pane.putalpha(mask)

    # Step E: Add subtle glass edge reflection (1px white inner border)
    draw_border = ImageDraw.Draw(pane)
    draw_border.rounded_rectangle(
        (1, 1, pane_width-2, pane_height-2), 
        radius=corner_radius, 
        outline=(255, 255, 255, 120), 
        width=2
    )

    pane_path = "temp_pane.png"
    pane.save(pane_path, format="PNG")

    # 4. Assemble in PowerPoint
    # Add Background
    slide.shapes.add_picture(bg_path, 0, 0, width=Inches(13.3333), height=Inches(7.5))

    # Add Glass Pane exactly where it was cropped from
    slide.shapes.add_picture(
        pane_path, 
        Inches(pane_left / DPI), 
        Inches(pane_top / DPI), 
        width=Inches(pane_width / DPI), 
        height=Inches(pane_height / DPI)
    )

    # Add overlapping decorative element (mimics the bird/element in the tutorial creating depth)
    # We will use a native PPTX shape that overlaps the left edge of the glass
    overlap_shape = slide.shapes.add_shape(
        9, # msoShapeOval
        Inches((pane_left / DPI) - 0.8), # Straddling the edge
        Inches((pane_top / DPI) + 1.0),
        Inches(1.6), Inches(1.6)
    )
    overlap_shape.fill.solid()
    overlap_shape.fill.fore_color.rgb = RGBColor(255, 215, 0) # Gold
    overlap_shape.line.color.rgb = RGBColor(255, 255, 255)
    overlap_shape.line.width = Pt(3)

    # 5. Add Typography
    # Title
    txBox = slide.shapes.add_textbox(
        Inches((pane_left / DPI) + 0.5), 
        Inches((pane_top / DPI) + 0.5), 
        Inches((pane_width / DPI) - 1.0), 
        Inches(2.0)
    )
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Georgia"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(10, 10, 10) # Dark text contrasts well with milky glass

    # Body Text
    txBox_body = slide.shapes.add_textbox(
        Inches((pane_left / DPI) + 0.5), 
        Inches((pane_top / DPI) + 2.5), 
        Inches((pane_width / DPI) - 1.0), 
        Inches(2.0)
    )
    tf_body = txBox_body.text_frame
    tf_body.word_wrap = True
    p_body = tf_body.paragraphs[0]
    p_body.text = body_text
    p_body.font.name = "Arial"
    p_body.font.size = Pt(20)
    p_body.font.color.rgb = RGBColor(40, 40, 40)

    # Save presentation
    prs.save(output_pptx_path)
    
    # Cleanup temp files
    if os.path.exists(bg_path): os.remove(bg_path)
    if os.path.exists(pane_path): os.remove(pane_path)

    return output_pptx_path
