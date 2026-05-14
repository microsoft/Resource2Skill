import os
import urllib.request
import tempfile
from lxml import etree
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

def create_slide(
    output_pptx_path: str,
    title_text: str = "MODULAR\nGRID\nSYSTEMS",
    subtitle_text: str = "Structuring chaos into coherent visual systems using mathematical proportions.",
    accent_color_1: tuple = (217, 248, 75),  # Vibrant Yellow-Green
    accent_color_2: tuple = (255, 87, 51),   # Vibrant Coral
    theme_keyword: str = "architecture",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Vibrant Modular Grid layout.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Set slide background to pure white
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    # --- Grid System Configuration ---
    margin_x = Inches(0.5)
    margin_y = Inches(0.5)
    gutter = Inches(0.15)
    cols, rows = 4, 3

    # Calculate exact cell dimensions based on usable space minus gutters
    total_w = prs.slide_width - (2 * margin_x)
    total_h = prs.slide_height - (2 * margin_y)
    cell_w = (total_w - ((cols - 1) * gutter)) / cols
    cell_h = (total_h - ((rows - 1) * gutter)) / rows

    def get_rect(r, c, r_span, c_span):
        """Helper to calculate absolute coordinates for a module spanning X rows and Y cols."""
        x = margin_x + c * (cell_w + gutter)
        y = margin_y + r * (cell_h + gutter)
        w = (c_span * cell_w) + ((c_span - 1) * gutter)
        h = (r_span * cell_h) + ((r_span - 1) * gutter)
        return x, y, w, h

    # --- Helper: Image Fetcher ---
    def get_image_path(w_in, h_in, seed):
        dpi = 96
        w_px, h_px = int(w_in * dpi), int(h_in * dpi)
        url = f"https://picsum.photos/seed/{seed}/{w_px}/{h_px}"
        out_path = tempfile.mktemp(suffix=".jpg")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as resp:
                with open(out_path, 'wb') as f:
                    f.write(resp.read())
            Image.open(out_path).verify()
            return out_path
        except Exception:
            # Fallback graphic if internet fails
            img = Image.new('RGB', (w_px, h_px), color=(220, 220, 225))
            draw = ImageDraw.Draw(img)
            draw.line((0, 0, w_px, h_px), fill=(200, 200, 205), width=2)
            img.save(out_path, format="JPEG")
            return out_path

    # --- Helper: PIL Pattern Generator ---
    def generate_dot_pattern(w_in, h_in, bg_color):
        dpi = 96
        w_px, h_px = int(w_in * dpi), int(h_in * dpi)
        img = Image.new('RGB', (w_px, h_px), color=bg_color)
        draw = ImageDraw.Draw(img)
        spacing = 16
        dot_radius = 2
        for x in range(0, w_px, spacing):
            for y in range(0, h_px, spacing):
                draw.ellipse((x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius), fill=(255, 255, 255))
        out_path = tempfile.mktemp(suffix=".png")
        img.save(out_path, format="PNG")
        return out_path

    # --- Helper: LXML Shadow Injection ---
    def apply_soft_shadow(shape):
        spPr = shape.element.spPr
        effectLst = spPr.find(qn('a:effectLst'))
        if effectLst is None:
            effectLst = etree.SubElement(spPr, qn('a:effectLst'))
        outerShdw = etree.SubElement(effectLst, qn('a:outerShdw'))
        outerShdw.set('blurRad', '150000')  # 15 pt blur
        outerShdw.set('dist', '50000')      # 5 pt distance
        outerShdw.set('dir', '2700000')     # 45 deg angle
        srgbClr = etree.SubElement(outerShdw, qn('a:srgbClr'))
        srgbClr.set('val', '000000')        # Black shadow
        alpha = etree.SubElement(srgbClr, qn('a:alpha'))
        alpha.set('val', '20000')           # 20% opacity

    # --- Module Builder ---
    def add_module(r, c, rs, cs, fill_type="color", color=(200,200,200), text="", font_size=14, font_color=(0,0,0), img_seed=""):
        x, y, w, h = get_rect(r, c, rs, cs)
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
        shape.line.fill.background() # Invisible border preserves gutters

        if fill_type == "color":
            shape.fill.solid()
            shape.fill.fore_color.rgb = RGBColor(*color)
        elif fill_type == "image":
            img_path = get_image_path(w.inches, h.inches, img_seed)
            shape.fill.user_picture(img_path)
            apply_soft_shadow(shape) # Apply depth to images
        elif fill_type == "pattern":
            pat_path = generate_dot_pattern(w.inches, h.inches, color)
            shape.fill.user_picture(pat_path)

        if text:
            tf = shape.text_frame
            tf.clear()
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf.word_wrap = True
            tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.25)
            
            for i, line in enumerate(text.split('\n')):
                p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
                p.text = line
                p.alignment = PP_ALIGN.LEFT
                p.font.size = Pt(font_size)
                p.font.color.rgb = RGBColor(*font_color)
                p.font.name = "Arial"
                if font_size >= 24:
                    p.font.bold = True
                    p.line_spacing = Pt(font_size * 0.85) # Tight editorial line spacing

    # ==========================================
    # POPULATING THE 4x3 MODULAR GRID
    # ==========================================
    
    # 1. Primary Hero Image (2x2 cells)
    add_module(0, 0, 2, 2, fill_type="image", img_seed=theme_keyword+"_main")
    
    # 2. Main Title Block (1x2 cells)
    add_module(0, 2, 1, 2, fill_type="color", color=(17, 24, 39), 
               text=title_text, font_size=36, font_color=(255, 255, 255))
    
    # 3. Solid Accent 1 Block (1x1 cell)
    add_module(1, 2, 1, 1, fill_type="color", color=accent_color_1)
    
    # 4. Info Text Block (1x1 cell)
    add_module(1, 3, 1, 1, fill_type="color", color=(243, 244, 246),
               text=subtitle_text, font_size=12, font_color=(31, 41, 55))
    
    # 5. Generative Pattern Accent Block (1x1 cell) - Bonus Tip 5 implementation
    add_module(2, 0, 1, 1, fill_type="pattern", color=accent_color_2)
    
    # 6. Secondary Wide Image (1x2 cells)
    add_module(2, 1, 1, 2, fill_type="image", img_seed=theme_keyword+"_sub")
    
    # 7. Highlight / Data Block (1x1 cell)
    add_module(2, 3, 1, 1, fill_type="color", color=(17, 24, 39),
               text="01\nSTRICT\nORDER", font_size=18, font_color=accent_color_1)

    prs.save(output_pptx_path)
    return output_pptx_path
