def create_slide(
    output_pptx_path: str,
    title_text: str = "LIFE IS LIKE SUMMER FLOWERS",
    body_text: str = "Let life be beautiful like summer flowers and death like autumn leaves.",
    image_url: str = "https://images.unsplash.com/photo-1563212896-185585b14144",
    accent_color: tuple = (255, 255, 255),  # Fallback accent color, though it's usually derived
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with an Image-to-Palette Harmony design.
    The background and text colors are automatically derived from the provided image URL.

    Args:
        output_pptx_path (str): The path to save the generated .pptx file.
        title_text (str): The main title for the slide.
        body_text (str): The subtitle or body text for the slide.
        image_url (str): URL of the hero image to use and analyze.
        accent_color (tuple): Fallback text color if image processing fails.

    Returns:
        str: The path to the saved PPTX file.
    """
    import io
    import urllib.request
    import numpy as np
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image
    
    try:
        from sklearn.cluster import KMeans
        sklearn_available = True
    except ImportError:
        sklearn_available = False

    def get_prominent_colors(img, num_colors=3):
        """Extracts dominant colors from a PIL image using KMeans clustering."""
        if not sklearn_available:
            # Fallback if scikit-learn is not installed
            return [(41, 57, 78), (220, 220, 220)]
        
        # Resize for faster processing
        img_small = img.resize((100, 100))
        # Convert to numpy array
        pixels = np.array(img_small.getdata())
        
        # Reshape to be a list of pixels
        pixels = pixels.reshape(-1, 3)
        
        # Use KMeans to find clusters
        kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # Get the RGB values of the cluster centers
        colors = kmeans.cluster_centers_.astype(int)
        return [tuple(color) for color in colors]

    def get_contrast_palette(colors):
        """Selects the darkest and lightest colors from a list for high contrast."""
        if not colors:
            return (41, 57, 78), (255, 255, 255) # Default dark blue and white

        def luminance(r, g, b):
            return 0.2126 * r + 0.7152 * g + 0.0722 * b

        sorted_colors = sorted(colors, key=lambda c: luminance(*c))
        
        darkest = sorted_colors[0]
        lightest = sorted_colors[-1]

        # Ensure there's a minimum contrast
        if luminance(*lightest) - luminance(*darkest) < 80: # Adjust threshold if needed
             # If contrast is too low, use pure white or black for text
            if luminance(*darkest) > 128:
                lightest = (0,0,0) # Use black text on light background
            else:
                lightest = (255,255,255) # Use white text on dark background

        return darkest, lightest

    # --- Presentation Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 ratio
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # --- Default/Fallback Colors ---
    bg_color_rgb = (41, 57, 78)  # Default dark blue
    text_color_rgb = accent_color

    # --- Image Processing ---
    try:
        with urllib.request.urlopen(image_url) as url:
            f = io.BytesIO(url.read())
            image = Image.open(f).convert("RGB")
        
        # Place image on the left
        img_width_px, img_height_px = image.size
        aspect_ratio = img_height_px / img_width_px
        
        slide_height_emu = prs.slide_height
        img_height_emu = slide_height_emu
        img_width_emu = int(img_height_emu / aspect_ratio)
        
        # Crop image from the center if it's too wide
        left_offset = int((img_width_emu - prs.slide_width * 0.45) / 2)
        
        pic = slide.shapes.add_picture(io.BytesIO(image.tobytes()), 0, 0, width=img_width_emu, height=img_height_emu)

        # Crop the picture shape
        pic.crop_left = 0
        pic.crop_right = 0
        # This is a bit of a trick: calculate crop based on desired visual width
        desired_width = prs.slide_width * 0.45
        if img_width_emu > desired_width:
             crop_percentage = (img_width_emu - desired_width) / img_width_emu
             pic.crop_left = crop_percentage / 2
             pic.crop_right = crop_percentage / 2
        
        pic.left = 0
        pic.top = 0
        
        # --- Color Extraction ---
        dominant_colors = get_prominent_colors(image)
        bg_color_rgb, text_color_rgb = get_contrast_palette(dominant_colors)

    except Exception as e:
        print(f"Warning: Could not load or process image from URL. Using fallback colors. Error: {e}")
        # On failure, create a simple gray shape as a placeholder
        slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), 
            width=prs.slide_width * 0.45, height=prs.slide_height
        ).fill.solid()

    # === Layer 1: Background Panel ===
    panel_left = prs.slide_width * 0.45
    panel_width = prs.slide_width * 0.55
    
    panel = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, panel_left, 0, panel_width, prs.slide_height
    )
    panel.fill.solid()
    panel.fill.fore_color.rgb = RGBColor(*bg_color_rgb)
    panel.line.fill.background() # No outline

    # === Layer 2: Text & Content ===
    # Title
    title_shape = slide.shapes.add_textbox(
        panel_left + Inches(0.5), Inches(1.8), panel_width - Inches(1.0), Inches(2.0)
    )
    title_tf = title_shape.text_frame
    title_tf.word_wrap = True
    p_title = title_tf.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = 'Arial Black'
    p_title.font.size = Pt(54)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(*text_color_rgb)
    
    # Body
    body_shape = slide.shapes.add_textbox(
        panel_left + Inches(0.5), Inches(4.0), panel_width - Inches(1.0), Inches(1.5)
    )
    body_tf = body_shape.text_frame
    body_tf.word_wrap = True
    p_body = body_tf.paragraphs[0]
    p_body.text = body_text
    p_body.font.name = 'Arial'
    p_body.font.size = Pt(20)
    p_body.font.color.rgb = RGBColor(*text_color_rgb)

    prs.save(output_pptx_path)
    return output_pptx_path
