def create_slide(
    output_pptx_path: str,
    title_text: str = "Sample",
    left_title: str = "Sample",
    right_title: str = "Sample",
    **kwargs
) -> str:
    """
    Create a PPTX file reproducing the Split-Screen Tangent Node Infographic effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from PIL import Image, ImageDraw
    import urllib.request
    import os

    # --- Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # blank layout

    # --- Colors ---
    RED = RGBColor(238, 59, 36)
    DARK = RGBColor(43, 50, 60)
    WHITE = RGBColor(255, 255, 255)

    # --- Helpers ---
    def add_line(sl, start_x, start_y, end_x, end_y, color, width=Pt(2.5)):
        connector = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, start_x, start_y, end_x, end_y)
        connector.line.color.rgb = color
        connector.line.width = width
        return connector

    def format_badge_text(shape, text, color, size):
        shape.text = text
        tf = shape.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        for p in tf.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            for run in p.runs:
                run.font.color.rgb = color
                run.font.size = size
                run.font.bold = True

    def make_circular_image(url, output_path, size=(300, 300)):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                img = Image.open(response).convert("RGBA")
        except Exception:
            # Fallback block
            img = Image.new("RGBA", size, (150, 150, 150, 255))
        
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim) / 2
        top = (h - min_dim) / 2
        img = img.crop((left, top, left + min_dim, top + min_dim))
        
        # Use newer Resampling enum if available, fallback to ANTIALIAS
        resample = getattr(Image, 'Resampling', Image).LANCZOS
        img = img.resize(size, resample)
        
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        
        result = Image.new('RGBA', size, (0, 0, 0, 0))
        result.paste(img, (0, 0), mask)
        result.save(output_path)
        return output_path

    # --- 1. Background Split ---
    left_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(6.666), Inches(7.5))
    left_bg.fill.solid(); left_bg.fill.fore_color.rgb = RED
    left_bg.line.fill.background()

    right_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.666), 0, Inches(6.667), Inches(7.5))
    right_bg.fill.solid(); right_bg.fill.fore_color.rgb = DARK
    right_bg.line.fill.background()

    # --- 2. Title Arch ---
    title_arch = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(4.666), Inches(-1.0), Inches(4.0), Inches(2.0))
    title_arch.fill.solid(); title_arch.fill.fore_color.rgb = WHITE
    title_arch.line.fill.background()

    title_box = slide.shapes.add_textbox(Inches(4.666), Inches(0.1), Inches(4.0), Inches(0.8))
    p = title_box.text_frame.paragraphs[0]
    p.text = title_text; p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(28); p.font.color.rgb = RED; p.font.bold = True

    # --- 3. Base Connecting Lines ---
    # Center vertical axis
    add_line(slide, Inches(6.666), Inches(1.0), Inches(6.666), Inches(6.8), WHITE)
    # Left structure (Downwards)
    add_line(slide, Inches(6.666), Inches(2.5), Inches(3.5), Inches(2.5), WHITE) # Branch
    add_line(slide, Inches(3.5), Inches(2.5), Inches(3.5), Inches(4.5), WHITE)   # Tangent Drop
    # Right structure (Upwards)
    add_line(slide, Inches(6.666), Inches(5.5), Inches(9.833), Inches(5.5), WHITE) # Branch
    add_line(slide, Inches(9.833), Inches(5.5), Inches(9.833), Inches(3.5), WHITE) # Tangent Drop

    # --- 4. Central Axis Nodes ---
    top_node = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(6.066), Inches(1.9), Inches(1.2), Inches(1.2))
    top_node.fill.solid(); top_node.fill.fore_color.rgb = RED
    top_node.line.color.rgb = WHITE; top_node.line.width = Pt(3)
    format_badge_text(top_node, "★", WHITE, Pt(36))

    bot_node = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(6.066), Inches(4.9), Inches(1.2), Inches(1.2))
    bot_node.fill.solid(); bot_node.fill.fore_color.rgb = DARK
    bot_node.line.color.rgb = WHITE; bot_node.line.width = Pt(3)
    format_badge_text(bot_node, "★", WHITE, Pt(36))

    # --- 5. Image & Crescent Backdrops ---
    # Left Crescent Backdrop
    left_crescent = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.9), Inches(1.2), Inches(2.6), Inches(2.6))
    left_crescent.fill.solid(); left_crescent.fill.fore_color.rgb = WHITE
    left_crescent.line.fill.background()
    
    # Right Crescent Backdrop
    right_crescent = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9.833), Inches(4.2), Inches(2.6), Inches(2.6))
    right_crescent.fill.solid(); right_crescent.fill.fore_color.rgb = WHITE
    right_crescent.line.fill.background()

    # PIL Images
    img_left = make_circular_image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&q=80", "tmp_left.png")
    img_right = make_circular_image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&q=80", "tmp_right.png")
    
    # Offset the image insertion over the backdrop to create the thick crescent illusion
    slide.shapes.add_picture(img_left, Inches(0.9), Inches(1.4), Inches(2.2), Inches(2.2))
    slide.shapes.add_picture(img_right, Inches(10.233), Inches(4.4), Inches(2.2), Inches(2.2))

    # --- 6. Nodes & Text on Tangent Drop Lines ---
    # Left Tangent Nodes
    for y in [3.2, 3.85, 4.5]:
        node = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(3.42), Inches(y - 0.08), Inches(0.16), Inches(0.16))
        node.fill.solid(); node.fill.fore_color.rgb = RED
        node.line.color.rgb = WHITE; node.line.width = Pt(2)
        
        tx = slide.shapes.add_textbox(Inches(1.0), Inches(y - 0.15), Inches(2.3), Inches(0.3))
        p = tx.text_frame.paragraphs[0]
        p.text = "Add Your Own Points Here"; p.alignment = PP_ALIGN.RIGHT
        p.font.size = Pt(12); p.font.color.rgb = WHITE

    # Right Tangent Nodes
    for y in [4.8, 4.15, 3.5]:
        node = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9.753), Inches(y - 0.08), Inches(0.16), Inches(0.16))
        node.fill.solid(); node.fill.fore_color.rgb = DARK
        node.line.color.rgb = WHITE; node.line.width = Pt(2)
        
        tx = slide.shapes.add_textbox(Inches(10.033), Inches(y - 0.15), Inches(2.3), Inches(0.3))
        p = tx.text_frame.paragraphs[0]
        p.text = "Add Your Own Points Here"; p.alignment = PP_ALIGN.LEFT
        p.font.size = Pt(12); p.font.color.rgb = WHITE

    # --- 7. Badges ---
    # Top-right overlapping Left Image
    badge_01 = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(2.82), Inches(1.28), Inches(0.6), Inches(0.6))
    badge_01.fill.solid(); badge_01.fill.fore_color.rgb = WHITE; badge_01.line.fill.background()
    format_badge_text(badge_01, "01", RED, Pt(14))

    # Left Branch Title Badge
    badge_l_title = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.3), Inches(2.3), Inches(1.4), Inches(0.4))
    badge_l_title.fill.solid(); badge_l_title.fill.fore_color.rgb = WHITE; badge_l_title.line.fill.background()
    format_badge_text(badge_l_title, left_title, RED, Pt(12))

    # Bottom-left overlapping Right Image
    badge_02 = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9.91), Inches(6.12), Inches(0.6), Inches(0.6))
    badge_02.fill.solid(); badge_02.fill.fore_color.rgb = WHITE; badge_02.line.fill.background()
    format_badge_text(badge_02, "02", DARK, Pt(14))

    # Right Branch Title Badge
    badge_r_title = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.55), Inches(5.3), Inches(1.4), Inches(0.4))
    badge_r_title.fill.solid(); badge_r_title.fill.fore_color.rgb = WHITE; badge_r_title.line.fill.background()
    format_badge_text(badge_r_title, right_title, DARK, Pt(12))

    # Cleanup temporary images
    if os.path.exists("tmp_left.png"): os.remove("tmp_left.png")
    if os.path.exists("tmp_right.png"): os.remove("tmp_right.png")

    prs.save(output_pptx_path)
    return output_pptx_path
