import urllib.request
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image

def create_slide(
    output_pptx_path: str,
    price_text: str = "$320.00",
    product_name: str = "eBook Sales Booster",
    body_text: str = "We pursue relationships based on transparency, persistence, mutual trust, and integrity with our employees, customers and other business partners.",
    features: list = None,
    cta_text: str = "Purchase Today!",
    image_keyword: str = "business",
    accent_color: tuple = (68, 84, 164),
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with the Asymmetric Hero CTA design.

    This layout features a strong full-height hero image on the right
    and a structured value proposition with a CTA on the left.

    Returns: path to the saved PPTX file.
    """
    if features is None:
        features = [
            "2,000+ Core Slides*",
            "Free Lifetime Support",
            "Free Lifetime Updates",
            "28,000+ Exclusive Icons",
            "1,500+ Exclusive Vectors",
        ]

    # --- Presentation Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 1280 pixels
    prs.slide_height = Inches(7.5)   # 720 pixels
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # --- Define Colors ---
    BG_COLOR = RGBColor(255, 255, 255)
    ACCENT_COLOR = RGBColor.from_rgb(*accent_color)
    TEXT_COLOR_DARK = RGBColor(30, 30, 30)
    TEXT_COLOR_LIGHT = RGBColor(89, 89, 89)
    TEXT_COLOR_WHITE = RGBColor(255, 255, 255)

    # --- Define Layout Proportions ---
    SLIDE_WIDTH_EMU = prs.slide_width
    SLIDE_HEIGHT_EMU = prs.slide_height
    TEXT_PANEL_WIDTH_IN = 5.5
    IMAGE_PANEL_WIDTH_IN = prs.slide_width.inches - TEXT_PANEL_WIDTH_IN
    
    # === Layer 1: Backgrounds ===
    
    # Left Panel (White Background)
    # We don't need to add a shape; the slide background is white by default.
    
    # Right Panel (Hero Image)
    try:
        # Download and process image
        url = f'https://source.unsplash.com/1200x1600/?{image_keyword}'
        with urllib.request.urlopen(url) as response:
            image_data = response.read()
        
        img = Image.open(BytesIO(image_data))

        # Resize and crop to fit the panel perfectly
        target_w_px = int(IMAGE_PANEL_WIDTH_IN * 96) # 96 DPI
        target_h_px = int(prs.slide_height.inches * 96)
        
        # Resize to match height, maintaining aspect ratio
        original_w, original_h = img.size
        aspect_ratio = original_w / original_h
        new_h = target_h_px
        new_w = int(new_h * aspect_ratio)
        img_resized = img.resize((new_w, new_h), Image.LANCZOS)
        
        # Center crop to target width
        left = (new_w - target_w_px) / 2
        top = 0
        right = left + target_w_px
        bottom = new_h
        img_cropped = img_resized.crop((left, top, right, bottom))

        image_stream = BytesIO()
        img_cropped.save(image_stream, format='PNG')
        image_stream.seek(0)
        
        slide.shapes.add_picture(image_stream, left=Inches(TEXT_PANEL_WIDTH_IN), top=Inches(0), 
                                width=Inches(IMAGE_PANEL_WIDTH_IN), height=prs.slide_height)
    except Exception as e:
        print(f"Could not download or process image. Using a fallback solid color. Error: {e}")
        fallback_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 
                                                left=Inches(TEXT_PANEL_WIDTH_IN), top=Inches(0), 
                                                width=Inches(IMAGE_PANEL_WIDTH_IN), height=prs.slide_height)
        fallback_shape.fill.solid()
        fallback_shape.fill.fore_color.rgb = RGBColor(40, 40, 40)
        fallback_shape.line.fill.background()

    # === Layer 2: Text & Content (Left Panel) ===
    left_margin = Inches(0.75)
    
    # Price
    price_box = slide.shapes.add_textbox(left_margin, Inches(1.0), Inches(4), Inches(0.8))
    p = price_box.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = price_text
    run.font.name = 'Calibri Light'
    run.font.size = Pt(44)
    run.font.bold = True
    run.font.color.rgb = ACCENT_COLOR

    # Product Name
    name_box = slide.shapes.add_textbox(left_margin, Inches(1.8), Inches(4), Inches(0.5))
    p = name_box.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = product_name
    run.font.name = 'Calibri'
    run.font.size = Pt(24)
    run.font.bold = True
    run.font.color.rgb = TEXT_COLOR_DARK

    # Body Text
    body_box = slide.shapes.add_textbox(left_margin, Inches(2.4), Inches(4.5), Inches(1))
    body_box.text_frame.word_wrap = True
    p = body_box.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = body_text
    run.font.name = 'Calibri'
    run.font.size = Pt(12)
    run.font.color.rgb = TEXT_COLOR_LIGHT
    
    # Feature List
    current_y = 3.6
    icon_size = 0.25
    for i, feature_text in enumerate(features):
        # Numbered Icon
        icon = slide.shapes.add_shape(MSO_SHAPE.OVAL, left_margin, Inches(current_y), Inches(icon_size), Inches(icon_size))
        icon.fill.solid()
        icon.fill.fore_color.rgb = ACCENT_COLOR
        icon.line.fill.background()
        icon.text_frame.text = str(i + 1)
        icon.text_frame.paragraphs[0].font.size = Pt(10)
        icon.text_frame.paragraphs[0].font.color.rgb = TEXT_COLOR_WHITE
        icon.text_frame.paragraphs[0].font.bold = True
        icon.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

        # Feature Text
        feature_box = slide.shapes.add_textbox(left_margin + Inches(0.4), Inches(current_y - 0.05), Inches(4), Inches(0.4))
        p = feature_box.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = feature_text
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        run.font.color.rgb = TEXT_COLOR_LIGHT
        current_y += 0.45
        
    # CTA Button
    cta_y_pos = current_y + 0.3
    cta_btn = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_margin, Inches(cta_y_pos), Inches(2.5), Inches(0.5))
    cta_btn.fill.solid()
    cta_btn.fill.fore_color.rgb = ACCENT_COLOR
    cta_btn.line.fill.background()
    cta_btn.text_frame.text = cta_text
    p = cta_btn.text_frame.paragraphs[0]
    p.font.name = 'Calibri'
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = TEXT_COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER
    
    prs.save(output_pptx_path)
    return output_pptx_path

