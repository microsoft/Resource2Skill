# Multi-Metric Combo Chart Overlay (Dual-Axis)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Multi-Metric Combo Chart Overlay (Dual-Axis)

*   **Core Visual Mechanism**: The defining visual idea is the juxtaposition of two different chart types (typically a Column/Bar chart and a Line chart) within the same spatial plot area. It maps two distinct data series to visual channels that don't obscure each other (area/mass for bars, connection/trend for the line).
*   **Why Use This Skill (Rationale)**: This technique drastically reduces cognitive load. Instead of forcing the audience's eyes to dart back and forth between two separate charts to spot a correlation (e.g., "Did higher velocity result in more bugs?"), overlaying them forces the intersection to appear immediately.
*   **Overall Applicability**: Perfect for project management dashboards (e.g., Velocity vs. Bugs), financial reviews (e.g., Gross Revenue [Bar] vs. Margin Percentage [Line]), or marketing reports (e.g., Ad Spend [Bar] vs. Cost Per Acquisition [Line]). 
*   **Value Addition**: It transforms raw data presentation into a specific analytical narrative. It answers the "how does X affect Y" question inherently, adding analytical depth to an otherwise standard status report.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    *   **Data Series 1 (Base/Volume):** Represented as clustered columns. Provides the "weight" or "volume" of the primary metric.
    *   **Data Series 2 (Trend/Rate):** Represented as a line with markers. Sits "on top" of the columns visually. 
    *   **Color Logic**: High contrast is required so the line isn't lost in the bars. 
        *   Bars: Muted, solid corporate color, e.g., Steel Blue `RGBA(70, 130, 180, 255)`.
        *   Line: Bright, high-visibility accent color, e.g., Dark Orange `RGBA(255, 140, 0, 255)`.
    *   **Text Hierarchy**: Large minimal title at the top, clear axes labels, and a distinct legend to prevent confusion about which axis belongs to which series.

*   **Step B: Compositional Style**
    *   The chart serves as the hero element, occupying roughly ~70% of the slide width and ~60% of the height.
    *   Ample negative space around the chart prevents it from feeling cluttered.
    *   If scales mismatch (e.g., hundreds of hours vs. single-digit bug counts), the Y-axis must be split left and right to maintain readability.

*   **Step C: Dynamic Effects & Transitions**
    *   *In PowerPoint:* Typically, bars fade or wipe in from the bottom first, followed by a "Wipe" (from left to right) transition for the Line chart to emphasize the progression of time. *(Requires native PPTX animation pane).*

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
| :--- | :--- | :--- |
| **Combo Chart (Bar + Line)** | `matplotlib` | Creating native dual-axis combo charts dynamically using `python-pptx` alone requires highly complex XML (`lxml`) manipulation of the `c:chartSpace` element that frequently breaks across PPT versions. `matplotlib` handles `twinx()` perfectly. |
| **Chart Styling & Polish** | `matplotlib` | Allows precise control over line thickness, marker size, grid lines, and transparent backgrounds. |
| **Slide Layout & Text** | `python-pptx` native | Ideal for placing the final rendered chart perfectly on the slide and adding native, editable title and insight text boxes. |

> **Feasibility Assessment**: 100% reproduction of the visual effect. By leveraging `matplotlib` to render the data visualization and injecting it as an image with a transparent background into `python-pptx`, we achieve pixel-perfect fidelity of the combo chart while keeping the overall slide layout programmatic and editable.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Velocity Planned vs. Bugs Found",
    body_text: str = "Analyzing the correlation between planned sprint output and the volume of defects reported.",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Combo Chart (Bar + Line) visual effect.
    """
    import io
    import numpy as np
    import matplotlib.pyplot as plt
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN

    # Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide

    # Set background color to subtle light gray
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 247, 250)

    # === Layer 1: Generate Combo Chart via Matplotlib ===
    
    # Sample Data
    sprints = ['Sprint 1', 'Sprint 2', 'Sprint 3', 'Sprint 4', 'Sprint 5']
    velocity = [45, 52, 48, 60, 58]
    bugs = [3, 4, 2, 7, 5]

    # Create figure with transparent background
    fig, ax1 = plt.subplots(figsize=(9, 4.5), dpi=300)
    fig.patch.set_alpha(0.0)
    ax1.set_facecolor((0, 0, 0, 0))

    # Plot 1: Bars (Velocity)
    color_bar = '#4682B4' # Steel Blue
    bars = ax1.bar(sprints, velocity, color=color_bar, width=0.5, alpha=0.85, label='Velocity Delivered')
    
    # Plot 2: Line (Bugs) on secondary Y-axis
    ax2 = ax1.twinx()
    color_line = '#FF8C00' # Dark Orange
    line, = ax2.plot(sprints, bugs, color=color_line, marker='o', linewidth=3, 
                     markersize=8, markerfacecolor='white', markeredgewidth=2, label='Bugs Found')

    # Styling axes and grids
    ax1.set_ylabel('Velocity (Points)', color=color_bar, fontsize=12, fontweight='bold')
    ax2.set_ylabel('Bugs (Count)', color=color_line, fontsize=12, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=color_bar)
    ax2.tick_params(axis='y', labelcolor=color_line)
    
    ax1.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    ax1.grid(axis='y', linestyle='--', alpha=0.3, color='gray')
    ax1.tick_params(axis='both', which='major', labelsize=11)
    
    # Combine legends from both axes
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left', 
               bbox_to_anchor=(0, 1.15), ncol=2, frameon=False, fontsize=11)

    plt.tight_layout()

    # Save plot to memory buffer as PNG
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png', bbox_inches='tight', transparent=True)
    image_stream.seek(0)
    plt.close(fig)

    # === Layer 2: Insert Chart into PPTX ===
    
    # Calculate position to center the chart roughly
    img_width = Inches(9)
    img_left = (prs.slide_width - img_width) / 2
    img_top = Inches(2.2)
    slide.shapes.add_picture(image_stream, img_left, img_top, width=img_width)

    # === Layer 3: Add Slide Title and Description ===
    
    # Slide Title
    title_box = slide.shapes.add_textbox(Inches(1), Inches(0.6), Inches(11.33), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = 'Calibri'
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(33, 37, 41)
    p.alignment = PP_ALIGN.CENTER

    # Slide Subtitle / Body
    body_box = slide.shapes.add_textbox(Inches(1), Inches(1.3), Inches(11.33), Inches(0.5))
    tf_body = body_box.text_frame
    p_body = tf_body.paragraphs[0]
    p_body.text = body_text
    p_body.font.name = 'Calibri'
    p_body.font.size = Pt(18)
    p_body.font.color.rgb = RGBColor(108, 117, 125)
    p_body.alignment = PP_ALIGN.CENTER

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
```