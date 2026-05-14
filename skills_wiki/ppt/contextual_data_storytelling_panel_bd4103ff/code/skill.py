import matplotlib.pyplot as plt
import numpy as np
import io
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR
from lxml import etree

def create_slide(
    output_pptx_path: str,
    title_text: str = "Storytelling Steps",
    bullet_points: list = None,
    background_type: str = "chart",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a contextual data storytelling panel.

    This effect layers a semi-transparent panel over a background visual (like a chart)
    to present a clear narrative or key takeaway, as seen in the tutorial.

    Args:
        output_pptx_path: The path to save the generated PPTX file.
        title_text: The main heading for the storytelling panel.
        bullet_points: A list of strings for the body of the panel.
        background_type: 'chart' or 'placeholder' for the background.
    
    Returns:
        The path to the saved PPTX file.
    """
    if bullet_points is None:
        bullet_points = [
            "Spot the trend (e.g., big peak in 2020)",
            "Ask: Why did this happen?",
            "Drill into dimensions (region, product, platform)",
            "Identify patterns or anomalies",
            "Share findings with stakeholders",
            "Collaborate on next steps",
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background Visual (Placeholder Chart) ===
    fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=100)
    
    # Generate some plausible-looking time series data to mimic a data visualization background
    time_periods = np.arange(0, 48, 1)
    sales_data = 100 + 20 * np.sin(time_periods / 6) + np.random.normal(0, 5, 48).cumsum() + \
                 (time_periods > 12) * (time_periods - 12) * 1.5 - (time_periods > 30) * (time_periods - 30) * 3
    sales_data = np.clip(sales_data, 50, 250)
    
    ax.plot(time_periods, sales_data, color='#0077b6', linewidth=2.5, alpha=0.8)
    ax.fill_between(time_periods, sales_data, color='#ade8f4', alpha=0.3)
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#e9ecef')
    ax.spines['bottom'].set_color('#e9ecef')
    ax.tick_params(axis='x', colors='#6c757d')
    ax.tick_params(axis='y', colors='#6c757d')
    plt.tight_layout()

    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', bbox_inches='tight', pad_inches=0)
    img_stream.seek(0)
    plt.close(fig)

    slide.shapes.add_picture(img_stream, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # === Layer 2: Translucent Rounded Panel ===
    left = Inches(0.5)
    top = Inches(0.5)
    width = Inches(6)
    height = prs.slide_height - Inches(1)
    
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.shadow.inherit = False
    
    # --- lxml injection for transparency ---
    fill = shape.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(248, 249, 250)

    # Access the shape's XML properties and add an alpha (transparency) element
    sp_pr = shape._sp.get_or_add_spPr()
    solid_fill = sp_pr.get_or_add_solidFill()
    
    # Find the color element (srgbClr) to attach alpha to
    srgbClr = solid_fill.find('{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
    if srgbClr is not None:
        # Create and append the alpha tag. val is a percentage * 1000, so 90000 = 90% opacity (10% transparent)
        alpha = etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', val='90000')

    # Remove the shape's border
    line = shape.line
    line.fill.background()

    # === Layer 3: Text Content ===
    txBox = slide.shapes.add_textbox(left + Inches(0.4), top + Inches(0.4), width - Inches(0.8), height - Inches(0.8))
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.clear()

    # Title paragraph
    p_title = tf.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = 'Segoe UI'
    p_title.font.bold = True
    p_title.font.size = Pt(28)
    p_title.font.color.rgb = RGBColor(33, 37, 41)
    p_title.space_after = Pt(12)
    
    # Bullet points
    for point in bullet_points:
        p = tf.add_paragraph()
        p.text = f"–  {point}"
        p.font.name = 'Segoe UI'
        p.font.size = Pt(18)
        p.font.color.rgb = RGBColor(73, 80, 87)
        p.level = 0
        p.space_before = Pt(8)

    prs.save(output_pptx_path)
    return output_pptx_path
