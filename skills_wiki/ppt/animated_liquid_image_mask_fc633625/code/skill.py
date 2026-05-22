import os
import urllib.request
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.oxml.xmlchemy import OxmlElement

def create_slide(
    output_pptx_path: str,
    title_text: str = "LIQUID IMAGE MASK",
    body_text: str = "Insert some awesome text right here. Just remember keep it short and sweet.",
    image_url: str = "https://images.unsplash.com/photo-1519681393784-d120267933ba?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1770&q=80",
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with an animated 'Liquid Image Mask' effect.

    This function reproduces the effect of a morphing, rotating window that reveals a
    background image. It achieves this by programmatically creating a complex

    freeform shape (a rectangle with a hole) and then applying Spin and Grow/Shrink
    animations using lxml to inject the necessary Open XML.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        title_text: The main title text for the slide.
        body_text: The subtitle or body text for the slide.
        image_url: URL for the background image. A default is provided.

    Returns:
        The path to the saved .pptx file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Utility function for XML namespace ---
    def qn(tag):
        ns = {
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
            'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
        }
        prefix, tagroot = tag.split(':')
        return f'{{{ns[prefix]}}}{tagroot}'

    # === 1. Background Image ===
    try:
        image_path = "background_image.jpg"
        urllib.request.urlretrieve(image_url, image_path)
        slide.background.fill.solid() # First set to solid to clear any theme background
        slide.background.fill.picture(image_path)
    except Exception as e:
        print(f"Warning: Could not download image. Using solid background. Error: {e}")
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = RGBColor(10, 10, 30)


    # === 2. Create the Mask Shape (Rectangle with a hole) ===
    # This shape is a large rectangle with a custom "liquid" shape path subtracted from it.
    W, H = prs.slide_width, prs.slide_height
    
    # Define the outer rectangle (larger than the slide to hide edges during rotation)
    outer_rect_w, outer_rect_h = W * 2, H * 2
    outer_rect_l, outer_rect_t = (W - outer_rect_w) / 2, (H - outer_rect_h) / 2

    # Define the inner "liquid" shape's path using cubic Bezier curves
    # Coordinates are relative to the slide dimensions
    path_data = [
        ("M", (0.27 * W, 0.23 * H)),
        ("C", (0.13 * W, 0.40 * H), (0.22 * W, 0.78 * H), (0.35 * W, 0.82 * H)),
        ("C", (0.50 * W, 0.87 * H), (0.63 * W, 0.65 * H), (0.55 * W, 0.45 * H)),
        ("C", (0.48 * W, 0.25 * H), (0.40 * W, 0.12 * H), (0.27 * W, 0.23 * H)),
    ]

    # Build the freeform shape with a hole
    freeform = slide.shapes.add_freeform_shape(1, 1, 1, 1) # temp position
    with freeform.build_freeform() as builder:
        # Path 1: Outer rectangle
        builder.move_to(outer_rect_l, outer_rect_t)
        builder.add_line_segments([(outer_rect_l + outer_rect_w, outer_rect_t),
                                   (outer_rect_l + outer_rect_w, outer_rect_t + outer_rect_h),
                                   (outer_rect_l, outer_rect_t + outer_rect_h)],
                                  close=True)
        # Path 2: Inner liquid shape hole
        builder.move_to(path_data[0][1][0], path_data[0][1][1])
        for op, p1, p2, p3 in [ (d[0], d[1], d[2], d[3]) for _,(d) in zip(path_data, [(x[1], y[1], z[1]) for x,y,z in zip(path_data[1:], path_data[2:]+path_data[1:], path_data[3:]+path_data[1:])]) ]:
            if path_data.index((op, (p1, p2, p3))) < len(path_data) -1:
                 builder.add_cubic_bezier_curve_segment(path_data[path_data.index((op, (p1, p2, p3)))+1][1][0], path_data[path_data.index((op, (p1, p2, p3)))+1][1][1], p1[0],p1[1], p2[0],p2[1])

    # Set shape properties
    freeform.left, freeform.top, freeform.width, freeform.height = 0, 0, W, H
    fill = freeform.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)
    line = freeform.line
    line.fill.background()

    # === 3. Add Animations via LXML ===
    sp = freeform.element
    sp_id = sp.xpath('.//p:spPr/..')[0].get(qn("p:nvSpPr"), {})[qn("p:cNvPr")].get("id")

    # Get or create the timing element
    if not slide.has_timing:
        slide.get_or_add_timing()
    
    timing_elm = slide.element.xpath('.//p:timing')[0]
    tn_lst = timing_elm.xpath('.//p:tnLst')[0]
    par_elm = tn_lst.xpath('.//p:par')[0]
    
    # Create main parallel container for animations
    main_par = OxmlElement('p:par')
    par_elm.append(main_par)

    # Common child node for shape target
    shape_target = f'<p:cTn id="1" dur="indefinite" nodeType="mainSeq"><p:childTnLst><p:par><p:cTn id="2" dur="indefinite" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst><p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
    end_target = '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn>'

    # Animation 1: Spin
    spin_anim_xml = f'''
    <p:par>
        <p:cTn id="4" presetID="1" presetClass="entr" presetSubtype="0" fill="hold" nodeType="afterEffect">
            <p:stCondLst><p:cond delay="0"/></p:stCondLst>
            <p:childTnLst>
                <p:par>
                    <p:cTn id="5" fill="hold">
                        <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                        <p:childTnLst>
                            <p:set>
                                <p:cBhvr>
                                    <p:cTn id="6" dur="20000" repeatCount="indefinite"/>
                                    <p:tgtEl><p:spTgt spid="{sp_id}"/></p:tgtEl>
                                    <p:attrNameLst><p:attrName>ppt_x</p:attrName></p:attrNameLst>
                                </p:cBhvr>
                                <p:to><p:strVal val="1"/></p:to>
                            </p:set>
                            <p:anim calcmode="lin" valueType="num">
                                <p:cBhvr additive="base" xfrmType="rot">
                                    <p:cTn id="7" dur="20000" repeatCount="indefinite"/>
                                    <p:tgtEl><p:spTgt spid="{sp_id}"/></p:tgtEl>
                                    <p:attrNameLst><p:attrName>rotation</p:attrName></p:attrNameLst>
                                </p:cBhvr>
                                <p:tavLst>
                                    <p:tav tm="0"><p:val>0</p:val></p:tav>
                                    <p:tav tm="100000"><p:val>360000</p:val></p:tav>
                                </p:tavLst>
                            </p:anim>
                        </p:childTnLst>
                    </p:cTn>
                </p:par>
            </p:childTnLst>
        </p:cTn>
    </p:par>
    '''

    # Animation 2: Grow/Shrink
    grow_shrink_anim_xml = f'''
    <p:par>
      <p:cTn id="8" fill="hold">
        <p:stCondLst><p:cond delay="0" /></p:stCondLst>
        <p:childTnLst>
          <p:animScale autoReverse="1">
            <p:cBhvr>
              <p:cTn id="9" dur="5000" repeatCount="indefinite" />
              <p:tgtEl><p:spTgt spid="{sp_id}" /></p:tgtEl>
            </p:cBhvr>
            <p:by><p:xVal x="100000" /><p:yVal y="110000" /></p:by>
          </p:animScale>
        </p:childTnLst>
      </p:cTn>
    </p:par>
    '''
    
    full_anim_tree = etree.fromstring(shape_target + spin_anim_xml + grow_shrink_anim_xml + end_target)
    main_par.append(full_anim_tree)


    # === 4. Text Content ===
    title_box = slide.shapes.add_textbox(Inches(7), Inches(2.5), Inches(5.5), Inches(1.5))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = 'Raleway'
    p.font.bold = True
    p.font.size = Pt(44)
    p.font.color.rgb = RGBColor(30, 30, 30)

    body_box = slide.shapes.add_textbox(Inches(7), Inches(4.0), Inches(5), Inches(1))
    tf = body_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = body_text
    p.font.name = 'Raleway Light'
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(80, 80, 80)
    
    prs.save(output_pptx_path)
    if 'image_path' in locals() and os.path.exists(image_path):
        os.remove(image_path)
    return output_pptx_path

# Example usage:
# create_slide("liquid_mask_slide.pptx")
