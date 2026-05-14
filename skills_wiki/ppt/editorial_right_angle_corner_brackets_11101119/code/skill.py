import os
import urllib.request
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image

def create_slide(
    output_pptx_path: str,
    title_text: str = "抹 茶",
    subtitle_text: str = "三 大 產 地",
    bg_keyword: str = "matcha",
    bracket_color: tuple = (255, 255, 255),
    bracket_thickness: int = 3,
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the "Editorial Right-Angle Corner Bracket" style.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Background Image ===
    try:
        url = f"https://source.unsplash.com/featured/1920x1080/?{bg_keyword},nature"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            img_data = response.read()
        image_stream = BytesIO(img_data)
        slide.shapes.add_picture(image_stream, 0, 0, prs.slide_width, prs.slide_height)
    except Exception as e:
        print(f"Image download failed, using solid color fallback. Error: {e}")
        bg = slide.shapes.add_shape(
            1, 0, 0, prs.slide_width, prs.slide_height # 1 = MSO_SHAPE.RECTANGLE
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(34, 55, 40) # Dark green
        bg.line.fill.background()

    # === Layer 2: Semi-Transparent Overlay (PIL) ===
    # Creates a 40% transparent black image to ensure text pops
    overlay_img = Image.new("RGBA", (100, 100), (0, 0, 0, 102)) # 102/255 approx 40% alpha
    overlay_stream = BytesIO()
    overlay_img.save(overlay_stream, format="PNG")
    overlay_stream.seek(0)
    slide.shapes.add_picture(overlay_stream, 0, 0, prs.slide_width, prs.slide_height)

    # === Layer 3: Typography ===
    # Title
    tx_box = slide.shapes.add_textbox(Inches(3), Inches(2), Inches(7.333), Inches(2))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(96)
    p.font.bold = True
    p.font.name = "Microsoft YaHei"
    p.font.color.rgb = RGBColor(255, 255, 255)

    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(3), Inches(4.5), Inches(7.333), Inches(1))
    sub_tf = sub_box.text_frame
    p2 = sub_tf.paragraphs[0]
    p2.text = subtitle_text
    p2.alignment = PP_ALIGN.CENTER
    p2.font.size = Pt(20)
    p2.font.name = "Microsoft YaHei"
    p2.font.color.rgb = RGBColor(200, 200, 200)

    # === Layer 4: The Core Effect - Right-Angle Brackets ===
    
    # Calculate framing box coordinates around the text
    center_x = prs.slide_width / 2
    center_y = prs.slide_height / 2
    
    # Frame dimensions
    frame_w = Inches(2.2)  # Distance from center to left/right bracket
    frame_h = Inches(1.8)  # Distance from center to top/bottom bracket
    arm_length = Inches(0.5) # How long the "L" arms are
    
    # Build Top-Left Bracket
    # Points: Bottom of vertical arm -> Corner -> End of horizontal arm
    builder_tl = slide.shapes.build_freeform()
    builder_tl.add_line_segments([
        (center_x - frame_w, center_y - frame_h + arm_length),
        (center_x - frame_w, center_y - frame_h),
        (center_x - frame_w + arm_length, center_y - frame_h)
    ])
    bracket_tl = builder_tl.convert_to_shape()
    bracket_tl.line.color.rgb = RGBColor(*bracket_color)
    bracket_tl.line.width = Pt(bracket_thickness)
    bracket_tl.line.join_type = 1 # MSO_LINE_JOIN.MITER (Sharp corners)

    # Build Bottom-Right Bracket
    # Points: Top of vertical arm -> Corner -> End of horizontal arm
    builder_br = slide.shapes.build_freeform()
    builder_br.add_line_segments([
        (center_x + frame_w, center_y + frame_h - arm_length),
        (center_x + frame_w, center_y + frame_h),
        (center_x + frame_w - arm_length, center_y + frame_h)
    ])
    bracket_br = builder_br.convert_to_shape()
    bracket_br.line.color.rgb = RGBColor(*bracket_color)
    bracket_br.line.width = Pt(bracket_thickness)
    bracket_br.line.join_type = 1 # MSO_LINE_JOIN.MITER (Sharp corners)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("editorial_brackets.pptx")
