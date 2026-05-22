import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml

def create_slide(
    output_pptx_path: str,
    title_text: str = "System Architecture Ecosystem",
    base_color_rgb: tuple = (44, 102, 104),  # The elegant teal from the video
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Monochromatic Hierarchical Architecture Diagram.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank slide

    # Helper: Color Tint Calculator (Mixes base color with white to simulate opacity/tints)
    def tint_color(base_rgb, factor):
        # factor: 0.0 = white, 1.0 = base_color
        r = int(255 + (base_rgb[0] - 255) * factor)
        g = int(255 + (base_rgb[1] - 255) * factor)
        b = int(255 + (base_rgb[2] - 255) * factor)
        return RGBColor(r, g, b)

    # Define Theme Colors based on the base color
    C_DARK = tint_color(base_color_rgb, 1.0)    # Level 1
    C_MED = tint_color(base_color_rgb, 0.65)    # Level 2
    C_LIGHT = tint_color(base_color_rgb, 0.35)   # Level 3
    C_BG = tint_color(base_color_rgb, 0.08)     # Level 4 Container BG

    # Add Main Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(0.8))
    tf = title_box.text_frame
    p = tf.add_paragraph()
    p.text = title_text
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    # Helper: Add Styled Rounded Rectangle
    def add_rounded_rect(left, top, width, height, text, level, is_container=False):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        
        # Adjust corner radius via XML (make it more pill-like / modern)
        adj_val = "10000" if is_container else "25000" # Smaller radius for large containers, larger for nodes
        xml = f'<a:avLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:gd name="adj" fmla="val {adj_val}"/></a:avLst>'
        shape.element.spPr.insert(1, parse_xml(xml))

        # Apply Color Logic based on hierarchical level
        if level == 1:
            shape.fill.solid()
            shape.fill.fore_color.rgb = C_DARK
            shape.line.fill.background()
            font_color = RGBColor(255, 255, 255)
        elif level == 2:
            shape.fill.solid()
            shape.fill.fore_color.rgb = C_MED
            shape.line.fill.background()
            font_color = RGBColor(255, 255, 255)
        elif level == 3:
            shape.fill.solid()
            shape.fill.fore_color.rgb = C_LIGHT
            shape.line.fill.background()
            font_color = RGBColor(40, 40, 40)
        elif level == 4: # Container
            shape.fill.solid()
            shape.fill.fore_color.rgb = C_BG
            shape.line.color.rgb = C_DARK
            shape.line.width = Pt(1.5)
            font_color = C_DARK
        
        # Configure Text
        tf = shape.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(16) if is_container else Pt(14)
        p.font.bold = is_container or level == 1
        p.font.color.rgb = font_color
        
        if is_container:
            # Align top left for containers
            tf.vertical_anchor = 1 # Top
            p.alignment = PP_ALIGN.LEFT
            tf.margin_top = Inches(0.15)
            tf.margin_left = Inches(0.2)
        else:
            # Center for nodes
            p.alignment = PP_ALIGN.CENTER
            
        return shape

    # --- Build the Architecture Layout ---
    
    # 1. Top Layer: Client Apps (Level 1)
    y_top = Inches(1.2)
    node_w, node_h = Inches(2.5), Inches(0.6)
    spacing = Inches(0.4)
    start_x = Inches(2.25)
    
    apps = ["Mobile App", "Web Portal", "Open API"]
    top_nodes = []
    for i, app in enumerate(apps):
        x = start_x + (i * (node_w + spacing))
        node = add_rounded_rect(x, y_top, node_w, node_h, app, level=1)
        top_nodes.append(node)

    # 2. Middle Layer: Business Middle-End (Container + Level 2 nodes)
    y_mid_container = Inches(2.4)
    cont_w, cont_h = Inches(11.3), Inches(2.2)
    cont_x = Inches(1.0)
    
    mid_container = add_rounded_rect(cont_x, y_mid_container, cont_w, cont_h, "Business & Data Platform", level=4, is_container=True)
    
    # Inner nodes for Middle Layer
    y_mid_node = y_mid_container + Inches(0.6)
    mid_modules = [
        ("User Center", 1), ("Payment Gateway", 1), ("Order System", 1), ("Data Analytics", 2)
    ]
    
    start_inner_x = cont_x + Inches(0.5)
    inner_spacing = Inches(0.25)
    for i, (mod, span) in enumerate(mid_modules):
        # Calculate width dynamically based on 'span' just to make it interesting
        w = (node_w * span) + (inner_spacing * (span-1))
        # Find exact x based on previous items
        current_x = start_inner_x + sum([(node_w * m[1]) + inner_spacing * m[1] for m in mid_modules[:i]])
        
        # Sub-container (Level 3)
        sub_cont = add_rounded_rect(current_x, y_mid_node, w, Inches(1.4), mod, level=3, is_container=True)
        
        # Mini feature nodes inside sub-container (Level 2)
        add_rounded_rect(current_x + Inches(0.2), y_mid_node + Inches(0.5), w - Inches(0.4), Inches(0.4), f"{mod.split()[0]} API", level=2)

    # 3. Bottom Layer: Cloud Infrastructure (Container + Level 1 nodes)
    y_bot_container = Inches(5.0)
    bot_container = add_rounded_rect(cont_x, y_bot_container, cont_w, Inches(1.8), "Cloud Infrastructure & Security", level=4, is_container=True)
    
    y_bot_node = y_bot_container + Inches(0.6)
    bot_modules = ["Compute (EC2)", "Database (RDS)", "Object Storage", "Security WAF"]
    for i, mod in enumerate(bot_modules):
        x = start_inner_x + (i * (node_w + inner_spacing))
        add_rounded_rect(x, y_bot_node, node_w, Inches(0.8), mod, level=1)

    # --- Add Curved Connectors (As recommended in the tutorial) ---
    # Connect "Web Portal" (top_nodes[1]) to "Business & Data Platform" (mid_container)
    connector = slide.shapes.add_connector(
        MSO_CONNECTOR.CURVE, 
        Inches(6.66), Inches(1.8),  # Bottom center of middle top node
        Inches(6.66), Inches(2.4)   # Top center of middle container
    )
    connector.line.color.rgb = C_MED
    connector.line.width = Pt(2)
    
    # Save the presentation
    prs.save(output_pptx_path)
    return output_pptx_path
