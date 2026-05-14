import pandas as pd
import matplotlib.pyplot as plt
import io
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def set_cell_style(cell, text, bold=False, font_size=8, font_name='Calibri', fill_color=None):
    """Helper function to style a table cell."""
    cell.text = str(text)
    p = cell.text_frame.paragraphs[0]
    p.font.name = font_name
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.alignment = PP_ALIGN.CENTER
    if fill_color:
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor.from_string(fill_color)

def create_explanatory_dashboard(output_pptx_path: str, region: str = "New York", month: str = "September 2021", **kwargs) -> str:
    """
    Creates a PPTX file with an explanatory data storytelling dashboard.

    Args:
        output_pptx_path: The path to save the generated PPTX file.
        region: The region name to display on the dashboard.
        month: The month/year to display on the dashboard.

    Returns:
        The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Colors
    PRIMARY_BLUE = (28, 56, 114)
    GRAY_TEXT = (128, 128, 128)
    LIGHT_GRAY_FILL = (242, 242, 242)
    GREEN_ACCENT = (118, 188, 33)
    RED_ACCENT = (192, 0, 0)

    # --- Header ---
    title = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12), Inches(0.5))
    p = title.text_frame.paragraphs[0]
    p.text = f"REGIONAL SALES DASHBOARD: {month.upper()}"
    p.font.name = 'Calibri'
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = RGBColor(*PRIMARY_BLUE)

    region_label = slide.shapes.add_textbox(Inches(10.5), Inches(0.5), Inches(2.5), Inches(0.3))
    p = region_label.text_frame.paragraphs[0]
    p.text = f"Region: {region}"
    p.font.name = 'Calibri'
    p.font.size = Pt(12)
    p.alignment = PP_ALIGN.RIGHT
    
    # --- KPIs (Left Panel) ---
    kpi_revenue_val = slide.shapes.add_textbox(Inches(0.5), Inches(1.0), Inches(2.5), Inches(0.7))
    p = kpi_revenue_val.text_frame.paragraphs[0]
    p.text = "$50,618"
    p.font.name = 'Calibri'
    p.font.size = Pt(44)
    p.font.bold = True
    
    kpi_revenue_label = slide.shapes.add_textbox(Inches(0.5), Inches(1.7), Inches(2.5), Inches(0.3))
    p = kpi_revenue_label.text_frame.paragraphs[0]
    p.text = "Total Monthly Revenue"
    p.font.name = 'Calibri'
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(*GRAY_TEXT)

    kpi_mom_val = slide.shapes.add_textbox(Inches(3.0), Inches(1.0), Inches(1.5), Inches(0.7))
    p = kpi_mom_val.text_frame.paragraphs[0]
    p.text = "+1.6%"
    p.font.name = 'Calibri'
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = RGBColor(*GREEN_ACCENT)

    kpi_mom_label = slide.shapes.add_textbox(Inches(3.0), Inches(1.4), Inches(1.5), Inches(0.3))
    p = kpi_mom_label.text_frame.paragraphs[0]
    p.text = "M-o-M Change"
    p.font.name = 'Calibri'
    p.font.size = Pt(10)
    p.font.color.rgb = RGBColor(*GRAY_TEXT)

    # --- Matplotlib Charts ---
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['font.family'] = 'Calibri'

    # Revenue by Date Line Chart
    data_rev_date = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
        '2020': [42000, 45000, 58000, 52000, 63000, 59000, 51000, 43000, 42000],
        '2021': [38000, 41000, 49000, 45000, 59000, 51000, 43000, 34000, 50618]
    }
    df_rev_date = pd.DataFrame(data_rev_date)
    fig, ax = plt.subplots(figsize=(5.5, 3))
    ax.plot(df_rev_date['Month'], df_rev_date['2020'], color=tuple(c/255 for c in GRAY_TEXT), linewidth=1.5, label='2020')
    ax.plot(df_rev_date['Month'], df_rev_date['2021'], color=tuple(c/255 for c in PRIMARY_BLUE), linewidth=2.5, label='2021')
    ax.set_title('Total Revenue by Date', fontsize=12, loc='left', color=tuple(c/255 for c in PRIMARY_BLUE))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)
    ax.legend(frameon=False, fontsize=8)
    
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', bbox_inches='tight', pad_inches=0.1, transparent=True)
    plt.close()
    slide.shapes.add_picture(img_stream, Inches(3.5), Inches(1.7), width=Inches(5.0))

    # Revenue by Category Bar Chart
    data_rev_cat = {'Category': ['Toys', 'Art & Crafts', 'Sports & Outdoors', 'Electronics', 'Games'],
                    'Revenue': [19299, 13882, 7465, 5368, 4603]}
    df_rev_cat = pd.DataFrame(data_rev_cat).sort_values('Revenue', ascending=True)
    fig, ax = plt.subplots(figsize=(4, 2.5))
    bars = ax.barh(df_rev_cat['Category'], df_rev_cat['Revenue'], color=tuple(c/255 for c in PRIMARY_BLUE))
    ax.set_title('Total Revenue by Product Category', fontsize=10, loc='left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='y', length=0, labelsize=9)
    ax.set_xticks([])
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 200, bar.get_y() + bar.get_height()/2, f'${width:,}', ha='left', va='center', fontsize=8)

    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', bbox_inches='tight', transparent=True)
    plt.close()
    slide.shapes.add_picture(img_stream, Inches(0.5), Inches(4.5), height=Inches(2.5))

    # --- Top/Bottom 5 Tables ---
    data_top5 = {'Category': ['Art & Crafts', 'Toys', 'Toys', 'Art & Crafts', 'Art & Crafts'],
                 'Product': ['Playfoam', 'Dinosaur Figures', 'Monopoly', 'Magic Sand', 'Barrel O Slime'],
                 'Revenue': [3352, 2893, 900, 4569, 1357],
                 'Δ Revenue': [2011, 989, 740, 680, 551]}
    df_top5 = pd.DataFrame(data_top5)

    data_bottom5 = {'Category': ['Games', 'Toys', 'Toys', 'Art & Crafts', 'Games'],
                    'Product': ['Rubik\'s Cube', 'Lego Bricks', 'Mr. Potatohead', 'Etch A Sketch', 'Glass Marbles'],
                    'Revenue': [640, 9310, 460, 882, 989],
                    'Δ Revenue': [-1339, -719, -719, -525, -517]}
    df_bottom5 = pd.DataFrame(data_bottom5)

    def create_perf_table(df, x, y, title_text):
        title = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(3.5), Inches(0.3))
        title.text_frame.paragraphs[0].text = title_text
        title.text_frame.paragraphs[0].font.size = Pt(10)

        rows, cols = df.shape[0] + 1, df.shape[1]
        table = slide.shapes.add_table(rows, cols, Inches(x), Inches(y + 0.3), Inches(3.5), Inches(1.2)).table
        
        # Set headers
        for i, col_name in enumerate(df.columns):
            set_cell_style(table.cell(0, i), col_name, bold=True, font_size=9, fill_color='F2F2F2')
            
        # Set data
        for r_idx, row in df.iterrows():
            for c_idx, item in enumerate(row):
                text = f'${item:,}' if df.columns[c_idx] in ['Revenue', 'Δ Revenue'] else item
                cell = table.cell(r_idx + 1, c_idx)
                
                fill = None
                if df.columns[c_idx] == 'Δ Revenue':
                    if item > 0: fill = 'C6E0B4' # Light Green
                    elif item < 0: fill = 'F8CBAD' # Light Red
                set_cell_style(cell, text, fill_color=fill)
    
    create_perf_table(df_top5, 9.3, 2.5, 'Top 5 Products by MoM Revenue Change')
    create_perf_table(df_bottom5, 9.3, 4.5, 'Bottom 5 Products by MoM Revenue Change')

    prs.save(output_pptx_path)
    return output_pptx_path
