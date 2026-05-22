import os
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml
from PIL import Image, ImageDraw, ImageFont

def create_slide(
    output_pptx_path: str,
    title_text: str = "World is happening what\nView the latest news and breaking news today.",
    tag_text: str = "LIVE",
    image_keywords: list = ["protest", "news", "city"], 
    **kwargs,
) -> str:
    """
    Creates a PPTX reproducing the 'Cinematic Interleaved Stack' (Dip-to-Black Carousel).
    Generates the exact Z-order stack of images and black overlays required for the effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Helper: Generate fallback images using PIL if download fails
    def create_fallback_image(text, filename):
        img = Image.new('RGB', (1920, 1080), color=(40, 40, 50))
        d = ImageDraw.Draw(img)
        # Draw a simple grid pattern to simulate an image
        for i in range(0, 1920, 100):
            d.line([(i, 0), (i, 1080)], fill=(60, 60, 70), width=2)
        for i in range(0, 1080, 100):
            d.line([(0, i), (1920, i)], fill=(60, 60, 70), width=2)
        # Add big text
        d.text((800, 500), f"Fallback: {text}", fill=(255, 255, 255))
        img.save(filename)
        return filename

    # === Layer 1: Construct the Interleaved Stack ===
    # Z-Order logic requires inserting from bottom-most to top-most.
    # Bottom layer is the last image in our sequence.
    # Sequence bottom-to-top: Img3 -> Rect -> Img2 -> Rect -> Img1
    
    images_to_stack = image_keywords[::-1] # Reverse for bottom-up insertion
    
    for i, keyword in enumerate(images_to_stack):
        img_filename = f"temp_stack_img_{i}.jpg"
        try:
            url = f"https://source.unsplash.com/1920x1080/?{keyword}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response, open(img_filename, 'wb') as out_file:
                out_file.write(response.read())
        except Exception:
            create_fallback_image(keyword, img_filename)

        # 1. Insert Image
        slide.shapes.add_picture(img_filename, 0, 0, width=prs.slide_width, height=prs.slide_height)
        
        # Clean up temp file
        if os.path.exists(img_filename):
            os.remove(img_filename)

        # 2. Insert Black Overlay Rectangle (Do not insert on top of the very last inserted image)
        if i < len(images_to_stack) - 1:
            black_rect = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
            )
            black_rect.fill.solid()
            black_rect.fill.fore_color.rgb = RGBColor(0, 0, 0)
            black_rect.line.fill.background() # No outline

    # === Layer 2: Static Foreground Text & UI ===
    # Because these are added last, they sit on top of the entire stack.
    
    # Red Accent Tag (like CNN logo in the video)
    tag_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1), Inches(5.2), Inches(1), Inches(0.5))
    tag_box.fill.solid()
    tag_box.fill.fore_color.rgb = RGBColor(204, 0, 0) # Dark Red
    tag_box.line.fill.background()
    tag_tf = tag_box.text_frame
    tag_tf.text = tag_text
    tag_tf.paragraphs[0].font.name = "Arial"
    tag_tf.paragraphs[0].font.size = Pt(16)
    tag_tf.paragraphs[0].font.bold = True
    tag_tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

    # Main Headline Text Box
    text_box = slide.shapes.add_textbox(Inches(0.8), Inches(5.8), Inches(8), Inches(1.5))
    text_frame = text_box.text_frame
    text_frame.word_wrap = True
    p = text_frame.add_paragraph()
    p.text = title_text
    p.font.name = "Arial"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    # Inject LXML Drop Shadow for cinematic readability on top of any image
    shadow_xml = """
    <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:outerShdw blurRad="50800" dist="38100" dir="2700000" algn="tl" rotWithShape="0">
            <a:srgbClr val="000000">
                <a:alpha val="60000"/>
            </a:srgbClr>
        </a:outerShdw>
    </a:effectLst>
    """
    # Apply shadow to the text box shape properties
    spPr = text_box.element.find('.//p:spPr', namespaces=text_box.element.nsmap)
    if spPr is not None:
        effectLst = parse_xml(shadow_xml)
        spPr.append(effectLst)

    prs.save(output_pptx_path)
    return output_pptx_path
