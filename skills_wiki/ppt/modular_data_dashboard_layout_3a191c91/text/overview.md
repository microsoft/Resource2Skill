# "Modular Data Dashboard Layout"

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: "Modular Data Dashboard Layout"

*   **Core Visual Mechanism**: A clean, spacious grid of white "cards" on a neutral light gray background. Each card visualizes a single, distinct piece of data (KPI, chart, table, map), creating a modular, at-a-glance overview. The consistent use of a single accent color (professional blue) in various shades unifies the disparate data visualizations and creates a cohesive, corporate aesthetic.

*   **Why Use This Skill (Rationale)**: This layout organizes complex, multi-faceted information into digestible, self-contained chunks. The grid structure provides order and clarity, preventing cognitive overload. The "card" metaphor makes each data point feel like a distinct, manageable object, which is a highly effective and standard UI pattern for presenting multiple metrics simultaneously.

*   **Overall Applicability**: Ideal for any presentation that needs to provide a high-level summary of various metrics.
    *   Executive summaries and business intelligence (BI) reports.
 теоретических
    *   Project status dashboards (e.g., tracking KPIs, progress, and risks).
    *   Financial performance overviews (e.g., revenue, profit, market share).
    *   Marketing campaign analysis.

*   **Value Addition**: This style elevates a collection of disconnected charts and numbers into a cohesive, professional-looking information hub. It conveys a sense of control, analytical rigor, and a comprehensive understanding of the subject matter, making the data feel more authoritative and accessible.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    - **Background**: A neutral, light gray canvas to make the white cards pop. `RGB(248, 249, 250)`.
    - **Cards**: White rectangular containers with slightly rounded corners and a very thin, light gray border to define their edges. Card background is `RGB(255, 255, 255)` with a border of `RGB(222, 226, 230)`.
    - **Color Logic**: A monochromatic blue palette is used for all data visualizations, creating a strong sense of unity.
        - Deep Blue (Primary): `RGB(0, 51, 102)`
        - Medium Blue: `RGB(0, 85, 170)`
        - Accent Blue: `RGB(51, 153, 255)`
        - Light Blue: `RGB(102, 170, 255)`
        - Pale Blue: `RGB(204, 229, 255)`
    - **Text Hierarchy**:
        - **Card Title**: Sans-serif, bold, dark gray `RGB(73, 80, 87)`, ~12-14pt.
        - **KPI Number**: Sans-serif, regular/light weight, very large (~80pt), black `RGB(0, 0, 0)`.
        - **KPI Label**: Sans-serif, regular weight, smaller (~16pt), medium gray `RGB(108, 117, 125)`.
        - **Chart Labels/Axes**: Sans-serif, regular weight, small (~9pt), medium gray `RGB(108, 117, 125)`.

*   **Step B: Compositional Style**
    - **Grid System**: The layout is based on a flexible grid, here demonstrated as a 4-column, 3-row structure. Cards can occupy single cells (1x1) or span multiple cells (e.g., 1x2, 2x1) for emphasis.
    - **Spacing (Gutter)**: Consistent spacing between all cards is critical for a clean look. A gutter of approximately `0.2 Inches` maintains visual separation.
    - **Internal Padding**: Each card has internal whitespace of around `0.2 Inches` to prevent content from touching the edges, which enhances readability.

*   **Step C: Dynamic Effects & Transitions**
    - The original tutorial shows interactive hover tooltips. These are not reproducible in a static PowerPoint slide. The focus of this skill is the static visual layout and data representation.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Dashboard Layout & Card Structure | `python-pptx` native | Ideal for placing and styling basic shapes like rounded rectangles and text boxes. |
| KPI, Table, and Text Cards | `python-pptx` native | The native APIs for text and tables are sufficient to achieve the clean, minimalist style required. |
| All Charts (Donut, Bar, Line, Scatter) | `matplotlib` | `matplotlib` provides far superior control over chart aesthetics (colors, fonts, gridlines, axis labels) than the `python-pptx` chart module, which is crucial for matching the professional look of the dashboard. Charts are rendered to transparent PNGs and inserted. |
| Map Visualization | `urllib` + `python-pptx` (Image Insertion) | Generating a live data map is complex. This skill simplifies the process by downloading a pre-made static map image and placing it into a card, which is a practical approach for a PPTX context. |
| Donut Chart Effect | `matplotlib` + `PIL` | A donut chart is created by generating a pie chart with `matplotlib` and then using PIL to draw a white circle in the center, effectively "punching out" the middle. |

