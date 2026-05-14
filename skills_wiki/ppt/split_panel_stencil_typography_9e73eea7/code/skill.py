import os
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_slide(
    output_pptx_path: str,
    title_text: str = "STAY\nHUNGRY\nSTAY\nFOOL\nISH.",
    overlay_color: tuple = (255, 255, 255),
    ground_color: tuple = (30, 30, 30),
    **kwargs,
) -> str:
    """
    Creates a split-panel slide with an image on the left and a 3D stencil 
    typography cut-out effect on the right.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Dimensions for halves
    half_width_emu = int(prs.slide_width / 2)
    height_emu = int(prs.slide_height)

    # --- Step 1: Left Image Processing ---
    img_path = "temp_portrait.jpg"
    cropped_img_path = "temp_portrait_cropped.jpg"
    
    # Download a reliable grayscale portrait
    image_url = "https://picsum.photos/seed/steve/800/1200?grayscale"
    try:
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(img_path, 'wb') as f:
                f.write(response.read())
    except Exception:
        # Fallback to solid color if download fails
        fallback = Image.new('RGB', (800, 1200), (100, 100, 100))
        fallback.save(img_path)

    # Crop image to perfectly fit the left half aspect ratio
    with Image.open(img_path) as img:
        img_w, img_h = img.size
        aspect_img = img_w / img_h
        aspect_target = (13.333 / 2) / 7.5
        
        if aspect_img > aspect_target:
            # Image is too wide
            new_w = int(img_h * aspect_target)
            left = (img_w - new_w) // 2
            img_cropped = img.crop((left, 0, left + new_w, img_h))
        else:
            # Image is too tall
            new_h = int(img_w / aspect_target)
            top = (img_h - new_h) // 2
            img_cropped = img.crop((0, top, img_w, top + new_h))
            
        img_cropped.save(cropped_img_path)

    # Insert left image
    slide.shapes.add_picture(cropped_img_path, 0, 0, width=half_width_emu, height=height_emu)


    # --- Step 2: Right Panel PIL Stencil Generation ---
    panel_img_path = "temp_right_panel.png"
    
    # Canvas for right half (high-res for crisp text)
    pil_w, pil_h = 1280, 1440
    
    # Base ground layer (what we see through the holes)
    canvas = Image.new('RGBA', (pil_w, pil_h), ground_color + (255,))

    # Create the text mask (White = opaque, Black = transparent hole)
    mask = Image.new('L', (pil_w, pil_h), 255)
    draw = ImageDraw.Draw(mask)

    # Load an ultra-bold font
    font = None
    font_choices = ["impact.ttf", "arialbd.ttf", "Arial Bold.ttf", "Helvetica-Bold.ttf"]
    for font_name in font_choices:
        try:
            font = ImageFont.truetype(font_name, 230)
            break
        except IOError:
            continue
    if not font:
        font = ImageFont.load_default()

    # Draw stacked text into the mask as transparent (0)
    lines = title_text.split('\n')
    font_size = 230
    line_spacing = int(font_size * 0.90)  # Tight stacking
    total_text_height = len(lines) * line_spacing
    y_offset = (pil_h - total_text_height) // 2

    for line in lines:
        # X=80 pushes it close to the left boundary (touching the image)
        draw.text((80, y_offset), line, font=font, fill=0)
        y_offset += line_spacing

    # Create inner shadow
    # Blur the mask so the edges of the holes fade
    blurred_mask = mask.filter(ImageFilter.GaussianBlur(15))
    
    # Offset the blurred mask to push the shadow down and right
    shadow_alpha = Image.new('L', (pil_w, pil_h), 255)
    shadow_alpha.paste(blurred_mask, (20, 20))
    
    # Shadow layer is entirely black, with the offset blurred alpha
    shadow_layer = Image.new('RGBA', (pil_w, pil_h), (0, 0, 0, 255))
    shadow_layer.putalpha(shadow_alpha)

    # Overlay layer is the solid panel color, using the crisp mask
    overlay_layer = Image.new('RGBA', (pil_w, pil_h), overlay_color + (255,))
    overlay_layer.putalpha(mask)

    # Composite layers: Ground -> Shadow -> Stencil Overlay
    canvas = Image.alpha_composite(canvas, shadow_layer)
    canvas = Image.alpha_composite(canvas, overlay_layer)
    canvas.save(panel_img_path)

    # Insert right panel
    slide.shapes.add_picture(panel_img_path, half_width_emu, 0, width=half_width_emu, height=height_emu)


    # --- Step 3: Overlay Brand Text ---
    txBox = slide.shapes.add_textbox(Inches(9.5), Inches(6.5), Inches(3.5), Inches(0.8))
    tf = txBox.text_frame
    
    p = tf.add_paragraph()
    p.alignment = PP_ALIGN.RIGHT
    
    run1 = p.add_run()
    run1.text = "Made by\n"
    run1.font.italic = True
    run1.font.size = Pt(18)
    run1.font.color.rgb = RGBColor(120, 120, 120)

    run2 = p.add_run()
    run2.text = "SlideSkills"
    run2.font.bold = True
    run2.font.size = Pt(22)
    run2.font.color.rgb = RGBColor(235, 175, 45) # Signature gold/yellow

    # Cleanup temp files
    for temp_file in [img_path, cropped_img_path, panel_img_path]:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    prs.save(output_pptx_path)
    return output_pptx_path
