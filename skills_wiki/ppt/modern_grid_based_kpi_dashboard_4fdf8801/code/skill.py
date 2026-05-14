import io
import matplotlib.pyplot as plt
import numpy as np
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# --- Matplotlib Chart Generation Functions ---

def create_traffic_sources_chart(colors, file_path):
    """Generates the 'Traffic Sources' donut chart."""
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(3, 2))
    
    labels = ['Direct', 'Display', 'Organic', 'Paid', 'Referral', 'Social']
    sizes = [76, 5, 9, 5, 4, 1]
    chart_colors = [colors['teal'], colors['light_purple'], colors['dark_purple'], colors['blue'], colors['teal_light'], colors['purple_light']]
    
    wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.0f%%', startangle=90, colors=chart_colors,
                                      wedgeprops=dict(width=0.4, edgecolor='w'))
    
    # Manually position percentage labels inside wedges
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        if sizes[i] > 5:
            ax.text(x*0.7, y*0.7, f'{sizes[i]}%', ha='center', va='center', color='white', fontsize=8, weight='bold')

    ax.axis('equal')
    ax.legend(labels, loc="center left", bbox_to_anchor=(1.1, 0.5), frameon=False, fontsize=8)
    
    plt.savefig(file_path, transparent=True, dpi=300, bbox_inches='tight')
    plt.close(fig)

def create_visitor_type_chart(colors, file_path):
    """Generates the 'Visitor By User Type' bar chart."""
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(3, 2))
    
    users = ['New', 'Returning']
    counts = [70, 30]
    ax.bar(users, counts, color=[colors['dark_purple'], colors['light_purple']], width=0.5)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.set_visible(False)
    ax.tick_params(axis='x', which='both', bottom=False, labelsize=9, labelcolor=colors['gray_text'])
    
    for i, v in enumerate(counts):
        ax.text(i, v + 2, str(v), color=colors['gray_text'], ha='center', fontsize=9)
        
    plt.savefig(file_path, transparent=True, dpi=300, bbox_inches='tight')
    plt.close(fig)

def create_weekly_visits_chart(colors, file_path):
    """Generates the 'Visits By Week Of Year' area chart."""
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(3.5, 2))
    
    weeks = [f'W{i}' for i in range(1, 15)]
    visits = [5, 8, 12, 10, 15, 25, 30, 28, 45, 35, 22, 18, 15, 10]
    
    ax.plot(weeks, visits, color=colors['dark_purple'], linewidth=2)
    ax.fill_between(weeks, visits, color=colors['dark_purple'], alpha=0.8)
    
    ax.set_ylim(0, 50)
    ax.set_ylabel('in (1000s)', fontsize=8, color=colors['gray_text'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='both', which='major', labelsize=8, labelcolor=colors['gray_text'])
    
    plt.xticks(rotation=45)
    plt.savefig(file_path, transparent=True, dpi=300, bbox_inches='tight')
    plt.close(fig)

def create_bounce_rate_chart(colors, file_path):
    """Generates the 'Bounce Rate By Week Of Year' line/scatter chart."""
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(3.5, 2))
    
    weeks = [f'W{i}' for i in range(1, 15)]
    rates = [1.2, 1.8, 3.5, 2.5, 2.8, 2.2, np.nan, 2.5, 1.8, 3.2, np.nan, 2.2, 2.8, 3.0]
    
    ax.plot(weeks, rates, color=colors['dark_purple'], linewidth=1.5)
    ax.scatter(weeks, rates, color=colors['dark_purple'], s=15)
    
    ax.set_ylim(0, 4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='both', which='major', labelsize=8, labelcolor=colors['gray_text'])
    
    plt.xticks(rotation=45)
    plt.savefig(file_path, transparent=True, dpi=300, bbox_inches='tight')
    plt.close(fig)
    
