import os
import urllib.request
from io import BytesIO
from PIL import Image, ImageDraw, ImageOps
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def create_slide(
    output_pptx_path: str,
    masthead_text: str = "Photo Magz",
    main_title: str = "Office\nIn Nature",
    highlight_year: str = "2024",
    bg_palette: str = "nature,office",
    tint_color: tuple = (15, 35, 60),  # Dark navy blue
    accent_color: tuple = (255, 204, 0) # Yellow highlight
) -> str:
    """
    Creates a PPTX file reproducing the 'Diagonal Duotone Split' magazine cover style.
    """
    # 1. Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    width_px, height_px = 1920, 1080

    # 2. Fetch or Generate Background Image
    try:
        url = f"https://source.unsplash.com/random/{width_px}x{height_px}/?{bg_palette}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            base_img = Image.open(BytesIO(response.read())).convert("RGBA")
            base_img = base_img.resize((width_px, height_px), Image.Resampling.LANCZOS)
    except Exception:
        # Fallback if download fails
        base_img = Image.new("RGBA", (width_px, height_px), (100, 120, 110, 255))
        draw = ImageDraw.Draw(base_img)
        draw.line([(0,0), (width_px, height_px)], fill=(120, 140, 130), width=10)

    # Save the base image
    base_img_path = "temp_base_bg.png"
    base_img.convert("RGB").save(base_img_path)

    # 3. Create the Duotone/Tinted Overlay Image
    # Convert to grayscale, then colorize with the tint color
    gray_img = base_img.convert("L")
    tinted_img = ImageOps.colorize(gray_img, black="black", white=tint_color).convert("RGBA")

    # 4. Create the Diagonal Mask
    # Triangle covering the bottom left
    mask = Image.new("L", (width_px, height_px), 0)
    mask_draw = ImageDraw.Draw(mask)
    # Define a polygon: from middle-left, down to bottom-left, across to bottom-right
    polygon_points = [
        (0, height_px * 0.25),   # Start a bit down from top left
        (0, height_px),          # Bottom left
        (width_px, height_px),   # Bottom right
        (width_px, height_px * 0.8) # Slight angle up on the right
    ]
    mask_draw.polygon(polygon_points, fill=255)

    # Apply the mask as alpha channel to the tinted image
    tinted_img.putalpha(mask)
    
    overlay_img_path = "temp_overlay_bg.png"
    tinted_img.save(overlay_img_path)

    # 5. Insert Images into PowerPoint
    # Insert Base Full-Color Image
    slide.shapes.add_picture(base_img_path, 0, 0, prs.slide_width, prs.slide_height)
    
    # Insert Tinted Overlay Image exactly on top
    slide.shapes.add_picture(overlay_img_path, 0, 0, prs.slide_width, prs.slide_height)

    # 6. Add Typography
    # Masthead (Top Center)
    tx_box_masthead = slide.shapes.add_textbox(Inches(0), Inches(0.5), prs.slide_width, Inches(1.5))
    tf_masthead = tx_box_masthead.text_frame
    tf_masthead.text = masthead_text
    p_masthead = tf_masthead.paragraphs[0]
    p_masthead.alignment = PP_ALIGN.CENTER
    p_masthead.font.name = "Century Gothic"
    p_masthead.font.size = Pt(64)
    p_masthead.font.bold = True
    p_masthead.font.color.rgb = RGBColor(255, 255, 255)

    # Feature Title (Bottom Left, over the tinted area)
    tx_box_title = slide.shapes.add_textbox(Inches(1.5), Inches(4.5), Inches(8), Inches(2))
    tf_title = tx_box_title.text_frame
    
    # Main Title Lines
    p_title = tf_title.paragraphs[0]
    p_title.text = main_title
    p_title.font.name = "Century Gothic"
    p_title.font.size = Pt(44)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255)
    
    # Highlight Year Line
    p_year = tf_title.add_paragraph()
    p_year.text = highlight_year
    p_year.font.name = "Century Gothic"
    p_year.font.size = Pt(44)
    p_year.font.bold = True
    p_year.font.color.rgb = RGBColor(accent_color[0], accent_color[1], accent_color[2])

    # Footer/Author (Bottom Center/Left)
    tx_box_footer = slide.shapes.add_textbox(Inches(1.5), Inches(6.8), Inches(5), Inches(0.5))
    tf_footer = tx_box_footer.text_frame
    tf_footer.text = "Citizen Photography / Design Issue"
    p_footer = tf_footer.paragraphs[0]
    p_footer.font.name = "Century Gothic"
    p_footer.font.size = Pt(14)
    p_footer.font.color.rgb = RGBColor(200, 200, 200)

    # Clean up temp files
    try:
        os.remove(base_img_path)
        os.remove(overlay_img_path)
    except OSError:
        pass

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# create_slide("magazine_cover_slide.pptx")
