import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from PIL import Image, ImageDraw, ImageFont

def create_slide(
    output_pptx_path: str,
    name_text: str = "小 美",
    pinyin_text: str = "XIAOMEI",
    bio_text: str = (
        "秋叶大学职场学院高材生，原就读于湖北省武汉市绝对学霸高中；\n\n"
        "身具段子天赋，因言语出口成章、举手投足出梗；\n"
        "被高中同学誉为“新时代段子手”的姑娘；\n\n"
        "小破站业余UP主，创造过10W+阅读量的姑娘。"
    ),
    accent_color: tuple = (235, 77, 75),  # Coral Red from the video vibe
    bg_color: tuple = (255, 255, 255)
) -> str:
    """
    Creates a PPTX file reproducing the "Typographic Profile Lockup" effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Set background color
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # ---------------------------------------------------------
    # 1. Generate Placeholder Avatar using PIL
    # ---------------------------------------------------------
    avatar_path = "temp_avatar.png"
    img_size = (600, 800)
    avatar_img = Image.new('RGB', img_size)
    draw = ImageDraw.Draw(avatar_img)
    # Draw a soft gradient placeholder
    for y in range(img_size[1]):
        r = int(245 - (245 - 220) * (y / img_size[1]))
        g = int(245 - (245 - 220) * (y / img_size[1]))
        b = int(250 - (250 - 230) * (y / img_size[1]))
        draw.line([(0, y), (img_size[0], y)], fill=(r, g, b))
    
    # Add an abstract geometric "person" icon logic
    draw.ellipse([(150, 150), (450, 450)], fill=(200, 200, 210))
    draw.pieslice([(50, 450), (550, 1050)], 180, 360, fill=(200, 200, 210))
    avatar_img.save(avatar_path)

    # Insert Avatar onto slide (Left side)
    slide.shapes.add_picture(avatar_path, Inches(1.5), Inches(1.5), width=Inches(3.5), height=Inches(4.66))

    # ---------------------------------------------------------
    # 2. Main Title (Giant Display Name)
    # ---------------------------------------------------------
    # We position this on the right side.
    title_box = slide.shapes.add_textbox(Inches(5.5), Inches(1.2), Inches(5.5), Inches(1.5))
    tf_title = title_box.text_frame
    tf_title.clear()
    
    p_title = tf_title.paragraphs[0]
    p_title.text = name_text
    p_title.alignment = PP_ALIGN.RIGHT  # Right align to create the invisible grid
    
    font_title = p_title.font
    font_title.name = "Microsoft YaHei" # Standard fallback (User applies custom font here in real life)
    font_title.size = Pt(72)
    font_title.bold = True
    font_title.color.rgb = RGBColor(*accent_color)

    # ---------------------------------------------------------
    # 3. Vertical Stacked Subtitle (Pinyin/English)
    # ---------------------------------------------------------
    # Positioned just to the right of the main text block
    vert_box = slide.shapes.add_textbox(Inches(11.2), Inches(1.2), Inches(0.8), Inches(5.0))
    tf_vert = vert_box.text_frame
    tf_vert.clear()
    
    p_vert = tf_vert.paragraphs[0]
    # Trick to create stacked vertical text: join characters with newlines, adding spaces for aesthetics
    stacked_text = "\n".join(list(pinyin_text.replace(" ", "")))
    p_vert.text = stacked_text
    p_vert.alignment = PP_ALIGN.CENTER
    
    font_vert = p_vert.font
    font_vert.name = "Arial"
    font_vert.size = Pt(20)
    font_vert.bold = True
    font_vert.color.rgb = RGBColor(180, 180, 180) # Muted light gray
    
    # ---------------------------------------------------------
    # 4. Biography Body Text Block
    # ---------------------------------------------------------
    bio_box = slide.shapes.add_textbox(Inches(5.5), Inches(3.0), Inches(5.5), Inches(3.0))
    tf_bio = bio_box.text_frame
    tf_bio.clear()
    tf_bio.word_wrap = True
    
    p_bio = tf_bio.paragraphs[0]
    p_bio.text = bio_text
    p_bio.alignment = PP_ALIGN.RIGHT # Align right to match the title's edge
    p_bio.line_spacing = 1.4 # Give it editorial breathing room
    
    font_bio = p_bio.font
    font_bio.name = "Microsoft YaHei"
    font_bio.size = Pt(14)
    font_bio.color.rgb = RGBColor(80, 80, 80) # Dark Charcoal

    # Save presentation
    prs.save(output_pptx_path)
    
    # Cleanup temp file
    if os.path.exists(avatar_path):
        os.remove(avatar_path)
        
    return output_pptx_path

# Example execution:
# create_slide("typographic_profile.pptx")
