import io
import math
import urllib.request
from pptx import Presentation
from pptx.util import Inches
from PIL import Image, ImageDraw

def create_advanced_background_slide(
    output_pptx_path: str,
    fill_type: str = "gradient",
    # General options
    slide_size: str = "widescreen", # "widescreen", "standard", "banner", "portrait"
    hide_theme_graphics: bool = False,
    # Solid fill options
    solid_color: tuple = (0, 112, 192), # RGB
    # Gradient fill options
    gradient_type: str = "radial", # "linear", "radial", "rectangular"
    gradient_colors: list = [(28, 69, 135), (79, 129, 189), (0, 176, 240)], # List of RGB tuples
    # Picture fill options
    image_url: str = "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=800",
    # Pattern fill options
    pattern_name: str = "plaid", # "dots", "lines", "grid", "plaid"
    pattern_fg_color: tuple = (79, 129, 189), # RGB
    pattern_bg_color: tuple = (219, 229, 241), # RGB
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with an advanced background fill.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        fill_type: Type of background fill ('solid', 'gradient', 'picture', 'pattern').
        slide_size: Aspect ratio preset ('widescreen', 'standard', 'banner', 'portrait').
        hide_theme_graphics: If True, hides graphics from the master theme.
        solid_color: RGB tuple for solid fill.
        gradient_type: Type of gradient ('linear', 'radial', 'rectangular').
        gradient_colors: A list of two or more RGB tuples for the gradient.
        image_url: URL of an image to use for picture fill.
        pattern_name: Name of the pattern to generate ('dots', 'lines', 'grid', 'plaid').
        pattern_fg_color: Foreground color for the pattern.
        pattern_bg_color: Background color for the pattern.

    Returns:
        The path to the saved PPTX file.
    """

    prs = Presentation()

    # --- 1. Set Slide Size and Orientation ---
    if slide_size == "widescreen":
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
    elif slide_size == "standard":
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)
    elif slide_size == "banner":
        prs.slide_width = Inches(8)
        prs.slide_height = Inches(1)
    elif slide_size == "portrait":
        prs.slide_width = Inches(7.5)
        prs.slide_height = Inches(10)

    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Hide background graphics from the theme if requested
    if hide_theme_graphics:
        slide.follow_master_background = False

    # --- 2. Generate and Apply Background Fill ---
    background = slide.background
    fill = background.fill
    
    # PIL Image dimensions (higher resolution for better quality)
    IMG_WIDTH, IMG_HEIGHT = 1920, 1080
    if slide_size == "portrait":
         IMG_WIDTH, IMG_HEIGHT = 1080, 1440

    if fill_type == "solid":
        fill.solid()
        fill.fore_color.rgb = solid_color
    
    elif fill_type == "gradient":
        img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT))
        draw = ImageDraw.Draw(img)
        
        num_colors = len(gradient_colors)
        if gradient_type == "linear":
            for i in range(IMG_WIDTH):
                r = int(gradient_colors[0][0] + (gradient_colors[1][0] - gradient_colors[0][0]) * (i / IMG_WIDTH))
                g = int(gradient_colors[0][1] + (gradient_colors[1][1] - gradient_colors[0][1]) * (i / IMG_WIDTH))
                b = int(gradient_colors[0][2] + (gradient_colors[1][2] - gradient_colors[0][2]) * (i / IMG_WIDTH))
                draw.line([(i, 0), (i, IMG_HEIGHT)], fill=(r, g, b))

        elif gradient_type == "radial":
            center_x, center_y = IMG_WIDTH / 2, IMG_HEIGHT / 2
            max_dist = math.sqrt(center_x**2 + center_y**2)
            for y in range(IMG_HEIGHT):
                for x in range(IMG_WIDTH):
                    dist = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                    ratio = dist / max_dist
                    
                    # Interpolate between all colors in the list
                    color_index = min(num_colors - 2, int(ratio * (num_colors - 1)))
                    local_ratio = (ratio * (num_colors - 1)) - color_index
                    
                    start_color = gradient_colors[color_index]
                    end_color = gradient_colors[color_index + 1]
                    
                    r = int(start_color[0] + (end_color[0] - start_color[0]) * local_ratio)
                    g = int(start_color[1] + (end_color[1] - start_color[1]) * local_ratio)
                    b = int(start_color[2] + (end_color[2] - start_color[2]) * local_ratio)
                    
                    img.putpixel((x, y), (r, g, b))

        elif gradient_type == "rectangular":
             for i in range(min(IMG_WIDTH, IMG_HEIGHT) // 2):
                ratio = i / (min(IMG_WIDTH, IMG_HEIGHT) / 2)
                color_index = min(num_colors - 2, int(ratio * (num_colors - 1)))
                local_ratio = (ratio * (num_colors - 1)) - color_index
                start_color = gradient_colors[color_index]
                end_color = gradient_colors[color_index + 1]
                r = int(start_color[0] + (end_color[0] - start_color[0]) * local_ratio)
                g = int(start_color[1] + (end_color[1] - start_color[1]) * local_ratio)
                b = int(start_color[2] + (end_color[2] - start_color[2]) * local_ratio)
                draw.rectangle([(i, i), (IMG_WIDTH - i, IMG_HEIGHT - i)], outline=(r,g,b))


        img_stream = io.BytesIO()
        img.save(img_stream, format='PNG')
        img_stream.seek(0)
        fill.picture(img_stream)

    elif fill_type == "picture":
        try:
            with urllib.request.urlopen(image_url) as url:
                image_data = io.BytesIO(url.read())
            fill.picture(image_data)
        except Exception as e:
            print(f"Warning: Could not download image. Falling back to solid fill. Error: {e}")
            fill.solid()
            fill.fore_color.rgb = (128, 128, 128)

    elif fill_type == "pattern":
        img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), pattern_bg_color)
        draw = ImageDraw.Draw(img)
        spacing = 20
        if pattern_name == "dots":
            for x in range(0, IMG_WIDTH, spacing):
                for y in range(0, IMG_HEIGHT, spacing):
                    draw.ellipse([(x-2, y-2), (x+2, y+2)], fill=pattern_fg_color)
        elif pattern_name == "lines":
            for i in range(0, IMG_WIDTH, spacing // 2):
                draw.line([(i, 0), (i, IMG_HEIGHT)], fill=pattern_fg_color, width=1)
        elif pattern_name == "grid":
            for i in range(0, IMG_WIDTH, spacing):
                draw.line([(i, 0), (i, IMG_HEIGHT)], fill=pattern_fg_color, width=1)
            for i in range(0, IMG_HEIGHT, spacing):
                draw.line([(0, i), (IMG_WIDTH, i)], fill=pattern_fg_color, width=1)
        elif pattern_name == "plaid":
            for i in range(0, IMG_WIDTH, spacing * 2):
                draw.rectangle([(i,0), (i+spacing, IMG_HEIGHT)], fill=pattern_fg_color)
            for i in range(0, IMG_HEIGHT, spacing * 2):
                draw.rectangle([(0,i), (IMG_WIDTH, i+spacing)], fill=pattern_fg_color)
        
        img_stream = io.BytesIO()
        img.save(img_stream, format='PNG')
        img_stream.seek(0)
        fill.picture(img_stream)

    prs.save(output_pptx_path)
    return output_pptx_path

