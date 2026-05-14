# Native Dashboard UI Simulation

## Analysis

# High-level Design Pattern Extraction

> **Skill Name**: Native Dashboard UI Simulation

* **Core Visual Mechanism**: This pattern simulates the user interface of an interactive Business Intelligence tool (like Power BI or Tableau) directly within a PowerPoint slide. It utilizes "UI Cards" for KPIs (Key Performance Indicators), a persistent tabbed navigation bar, a side-panel for active filters, and a clean, grid-aligned focal data visualization.
* **Why Use This Skill (Rationale)**: True interactive dashboards require specific add-ins, active logins, and reliable internet connections during presentations. Simulating the dashboard natively guarantees zero friction, perfect PDF exports, and offline reliability, while preserving the cognitive benefits of a structured, data-dense UI. The card-based layout isolates metrics, reducing cognitive load compared to crowded traditional slides.
* **Overall Applicability**: Quarterly business reviews, financial reporting, product telemetry updates, and any scenario where executives are accustomed to looking at software dashboards but require a frictionless, static presentation format.
* **Value Addition**: Transforms a standard bullet-point and chart slide into a modern "application-like" experience. The use of drop shadows and structured containers elevates the perceived authority and precision of the data.

---

# Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background Logic**: A very subtle tinted background (`#EBEBF5` - Lavender/Periwinkle Gray) to ensure white UI cards pop out.
  - **Containers (Cards)**: White `#FFFFFF` rectangles with subtle gray borders and soft OpenXML drop shadows to mimic web-based CSS `box-shadow`.
  - **Brand Colors**: Active UI elements and data lines use a primary dark purple/navy `(70, 70, 150)`.
  - **Typography**: Clean, sans-serif fonts. KPI values are massive (`28pt`) and color-coded (red for negative, dark gray for positive) to immediately draw the eye.

* **Step B: Compositional Style**
  - **Header Zone (Top 10%)**: Clean white bar containing the title and tabbed navigation.
  - **KPI Zone (Next 20%)**: Row of four uniform, equally spaced summary cards.
  - **Main Visualization (Bottom 70%, Left 80%)**: The primary chart, styled minimalist (no heavy axes, light gridlines) to mimic modern BI tools.
  - **Filter Panel (Right 20%)**: A vertical column imitating a software slicer/checkbox panel, anchoring the right side of the screen.

* **Step C: Dynamic Effects & Transitions**
  - While this pattern creates a *static* slide, you can duplicate this layout across multiple slides and apply the **Morph transition**. Because the filter panel and tabs remain in identical positions, moving between slides feels exactly like clicking tabs in a live software dashboard.

---

# Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Data Visualization** | `matplotlib` | Allows us to render a sophisticated, styling-stripped line chart that perfectly mimics a Power BI visual. Python-pptx native charts are harder to strip down to this exact minimalist BI aesthetic. |
| **UI Card Depth (Shadows)** | `lxml` XML injection | Native `python-pptx` cannot apply drop shadows to shapes. We must inject `<a:outerShdw>` tags directly to achieve the "floating card" software UI look. |
| **Dashboard Layout & Filters** | `python-pptx` native | Ideal for positioning the tabs, checkboxes, and KPI text boxes with pixel-perfect alignment. |

