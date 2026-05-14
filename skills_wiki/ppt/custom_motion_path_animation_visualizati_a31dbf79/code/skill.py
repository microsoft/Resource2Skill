def create_slide(
    output_pptx_path: str,
    title_text: str = "Custom Bouncing Motion Path",
    duration_ms: int = 3000,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Custom Motion Path Animation effect.
    
    Returns: path to the saved PPTX file.
    """
    import os
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from lxml import etree
    from PIL import Image, ImageDraw

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    # Using blank layout to manage z-order perfectly from bottom-up
    slide = prs.slides.add_slide(prs.slide_layouts[6])  
    
    # === Layer 1: Background ===
    bg_path = "temp_gradient_bg.png"
    img_bg = Image.new('RGBA', (1920, 1080))
    draw_bg = ImageDraw.Draw(img_bg)
    # Draw radial gradient (spotlight effect)
    for r in range(1200, 0, -20):
        ratio = r / 1200
        # Dark forest green to near black
        c = (
            int(34 * (1-ratio) + 10 * ratio),
            int(139 * (1-ratio) + 30 * ratio),
            int(34 * (1-ratio) + 10 * ratio),
            255
        )
        draw_bg.ellipse((960-r, 540-r, 960+r, 540+r), fill=c)
    img_bg.save(bg_path)
    slide.shapes.add_picture(bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
    
    # === Layer 2: Text Box ===
    tx_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12), Inches(1))
    tf = tx_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    # === Layer 3: Visual Path Construction ===
    w_inches = 13.333
    h_inches = 7.5
    start_x_inches = w_inches * 0.15
    start_y_inches = h_inches * 0.6
    
    # Relative path points for motion (x_rel, y_rel) - represents a double bounce
    # Note: in PPTX, +Y is downwards, -Y is upwards
    rel_pts = [
        (0.15, -0.30),  # Bounce Up & Right
        (0.30, 0.00),   # Fall Down & Right
        (0.45, 0.30),   # Fall Further Down & Right
        (0.60, 0.00)    # Bounce Back Up & Right
    ]
    
    # Draw dashed visualization line
    builder = slide.shapes.build_freeform(Inches(start_x_inches), Inches(start_y_inches))
    abs_pts = [(Inches(start_x_inches + x*w_inches), Inches(start_y_inches + y*h_inches)) for x, y in rel_pts]
    builder.add_line_segments(abs_pts, close=False)
    path_shape = builder.convert_to_shape()
    path_shape.line.color.rgb = RGBColor(200, 255, 200)
    path_shape.line.dash_style = 7  # MSO_LINE_DASH_STYLE.DASH
    path_shape.line.width = Pt(3)
    
    # === Layer 4: Procedural Object (Soccer Ball) ===
    ball_path = "temp_soccer_ball.png"
    b_size = 200
    b_img = Image.new('RGBA', (b_size, b_size), (0,0,0,0))
    b_draw = ImageDraw.Draw(b_img)
    # Drop shadow
    b_draw.ellipse((15, 20, 185, 190), fill=(0,0,0,100))
    # Main white sphere
    b_draw.ellipse((10, 10, 190, 190), fill=(255,255,255,255), outline=(0,0,0,255), width=5)
    # Hexagon pattern lines
    b_draw.polygon([(100, 45), (135, 75), (120, 120), (80, 120), (65, 75)], fill=(0,0,0,255))
    b_draw.line([(100,45), (100,10)], fill=(0,0,0,255), width=5)
    b_draw.line([(135,75), (185,65)], fill=(0,0,0,255), width=5)
    b_draw.line([(120,120), (155,175)], fill=(0,0,0,255), width=5)
    b_draw.line([(80,120), (45,175)], fill=(0,0,0,255), width=5)
    b_draw.line([(65,75), (15,65)], fill=(0,0,0,255), width=5)
    b_img.save(ball_path)
    
    # Insert object centered on the start coordinates
    ball_size = Inches(1.5)
    left = Inches(start_x_inches) - ball_size/2
    top = Inches(start_y_inches) - ball_size/2
    ball_pic = slide.shapes.add_picture(ball_path, left, top, width=ball_size, height=ball_size)
    
    # === Layer 5: Animation XML Injection ===
    # Convert points to PPTX SVG-like path string
    path_str = "M 0 0 "
    for x, y in rel_pts:
        path_str += f"L {x:.3f} {y:.3f} "
        
    nsmap = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
    
    # Root timing tree wrapper (safely injecting into a new slide)
    timing_xml = """
    <p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
        <p:tnLst>
            <p:par>
                <p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
                    <p:childTnLst>
                        <p:seq concurrent="1" nextAc="seek">
                            <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
                                <p:childTnLst>
                                    <p:par>
                                        <p:cTn id="3" fill="hold">
                                            <p:stCondLst>
                                                <p:cond delay="0"/>
                                            </p:stCondLst>
                                            <p:childTnLst/>
                                        </p:cTn>
                                    </p:par>
                                </p:childTnLst>
                            </p:cTn>
                        </p:seq>
                    </p:childTnLst>
                </p:cTn>
            </p:par>
        </p:tnLst>
    </p:timing>
    """
    slide.element.append(etree.fromstring(timing_xml))
    
    # Target the deepest child node
    target_lst = slide.element.xpath('.//p:seq/p:cTn/p:childTnLst/p:par/p:cTn/p:childTnLst', namespaces=nsmap)[0]
    
    # Inject actual motion path behavior targeting the ball picture ID
    anim_xml = f'''
    <p:par xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
        <p:cTn id="4" presetID="14" presetClass="path" presetSubtype="0" fill="hold" nodeType="withEffect">
            <p:stCondLst>
                <p:cond delay="0"/>
            </p:stCondLst>
            <p:childTnLst>
                <p:animMotion path="{path_str}" pathEditMode="relative" rAng="0">
                    <p:cBhvr>
                        <p:cTn id="5" dur="{duration_ms}" fill="hold"/>
                        <p:tgtEl>
                            <p:spTgt spid="{ball_pic.shape_id}"/>
                        </p:tgtEl>
                        <p:attrNameLst>
                            <p:attrName>ppt_x</p:attrName>
                            <p:attrName>ppt_y</p:attrName>
                        </p:attrNameLst>
                    </p:cBhvr>
                </p:animMotion>
            </p:childTnLst>
        </p:cTn>
    </p:par>
    '''
    target_lst.append(etree.fromstring(anim_xml))
    
    prs.save(output_pptx_path)
    
    # Cleanup temporary local assets
    if os.path.exists(bg_path): os.remove(bg_path)
    if os.path.exists(ball_path): os.remove(ball_path)
        
    return output_pptx_path
