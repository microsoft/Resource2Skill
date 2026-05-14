import math
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt
from PIL import Image, ImageDraw, ImageFont
import urllib.request

def create_slide(
    output_pptx_path: str,
    title_text: str = "Sales Performance",
    current_value: float = 450,
    min_value: float = 0,
    max_value: float = 1200,
    red_zone_end: float = 300,
    yellow_zone_end: float = 900,
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a KPI Performance Gauge visual.

    Args:
        output_pptx_path: The path to save the generated PPTX file.
        title_text: The title to display in the center of the gauge.
        current_value: The current value to display on the gauge.
        min_value: The minimum value of the gauge scale.
        max_value: The maximum value of the gauge scale.
 컴퓨_zone_end: The value at which the red zone ends.
        yellow_zone_end: The value at which the yellow zone ends.

    Returns:
        Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- PIL Image Generation ---
    # Create a transparent canvas
    img_size = 600
    img = Image.new('RGBA', (img_size, img_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Define gauge properties
    center = (img_size // 2, img_size // 2)
    radius = img_size // 2 - 40
    thickness = 80
    bbox = [
        (center[0] - radius, center[1] - radius),
        (center[0] + radius, center[1] + radius),
    ]
    
    start_angle = 135
    end_angle = 405 # 135 + 270

    # Define color zones
    red_color = (217, 30, 24)
    yellow_color = (242, 194, 0)
    green_color = (80, 175, 71)

    # Function to map a value to an angle
    def value_to_angle(value):
        value_ratio = (value - min_value) / (max_value - min_value)
        angle_range = end_angle - start_angle
        return start_angle + (value_ratio * angle_range)

    # Draw the zones
    angle_red_end = value_to_angle(red_zone_end)
    angle_yellow_end = value_to_angle(yellow_zone_end)
    
    # Red zone
    draw.arc(bbox, start_angle, angle_red_end, fill=red_color, width=thickness)
    # Yellow zone
    draw.arc(bbox, angle_red_end, angle_yellow_end, fill=yellow_color, width=thickness)
    # Green zone
    draw.arc(bbox, angle_yellow_end, end_angle, fill=green_color, width=thickness)
    
    # --- Draw the Needle ---
    needle_angle_deg = value_to_angle(current_value)
    needle_angle_rad = math.radians(-needle_angle_deg + 90) # Adjust for PIL's coordinate system
    
    needle_len = radius - 10
    needle_width = 15
    
    p1 = (center[0], center[1])
    p2 = (
        center[0] + needle_width * math.cos(needle_angle_rad + math.pi / 2),
        center[1] + needle_width * math.sin(needle_angle_rad + math.pi / 2),
    )
    p3 = (
        center[0] + needle_len * math.cos(needle_angle_rad),
        center[1] + needle_len * math.sin(needle_angle_rad),
    )
    p4 = (
        center[0] + needle_width * math.cos(needle_angle_rad - math.pi / 2),
        center[1] + needle_width * math.sin(needle_angle_rad - math.pi / 2),
    )
    
    draw.polygon([p2, p3, p4], fill=(89, 89, 89))
    
    # Draw center hub
    hub_radius = 25
    draw.ellipse(
        (center[0] - hub_radius, center[1] - hub_radius,
         center[0] + hub_radius, center[1] + hub_radius),
        fill=(0, 120, 215),
        outline=(255,255,255),
        width=4
    )

    # --- Draw Text ---
    try:
        font_main_path = "C:/Windows/Fonts/arialbd.ttf"
        font_sub_path = "C:/Windows/Fonts/arial.ttf"
        font_main = ImageFont.truetype(font_main_path, 90)
        font_sub = ImageFont.truetype(font_sub_path, 36)
        font_title = ImageFont.truetype(font_sub_path, 40)
    except IOError:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_title = ImageFont.load_default()
        
    # Main value text
    value_str = f"{current_value:,.0f}"
    text_bbox = draw.textbbox((0, 0), value_str, font=font_main)
    text_width = text_bbox[2] - text_bbox[0]
    draw.text((center[0] - text_width / 2, center[1] - 60), value_str, font=font_main, fill=(0, 0, 0))
    
    # Title text
    title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text((center[0] - title_width / 2, center[1] - 180), title_text, font=font_title, fill=(89, 89, 89))
    
    # Percentage text
    percentage = (current_value - min_value) / (max_value - min_value)
    percent_str = f"{percentage:.1%}"
    percent_bbox = draw.textbbox((0, 0), percent_str, font=font_sub)
    percent_width = percent_bbox[2] - percent_bbox[0]
    draw.text((center[0] - percent_width / 2, center[1] + 60), percent_str, font=font_sub, fill=(128, 128, 128))

    # --- Save image and insert into slide ---
    image_stream = BytesIO()
    img.save(image_stream, format="PNG")
    image_stream.seek(0)
    
    slide.shapes.add_picture(
        image_stream, Inches(3.66), Inches(0.75), width=Inches(6)
    )

    prs.save(output_pptx_path)
    return output_pptx_path