> **Feasibility Assessment**: 80% — The script perfectly reproduces the *visual aesthetic* of the Power BI dashboard shown in the tutorial (layout, colors, typography, shadow depth, and chart style). It does not embed a live HTML/JS web object (as that requires user-authenticated Office Add-ins), but it provides a highly valuable, presentation-safe, native simulation.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "OfficePlus California Sales",
    **kwargs
) -> str:
    """
    Create a PPTX file reproducing the Native Dashboard UI Simulation effect.
    Returns: path to the saved PPTX file.
    """
    import io
    import matplotlib.pyplot as plt
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from lxml import etree

    # Helper: Inject OpenXML drop shadow for the "UI Card" effect
    def add_ui_shadow(shape):
        spPr = shape.element.spPr
        a = "http://schemas.openxmlformats.org/drawingml/2006/main"
        effectLst = spPr.find(f"{{{a}}}effectLst")
        if effectLst is None:
            effectLst = etree.SubElement(spPr, f"{{{a}}}effectLst")
        outerShdw = etree.SubElement(effectLst, f"{{{a}}}outerShdw", 
                                     blurRad="200000", dist="40000", dir="5400000", rotWithShape="0")
        srgbClr = etree.SubElement(outerShdw, f"{{{a}}}srgbClr", val="000000")
        etree.SubElement(srgbClr, f"{{{a}}}alpha", val="10000") # 10% opacity

    # Initialize presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === 1. Slide Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(235, 235, 245) # Light Lavender/Periwinkle

    # === 2. Header & Tabs ===
    header_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.6))
    header_rect.fill.solid()
    header_rect.fill.fore_color.rgb = RGBColor(255, 255, 255)
    header_rect.line.fill.background()
    add_ui_shadow(header_rect)

    title_box = slide.shapes.add_textbox(Inches(0.3), Inches(0.05), Inches(5), Inches(0.5))
    tf = title_box.text_frame
    tf.text = title_text
    tf.paragraphs[0].font.size = Pt(22)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = RGBColor(70, 70, 150) # Brand Purple

    # Tabs
    tab_names = ["Overview", "Products", "Customers", "Online vs Store"]
    tab_left = 0.36
    for i, name in enumerate(tab_names):
        is_active = (i == 0)
        tab = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(tab_left), Inches(0.8), Inches(1.5), Inches(0.4))
        tab.fill.solid()
        if is_active:
            tab.fill.fore_color.rgb = RGBColor(70, 70, 150)
            text_color = RGBColor(255, 255, 255)
        else:
            tab.fill.fore_color.rgb = RGBColor(210, 210, 225)
            text_color = RGBColor(70, 70, 150)
        tab.line.fill.background()
        
        tf = tab.text_frame
        tf.text = name
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        tf.paragraphs[0].font.color.rgb = text_color
        tf.paragraphs[0].font.size = Pt(11)
        tf.paragraphs[0].font.bold = is_active
        tab_left += 1.55

    # === 3. KPI Cards ===
    kpis = [
        {"title": "Total Sales", "value": "$225.44K"},
        {"title": "Profit", "value": "$44.98K"},
        {"title": "Margin", "value": "19.95%"},
        {"title": "MoM Change", "value": "-12.17%"}
    ]
    kpi_left = 0.36
    for kpi in kpis:
        # Card Container
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(kpi_left), Inches(1.4), Inches(2.55), Inches(1.2))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(255, 255, 255)
        card.line.color.rgb = RGBColor(220, 220, 235)
        add_ui_shadow(card)
        
        # KPI Title
        txBox = slide.shapes.add_textbox(Inches(kpi_left), Inches(1.4), Inches(2.55), Inches(0.4))
        tf = txBox.text_frame
        tf.text = kpi["title"]
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        tf.paragraphs[0].font.size = Pt(12)
        tf.paragraphs[0].font.color.rgb = RGBColor(100, 100, 100)
        
        # KPI Value
        txBox2 = slide.shapes.add_textbox(Inches(kpi_left), Inches(1.75), Inches(2.55), Inches(0.6))
        tf2 = txBox2.text_frame
        tf2.text = kpi["value"]
        tf2.paragraphs[0].alignment = PP_ALIGN.CENTER
        tf2.paragraphs[0].font.size = Pt(28)
        # Conditional formatting
        if "-" in kpi["value"]:
            tf2.paragraphs[0].font.color.rgb = RGBColor(200, 50, 50)
        else:
            tf2.paragraphs[0].font.color.rgb = RGBColor(50, 50, 50)
            
        kpi_left += 2.62

    # === 4. Side Filter Panel ===
    filter_rect = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.95), Inches(0.8), Inches(2.0), Inches(6.3))
    filter_rect.fill.solid()
    filter_rect.fill.fore_color.rgb = RGBColor(255, 255, 255)
    filter_rect.line.color.rgb = RGBColor(220, 220, 235)
    add_ui_shadow(filter_rect)

    fbox = slide.shapes.add_textbox(Inches(11.05), Inches(0.9), Inches(1.8), Inches(0.4))
    fbox.text_frame.text = "Select Year"
    fbox.text_frame.paragraphs[0].font.color.rgb = RGBColor(70, 70, 150)
    fbox.text_frame.paragraphs[0].font.size = Pt(12)

    years = ["2020", "2021", "2022"]
    y_pos = 1.3
    for i, year in enumerate(years):
        # Fake UI Checkbox
        cb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(11.15), Inches(y_pos), Inches(0.15), Inches(0.15))
        cb.fill.solid()
        if i == 2: # '2022' is checked
            cb.fill.fore_color.rgb = RGBColor(70, 70, 150)
        else:
            cb.fill.fore_color.rgb = RGBColor(255, 255, 255)
        cb.line.color.rgb = RGBColor(150, 150, 150)
        
        lbox = slide.shapes.add_textbox(Inches(11.35), Inches(y_pos - 0.08), Inches(1.0), Inches(0.3))
        lbox.text_frame.text = year
        lbox.text_frame.paragraphs[0].font.size = Pt(11)
        y_pos += 0.35

    # === 5. Main Visualization (Matplotlib BI-style) ===
    fig, ax = plt.subplots(figsize=(10.45, 4.5), dpi=150)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    # Chart Data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sales = [150, 200, 180, 220, 280, 250, 310, 290, 350, 380, 360, 420]
    
    # Modern BI styling
    ax.plot(months, sales, color='#464696', linewidth=2.5, marker='o', markersize=7, markerfacecolor='#FFFFFF', markeredgewidth=2)
    ax.fill_between(months, sales, color='#464696', alpha=0.08)
    
    # Clean up axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.yaxis.grid(True, linestyle='-', color='#EEEEEE', alpha=1)
    ax.set_axisbelow(True)
    ax.tick_params(axis='both', which='major', length=0, labelsize=9, colors='#888888', pad=8)
    
    # Save to memory
    plt.tight_layout()
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', bbox_inches='tight', facecolor='#FFFFFF')
    img_stream.seek(0)
    plt.close(fig)

    # Insert chart as a "Card"
    chart_pic = slide.shapes.add_picture(img_stream, Inches(0.36), Inches(2.8), Inches(10.41), Inches(4.3))
    add_ui_shadow(chart_pic)

    prs.save(output_pptx_path)
    return output_pptx_path
```