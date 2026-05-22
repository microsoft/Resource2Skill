def create_slide(
    output_pptx_path: str,
    title_text: str = "SUBSCRIBE",
    left_banner_text: str = "L A T E S T",
    right_banner_text: str = "P O P U L A R",
    accent_color: tuple = (163, 15, 35),  # Deep Crimson
    dark_color: tuple = (22, 22, 24),     # Charcoal/Off-Black
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Dynamic Split-Diagonal End Card visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.enum.shapes import MSO_SHAPE
    from lxml import etree

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Convert tuples to RGBColor
    COLOR_ACCENT = RGBColor(*accent_color)
    COLOR_DARK = RGBColor(*dark_color)
    COLOR_BG = RGBColor(245, 245, 247)
    COLOR_WHITE = RGBColor(255, 255, 255)

    # Helper: Add Text Box
    def add_text(left, top, width, height, text, size, bold=False, color=COLOR_DARK, align=PP_ALIGN.CENTER):
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = text
        p.alignment = align
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = color
        p.font.name = "Arial"
        return txBox

    # Helper: Inject Native Shadow
    def apply_shadow(shape):
        spPr = shape.element.spPr
        effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
        outerShdw = etree.SubElement(effectLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw')
        outerShdw.set('blurRad', '150000')  # Blur radius
        outerShdw.set('dist', '40000')      # Distance
        outerShdw.set('dir', '2700000')     # Angle (bottom)
        srgbClr = etree.SubElement(outerShdw, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
        srgbClr.set('val', '000000')
        alpha = etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha')
        alpha.set('val', '25000')           # 25% opacity

    # === Layer 1: Background ===
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_BG
    bg.line.fill.background()

    # === Layer 2: Diagonal Structural Banners (V-Shape framing) ===
    # Left Banner (slopes inward to the right)
    points_left = [(Inches(1.5), 0), (Inches(2.8), 0), (Inches(4.3), Inches(7.5)), (Inches(3.0), Inches(7.5))]
    builder_l = slide.shapes.build_freeform()
    builder_l.add_line_segments(points_left, close=True)
    shape_left = builder_l.convert_to_shape()
    shape_left.fill.solid(); shape_left.fill.fore_color.rgb = COLOR_ACCENT
    shape_left.line.fill.background()

    # Right Banner (slopes inward to the left)
    points_right = [(Inches(10.53), 0), (Inches(11.83), 0), (Inches(10.33), Inches(7.5)), (Inches(9.03), Inches(7.5))]
    builder_r = slide.shapes.build_freeform()
    builder_r.add_line_segments(points_right, close=True)
    shape_right = builder_r.convert_to_shape()
    shape_right.fill.solid(); shape_right.fill.fore_color.rgb = COLOR_ACCENT
    shape_right.line.fill.background()

    # === Layer 3: Placeholders with Flat Accent Shadows ===
    # Left Content Block
    s1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(2.9), Inches(3.6), Inches(2.2))
    s1.fill.solid(); s1.fill.fore_color.rgb = COLOR_ACCENT; s1.line.fill.background()
    m1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(2.8), Inches(3.6), Inches(2.2))
    m1.fill.solid(); m1.fill.fore_color.rgb = COLOR_DARK; m1.line.fill.background()
    add_text(Inches(0.5), Inches(3.65), Inches(3.6), Inches(0.5), "Video / Content", 18, color=COLOR_WHITE)

    # Right Content Block
    s2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.33), Inches(2.9), Inches(3.6), Inches(2.2))
    s2.fill.solid(); s2.fill.fore_color.rgb = COLOR_ACCENT; s2.line.fill.background()
    m2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.23), Inches(2.8), Inches(3.6), Inches(2.2))
    m2.fill.solid(); m2.fill.fore_color.rgb = COLOR_DARK; m2.line.fill.background()
    add_text(Inches(9.23), Inches(3.65), Inches(3.6), Inches(0.5), "Video / Content", 18, color=COLOR_WHITE)

    # === Layer 4: Central Floating Anchor ===
    # Outer accent ring
    ring = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(5.66), Inches(2.75), Inches(2.0), Inches(2.0))
    ring.fill.solid(); ring.fill.fore_color.rgb = COLOR_ACCENT; ring.line.fill.background()
    apply_shadow(ring)
    # Inner white circle (creating a logo/profile placeholder)
    inner = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(5.81), Inches(2.90), Inches(1.7), Inches(1.7))
    inner.fill.solid(); inner.fill.fore_color.rgb = COLOR_WHITE; inner.line.fill.background()

    # === Layer 5: Typography & Decals ===
    # Hero Title
    add_text(Inches(3.66), Inches(0.8), Inches(6.0), Inches(1.0), title_text.upper(), 44, bold=True, color=COLOR_ACCENT)

    # Vertical Banner Texts
    # Center points geometrically calculated to sit perfectly inside the sloping pillars
    tb1 = add_text(Inches(1.15), Inches(5.0), Inches(4.0), Inches(0.5), left_banner_text, 24, bold=True, color=COLOR_WHITE)
    tb1.rotation = -90.0

    tb2 = add_text(Inches(8.18), Inches(5.0), Inches(4.0), Inches(0.5), right_banner_text, 24, bold=True, color=COLOR_WHITE)
    tb2.rotation = 90.0

    # Socials / Footer links
    add_text(Inches(4.66), Inches(5.2), Inches(4.0), Inches(0.5), "@your_handle_here", 14, color=RGBColor(80,80,80))
    add_text(Inches(4.66), Inches(5.5), Inches(4.0), Inches(0.5), "website.com/link", 14, color=RGBColor(80,80,80))

    prs.save(output_pptx_path)
    return output_pptx_path
