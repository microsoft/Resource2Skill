import os
import random
from PIL import Image, ImageDraw, ImageFilter
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from lxml import etree

def create_slide(
    output_pptx_path: str,
    title_text: str = "一個人的奔跑，始終找不到終點",
    body_text: str = "",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the 'Cinematic Side-Scrolling Panorama' effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # ==========================================
    # Layer 1: Generate Cinematic Landscape via PIL
    # ==========================================
    width, height = 1920, 1080
    bg_img = Image.new('RGBA', (width, height), (0, 0, 0, 255))
    draw = ImageDraw.Draw(bg_img)

    # 1. Sky Gradient
    color_top = (10, 30, 60, 255)
    color_bottom = (40, 100, 150, 255)
    for y in range(int(height * 0.6)):
        ratio = y / (height * 0.6)
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # 2. Stars
    for _ in range(150):
        sx = random.randint(0, width)
        sy = random.randint(0, int(height * 0.4))
        draw.point((sx, sy), fill=(255, 255, 255, random.randint(100, 255)))

    # 3. Soft Clouds
    cloud_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(cloud_layer)
    for _ in range(12):
        cx = random.randint(int(width * 0.2), width)
        cy = random.randint(50, 300)
        cr = random.randint(60, 200)
        cdraw.ellipse([cx-cr, cy-cr//2, cx+cr, cy+cr//2], fill=(255, 255, 255, 120))
    cloud_layer = cloud_layer.filter(ImageFilter.GaussianBlur(50))
    bg_img.alpha_composite(cloud_layer)

    # 4. Distant Cityscape
    city_y = int(height * 0.55)
    for x in range(0, width, 50):
        if random.random() > 0.3:
            cw = random.randint(25, 65)
            ch = random.randint(60, 200)
            draw.rectangle([x, city_y - ch, x + cw, city_y], fill=(120, 130, 140, 255))
            # Windows
            for wy in range(city_y - ch + 15, city_y - 15, 20):
                for wx in range(x + 5, x + cw - 10, 15):
                    if random.random() > 0.6:
                        draw.rectangle([wx, wy, wx+6, wy+10], fill=(255, 240, 150, 200))

    # 5. Lush Hills
    hill_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    hdr = ImageDraw.Draw(hill_layer)
    hdr.ellipse([-400, city_y - 80, 700, city_y + 400], fill=(20, 80, 40, 255))
    hdr.ellipse([300, city_y - 120, 1600, city_y + 350], fill=(34, 110, 60, 255))
    hdr.ellipse([1100, city_y - 60, 2500, city_y + 450], fill=(46, 139, 87, 255))
    bg_img.alpha_composite(hill_layer)

    # 6. Water Layer
    water_y = int(height * 0.65)
    draw.rectangle([0, water_y, width, water_y + 200], fill=(15, 45, 85, 255))
    # Water ripples
    for _ in range(70):
        rx = random.randint(0, width)
        ry = random.randint(water_y + 10, water_y + 190)
        rw = random.randint(40, 150)
        draw.line([(rx, ry), (rx+rw, ry)], fill=(255, 255, 255, 40), width=3)

    # 7. Foreground Road
    road_y = int(height * 0.8)
    draw.rectangle([0, road_y, width, height], fill=(45, 45, 50, 255))
    draw.line([(0, road_y + 15), (width, road_y + 15)], fill=(255, 255, 255, 255), width=8)
    draw.line([(0, height - 15), (width, height - 15)], fill=(255, 255, 255, 255), width=8)
    dash_y = road_y + (height - road_y) // 2
    for x in range(0, width, 160):
        draw.line([(x, dash_y), (x+90, dash_y)], fill=(255, 255, 255, 255), width=12)

    # 8. Stylized Dynamic Runner
    runner_x = int(width * 0.75)
    runner_y = road_y + 60
    head_r = 22
    skin = (255, 210, 170, 255)
    shirt = (240, 240, 240, 255)
    pants = (20, 20, 25, 255)

    # Back Arm
    draw.line([(runner_x-5, runner_y-60), (runner_x+35, runner_y-40), (runner_x+50, runner_y-65)], fill=skin, width=16, joint="curve")
    # Back Leg
    draw.line([(runner_x-5, runner_y-30), (runner_x-35, runner_y), (runner_x-55, runner_y-15)], fill=pants, width=20, joint="curve")
    draw.rectangle([runner_x-70, runner_y-20, runner_x-45, runner_y-5], fill=(160, 40, 40, 255)) # Shoe
    # Torso
    draw.polygon([(runner_x-15, runner_y-90), (runner_x+20, runner_y-90), (runner_x+10, runner_y-30), (runner_x-15, runner_y-30)], fill=shirt)
    # Front Leg
    draw.line([(runner_x+5, runner_y-30), (runner_x+40, runner_y-40), (runner_x+50, runner_y+15)], fill=pants, width=20, joint="curve")
    draw.rectangle([runner_x+40, runner_y+15, runner_x+65, runner_y+30], fill=(160, 40, 40, 255)) # Shoe
    # Front Arm
    draw.line([(runner_x+10, runner_y-70), (runner_x-20, runner_y-40), (runner_x-45, runner_y-55)], fill=skin, width=16, joint="curve")
    # Head & Hair
    draw.ellipse([runner_x-head_r+5, runner_y-130-head_r, runner_x+head_r+5, runner_y-130+head_r], fill=skin)
    draw.chord([runner_x-head_r, runner_y-130-head_r-5, runner_x+head_r+10, runner_y-130+5], 160, 360, fill=(15,15,15,255)) 

    # Save Composite Image
    temp_img_path = "temp_panorama_bg.png"
    bg_img.save(temp_img_path)

    # ==========================================
    # Layer 2: PPTX Assembly & Typography
    # ==========================================
    slide.shapes.add_picture(temp_img_path, 0, 0, prs.slide_width, prs.slide_height)

    # Add Text Box
    txBox = slide.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(8), Inches(1.5))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(40)
    p.font.name = "Microsoft YaHei"
    p.font.color.rgb = RGBColor(255, 255, 255)

    # Inject Soft Shadow for readability against clouds via lxml
    rPr = p.runs[0]._r.get_or_add_rPr()
    effectLst = etree.SubElement(rPr, "{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst")
    outerShdw = etree.SubElement(effectLst, "{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw", 
                                 blurRad="50000", dist="38100", dir="2700000", algn="tl")
    srgbClr = etree.SubElement(outerShdw, "{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr", val="000000")
    etree.SubElement(srgbClr, "{http://schemas.openxmlformats.org/drawingml/2006/main}alpha", val="60000")

    # Clean up and save
    prs.save(output_pptx_path)
    if os.path.exists(temp_img_path):
        os.remove(temp_img_path)

    return output_pptx_path
