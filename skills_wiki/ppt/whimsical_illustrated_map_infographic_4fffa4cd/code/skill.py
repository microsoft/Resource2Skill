import io
import math
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw, ImageFilter
import random

def create_slide(
    output_pptx_path: str,
    title_text: str = "古亭周邊美食散策地圖 (Guting Food Map)",
    locations: list = None,
    **kwargs,
) -> str:
    """
    Creates an illustrated, whimsical map infographic in PowerPoint.
    """
    if locations is None:
        locations = [
            {"name": "Ice Gyaru 霜淇淋", "desc": "和平東路一段10-1號\n燕麥奶霜淇淋專門店", "color": (255, 182, 193)},
            {"name": "OOH CHA CHA 自然食", "desc": "和平東路二段207號\n提倡純素、全食物餐點", "color": (152, 251, 152)},
            {"name": "青滷 Vegluu", "desc": "晉江街101號\n特色文青蔬食滷味", "color": (173, 216, 230)},
            {"name": "啼岸 Vegan Resort", "desc": "晉江街133號\n全素日式定食與甜點", "color": (255, 228, 181)},
            {"name": "客來源素坊", "desc": "南昌路二段221號\n平價美味的素食麵館", "color": (221, 160, 221)}
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Universal styling colors
    INK_COLOR = RGBColor(70, 50, 40)
    ROAD_COLOR = RGBColor(255, 250, 240)
    
    # ---------------------------------------------------------
    # 1. Generate Illustrated Canvas Background via PIL
    # ---------------------------------------------------------
    bg_width, bg_height = int(13.333 * 100), int(7.5 * 100)
    bg_img = Image.new('RGBA', (bg_width, bg_height), (226, 240, 217, 255)) # Soft Mint
    
    # Add subtle "terrain" blobs for illustration texture
    draw = ImageDraw.Draw(bg_img)
    for _ in range(15):
        x = random.randint(-200, bg_width)
        y = random.randint(-200, bg_height)
        r = random.randint(100, 400)
        draw.ellipse([x, y, x+r, y+r], fill=(210, 233, 200, 150))
    
    bg_img = bg_img.filter(ImageFilter.GaussianBlur(10))
    bg_stream = io.BytesIO()
    bg_img.save(bg_stream, format='PNG')
    bg_stream.seek(0)
    slide.shapes.add_picture(bg_stream, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # ---------------------------------------------------------
    # 2. Draw the Winding Road (FreeformBuilder)
    # ---------------------------------------------------------
    # We create a sweeping 'S' curve path
    road_points = [
        (Inches(0), Inches(1.5)),
        (Inches(4), Inches(1.5)),
        (Inches(8), Inches(4)),
        (Inches(4), Inches(6)),
        (Inches(13.333), Inches(6))
    ]
    
    ff_builder = slide.shapes.build_freeform(road_points[0][0], road_points[0][1])
    # Add smooth bezier curves to simulate a meandering road
    ff_builder.add_line_segments([
        road_points[1], 
        road_points[2], 
        road_points[3], 
        road_points[4]
    ])
    
    road_shape = ff_builder.convert_to_shape()
    road_shape.line.width = Pt(45)
    road_shape.line.color.rgb = ROAD_COLOR
    road_shape.line.join_style = 'round'
    
    # Duplicate path to create the "ink outline" effect common in illustrations
    ff_builder_outline = slide.shapes.build_freeform(road_points[0][0], road_points[0][1])
    ff_builder_outline.add_line_segments([road_points[1], road_points[2], road_points[3], road_points[4]])
    outline_shape = ff_builder_outline.convert_to_shape()
    outline_shape.line.width = Pt(55) # Slightly thicker
    outline_shape.line.color.rgb = INK_COLOR
    outline_shape.line.join_style = 'round'
    
    # Send outline backward (PowerPoint API doesn't have z-order, so we swap geometry or re-add)
    # Actually, to do this easily in pptx: delete and re-add in correct order.
    # We will just draw outline first, then inner road.
    sp = slide.shapes._spTree
    sp.remove(road_shape._element)
    sp.append(road_shape._element)

    # ---------------------------------------------------------
    # 3. Add Title Banner
    # ---------------------------------------------------------
    title_w, title_h = Inches(6), Inches(1)
    title_box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, 
        Inches(13.333/2) - (title_w/2), Inches(0.4), 
        title_w, title_h
    )
    title_box.fill.solid()
    title_box.fill.fore_color.rgb = RGBColor(255, 250, 240)
    title_box.line.color.rgb = INK_COLOR
    title_box.line.width = Pt(3)
    
    tf = title_box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    run = p.runs[0]
    run.font.size = Pt(28)
    run.font.bold = True
    run.font.color.rgb = INK_COLOR

    # ---------------------------------------------------------
    # 4. Helper function: Generate "Sticker" Marker via PIL
    # ---------------------------------------------------------
    def create_sticker_marker(inner_color):
        size = 120
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        # Drop shadow
        d.ellipse([15, 15, size-5, size-5], fill=(0, 0, 0, 50))
        # White sticker border
        d.ellipse([5, 5, size-15, size-15], fill=(255, 255, 255, 255))
        # Inner color
        d.ellipse([15, 15, size-25, size-25], fill=inner_color)
        # Cute highlight (glassy effect)
        d.ellipse([25, 25, 45, 45], fill=(255, 255, 255, 150))
        
        stream = io.BytesIO()
        img.save(stream, format='PNG')
        stream.seek(0)
        return stream

    # ---------------------------------------------------------
    # 5. Place POIs (Points of Interest) along the map
    # ---------------------------------------------------------
    # Hardcoded pleasant coordinates along our drawn road
    node_coords = [
        (Inches(1.5), Inches(1.0)),
        (Inches(5.0), Inches(2.0)),
        (Inches(8.5), Inches(3.2)),
        (Inches(3.0), Inches(5.0)),
        (Inches(10.0), Inches(5.5))
    ]

    for idx, loc in enumerate(locations):
        if idx >= len(node_coords): break
        nx, ny = node_coords[idx]
        
        # Add Marker
        marker_stream = create_sticker_marker(loc["color"])
        slide.shapes.add_picture(marker_stream, nx, ny, width=Inches(0.8), height=Inches(0.8))
        
        # Add Text Bubble
        bubble_w, bubble_h = Inches(2.8), Inches(1.2)
        
        # Alternate bubble placement (left vs right of marker)
        if idx % 2 == 0:
            bx, by = nx + Inches(0.9), ny - Inches(0.2)
        else:
            bx, by = nx - Inches(2.9), ny - Inches(0.2)
            
        bubble = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, bubble_w, bubble_h
        )
        bubble.fill.solid()
        bubble.fill.fore_color.rgb = RGBColor(255, 255, 255)
        # Thick dark outline for illustrated style
        bubble.line.color.rgb = INK_COLOR
        bubble.line.width = Pt(2.5)
        
        # Format Text
        tf = bubble.text_frame
        tf.word_wrap = True
        
        p_name = tf.paragraphs[0]
        p_name.text = loc["name"]
        p_name.font.size = Pt(14)
        p_name.font.bold = True
        p_name.font.color.rgb = INK_COLOR
        
        p_desc = tf.add_paragraph()
        p_desc.text = loc["desc"]
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = RGBColor(100, 100, 100)

    prs.save(output_pptx_path)
    return output_pptx_path

