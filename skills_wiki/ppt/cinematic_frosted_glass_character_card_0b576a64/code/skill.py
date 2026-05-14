import os
import urllib.request
from io import BytesIO
from typing import Tuple
from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageFilter, ImageDraw

def create_slide(
    output_pptx_path: str,
    person_name: str = "GU JIUSI",
    person_role: str = "Lead Protagonist",
    body_text: str = "A cinematic approach to character introductions. The frosted glass effect allows atmospheric backgrounds to coexist with crisp, readable typography.",
    bg_keyword: str = "cinematic,interior",
) -> str:
    """
    Create a PPTX file reproducing the Cinematic Frosted Glass Character Card.
    """
    # 1. Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333) # 16:9 
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide

    # Screen dimensions in pixels (assuming 96 dpi for PIL generation)
    WIDTH, HEIGHT = 1280, 720
    
    # --- PIL ASSET GENERATION ---
    
    # 2. Fetch or Generate Background Image
    bg_url = f"https://source.unsplash.com/random/{WIDTH}x{HEIGHT}/?{bg_keyword}"
    try:
        req = urllib.request.Request(bg_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            bg_img = Image.open(BytesIO(response.read())).convert("RGBA")
            bg_img = bg_img.resize((WIDTH, HEIGHT))
    except Exception:
        # Fallback: Dark moody gradient if network fails
        bg_img = Image.new("RGBA", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(bg_img)
        for y in range(HEIGHT):
            r = int(20 + (y / HEIGHT) * 20)
            g = int(30 + (y / HEIGHT) * 30)
            b = int(40 + (y / HEIGHT) * 40)
            draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))

    # Save base background
    bg_path = "temp_bg.jpg"
    bg_img.convert("RGB").save(bg_path, quality=90)

    # 3. Generate "Frosted Glass" Card Layer
    # Card coordinates (Left 5%, Top 10%, Width 55%, Height 80%)
    card_box = (
        int(WIDTH * 0.05), int(HEIGHT * 0.10),
        int(WIDTH * 0.60), int(HEIGHT * 0.90)
    )
    
    # Crop, Blur, and Darken
    glass_img = bg_img.crop(card_box)
    glass_img = glass_img.filter(ImageFilter.GaussianBlur(radius=25))
    
    # Add dark semi-transparent overlay to ensure text readability
    overlay = Image.new("RGBA", glass_img.size, (15, 20, 25, 140))
    glass_img = Image.alpha_composite(glass_img, overlay)
    
    # Add subtle bright border to simulate glass edge reflection
    draw = ImageDraw.Draw(glass_img)
    draw.rectangle([0, 0, glass_img.width-1, glass_img.height-1], outline=(255, 255, 255, 60), width=2)
    
    glass_path = "temp_glass.png"
    glass_img.save(glass_path)

    # 4. Generate Subject Cutout (Placeholder Silhouette)
    # Simulates an AI-cutout character portrait with a transparent background
    subject_img = Image.new("RGBA", (int(WIDTH * 0.5), int(HEIGHT * 0.9)), (255, 255, 255, 0))
    s_draw = ImageDraw.Draw(subject_img)
    
    # Draw elegant silhouette
    s_w, s_h = subject_img.size
    head_radius = int(s_w * 0.2)
    head_center = (s_w // 2, int(s_h * 0.3))
    # Head
    s_draw.ellipse(
        [head_center[0]-head_radius, head_center[1]-head_radius, head_center[0]+head_radius, head_center[1]+head_radius], 
        fill=(180, 190, 200, 255)
    )
    # Shoulders/Body
    s_draw.polygon(
        [(s_w * 0.1, s_h), (s_w * 0.2, s_h * 0.6), (s_w * 0.4, s_h * 0.5), 
         (s_w * 0.6, s_h * 0.5), (s_w * 0.8, s_h * 0.6), (s_w * 0.9, s_h)], 
        fill=(100, 110, 120, 255)
    )
    # Shadow/glow behind subject
    subject_img = subject_img.filter(ImageFilter.SMOOTH_MORE)
    subject_path = "temp_subject.png"
    subject_img.save(subject_path)

    # --- PPTX ASSEMBLY ---

    # A. Insert Background
    slide.shapes.add_picture(bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # B. Insert Frosted Glass Card (precisely aligned with the crop coordinates)
    glass_left = Inches(13.333 * 0.05)
    glass_top = Inches(7.5 * 0.10)
    glass_width = Inches(13.333 * 0.55)
    glass_height = Inches(7.5 * 0.80)
    slide.shapes.add_picture(glass_path, glass_left, glass_top, width=glass_width, height=glass_height)

    # C. Add Typography inside the Glass Card
    # C1. Hero Name (Golden)
    tx_name = slide.shapes.add_textbox(glass_left + Inches(0.4), glass_top + Inches(0.4), Inches(6), Inches(1))
    tf_name = tx_name.text_frame
    p_name = tf_name.paragraphs[0]
    p_name.text = person_name.upper()
    p_name.font.size = Pt(54)
    p_name.font.bold = True
    p_name.font.name = "Impact" # Or any thick display font
    p_name.font.color.rgb = RGBColor(212, 175, 55) # Metallic Gold
    
    # C2. Role / Label (Muted White)
    tx_role = slide.shapes.add_textbox(glass_left + Inches(0.4), glass_top + Inches(1.5), Inches(4), Inches(0.5))
    p_role = tx_role.text_frame.paragraphs[0]
    p_role.text = "Role | " + person_role
    p_role.font.size = Pt(16)
    p_role.font.color.rgb = RGBColor(200, 200, 200)

    # C3. Body Text (White, readable against the dark blurred background)
    tx_body = slide.shapes.add_textbox(glass_left + Inches(0.4), glass_top + Inches(2.2), glass_width - Inches(0.8), Inches(2))
    tx_body.text_frame.word_wrap = True
    p_body = tx_body.text_frame.paragraphs[0]
    p_body.text = body_text
    p_body.font.size = Pt(14)
    p_body.font.color.rgb = RGBColor(240, 240, 240)
    p_body.line_spacing = 1.5

    # D. Insert Subject Cutout (Overlapping the glass card on the right)
    subj_width = Inches(13.333 * 0.45)
    subj_left = Inches(13.333 * 0.50) # Starts slightly inside the glass card, extends out
    subj_top = Inches(7.5 * 0.10)
    slide.shapes.add_picture(subject_path, subj_left, subj_top, width=subj_width)

    # Save and clean up
    prs.save(output_pptx_path)
    
    for temp_file in [bg_path, glass_path, subject_path]:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    return output_pptx_path
