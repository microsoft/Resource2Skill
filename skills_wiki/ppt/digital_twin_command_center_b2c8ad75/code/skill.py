import io
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_SHAPE_TYPE
from pptx.enum.dml import MSO_THEME_COLOR
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np

# Define the color palette
BG_COLOR = (20, 24, 37)
GRID_COLOR = (50, 60, 80)
TEXT_COLOR_LIGHT = RGBColor(200, 200, 210)
TEXT_COLOR_WHITE = RGBColor(255, 255, 255)
ACCENT_CYAN = RGBColor(0, 220, 255)
ACCENT_MAGENTA = RGBColor(255, 0, 150)
ACCENT_GREEN = RGBColor(80, 255, 150)
ACCENT_YELLOW = RGBColor(255, 220, 0)
ACCENT_RED = RGBColor(255, 0, 80)
MAP_BASE_COLOR = (100, 150, 200)

def create_background_grid(width_px, height_px, grid_spacing=40) -> io.BytesIO:
    """Generates a dark background with a subtle grid."""
    image = Image.new('RGB', (width_px, height_px), BG_COLOR)
    draw = ImageDraw.Draw(image)
    for x in range(0, width_px, grid_spacing):
        draw.line([(x, 0), (x, height_px)], fill=GRID_COLOR, width=1)
    for y in range(0, height_px, grid_spacing):
        draw.line([(0, y), (width_px, y)], fill=GRID_COLOR, width=1)
    
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

def create_gauge(slide, left, top, size, value, max_value, label, color):
    """Creates a circular KPI gauge."""
    # Background donut
    bg_donut = slide.shapes.add_shape(MSO_SHAPE.DONUT, left, top, size, size)
    bg_donut.fill.solid()
    bg_donut.fill.fore_color.rgb = RGBColor(40, 48, 74)
    bg_donut.line.fill.background()
    
    # Adjust donut hole size
    adj = bg_donut.adjustments
    adj[0] = 0.8  # 0.8 means hole radius is 80% of shape radius
    
    # Foreground arc for value
    angle = int(value / max_value * 360)
    fg_arc = slide.shapes.add_shape(MSO_SHAPE.PIE, left, top, size, size)
    fg_arc.fill.solid()
    fg_arc.fill.fore_color.rgb = color
    fg_arc.line.fill.background()
    fg_arc.adjustments[0] = -27000000 # Start angle (0 is right, -27M is top)
    fg_arc.adjustments[1] = angle * 60000
    
    # Add a circle to create the donut hole effect
    hole_size_factor = 0.8
    hole_size = size * hole_size_factor
    hole_left = left + (size - hole_size) / 2
    hole_top = top + (size - hole_size) / 2
    hole = slide.shapes.add_shape(MSO_SHAPE.OVAL, hole_left, hole_top, hole_size, hole_size)
    hole.fill.solid()
    hole.fill.fore_color.rgb = BG_COLOR
    hole.line.fill.background()

    # Value text
    val_textbox = slide.shapes.add_textbox(left, top + size * 0.3, size, size * 0.4)
    p = val_textbox.text_frame.paragraphs[0]
    p.text = f"{value:.1f}"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = TEXT_COLOR_WHITE
    p.alignment = 1 # Center

    # Label text
    lbl_textbox = slide.shapes.add_textbox(left, top + size * 0.9, size, Inches(0.2))
    p = lbl_textbox.text_frame.paragraphs[0]
    p.text = label
    p.font.size = Pt(9)
    p.font.color.rgb = TEXT_COLOR_LIGHT
    p.alignment = 1

def create_bottom_chart(chart_type='bar') -> io.BytesIO:
    """Generates a styled data chart using matplotlib."""
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(4, 1.5))
    fig.patch.set_alpha(0.0)
    ax.set_facecolor((BG_COLOR[0]/255, BG_COLOR[1]/255, BG_COLOR[2]/255, 0.8))

    x = np.arange(10)
    y = np.random.randint(20, 100, 10)
    
    if chart_type == 'bar':
        ax.bar(x, y, color=(ACCENT_CYAN.rgb[0]/255, ACCENT_CYAN.rgb[1]/255, ACCENT_CYAN.rgb[2]/255))
    else: # line
        ax.plot(x, y, color=(ACCENT_MAGENTA.rgb[0]/255, ACCENT_MAGENTA.rgb[1]/255, ACCENT_MAGENTA.rgb[2]/255), marker='o', markersize=4)
        ax.fill_between(x, y, color=(ACCENT_MAGENTA.rgb[0]/255, ACCENT_MAGENTA.rgb[1]/255, ACCENT_MAGENTA.rgb[2]/255), alpha=0.2)


    ax.tick_params(axis='x', colors='grey')
    ax.tick_params(axis='y', colors='grey')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('grey')
    ax.spines['left'].set_color('grey')
    ax.grid(axis='y', linestyle='--', alpha=0.2)
    plt.tight_layout()

    img_byte_arr = io.BytesIO()
    plt.savefig(img_byte_arr, format='PNG', dpi=150, transparent=True)
    img_byte_arr.seek(0)
    plt.close(fig)
    return img_byte_arr

