import pandas as pd
import matplotlib.pyplot as plt
import io
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def create_slide(
    output_pptx_path: str,
    title_text: str = "SALES DASHBOARD",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a static business dashboard snapshot, inspired by an Excel tutorial.

    This function uses pandas for data aggregation and matplotlib for chart generation to
    replicate the visual style of a supermarket sales dashboard.

    Args:
        output_pptx_path: The path to save the generated PPTX file.
        title_text: The main title for the dashboard.

    Returns:
        The path to the saved PPTX file.
    """
    # --- Create Presentation and Slide ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Sample Data (mimicking the video's data structure) ---
    csv_data = """City,Customer type,Product line,Quantity,Total,Date,Payment,cogs,Rating,gross income
Mandalay,Member,Health and beauty,7,38.85,2019-02-05,Ewallet,38.85,9.1
Yangon,Normal,Electronic accessories,5,26.25,2019-03-08,Cash,26.25,9.6
Naypyitaw,Normal,Home and lifestyle,5,30.45,2019-01-27,Credit card,30.45,7.4
Mandalay,Member,Health and beauty,7,28.245,2019-01-23,Ewallet,28.245,8.8
Yangon,Normal,Sports and travel,6,58.8,2019-01-18,Ewallet,58.8,4.3
Naypyitaw,Member,Food and beverages,7,43.89,2019-03-24,Credit card,43.89,9.3
Mandalay,Normal,Fashion accessories,3,25.515,2019-01-10,Wallet,25.515,7.7
Yangon,Member,Food and beverages,3,10.5,2019-02-17,Cash,10.5,7.3
Yangon,Normal,Home and lifestyle,10,50.4,2019-03-13,Ewallet,50.4,4.d
Naypyitaw,Member,Health and beauty,8,42.42,2019-02-09,Ewallet,42.42,7.6
"""
    df = pd.read_csv(io.StringIO(csv_data))
    df['Date'] = pd.to_datetime(df['Date'])

    # --- Define Colors and Fonts ---
    BG_COLOR = RGBColor(217, 217, 217)
    TITLE_BAR_COLOR = RGBColor(255, 192, 0)
    CHART_YELLOW = (255/255, 217/255, 102/255) # For matplotlib
    KPI_FILL_COLOR = RGBColor(255, 242, 204)
    FONT_NAME = "Calibri"

    # --- Background ---
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

    # --- Title Bar ---
    title_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.75))
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = TITLE_BAR_COLOR
    title_shape.line.fill.background()

    tf = title_shape.text_frame
    tf.text = title_text
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(36)
    tf.paragraphs[0].font.name = FONT_NAME
    tf.vertical_anchor = 1 # MSO_VERTICAL_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.2)

    # --- KPI Calculations ---
    total_sales = df['Total'].sum()
    total_products = df['Quantity'].sum()
    sales_after_tax = df['gross income'].sum()
    avg_rating = df['Rating'].mean()

    # --- Create KPI Cards ---
    kpi_data = [
        ("Total Penjualan", f"${total_sales:,.0f}"),
        ("Jumlah Produk Terjual", f"{total_products}"),
        ("Total Penjualan Sudah Dikurangi Pajak", f"${sales_after_tax:,.0f}"),
        ("Rata-rata Rating", f"{avg_rating:.2f}")
    ]
    
    kpi_width = Inches(2.5)
    kpi_height = Inches(0.7)
    kpi_y = Inches(0.85)

    for i, (label, value) in enumerate(kpi_data):
        x = Inches(2.5 + i * (kpi_width + 0.3))
        
        # Label
        lbl_box = slide.shapes.add_textbox(x, kpi_y, kpi_width, kpi_height / 2)
        lbl_tf = lbl_box.text_frame
        lbl_p = lbl_tf.paragraphs[0]
        lbl_p.text = label
        lbl_p.font.name = FONT_NAME
        lbl_p.font.size = Pt(11)
        lbl_p.alignment = PP_ALIGN.CENTER
        
        # Value
        val_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, kpi_y + kpi_height / 2, kpi_width, kpi_height)
        val_shape.fill.solid()
        val_shape.fill.fore_color.rgb = KPI_FILL_COLOR
        val_shape.line.fill.background()
        
        val_tf = val_shape.text_frame
        val_p = val_tf.paragraphs[0]
        val_p.text = value
        val_p.font.name = FONT_NAME
        val_p.font.bold = True
        val_p.font.size = Pt(20)
        val_p.alignment = PP_ALIGN.CENTER
        val_tf.vertical_anchor = 1

    # --- Chart Data Aggregation ---
    monthly_sales = df.groupby(df['Date'].dt.strftime('%b'))['Total'].sum().reindex(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    product_sales = df.groupby('Product line')['Total'].sum()
    payment_method = df['Payment'].value_counts()
    rating_by_city = df.groupby('City')['Rating'].mean()

    # --- Chart Style ---
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['font.family'] = FONT_NAME

    # --- Generate Monthly Sales Chart (Line) ---
    fig, ax = plt.subplots(figsize=(5, 3))
    monthly_sales.plot(kind='line', ax=ax, color=CHART_YELLOW, marker='o')
    ax.set_title("Monthly Sales", fontsize=12, weight='bold')
    ax.set_xlabel(''), ax.set_ylabel('')
    ax.tick_params(axis='x', labelsize=8), ax.tick_params(axis='y', labelsize=8)
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    line_chart_img = io.BytesIO()
    plt.savefig(line_chart_img, format='png', bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()

    # --- Generate Product Sales Chart (Bar) ---
    fig, ax = plt.subplots(figsize=(5, 3))
    product_sales.sort_values().plot(kind='bar', ax=ax, color=CHART_YELLOW)
    ax.set_title("Produk Terjual", fontsize=12, weight='bold')
    ax.set_xlabel(''), ax.set_ylabel('')
    ax.tick_params(axis='x', labelsize=7, rotation=45, ha='right')
    ax.tick_params(axis='y', labelsize=8)
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    bar_chart_img = io.BytesIO()
    plt.savefig(bar_chart_img, format='png', bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()
    
    # --- Generate Payment Method Chart (Pie) ---
    fig, ax = plt.subplots(figsize=(4, 3))
    colors = [CHART_YELLOW, (255/255, 242/255, 204/255), 'darkgoldenrod']
    payment_method.plot(kind='pie', ax=ax, colors=colors, autopct='%1.0f%%', textprops={'fontsize': 8})
    ax.set_title("Metode Pembayaran", fontsize=12, weight='bold')
    ax.set_ylabel('')
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    pie_chart_img = io.BytesIO()
    plt.savefig(pie_chart_img, format='png', bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()

    # --- Generate Rating by City Chart (Horizontal Bar) ---
    fig, ax = plt.subplots(figsize=(4, 3))
    rating_by_city.sort_values().plot(kind='barh', ax=ax, color=CHART_YELLOW)
    ax.set_title("Rating Berdasarkan Kota", fontsize=12, weight='bold')
    ax.set_xlabel(''), ax.set_ylabel('')
    ax.tick_params(labelsize=8)
    ax.set_xlim(6, 8)
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    hbar_chart_img = io.BytesIO()
    plt.savefig(hbar_chart_img, format='png', bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()

    # --- Add Charts to Slide ---
    slide.shapes.add_picture(line_chart_img, Inches(2.5), Inches(2.0), width=Inches(5.0))
    slide.shapes.add_picture(bar_chart_img, Inches(2.5), Inches(4.7), width=Inches(5.0))
    slide.shapes.add_picture(pie_chart_img, Inches(8.0), Inches(2.0), width=Inches(4.8))
    slide.shapes.add_picture(hbar_chart_img, Inches(8.0), Inches(4.7), width=Inches(4.8))

    # --- Decorative Slicer Panel ---
    slicer_labels = ["City", "Customer Type", "Product Line", "Payment"]
    for i, label in enumerate(slicer_labels):
        top = Inches(2.0 + i * 1.4)
        slicer_box = slide.shapes.add_textbox(Inches(0.3), top, Inches(1.8), Inches(1.2))
        slicer_box.fill.solid()
        slicer_box.fill.fore_color.rgb = KPI_FILL_COLOR
        slicer_box.line.color.rgb = TITLE_BAR_COLOR
        
        tf = slicer_box.text_frame
        p = tf.add_paragraph()
        p.text = label
        p.font.bold = True
        p.font.size = Pt(12)
    
    prs.save(output_pptx_path)
    return output_pptx_path
