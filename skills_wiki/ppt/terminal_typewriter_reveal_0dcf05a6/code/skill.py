import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    title_text: str = "SYSTEM INITIALIZATION",
    body_text: str = "Loading core modules...\nAccessing secure server...\nDecrypting mainframe... SUCCESS.\nWelcome, admin.",
    bg_palette: str = "technology",  
    accent_color: tuple = (39, 201, 63), # Terminal Green
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Terminal Typewriter Reveal effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Background Gradient ===
    bg_path = "temp_gradient_bg.png"
    width_px, height_px = 1280, 720
    img = Image.new("RGB", (width_px, height_px))
    draw = ImageDraw.Draw(img)
    
    # Draw a smooth vertical dark gradient
    c1, c2 = (15, 20, 30), (5, 5, 8)
    for y in range(height_px):
        r = int(c1[0] + (c2[0] - c1[0]) * y / height_px)
        g = int(c1[1] + (c2[1] - c1[1]) * y / height_px)
        b = int(c1[2] + (c2[2] - c1[2]) * y / height_px)
        draw.line([(0, y), (width_px, y)], fill=(r, g, b))
    img.save(bg_path)
    
    # Insert background
    slide.shapes.add_picture(bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # === Layer 2: Terminal UI Container ===
    term_w = Inches(10)
    term_h = Inches(5.5)
    term_l = (prs.slide_width - term_w) / 2
    term_t = (prs.slide_height - term_h) / 2
    
    # Main Terminal Window
    term_bg = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, term_l, term_t, term_w, term_h
    )
    term_bg.fill.solid()
    term_bg.fill.fore_color.rgb = RGBColor(25, 28, 35)
    term_bg.line.color.rgb = RGBColor(60, 64, 70)
    term_bg.line.width = Pt(1)
    
    # Title bar separator
    bar_h = Inches(0.4)
    sep = slide.shapes.add_shape(
        MSO_SHAPE.LINE, term_l, term_t + bar_h, term_w, 0
    )
    sep.line.color.rgb = RGBColor(60, 64, 70)
    sep.line.width = Pt(1)
    
    # Window Control Buttons
    btn_colors = [(255, 95, 86), (255, 189, 46), (39, 201, 63)]
    for i, color in enumerate(btn_colors):
        btn = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, term_l + Inches(0.15 + i * 0.25), term_t + Inches(0.12), Inches(0.15), Inches(0.15)
        )
        btn.fill.solid()
        btn.fill.fore_color.rgb = RGBColor(*color)
        btn.line.fill.background()

    # Title Bar Text
    title_box = slide.shapes.add_textbox(term_l, term_t, term_w, bar_h)
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "admin@system:~"
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Consolas"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(120, 125, 135)

    # === Layer 3: Text Content & Animation Logic ===
    # Set up Content Box
    txt_l = term_l + Inches(0.4)
    txt_t = term_t + Inches(0.6)
    txt_w = term_w - Inches(0.8)
    txt_h = term_h - Inches(0.8)
    
    content_box = slide.shapes.add_textbox(txt_l, txt_t, txt_w, txt_h)
    content_box.text_frame.word_wrap = True
    
    # Trick: Convert newlines (\n) to soft line breaks (\x0b)
    # This forces PowerPoint to treat it as a single paragraph, guaranteeing seamless A-Z animation over the entire block.
    soft_break_body = body_text.replace('\n', '\x0b')
    full_text = f"> {title_text}\x0b> \x0b{soft_break_body}\x0b> \u2588"
    
    p = content_box.text_frame.paragraphs[0]
    p.text = full_text
    for run in p.runs:
        run.font.name = "Consolas"
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(*accent_color)
    
    shape_id = content_box.shape_id

    # Construct the Typewriter XML Injection Block
    # 500ms startup delay, 30ms absolute delay per character typed.
    timing_xml_str = f"""
    <p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
      <p:bldLst>
        <p:bldP spid="{shape_id}" grpId="0" animBg="0"/>
      </p:bldLst>
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
                        <p:childTnLst>
                          <p:par>
                            <p:cTn id="4" fill="hold">
                              <p:stCondLst>
                                <p:cond delay="0"/>
                              </p:stCondLst>
                              <p:childTnLst>
                                <p:par>
                                  <p:cTn id="5" presetID="1" presetClass="entr" presetSubtype="0" fill="hold" grpId="0" nodeType="withEffect">
                                    <p:stCondLst>
                                      <p:cond delay="500"/>
                                    </p:stCondLst>
                                    <p:childTnLst>
                                      <p:set>
                                        <p:cBhvr>
                                          <p:cTn id="6" dur="1" fill="hold">
                                            <p:stCondLst>
                                              <p:cond delay="0"/>
                                            </p:stCondLst>
                                            <p:iter type="el">
                                              <p:tmAbs val="30"/> 
                                            </p:iter>
                                          </p:cTn>
                                          <p:tgtEl>
                                            <p:spTgt spid="{shape_id}">
                                              <p:txEl>
                                                <p:pRg st="0" end="0"/>
                                              </p:txEl>
                                            </p:spTgt>
                                          </p:tgtEl>
                                          <p:attrNameLst>
                                            <p:attrName>style.visibility</p:attrName>
                                          </p:attrNameLst>
                                        </p:cBhvr>
                                        <p:to>
                                          <p:strVal val="visible"/>
                                        </p:to>
                                      </p:set>
                                    </p:childTnLst>
                                  </p:cTn>
                                </p:par>
                              </p:childTnLst>
                            </p:cTn>
                          </p:par>
                        </p:childTnLst>
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
    
    timing_element = parse_xml(timing_xml_str)
    
    # Safely insert the generated animation timing into the slide XML hierarchy
    # OOXML schema requires <p:timing> to appear exactly before <p:extLst> if it exists
    extLst = slide.element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}extLst')
    if extLst is not None:
        extLst.addprevious(timing_element)
    else:
        slide.element.append(timing_element)

    # Cleanup temporary image file
    if os.path.exists(bg_path):
        os.remove(bg_path)

    prs.save(output_pptx_path)
    return output_pptx_path