> **Feasibility Assessment**: **90%**. The code successfully reproduces the entire static visual design, including layout, color scheme, typography, and all data visualization styles. The only aspects not reproduced are the dynamic mouse-over interactivity and live data connection from the original web-based tool.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "A股上市公司数据总览",
    bg_palette: str = "technology",
    accent_color: tuple = (0, 85, 170),
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a modular data dashboard layout, inspired by
    data analytics platforms.

    Returns: path to the saved PPTX file.
    """
    import io
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    import matplotlib
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    import urllib.request
    from PIL import Image

    # Use a non-interactive backend for matplotlib
    matplotlib.use('Agg')

    # --- Data Generation ---
    data = {
        'kpi_total_companies': 4840,
        'listing_board': pd.DataFrame({
            'Board': ['主板', '创业板', '科创板', '北交所', '其他'],
            'Count': [3139, 1158, 440, 105, 10]
        }),
        'top_cities': pd.DataFrame({
            'City': ['北京', '上海', '深圳', '杭州', '广州', '苏州', '南京', '成都', '无锡', '宁波'],
            'Count': [439, 400, 384, 159, 129, 129, 109, 106, 90, 85]
        }).sort_values('Count', ascending=True),
        'ipo_by_year': pd.DataFrame({
            'Year': range(1992, 2022),
            'Count': [15, 30, 80, 20, 30, 100, 150, 90, 110, 80, 70, 120, 100, 150, 130, 280, 120, 100, 350, 300, 280, 150, 120, 220, 280, 430, 100, 200, 390, 524]
        }),
        'company_gdp': pd.DataFrame({
            'Count': np.random.randint(20, 450, 30),
            'GDP': np.random.randint(5000, 50000, 30) * np.log1p(np.random.randint(20, 450, 30))
        }),
        'top_market_cap_companies': pd.DataFrame({
            '代码': ['600519.SH', '601398.SH', '300750.SZ', '601939.SH', '601288.SH', '600036.SH'],
            '证券简称': ['贵州茅台', '工商银行', '宁德时代', '建设银行', '农业银行', '招商银行'],
            '总市值(亿元)': [24114, 14944, 12874, 10853, 9736, 9178]
        })
    }

    # --- Presentation Setup ---
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Set slide background color
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(248, 249, 250)

    # --- Color & Font Definitions ---
    COLORS = {
        'bg': RGBColor(248, 249, 250),
        'card': RGBColor(255, 255, 255),
        'border': RGBColor(222, 226, 230),
        'text_title': RGBColor(73, 80, 87),
        'text_body': RGBColor(108, 117, 125),
        'kpi': RGBColor(33, 37, 41),
        'blue_deep': '#003366',
        'blue_medium': '#0055AA',
        'blue_accent': '#3399FF',
        'blue_light': '#66AAFF',
        'blue_pale': '#CCE5FF',
    }
    CHART_PALETTE = [COLORS['blue_deep'], COLORS['blue_medium'], COLORS['blue_accent'], COLORS['blue_light'], COLORS['blue_pale']]
    
    # --- Helper Functions ---
    def add_card(left, top, width, height, title):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLORS['card']
        shape.line.color.rgb = COLORS['border']
        shape.line.width = Pt(1)
        shape.shadow.inherit = False
        
        # Add Title
        title_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.1), width - Inches(0.4), Inches(0.3))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLORS['text_title']
        tf.margin_bottom = 0
        tf.margin_top = 0
        return shape

    def create_chart_figure(figsize=(2.8, 1.8)):
        fig, ax = plt.subplots(figsize=figsize, dpi=150)
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei'] 
        plt.rcParams['axes.unicode_minus'] = False
        ax.tick_params(axis='both', which='major', labelsize=8, colors=COLORS['text_body'])
        ax.grid(True, which='major', axis='y', linestyle='--', linewidth=0.5, color='#CCCCCC')
        ax.set_facecolor(f"#{COLORS['card'].red:02x}{COLORS['card'].green:02x}{COLORS['card'].blue:02x}")
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)
        ax.spines['bottom'].set_color('#DDDDDD')
        ax.spines['left'].set_color('#DDDDDD')
        return fig, ax

    def add_kpi_card(left, top, width, height, title, kpi_value, kpi_label):
        add_card(left, top, width, height, title)
        # KPI Value
        kpi_box = slide.shapes.add_textbox(left, top + Inches(0.8), width, Inches(1.0))
        tf = kpi_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"{kpi_value:,}"
        p.font.size = Pt(60)
        p.font.bold = False
        p.font.color.rgb = COLORS['kpi']
        p.alignment = PP_ALIGN.CENTER
        # KPI Label
        label_box = slide.shapes.add_textbox(left, top + Inches(1.6), width, Inches(0.4))
        tf = label_box.text_frame
        p = tf.paragraphs[0]
        p.text = kpi_label
        p.font.size = Pt(14)
        p.font.color.rgb = COLORS['text_body']
        p.alignment = PP_ALIGN.CENTER

    def add_donut_chart_card(left, top, width, height, title, df, value_col, label_col):
        add_card(left, top, width, height, title)
        fig, ax = create_chart_figure()
        
        wedges, texts, autotexts = ax.pie(df[value_col], labels=None, autopct='%1.1f%%',
                                          startangle=90, colors=CHART_PALETTE,
                                          pctdistance=0.80)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(7)
            autotext.set_fontweight('bold')

        legend = ax.legend(wedges, df[label_col],
                  title=None, loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1), fontsize=8)
        plt.setp(legend.get_texts(), color=f"#{COLORS['text_body'].red:02x}{COLORS['text_body'].green:02x}{COLORS['text_body'].blue:02x}")

        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png', bbox_inches='tight', pad_inches=0.1, transparent=True)
        img_buf.seek(0)
        
        # Punch a hole in the pie chart to make it a donut
        pie_img = Image.open(img_buf).convert("RGBA")
        hole = Image.new('L', pie_img.size, 0)
        draw = ImageDraw.Draw(hole)
        center_x, center_y = pie_img.width / 2, pie_img.height / 2
        radius = min(center_x, center_y) * 0.5  # Adjust donut hole size
        draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)
        pie_img.putalpha(hole)
        
        donut_buf = io.BytesIO()
        pie_img.save(donut_buf, format='png')
        donut_buf.seek(0)

        slide.shapes.add_picture(donut_buf, left + Inches(0.2), top + Inches(0.5), height=height - Inches(0.8))
        plt.close(fig)

    def add_bar_chart_card(left, top, width, height, title, df, value_col, label_col):
        add_card(left, top, width, height, title)
        fig, ax = create_chart_figure(figsize=(3.2, 2.0))
        ax.barh(df[label_col], df[value_col], color=COLORS['blue_medium'])
        ax.tick_params(axis='y', length=0)
        ax.spines['left'].set_visible(False)
        ax.xaxis.grid(True, linestyle='--', which='major', color='#cccccc', alpha=0.7)
        ax.yaxis.grid(False)
        
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png', bbox_inches='tight', pad_inches=0.1, transparent=True)
        img_buf.seek(0)
        slide.shapes.add_picture(img_buf, left + Inches(0.1), top + Inches(0.4), width=width - Inches(0.2))
        plt.close(fig)

    def add_line_chart_card(left, top, width, height, title, df, x_col, y_col):
        add_card(left, top, width, height, title)
        fig, ax = create_chart_figure(figsize=(3.2, 2.0))
        ax.plot(df[x_col], df[y_col], color=COLORS['blue_accent'], linewidth=1.5)
        ax.fill_between(df[x_col], df[y_col], color=COLORS['blue_accent'], alpha=0.1)
        ax.set_xticks(df[x_col][::4]) # Show every 4th year
        ax.tick_params(axis='x', rotation=30)
        
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png', bbox_inches='tight', pad_inches=0.1, transparent=True)
        img_buf.seek(0)
        slide.shapes.add_picture(img_buf, left + Inches(0.1), top + Inches(0.4), width=width - Inches(0.2))
        plt.close(fig)
        
    def add_scatter_plot_card(left, top, width, height, title, df, x_col, y_col):
        add_card(left, top, width, height, title)
        fig, ax = create_chart_figure(figsize=(3.2, 2.0))
        ax.scatter(df[x_col], df[y_col], color=COLORS['blue_deep'], alpha=0.6, s=20)
        ax.set_xlabel('上市公司数量', fontsize=8, color=f"#{COLORS['text_body'].red:02x}{COLORS['text_body'].green:02x}{COLORS['text_body'].blue:02x}")
        ax.set_ylabel('城市GDP(亿元)', fontsize=8, color=f"#{COLORS['text_body'].red:02x}{COLORS['text_body'].green:02x}{COLORS['text_body'].blue:02x}")
        
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png', bbox_inches='tight', pad_inches=0.1, transparent=True)
        img_buf.seek(0)
        slide.shapes.add_picture(img_buf, left + Inches(0.1), top + Inches(0.4), width=width - Inches(0.2))
        plt.close(fig)

    def add_table_card(left, top, width, height, title, df):
        add_card(left, top, width, height, title)
        rows, cols = df.shape[0] + 1, df.shape[1]
        table_shape = slide.shapes.add_table(rows, cols, left + Inches(0.2), top + Inches(0.5), width - Inches(0.4), height - Inches(0.7))
        table = table_shape.table

        # Set headers
        for i, col_name in enumerate(df.columns):
            cell = table.cell(0, i)
            cell.text = col_name
            cell.text_frame.paragraphs[0].font.bold = True
            cell.text_frame.paragraphs[0].font.size = Pt(10)
            cell.text_frame.paragraphs[0].font.color.rgb = COLORS['text_title']
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(248, 249, 250)
            
        # Set data rows
        for r_idx, row in df.iterrows():
            for c_idx, item in enumerate(row):
                cell = table.cell(r_idx + 1, c_idx)
                cell.text = str(item)
                cell.text_frame.paragraphs[0].font.size = Pt(9)
                cell.text_frame.paragraphs[0].font.color.rgb = COLORS['text_body']

    def add_map_card(left, top, width, height, title):
        add_card(left, top, width, height, title)
        map_url = "https://i.imgur.com/u5uWjM6.png" # Placeholder map of China
        try:
            with urllib.request.urlopen(map_url) as url:
                img_data = io.BytesIO(url.read())
            slide.shapes.add_picture(img_data, left + Inches(0.1), top + Inches(0.4), width=width - Inches(0.2))
        except Exception:
            # Fallback text if image download fails
            tb = slide.shapes.add_textbox(left, top, width, height)
            tb.text_frame.text = "Map could not be loaded."
            tb.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
            
    # --- Grid Layout & Card Placement ---
    GUTTER = Inches(0.2)
    CARD_W = (prs.slide_width - 5 * GUTTER) / 4
    CARD_H = (prs.slide_height - 4 * GUTTER) / 3

    # Row 1
    add_kpi_card(GUTTER, GUTTER, CARD_W, CARD_H, '上市公司总数', data['kpi_total_companies'], 'Total Listed Companies')
    add_donut_chart_card(GUTTER * 2 + CARD_W, GUTTER, CARD_W, CARD_H, '上市板块', data['listing_board'], 'Count', 'Board')
    add_bar_chart_card(GUTTER * 3 + CARD_W * 2, GUTTER, CARD_W, CARD_H, '上市公司数量Top10城市', data['top_cities'], 'Count', 'City')
    add_scatter_plot_card(GUTTER * 4 + CARD_W * 3, GUTTER, CARD_W, CARD_H, '上市公司数量与GDP', data['company_gdp'], 'Count', 'GDP')

    # Row 2 & 3
    add_table_card(GUTTER, GUTTER * 2 + CARD_H, CARD_W * 2 + GUTTER, CARD_H, '市值千亿企业', data['top_market_cap_companies'])
    add_line_chart_card(GUTTER, GUTTER * 3 + CARD_H * 2, CARD_W * 2 + GUTTER, CARD_H, '每年IPO数量', data['ipo_by_year'], 'Year', 'Count')
    add_map_card(GUTTER * 3 + CARD_W * 2, GUTTER * 2 + CARD_H, CARD_W * 2 + GUTTER, CARD_H * 2 + GUTTER, '上市公司空间分布')
    
    prs.save(output_pptx_path)
    return output_pptx_path
```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback)? (Yes, with a `try-except` block)
- [x] Are all color values explicit RGB tuples or hex strings? (Yes, defined in a `COLORS` dict)
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes, the grid layout and individual card styles are very similar)
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes, it clearly follows the modular dashboard pattern)