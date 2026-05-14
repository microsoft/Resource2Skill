import requests
import io
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    title_text: str = "The Technique Journey",
    subtitle_text: str = "@Microsoft",
    image_keyword: str = "cityscape",
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with the 'Geometric Image Mosaic' effect.

    Args:
        output_pptx_path (str): The path to save the generated PPTX file.
        title_text (str): The main title for the slide.
        subtitle_text (str): The subtitle for the slide.
        image_keyword (str): A keyword to search for a background image on Unsplash.

    Returns:
        str: The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    background = slide.background
    background.fill.solid()
    background.fill.fore_color.rgb = RGBColor(0, 0, 0)

    # === Layer 2: Geometric Image Mosaic ===
    # Define slide dimensions in pixels for PIL
    slide_width_px = int(prs.slide_width.emu / 9525)
    slide_height_px = int(prs.slide_height.emu / 9525)

    # Fetch an image from Unsplash
    image_url = f"https://source.unsplash.com/1280x720/?{image_keyword}"
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        bg_image = Image.open(io.BytesIO(response.content)).resize((slide_width_px, slide_height_px))
    except (requests.exceptions.RequestException, IOError):
        # Fallback to a plain gradient if image download fails
        bg_image = Image.new("RGB", (slide_width_px, slide_height_px), (10, 20, 40))

    # Create the geometric mask (using triangles as in the tutorial)
    mask = Image.new("L", (slide_width_px, slide_height_px), 0)
    draw = ImageDraw.Draw(mask)

    # Triangle properties
    side_length = 180
    height = int(side_length * (3**0.5) / 2)
    border_width = 8 # Corresponds to the white border in the tutorial

    # Draw the triangle grid on the right side of the slide
    start_x = int(slide_width_px * 0.45)
    for row in range(-1, int(slide_height_px / height) + 1):
        for col in range(int((slide_width_px - start_x) / side_length) + 1):
            cx = start_x + col * side_length
            cy = row * height
            if col % 2 != 0:
                cy += height // 2

            # Upward pointing triangle
            p1 = (cx, cy + height)
            p2 = (cx + side_length, cy + height)
            p3 = (cx + side_length // 2, cy)
            draw.polygon([p1, p2, p3], fill=255)

            # Downward pointing triangle (inverted)
            p1_inv = (cx, cy)
            p2_inv = (cx + side_length, cy)
            p3_inv = (cx + side_length // 2, cy + height)
            draw.polygon([p1_inv, p2_inv, p3_inv], fill=255)

    # Create a separate image for the borders
    border_image = Image.new("RGBA", (slide_width_px, slide_height_px), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(border_image)
    
    # Redraw triangles with outlines for the border effect
    for row in range(-1, int(slide_height_px / height) + 1):
        for col in range(int((slide_width_px - start_x) / side_length) + 1):
            cx = start_x + col * side_length
            cy = row * height
            if col % 2 != 0:
                cy += height // 2
            
            p1, p2, p3 = (cx, cy + height), (cx + side_length, cy + height), (cx + side_length // 2, cy)
            border_draw.polygon([p1, p2, p3], outline=(255, 255, 255, 255), width=border_width)
            
            p1_inv, p2_inv, p3_inv = (cx, cy), (cx + side_length, cy), (cx + side_length // 2, cy + height)
            border_draw.polygon([p1_inv, p2_inv, p3_inv], outline=(255, 255, 255, 255), width=border_width)


    # Composite the image with the mask
    composite_image = Image.new("RGBA", (slide_width_px, slide_height_px))
    composite_image.paste(bg_image.convert("RGBA"), (0, 0), mask)
    composite_image.paste(border_image, (0, 0), border_image) # Add borders on top

    # Save the composite image to a buffer
    image_stream = io.BytesIO()
    composite_image.save(image_stream, format="PNG")
    image_stream.seek(0)

    # Add the final image to the slide
    slide.shapes.add_picture(image_stream, Inches(0), Inches(0), width=prs.slide_width)

    # === Layer 3: Text & Content ===
    # Add Title
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(6), Inches(1))
    title_tf = title_shape.text_frame
    p = title_tf.paragraphs[0]
    p.text = title_text
    p.font.name = 'Arial Black'
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # Add Subtitle
    subtitle_shape = slide.shapes.add_textbox(Inches(0.5), Inches(3.5), Inches(6), Inches(1))
    subtitle_tf = subtitle_shape.text_frame
    p_sub = subtitle_tf.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.name = 'Arial'
    p_sub.font.size = Pt(28)
    p_sub.font.color.rgb = RGBColor(255, 255, 255)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_slide("geometric_mosaic_slide.pptx", image_keyword="chicago")

