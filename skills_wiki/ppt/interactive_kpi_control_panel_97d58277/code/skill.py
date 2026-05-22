import io
import numpy as np
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_slide(
    output_pptx_path: str,
    main_sections: dict = None,
    source_text: str = "Source: NextGenTemplates.Com",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide reproducing the 'Interactive KPI Control Panel' visual effect.

    This function generates the main navigation slide of a dashboard-style presentation,
    featuring clean, button-like links to different sections.

    Returns:
        str: The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    # Generate a subtle textured background with PIL for a professional, non-stark look.
    width, height = int(prs.slide_width * 96), int(prs.slide_height * 96) # Use 96 DPI for conversion
    base_color = (235, 239, 248)
    
    # Create a noise texture
    noise = np.random.randint(0, 15, (height, width), dtype=np.uint8)
    noise_image = Image.fromarray(noise, 'L').convert('RGB')

    # Create the base color image
    background_img = Image.new('RGB', (width, height), base_color)
    
    # Blend the noise with the base color. The alpha makes the noise very subtle.
    final_bg = Image.blend(background_img, noise_image, alpha=0.05)

    img_stream = io.BytesIO()
    final_bg.save(img_stream, format='PNG')
    img_stream.seek(0)
    slide.background.fill.picture(img_stream)

    # === Layer 2 & 3: Content and Navigation Panels ===

    if main_sections is None:
        main_sections = {
            "Dashboard": {
                "color": RGBColor(68, 114, 196),
                "buttons": ["Dashboard", "KPI Trend"]
            },
            "Input sheets": {
                "color": RGBColor(112, 48, 160),
                "buttons": ["Actual", "Target", "Previous Year"]
            },
            "KPI": {
                "color": RGBColor(155, 194, 230),
                "buttons": ["Define"]
            }
        }

    # Common styling parameters for a consistent look
    container_width = Inches(3.5)
    container_height = Inches(4)
    total_width = container_width * 3 + Inches(0.5) * 2
    start_left = (prs.slide_width - total_width) / 2
    start_top = (prs.slide_height - container_height) / 2

    panel_border_color = RGBColor(191, 184, 222)
    panel_fill_color = RGBColor(255, 255, 255)
    header_font_size = Pt(18)
    button_font_size = Pt(16)
    
    current_left = start_left
    
    # Create the three main panels in a loop
    for i, (section_title, details) in enumerate(main_sections.items()):
        # Main container card
        container = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, current_left, start_top, container_width, container_height
        )
        container.shadow.inherit = False
        fill = container.fill
        fill.solid()
        fill.fore_color.rgb = panel_fill_color
        line = container.line
        line.color.rgb = panel_border_color
        line.width = Pt(1.5)

        # Section header
        header_tb = slide.shapes.add_textbox(
            current_left, start_top + Inches(0.2), container_width, Inches(0.5)
        )
        p = header_tb.text_frame.paragraphs[0]
        p.text = section_title
        p.font.name = 'Arial'
        p.font.size = header_font_size
        p.font.bold = True
        p.font.color.rgb = RGBColor(64, 64, 64)
        p.alignment = 1  # PP_ALIGN.CENTER

        # Add buttons within the container
        button_height = Inches(0.6)
        button_width = container_width - Inches(0.8)
        button_left = current_left + Inches(0.4)
        button_start_top = start_top + Inches(1.0)
        
        for j, button_text in enumerate(details["buttons"]):
            button_top = button_start_top + j * (button_height + Inches(0.2))
            button_shape = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, button_left, button_top, button_width, button_height
            )
            button_shape.adjustments[0] = 0.3  # Adjust corner roundness for a softer look
            button_shape.shadow.inherit = False
            
            button_fill = button_shape.fill
            button_fill.solid()
            button_fill.fore_color.rgb = details["color"]
            button_shape.line.fill.background() # No line for a flatter, modern design
            
            text_frame = button_shape.text_frame
            text_frame.margin_bottom = 0
            text_frame.margin_top = 0
            p_button = text_frame.paragraphs[0]
            p_button.text = button_text
            p_button.font.name = 'Arial'
            p_button.font.size = button_font_size
            p_button.font.color.rgb = RGBColor(255, 255, 255)
            p_button.alignment = 1 # PP_ALIGN.CENTER
            text_frame.vertical_anchor = 3 # MSO_ANCHOR.MIDDLE

            # Add a placeholder hyperlink to demonstrate the intended interactivity.
            # To link to another slide, you would first create the slide, then use its .slide_id.
            if i == 0 and j == 0:
                hlink = p_button.runs[0].hyperlink
                hlink.address = "https://www.nextgentemplates.com" # Example external link
        
        current_left += container_width + Inches(0.5)
        
    # Add the source text at the bottom right of the panel group
    source_tb = slide.shapes.add_textbox(
        start_left + total_width - Inches(3), start_top + container_height + Inches(0.2), Inches(3), Inches(0.3)
    )
    p_source = source_tb.text_frame.paragraphs[0]
    p_source.text = source_text
    p_source.font.name = 'Arial'
    p_source.font.size = Pt(11)
    p_source.font.color.rgb = RGBColor(100, 100, 100)
    p_source.alignment = 2 # PP_ALIGN.RIGHT

    prs.save(output_pptx_path)
    return output_pptx_path
