import os
import tempfile
from pptx import Presentation
from pptx.util import Inches
from PIL import Image, ImageDraw, ImageFilter, ImageOps

def create_slide(
    output_pptx_path: str,
    title_text: str = "FLIGHT PATH",
    **kwargs
) -> str:
    """
    Creates a retro-futuristic flight perspective slide.
    Generates a perspective grid, horizon, hovering aircraft, and projected shadow.
    """
    
    # 1. Setup Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # Temporary directory for our generated assets
    temp_dir = tempfile.mkdtemp()
    
    # Canvas dimensions for high-res asset generation
    W, H = 1920, 1080
    horizon_y = int(H * 0.6) # Horizon at 60% down

    # ==========================================
    # ASSET 1: Background, Ground, & Perspective Grid
    # ==========================================
    bg_img = Image.new('RGBA', (W, H))
    draw_bg = ImageDraw.Draw(bg_img)

    # Draw Sky Gradient (Top to Horizon)
    sky_top = (150, 170, 210, 255)
    sky_bottom = (220, 230, 240, 255)
    for y in range(horizon_y):
        ratio = y / horizon_y
        r = int(sky_top[0] * (1 - ratio) + sky_bottom[0] * ratio)
        g = int(sky_top[1] * (1 - ratio) + sky_bottom[1] * ratio)
        b = int(sky_top[2] * (1 - ratio) + sky_bottom[2] * ratio)
        draw_bg.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # Draw Ground Gradient (Horizon to Bottom)
    ground_top = (100, 160, 120, 255)
    ground_bottom = (40, 90, 50, 255)
    for y in range(horizon_y, H):
        ratio = (y - horizon_y) / (H - horizon_y)
        r = int(ground_top[0] * (1 - ratio) + ground_bottom[0] * ratio)
        g = int(ground_top[1] * (1 - ratio) + ground_bottom[1] * ratio)
        b = int(ground_top[2] * (1 - ratio) + ground_bottom[2] * ratio)
        draw_bg.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # Draw Radial Perspective Lines (Vanishing point at center horizon)
    vp_x, vp_y = W // 2, horizon_y
    grid_color = (255, 255, 255, 90)
    
    # Draw lines fanning out downwards
    num_radials = 24
    for i in range(-num_radials, num_radials + 1):
        # Calculate x intercept at the bottom of the screen
        x_bottom = vp_x + (i * (W // 8))
        draw_bg.line([(vp_x, vp_y), (x_bottom, H)], fill=grid_color, width=3)

    # Draw Horizontal Perspective Lines (Spacing increases exponentially)
    num_horizontals = 15
    for i in range(1, num_horizontals + 1):
        # Quadratic curve for perspective feeling
        factor = (i / num_horizontals) ** 2.2 
        y_line = vp_y + int((H - vp_y) * factor)
        draw_bg.line([(0, y_line), (W, y_line)], fill=grid_color, width=3)

    bg_path = os.path.join(temp_dir, "bg_grid.png")
    bg_img.save(bg_path)


    # ==========================================
    # ASSET 2: The Aircraft (Sci-Fi Silhouette)
    # ==========================================
    plane_w, plane_h = 600, 300
    plane_img = Image.new('RGBA', (plane_w, plane_h), (0,0,0,0))
    draw_plane = ImageDraw.Draw(plane_img)

    hull_color = (40, 45, 55, 255)
    engine_color = (255, 200, 0, 255)

    # Custom Sci-Fi Jet Polygon coordinates (Symmetrical)
    # Center is at x=300, y=150
    cx, cy = plane_w // 2, plane_h // 2
    
    # Main Wings
    draw_plane.polygon([
        (cx, cy - 20),           # Nose
        (cx + 250, cy + 30),     # Right Wingtip
        (cx + 250, cy + 50),     # Right Wingtip back
        (cx + 40, cy + 30),      # Right Inner Wing
        (cx, cy + 80),           # Tail Center
        (cx - 40, cy + 30),      # Left Inner Wing
        (cx - 250, cy + 50),     # Left Wingtip back
        (cx - 250, cy + 30),     # Left Wingtip
    ], fill=hull_color)

    # Engine Glow (Two circles)
    draw_plane.ellipse([cx - 35, cy + 20, cx - 15, cy + 40], fill=engine_color)
    draw_plane.ellipse([cx + 15, cy + 20, cx + 35, cy + 40], fill=engine_color)

    # Tail Fins
    draw_plane.polygon([(cx - 25, cy + 10), (cx - 35, cy - 30), (cx - 15, cy + 20)], fill=hull_color)
    draw_plane.polygon([(cx + 25, cy + 10), (cx + 35, cy - 30), (cx + 15, cy + 20)], fill=hull_color)

    plane_path = os.path.join(temp_dir, "plane.png")
    plane_img.save(plane_path)


    # ==========================================
    # ASSET 3: The Shadow (Flipped, Darkened, Blurred)
    # ==========================================
    # Extract alpha mask from plane to make the shadow
    shadow_img = Image.new('RGBA', (plane_w, plane_h), (0,0,0,0))
    shadow_draw = ImageDraw.Draw(shadow_img)
    
    # We draw the same polygon but in dark green
    shadow_color = (20, 60, 30, 200) # Dark semi-transparent green
    shadow_draw.polygon([
        (cx, cy - 20), (cx + 250, cy + 30), (cx + 250, cy + 50), (cx + 40, cy + 30), 
        (cx, cy + 80), (cx - 40, cy + 30), (cx - 250, cy + 50), (cx - 250, cy + 30)
    ], fill=shadow_color)
    
    # Flip vertically
    shadow_img = ImageOps.flip(shadow_img)
    # Squash it to look like it's resting flat on the perspective plane
    shadow_img = shadow_img.resize((plane_w, int(plane_h * 0.4)), resample=Image.Resampling.LANCZOS)
    
    # Create a new canvas to give blur room to expand
    shadow_canvas = Image.new('RGBA', (plane_w + 100, int(plane_h * 0.4) + 100), (0,0,0,0))
    shadow_canvas.paste(shadow_img, (50, 50), shadow_img)
    
    # Apply Gaussian Blur (Equivalent to PPTX Soft Edges)
    shadow_canvas = shadow_canvas.filter(ImageFilter.GaussianBlur(radius=15))
    
    shadow_path = os.path.join(temp_dir, "shadow.png")
    shadow_canvas.save(shadow_path)


    # ==========================================
    # PPTX SCENE ASSEMBLY
    # ==========================================
    
    # 1. Background Grid (Fills slide)
    slide.shapes.add_picture(bg_path, Inches(0), Inches(0), Inches(13.333), Inches(7.5))

    # 2. Shadow (Placed on the "ground" below the plane)
    shadow_width = Inches(5)
    # Calculate position to center it
    sh_left = (prs.slide_width - shadow_width) / 2
    sh_top = Inches(4.8) # Placed below the horizon line
    slide.shapes.add_picture(shadow_path, sh_left, sh_top, width=shadow_width)

    # 3. Aircraft (Floating above the ground)
    plane_width_in = Inches(5)
    p_left = (prs.slide_width - plane_width_in) / 2
    p_top = Inches(2.5) # Hovering in the sky
    slide.shapes.add_picture(plane_path, p_left, p_top, width=plane_width_in)


    # Clean up temp files (optional, but good practice)
    try:
        os.remove(bg_path)
        os.remove(plane_path)
        os.remove(shadow_path)
        os.rmdir(temp_dir)
    except:
        pass

    prs.save(output_pptx_path)
    return output_pptx_path
