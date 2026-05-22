import io
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR
from PIL import Image, ImageDraw

# Helper for lxml XML manipulation
def SubElement(parent, tagname, **kwargs):
    element = etree.SubElement(parent, tagname)
    for key, value in kwargs.items():
        element.set(key, value)
    return element

def qn(tag):
    """
    Stands for 'qualified name', a utility function to turn a namespace prefixed
    tag name into a Clark-notation qualified tag name for lxml.
    """
    nsmap = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
    }
    prefix, tagroot = tag.split(':')
    uri = nsmap[prefix]
    return f'{{{uri}}}{tagroot}'

def add_glowing_text(shape, text, font_size, font_color, glow_color):
    """Adds text to a shape and applies a glow effect using lxml."""
    text_frame = shape.text_frame
    p = text_frame.paragraphs[0]
    run = p.add_run()
    run.text = text
    
    font = run.font
    font.name = 'Segoe UI Semibold'
    font.size = Pt(font_size)
    font.color.rgb = RGBColor(*font_color)

    # Use lxml to add the glow effect (simulated with a soft shadow)
    rPr = run._r.get_or_add_rPr()
    effect_lst = SubElement(rPr, qn('a:effectLst'))
    
    # Outer shadow acts as a glow
    outer_shadow = SubElement(effect_lst, qn('a:outerShdw'), blurRad='101600', dist='0', dir='0', rotWithShape='0')
    srgb_clr = SubElement(outer_shadow, qn('a:srgbClr'), val=f'{glow_color[0]:02X}{glow_color[1]:02X}{glow_color[2]:02X}')
    SubElement(srgb_clr, qn('a:alpha'), val='65000') # 65% alpha

def create_slide(output_pptx_path: str, title_text: str = "SALES DASHBOARD", **kwargs) -> str:
    """
    Creates a PPTX slide with a Digital HUD Dashboard Layout.

    Returns: The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Colors ---
    BG_CENTER_COLOR = (52, 0, 0)
    BG_EDGE_COLOR = (10, 10, 10)
    PANEL_FILL_COLOR = RGBColor(35, 39, 43)
    PANEL_LINE_COLOR = RGBColor(70, 78, 86)
    ACCENT_COLOR = (218, 255, 112)
    WHITE_COLOR = (255, 255, 255)
    
    # === Layer 1: Background ===
    width, height = prs.slide_width.emu, prs.slide_height.emu
    img_width, img_height = Emu(width).pt, Emu(height).pt

    img = Image.new('RGB', (int(img_width), int(img_height)), BG_EDGE_COLOR)
    draw = ImageDraw.Draw(img)

    center_x, center_y = img_width / 2, img_height / 2
    max_radius = int((img_width**2 + img_height**2)**0.5 / 2)

    for i in range(max_radius, 0, -1):
        ratio = i / max_radius
        r = int(BG_CENTER_COLOR[0] * (1 - ratio) + BG_EDGE_COLOR[0] * ratio)
        g = int(BG_CENTER_COLOR[1] * (1 - ratio) + BG_EDGE_COLOR[1] * ratio)
        b = int(BG_CENTER_COLOR[2] * (1 - ratio) + BG_EDGE_COLOR[2] * ratio)
        
        # Draw a circle for a smoother radial gradient effect
        draw.ellipse(
            (center_x - i, center_y - i, center_x + i, center_y + i),
            fill=(r, g, b)
        )

    img_stream = io.BytesIO()
    img.save(img_stream, format='png')
    img_stream.seek(0)
    slide.shapes.add_picture(img_stream, 0, 0, width=prs.slide_width, height=prs.slide_height)
    
    # === Layer 2: Panel Layout ===
    def add_panel(left, top, width, height, is_rounded=True):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if is_rounded else MSO_SHAPE.RECTANGLE, 
                                       Inches(left), Inches(top), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = PANEL_FILL_COLOR
        shape.line.color.rgb = PANEL_LINE_COLOR
        shape.line.width = Pt(1.5)
        if is_rounded:
            shape.adjustments[0] = 0.15 # Adjust roundness
        return shape

    # Header panels
    add_panel(1.3, 0.4, 7.5, 0.7) # Title Panel
    add_panel(9.0, 0.4, 1.8, 0.7) # Sale Type
    add_panel(11.0, 0.4, 2.0, 0.7) # Payment Mode

    # KPI panels
    add_panel(1.3, 1.3, 2.2, 1.2) # Total Sales
    add_panel(3.7, 1.3, 2.2, 1.2) # Total Profit
    add_panel(6.1, 1.3, 2.2, 1.2) # Profit %
    
    # Top Product/Category panels (with decorative ribbon shape)
    add_panel(13.2, 0.4, 2.5, 2.1, is_rounded=False) 
    
    # Main content panels
    add_panel(0.3, 1.3, 0.8, 7.4) # Year/Month Slicers
    add_panel(1.3, 2.7, 5.0, 3.0) # Monthly
    add_panel(6.5, 2.7, 3.5, 3.0) # Product
    add_panel(1.3, 5.9, 8.7, 2.8) # Daily
    add_panel(10.2, 2.7, 2.8, 2.8) # Sales Type Donut
    add_panel(10.2, 5.7, 2.8, 3.0) # Payment Mode Donut
    add_panel(13.2, 2.7, 2.5, 6.0) # Category Treemap
    
    # === Layer 3: Text & Content ===
    # Title
    shape = slide.shapes.add_textbox(Inches(1.5), Inches(0.45), Inches(7.3), Inches(0.6))
    add_glowing_text(shape, title_text.upper(), 28, WHITE_COLOR, ACCENT_COLOR)

    # KPI 1: Total Sales
    shape = slide.shapes.add_textbox(Inches(1.4), Inches(1.4), Inches(2.0), Inches(0.8))
    add_glowing_text(shape, "401K", 40, ACCENT_COLOR, ACCENT_COLOR)
    
    # KPI 2: Total Profit
    shape = slide.shapes.add_textbox(Inches(3.8), Inches(1.4), Inches(2.0), Inches(0.8))
    add_glowing_text(shape, "69K", 40, ACCENT_COLOR, ACCENT_COLOR)
    
    # KPI 3: Profit %
    shape = slide.shapes.add_textbox(Inches(6.2), Inches(1.4), Inches(2.0), Inches(0.8))
    add_glowing_text(shape, "21%", 40, ACCENT_COLOR, ACCENT_COLOR)

    # Placeholder for chart labels
    def add_label(text, left, top, size=12, bold=False, color=WHITE_COLOR):
        txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(2), Inches(0.5))
        p = txBox.text_frame.paragraphs[0]
        p.text = text
        p.font.name = 'Segoe UI'
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = RGBColor(*color)
    
    add_label("MONTHLY", 1.5, 2.8, 14, True, ACCENT_COLOR)
    add_label("DAILY", 1.5, 6.0, 14, True, ACCENT_COLOR)
    add_label("PRODUCT", 6.7, 2.8, 14, True, ACCENT_COLOR)
    add_label("SALES TYPE", 10.4, 2.8, 14, True, ACCENT_COLOR)
    add_label("PAYMENT MODE", 10.4, 5.8, 14, True, ACCENT_COLOR)
    add_label("CATEGORY", 13.4, 2.8, 14, True, ACCENT_COLOR)
    
    prs.save(output_pptx_path)
    return output_pptx_path
