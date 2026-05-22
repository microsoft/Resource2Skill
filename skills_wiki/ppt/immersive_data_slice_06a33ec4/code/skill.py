import requests
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    data_percentage: int = 35,
    main_text: list = ["OF CAMPERS", "DON'T LIKE", "SMORES*"],
    footnote_text: str = "*According to me",
    image_keyword: str = "camping",
    accent_color_1: tuple = (1, 31, 75),  # Dark Navy
    accent_color_2: tuple = (255, 165, 0), # Orange
    bg_color: tuple = (79, 235, 227),  # Cyan
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with the "Immersive Data Slice" data visualization.

    Args:
        output_pptx_path: The path to save the generated PPTX file.
        data_percentage: The integer percentage to display (e.g., 35 for 35%).
        main_text: A list of strings for the main description.
        footnote_text: The small text for the footnote.
        image_keyword: Keyword to search for the background image on Pexels.
        accent_color_1: The primary dark color for the data slice and text.
        accent_color_2: The accent color for highlighting text.
        bg_color: The slide background color.

    Returns:
        The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # === Layer 2: Visual Effect (Image & Data Slice) ===
    
    # Download image from Pexels
    image_url = f"https://images.pexels.com/photos/2398220/pexels-photo-2398220.jpeg" # A nice camping at night photo
    image_path = None
    try:
        response = requests.get(image_url, stream=True, timeout=5)
        response.raise_for_status()
        image_bytes = BytesIO(response.content)
        image_path = image_bytes
    except requests.exceptions.RequestException:
        # Fallback: create a placeholder gradient image with Pillow
        img = Image.new('RGB', (800, 800), color=accent_color_1)
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, 800, 800], fill=(20, 40, 90))
        fallback_bytes = BytesIO()
        img.save(fallback_bytes, format='PNG')
        fallback_bytes.seek(0)
        image_path = fallback_bytes

    # Create the circular image container
    img_diameter = Inches(4.5)
    img_left = Inches(1.5)
    img_top = Inches(1.5)
    img_shape = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, img_left, img_top, img_diameter, img_diameter
    )
    img_shape.line.fill.background()
    
    if image_path:
        img_shape.fill.solid()
        img_shape.fill.picture(image_path)
    
    # Send image to back
    # In python-pptx, order of creation determines z-order.
    # To send to back, we'd need lxml. For this design, we can just create it first.
    # But since we need to send it behind the pie, let's use lxml.
    from lxml import etree
    
    # Get the XML elements for the shapes
    sp_tree = img_shape._sp.get_or_add_spTree()
    shapes = list(sp_tree.iterchildren())
    
    # Move the last added shape (our circle) to the beginning of the list
    sp_tree.insert(0, shapes[-1])


    # Create the data slice (pie shape)
    pie_diameter = Inches(4.5)
    pie_left = Inches(1.5)
    pie_top = Inches(1.5)
    pie = slide.shapes.add_shape(
        MSO_SHAPE.PIE, pie_left, pie_top, pie_diameter, pie_diameter
    )
    pie.line.fill.background()
    pie.fill.solid()
    pie.fill.fore_color.rgb = RGBColor(*accent_color_1)

    # Adjust the pie slice to represent the percentage
    # Angles are in 64,000ths of a degree. 0 is East.
    # We want to start at the top (-90 deg) and sweep clockwise.
    angle_start = -90 * 64000
    angle_sweep = int((data_percentage / 100) * 360 * 64000)
    pie.adjustments[0] = angle_start
    pie.adjustments[1] = angle_sweep

    # === Layer 3: Text & Content ===
    
    # Percentage Text
    tb_percent = slide.shapes.add_textbox(
        Inches(1.8), Inches(2.2), Inches(2), Inches(2)
    )
    p_percent = tb_percent.text_frame.paragraphs[0]
    run_percent = p_percent.add_run()
    run_percent.text = f"{data_percentage}%"
    font_percent = run_percent.font
    font_percent.name = 'Bebas Neue'
    font_percent.size = Pt(90)
    font_percent.bold = True
    font_percent.color.rgb = RGBColor(255, 255, 255)

    # Main Description Text
    current_top = Inches(2.3)
    for i, line in enumerate(main_text):
        is_highlighted = "SMORES" in line.upper()
        tb = slide.shapes.add_textbox(
            Inches(6.5), current_top, Inches(6), Inches(1)
        )
        p = tb.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = line
        font = run.font
        font.name = 'Bebas Neue'
        font.size = Pt(44)
        font.bold = True
        if is_highlighted:
            font.color.rgb = RGBColor(*accent_color_2)
        else:
            font.color.rgb = RGBColor(*accent_color_1)
        current_top += Inches(0.8)

    # Footnote
    tb_footnote = slide.shapes.add_textbox(
        Inches(6.5), current_top + Inches(0.2), Inches(4), Inches(0.5)
    )
    p_footnote = tb_footnote.text_frame.paragraphs[0]
    run_footnote = p_footnote.add_run()
    run_footnote.text = footnote_text
    font_footnote = run_footnote.font
    font_footnote.name = 'Arial'
    font_footnote.size = Pt(12)
    font_footnote.color.rgb = RGBColor(*accent_color_1)

    prs.save(output_pptx_path)
    return output_pptx_path

