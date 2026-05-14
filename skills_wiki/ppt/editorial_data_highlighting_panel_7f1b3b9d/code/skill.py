def create_slide(
    output_pptx_path: str,
    title_text: str = "A Steady Increase... Except in Japan",
    subtitle_text: str = "Japan experiences a 30-year bubble that peaked in the early '90s",
    highlight_start: int = 2005,
    highlight_end: int = 2017,
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the "Editorial Data Highlighting Panel" 
    effect from the Harvard Business Review video.
    
    Requires: pip install python-pptx matplotlib numpy
    """
    import os
    import numpy as np
    import matplotlib.pyplot as plt
    from io import BytesIO
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE

    # ---------------------------------------------------------
    # 1. Generate the Data Graphic (matplotlib)
    # ---------------------------------------------------------
    # Create synthetic data resembling the video's housing price index
    years = np.arange(1975, 2018)
    np.random.seed(42)
    
    # Generate background "noise" lines (other countries)
    bg_lines = []
    for _ in range(5):
        trend = np.cumsum(np.random.normal(0.5, 2.0, len(years))) + 60
        bg_lines.append(trend)
        
    # Generate the "Japan" line (the anomaly/story focus)
    japan_trend = np.cumsum(np.random.normal(0, 1.5, len(years))) + 50
    # Add the "bubble" in the 90s
    bubble_mask = (years > 1985) & (years < 2005)
    japan_trend[bubble_mask] += np.sin(np.linspace(0, 3.14, sum(bubble_mask))) * 80
    
    # Generate the "Aggregate" line
    agg_trend = np.cumsum(np.random.normal(1.0, 1.0, len(years))) + 55

    # Setup matplotlib figure (wide aspect ratio)
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=150)
    
    # Plot background context lines
    for line in bg_lines:
        ax.plot(years, line, color='#B4B4B4', linewidth=1.5, alpha=0.7)
        
    # Plot key story lines
    ax.plot(years, japan_trend, color='#2E8653', linewidth=2.5, label='Japan') # Green
    ax.plot(years, agg_trend, color='#404040', linewidth=2.5, label='Aggregate') # Dark Gray

    # --- THE CORE VISUAL MECHANIC: The Focus Span ---
    # Draw the yellow highlight box behind the specific "conflict" era
    ax.axvspan(highlight_start, highlight_end, color='#F4D03F', alpha=0.4, lw=0)

    # Styling the chart to look editorial and clean
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#E0E0E0')
    ax.spines['bottom'].set_color('#E0E0E0')
    
    ax.grid(axis='y', color='#EEEEEE', linestyle='-', linewidth=1)
    ax.set_xlim(years[0], years[-1])
    ax.set_ylim(20, 200)
    
    # Customizing ticks
    ax.tick_params(axis='both', colors='#888888', labelsize=10)
    plt.xticks(np.arange(1975, 2018, 8))
    
    # Save chart to memory buffer
    chart_stream = BytesIO()
    plt.tight_layout()
    plt.savefig(chart_stream, format='png', transparent=True)
    chart_stream.seek(0)
    plt.close(fig)

    # ---------------------------------------------------------
    # 2. Assemble the PowerPoint Slide
    # ---------------------------------------------------------
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Add blank slide
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # --- Brand Accent Bars (Left Edge) ---
    # Recreating the HBR transition aesthetic
    colors = [
        RGBColor(255, 217, 102), # Light Yellow
        RGBColor(218, 165, 32),  # Goldenrod
        RGBColor(233, 30, 99)    # Pink
    ]
    bar_width = Inches(0.15)
    for i, color in enumerate(colors):
        shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 
            left=Inches(0.5 + (i * 0.15)), 
            top=Inches(0), 
            width=bar_width, 
            height=prs.slide_height
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        shape.line.fill.background() # No border

    # --- Insert Chart Image ---
    # Positioned at the bottom, leaving room at the top for the narrative
    slide.shapes.add_picture(
        chart_stream, 
        left=Inches(1.5), 
        top=Inches(1.8), 
        width=Inches(11.0)
    )

    # --- Add Narrative Titles (Editable Text) ---
    # Main Title
    title_box = slide.shapes.add_textbox(Inches(1.5), Inches(0.5), Inches(11.0), Inches(0.6))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(40, 40, 40) # Dark Charcoal
    
    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(1.5), Inches(1.1), Inches(11.0), Inches(0.5))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = RGBColor(120, 120, 120) # Medium Gray

    # --- Add Axis Labels (Manual for crispness) ---
    lbl_box = slide.shapes.add_textbox(Inches(1.5), Inches(1.6), Inches(3.0), Inches(0.4))
    lbl_p = lbl_box.text_frame.paragraphs[0]
    lbl_p.text = "Global Real Home Price Index (Index = 100)"
    lbl_p.font.size = Pt(10)
    lbl_p.font.color.rgb = RGBColor(150, 150, 150)

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
