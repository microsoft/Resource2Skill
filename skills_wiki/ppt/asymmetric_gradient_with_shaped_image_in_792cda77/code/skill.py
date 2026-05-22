import io
import requests
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image, ImageDraw, ImageOps

def create_slide(
    output_pptx_path: str,
    title_text: str = "New Software\nDevelopment",
    company_name: str = "Your Company Name",
    image_keyword: str = "developer coding",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide reproducing the 'Asymmetric Gradient with Shaped Image Inset' style.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background Gradient (using PIL) ===
    width, height = prs.slide_width, prs.slide_height
    dark_green = (1, 105, 56)
    light_green = (142, 198, 63)

    gradient_img = Image.new("RGB", (int(width.emu / 9525), int(height.emu / 9525)), light_green)
    draw = ImageDraw.Draw(gradient_img)

    # Diagonal gradient
    for i in range(gradient_img.width):
        for j in range(gradient_img.height):
            ratio = (i + j) / (gradient_img.width + gradient_img.height)
            r = int(dark_green[0] * ratio + light_green[0] * (1 - ratio))
            g = int(dark_green[1] * ratio + light_green[1] * (1 - ratio))
            b = int(dark_green[2] * ratio + light_green[2] * (1 - ratio))
            draw.point((i, j), (r, g, b))

    img_bytes = io.BytesIO()
    gradient_img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    slide.shapes.add_picture(img_bytes, 0, 0, width=prs.slide_width, height=prs.slide_height)
    
    # === Layer 2: Thin Accent Bar ===
    left = Inches(0.2)
    top = Inches(0)
    width = Inches(0.05)
    height = prs.slide_height
    accent_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = RGBColor(240, 240, 240)
    accent_bar.line.fill.background()

    # === Layer 3: Shaped Image (using PIL) ===
    try:
        # Download image from Unsplash
        img_url = f"https://source.unsplash.com/800x1200/?{image_keyword.replace(' ', ',')}"
        response = requests.get(img_url, timeout=10)
        response.raise_for_status()
        source_img_bytes = io.BytesIO(response.content)
        
        # Open and process the image
        source_img = Image.open(source_img_bytes).convert("RGBA")
        
        # Desaturate
        bw_img = ImageOps.grayscale(source_img)
        
        # Create oval mask
        mask = Image.new('L', source_img.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, source_img.size[0], source_img.size[1]), fill=255)
        
        # Apply mask
        masked_img = Image.new('RGBA', source_img.size)
        masked_img.paste(bw_img, (0, 0), mask)
        
        # Save to bytes and add to slide
        final_img_bytes = io.BytesIO()
        masked_img.save(final_img_bytes, format='PNG')
        final_img_bytes.seek(0)
        
        img_height = Inches(6.5)
        img_aspect_ratio = masked_img.width / masked_img.height
        img_width = img_height * img_aspect_ratio
        
        slide.shapes.add_picture(
            final_img_bytes,
            left=Inches(0.4),
            top=Inches(0.5),
            height=img_height,
            width=img_width
        )
    except Exception as e:
        print(f"Warning: Could not download or process image. Skipping. Error: {e}")

    # === Layer 4: Text & Content ===
    # Main Title
    title_shape = slide.shapes.add_textbox(
        Inches(5.5), Inches(2.0), Inches(7), Inches(2.5)
    )
    title_tf = title_shape.text_frame
    title_tf.word_wrap = True
    p = title_tf.paragraphs[0]
    p.text = title_text
    p.font.name = 'Georgia'
    p.font.size = Pt(54)
    p.font.bold = False
    p.font.color.rgb = RGBColor(255, 255, 255)

    # Company Name "Button"
    btn_width = Inches(3.5)
    btn_height = Inches(0.6)
    btn_left = Inches(5.5)
    btn_top = Inches(4.8)

    # Background shape for the button
    company_bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, btn_left, btn_top, btn_width, btn_height)
    company_bg.fill.solid()
    company_bg.fill.fore_color.rgb = RGBColor(255, 255, 255)
    company_bg.line.fill.background()

    # Text for the button
    company_shape = slide.shapes.add_textbox(btn_left, btn_top, btn_width, btn_height)
    company_tf = company_shape.text_frame
    company_tf.margin_bottom = Inches(0)
    company_tf.margin_top = Inches(0)
    company_tf.vertical_anchor = 2 # Middle
    p_company = company_tf.paragraphs[0]
    p_company.text = company_name
    p_company.font.name = 'Calibri'
    p_company.font.size = Pt(16)
    p_company.font.color.rgb = RGBColor(80, 80, 80)
    p_company.alignment = 1 # Center

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# create_slide("New_Software_Development_Slide.pptx")

