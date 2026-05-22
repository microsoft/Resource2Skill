import os
from io import BytesIO
import urllib.request
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def create_slide(
    output_pptx_path: str,
    person_name: str = "Satomi Ishihara",
    person_title: str = "Actress / Presenter",
    body_text: str = "Award-winning actress recognized for leading roles in top television dramas.\n\nKnown for exceptional range, expressive performances, and significant contributions to the modern entertainment industry.",
    bg_color: tuple = (215, 232, 245),  # Soft blue matching the tutorial's example
    accent_color: tuple = (50, 80, 120),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Seamless Gradient Image Blending" visual effect.
    """
    prs = Presentation()
    # Set 16:9 aspect ratio
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    slide_layout = prs.slide_layouts[6] # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # === Layer 0: Slide Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(bg_color[0], bg_color[1], bg_color[2])

    # === Layer 1: Download/Create Source Portrait Image ===
    # Using a generic portrait photo from Unsplash
    img_url = "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=800&auto=format&fit=crop"
    img_stream = BytesIO()
    
    try:
        req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img_stream.write(response.read())
    except Exception as e:
        print(f"Failed to download image: {e}. Generating fallback image.")
        # Fallback: Create a solid block to represent the photo
        fallback_img = Image.new('RGB', (600, 720), color=(180, 200, 220))
        d = ImageDraw.Draw(fallback_img)
        d.text((200, 350), "Portrait Image", fill=(100, 100, 100))
        fallback_img.save(img_stream, format='PNG')
        
    img_stream.seek(0)
    
    # Place the image on the left side, stretching to slide height
    # Original image might not be exactly 16:9, we set height and let width auto-scale
    slide.shapes.add_picture(img_stream, Inches(0), Inches(0), height=Inches(7.5))

    # === Layer 2: The Core Skill - PIL Gradient Alpha Mask ===
    # We create a gradient that goes from fully transparent (Left) to solid bg_color (Right)
    # This will sit over the right edge of the photo to blend it into the background.
    
    grad_width = 800  # High res for smooth transition
    grad_height = 100
    
    # Create a 1D gradient (width x 1) then resize
    base_grad = Image.new('RGBA', (grad_width, 1))
    draw = ImageDraw.Draw(base_grad)
    
    for x in range(grad_width):
        # Calculate alpha: 0 at x=0 (transparent), 255 at x=grad_width (opaque)
        # We use an ease-in-out or linear mapping. Linear is fine here.
        alpha = int((x / grad_width) * 255)
        draw.line((x, 0, x, 0), fill=(bg_color[0], bg_color[1], bg_color[2], alpha))
        
    # Resize to full block size
    gradient_img = base_grad.resize((grad_width, 2000))
    
    grad_stream = BytesIO()
    gradient_img.save(grad_stream, format='PNG')
    grad_stream.seek(0)
    
    # Place the gradient mask overlapping the seam.
    # Assuming the photo takes up roughly 4.5 inches of width.
    # We start the gradient around 2.5 inches from the left, making it 4 inches wide.
    slide.shapes.add_picture(
        grad_stream, 
        left=Inches(2.5), 
        top=Inches(0), 
        width=Inches(4.5), 
        height=Inches(7.5)
    )

    # === Layer 3: Typography & Content ===
    # Add text on the right side (where the background is solid)
    
    # 1. Name
    name_box = slide.shapes.add_textbox(Inches(7.5), Inches(1.5), Inches(5), Inches(1))
    name_frame = name_box.text_frame
    name_frame.word_wrap = True
    p_name = name_frame.paragraphs[0]
    p_name.text = person_name
    p_name.font.size = Pt(44)
    p_name.font.bold = True
    p_name.font.color.rgb = RGBColor(30, 30, 30)

    # 2. Title / Subtitle
    title_box = slide.shapes.add_textbox(Inches(7.5), Inches(2.2), Inches(5), Inches(0.5))
    title_frame = title_box.text_frame
    p_title = title_frame.paragraphs[0]
    p_title.text = person_title
    p_title.font.size = Pt(18)
    p_title.font.color.rgb = RGBColor(accent_color[0], accent_color[1], accent_color[2])
    
    # Decorative line under title
    line = slide.shapes.add_shape(
        1, # msoShapeRectangle
        Inches(7.5), Inches(2.8), Inches(0.5), Inches(0.05)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(accent_color[0], accent_color[1], accent_color[2])
    line.line.fill.background() # No border

    # 3. Bio / Body Text
    body_box = slide.shapes.add_textbox(Inches(7.5), Inches(3.2), Inches(5), Inches(3))
    body_frame = body_box.text_frame
    body_frame.word_wrap = True
    p_body = body_frame.paragraphs[0]
    p_body.text = body_text
    p_body.font.size = Pt(14)
    p_body.font.color.rgb = RGBColor(80, 80, 80)
    p_body.line_spacing = 1.5

    # 4. Large Background Decorative Text (Optional touch from tutorial)
    deco_box = slide.shapes.add_textbox(Inches(6.0), Inches(0.5), Inches(7), Inches(2))
    deco_frame = deco_box.text_frame
    p_deco = deco_frame.paragraphs[0]
    p_deco.text = person_name.split()[-1].upper() # Last name
    p_deco.font.size = Pt(120)
    p_deco.font.bold = True
    # Very faint text
    p_deco.font.color.rgb = RGBColor(255, 255, 255)
    # Send to back essentially by relying on draw order (it's drawn last, so we'd need to reorder in actual XML, 
    # but using a color slightly lighter than BG achieves the same watermark effect)
    p_deco.font.color.rgb = RGBColor(
        min(bg_color[0]+20, 255), 
        min(bg_color[1]+20, 255), 
        min(bg_color[2]+20, 255)
    )
    
    # Save the presentation
    prs.save(output_pptx_path)
    return output_pptx_path
