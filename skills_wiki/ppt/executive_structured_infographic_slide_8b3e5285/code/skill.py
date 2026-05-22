import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION

def create_slide(
    output_pptx_path: str,
    title_text: str = "品牌格局：特斯拉領先，本土品牌崛起",
    core_message: str = "2024年台灣電動車市場持續成長，除了特斯拉佔據首位，本土品牌如Luxgen憑藉高性價比快速崛起。",
    chart_data_dict: dict = {"Tesla": 40.0, "Luxgen": 18.7, "BMW": 16.7, "Mercedes": 7.8, "Kia": 3.6, "Others": 13.2},
    key_points: list = None,
    primary_color: tuple = (23, 43, 77),   # Deep Navy
    accent_color: tuple = (0, 191, 255),   # Tech Blue
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Executive Structured Infographic Slide" pattern.
    """
    if key_points is None:
        key_points = [
            ("特斯拉(Tesla)持續主導", "以明顯優勢穩坐市佔率龍頭，強大充電網路與品牌力依然是消費者首選。"),
            ("納智捷(Luxgen)突圍", "主打平價親民路線，n7車型成功切入大眾市場，成為第二大品牌。"),
            ("豪華車廠佈局深化", "BMW與Mercedes等傳統豪華車廠積極導入多元純電車款，穩固高階市場。")
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Background color (very light gray for modern UI feel)
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(248, 249, 250)

    # ==========================================
    # Layer 1: Header (Title & Core Message)
    # ==========================================
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(36)
    p.font.color.rgb = RGBColor(*primary_color)
    p.font.name = "Arial"

    # Core Message Background Ribbon
    msg_bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.3), Inches(11.7), Inches(0.8))
    msg_bg.fill.solid()
    msg_bg.fill.fore_color.rgb = RGBColor(235, 244, 255) # Light blue accent bg
    msg_bg.line.fill.background() # No border
    
    # Left vertical accent line for Core Message
    accent_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.3), Inches(0.1), Inches(0.8))
    accent_line.fill.solid()
    accent_line.fill.fore_color.rgb = RGBColor(*accent_color)
    accent_line.line.fill.background()

    # Core Message Text
    msg_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.35), Inches(11.3), Inches(0.7))
    tf_msg = msg_box.text_frame
    tf_msg.word_wrap = True
    p_msg = tf_msg.paragraphs[0]
    p_msg.text = core_message
    p_msg.font.size = Pt(20)
    p_msg.font.bold = True
    p_msg.font.color.rgb = RGBColor(40, 50, 70)
    p_msg.font.name = "Arial"

    # ==========================================
    # Layer 2: Left Side - Data Visualization (Doughnut Chart)
    # ==========================================
    chart_data = CategoryChartData()
    chart_data.categories = list(chart_data_dict.keys())
    chart_data.add_series('Market Share', list(chart_data_dict.values()))

    x, y, cx, cy = Inches(0.8), Inches(2.5), Inches(5.5), Inches(4.5)
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.DOUGHNUT, x, y, cx, cy, chart_data
    ).chart

    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.BOTTOM
    chart.legend.font.size = Pt(14)
    chart.plots[0].has_data_labels = True
    data_labels = chart.plots[0].data_labels
    data_labels.font.size = Pt(12)
    data_labels.font.color.rgb = RGBColor(255, 255, 255)
    data_labels.number_format = '0.0%'

    # Custom colors for chart series (to match modern palette)
    colors = [
        RGBColor(*primary_color),      # Navy
        RGBColor(*accent_color),       # Blue
        RGBColor(54, 179, 126),        # Mint Green
        RGBColor(255, 171, 0),         # Yellow Orange
        RGBColor(101, 84, 192),        # Purple
        RGBColor(137, 147, 164)        # Gray
    ]
    for i, point in enumerate(chart.plots[0].series[0].points):
        fill = point.format.fill
        fill.solid()
        fill.fore_color.rgb = colors[i % len(colors)]

    # ==========================================
    # Layer 3: Right Side - Key Points (Card UI)
    # ==========================================
    start_x = Inches(6.8)
    start_y = Inches(2.5)
    card_width = Inches(5.7)
    card_height = Inches(1.3)
    spacing = Inches(0.2)

    for i, (kp_title, kp_desc) in enumerate(key_points):
        current_y = start_y + i * (card_height + spacing)

        # Card Background
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x, current_y, card_width, card_height)
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(255, 255, 255)
        card.line.color.rgb = RGBColor(223, 225, 230) # Subtle border
        card.line.width = Pt(1)

        # Card Accent Dot (Visual bullet point)
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, start_x + Inches(0.3), current_y + Inches(0.25), Inches(0.15), Inches(0.15))
        dot.fill.solid()
        dot.fill.fore_color.rgb = RGBColor(*accent_color) if i == 0 else RGBColor(*primary_color)
        dot.line.fill.background()

        # Key Point Title
        kp_title_box = slide.shapes.add_textbox(start_x + Inches(0.5), current_y + Inches(0.1), card_width - Inches(0.6), Inches(0.4))
        tf_kp_title = kp_title_box.text_frame
        p_kp_title = tf_kp_title.paragraphs[0]
        p_kp_title.text = kp_title
        p_kp_title.font.bold = True
        p_kp_title.font.size = Pt(18)
        p_kp_title.font.color.rgb = RGBColor(*primary_color)

        # Key Point Description
        kp_desc_box = slide.shapes.add_textbox(start_x + Inches(0.5), current_y + Inches(0.5), card_width - Inches(0.6), Inches(0.7))
        tf_kp_desc = kp_desc_box.text_frame
        tf_kp_desc.word_wrap = True
        p_kp_desc = tf_kp_desc.paragraphs[0]
        p_kp_desc.text = kp_desc
        p_kp_desc.font.size = Pt(14)
        p_kp_desc.font.color.rgb = RGBColor(94, 108, 132) # Secondary text color

    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("ai_structured_report.pptx")