def create_top3_chart(colors, data, title, file_path):
    """Generic function for the three 'Top 3...' horizontal bar charts."""
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(3, 1.8))

    labels = list(data.keys())
    values = list(data.values())
    
    bars = ax.barh(labels, values, color=[colors['dark_purple'], colors['teal'], colors['blue']][0:len(labels)])
    
    ax.invert_yaxis()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.xaxis.set_visible(False)
    ax.tick_params(axis='y', which='both', left=False, labelsize=9, labelcolor=colors['gray_text'])
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + max(values) * 0.05, bar.get_y() + bar.get_height()/2, f'{int(width)}%', 
                va='center', ha='left', color=colors['gray_text'], fontsize=9)
    
    ax.set_xlim(0, max(values) * 1.2)
    plt.savefig(file_path, transparent=True, dpi=300, bbox_inches='tight')
    plt.close(fig)

# --- Main Slide Creation Function ---

def create_slide(output_pptx_path: str):
    """
    Creates a PPTX file reproducing the Modern Grid-Based KPI Dashboard.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Define Color Palette ---
    colors = {
        'bg': RGBColor(242, 242, 242),
        'text': RGBColor(89, 89, 89),
        'gray_text': RGBColor(100, 100, 100),
        'dark_purple': (102/255, 78/255, 163/255),
        'light_purple': (170/255, 153/255, 204/255),
        'teal': (26/255, 175/255, 154/255),
        'teal_light': (128/255, 204/255, 195/255),
        'blue': (93/255, 133/255, 190/255),
        'purple_light': (204/255, 170/255, 238/255),
        'kpi_purple': RGBColor(128, 100, 162),
    }

    # Set slide background color
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = colors['bg']

    # --- Add Slide Title ---
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12), Inches(0.5))
    title_tf = title_shape.text_frame
    p = title_tf.paragraphs[0]
    p.text = "Business KPI Dashboard Showing Weekly Visits Bounce Rate"
    p.font.name = 'Calibri'
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = colors['text']

    # --- Helper function to add chart with title ---
    def add_chart_with_title(title, left, top, img_path):
        title_shape = slide.shapes.add_textbox(left, top, Inches(4), Inches(0.3))
        p = title_shape.text_frame.paragraphs[0]
        p.text = title
        p.font.name = 'Calibri'
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = colors['text']
        slide.shapes.add_picture(img_path, left, top + Inches(0.35))
    
    # --- Generate and Place Charts ---
    chart_paths = {
        'traffic': 'traffic_sources.png', 'visitor': 'visitor_type.png',
        'visits': 'weekly_visits.png', 'bounce': 'bounce_rate.png',
        'channels': 'top_channels.png', 'campaigns': 'top_campaigns.png', 'pages': 'top_pages.png'
    }

    create_traffic_sources_chart({k: v for k, v in colors.items() if isinstance(v, tuple)}, chart_paths['traffic'])
    add_chart_with_title('Traffic Sources', Inches(0.5), Inches(1.0), chart_paths['traffic'])

    create_visitor_type_chart({k: v for k, v in colors.items() if isinstance(v, tuple)}, chart_paths['visitor'])
    add_chart_with_title('Visitor By User Type', Inches(4.7), Inches(1.0), chart_paths['visitor'])
    
    create_weekly_visits_chart({k: v for k, v in colors.items() if isinstance(v, tuple)}, chart_paths['visits'])
    add_chart_with_title('Visits By Week Of Year', Inches(0.5), Inches(3.0), chart_paths['visits'])
    
    create_bounce_rate_chart({k: v for k, v in colors.items() if isinstance(v, tuple)}, chart_paths['bounce'])
    add_chart_with_title('Bounce Rate By Week Of Year', Inches(4.7), Inches(3.0), chart_paths['bounce'])

    top3_channels_data = {'Organic': 20, 'Paid Search': 12, 'Direct': 8}
    create_top3_chart({k: v for k, v in colors.items() if isinstance(v, tuple)}, top3_channels_data, 'Top 3 Channels By conversion', chart_paths['channels'])
    add_chart_with_title('Top 3 Channels By conversion', Inches(0.5), Inches(5.1), chart_paths['channels'])
    
    top3_campaigns_data = {'Campaign 3': 20, 'Campaign 2': 15, 'Campaign 1': 10}
    create_top3_chart({k: v for k, v in colors.items() if isinstance(v, tuple)}, top3_campaigns_data, 'Top 3 campaigns by conversion', chart_paths['campaigns'])
    add_chart_with_title('Top 3 campaigns by conversion', Inches(3.9), Inches(5.1), chart_paths['campaigns'])

    top3_pages_data = {'Page 3': 30, 'Page 2': 20, 'Page 1': 10}
    create_top3_chart({k: v for k, v in colors.items() if isinstance(v, tuple)}, top3_pages_data, 'Top 3 pages by conversion', chart_paths['pages'])
    add_chart_with_title('Top 3 pages by conversion', Inches(7.3), Inches(5.1), chart_paths['pages'])

    # --- Helper function for KPI cards ---
    def add_kpi_card(top, value_text, label_text, icon_char, color):
        card = slide.shapes.add_shape(1, Inches(10.2), top, Inches(2.8), Inches(0.8)) # 1 is rect
        card.fill.solid()
        card.fill.fore_color.rgb = color
        card.line.fill.background()

        # Icon
        icon_box = slide.shapes.add_textbox(Inches(12.3), top, Inches(0.6), Inches(0.8))
        icon_tf = icon_box.text_frame
        icon_tf.margin_left = icon_tf.margin_right = icon_tf.margin_top = icon_tf.margin_bottom = 0
        p_icon = icon_tf.paragraphs[0]
        p_icon.text = icon_char
        p_icon.font.name = 'Segoe UI Symbol'
        p_icon.font.size = Pt(32)
        p_icon.font.color.rgb = RGBColor(255, 255, 255)
        p_icon.alignment = PP_ALIGN.CENTER

        # Value
        value_box = slide.shapes.add_textbox(Inches(10.3), top + Inches(0.05), Inches(2.0), Inches(0.5))
        value_tf = value_box.text_frame
        value_tf.margin_left = value_tf.margin_right = value_tf.margin_top = value_tf.margin_bottom = 0
        p_value = value_tf.paragraphs[0]
        p_value.text = value_text
        p_value.font.name = 'Calibri'
        p_value.font.size = Pt(22)
        p_value.font.bold = True
        p_value.font.color.rgb = RGBColor(255, 255, 255)

        # Label
        label_box = slide.shapes.add_textbox(Inches(10.3), top + Inches(0.45), Inches(2.0), Inches(0.3))
        label_tf = label_box.text_frame
        label_tf.margin_left = label_tf.margin_right = label_tf.margin_top = label_tf.margin_bottom = 0
        p_label = label_tf.paragraphs[0]
        p_label.text = label_text
        p_label.font.name = 'Calibri'
        p_label.font.size = Pt(10)
        p_label.font.color.rgb = RGBColor(255, 255, 255)

    # --- Add KPI Cards ---
    kpi_data = [
        (Inches(1.0), "2,035,687", "Visits", "👤", RGBColor.from_string('1AA999')),
        (Inches(1.9), "96 sec", "Avg. Session Duration", "🕒", RGBColor.from_string('1AA999')),
        (Inches(2.8), "2.2 Pages", "Per Visit", "👁️", RGBColor.from_string('1AA999')),
        (Inches(3.7), "58%", "Bounce Rate", "⚠️", colors['kpi_purple']),
        (Inches(4.6), "2,354,565", "Page Views", "📄", colors['kpi_purple']),
        (Inches(5.5), "13%", "Goal Conversion", "🚩", colors['kpi_purple']),
    ]
    for top, value, label, icon, color in kpi_data:
        add_kpi_card(top, value, label, icon, color)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example of how to run the function
if __name__ == '__main__':
    create_slide("Business_KPI_Dashboard.pptx")
