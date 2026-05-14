import os
import urllib.request
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.oxml import OxmlElement, parse_xml
from pptx.oxml.ns import qn

def create_element(name, **attrs):
    """Utility to create an lxml element with attributes."""
    elm = OxmlElement(name)
    for k, v in attrs.items():
        elm.set(k, v)
    return elm

def fetch_image(url, fallback_color, filename):
    """Download an image from a URL or create a solid fallback image."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response, open(filename, 'wb') as out_file:
            out_file.write(response.read())
    except Exception as e:
        print(f"Failed to download image {url}. Creating fallback. Error: {e}")
        img = Image.new('RGB', (1920, 1080), color=fallback_color)
        img.save(filename)
    return filename

def inject_slide_background(slide, image_path):
    """Sets a true Slide Background Picture using lxml."""
    # Add picture temporarily to get the relationship ID (embed code)
    pic = slide.shapes.add_picture(image_path, 0, 0)
    rId = pic.element.blipFill.blip.embed
    pic.element.getparent().remove(pic.element) # Remove the temporary shape
    
    bg_xml = f"""
    <p:bg xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" 
          xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" 
          xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
        <p:bgPr>
            <a:blipFill dpi="0" rotWithShape="0">
                <a:blip r:embed="{rId}"/>
                <a:stretch>
                    <a:fillRect/>
                </a:stretch>
            </a:blipFill>
            <a:effectLst/>
        </p:bgPr>
    </p:bg>
    """
    cSld = slide.element.cSld
    if cSld.bg is not None:
        cSld.remove(cSld.bg)
    cSld.insert(0, parse_xml(bg_xml))

def add_gradient_overlay(slide, width, height):
    """Adds a slide-sized alpha-transparent dark gradient overlay."""
    grad_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, width, height)
    spPr = grad_rect.element.spPr
    
    for elem in list(spPr):
        if elem.tag.endswith('Fill'):
            spPr.remove(elem)
            
    gradFill = create_element('a:gradFill', rotWithShape="1")
    gsLst = create_element('a:gsLst')
    
    # 85% opacity dark blue on the left
    gs1 = create_element('a:gs', pos="0")
    clr1 = create_element('a:srgbClr', val="081018") 
    clr1.append(create_element('a:alpha', val="85000")) 
    gs1.append(clr1)
    
    # 0% opacity on the right
    gs2 = create_element('a:gs', pos="100000")
    clr2 = create_element('a:srgbClr', val="081018")
    clr2.append(create_element('a:alpha', val="0"))
    gs2.append(clr2)
    
    gsLst.append(gs1)
    gsLst.append(gs2)
    gradFill.append(gsLst)
    # Angle 0 in OOXML is Left to Right
    gradFill.append(create_element('a:lin', ang="0", scaled="1")) 
    spPr.append(gradFill)
    
    # Remove borders
    ln = spPr.find(qn('a:ln'))
    if ln is not None:
        spPr.remove(ln)
    noFill = create_element('a:ln')
    noFill.append(create_element('a:noFill'))
    spPr.append(noFill)

def create_segmented_wheel(slide, cx, cy, radius, rotation_deg, name_prefix="Wheel"):
    """Creates a segmented doughnut shape utilizing Slide Background Fill."""
    for i in range(4):
        start_angle = i * 90 + 3
        end_angle = i * 90 + 87
        
        shape = slide.shapes.add_shape(
            MSO_SHAPE.BLOCK_ARC, 
            cx - radius, cy - radius, radius*2, radius*2
        )
        shape.name = f"{name_prefix}_Arc_{i}"
        shape.rotation = rotation_deg
        
        spPr = shape.element.spPr
        prstGeom = spPr.prstGeom
        prstGeom.set("prst", "blockArc")
        for child in list(prstGeom):
            prstGeom.remove(child)
            
        avLst = create_element('a:avLst')
        avLst.append(create_element('a:gd', name="adj1", fmla=f"val {int(start_angle * 60000)}"))
        avLst.append(create_element('a:gd', name="adj2", fmla=f"val {int(end_angle * 60000)}"))
        avLst.append(create_element('a:gd', name="adj3", fmla="val 20000")) # 20% thickness
        prstGeom.append(avLst)
        
        # Inject Background Fill
        for elem in list(spPr):
            if elem.tag.endswith('Fill'):
                spPr.remove(elem)
        spPr.append(create_element('a:bgFill'))
        
        # Inject Drop Shadow
        effectLst = create_element('a:effectLst')
        outerShdw = create_element('a:outerShdw', blurRad="381000", dist="0", dir="0")
        clr = create_element('a:srgbClr', val="000000")
        clr.append(create_element('a:alpha', val="40000"))
        outerShdw.append(clr)
        effectLst.append(outerShdw)
        spPr.append(effectLst)
        
        # Remove outlines
        ln = spPr.find(qn('a:ln'))
        if ln is not None:
            spPr.remove(ln)
        noFill = create_element('a:ln')
        noFill.append(create_element('a:noFill'))
        spPr.append(noFill)

def add_morph_transition(slide):
    """Applies the Morph transition to the slide."""
    transition_xml = """
    <p:transition spd="slow" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
        <p:morph option="byObject"/>
    </p:transition>
    """
    slide.element.insert(1, parse_xml(transition_xml))

def create_slide(
    output_pptx_path: str,
    title_text: str = "Explore the Unseen",
    body_text: str = "Fusce tristique massa eget finibus iaculis. Vestibulum convallis, tortor ac dictum tincidunt, et venenatis tortor justo et sem. Etiam in pellentesque massa.",
    bg_palette: str = "nature", 
    accent_color: tuple = (0, 191, 255), 
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Segmented Background-Reveal Wheel visual effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Download images
    img1_path = fetch_image("https://images.unsplash.com/photo-1559128010-7c1ad6e1b6a5?auto=format&fit=crop&w=1920&q=80", (30, 100, 70), "bg1.jpg")
    img2_path = fetch_image("https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=1920&q=80", (20, 60, 150), "bg2.jpg")

    slides_data = [
        {"img": img1_path, "title": title_text, "wheel_rot": 0, "text_y": 2.5},
        {"img": img2_path, "title": "Lorem Ipsum", "wheel_rot": 90, "text_y": 2.8}
    ]

    for idx, data in enumerate(slides_data):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # 1. Slide Background Image
        inject_slide_background(slide, data["img"])
        
        # 2. Gradient Overlay Mask
        add_gradient_overlay(slide, prs.slide_width, prs.slide_height)
        
        # 3. Segmented Reveal Wheel (Center: off-center right, huge radius)
        create_segmented_wheel(
            slide=slide,
            cx=Inches(9.5), 
            cy=Inches(3.75), 
            radius=Inches(5.5), 
            rotation_deg=data["wheel_rot"], 
            name_prefix="RevealWheel"
        )
        
        # 4. Content - Typography
        # Title
        title_box = slide.shapes.add_textbox(Inches(1.0), Inches(data["text_y"]), Inches(5.0), Inches(1.0))
        title_box.name = "MorphTitle"
        tf = title_box.text_frame
        tf.text = data["title"]
        p = tf.paragraphs[0]
        p.font.size = Pt(54)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        
        # Body Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.1), Inches(data["text_y"] + 1.1), Inches(0.5), Inches(0.05))
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(255, 255, 255)
        line.line.color.type = None
        line.name = "MorphLine"

        # Body Text
        body_box = slide.shapes.add_textbox(Inches(1.0), Inches(data["text_y"] + 1.4), Inches(4.5), Inches(1.5))
        body_box.name = "MorphBody"
        tf_body = body_box.text_frame
        tf_body.word_wrap = True
        p_body = tf_body.paragraphs[0]
        p_body.text = body_text
        p_body.font.size = Pt(16)
        p_body.font.color.rgb = RGBColor(220, 220, 230)
        
        # Button
        btn = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.1), Inches(data["text_y"] + 2.6), Inches(1.8), Inches(0.45))
        btn.name = "MorphButton"
        btn.fill.solid()
        btn.fill.fore_color.rgb = RGBColor(*accent_color)
        btn.line.color.type = None
        btn.text = "MORE INFO"
        btn.text_frame.paragraphs[0].font.size = Pt(12)
        btn.text_frame.paragraphs[0].font.bold = True
        btn.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

        # 5. Apply Morph
        if idx > 0:
            add_morph_transition(slide)

    prs.save(output_pptx_path)
    
    # Cleanup temp images
    for img in [img1_path, img2_path]:
        if os.path.exists(img):
            os.remove(img)
            
    return output_pptx_path
