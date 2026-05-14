import os
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image

def get_bezier_points(p0, p1, p2, p3, num_points=50):
    """
    Calculate coordinates for a cubic Bezier curve.
    Returns a list of (x, y) tuples.
    """
    points = []
    for i in range(num_points + 1):
        t = i / num_points
        u = 1 - t
        # Cubic bezier formula
        x = (u**3 * p0[0]) + (3 * u**2 * t * p1[0]) + (3 * u * t**2 * p2[0]) + (t**3 * p3[0])
        y = (u**3 * p0[1]) + (3 * u**2 * t * p1[1]) + (3 * u * t**2 * p2[1]) + (t**3 * p3[1])
        points.append((Inches(x), Inches(y)))
    return points

def create_slide(
    output_pptx_path: str,
    title_text: str = "商务服务",
    subtitle_text: str = "对接方案可行性报告",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas porttitor congue massa. Fusce posuere, magna sed pulvinar ultricies, purus lectus malesuada libero, sit amet commodo magna eros quis urna.\n\nNunc viverra imperdiet enim. Fusce est. Vivamus a tellus.",
    bg_palette: str = "architecture", 
    accent_color: tuple = (255, 192, 0),   # Yellow
    primary_color: tuple = (0, 85, 164),   # Navy Blue
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Dynamic Wave Split-Screen Layout.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Download background image
    image_path = "temp_city_bg.jpg"
    try:
        # High-quality architectural/corporate image matching the tutorial vibe
        url = "https://images.unsplash.com/photo-1449844908441-8829872d2607?q=80&w=1024&auto=format&fit=crop"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(image_path, 'wb') as out_file:
            out_file.write(response.read())
    except Exception:
        # Fallback to generated solid image if download fails
        img = Image.new('RGB', (1024, 768), color=(200, 210, 220))
        img.save(image_path)

    # ==========================================
    # Layer 1: The Yellow Offset Wavy Shape (Underlay)
    # ==========================================
    offset_x = -0.3  # Shift left by 0.3 inches
    p0_yell = (6.5 + offset_x, 7.5) # Bottom Left
    p1_yell = (8.5 + offset_x, 5.0) # Control Point 1
    p2_yell = (4.5 + offset_x, 2.5) # Control Point 2
    p3_yell = (6.5 + offset_x, 0.0) # Top Left

    curve_points_yell = get_bezier_points(p0_yell, p1_yell, p2_yell, p3_yell)
    
    # Build shape starting from Top-Right
    ff_yell = slide.shapes.build_freeform(Inches(13.333), Inches(0))
    ff_yell.add_line_segments([
        (Inches(13.333), Inches(7.5)),  # Line to Bottom-Right
        curve_points_yell[0]            # Line to Bottom-Left (start of curve)
    ])
    ff_yell.add_line_segments(curve_points_yell[1:]) # The S-Curve going up
    ff_yell.add_line_segments([(Inches(13.333), Inches(0))]) # Close the shape
    
    yellow_shape = ff_yell.convert_to_shape()
    yellow_shape.fill.solid()
    yellow_shape.fill.fore_color.rgb = RGBColor(*accent_color)
    yellow_shape.line.fill.background() # Remove border

    # ==========================================
    # Layer 2: The Picture Fill Wavy Shape (Overlay)
    # ==========================================
    p0_img = (6.5, 7.5) # Bottom Left
    p1_img = (8.5, 5.0) # Control Point 1
    p2_img = (4.5, 2.5) # Control Point 2
    p3_img = (6.5, 0.0) # Top Left

    curve_points_img = get_bezier_points(p0_img, p1_img, p2_img, p3_img)
    
    ff_img = slide.shapes.build_freeform(Inches(13.333), Inches(0))
    ff_img.add_line_segments([
        (Inches(13.333), Inches(7.5)), 
        curve_points_img[0]
    ])
    ff_img.add_line_segments(curve_points_img[1:])
    ff_img.add_line_segments([(Inches(13.333), Inches(0))])
    
    img_shape = ff_img.convert_to_shape()
    img_shape.line.fill.background()
    # Fill the shape natively with the image (remains perfectly upright!)
    img_shape.fill.user_picture(image_path)

    # ==========================================
    # Layer 3: Typography and Content Setup
    # ==========================================
    
    # 1. Logo Badge
    logo_box = slide.shapes.add_shape(
        1, Inches(1.0), Inches(1.2), Inches(0.8), Inches(0.35) # MSO_SHAPE.RECTANGLE = 1
    )
    logo_box.fill.solid()
    logo_box.fill.fore_color.rgb = RGBColor(*primary_color)
    logo_box.line.fill.background()
    logo_frame = logo_box.text_frame
    logo_p = logo_frame.paragraphs[0]
    logo_p.text = "LOGO"
    logo_p.alignment = PP_ALIGN.CENTER
    logo_p.font.bold = True
    logo_p.font.size = Pt(12)
    logo_p.font.color.rgb = RGBColor(255, 255, 255)

    # 2. Main Title (Yellow)
    title_box = slide.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(5.0), Inches(0.8))
    t_frame = title_box.text_frame
    t_p = t_frame.add_paragraph()
    t_p.text = title_text
    t_p.font.bold = True
    t_p.font.size = Pt(40)
    t_p.font.color.rgb = RGBColor(*accent_color)
    t_p.font.name = "Microsoft YaHei"

    # 3. Subtitle (Navy Blue)
    sub_box = slide.shapes.add_textbox(Inches(0.9), Inches(2.8), Inches(6.0), Inches(1.0))
    s_frame = sub_box.text_frame
    s_p = s_frame.add_paragraph()
    s_p.text = subtitle_text
    s_p.font.bold = True
    s_p.font.size = Pt(44)
    s_p.font.color.rgb = RGBColor(*primary_color)
    s_p.font.name = "Microsoft YaHei"

    # 4. Small Yellow Divider Line
    divider = slide.shapes.add_shape(
        1, Inches(1.0), Inches(4.0), Inches(0.4), Inches(0.06)
    )
    divider.fill.solid()
    divider.fill.fore_color.rgb = RGBColor(*accent_color)
    divider.line.fill.background()

    # 5. Body Text Box
    body_box = slide.shapes.add_textbox(Inches(0.9), Inches(4.3), Inches(4.5), Inches(2.0))
    b_frame = body_box.text_frame
    b_frame.word_wrap = True
    b_p = b_frame.add_paragraph()
    b_p.text = body_text
    b_p.font.size = Pt(12)
    b_p.font.color.rgb = RGBColor(120, 120, 120)
    b_p.font.name = "Arial"

    # Save and clean up
    prs.save(output_pptx_path)
    if os.path.exists(image_path):
        os.remove(image_path)
        
    return output_pptx_path

