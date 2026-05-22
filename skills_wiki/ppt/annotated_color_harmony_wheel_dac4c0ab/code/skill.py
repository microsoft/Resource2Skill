import math
import io
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw, ImageFont, ImageColor

def create_color_theory_slides(output_pptx_path: str, **kwargs) -> str:
    """
    Creates a multi-slide PPTX presentation explaining color theory concepts
    using an annotated color wheel, as seen in the tutorial.

    Each slide demonstrates a different color harmony principle.

    Returns:
        str: The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # --- Data for each slide ---
    harmonies = {
        "同色系 (Monochromatic)": {
            "description": "同一色相调整明度和饱和度\n(Adjusting brightness and saturation of a single hue)",
            "type": "monochromatic",
            "angle": 0,
        },
        "类似色 (Analogous)": {
            "description": "相差60°以内的色彩\n(Colors within a 60° arc)",
            "type": "arc",
            "angle": 60,
        },
        "邻近色 (Adjacent)": {
            "description": "间隔60-90°以内的色彩\n(Colors within a 90° arc)",
            "type": "arc",
            "angle": 90,
        },
        "对比色 (Triadic)": {
            "description": "相互之间角度为120°的色彩\n(Colors 120° apart from each other)",
            "type": "triadic",
            "angle": 120,
        },
        "互补色 (Complementary)": {
            "description": "相互之间角度为180°的色彩\n(Colors 180° apart from each other)",
            "type": "complementary",
            "angle": 180,
        },
    }

    # --- Helper function to generate the wheel image ---
    def _generate_harmony_wheel_image(harmony_type: str, angle: int, size: int = 1000) -> io.BytesIO:
        img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        center = size / 2
        radius = size / 2 * 0.9
        inner_radius_ratio = 0.4
        
        # 1. Draw the color wheel (24 segments)
        num_segments = 24
        angle_step = 360 / num_segments
        for i in range(num_segments):
            start_angle = i * angle_step
            end_angle = (i + 1) * angle_step
            hue = int(start_angle)
            
            fill_color = ImageColor.getrgb(f"hsl({hue}, 100%, 50%)")
            draw.pieslice(
                [center - radius, center - radius, center + radius, center + radius],
                start_angle - 90,
                end_angle - 90,
                fill=fill_color,
            )
            
        # 2. Draw the inner white circle to create a donut
        inner_radius = radius * inner_radius_ratio
        draw.ellipse(
            [center - inner_radius, center - inner_radius, center + inner_radius, center + inner_radius],
            fill=(255, 255, 255, 255),
        )
        
        # 3. Draw annotations based on harmony type
        # Rotate all angles by -90 to align 0 degrees with the right horizontal axis
        rotation = -90 
        annotation_color = (80, 80, 80)
        
        if harmony_type == "monochromatic":
            # Point to the red color and show variations
            base_hue = 0
            for i in range(4):
                lightness = 30 + i * 15
                sat = 100 - i * 5
                color = ImageColor.getrgb(f"hsl({base_hue}, {sat}%, {lightness}%)")
                r_offset = inner_radius + (radius - inner_radius) * (0.2 + 0.2 * i)
                x = center + r_offset * math.cos(math.radians(base_hue + rotation))
                y = center + r_offset * math.sin(math.radians(base_hue + rotation))
                draw.ellipse([x-20, y-20, x+20, y+20], fill=color, outline=annotation_color, width=2)

        elif harmony_type == "arc":
            start, end = 0, angle
            draw.pieslice([0, 0, size, size], start + rotation, end + rotation,
                          outline=annotation_color, width=5)
            
        elif harmony_type == "triadic":
            for i in range(3):
                a = (i * angle) + rotation
                x_end = center + radius * math.cos(math.radians(a))
                y_end = center + radius * math.sin(math.radians(a))
                draw.line([center, center, x_end, y_end], fill=annotation_color, width=5)
                
        elif harmony_type == "complementary":
            start_angle_rad = math.radians(0 + rotation)
            end_angle_rad = math.radians(180 + rotation)
            x1 = center + inner_radius * math.cos(start_angle_rad)
            y1 = center + inner_radius * math.sin(start_angle_rad)
            x2 = center + radius * math.cos(start_angle_rad)
            y2 = center + radius * math.sin(start_angle_rad)
            draw.line([x1, y1, x2, y2], fill=annotation_color, width=5)
            
            x3 = center + inner_radius * math.cos(end_angle_rad)
            y3 = center + inner_radius * math.sin(end_angle_rad)
            x4 = center + radius * math.cos(end_angle_rad)
            y4 = center + radius * math.sin(end_angle_rad)
            draw.line([x3, y3, x4, y4], fill=annotation_color, width=5)


        image_stream = io.BytesIO()
        img.save(image_stream, format="PNG")
        image_stream.seek(0)
        return image_stream

    # --- Loop through harmonies and create a slide for each ---
    for title, data in harmonies.items():
        slide_layout = prs.slide_layouts[6]  # Blank layout
        slide = prs.slides.add_slide(slide_layout)
        
        # Set a plain white background
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(255, 255, 255)

        # Generate and add the wheel image
        image_stream = _generate_harmony_wheel_image(data["type"], data["angle"])
        slide.shapes.add_picture(image_stream, Inches(7), Inches(1), height=Inches(5.5))

        # Add title and description text
        # Title box with red accent
        title_shape = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(5), Inches(1))
        title_frame = title_shape.text_frame
        p = title_frame.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(28)
        p.font.color.rgb = RGBColor(80, 80, 80)

        accent_box = slide.shapes.add_shape(1, Inches(1), Inches(2.1), Inches(1.5), Inches(0.4))
        accent_fill = accent_box.fill
        accent_fill.solid()
        accent_fill.fore_color.rgb = RGBColor(211, 84, 0)
        line = accent_box.line
        line.fill.background() # No outline

        # Move accent box behind title text
        accent_xml = accent_box._element
        accent_xml.getparent().remove(accent_xml)
        title_shape._element.getparent().insert(0, accent_xml)
        
        # Description box
        desc_shape = slide.shapes.add_textbox(Inches(1.2), Inches(3.2), Inches(5), Inches(1.5))
        desc_frame = desc_shape.text_frame
        desc_frame.word_wrap = True
        p_desc = desc_frame.paragraphs[0]
        p_desc.text = data["description"]
        p_desc.font.size = Pt(18)
        p_desc.font.color.rgb = RGBColor(128, 128, 128)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_color_theory_slides("color_theory_presentation.pptx")
