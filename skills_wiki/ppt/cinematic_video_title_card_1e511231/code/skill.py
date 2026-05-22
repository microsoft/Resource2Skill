import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from lxml import etree

def create_cinematic_closing_slide(
    output_pptx_path: str,
    video_path: str,
    line1_text: str = "道阻且长",
    line2_text: str = "行则将至",
    font_name: str = "KaiTi", # A common Chinese calligraphy font, change if needed
    **kwargs,
) -> str:
    """
    Creates a PPTX file with a cinematic closing slide featuring a background video
    and animated calligraphic text.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        video_path: Local path to the background video file (e.g., .mp4).
        line1_text: The first line of the closing statement.
        line2_text: The second line of the closing statement.
        font_name: The calligraphy font to use. Must be installed on the viewing system.

    Returns:
        Path to the saved PPTX file.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found at: {video_path}")

    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Background Video ===
    vid_shape = slide.shapes.add_movie(
        video_path,
        left=0, top=0,
        width=prs.slide_width, height=prs.slide_height,
        poster_frame_image=None
    )

    # Move video to the back of the z-order
    spTree = slide.shapes.element
    spTree.insert(2, spTree.pop(-1)) # Insert after nvGrpSpPr and grpSpPr

    # --- XML Injection for Auto-Play and Loop ---
    pic_elm = vid_shape.element
    nvPicPr = pic_elm.find('.//p:nvPicPr', namespaces=pic_elm.nsmap)
    nvPr = nvPicPr.find('.//p:nvPr', namespaces=pic_elm.nsmap)
    videoFile = etree.SubElement(
        nvPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}videoFile'
    )
    video_rId = vid_shape.video.rId
    videoFile.set('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}link', video_rId)
    
    # Add loop attribute
    media_elm = pic_elm.find('.//a:blip', namespaces=pic_elm.nsmap)
    if media_elm is not None:
        etree.SubElement(media_elm, '{http://schemas.microsoft.com/office/powerpoint/2010/main}loop', val="1")

    # Add timing for auto-play
    timing_elm = etree.fromstring(
        f'''
        <p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
          <p:tnLst>
            <p:par>
              <p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
                <p:childTnLst>
                  <p:seq concurrent="1" nextAc="seek">
                    <p:cTn id="2" dur="indefinite" nodeType="mainSeq"/>
                    <p:prevCondLst>
                      <p:cond evt="onBegin" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond>
                    </p:prevCondLst>
                  </p:seq>
                </p:childTnLst>
              </p:cTn>
            </p:par>
          </p:tnLst>
        </p:timing>
        '''
    )
    
    main_seq_children = timing_elm.find('.//p:cTn[@id="2"]', namespaces=timing_elm.nsmap)
    if main_seq_children is not None:
         main_seq_children.append(etree.fromstring(f'''
            <p:childTnLst xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
                <p:par>
                    <p:cTn id="3" fill="hold">
                        <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                        <p:childTnLst>
                            <p:cmd type="play" cmd="play">
                                <p:cBhvr>
                                    <p:cTn id="4" dur="0.001"/>
                                    <p:tgtEl><p:spTgt spid="{vid_shape.shape_id}"/></p:tgtEl>
                                </p:cBhvr>
                            </p:cmd>
                        </p:childTnLst>
                    </p:cTn>
                </p:par>
            </p:childTnLst>
        '''))
    slide.part.element.append(timing_elm)

    # === Layer 2: Text & Animation ===
    text_color = RGBColor(255, 255, 255)
    font_size = Pt(96)
    
    tb1 = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(14), Inches(2))
    p1 = tb1.text_frame.paragraphs[0]
    p1.text = line1_text
    p1.font.name = font_name
    p1.font.size = font_size
    p1.font.color.rgb = text_color
    p1.font.bold = True
    
    tb2 = slide.shapes.add_textbox(Inches(2), Inches(4.5), Inches(14), Inches(2))
    p2 = tb2.text_frame.paragraphs[0]
    p2.text = line2_text
    p2.font.name = font_name
    p2.font.size = font_size
    p2.font.color.rgb = text_color
    p2.font.bold = True
    
    # --- XML Injection for Animations ---
    main_seq_node = timing_elm.find('.//p:cTn[@id="2"]', namespaces=timing_elm.nsmap)
    if main_seq_node is None:
        raise ValueError("Could not find main sequence node for animations.")
    child_tn_lst_main = main_seq_node.find('p:childTnLst', namespaces=timing_elm.nsmap)
    if child_tn_lst_main is None:
        child_tn_lst_main = etree.SubElement(main_seq_node, '{http://schemas.openxmlformats.org/presentationml/2006/main}childTnLst')
    
    par_node = child_tn_lst_main.find('p:par', namespaces=timing_elm.nsmap)
    if par_node is None:
        par_node = etree.SubElement(child_tn_lst_main, '{http://schemas.openxmlformats.org/presentationml/2006/main}par')
    
    def add_wipe_animation(parent_node, shape_id, delay_ms, base_id):
        anim_par = etree.SubElement(parent_node, '{http://schemas.openxmlformats.org/presentationml/2006/main}par')
        cTn = etree.SubElement(anim_par, '{http://schemas.openxmlformats.org/presentationml/2006/main}cTn', id=str(base_id), fill="hold")
        stCondLst = etree.SubElement(cTn, '{http://schemas.openxmlformats.org/presentationml/2006/main}stCondLst')
        etree.SubElement(stCondLst, '{http://schemas.openxmlformats.org/presentationml/2006/main}cond', delay=str(delay_ms))
        
        childTnLst = etree.SubElement(cTn, '{http://schemas.openxmlformats.org/presentationml/2006/main}childTnLst')
        anim_effect = etree.fromstring(f'''
            <p:animEffect xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" transition="wipe" filter="from(L)">
                <p:cTn id="{str(base_id + 1)}" dur="1000"/>
                <p:tgtEl><p:spTgt spid="{shape_id}"/></p:tgtEl>
            </p:animEffect>''')
        childTnLst.append(anim_effect)

    add_wipe_animation(par_node, tb1.shape_id, 500, 5)
    add_wipe_animation(par_node, tb2.shape_id, 750, 8)

    # === Layer 3: Decorative Seal ===
    seal_size = Inches(0.8)
    seal_left = tb1.left + Pt(len(line1_text) * 96 * 0.9) # Approximate text width
    seal_top = tb1.top - seal_size / 4
    
    seal = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, seal_left, seal_top, seal_size, seal_size)
    seal.fill.solid()
    seal.fill.fore_color.rgb = RGBColor(200, 0, 0)
    seal.line.fill.background()

    prs.save(output_pptx_path)
    return output_pptx_path

if __name__ == '__main__':
    # --- Example Usage ---
    # 1. Ensure you have a video file named 'road_video.mp4' in the same directory.
    #    You can download a suitable video from a free stock footage site like Pexels.
    # 2. Ensure you have the 'KaiTi' font installed, or change `font_name` to a font
    #    that is on your system (e.g., 'Arial').

    sample_video_path = 'road_video.mp4'
    if not os.path.exists(sample_video_path):
        print(f"ERROR: Video file '{sample_video_path}' not found.")
        print("Please download a sample video and place it in the same directory to run this example.")
    else:
        output_file_path = "cinematic_closing_slide_generated.pptx"
        create_cinematic_closing_slide(
            output_pptx_path=output_file_path,
            video_path=sample_video_path,
            line1_text="The Road Ahead",
            line2_text="Is Full of Promise",
            font_name="Garamond" # Using a more common font for wider compatibility
        )
        print(f"Successfully created presentation: {output_file_path}")
        # On Windows, this will open the file automatically:
        # os.startfile(output_file_path)
