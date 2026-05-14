import os
import urllib.request
from io import BytesIO
from typing import Tuple
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def add_hero_slide(prs, img_bytes: bytes, cyan: RGBColor, red: RGBColor, dark: RGBColor):
    """Generates the split-screen Title/Hero slide (Slide 1 style)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
    
    # 1. Left side Image (approx 45% width)
    img_width = Inches(6)
    try:
        # Add picture and let pptx handle basic scaling, we center crop via placeholder logic if needed, 
        # but standard add_picture stretches. We'll add it and crop.
        pic = slide.shapes.add_picture(img_bytes, Inches(0), Inches(0), width=img_width, height=Inches(7.5))
    except Exception:
        # Fallback if image is invalid
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), img_width, Inches(7.5))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(200, 200, 200)
        shape.line.fill.background()
        
    # 2. Right side framing box (Subtle grey outline)
    frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.5), Inches(0.5), Inches(6.3), Inches(6.5))
    frame.fill.background()
    frame.line.color.rgb = RGBColor(230, 230, 230)
    frame.line.width = Pt(1)

    # 3. Main Title Text
    tb = slide.shapes.add_textbox(Inches(7), Inches(2.5), Inches(5.5), Inches(2))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    run1 = p.add_run()
    run1.text = "Packaging\n"
    run1.font.bold = True
    run1.font.size = Pt(64)
    run1.font.color.rgb = cyan
    run1.font.name = "Arial"
    
    run2 = p.add_run()
    run2.text = "Design"
    run2.font.bold = True
    run2.font.size = Pt(64)
    run2.font.color.rgb = dark
    run2.font.name = "Arial"

    # 4. Cyan Accent Line
    line = slide.shapes.add_connector(1, Inches(12.5), Inches(4.5), Inches(12.5), Inches(2.5))
    line.line.color.rgb = cyan
    line.line.width = Pt(4)

    # 5. Red Accent Triangles
    # Top Left of text area
    tri1 = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(6.8), Inches(1.8), Inches(0.4), Inches(0.4))
    tri1.rotation = 135
    tri1.fill.solid()
    tri1.fill.fore_color.rgb = red
    tri1.line.fill.background()

    # Bottom Right of subtitle area
    tri2 = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(8.5), Inches(5.8), Inches(0.3), Inches(0.3))
    tri2.rotation = 90
    tri2.fill.solid()
    tri2.fill.fore_color.rgb = red
    tri2.line.fill.background()

    # 6. Subtitle Box
    tb_sub = slide.shapes.add_textbox(Inches(9), Inches(5.6), Inches(3.5), Inches(0.8))
    tf_sub = tb_sub.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.alignment = PP_ALIGN.LEFT
    run_sub = p_sub.add_run()
    run_sub.text = "Collection of 10 + PowerPoint Templates"
    run_sub.font.size = Pt(12)
    run_sub.font.color.rgb = RGBColor(100, 100, 100)
    run_sub.font.name = "Arial"
    
    # Subtitle outline box
    sub_frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.8), Inches(5.6), Inches(3.8), Inches(0.6))
    sub_frame.fill.background()
    sub_frame.line.color.rgb = red
    sub_frame.line.width = Pt(1)
    
    # Send sub_frame backward so text is visible (pseudo z-order trick: text added after shape usually works, 
    # but since we added text first, let's swap their positions conceptually by putting text in the shape)
    # Actually, let's just make the shape transparent.
    sub_frame.fill.background()


def add_process_slide(prs, cyan: RGBColor, red: RGBColor, dark: RGBColor):
    """Generates the Horizontal Process Flow slide (Slide 2/4 style)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Title
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(8), Inches(1))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "New packaging design and\nproduct development process"
    run.font.size = Pt(32)
    run.font.color.rgb = dark
    run.font.bold = True
    
    # Horizontal Axis Line
    axis = slide.shapes.add_connector(1, Inches(1), Inches(5), Inches(12.3), Inches(5))
    axis.line.color.rgb = cyan
    axis.line.width = Pt(2)

    steps = ["Plan", "Design", "Quality", "Implement", "Maintain"]
    num_steps = len(steps)
    spacing = 11.3 / num_steps
    start_x = 1.0 + (spacing / 2) - 0.5 # center circles

    for i, step_name in enumerate(steps):
        cx = start_x + (i * spacing)
        
        # Connection drop line
        drop = slide.shapes.add_connector(1, Inches(cx + 0.5), Inches(4.5), Inches(cx + 0.5), Inches(5))
        drop.line.color.rgb = RGBColor(200, 200, 200)

        # Circle Node (Teardrop shape rotated used as marker in video, but circle is standard fallback)
        # We will use an MSO_SHAPE.TEARDROP pointed downwards to match the specific UI exactly
        node = slide.shapes.add_shape(MSO_SHAPE.TEARDROP, Inches(cx + 0.1), Inches(3.6), Inches(0.8), Inches(0.8))
        node.rotation = -90 # Point down
        node.fill.solid()
        node.fill.fore_color.rgb = cyan if i % 2 == 0 else red # Alternate colors for style
        node.line.fill.background()

        # Step Title
        tb_st = slide.shapes.add_textbox(Inches(cx - 0.5), Inches(5.2), Inches(2), Inches(0.5))
        tf_st = tb_st.text_frame
        p_st = tf_st.paragraphs[0]
        p_st.alignment = PP_ALIGN.CENTER
        run_st = p_st.add_run()
        run_st.text = step_name
        run_st.font.size = Pt(18)
        run_st.font.bold = True
        run_st.font.color.rgb = dark

        # Step Description
        tb_desc = slide.shapes.add_textbox(Inches(cx - 0.5), Inches(5.6), Inches(2), Inches(1.5))
        tf_desc = tb_desc.text_frame
        tf_desc.word_wrap = True
        p_desc = tf_desc.paragraphs[0]
        p_desc.alignment = PP_ALIGN.CENTER
        run_desc = p_desc.add_run()
        run_desc.text = "> Task specification\n> Workload review\n> Add text here"
        run_desc.font.size = Pt(10)
        run_desc.font.color.rgb = RGBColor(100, 100, 100)


def create_slide(
    output_pptx_path: str,
    title_text: str = "Corporate Deck",
    body_text: str = "",
    bg_palette: str = "packaging,box", 
    accent_color: tuple = (0, 174, 239), 
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Corporate Geometric Split & Flow Deck style.
    Generates two slides: A Hero split-screen and a Process flow diagram.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Core Palette based on visual extraction
    CYAN = RGBColor(*accent_color)
    RED = RGBColor(240, 90, 80)
    DARK_TEXT = RGBColor(40, 40, 40)

    # Fetch Background Image
    img_url = f"https://source.unsplash.com/featured/800x1000/?{bg_palette.replace(' ', ',')}"
    img_bytes = BytesIO()
    
    try:
        req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            img_bytes.write(response.read())
        img_bytes.seek(0)
    except Exception:
        # Create a dummy colored image using PIL if download fails
        from PIL import Image
        img = Image.new('RGB', (800, 1000), color=(220, 220, 230))
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)

    # Add Slide 1: Hero Split
    add_hero_slide(prs, img_bytes, CYAN, RED, DARK_TEXT)
    
    # Add Slide 2: Process Flow
    add_process_slide(prs, CYAN, RED, DARK_TEXT)

    prs.save(output_pptx_path)
    return output_pptx_path
