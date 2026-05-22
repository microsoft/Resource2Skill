def create_slide(
    output_pptx_path: str,
    stroke_color: tuple = (0, 191, 255),  # Cyan strokes
    bg_color: tuple = (20, 20, 20),       # Dark background
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Sequential Stroke-by-Stroke Wipe Reveal" effect.
    The script builds geometric letters out of individual shapes and uses lxml to 
    inject standard PowerPoint sequential wipe animations based on writing direction.
    """
    from pptx import Presentation
    from pptx.util import Inches
    from pptx.dml.color import RGBColor
    from lxml import etree

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # 1. Set Background Color
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # 2. Define Strokes for a sample word ("HI")
    # Each stroke has (x, y, width, height, wipe_direction_subtype)
    # Wipe Subtypes in PPTX XML: 0=From Bottom, 1=From Left, 2=From Right, 3=From Top
    strokes_data = [
        # --- Letter 'H' ---
        # Left stem (Top to Bottom -> 3)
        (Inches(4.5), Inches(2.5), Inches(0.4), Inches(2.5), 3),
        # Crossbar (Left to Right -> 1)
        (Inches(4.9), Inches(3.55), Inches(1.2), Inches(0.4), 1),
        # Right stem (Top to Bottom -> 3)
        (Inches(6.1), Inches(2.5), Inches(0.4), Inches(2.5), 3),
        
        # --- Letter 'I' ---
        # Top bar (Left to Right -> 1)
        (Inches(7.2), Inches(2.5), Inches(1.2), Inches(0.4), 1),
        # Middle stem (Top to Bottom -> 3)
        (Inches(7.6), Inches(2.9), Inches(0.4), Inches(1.7), 3),
        # Bottom bar (Left to Right -> 1)
        (Inches(7.2), Inches(4.6), Inches(1.2), Inches(0.4), 1),
    ]

    shape_anim_info = []

    # 3. Draw Shapes and Capture IDs
    for (x, y, w, h, subtype) in strokes_data:
        shape = slide.shapes.add_shape(
            1, # MSO_SHAPE.RECTANGLE
            x, y, w, h
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*stroke_color)
        shape.line.fill.background() # No outline so shapes blend seamlessly
        
        shape_anim_info.append({
            "id": shape.shape_id,
            "subtype": subtype
        })

    # 4. Inject Sequential Animation XML using lxml
    # This builds the exact timing node structure PowerPoint requires.
    timing_ns = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
    
    # Base timing structure
    timing_xml = """
    <p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
        <p:tnLst>
            <p:par>
                <p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
                    <p:childTnLst>
                        <p:seq concurrent="1" nextAc="seek">
                            <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
                                <p:childTnLst>
                                </p:childTnLst>
                            </p:cTn>
                        </p:seq>
                    </p:childTnLst>
                </p:cTn>
            </p:par>
        </p:tnLst>
    </p:timing>
    """
    
    timing_tree = etree.fromstring(timing_xml.encode('utf-8'))
    child_tn_lst = timing_tree.xpath(".//p:seq/p:cTn/p:childTnLst", namespaces=timing_ns)[0]

    node_id_counter = 3
    
    for i, info in enumerate(shape_anim_info):
        spid = info["id"]
        subtype = info["subtype"]
        
        # The first shape starts "On Click" (clickEffect), others start "After Previous" (afterEffect)
        node_type = "clickEffect" if i == 0 else "afterEffect"
        
        # XML for a standard entrance Wipe effect
        anim_node_xml = f"""
        <p:par xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
            <p:cTn id="{node_id_counter}" presetID="22" presetClass="entr" presetSubtype="{subtype}" fill="hold" nodeType="{node_type}">
                <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                <p:childTnLst>
                    <p:animEffect transition="in" filter="wipe">
                        <p:cBhvr>
                            <p:cTn id="{node_id_counter+1}" dur="250"/>
                            <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>
                        </p:cBhvr>
                    </p:animEffect>
                </p:childTnLst>
            </p:cTn>
        </p:par>
        """
        node_id_counter += 2
        
        anim_element = etree.fromstring(anim_node_xml.encode('utf-8'))
        child_tn_lst.append(anim_element)

    # Append the timing tree to the slide's XML
    slide.element.append(timing_tree)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("stroke_reveal_animation.pptx")
