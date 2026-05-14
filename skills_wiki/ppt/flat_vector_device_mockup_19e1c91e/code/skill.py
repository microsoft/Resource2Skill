import os
import urllib.request
from PIL import Image, ImageOps, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_slide(
    output_pptx_path: str,
    title_text: str = "HOW TO CREATE\nIPHONE MOCKUP",
    subtitle_text: str = "IN POWERPOINT",
    theme_keyword: str = "technology,gradient",
    device_color: tuple = (28, 28, 30),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Flat Vector Device Mockup visual effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # === Slide Background ===
    # Set a vibrant background color to make the device pop
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.line.fill.background()
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(18, 80, 200) # Deep Blue

    # === Add Typography ===
    tx_box = slide.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(5.5), Inches(3.0))
    tf = tx_box.text_frame
    
    p = tf.add_paragraph()
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(48)
    p.font.name = "Arial Black"
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.line_spacing = 1.0

    p_sub = tf.add_paragraph()
    p_sub.text = subtitle_text
    p_sub.font.bold = True
    p_sub.font.size = Pt(28)
    p_sub.font.name = "Arial"
    p_sub.font.color.rgb = RGBColor(100, 200, 255) # Light Cyan

    # === Prepare Image for Screen using PIL ===
    # We want a 1:2.06 ratio to match the iPhone geometry nicely
    screen_w_px, screen_h_px = 900, 1860
    temp_img_path = "temp_screen_fill.png"
    
    try:
        req = urllib.request.Request(
            f"https://picsum.photos/{screen_w_px}/{screen_h_px}?{theme_keyword}",
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            img = Image.open(response).convert("RGBA")
            img = ImageOps.fit(img, (screen_w_px, screen_h_px), Image.Resampling.LANCZOS)
    except Exception as e:
        # Fallback: Create a gradient image if download fails
        img = Image.new("RGBA", (screen_w_px, screen_h_px))
        draw = ImageDraw.Draw(img)
        for y in range(screen_h_px):
            r = int(255 - (y / screen_h_px) * 100)
            g = int(100 + (y / screen_h_px) * 100)
            b = int(200 + (y / screen_h_px) * 55)
            draw.line([(0, y), (screen_w_px, y)], fill=(r, g, b, 255))

    img.save(temp_img_path)

    # === Device Math & Geometry ===
    # Positioning on the right side of the slide
    device_w = 3.3
    device_h = 6.6
    device_left = Inches(8.5)
    device_top = Inches(0.45)
    margin = 0.15 # bezel thickness
    
    # === Layer 1: Hardware Buttons ===
    btn_color = RGBColor(*device_color)
    
    # Left Side: Volume Up
    vol_up = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, 
                                    device_left - Inches(0.06), device_top + Inches(1.5), 
                                    Inches(0.15), Inches(0.6))
    vol_up.fill.solid()
    vol_up.fill.fore_color.rgb = btn_color
    vol_up.line.color.rgb = btn_color
    vol_up.adjustments[0] = 0.5 # fully rounded pill

    # Left Side: Volume Down
    vol_dn = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, 
                                    device_left - Inches(0.06), device_top + Inches(2.2), 
                                    Inches(0.15), Inches(0.6))
    vol_dn.fill.solid()
    vol_dn.fill.fore_color.rgb = btn_color
    vol_dn.line.color.rgb = btn_color
    vol_dn.adjustments[0] = 0.5

    # Right Side: Power Button
    power_btn = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, 
                                       device_left + Inches(device_w) - Inches(0.09), device_top + Inches(1.8), 
                                       Inches(0.15), Inches(0.8))
    power_btn.fill.solid()
    power_btn.fill.fore_color.rgb = btn_color
    power_btn.line.color.rgb = btn_color
    power_btn.adjustments[0] = 0.5

    # === Layer 2: Outer Bezel ===
    bezel = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        device_left, device_top,
        Inches(device_w), Inches(device_h)
    )
    bezel.fill.solid()
    bezel.fill.fore_color.rgb = btn_color
    bezel.line.color.rgb = btn_color
    bezel.adjustments[0] = 0.16  # Soft, modern curve

    # === Layer 3: Screen Cover ===
    screen_left = device_left + Inches(margin)
    screen_top = device_top + Inches(margin)
    screen_w = device_w - (margin * 2)
    screen_h = device_h - (margin * 2)
    
    screen = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        screen_left, screen_top,
        Inches(screen_w), Inches(screen_h)
    )
    # Fill the shape with the perfectly cropped image
    screen.fill.user_picture(temp_img_path)
    screen.line.color.rgb = btn_color # Match bezel color for seamless edge
    screen.adjustments[0] = 0.14  # Slightly tighter curve for inner screen

    # === Layer 4: The Notch ===
    notch_w = 1.4
    notch_h = 0.22
    notch_left = device_left + Inches((device_w - notch_w) / 2)
    notch_top = screen_top - Inches(0.01) # Slightly overlap top edge to hide seams
    
    notch = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        notch_left, notch_top,
        Inches(notch_w), Inches(notch_h)
    )
    notch.fill.solid()
    notch.fill.fore_color.rgb = btn_color
    notch.line.color.rgb = btn_color
    notch.adjustments[0] = 0.5  # fully rounded bottom pill

    prs.save(output_pptx_path)
    
    # Cleanup temporary image
    if os.path.exists(temp_img_path):
        os.remove(temp_img_path)
        
    return output_pptx_path
