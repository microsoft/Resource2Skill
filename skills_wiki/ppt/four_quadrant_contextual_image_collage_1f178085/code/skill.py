import os
import io
import urllib.request
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def create_slide(
    output_pptx_path: str,
    title_text: str = "Wif手机百度贴吧\n营销方案",
    subtitle_text: str = "SCENARIO-BASED MARKETING COLLAGE",
    accent_color: tuple = (255, 204, 0),  # Default yellow accent
    **kwargs,
) -> str:
    """
    Creates a PPTX file featuring a 4-quadrant edge-to-edge image collage 
    with a cinematic central semi-transparent overlay for text legibility.
    """
    # 1. Initialize Presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    temp_files = []

    # --- Helper: Fetch or Generate Grid Images ---
    def get_grid_image(seed: int, width=800, height=450):
        """Fetches a random image, falls back to a solid color if offline."""
        url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                img_data = response.read()
            img = Image.open(io.BytesIO(img_data)).convert("RGB")
        except Exception as e:
            print(f"Image download failed for seed {seed}, generating fallback. Error: {e}")
            # Fallback: Generate a solid colored block based on seed
            base_colors = [(40,60,80), (80,40,60), (40,80,60), (60,60,80)]
            img = Image.new("RGB", (width, height), color=base_colors[seed % 4])
        
        # Ensure perfect 16:9 crop
        target_ratio = 16 / 9
        w, h = img.size
        if w / h > target_ratio:
            new_w = int(h * target_ratio)
            left = (w - new_w) / 2
            img = img.crop((left, 0, left + new_w, h))
        elif w / h < target_ratio:
            new_h = int(w / target_ratio)
            top = (h - new_h) / 2
            img = img.crop((0, top, w, top + new_h))
            
        temp_path = f"temp_grid_{seed}.jpg"
        img.save(temp_path, quality=85)
        temp_files.append(temp_path)
        return temp_path

    # --- 2. Build Layer 1: Background 2x2 Grid ---
    quad_w = Inches(13.333 / 2)
    quad_h = Inches(7.5 / 2)
    positions = [
        (0, 0),                  # Top-Left
        (Inches(13.333 / 2), 0), # Top-Right
        (0, Inches(7.5 / 2)),    # Bottom-Left
        (Inches(13.333 / 2), Inches(7.5 / 2)) # Bottom-Right
    ]

    for i in range(4):
        img_path = get_grid_image(seed=i+10) # arbitrary seeds for variety
        left, top = positions[i]
        slide.shapes.add_picture(img_path, left, top, width=quad_w, height=quad_h)


    # --- 3. Build Layer 2: Cinematic Semi-Transparent Overlay ---
    # Create a full slide-sized PNG with a central dark band
    overlay_w, overlay_h = 1920, 1080
    overlay_img = Image.new("RGBA", (overlay_w, overlay_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay_img)
    
    # Draw central band spanning 35% of the height
    band_height = int(overlay_h * 0.40)
    y0 = int((overlay_h - band_height) / 2)
    y1 = y0 + band_height
    
    # Draw semi-transparent dark navy/black band
    draw.rectangle([0, y0, overlay_w, y1], fill=(15, 20, 30, 215))
    
    # Draw thin accent lines at the top and bottom of the band
    draw.rectangle([0, y0, overlay_w, y0+4], fill=accent_color + (255,))
    draw.rectangle([0, y1-4, overlay_w, y1], fill=accent_color + (255,))

    overlay_path = "temp_overlay.png"
    overlay_img.save(overlay_path)
    temp_files.append(overlay_path)
    
    # Insert overlay over the whole slide
    slide.shapes.add_picture(overlay_path, 0, 0, width=Inches(13.333), height=Inches(7.5))


    # --- 4. Build Layer 3: Typography ---
    # Centered Text Box inside the overlay band
    tx_box_height = Inches(2.5)
    tx_box = slide.shapes.add_textbox(
        left=Inches(1.5), 
        top=Inches((7.5 / 2) - 1.25), 
        width=Inches(10.333), 
        height=tx_box_height
    )
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.clear()

    # Main Title
    p_title = tf.paragraphs[0]
    p_title.text = title_text
    p_title.alignment = PP_ALIGN.CENTER
    p_title.font.size = Pt(48)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255) # Pure White
    
    # Subtitle
    p_sub = tf.add_paragraph()
    p_sub.text = subtitle_text
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.font.size = Pt(18)
    p_sub.font.bold = True
    p_sub.font.color.rgb = RGBColor(accent_color[0], accent_color[1], accent_color[2]) # Accent Color
    # Add spacing before subtitle
    p_sub.space_before = Pt(20)


    # --- 5. Cleanup and Save ---
    prs.save(output_pptx_path)
    
    # Clean up temporary image files
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass

    return output_pptx_path

# Example usage (uncomment to test):
# create_slide("four_quadrant_collage.pptx")