def create_slide(
    output_pptx_path: str,
    title_text: str = "新DC工場トップ",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide reproducing the Digital Twin Command Center effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    bg_img = create_background_grid(int(prs.slide_width * 96), int(prs.slide_height * 96))
    slide.background.fill.picture(bg_img)

    # === Layer 2: Main Map Schematic ===
    # This is a simplified, representative map.
    map_container = slide.shapes.add_group_shape()
    
    def add_map_shape(points, fill_color, transparency):
        freeform = map_container.shapes.add_freeform_shape()
        with freeform.build() as builder:
            builder.move_to(Inches(points[0][0]), Inches(points[0][1]))
            for p in points[1:]:
                builder.add_line_to(Inches(p[0]), Inches(p[1]))
            builder.close()
        
        freeform.fill.solid()
        freeform.fill.fore_color.rgb = RGBColor(*fill_color)
        freeform.fill.transparency = transparency
        freeform.line.fill.solid()
        freeform.line.fill.fore_color.rgb = RGBColor(150, 200, 255)
        freeform.line.width = Pt(1)

    # Base building shapes (semi-transparent blue)
    add_map_shape([(4.5, 1.5), (7, 1), (8.5, 2), (6, 2.5)], MAP_BASE_COLOR, 0.7)
    add_map_shape([(3, 3), (5.5, 2.5), (7, 3.5), (4.5, 4)], MAP_BASE_COLOR, 0.7)
    add_map_shape([(7.2, 3.6), (9, 3.2), (10, 4.2), (8.2, 4.6)], MAP_BASE_COLOR, 0.7)
    
    # Highlighted shapes (e.g., warning and freeze)
    add_map_shape([(5.6, 2.6), (7, 2.3), (8, 3.1), (6.6, 3.4)], ACCENT_YELLOW.rgb, 0.6) # Warning
    add_map_shape([(6.2, 4.2), (7.8, 3.9), (8.5, 4.7), (6.9, 5)], ACCENT_RED.rgb, 0.5) # Freeze

    # === Layer 3: Text & Data Pods ===
    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(5), Inches(0.5))
    p = title_box.text_frame.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = TEXT_COLOR_WHITE

    # Gauges on the map
    create_gauge(slide, Inches(3.5), Inches(3.2), Inches(0.8), 32.3, 100, "Line B", ACCENT_MAGENTA)
    create_gauge(slide, Inches(8.5), Inches(2.2), Inches(0.8), 88.8, 100, "Line G", ACCENT_GREEN)
    create_gauge(slide, Inches(10), Inches(4.5), Inches(0.8), 45.5, 100, "Line H", ACCENT_MAGENTA)

    # Side KPI panel
    create_gauge(slide, Inches(0.5), Inches(1.0), Inches(1.5), 85.6, 100, "工場マップ 可動率", ACCENT_CYAN)

    # Bottom Charts
    chart_title = slide.shapes.add_textbox(Inches(0.5), Inches(5.5), Inches(4), Inches(0.3))
    p = chart_title.text_frame.paragraphs[0]
    p.text = "生産量推移"
    p.font.color.rgb = TEXT_COLOR_WHITE
    p.font.size = Pt(12)
    chart1_img = create_bottom_chart('bar')
    slide.shapes.add_picture(chart1_img, Inches(0.5), Inches(5.8), Inches(4))

    chart_title_2 = slide.shapes.add_textbox(Inches(4.8), Inches(5.5), Inches(4), Inches(0.3))
    p = chart_title_2.text_frame.paragraphs[0]
    p.text = "エネルギー消費"
    p.font.color.rgb = TEXT_COLOR_WHITE
    p.font.size = Pt(12)
    chart2_img = create_bottom_chart('line')
    slide.shapes.add_picture(chart2_img, Inches(4.8), Inches(5.8), Inches(4))

    prs.save(output_pptx_path)
    return output_pptx_path
