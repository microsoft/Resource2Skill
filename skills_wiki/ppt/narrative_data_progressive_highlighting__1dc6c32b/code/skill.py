def create_slide(
    output_pptx_path: str = "Data_Storytelling_Sequence.pptx",
    **kwargs,
) -> str:
    """
    Creates a 3-slide PPTX sequence demonstrating the Setup-Conflict-Resolution 
    data storytelling framework using matplotlib for chart rendering.
    """
    import numpy as np
    import matplotlib.pyplot as plt
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    import io

    # --- 1. Generate Synthetic Data (Mimicking the video's index data) ---
    np.random.seed(42)
    years = np.arange(1975, 2020)
    
    # "Steady" lines (Setup)
    line_steady1 = np.linspace(60, 120, len(years)) + np.random.normal(0, 2, len(years))
    line_steady2 = np.linspace(40, 110, len(years)) + np.random.normal(0, 3, len(years))
    
    # "Bubble" line (Conflict - Japan-style spike in the early 90s)
    bubble_base = np.linspace(50, 80, len(years))
    bubble_spike = 100 * np.exp(-((years - 1992) ** 2) / (2 * 3 ** 2))
    line_bubble = bubble_base + bubble_spike + np.random.normal(0, 2, len(years))
    
    # "Bifurcated" line (Resolution - Spikes after 2005)
    late_spike = np.where(years > 2005, (years - 2005) * 5, 0)
    line_late = np.linspace(70, 100, len(years)) + late_spike + np.random.normal(0, 2, len(years))

    all_data = [
        {"data": line_steady1, "color": "#2ca02c", "name": "Market A"}, # Green
        {"data": line_steady2, "color": "#ff7f0e", "name": "Market B"}, # Orange
        {"data": line_bubble,  "color": "#9467bd", "name": "Market C (Bubble)"}, # Purple
        {"data": line_late,    "color": "#d62728", "name": "Market D (Late Surge)"} # Red
    ]

    # --- 2. Define Story Stages ---
    stages = [
        {
            "id": "setup",
            "title": "A Steady Increase...",
            "subtitle": "Home prices saw few spikes or dips for 30 years across most global markets.",
            "focus_indices": [0, 1], # Highlight steady lines
            "span_start": 1975,
            "span_end": 2005
        },
        {
            "id": "conflict",
            "title": "...Except in Market C",
            "subtitle": "This market experienced a 30-year bubble that peaked dramatically in the early '90s.",
            "focus_indices": [2], # Highlight bubble line
            "span_start": 1985,
            "span_end": 1998
        },
        {
            "id": "resolution",
            "title": "New Bubbles Floating",
            "subtitle": "Post-2005, the markets bifurcated, with some markets soaring away from the rest.",
            "focus_indices": [3], # Highlight late surge line
            "span_start": 2005,
            "span_end": 2019
        }
    ]

    # --- 3. Initialize Presentation ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- 4. Loop through stages and build slides ---
    for stage in stages:
        slide = prs.slides.add_slide(blank_layout)
        
        # A. Create the Chart via Matplotlib
        fig, ax = plt.subplots(figsize=(10, 5.5), dpi=150)
        
        # Plot all lines
        for i, line_dict in enumerate(all_data):
            is_focused = i in stage["focus_indices"]
            
            # Key Styling Mechanism: Mute background lines, pop focus lines
            color = line_dict["color"] if is_focused else "#cccccc"
            linewidth = 3 if is_focused else 1.5
            alpha = 1.0 if is_focused else 0.5
            zorder = 10 if is_focused else 1
            
            ax.plot(years, line_dict["data"], color=color, linewidth=linewidth, alpha=alpha, zorder=zorder)
            
            # Add label at the end of the line
            if is_focused:
                ax.text(years[-1] + 0.5, line_dict["data"][-1], line_dict["name"], 
                        color=color, va='center', fontweight='bold')

        # Add vertical span for time focus
        ax.axvspan(stage["span_start"], stage["span_end"], color='#FFE696', alpha=0.5, zorder=0)

        # Styling the axes to look clean and presentation-ready
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#dddddd')
        ax.spines['bottom'].set_color('#dddddd')
        ax.tick_params(colors='#555555')
        ax.set_xlim(1975, 2022)
        ax.set_ylim(0, 200)
        ax.grid(axis='y', linestyle='--', alpha=0.3)
        plt.tight_layout()

        # Save plot to memory buffer
        img_stream = io.BytesIO()
        plt.savefig(img_stream, format='png', transparent=True)
        plt.close(fig)
        img_stream.seek(0)

        # B. Insert Chart into PPTX
        slide.shapes.add_picture(img_stream, Inches(1.5), Inches(1.5), width=Inches(11.5))

        # C. Add Narrative Text Boxes
        # Title
        txBox_title = slide.shapes.add_textbox(Inches(1.5), Inches(0.4), Inches(10), Inches(0.6))
        tf_title = txBox_title.text_frame
        tf_title.clear()
        p_title = tf_title.paragraphs[0]
        p_title.text = stage["title"]
        p_title.font.size = Pt(36)
        p_title.font.bold = True
        p_title.font.name = 'Arial'
        p_title.font.color.rgb = RGBColor(30, 30, 30)

        # Subtitle
        txBox_sub = slide.shapes.add_textbox(Inches(1.5), Inches(0.95), Inches(10), Inches(0.5))
        tf_sub = txBox_sub.text_frame
        tf_sub.clear()
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = stage["subtitle"]
        p_sub.font.size = Pt(20)
        p_sub.font.name = 'Arial'
        p_sub.font.color.rgb = RGBColor(100, 100, 100)

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
