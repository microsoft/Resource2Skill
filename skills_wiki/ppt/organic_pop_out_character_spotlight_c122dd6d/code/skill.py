import io
import requests
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR
from PIL import Image, ImageDraw, ImageFilter, ImageOps

def create_slide(
    output_pptx_path: str,
    name: str = "李玉婷",
    credential: str = "MBA",
    details_bullets: list = None,
    details_paragraph: str = "拥有丰富的商业经验和管理能力。在公司的发展过程中，始终坚持以客户为中心的理念，不断推动公司的产品和服务创新和升级。",
    secondary_paragraph: str = "积极参与公司的社会责任活动，为社会做出了积极的贡献。喜欢旅行、阅读和健身，保持身体健康和积极的生活态度。",
    photo_url: str = "https://i.imgur.com/vNSgHnL.png", # URL to a portrait with transparent background
    accent_color_rgb: tuple = (255, 192, 0),
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with the "Organic Pop-out Character Spotlight" effect.

    Args:
        output_pptx_path: Path to save the generated PPTX file.
        name: The main name of the person.
        credential: A short credential (e.g., MBA, PhD).
        details_bullets: A list of strings for the bullet points.
        details_paragraph: The main descriptive paragraph.
        secondary_paragraph: The second descriptive paragraph.
        photo_url: URL of the character's portrait with a transparent background.
        accent_color_rgb: The main accent color for the blob and tags.

    Returns:
        The path to the saved PPTX file.
    """
    
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Default bullet points if none provided
    if details_bullets is None:
        details_bullets = [
            "知名企业的高管",
            "毕业于北京大学经济学专业",
            "在国际投资银行工作多年",
            "2010年成为商务经理",
        ]

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 248, 227)

    # === Layer 2: Decorative Blurred Circles ===
    def create_blurred_circle(diameter, color, blur_radius):
        size = int(diameter * 1.5)
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Calculate ellipse position to center it
        ellipse_bbox = [
            (size - diameter) / 2, (size - diameter) / 2,
            (size + diameter) / 2, (size + diameter) / 2
        ]
        draw.ellipse(ellipse_bbox, fill=color)
        blurred_img = img.filter(ImageFilter.GaussianBlur(blur_radius))
        
        # Crop the blurred image to reduce extra transparent space
        return blurred_img.crop(blurred_img.getbbox())

    blur_color = (*accent_color_rgb, 50)  # Add alpha for transparency
    
    # Create and place circles
    circle1_img = create_blurred_circle(Inches(2).pixels, blur_color, 40)
    circle2_img = create_blurred_circle(Inches(1.5).pixels, blur_color, 30)

    with io.BytesIO() as output:
        circle1_img.save(output, format="PNG")
        slide.shapes.add_picture(io.BytesIO(output.getvalue()), Inches(-0.5), Inches(-0.5), height=Inches(3))
    
    with io.BytesIO() as output:
        circle2_img.save(output, format="PNG")
        slide.shapes.add_picture(io.BytesIO(output.getvalue()), Inches(3), Inches(-0.8), height=Inches(2.5))
    
    # === Layer 3: Character Pop-out Effect ===
    # Define the organic blob shape as a polygon
    # Vertices are in percentage of the final shape's bounding box
    blob_poly_norm = [
        (0.48, 0.02), (0.75, 0.04), (0.94, 0.22), (0.98, 0.45), (0.92, 0.70),
        (0.75, 0.90), (0.50, 0.98), (0.25, 0.95), (0.08, 0.80), (0.01, 0.55),
        (0.06, 0.30), (0.25, 0.10)
    ]

    # Define bounding box for the blob on the slide
    blob_left, blob_top = Inches(7.5), Inches(1)
    blob_width, blob_height = Inches(7), Inches(7)

    # Add the colored blob shape using FreeformBuilder
    shape = slide.shapes.add_shape(MSO_SHAPE.FREEFORM, blob_left, blob_top, blob_width, blob_height)
    fill = shape.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*accent_color_rgb)
    shape.line.fill.background() # No outline

    # Download character photo
    try:
        response = requests.get(photo_url)
        response.raise_for_status()
        char_img_file = io.BytesIO(response.content)
        char_img = Image.open(char_img_file).convert("RGBA")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image: {e}")
        # Create a placeholder if download fails
        char_img = Image.new('RGBA', (500, 750), (100, 100, 100, 255))
        draw = ImageDraw.Draw(char_img)
        draw.text((100, 300), "Image Failed to Load", fill=(255,255,255))
        
    # Position and scale character image
    char_aspect_ratio = char_img.width / char_img.height
    char_height = Inches(8)
    char_width = char_height * char_aspect_ratio
    char_left = Inches(8.5)
    char_top = Inches(0.5)

    # Add the full character image and send it to back (will be cropped later)
    pic_full = slide.shapes.add_picture(io.BytesIO(response.content), char_left, char_top, height=char_height)

    # Add the blob shape again (it will be on top of the image)
    blob_shape = slide.shapes.add_freeform_builder(
        blob_left, blob_top, blob_width, blob_height
    )
    blob_shape.add_closed_path([ (x * blob_width, y * blob_height) for x, y in blob_poly_norm ])
    shape_obj = blob_shape.convert_to_shape()
    shape_obj.fill.solid()
    shape_obj.fill.fore_color.rgb = RGBColor(*accent_color_rgb)
    shape_obj.line.fill.background()

    # Crop the top-most full image to create the "pop-out"
    # The crop reveals the person's head and shoulders
    crop_amount = 0.55  # Crop 55% from the bottom
    pic_full.crop_bottom = crop_amount

    # === Layer 4: Text Content ===
    # Name
    tx_name = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(5), Inches(1))
    p_name = tx_name.text_frame.paragraphs[0]
    p_name.text = name
    p_name.font.name = 'Helvetica Neue'
    p_name.font.size = Pt(44)
    p_name.font.bold = True
    p_name.font.color.rgb = RGBColor(51, 51, 51)
    tx_name.text_frame.margin_bottom = 0

    # Credential Tag
    tag_width = Inches(1.2)
    tag_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, tx_name.left + tx_name.width - Inches(0.5), tx_name.top + Inches(0.2), tag_width, Inches(0.5))
    tag_shape.fill.solid()
    tag_shape.fill.fore_color.rgb = RGBColor(*accent_color_rgb)
    tag_shape.line.fill.background()
    tag_shape.text_frame.text = credential
    p_tag = tag_shape.text_frame.paragraphs[0]
    p_tag.font.name = 'Helvetica Neue'
    p_tag.font.bold = True
    p_tag.font.size = Pt(16)
    p_tag.font.color.rgb = RGBColor(255, 255, 255)
    
    # Bullet Points
    tx_bullets = slide.shapes.add_textbox(Inches(1), Inches(2.2), Inches(6), Inches(2))
    tf_bullets = tx_bullets.text_frame
    tf_bullets.clear()
    for item in details_bullets:
        p = tf_bullets.add_paragraph()
        p.text = item
        p.font.name = 'Helvetica Neue'
        p.font.size = Pt(16)
        p.font.color.rgb = RGBColor(89, 89, 89)
        p.level = 0

    # Paragraphs
    tx_para1 = slide.shapes.add_textbox(Inches(1), Inches(4.5), Inches(6), Inches(2))
    tx_para1.text_frame.text = details_paragraph
    p1 = tx_para1.text_frame.paragraphs[0]
    p1.font.name = 'Helvetica Neue'
    p1.font.size = Pt(16)
    p1.font.color.rgb = RGBColor(89, 89, 89)
    
    tx_para2 = slide.shapes.add_textbox(Inches(1), Inches(6), Inches(6), Inches(2))
    tx_para2.text_frame.text = secondary_paragraph
    p2 = tx_para2.text_frame.paragraphs[0]
    p2.font.name = 'Helvetica Neue'
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(89, 89, 89)
    
    # Bottom right label
    tx_label = slide.shapes.add_textbox(Inches(12.5), Inches(8), Inches(3), Inches(0.5))
    p_label = tx_label.text_frame.paragraphs[0]
    p_label.text = "CHARACTER\nINTRODUCTION"
    p_label.font.name = 'Helvetica Neue'
    p_label.font.size = Pt(10)
    p_label.font.bold = True
    p_label.font.color.rgb = RGBColor(180, 180, 180)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_slide("character_spotlight.pptx")

