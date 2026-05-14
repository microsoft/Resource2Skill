import tempfile
import os
from pptx import Presentation
from pptx.util import Inches
from PIL import Image, ImageDraw, ImageFont
import math

def create_slide(
    output_pptx_path: str,
    title_text: str = "Example: Git to S3 Webhooks",
    body_text: str = "",
    accent_color: tuple = (255, 140, 0),  # RGB for the tracer (bright orange)
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with an animated GIF showing a data flow path.

    The animation is generated frame-by-frame using PIL and saved as a GIF,
    which is then placed onto a PowerPoint slide.

    Returns: path to the saved PPTX file.
    """
    # === Constants and Setup ===
    IMG_WIDTH, IMG_HEIGHT = 1280, 720
    BG_COLOR = (10, 10, 25)
    TEXT_COLOR = (220, 220, 220)
    LINE_COLOR = (80, 80, 90)
    
    # Define key points for the animation path
    path_points = [(250, 500), (450, 500), (450, 360), (800, 360)]
    
    # Animation parameters
    NUM_FRAMES_PER_SEGMENT = 30
    TRACER_RADIUS = 8
    GLOW_RADIUS = 16

    # --- Helper function to interpolate points for smooth animation ---
    def interpolate(p1, p2, n_steps):
        points = []
        for i in range(n_steps + 1):
            t = i / n_steps
            x = p1[0] * (1 - t) + p2[0] * t
            y = p1[1] * (1 - t) + p2[1] * t
            points.append((x, y))
        return points

    # === Layer 1: Create Static Background Image ===
    try:
        font = ImageFont.truetype("Arial.ttf", 24)
        title_font = ImageFont.truetype("Arial-Bold.ttf", 32)
    except IOError:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()

    base_img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(base_img)

    # Draw diagram components (as placeholders)
    # Git Repository
    draw.rectangle([(150, 200), (350, 420)], outline=LINE_COLOR, width=2)
    draw.text((160, 210), "Third-party\nGit repository", font=font, fill=TEXT_COLOR)
    
    # AWS Lambda
    draw.rectangle([(550, 310), (750, 410)], outline=accent_color, width=3)
    draw.text((595, 345), "AWS Lambda", font=font, fill=accent_color)
    
    # Draw connecting lines for the static diagram
    draw.line([(350, 360), (550, 360)], fill=LINE_COLOR, width=2) # Main line
    draw.line([(250, 420), (250, 500), (450, 500), (450, 410)], fill=LINE_COLOR, width=2) # Lower path

    # Draw title text
    draw.text((50, 50), title_text, font=title_font, fill=TEXT_COLOR)

    # === Layer 2: Generate Animation Frames ===
    frames = []
    full_path = []
    for i in range(len(path_points) - 1):
        full_path.extend(interpolate(path_points[i], path_points[i+1], NUM_FRAMES_PER_SEGMENT))
    
    for pos in full_path:
        frame = base_img.copy()
        draw_frame = ImageDraw.Draw(frame)
        
        # Draw glow
        glow_bbox = (pos[0] - GLOW_RADIUS, pos[1] - GLOW_RADIUS, pos[0] + GLOW_RADIUS, pos[1] + GLOW_RADIUS)
        draw_frame.ellipse(glow_bbox, fill=accent_color + (64,)) # Use RGBA for transparency
        
        # Draw tracer core
        tracer_bbox = (pos[0] - TRACER_RADIUS, pos[1] - TRACER_RADIUS, pos[0] + TRACER_RADIUS, pos[1] + TRACER_RADIUS)
        draw_frame.ellipse(tracer_bbox, fill=accent_color)
        
        frames.append(frame)
        
    # Add auto-reverse
    frames.extend(frames[::-1])

    # === Save animation as a GIF file ===
    gif_path = os.path.join(tempfile.gettempdir(), "animated_flow.gif")
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=20,  # Milliseconds per frame
        loop=0,       # Loop forever
        optimize=True
    )

    # === Layer 3: Create PowerPoint and Insert GIF ===
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Add a black background to the slide
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = (0,0,0)

    # Add the generated GIF, centered
    left = (prs.slide_width - Inches(IMG_WIDTH / 96)) / 2
    top = (prs.slide_height - Inches(IMG_HEIGHT / 96)) / 2
    pic = slide.shapes.add_picture(gif_path, left, top, width=Inches(IMG_WIDTH / 96))

    # Clean up the temporary GIF file
    os.remove(gif_path)

    prs.save(output_pptx_path)
    return output_pptx_path

