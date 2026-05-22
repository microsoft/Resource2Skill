import os
import io
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw, ImageFilter

def create_slide(
    output_pptx_path: str,
    title_text: str = "高性能雷达探测",
    subtitle_text: str = "HIGH-PERFORMANCE RADAR DETECTION",
    accent_color_rgb: tuple = (0, 255, 153), # Neon Green/Cyan
    dot_color_rgb: tuple = (255, 102, 0),    # Alert Orange
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the High-Tech Concentric Radar Wave Overlay effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Dark Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(10, 10, 12) # Near black

    # === Helper: Generate Radar Waves using PIL ===
    def generate_radar_waves(size=800, num_rings=25):
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        center = (size // 2, size // 2)
        max_radius = size // 2 - 10
        
        for i in range(num_rings):
            progress = i / (num_rings - 1)
            # Exponential decay for radius to make rings closer near the center
            radius = 20 + (max_radius - 20) * (progress ** 1.2)
            
            # Fade out alpha towards the edges
            alpha = int(200 * (1 - progress))
            color = accent_color_rgb + (alpha,)
            
            bbox = [center[0] - radius, center[1] - radius, 
                    center[0] + radius, center[1] + radius]
            draw.ellipse(bbox, outline=color, width=2)
            
        return img

    # Generate and insert radar waves
    radar_img = generate_radar_waves()
    radar_stream = io.BytesIO()
    radar_img.save(radar_stream, format='PNG')
    radar_stream.seek(0)
    slide.shapes.add_picture(radar_stream, Inches(0.5), Inches(1.5), width=Inches(6.5), height=Inches(6.5))

    # === Helper: Generate Glowing Dot using PIL ===
    def generate_glowing_dot(size=200):
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        
        # Draw halo
        halo = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw_halo = ImageDraw.Draw(halo)
        halo_radius = size * 0.4
        halo_bbox = [size//2 - halo_radius, size//2 - halo_radius, 
                     size//2 + halo_radius, size//2 + halo_radius]
        draw_halo.ellipse(halo_bbox, fill=dot_color_rgb + (80,))
        halo = halo.filter(ImageFilter.GaussianBlur(15))
        
        img.alpha_composite(halo)
        
        # Draw core
        draw_img = ImageDraw.Draw(img)
        core_radius = size * 0.1
        core_bbox = [size//2 - core_radius, size//2 - core_radius, 
                     size//2 + core_radius, size//2 + core_radius]
        draw_img.ellipse(core_bbox, fill=dot_color_rgb + (255,))
        
        return img

    # Generate and insert glowing dots randomly around the radar area
    dot_img = generate_glowing_dot()
    dot_stream = io.BytesIO()
    dot_img.save(dot_stream, format='PNG')
    
    dot_positions = [(2.0, 5.0), (3.5, 6.2), (5.0, 4.5), (1.5, 3.5)]
    for dx, dy in dot_positions:
        dot_stream.seek(0)
        # Randomize dot sizes slightly
        dot_width = Inches(0.8)
        slide.shapes.add_picture(dot_stream, Inches(dx), Inches(dy), width=dot_width, height=dot_width)

    # === Layer 2: Main Subject Image ===
    # Using a transparent placeholder image (simulating the drone)
    # If network fails, we create a stylized placeholder rectangle
    try:
        # A generic transparent 3D tech object/drone placeholder
        url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Drone_icon_1.svg/512px-Drone_icon_1.svg.png"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img_data = response.read()
            img_stream = io.BytesIO(img_data)
            slide.shapes.add_picture(img_stream, Inches(1.5), Inches(1.0), width=Inches(5.0))
    except Exception:
        # Fallback if image fails to download
        from pptx.enum.shapes import MSO_SHAPE
        shape = slide.shapes.add_shape(MSO_SHAPE.HEXAGON, Inches(2.5), Inches(2.0), Inches(3.0), Inches(3.0))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(200, 200, 200)
        shape.line.color.rgb = accent_color_rgb

    # === Layer 3: Typography ===
    
    # Title Box
    title_box = slide.shapes.add_textbox(Inches(7.5), Inches(1.0), Inches(5.0), Inches(1.0))
    tf = title_box.text_frame
    p = tf.add_paragraph()
    p.text = title_text
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = accent_color_rgb
    
    p2 = tf.add_paragraph()
    p2.text = subtitle_text
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(180, 180, 180)

    # Stat Box 1
    stat1_box = slide.shapes.add_textbox(Inches(7.5), Inches(3.0), Inches(5.0), Inches(1.0))
    tf1 = stat1_box.text_frame
    sp1 = tf1.paragraphs[0]
    sp1.text = "系统流畅度提升"
    sp1.font.size = Pt(16)
    sp1.font.color.rgb = RGBColor(255, 255, 255)
    
    sp2 = tf1.add_paragraph()
    sp2.text = "20% - 27%"
    sp2.font.size = Pt(32)
    sp2.font.bold = True
    sp2.font.color.rgb = accent_color_rgb

    # Stat Box 2
    stat2_box = slide.shapes.add_textbox(Inches(7.5), Inches(4.5), Inches(5.0), Inches(1.0))
    tf2 = stat2_box.text_frame
    sp3 = tf2.paragraphs[0]
    sp3.text = "雷达探测灵敏度提升"
    sp3.font.size = Pt(16)
    sp3.font.color.rgb = RGBColor(255, 255, 255)
    
    sp4 = tf2.add_paragraph()
    sp4.text = "53% - 67%"
    sp4.font.size = Pt(32)
    sp4.font.bold = True
    sp4.font.color.rgb = accent_color_rgb

    # Footer/Description Box
    desc_box = slide.shapes.add_textbox(Inches(7.5), Inches(6.0), Inches(5.0), Inches(1.0))
    tf3 = desc_box.text_frame
    tf3.word_wrap = True
    dp = tf3.paragraphs[0]
    dp.text = "应用最新一代雷达传感器，软件系统全面升级，流畅度大幅提升，确保在高干扰环境下依然能够稳定输出高精度数据。"
    dp.font.size = Pt(12)
    dp.font.color.rgb = RGBColor(150, 150, 150)

    prs.save(output_pptx_path)
    return output_pptx_path
