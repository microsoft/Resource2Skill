import os
import urllib.request
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml
from PIL import Image, ImageDraw

# Specify ambient capability for shell retrieval
AMBIENT_CAPABLE = True
try:
    from _shell_helpers import add_drift_motion
except ImportError:
    # Fallback mock if _shell_helpers is missing in execution environment
    def add_drift_motion(slide, shape, dx_in=0, dy_in=0, duration_ms=2000, pingpong=True):
        pass

def create_slide(
    output_pptx_path: str,
    title_text: str = "VizDeals Product Demo",
    subtitle_text: str = "An AI-powered lightweight CRM built specifically for independent professionals.",
    accent_color: tuple = (255, 107, 107),  # Vibrant Coral
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Lovable Dark Navy & Coral SaaS Pitch Slide aesthetic.
    Features a floating mockup and a clean feature list with coral accents.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # === Color Palette ===
    COLOR_BG_DARK = (10, 15, 30)       # Darkest navy edge
    COLOR_BG_LIGHT = (25, 35, 60)      # Lighter navy center/top-left
    COLOR_TEXT_PRIMARY = RGBColor(255, 255, 255)
    COLOR_TEXT_MUTED = RGBColor(148, 163, 184)
    COLOR_ACCENT = RGBColor(*accent_color)

    # === Layer 1: Generate & Apply Radial Gradient Background ===
    bg_img_path = "temp_dark_navy_bg.png"
    width, height = int(13.333 * 100), int(7.5 * 100)  # High res enough for BG
    bg_img = Image.new('RGBA', (width, height), COLOR_BG_DARK)
    draw = ImageDraw.Draw(bg_img)
    
    # Draw a subtle spotlight in the top left
    cx, cy = width * 0.3, height * 0.3
    max_radius = width * 0.8
    for r in range(int(max_radius), 0, -10):
        # Calculate interpolation factor
        factor = (r / max_radius) ** 2
        r_c = int(COLOR_BG_DARK[0] * factor + COLOR_BG_LIGHT[0] * (1 - factor))
        g_c = int(COLOR_BG_DARK[1] * factor + COLOR_BG_LIGHT[1] * (1 - factor))
        b_c = int(COLOR_BG_DARK[2] * factor + COLOR_BG_LIGHT[2] * (1 - factor))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(r_c, g_c, b_c, 255))
        
    bg_img.save(bg_img_path)
    slide.shapes.add_picture(bg_img_path, 0, 0, prs.slide_width, prs.slide_height)
    os.remove(bg_img_path)

    # === Layer 2: Main Headers ===
    # Title
    tx_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(12.333), Inches(0.8))
    tf = tx_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    p.font.name = "Arial"

    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.1), Inches(8.0), Inches(0.5))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = COLOR_TEXT_MUTED
    p_sub.font.name = "Arial"

    # === Layer 3: The Product Mockup (Left Side) ===
    # Attempt to download a cool dashboard/tech image
    img_url = "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=1000&auto=format&fit=crop"
    try:
        req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img_data = BytesIO(response.read())
            img_to_insert = img_data
    except Exception:
        # Fallback PIL image if offline
        fallback_img = Image.new('RGB', (800, 600), (30, 41, 59))
        draw_fb = ImageDraw.Draw(fallback_img)
        draw_fb.rectangle([0, 0, 800, 40], fill=(15, 23, 42))
        draw_fb.ellipse([20, 15, 30, 25], fill=(255, 107, 107))
        draw_fb.ellipse([40, 15, 50, 25], fill=(255, 217, 102))
        draw_fb.ellipse([60, 15, 70, 25], fill=(112, 173, 71))
        draw_fb.text((300, 280), "Mockup Unavailable", fill=(255,255,255))
        img_data = BytesIO()
        fallback_img.save(img_data, format='PNG')
        img_to_insert = img_data

    # Add the mockup picture
    mockup_pic = slide.shapes.add_picture(img_to_insert, Inches(0.5), Inches(2.0), width=Inches(6.8))
    
    # Inject an advanced drop shadow via lxml to elevate the mockup
    shadow_xml = """
    <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:outerShdw blurRad="250000" dist="150000" dir="5400000" algn="b" rotWithShape="0">
            <a:srgbClr val="000000">
                <a:alpha val="60000"/>
            </a:srgbClr>
        </a:outerShdw>
    </a:effectLst>
    """
    mockup_pic.spPr.append(parse_xml(shadow_xml))

    # Add ambient floating motion to the mockup!
    add_drift_motion(slide, mockup_pic, dx_in=0, dy_in=0.15, duration_ms=3500, pingpong=True)

    # === Layer 4: Feature List (Right Side) ===
    features = [
        ("Visual Deal Pipeline", "Track every opportunity from lead to close with drag-and-drop stages. Fully customizable."),
        ("AI Assistant Command Bar", "Type natural language to add contacts, create deals, and update stages instantly."),
        ("Dashboard Analytics", "Real-time metrics, conversion rate pipeline value, and revenue at a glance."),
        ("Cloud-Backed & Secure", "Your data is encrypted, persistent, and accessible from any device.")
    ]

    start_x = Inches(8.0)
    start_y = Inches(2.0)
    spacing = Inches(1.2)

    for i, (feat_title, feat_desc) in enumerate(features):
        y_pos = start_y + (i * spacing)
        
        # Draw Coral Accent Indicator (Small Rounded Rect / Dash)
        accent_shape = slide.shapes.add_shape(
            1, # MSO_SHAPE.RECTANGLE
            start_x, y_pos + Inches(0.05), Inches(0.15), Inches(0.15)
        )
        accent_shape.fill.solid()
        accent_shape.fill.fore_color.rgb = COLOR_ACCENT
        accent_shape.line.fill.background() # No border
        
        # Feature Title
        f_box = slide.shapes.add_textbox(start_x + Inches(0.3), y_pos - Inches(0.05), Inches(4.5), Inches(0.4))
        tf_f = f_box.text_frame
        p_f = tf_f.paragraphs[0]
        p_f.text = feat_title
        p_f.font.size = Pt(18)
        p_f.font.bold = True
        p_f.font.color.rgb = COLOR_TEXT_PRIMARY
        p_f.font.name = "Arial"
        
        # Feature Description
        d_box = slide.shapes.add_textbox(start_x + Inches(0.3), y_pos + Inches(0.3), Inches(4.6), Inches(0.8))
        tf_d = d_box.text_frame
        tf_d.word_wrap = True
        p_d = tf_d.paragraphs[0]
        p_d.text = feat_desc
        p_d.font.size = Pt(13)
        p_d.font.color.rgb = COLOR_TEXT_MUTED
        p_d.font.name = "Arial"
        p_d.line_spacing = 1.2

    prs.save(output_pptx_path)
    return output_pptx_path
