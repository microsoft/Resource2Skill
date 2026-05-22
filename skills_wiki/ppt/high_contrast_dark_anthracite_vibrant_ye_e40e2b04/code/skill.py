import os
import urllib.request
from io import BytesIO
from typing import List, Tuple

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from PIL import Image

def _add_text_shadow(run):
    """
    Injects Open XML to apply a subtle, cinematic drop shadow to a specific text run.
    """
    rPr = run._r.get_or_add_rPr()
    
    # Create the effect list
    effectLst = OxmlElement('a:effectLst')
    
    # Create outer shadow element
    outerShdw = OxmlElement('a:outerShdw')
    outerShdw.set('blurRad', '400000')  # 4pt blur
    outerShdw.set('dist', '300000')     # 3pt distance
    outerShdw.set('dir', '5400000')     # 90 degrees (straight down)
    outerShdw.set('algn', 'tl')
    
    # Set shadow color (Black with 60% opacity)
    srgbClr = OxmlElement('a:srgbClr')
    srgbClr.set('val', '000000')
    alpha = OxmlElement('a:alpha')
    alpha.set('val', '60000')           # 60.000%
    srgbClr.append(alpha)
    
    outerShdw.append(srgbClr)
    effectLst.append(outerShdw)
    rPr.append(effectLst)

def create_slide(
    output_pptx_path: str,
    title_text: str = "WELCOME",
    subtitle_text: str = "Black & Yellow",
    bg_keyword: str = "architecture,bridge",
    accent_color: Tuple[int, int, int] = (254, 203, 14), # #FECB0E Vibrant Yellow
    dark_bg_color: Tuple[int, int, int] = (33, 35, 39),  # #212327 Dark Anthracite
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the High-Contrast Black & Yellow design pattern.
    Generates two slides: A Hero Welcome Slide and a Custom Bar Chart Feature Slide.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    accent_rgb = RGBColor(*accent_color)
    dark_rgb = RGBColor(*dark_bg_color)
    white_rgb = RGBColor(255, 255, 255)

    # =======================================================
    # SLIDE 1: HERO / WELCOME SLIDE
    # =======================================================
    slide_hero = prs.slides.add_slide(blank_layout)
    
    # --- PIL Image Generation (Grayscale + Overlay) ---
    bg_img_path = "temp_hero_bg.png"
    try:
        url = f"https://source.unsplash.com/1600x900/?{bg_keyword}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            raw_img = Image.open(BytesIO(response.read())).convert("RGBA")
    except Exception:
        # Fallback to solid dark gray noise if network fails
        raw_img = Image.new("RGBA", (1600, 900), dark_bg_color)

    # Convert to grayscale and composite a 75% black mask
    gray_img = raw_img.convert("L").convert("RGBA")
    overlay = Image.new("RGBA", gray_img.size, (0, 0, 0, 190)) # ~75% opacity
    composited = Image.alpha_composite(gray_img, overlay)
    composited.save(bg_img_path)

    # Insert background
    slide_hero.shapes.add_picture(bg_img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
    
    # --- Hero Title ---
    tb_title = slide_hero.shapes.add_textbox(Inches(1), Inches(2.5), Inches(11.333), Inches(2))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.alignment = PP_ALIGN.CENTER
    run_title = p_title.add_run()
    run_title.text = title_text.upper()
    run_title.font.name = "Arial" # Standard fallback for Avenir Next
    run_title.font.size = Pt(96)
    run_title.font.bold = True
    run_title.font.color.rgb = white_rgb
    
    # Apply LXML drop shadow for cinematic effect
    _add_text_shadow(run_title)

    # --- Hero Subtitle (Yellow Pill) ---
    # We dynamically approximate width based on char count
    pill_width = Inches(max(3.0, len(subtitle_text) * 0.25))
    pill_left = (prs.slide_width - pill_width) / 2
    
    shape_subtitle = slide_hero.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, 
        pill_left, Inches(4.7), pill_width, Inches(0.8)
    )
    shape_subtitle.fill.solid()
    shape_subtitle.fill.fore_color.rgb = accent_rgb
    shape_subtitle.line.fill.background() # No outline
    
    tf_sub = shape_subtitle.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.alignment = PP_ALIGN.CENTER
    run_sub = p_sub.add_run()
    run_sub.text = subtitle_text
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(28)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(0, 0, 0) # Black text on yellow pill

    # =======================================================
    # SLIDE 2: CUSTOM BAR CHARTS SLIDE
    # =======================================================
    slide_charts = prs.slides.add_slide(blank_layout)
    
    # Set Solid Dark Background
    background = slide_charts.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = dark_rgb

    # Chart Section Title
    tb_chart_title = slide_charts.shapes.add_textbox(Inches(4.5), Inches(0.8), Inches(4.333), Inches(0.8))
    p_ct = tb_chart_title.text_frame.paragraphs[0]
    p_ct.alignment = PP_ALIGN.CENTER
    run_ct = p_ct.add_run()
    run_ct.text = "PERFORMANCE CHARTS"
    run_ct.font.name = "Arial"
    run_ct.font.size = Pt(32)
    run_ct.font.bold = True
    run_ct.font.color.rgb = accent_rgb

    # Define chart data
    data_points = [
        ("Revenue Growth", 75),
        ("Market Share", 50),
        ("Customer Retention", 85),
        ("New Acquisition", 35)
    ]
    
    start_y = 2.2
    spacing_y = 1.2
    chart_left = Inches(2.5)
    chart_width = Inches(5.0)

    # Render Custom Lines and Labels
    for i, (label, pct) in enumerate(data_points):
        current_y = start_y + (i * spacing_y)
        
        # 1. Label Text
        tb_lbl = slide_charts.shapes.add_textbox(chart_left, Inches(current_y - 0.4), Inches(3), Inches(0.4))
        p_lbl = tb_lbl.text_frame.paragraphs[0]
        r_lbl = p_lbl.add_run()
        r_lbl.text = label.upper()
        r_lbl.font.name = "Arial"
        r_lbl.font.size = Pt(14)
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = white_rgb
        
        # 2. Percentage Text (Right aligned to chart)
        tb_pct = slide_charts.shapes.add_textbox(chart_left + chart_width + Inches(0.2), Inches(current_y - 0.4), Inches(1), Inches(0.4))
        p_pct = tb_pct.text_frame.paragraphs[0]
        r_pct = p_pct.add_run()
        r_pct.text = f"{pct}%"
        r_pct.font.name = "Arial"
        r_pct.font.size = Pt(16)
        r_pct.font.bold = True
        r_pct.font.color.rgb = white_rgb

        # 3. Base Line (Thin Gray)
        base_line = slide_charts.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT, 
            chart_left, Inches(current_y + 0.1), chart_left + chart_width, Inches(current_y + 0.1)
        )
        base_line.line.color.rgb = RGBColor(70, 70, 70)
        base_line.line.width = Pt(2)
        
        # 4. Fill Line (Thick Yellow)
        fill_width = chart_width * (pct / 100.0)
        fill_line = slide_charts.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT, 
            chart_left, Inches(current_y + 0.1), chart_left + fill_width, Inches(current_y + 0.1)
        )
        fill_line.line.color.rgb = accent_rgb
        fill_line.line.width = Pt(6)

    # Save output
    prs.save(output_pptx_path)
    
    # Cleanup temp file
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)
        
    return output_pptx_path

