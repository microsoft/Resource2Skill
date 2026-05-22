def create_slide(
    output_pptx_path: str,
    title_text: str = "PHANTOM TRANSPARENCY",
    subtitle_text: str = "Solid vs. Glassmorphic State",
    bg_keyword: str = "forest,macro",
    solid_color: tuple = (220, 40, 60),  # RGB for Red (Solid Object)
    glass_tint: tuple = (230, 255, 230), # RGB for slight green tint (Glass Object)
    **kwargs,
) -> str:
    """
    Creates a PPTX demonstrating the "Phantom Glassmorphism" effect.
    Generates 3D shaded objects and applies luminance-to-alpha conversion 
    to simulate Photoshop's 'Screen' blending mode.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw, ImageEnhance, ImageChops
    import urllib.request
    import io
    import math
    import os

    # --- 1. Helper Function: Generate 3D Spheres (Mocking the Pears) ---
    def generate_3d_sphere(base_color, radius=300):
        """Generates a pseudo-3D sphere with radial gradient shading."""
        size = radius * 2
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Center of the highlight (offset to top-left)
        hx, hy = radius * 0.6, radius * 0.6
        
        for r in range(radius, 0, -1):
            # Calculate interpolation factor based on distance from highlight
            factor = (r / radius) ** 1.5 
            
            # Interpolate between shadow (dark) and highlight (white)
            r_val = int(base_color[0] * factor + 255 * (1 - factor))
            g_val = int(base_color[1] * factor + 255 * (1 - factor))
            b_val = int(base_color[2] * factor + 255 * (1 - factor))
            
            # Add a bit of shadow towards the edge
            if factor > 0.8:
                darken = 1 - ((factor - 0.8) * 2)
                r_val = int(r_val * darken)
                g_val = int(g_val * darken)
                b_val = int(b_val * darken)
                
            color = (r_val, g_val, b_val, 255)
            
            # Draw concentric circles towards the highlight center
            x0 = hx - r * (hx/radius)
            y0 = hy - r * (hy/radius)
            draw.ellipse([x0, y0, x0 + r*2, y0 + r*2], fill=color)
            
        return img

    # --- 2. Generate Assets ---
    # Create the solid object
    solid_sphere = generate_3d_sphere(solid_color)
    solid_path = "temp_solid.png"
    solid_sphere.save(solid_path)

    # Create the transparent/glass object (The Core Skill Extraction)
    # Step A: Convert solid object to grayscale (L)
    gray = solid_sphere.convert('L')
    
    # Step B: Adjust levels (Contrast + Brightness) to make highlights pop and shadows disappear
    gray = ImageEnhance.Contrast(gray).enhance(1.8)
    gray = ImageEnhance.Brightness(gray).enhance(1.2)
    
    # Step C: Reduce overall opacity slightly (like the 70% in video)
    gray = gray.point(lambda p: int(p * 0.85))
    
    # Step D: Extract original mask to keep crisp edges
    _, _, _, alpha_mask = solid_sphere.split()
    
    # Bound the new alpha by the original shape's boundaries
    final_alpha = ImageChops.multiply(gray, alpha_mask)
    
    # Step E: Apply "Screen" blend logic. 
    # A white image with Grayscale Alpha acts exactly like Screen Blend over a background.
    glass_sphere = Image.new('RGBA', solid_sphere.size, glass_tint + (255,))
    glass_sphere.putalpha(final_alpha)
    
    glass_path = "temp_glass.png"
    glass_sphere.save(glass_path)

    # --- 3. PPTX Construction ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Add Background Image
    bg_path = "temp_bg.jpg"
    try:
        url = f"https://source.unsplash.com/random/1920x1080/?{bg_keyword}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(bg_path, 'wb') as f:
                f.write(response.read())
        slide.shapes.add_picture(bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
    except Exception:
        # Fallback Background if network fails
        bg_img = Image.new('RGB', (1920, 1080), (13, 27, 42))
        bg_draw = ImageDraw.Draw(bg_img)
        for i in range(1080):
            bg_draw.line([(0, i), (1920, i)], fill=(13 + int(i*0.02), 27 + int(i*0.03), 42 + int(i*0.05)))
        bg_img.save(bg_path)
        slide.shapes.add_picture(bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # Add Solid Object (Left)
    slide.shapes.add_picture(solid_path, Inches(1.5), Inches(2.0), width=Inches(4.5))

    # Add Transparent/Glass Object (Right)
    slide.shapes.add_picture(glass_path, Inches(7.333), Inches(2.0), width=Inches(4.5))

    # Add Title Text
    title_box = slide.shapes.add_textbox(Inches(0), Inches(0.5), prs.slide_width, Inches(1))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Arial"
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # Add Subtitle Text
    sub_box = slide.shapes.add_textbox(Inches(0), Inches(1.2), prs.slide_width, Inches(0.5))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(24)
    p_sub.font.color.rgb = RGBColor(200, 200, 200)

    # Cleanup temp files
    prs.save(output_pptx_path)
    
    for tmp_file in [solid_path, glass_path, bg_path]:
        if os.path.exists(tmp_file):
            try:
                os.remove(tmp_file)
            except:
                pass

    return output_pptx_path
