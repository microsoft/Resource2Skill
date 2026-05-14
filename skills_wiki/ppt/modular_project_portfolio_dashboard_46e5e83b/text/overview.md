# Modular Project Portfolio Dashboard

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Modular Project Portfolio Dashboard

*   **Core Visual Mechanism**: A clean, multi-row, card-based layout where each row represents a distinct project. Key performance indicators (KPIs) like status, risk, and resource allocation are visualized using consistent, color-coded donut charts within each project's card. A right-hand sidebar provides portfolio-level summary metrics, creating a dense, at-a-glance overview.

*   **Why Use This Skill (Rationale)**: This design excels at presenting comparative data. The modular, repetitive structure allows stakeholders to quickly scan and contrast project health across a standardized set of metrics. The visual separation into rows and cards prevents cognitive overload, while the donut charts offer an immediate, intuitive understanding of percentage-based data.

*   **Overall Applicability**: Ideal for executive summaries, project portfolio review meetings, program status updates, and PMO (Project Management Office) dashboards where the status of multiple parallel initiatives must be conveyed efficiently.

*   **Value Addition**: It transforms a complex dataset spanning multiple projects into a single, digestible, and visually scannable slide. This promotes consistency in reporting, instantly highlights outlier projects needing attention, and facilitates data-driven decision-making.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    *   **Elements**: The design is built from rectangular cards with very light grey fills, project title blocks, summary text blocks, donut charts, and a text-based sidebar.
    *   **Color Logic**: A professional and functional palette is key.
        *   Background: White `(255, 255, 255, 255)`
        *   Card Fill: Very light grey `(248, 249, 250, 255)`
        *   Project Title Blocks: Distinct primary colors for each project (e.g., Project A: Blue `(88, 114, 255, 255)`, Project B: Green `(40, 167, 69, 255)`, Project C: Teal `(23, 162, 184, 255)`).
        *   KPI Colors (Donuts): Specific colors are used to represent the metric type consistently.
            *   Status Track (Yellow): `(255, 193, 7, 255)`
            *   Risk Analysis (Orange): `(253, 126, 20, 255)`
            *   Resources (Red): `(220, 53, 69, 255)`
        *   Text: Dark grey/black `(33, 37, 41, 255)` for headings and values, with a lighter grey for descriptive text `(108, 117, 125, 255)`.
        *   Donut Chart Track: Light grey `(233, 236, 239, 255)` to show the unfilled portion of the 100%.
    *   **Text Hierarchy**:
        *   Slide Title: Large, bold, top-left (e.g., 'Arial Black', 24pt).
        *   Project Title: Medium, bold, white text, centered within the colored block.
        *   Card Title: Small, bold, grey (e.g., "Summary", "Status Track").
        *   Donut Chart Percentage: Medium, bold, dark grey, centered in the donut.
        *   Sidebar Value: Large, bold, dark grey.
        *   Sidebar Title: Small, regular, grey.

*   **Step B: Compositional Style**
    *   **Layout**: A rigid grid system dominates the composition. The main content area is divided into 3 rows (for projects) and 4 primary content columns. A fifth column on the far right is reserved for the sidebar.
    *   **Proportions**: The project identifier column occupies ~12% of the content width. The summary column is the widest at ~28%. The three KPI columns are equally sized at ~20% each. The sidebar occupies the remaining ~20% of the slide width.
    *   **Spacing**: Generous, consistent white space (gutters) between all rows and columns is critical for readability and a clean aesthetic.

*   **Step C: Dynamic Effects & Transitions**
    *   The source video is a static showcase. This design pattern is intended for static, information-rich presentation and does not rely on animations.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Overall layout, cards, text | `python-pptx` native | `python-pptx` is the most direct and efficient tool for creating the slide's skeleton: placing rectangular shapes, adding and formatting text boxes, and managing the grid structure. |
| Donut Charts | PIL/Pillow | `python-pptx` lacks the capability to draw partial arcs required for donut charts. PIL allows for precise programmatic drawing of the track and value arcs, rendering text in the center, and exporting the result as a transparent PNG for seamless insertion into the slide. |

> **Feasibility Assessment**: 95%. This code faithfully reproduces the core visual identity of the dashboard: the grid layout, color-coded project rows, data-driven donut charts, and sidebar metrics. Minor variations in font rendering may occur depending on the system, but the overall style and structure are accurately replicated.

#### 3b. Complete Reproduction Code

