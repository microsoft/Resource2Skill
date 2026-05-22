def create_slide(
    output_pptx_path: str,
    title_text: str = "Corporate Organizational Architecture",
    **kwargs,
) -> str:
    """
    Creates a presentation with an aesthetic, color-coded hierarchical architecture chart.
    Replicates the visual styling of customized SmartArt (rounded shapes, branch colors).
    """
    from pptx import Presentation
    from pptx.util import Pt, Inches
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.shapes import MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Slide Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 247, 250) # Very light cool grey

    # === Add Title ===
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(40, 50, 60)

    # === Define Architecture Data & Color Palette ===
    # Colors for different branches: Navy, Coral, Sage, Gold
    palettes = [
        {"main": RGBColor(38, 115, 129), "sub": RGBColor(94, 160, 172)},
        {"main": RGBColor(200, 85, 80),  "sub": RGBColor(226, 133, 126)},
        {"main": RGBColor(105, 142, 115), "sub": RGBColor(149, 182, 158)},
        {"main": RGBColor(196, 143, 73),  "sub": RGBColor(222, 180, 124)},
    ]

    # Data structure: Root -> Branches -> Leaves
    root_node = "Board of Directors"
    branches = [
        {"name": "Marketing Dept", "children": ["Digital Marketing", "Brand Strategy", "PR & Events"]},
        {"name": "Operations Dept", "children": ["Supply Chain", "Logistics", "Customer Success"]},
        {"name": "Finance Dept", "children": ["Accounting", "Investment", "Audit"]},
        {"name": "Tech & Dev", "children": ["Frontend", "Backend", "Data Science"]}
    ]

    # === Layout Mathematics ===
    node_w = Inches(1.8)
    node_h = Inches(0.6)
    
    y_root = Inches(1.5)
    y_branch = Inches(3.0)
    y_leaf_start = Inches(4.2)
    leaf_y_gap = Inches(0.8)

    center_x = prs.slide_width / 2

    # A dictionary to store absolute coordinates of nodes to draw lines later
    coords = {}

    def style_node(shape, color_rgb, font_size=14, is_bold=False):
        """Helper to style the shape as an elegant rounded rectangle"""
        shape.fill.solid()
        shape.fill.fore_color.rgb = color_rgb
        shape.line.fill.background() # No border
        
        # Adjust corner radius to be elegant (0.0 to 1.0)
        if len(shape.adjustments) > 0:
            shape.adjustments[0] = 0.25 
            
        tf = shape.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(font_size)
        p.font.bold = is_bold
        p.font.color.rgb = RGBColor(255, 255, 255)

    def draw_line(x1, y1, x2, y2):
        """Draws a subtle connecting line"""
        connector = slide.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2
        )
        connector.line.color.rgb = RGBColor(180, 180, 180)
        connector.line.width = Pt(1.5)
        # Send line to back (XML manipulation)
        slide.shapes._spTree.insert(2, connector._element) # Insert right after bg/title

    # --- Draw Root Node ---
    root_x = center_x - (node_w / 2)
    root_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, root_x, y_root, node_w, node_h)
    root_shape.text = root_node
    style_node(root_shape, RGBColor(50, 60, 75), font_size=16, is_bold=True)
    coords['root'] = (center_x, y_root + node_h) # bottom center

    # --- Draw Branches and Leaves ---
    num_branches = len(branches)
    total_width = prs.slide_width - Inches(1.0) # Leave 0.5 inch margins
    branch_spacing = total_width / num_branches
    start_x = Inches(0.5) + (branch_spacing / 2)

    for i, branch in enumerate(branches):
        palette = palettes[i % len(palettes)]
        
        # Branch Node
        b_cx = start_x + (i * branch_spacing)
        b_x = b_cx - (node_w / 2)
        
        b_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, b_x, y_branch, node_w, node_h)
        b_shape.text = branch["name"]
        style_node(b_shape, palette["main"], font_size=14, is_bold=True)
        
        # Line from Root to Branch
        draw_line(coords['root'][0], coords['root'][1], b_cx, y_branch)
        
        b_bottom_y = y_branch + node_h

        # Leaf Nodes
        for j, leaf in enumerate(branch["children"]):
            l_y = y_leaf_start + (j * leaf_y_gap)
            l_x = b_x
            
            l_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l_x, l_y, node_w, node_h)
            l_shape.text = leaf
            style_node(l_shape, palette["sub"], font_size=12, is_bold=False)
            
            # Line from parent (or previous leaf) to this leaf
            parent_y = b_bottom_y if j == 0 else y_leaf_start + ((j-1) * leaf_y_gap) + node_h
            draw_line(b_cx, parent_y, b_cx, l_y)

    prs.save(output_pptx_path)
    return output_pptx_path
