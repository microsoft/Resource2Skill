import io
import requests
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from PIL import Image, ImageDraw, ImageFilter

def create_slide(
    output_pptx_path: str,
    title_text: str = "WELCOME TO",
    subtitle_text: str = "SEE THE",
    main_text: str = "MOUNTAINS",
    image_url: str = "https://images.unsplash.com/photo-1549880338-65ddcdfd017b?w=1600&h=900&fit=crop",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a Parallax Glass Pane Reveal effect.

    This function simulates PowerPoint's "Slide background fill" by pre-compositing
    angled panes with shadows and the background image using PIL. The complex
    parallax animation from the tutorial is best applied manually in PowerPoint.

    Returns: Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Emu(12192000)  # 16:9 aspect ratio
    prs.slide_height = Emu(6858000)
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # --- 1. Background Image Preparation ---
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        bg_image_stream = io.BytesIO(response.content)
        bg_pil = Image.open(bg_image_stream).convert("RGBA")
    except (requests.exceptions.RequestException, IOError):
        # Fallback to a gradient if image download fails
        bg_pil = Image.new("RGBA", (1920, 1080), (13, 17, 28))
        draw = ImageDraw.Draw(bg_pil)
        for i in range(1080):
            r = 13 + int((50 - 13) * (i / 1080))
            g = 17 + int((60 - 17) * (i / 1080))
            b = 28 + int((80 - 28) * (i / 1080))
            draw.line([(0, i), (1920, i)], fill=(r, g, b))

    # Resize image to fit slide dimensions
    slide_w_px, slide_h_px = 1920, 1080
    bg_pil = bg_pil.resize((slide_w_px, slide_h_px), Image.Resampling.LANCZOS)
    
    # Set the main slide background
    bg_stream = io.BytesIO()
    bg_pil.save(bg_stream, format="PNG")
    bg_stream.seek(0)
    slide.background.fill.solid() # First clear any existing fill
    slide.background.fill.picture(bg_stream)

    # --- 2. Define Pane Geometry (as polygons in pixel coordinates) ---
    # These coordinates define three angled parallelograms
    pane_polygons = [
        [(300, 0), (800, 0), (500, 1080), (0, 1080)],
        [(850, 0), (1350, 0), (1050, 1080), (550, 1080)],
        [(1400, 0), (1900, 0), (1600, 1080), (1100, 1080)],
    ]

    # --- 3. Create and Place Panes with Shadows using PIL ---
    for poly in pane_polygons:
        # Create a canvas for the pane and its shadow
        pane_canvas = Image.new("RGBA", (slide_w_px, slide_h_px), (0, 0, 0, 0))
        
        # a) Draw the shadow
        shadow_offset = (15, 15)
        shadow_poly = [(p[0] + shadow_offset[0], p[1] + shadow_offset[1]) for p in poly]
        shadow_layer = Image.new("RGBA", (slide_w_px, slide_h_px), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_layer)
        shadow_draw.polygon(shadow_poly, fill=(0, 0, 0, 80)) # Semi-transparent black
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=15))

        # b) Create the pane mask
        mask = Image.new("L", (slide_w_px, slide_h_px), 0)
        ImageDraw.Draw(mask).polygon(poly, fill=255)

        # c) Composite the elements: shadow first, then the pane content
        pane_content = Image.new("RGBA", (slide_w_px, slide_h_px))
        pane_content.paste(bg_pil, mask=mask)
        
        final_pane = Image.alpha_composite(shadow_layer, pane_content)

        # d) Save to stream and add to slide
        pane_stream = io.BytesIO()
        final_pane.save(pane_stream, format="PNG")
        pane_stream.seek(0)
        slide.shapes.add_picture(pane_stream, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # --- 4. Add Text Layer ---
    def add_text(text, top_inch, size_pt, bold=True):
        textbox = slide.shapes.add_textbox(Inches(0), top_inch, width=prs.slide_width, height=Inches(1.5))
        tf = textbox.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = text
        p.font.name = 'Arial Black'
        p.font.size = Pt(size_pt)
        p.font.bold = bold
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = 1 # PP_ALIGN.CENTER
        # Add a subtle text shadow
        shadow = p.font.shadow
        shadow.visible = True
        shadow.blur_radius = Emu(25400)
        shadow.distance = Emu(25400)
        shadow.angle = 90 * 60000
        shadow.color.rgb = RGBColor(0,0,0)
        shadow.alpha = int(0.5 * 100000) # 50% transparent

    add_text(title_text, Inches(2.5), 44)
    add_text(subtitle_text, Inches(3.2), 28)
    add_text(main_text, Inches(3.7), 60)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_slide("parallax_glass_pane.pptx")