```python
import os
import io
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image, ImageDraw, ImageFont

def create_donut_chart(percentage: int, color: tuple, size: tuple = (200, 200), track_color: tuple = (233, 236, 239), text_color: tuple = (33, 37, 41)) -> io.BytesIO:
    """
    Creates a donut chart as a transparent PNG image in a byte stream.
    """
    image = Image.new("RGBA", size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    bbox = (10, 10, size[0] - 10, size[1] - 10)
    width = 20

    # Draw the background track
    draw.arc(bbox, start=-90, end=270, fill=track_color, width=width)
    
    # Draw the foreground arc
    end_angle = -90 + (percentage / 100.0) * 360
    if percentage > 0:
        draw.arc(bbox, start=-90, end=end_angle, fill=color, width=width)

    # Draw the text in the center
    try:
        font = ImageFont.truetype("arialbd.ttf", 48)
    except IOError:
        font = ImageFont.load_default()

    text = f"{percentage}%"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (size[0] - text_width) / 2
    text_y = (size[1] - text_height) / 2
    draw.text((text_x, text_y), text, font=font, fill=text_color)
    
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

def create_slide(
    output_pptx_path: str,
    title_text: str = "Project KPI Dashboard",
    project_data: list = None,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Modular Project Portfolio Dashboard visual effect.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    # Slide Title
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.25), Inches(12.33), Inches(0.5))
    p = title_shape.text_frame.paragraphs[0]
    p.text = title_text
    p.font.name = 'Arial Black'
    p.font.size = Pt(24)
    p.font.color.rgb = RGBColor(33, 37, 41)
    
    # Default data if none provided
    if project_data is None:
        project_data = [
            {"name": "Project A", "color": (88, 114, 255), "summary": "On track for Q3 launch. Key milestones for UI/UX are completed.", "status": 50, "risk": 30, "resources": 90},
            {"name": "Project B", "color": (40, 167, 69), "summary": "Budget review pending. Experiencing minor delays in backend integration.", "status": 70, "risk": 50, "resources": 90},
            {"name": "Project C", "color": (23, 162, 184), "summary": "Awaiting final stakeholder feedback. All development tasks are 90% complete.", "status": 90, "risk": 15, "resources": 90}
        ]
        
    # --- Sidebar ---
    sidebar_left = Inches(11.2)
    sidebar_width = Inches(1.8)
    sidebar_top = Inches(1.0)
    
    sidebar_data = [
        {"value": "08", "title": "Ongoing Projects"},
        {"value": "$25.3M", "title": "Allocated Budget"},
        {"value": "50", "title": "Team Members"},
        {"value": "102", "title": "Task Pending"},
    ]
    
    y_pos = sidebar_top
    for item in sidebar_data:
        tb = slide.shapes.add_textbox(sidebar_left, y_pos, sidebar_width, Inches(0.8))
        tf = tb.text_frame
        tf.clear()

        p_val = tf.paragraphs[0]
        p_val.text = item["value"]
        p_val.font.name = 'Arial Black'
        p_val.font.size = Pt(28)
        p_val.font.color.rgb = RGBColor(33, 37, 41)
        
        p_title = tf.add_paragraph()
        p_title.text = item["title"]
        p_title.font.name = 'Arial'
        p_title.font.size = Pt(11)
        p_title.font.color.rgb = RGBColor(108, 117, 125)
        
        y_pos += Inches(1.2)

    # --- Project Rows ---
    start_y = Inches(1.0)
    row_height = Inches(2.0)
    row_gutter = Inches(0.2)
    
    col_starts = [Inches(0.5), Inches(2.2), Inches(5.8), Inches(7.5), Inches(9.2)]
    col_widths = [Inches(1.5), Inches(3.4), Inches(1.5), Inches(1.5), Inches(1.5)]

    for i, project in enumerate(project_data):
        current_y = start_y + i * (row_height + row_gutter)
        
        # Project Name Card
        proj_card = slide.shapes.add_textbox(col_starts[0], current_y, col_widths[0], row_height)
        proj_card.fill.solid()
        proj_card.fill.fore_color.rgb = RGBColor(*project["color"])
        tf = proj_card.text_frame
        tf.vertical_anchor = PP_ALIGN.CENTER
        p = tf.paragraphs[0]
        p.text = project["name"]
        p.font.name = 'Arial Bold'
        p.font.size = Pt(18)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER

        kpi_defs = [
            {"title": "Summary", "type": "text", "value": project["summary"]},
            {"title": "Status Track", "type": "donut", "value": project["status"], "color": (255, 193, 7)},
            {"title": "Risk Analysis", "type": "donut", "value": project["risk"], "color": (253, 126, 20)},
            {"title": "Resources", "type": "donut", "value": project["resources"], "color": (220, 53, 69)}
        ]

        for j in range(1, 5):
            kpi = kpi_defs[j-1]
            card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_starts[j], current_y, col_widths[j], row_height)
            card.shadow.inherit = False
            card.fill.solid()
            card.fill.fore_color.rgb = RGBColor(248, 249, 250)
            card.line.fill.background()

            title_box = slide.shapes.add_textbox(col_starts[j] + Inches(0.1), current_y + Inches(0.1), col_widths[j] - Inches(0.2), Inches(0.3))
            p = title_box.text_frame.paragraphs[0]
            p.text = kpi['title']
            p.font.name = 'Arial Bold'
            p.font.size = Pt(12)
            p.font.color.rgb = RGBColor(108, 117, 125)

            if kpi['type'] == 'text':
                body_box = slide.shapes.add_textbox(col_starts[j] + Inches(0.1), current_y + Inches(0.5), col_widths[j] - Inches(0.2), row_height - Inches(0.6))
                tf = body_box.text_frame
                tf.word_wrap = True
                p = tf.paragraphs[0]
                p.text = kpi['value']
                p.font.name = 'Arial'
                p.font.size = Pt(11)
                p.font.color.rgb = RGBColor(33, 37, 41)
            elif kpi['type'] == 'donut':
                donut_img_stream = create_donut_chart(kpi['value'], kpi['color'])
                img_size = Inches(1.2)
                img_left = col_starts[j] + (col_widths[j] - img_size) / 2
                img_top = current_y + (row_height - img_size) / 2 + Inches(0.1)
                slide.shapes.add_picture(donut_img_stream, img_left, img_top, width=img_size)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example of how to run the function
if __name__ == '__main__':
    output_path = "modular_project_dashboard.pptx"
    create_slide(output_path)
    print(f"Slide saved to {output_path}")
    if os.name == 'nt':
        os.startfile(output_path)
```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback)? (N/A: Images are generated locally with PIL)
- [x] Are all color values explicit RGB tuples?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?
- [x] Would someone looking at the output say "yes, that's the same technique"?