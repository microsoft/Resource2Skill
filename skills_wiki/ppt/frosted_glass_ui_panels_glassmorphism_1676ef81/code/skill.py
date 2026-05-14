import io
import urllib.request
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

def create_slide(
    output_pptx_path: str,
    title_text: str = "Hello hmppt",
    body_text: str = "with custom layout animation and many more...",
    card1_title: str = "Build Records\nmore easily",
    card2_body: str = "Lately I really like to do this glass look.\nMatching modern UI look.",
    bg_keyword: str = "purple abstract gradient",
) -> str:
    """
    Creates a PPTX file reproducing the Frosted Glass UI Panels (Glassmorphism) effect,
    complete with a Morph transition.

    Args:
        output_pptx_path: The path to save the generated PPTX file.
        title_text: Text for the main title on the left panel.
        body_text: Body text for the left panel.
        card1_title: Title for the top-right card.
        card2_body: Body text for the bottom-right card.
        bg_keyword: A keyword to search for a background image on Unsplash.

    Returns:
        Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # --- Helper Function to Create Glass Panel ---
    def create_glass_panel(bg_image, x_in, y_in, w_in, h_in, corner_radius=30, blur_radius=60):
        # Convert inches to pixels (assuming 96 DPI for PowerPoint)
        dpi = 96
        x, y, w, h = int(x_in * dpi), int(y_in * dpi), int(w_in * dpi), int(h_in * dpi)

        # 1. Crop the section of the background
        panel_bg = bg_image.crop((x, y, x + w, y + h))

        # 2. Apply Gaussian Blur
        blurred_bg = panel_bg.filter(ImageFilter.GaussianBlur(radius=blur_radius))

        # 3. Increase Brightness
        enhancer = ImageEnhance.Brightness(blurred_bg)
        brightened_bg = enhancer.enhance(1.2)

        # 4. Create a rounded rectangle mask for the panel
        mask = Image.new('L', (w, h), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, w, h), radius=corner_radius, fill=255)

        # 5. Create a slightly larger, blurred mask for the glow
        glow_mask = Image.new('L', (w, h), 0)
        draw_glow = ImageDraw.Draw(glow_mask)
        draw_glow.rounded_rectangle((0, 0, w, h), radius=corner_radius, fill=100) # Semi-transparent glow
        glow_mask = glow_mask.filter(ImageFilter.GaussianBlur(radius=15))

        # 6. Composite the final panel
        final_panel = Image.new('RGBA', (w, h))
        final_panel.paste(brightened_bg, (0, 0), mask)
        
        # Create a white base for the glow
        glow_base = Image.new('RGBA', (w,h), (255, 255, 255, 255))
        
        # Composite glow, then panel on top
        final_image = Image.new('RGBA', (w, h))
        final_image.paste(glow_base, (0,0), glow_mask)
        final_image.paste(final_panel, (0,0), final_panel)

        img_byte_arr = io.BytesIO()
        final_image.save(img_byte_arr, format='PNG')
        return io.BytesIO(img_byte_arr.getvalue())

    # --- Background Image ---
    try:
        url = f"https://source.unsplash.com/1280x720/?{bg_keyword.replace(' ', '%20')}"
        with urllib.request.urlopen(url) as response:
            bg_image_data = response.read()
        bg_image = Image.open(io.BytesIO(bg_image_data)).convert("RGBA")
    except Exception:
        # Fallback to a generated gradient
        bg_image = Image.new('RGB', (1280, 720), (173, 216, 230))
        draw = ImageDraw.Draw(bg_image)
        for i in range(720):
            r = 135 - int(i / 720 * 50)
            g = 206 - int(i / 720 * 100)
            b = 250 - int(i / 720 * 100)
            draw.line([(0, i), (1280, i)], fill=(r, g, b))

    bg_image_stream = io.BytesIO()
    bg_image.save(bg_image_stream, format="PNG")
    bg_image_stream.seek(0)
    
    # --- Slide Creation Logic ---
    def add_content_to_slide(slide):
        # Add background
        slide.shapes.add_picture(io.BytesIO(bg_image_stream.getvalue()), 0, 0, width=prs.slide_width, height=prs.slide_height)
        
        # Create and add glass panels
        panel_1_stream = create_glass_panel(bg_image, 1.5, 1.2, 3.5, 5.1)
        panel1 = slide.shapes.add_picture(panel_1_stream, Inches(1.5), Inches(1.2), Inches(3.5), Inches(5.1))
        panel1.name = "Panel 1"
        
        panel_2_stream = create_glass_panel(bg_image, 5.5, 1.2, 6.5, 2.5)
        panel2 = slide.shapes.add_picture(panel_2_stream, Inches(5.5), Inches(1.2), Inches(6.5), Inches(2.5))
        panel2.name = "Panel 2"

        panel_3_stream = create_glass_panel(bg_image, 5.5, 4.0, 6.5, 2.3)
        panel3 = slide.shapes.add_picture(panel_3_stream, Inches(5.5), Inches(4.0), Inches(6.5), Inches(2.3))
        panel3.name = "Panel 3"
        
        # Add Text Elements
        # On Panel 1
        txBox = slide.shapes.add_textbox(Inches(1.8), Inches(3.2), Inches(3), Inches(1.5))
        txBox.name = "Title Text"
        p = txBox.text_frame.paragraphs[0]
        p.text = title_text
        p.font.name = 'Century Gothic'
        p.font.size = Pt(44)
        p.font.bold = True

        txBox2 = slide.shapes.add_textbox(Inches(1.8), Inches(4.5), Inches(3), Inches(0.5))
        txBox2.name = "Body Text"
        p2 = txBox2.text_frame.paragraphs[0]
        p2.text = body_text
        p2.font.name = 'Century Gothic'
        p2.font.size = Pt(12)
        
        # On Panel 2
        txBox3 = slide.shapes.add_textbox(Inches(5.8), Inches(1.8), Inches(6), Inches(1.5))
        txBox3.name = "Card 1 Title"
        p3 = txBox3.text_frame.paragraphs[0]
        p3.text = card1_title
        p3.font.name = 'Century Gothic'
        p3.font.size = Pt(28)
        p3.font.bold = True
        
        # On Panel 3
        txBox4 = slide.shapes.add_textbox(Inches(5.8), Inches(4.5), Inches(6), Inches(1.5))
        txBox4.name = "Card 2 Body"
        p4 = txBox4.text_frame.paragraphs[0]
        p4.text = card2_body
        p4.font.name = 'Century Gothic'
        p4.font.size = Pt(16)
        
    # SLIDE 1 (Start state for Morph)
    start_slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_content_to_slide(start_slide)
    # Move elements off-slide
    for shape in start_slide.shapes:
        shape.top += prs.slide_height # Move everything down off the slide

    # SLIDE 2 (End state for Morph)
    end_slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_content_to_slide(end_slide)

    # --- XML Injection for Morph Transition ---
    slide_xml = end_slide.part.blob
    root = etree.fromstring(slide_xml)
    
    # Find or create the transition tag
    transition_tag = root.find('{http://schemas.openxmlformats.org/drawingml/2006/main}transition')
    if transition_tag is None:
        transition_tag = etree.SubElement(root.find('{http://schemas.openxmlformats.org/presentationml/2006/main}cSld'), 
                                           '{http://schemas.openxmlformats.org/presentationml/2006/main}transition')
    
    # Add the morph element
    morph_tag = etree.SubElement(transition_tag, '{http://schemas.openxmlformats.org/presentationml/2006/main}morph')
    
    # Save the modified XML
    end_slide.part._blob = etree.tostring(root)
    
    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_slide("glassmorphism_presentation.pptx")
