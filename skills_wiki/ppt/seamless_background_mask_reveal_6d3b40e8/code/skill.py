import io
import urllib.request
from pptx import Presentation
from pptx.util import Inches
from pptx.enum.shapes import MSO_SHAPE
from lxml import etree

def create_slide(
    output_pptx_path: str,
    title_text: str = "This is My Awesome Gym",
    bg_image_url: str = "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=1600&q=80",
    character_gif_url: str = "https://i.imgur.com/Gz4B5d6.gif",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide reproducing the "Seamless Background Mask Reveal" effect.

    This function demonstrates how to create an invisible mask that matches the slide
    background, allowing text to animate from "within" the scene. It uses lxml
    to inject the necessary Open XML for the "Slide background fill" and the animation.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        title_text: The main text to be animated on the slide.
        bg_image_url: URL for the background image. A fallback is used if fetching fails.
        character_gif_url: URL for the foreground animated GIF.

    Returns:
        Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Layer 1: Background ---
    try:
        with urllib.request.urlopen(bg_image_url) as url:
            image_data = io.BytesIO(url.read())
        slide.background.fill.picture(image_data)
    except Exception:
        # Fallback to a solid color if image download fails
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = (13, 17, 28) # Dark Navy Blue

    # --- Layer Order Setup ---
    # We add elements in the order they should be layered from back to front.
    # 1. Animated Text (will be at the back)
    # 2. Mask Shape (will be in front of text)
    # 3. Character GIF (will be at the very front)

    # --- Layer 2: Animated Text ---
    textbox = slide.shapes.add_textbox(
        Inches(1), Inches(3), Inches(7), Inches(1.5)
    )
    textbox.text_frame.text = title_text
    p = textbox.text_frame.paragraphs[0]
    font = p.font
    font.name = "Arial Black"
    font.size = Pt(44)
    font.bold = True
    font.color.rgb = (255, 255, 255)

    # --- Layer 3: Mask Shape ---
    # This shape will be made invisible by matching the background
    mask_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(8.5), Inches(0), Inches(4.833), Inches(7.5)
    )
    
    # --- Layer 4: Foreground Character ---
    try:
        with urllib.request.urlopen(character_gif_url) as url:
            gif_data = io.BytesIO(url.read())
        slide.shapes.add_picture(
            gif_data, Inches(8), Inches(2), Inches(3), content_type='image/gif'
        )
    except Exception:
        # If GIF fails, we can skip it. The mask effect will still work.
        pass

    # --- LXML Injection for Mask and Animation ---
    
    # Get the lxml element representation of the slide
    slide_element = slide.element
    
    # Find the mask shape and apply "Slide background fill"
    mask_sp = mask_shape.element
    spPr = mask_sp.xpath('.//p:spPr')[0]
    
    # Remove existing fill (e.g., solidFill)
    for fill_prop in spPr.xpath('a:solidFill | a:gradFill | a:pattFill'):
        spPr.remove(fill_prop)
    
    # Add the background fill property
    bg_fill_xml = etree.fromstring('<a:bgFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>')
    spPr.append(bg_fill_xml)

    # Also remove the line/outline from the mask
    ln = spPr.xpath('.//a:ln')[0]
    ln.getparent().remove(ln)

    # --- LXML for Animation ---
    
    # Every animated shape needs a unique ID. We get the ID of our textbox.
    text_shape_id = textbox.shape_id

    # Create the animation XML tree structure
    # This structure defines a "Fly In" from right animation that happens on click
    # and has a "smooth end" effect.
    anim_xml_str = f"""
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
                          <p:cond delay="indefinite"/>
                        </p:stCondLst>
                        <p:childTnLst>
                          <p:par>
                            <p:cTn id="4" presetID="1" presetClass="entr" presetSubtype="0" fill="hold" nodeType="clickEffect">
                              <p:stCondLst>
                                <p:cond evt="onClick" delay="0">
                                  <p:tgtEl>
                                    <p:sldTgt/>
                                  </p:tgtEl>
                                </p:cond>
                              </p:stCondLst>
                              <p:childTnLst>
                                <p:animEffect transition="in" filter="fly(right)">
                                  <p:cBhvr>
                                    <p:cTn id="5" dur="1000" fill="hold">
                                      <p:accel val="80000"/>
                                      <p:decel val="0"/>
                                    </p:cTn>
                                    <p:tgtEl>
                                      <p:spTgt spid="{text_shape_id}"/>
                                    </p:tgtEl>
                                  </p:cBhvr>
                                </p:animEffect>
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
    
    timing_elm = etree.fromstring(anim_xml_str)
    slide_element.append(timing_elm)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example of how to run the function
if __name__ == '__main__':
    create_slide("seamless_mask_reveal.pptx")
