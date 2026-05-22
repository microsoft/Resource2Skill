import io
import numpy as np
import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def _hex_to_rgb(hex_str: str) -> tuple:
    """Convert hex color string to an RGB tuple."""
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def create_slide(
    output_pptx_path: str,
    title_text: str = "Figure 3. Share And Breakdown Of Heat Demand In Industry",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Hierarchical Sunburst Breakdown chart.
    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # ==========================================================
    # 1. GENERATE CONCENTRIC CHART VIA MATPLOTLIB
    # ==========================================================
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(aspect="equal"))
    fig.patch.set_alpha(0.0) # Transparent figure background
    ax.patch.set_alpha(0.0)  # Transparent axes background

    ring_width = 0.35
    
    # Data Definition: Values are calculated so the targeted slices naturally start at 0 degrees.
    # Level 1 (Inner): 32% is the target.
    vals1 = [32, 31, 24, 13]
    colors1 = ['#E5B82A', '#3B5B75', '#885E8E', '#85878A']
    labels1 = ['32%', '31%', '24%', '13%']
    
    # Level 2 (Middle): Breaks down the 32% slice into 24% and 8%. 
    # The remaining 68% (31+24+13) is rendered as transparent.
    vals2 = [24, 8, 68]
    colors2 = ['#E68A2E', '#9E596E', 'none']
    labels2 = ['24%\nHeat', '8%\nElec.', '']
    
    # Level 3 (Outer): Breaks down the 24% Heat slice into 11, 7, 4, 2.
    # The remaining 76% (8+68) is rendered as transparent.
    vals3 = [11, 7, 4, 2, 76]
    colors3 = ['#4E77B8', '#E38D34', '#B3B4B8', '#9EBC4B', 'none']
    labels3 = ['11%', '7%', '4%', '2%', '']
    categories3 = ['Coal', 'Natural Gas', 'Oil', 'Renewables', '']

    def draw_level(vals, colors, labels, radius, width, text_scale=1.0, categories=None):
        wedges, texts = ax.pie(
            vals, radius=radius, colors=colors, startangle=90, counterclock=False,
            wedgeprops=dict(width=width, edgecolor='white', linewidth=2)
        )
        for i, w in enumerate(wedges):
            if colors[i] == 'none':
                w.set_edgecolor('none') # Hide borders for invisible slices
            else:
                # Calculate center of the wedge for text placement
                angle = (w.theta2 - w.theta1) / 2. + w.theta1
                x = (radius - width/2) * np.cos(np.radians(angle))
                y = (radius - width/2) * np.sin(np.radians(angle))
                
                # Scale down font for thinner slices
                fontsize = 14 * text_scale
                if vals[i] <= 4:
                    fontsize = 10 * text_scale
                    
                ax.text(x, y, labels[i], ha='center', va='center', 
                        color='white', fontweight='bold', fontsize=fontsize)
                        
                # Draw outer annotations/callouts if provided
                if categories and categories[i]:
                    x_out = (radius + 0.05) * np.cos(np.radians(angle))
                    y_out = (radius + 0.05) * np.sin(np.radians(angle))
                    ha = 'left' if x_out > 0 else 'right'
                    
                    ax.annotate(categories[i], 
                                xy=((radius)*np.cos(np.radians(angle)), (radius)*np.sin(np.radians(angle))),
                                xytext=(x_out + (0.35 if x_out > 0 else -0.35), y_out + 0.1),
                                arrowprops=dict(arrowstyle="-", color='#7F7F7F', lw=1.5),
                                ha=ha, va='center', fontsize=14, fontweight='bold', color='#4A4A4A')

    # Draw the three hierarchical rings
    draw_level(vals1, colors1, labels1, radius=1, width=ring_width)
    draw_level(vals2, colors2, labels2, radius=1+ring_width, width=ring_width, text_scale=0.85)
    draw_level(vals3, colors3, labels3, radius=1+2*ring_width, width=ring_width, text_scale=0.75, categories=categories3)

    plt.tight_layout()
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', transparent=True, dpi=300)
    plt.close()
    img_stream.seek(0)

    # ==========================================================
    # 2. PPTX SLIDE CONSTRUCTION (Layout, Title, Legend)
    # ==========================================================
    
    # Insert the Matplotlib chart image
    slide.shapes.add_picture(img_stream, Inches(3.5), Inches(0.2), width=Inches(7.2), height=Inches(7.2))

    # Add Academic/Professional Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(10), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.name = "Times New Roman"
    p.font.color.rgb = RGBColor(40, 60, 80)

    # Add dividing line under title
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.1), Inches(11), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(40, 60, 80)
    line.line.color.rgb = RGBColor(40, 60, 80)

    # Build the interactive Legend (Level 1 Categories)
    legend_data = [
        ('Transport', '#85878A'),
        ('Industry', '#E5B82A'),
        ('Residential', '#885E8E'),
        ('Other', '#3B5B75')
    ]
    
    start_y = 2.5
    start_x = 0.5
    for i, (label, color) in enumerate(legend_data):
        # Color Swatch Box
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(start_x), Inches(start_y + i*0.45), Inches(0.3), Inches(0.2))
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(*_hex_to_rgb(color))
        box.line.color.rgb = RGBColor(*_hex_to_rgb(color))
        
        # Legend Text
        tb = slide.shapes.add_textbox(Inches(start_x + 0.4), Inches(start_y + i*0.45 - 0.05), Inches(2.5), Inches(0.3))
        p = tb.text_frame.paragraphs[0]
        p.text = label
        p.font.size = Pt(16)
        p.font.name = "Arial"
        p.font.color.rgb = RGBColor(80, 80, 80)

    prs.save(output_pptx_path)
    return output_pptx_path

