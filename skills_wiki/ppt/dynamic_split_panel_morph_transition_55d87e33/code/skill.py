import io
import urllib.request
from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def create_transparent_rect(slide, left, top, width, height, r, g, b, alpha_pct):
    """
    Helper to create a rectangle with transparency via lxml injection.
    """
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(r, g, b)
    shape.line.fill.background() # No outline
    
    # Inject transparency using lxml
    srgbClr = shape._element.xpath('.//a:srgbClr', namespaces={'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'})
    if srgbClr:
        alpha_val = int((1.0 - alpha_pct) * 100000)
        alpha_elem = etree.SubElement(srgbClr[0], '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha')
        alpha_elem.set('val', str(alpha_val))
    return shape

def apply_morph_transition(slide):
    """
    Helper to inject the Morph transition into a slide's XML.
    """
    transition = etree.SubElement(slide._element, '{http://schemas.openxmlformats.org/presentationml/2006/main}transition')
    morph = etree.SubElement(transition, '{http://schemas.openxmlformats.org/presentationml/2006/main}morph')
    morph.set('option', 'byObject')

def create_slide(
    output_pptx_path: str,
    title_text: str = "FUTURE VISION",
    body_text: str = "",
    bg_palette: str = "city,architecture",
    accent_color: tuple = (0, 191, 255),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Dynamic Split-Panel Morph Transition".
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # 1. Fetch Background Image (with Pillow fallback)
    try:
        url = "https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=1600&auto=format&fit=crop"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            image_stream = io.BytesIO(response.read())
    except Exception:
        img = Image.new('RGB', (1600, 900), color=(40, 50, 60))
        image_stream = io.BytesIO()
        img.save(image_stream, format='PNG')
        image_stream.seek(0)

    # Calculate Panel Dimensions
    panel_w = prs.slide_width / 3
    panel_h = prs.slide_height
    panel_colors = [
        (68, 84, 106),
        (54, 69, 90),
        (40, 54, 74)
    ]
    
    # ==========================================
    # SLIDE 1: The Initial "Hero" State
    # ==========================================
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])
    
    # A. Background Image
    slide1.shapes.add_picture(image_stream, 0, 0, prs.slide_width, prs.slide_height)
    
    # B. Dark Overlay
    create_transparent_rect(slide1, 0, 0, prs.slide_width, prs.slide_height, 20, 25, 40, 0.6)
    
    # C. Main Title
    tx1 = slide1.shapes.add_textbox(Inches(1), Inches(2.8), Inches(11.333), Inches(1.5))
    p1 = tx1.text_frame.paragraphs[0]
    p1.text = title_text
    p1.alignment = PP_ALIGN.CENTER
    p1.font.size = Pt(72)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)
    
    # D. Off-Screen Panels (Staggered to create cascade effect)
    # They are created in exact order to pair with Slide 2 for Morphing
    create_transparent_rect(slide1, 0, Inches(8.0), panel_w, panel_h, *panel_colors[0], 0.0)
    create_transparent_rect(slide1, panel_w, Inches(9.5), panel_w, panel_h, *panel_colors[1], 0.0)
    create_transparent_rect(slide1, panel_w*2, Inches(8.5), panel_w, panel_h, *panel_colors[2], 0.0)

    # ==========================================
    # SLIDE 2: The "Split Panel" Revealed State
    # ==========================================
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    
    # A. Background Image (Must match exactly)
    image_stream.seek(0)
    slide2.shapes.add_picture(image_stream, 0, 0, prs.slide_width, prs.slide_height)
    
    # B. Dark Overlay
    create_transparent_rect(slide2, 0, 0, prs.slide_width, prs.slide_height, 20, 25, 40, 0.6)
    
    # C. Main Title (Shifted and shrunk)
    tx2 = slide2.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.333), Inches(1.0))
    p2 = tx2.text_frame.paragraphs[0]
    p2.text = title_text
    p2.alignment = PP_ALIGN.CENTER
    p2.font.size = Pt(40)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(200, 200, 200)

    # D. On-Screen Panels (Moved up to Y=0 to trigger the morph)
    create_transparent_rect(slide2, 0, 0, panel_w, panel_h, *panel_colors[0], 0.0)
    create_transparent_rect(slide2, panel_w, 0, panel_w, panel_h, *panel_colors[1], 0.0)
    create_transparent_rect(slide2, panel_w*2, 0, panel_w, panel_h, *panel_colors[2], 0.0)
    
    # E. Add Content inside Panels (Fades in dynamically during morph)
    for i in range(3):
        # Decorative Outline Circle (Pseudo-icon placeholder)
        cx = (panel_w * i) + (panel_w / 2) - Inches(0.75)
        cy = Inches(2.0)
        circle = slide2.shapes.add_shape(MSO_SHAPE.OVAL, cx, cy, Inches(1.5), Inches(1.5))
        circle.fill.background()
        circle.line.color.rgb = RGBColor(255, 255, 255)
        circle.line.width = Pt(1.5)
        
        # Sub-heading
        hx = slide2.shapes.add_textbox((panel_w * i) + Inches(0.5), Inches(3.8), panel_w - Inches(1.0), Inches(0.5))
        hp = hx.text_frame.paragraphs[0]
        hp.text = f"Pillar 0{i+1}"
        hp.font.color.rgb = RGBColor(255, 255, 255)
        hp.font.size = Pt(24)
        hp.font.bold = True
        hp.alignment = PP_ALIGN.CENTER
        
        # Body Paragraph
        bx = slide2.shapes.add_textbox((panel_w * i) + Inches(0.5), Inches(4.5), panel_w - Inches(1.0), Inches(1.5))
        bp = bx.text_frame.paragraphs[0]
        bp.text = "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        bx.text_frame.word_wrap = True
        bp.font.color.rgb = RGBColor(200, 210, 220)
        bp.font.size = Pt(13)
        bp.alignment = PP_ALIGN.CENTER

    # Inject the Morph Transition into Slide 2 XML
    apply_morph_transition(slide2)

    prs.save(output_pptx_path)
    return output_pptx_path
