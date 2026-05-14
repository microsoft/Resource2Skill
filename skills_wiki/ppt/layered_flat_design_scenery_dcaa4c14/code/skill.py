def create_slide(
    output_pptx_path: str,
    title_text: str = "如何用PPT繪圖設計?",
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with a layered flat design landscape illustration.

    This function reproduces the visual style from a tutorial, using python-pptx
    to generate and layer simple shapes, creating a cohesive and professional
    scenery illustration.

    Returns:
        str: The path to the saved PPTX file.
    """
    import math
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE
    from lxml import etree

    # --- Presentation and Slide Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # --- Color Palette ---
    BG_COLOR = RGBColor(0, 77, 64)
    HILL_DARK = RGBColor(85, 139, 47)
    HILL_MEDIUM = RGBColor(156, 204, 101)
    HILL_LIGHT = RGBColor(185, 228, 168)
    TREE_CANOPY_LIGHT = RGBColor(185, 228, 168)
    TREE_CANOPY_DARK = RGBColor(156, 204, 101)
    TREE_TRUNK = RGBColor(85, 139, 47)
    WATER_MAIN = RGBColor(129, 212, 250)
    WATER_ACCENT = RGBColor(225, 245, 254)
    HOUSE_BODY = RGBColor(255, 204, 188)
    HOUSE_ROOF = RGBColor(191, 54, 12)
    CLOUD_COLOR = RGBColor(255, 255, 255)
    
    # --- Layer 1: Background ---
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

    # --- Helper Functions for Creating Elements ---
    def create_element(shape_type, left, top, width, height, color, line_color=None, transparency=0.0):
        shape = slide.shapes.add_shape(shape_type, Inches(left), Inches(top), Inches(width), Inches(height))
        fill = shape.fill
        fill.solid()
        fill.fore_color.rgb = color
        if transparency > 0:
            fill.transparency = transparency
        
        line = shape.line
        if line_color:
            line.fill.solid()
            line.fill.fore_color.rgb = line_color
        else:
            line.fill.background() # No line
        return shape

    def create_hill(left, top, width, height, color):
        # Use a pie shape to create a semi-circle for the hill
        hill = create_element(MSO_SHAPE.PIE, left, top, width, height * 2, color)
        hill.adjustments[0] = 10800000  # Start angle 180 deg
        hill.adjustments[1] = 10800000  # Extent 180 deg
        return hill

    def create_tree(left, top, width, color1, color2, trunk_color):
        height = width * 2 # Maintain aspect ratio
        trunk_w, trunk_h = width * 0.2, height * 0.5
        canopy_h = height * 0.6
        
        # Trunk
        create_element(MSO_SHAPE.RECTANGLE, left + (width - trunk_w) / 2, top + canopy_h, trunk_w, trunk_h, trunk_color)
        
        # Canopy (as two halves to mimic shadow)
        create_element(MSO_SHAPE.TEARDROP, left, top, width / 2, canopy_h, color1).rotation = 90
        create_element(MSO_SHAPE.TEARDROP, left + width / 2, top, width / 2, canopy_h, color2).rotation = 90

    # --- Layer 2: Scene Composition (from back to front) ---
    # Far back hill
    create_hill(5.5, 3.5, 3.5, 1.7, HILL_DARK)
    
    # House
    house_l, house_t, house_w, house_h = 7.0, 3.2, 0.7, 0.8
    house_body = create_element(MSO_SHAPE.RECTANGLE, house_l, house_t + 0.2, house_w, house_h-0.2, HOUSE_BODY, line_color=HOUSE_ROOF)
    house_roof = create_element(MSO_SHAPE.TRAPEZOID, house_l-0.1, house_t, house_w+0.2, 0.3, HOUSE_ROOF)
    house_roof.rotation = 180
    
    # Smoke from chimney
    smoke1 = create_element(MSO_SHAPE.OVAL, 6.7, 3.0, 0.4, 0.4, CLOUD_COLOR)
    smoke2 = create_element(MSO_SHAPE.OVAL, 6.6, 2.9, 0.2, 0.2, CLOUD_COLOR)
    smoke3 = create_element(MSO_SHAPE.OVAL, 6.5, 2.95, 0.1, 0.1, CLOUD_COLOR)

    # Mid-ground hills
    create_hill(1.5, 4.0, 3.0, 1.5, HILL_MEDIUM)
    create_hill(8.5, 4.2, 2.5, 1.2, HILL_MEDIUM)
    
    # Main foreground hill
    create_hill(3.5, 3.8, 5.0, 2.5, HILL_LIGHT)

    # Trees (place them on their respective hills)
    create_tree(2.0, 3.5, 0.5, TREE_CANOPY_LIGHT, TREE_CANOPY_DARK, TREE_TRUNK)
    create_tree(3.0, 3.8, 0.3, TREE_CANOPY_LIGHT, TREE_CANOPY_DARK, TREE_TRUNK)
    create_tree(4.5, 3.5, 0.4, TREE_CANOPY_LIGHT, TREE_CANOPY_DARK, TREE_TRUNK)
    create_tree(9.0, 3.8, 0.4, TREE_CANOPY_LIGHT, TREE_CANOPY_DARK, TREE_TRUNK)
    create_tree(5.5, 4.5, 0.2, TREE_CANOPY_LIGHT, TREE_CANOPY_DARK, TREE_TRUNK)
    create_tree(6.5, 4.8, 0.2, TREE_CANOPY_LIGHT, TREE_CANOPY_DARK, TREE_TRUNK)
    create_tree(7.8, 4.9, 0.2, TREE_CANOPY_LIGHT, TREE_CANOPY_DARK, TREE_TRUNK)

    # --- Layer 3: Foreground and Sky ---
    # Water
    water = create_element(MSO_SHAPE.ROUNDED_RECTANGLE, 0, 5.8, 13.333, 1.7, WATER_MAIN)
    water.adjustments[0] = 0.1
    wave1 = create_element(MSO_SHAPE.ROUNDED_RECTANGLE, 0.5, 6.5, 2.0, 0.8, WATER_ACCENT)
    wave1.adjustments[0] = 1.0
    wave2 = create_element(MSO_SHAPE.ROUNDED_RECTANGLE, 10.5, 6.4, 2.5, 0.9, WATER_ACCENT)
    wave2.adjustments[0] = 1.0

    # Clouds & Light Beams (created last to be on top initially)
    cloud1_base = create_element(MSO_SHAPE.ROUNDED_RECTANGLE, 1.5, 1.0, 3.0, 1.0, CLOUD_COLOR)
    cloud1_base.adjustments[0] = 1.0
    create_element(MSO_SHAPE.OVAL, 2.0, 0.7, 1.5, 1.5, CLOUD_COLOR)

    cloud2_base = create_element(MSO_SHAPE.ROUNDED_RECTANGLE, 9.5, 1.2, 2.5, 0.8, CLOUD_COLOR)
    cloud2_base.adjustments[0] = 1.0
    create_element(MSO_SHAPE.OVAL, 10.0, 0.9, 1.2, 1.2, CLOUD_COLOR)

    beam1 = create_element(MSO_SHAPE.TRAPEZOID, 2.0, 1.5, 2.0, 5.0, CLOUD_COLOR, transparency=0.9)
    beam1.rotation=180; beam1.adjustments[0]=0.7
    beam2 = create_element(MSO_SHAPE.TRAPEZOID, 10.0, 1.5, 1.5, 5.0, CLOUD_COLOR, transparency=0.9)
    beam2.rotation=180; beam2.adjustments[0]=0.8

    # --- Layer Re-ordering via LXML ---
    # Move clouds and beams to the back (bottom of the spTree)
    spTree = slide.shapes._spTree
    elements_to_move_back = [cloud1_base, cloud2_base, beam1, beam2]
    
    # Get all shape elements that need to be moved
    xml_elements = [s.element for s in slide.shapes if s in elements_to_move_back]
    
    # Re-insert them at the beginning of the shape tree
    for elem in reversed(xml_elements):
        spTree.insert(0, elem)

    # --- Add Title from the opening shot of the video ---
    textbox = slide.shapes.add_textbox(Inches(5.0), Inches(2.5), Inches(8), Inches(2))
    text_frame = textbox.text_frame
    text_frame.clear() 
    text_frame.word_wrap = True
    p = text_frame.paragraphs[0]
    run = p.add_run()
    run.text = title_text
    font = run.font
    font.name = 'Microsoft JhengHei UI'
    font.size = Pt(66)
    font.bold = True
    font.color.rgb = RGBColor(255, 255, 255)

    prs.save(output_pptx_path)
    return output_pptx_path
