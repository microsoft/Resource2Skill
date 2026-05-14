import os
import urllib.request
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches
from pptx.dml.color import RGBColor
from pptx.oxml import parse_xml

def create_slide(
    output_pptx_path: str,
    title_text: str = "Isometric 3D Showcase",
    body_text: str = "",
    bg_palette: str = "nature",  
    accent_color: tuple = (0, 191, 255),  
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Isometric 3D Photo Cube effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Helper 1: Background Gradient Generator ===
    bg_path = "temp_bg_gradient.png"
    bg_img = Image.new("RGB", (1920, 1080))
    draw = ImageDraw.Draw(bg_img)
    color_top = (173, 216, 230)
    color_bottom = (13, 85, 145)
    for y in range(1080):
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * (y / 1080))
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * (y / 1080))
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * (y / 1080))
        draw.line([(0, y), (1920, y)], fill=(r, g, b))
    bg_img.save(bg_path)
    slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)

    # === Helper 2: Fetch and Crop Images to 1:1 Squares ===
    def get_square_image(url, filename, fallback_color):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                with open(filename, 'wb') as out_file:
                    out_file.write(response.read())
            img = Image.open(filename)
            # Center crop to 1:1
            w, h = img.size
            m = min(w, h)
            left, top = (w - m) / 2, (h - m) / 2
            img = img.crop((left, top, left + m, top + m))
            img.save(filename)
        except Exception:
            # Fallback to solid color if download fails
            img = Image.new("RGB", (500, 500), fallback_color)
            img.save(filename)
        return filename

    img1 = get_square_image(f"https://source.unsplash.com/random/800x800/?{bg_palette},sky", "temp_top.jpg", (100, 150, 200))
    img2 = get_square_image(f"https://source.unsplash.com/random/800x800/?{bg_palette},forest", "temp_left.jpg", (50, 120, 80))
    img3 = get_square_image(f"https://source.unsplash.com/random/800x800/?{bg_palette},water", "temp_right.jpg", (20, 80, 160))

    # === Helper 3: Inject 3D Rotation and Bevel via lxml ===
    def apply_3d_engine(shape, camera_preset):
        spPr = shape._element.spPr
        
        # 3D Formatting (Bevel)
        sp3d_xml = '''
        <a:sp3d xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:bevelT w="12700" h="12700" prst="circle"/>
        </a:sp3d>
        '''
        # 3D Scene (Camera projection)
        scene3d_xml = f'''
        <a:scene3d xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:camera prst="{camera_preset}"/>
            <a:lightRig rig="threePt" dir="t"/>
        </a:scene3d>
        '''
        spPr.append(parse_xml(sp3d_xml))
        spPr.append(parse_xml(scene3d_xml))

    # === Layer Configurations & Math ===
    # Math to perfectly stack isometric faces based on PPT's projection matrix
    S = 3.2  # Square size in inches
    Cx = 13.333 / 2  # Slide center X
    Cy = 7.5 / 2     # Slide center Y
    
    dx = S * 0.355   # Isometric X offset
    dy_top = S * 0.36   # Isometric Y offset for top face
    dy_side = S * 0.17  # Isometric Y offset for side faces

    # === Layer 1: The Ambient Floor Shadow ===
    # Using a standard shape, flattening it with top-up camera, and blurring
    shadow = slide.shapes.add_shape(1, Inches(Cx - S/2), Inches(Cy - S/2 + S*0.85), Inches(S), Inches(S))
    shadow.line.fill.background()
    shadow.fill.solid()
    shadow.fill.fore_color.rgb = RGBColor(0, 0, 0)
    
    # Inject 3D and shadow alpha + blur (soft edges)
    apply_3d_engine(shadow, "isometricTopUp")
    spPr = shadow._element.spPr
    spPr.append(parse_xml('<a:softEdge xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" rad="350000"/>'))
    
    srgbClr_nodes = shadow._element.xpath('.//a:srgbClr')
    if srgbClr_nodes:
        srgbClr_nodes[0].append(parse_xml('<a:alpha xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" val="30000"/>'))

    # === Layer 2: The 3D Faces ===
    # Face 1: Top
    top_pic = slide.shapes.add_picture(img1, Inches(Cx - S/2), Inches(Cy - S/2 - dy_top), width=Inches(S), height=Inches(S))
    apply_3d_engine(top_pic, "isometricTopUp")

    # Face 2: Left
    left_pic = slide.shapes.add_picture(img2, Inches(Cx - S/2 - dx), Inches(Cy - S/2 + dy_side), width=Inches(S), height=Inches(S))
    apply_3d_engine(left_pic, "isometricLeftUp")

    # Face 3: Right
    right_pic = slide.shapes.add_picture(img3, Inches(Cx - S/2 + dx), Inches(Cy - S/2 + dy_side), width=Inches(S), height=Inches(S))
    apply_3d_engine(right_pic, "isometricRightUp")

    # === Layer 3: Title Context ===
    tx_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.333), Inches(1))
    tf = tx_box.text_frame
    tf.text = title_text
    p = tf.paragraphs[0]
    p.font.name = 'Segoe UI Light'
    p.font.size = Pt(36)
    p.font.color.rgb = RGBColor(255, 255, 255)

    # Save presentation
    prs.save(output_pptx_path)

    # Cleanup temp files
    for f in [bg_path, img1, img2, img3]:
        if os.path.exists(f):
            os.remove(f)

    return output_pptx_path
