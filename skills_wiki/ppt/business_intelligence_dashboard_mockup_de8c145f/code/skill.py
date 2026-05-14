import io
import os
import zipfile
import urllib.request
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import squarify
import geopandas
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Define a consistent style for all matplotlib charts
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.labelcolor'] = '#505050'
plt.rcParams['xtick.color'] = '#505050'
plt.rcParams['ytick.color'] = '#505050'
plt.rcParams['text.color'] = '#505050'

# Define a color palette (RGB tuples 0-255)
PALETTE = [
    (57, 98, 172), (115, 178, 98), (247, 182, 72),
    (124, 82, 161), (236, 112, 103), (48, 187, 187)
]
PALETTE_RGB_FLOAT = [(r/255, g/255, b/255) for r, g, b in PALETTE]

def _add_chart_title(slide, left, top, width, text):
    """Helper to add a title above a chart."""
    title_box = slide.shapes.add_textbox(left, top, width, Inches(0.3))
    p = title_box.text_frame.paragraphs[0]
    p.text = text
    p.font.name = 'Segoe UI'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(80, 80, 80)
    p.alignment = PP_ALIGN.LEFT

def _create_kpi_card(slide, left, top, width, height, value_text, label_text):
    """Creates a KPI card on the slide."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(255, 255, 255)
    card.line.fill.solid()
    card.line.fill.fore_color.rgb = RGBColor(220, 220, 220)
    card.line.width = Pt(1)

    val_tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.1), width - Inches(0.4), height / 2)
    p_val = val_tb.text_frame.paragraphs[0]
    p_val.text = value_text
    p_val.font.name = 'Segoe UI Semibold'
    p_val.font.size = Pt(28)
    p_val.font.color.rgb = RGBColor(30, 30, 30)

    lbl_tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.6), width - Inches(0.4), height / 2 - Inches(0.2))
    p_lbl = lbl_tb.text_frame.paragraphs[0]
    p_lbl.text = label_text
    p_lbl.font.name = 'Segoe UI'
    p_lbl.font.size = Pt(11)
    p_lbl.font.color.rgb = RGBColor(120, 120, 120)

def _create_line_chart(data, title):
    """Generates a line chart PNG in a memory buffer."""
    fig, ax = plt.subplots(figsize=(4, 2.5))
    data.plot(kind='line', ax=ax, color=PALETTE_RGB_FLOAT[0], marker='o', legend=None)
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(axis='both', which='major', labelsize=8)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1_000_000:.1f}M'))
    plt.xticks(rotation=0)
    ax.set_xlabel(''), ax.set_ylabel('')
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf

def _create_bar_chart(data, title):
    """Generates a horizontal bar chart PNG."""
    fig, ax = plt.subplots(figsize=(4, 2.5))
    data.sort_values().plot(kind='barh', ax=ax, color=PALETTE_RGB_FLOAT[1], width=0.7)
    ax.spines[['top', 'right', 'bottom']].set_visible(False)
    ax.tick_params(axis='both', which='major', labelsize=9)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0f}%'))
    ax.grid(False)
    ax.set_xlabel(''), ax.set_ylabel('')
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf

def _create_pie_chart(data, title):
    """Generates a pie chart PNG."""
    fig, ax = plt.subplots(figsize=(3, 2.5))
    wedges, texts, autotexts = ax.pie(data, autopct='%1.1f%%', startangle=90, colors=PALETTE_RGB_FLOAT)
    plt.setp(autotexts, size=8, weight="bold", color="white")
    ax.legend(data.index, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
    fig.tight_layout(rect=[0, 0, 0.7, 1])
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf
    
def _create_treemap(data, title):
    """Generates a treemap PNG."""
    fig, ax = plt.subplots(figsize=(4, 2.5))
    squarify.plot(sizes=data.values, label=[f"{i}\n${v/1_000_000:.2f}M" for i, v in data.items()],
                  color=PALETTE_RGB_FLOAT, alpha=0.8, ax=ax, text_kwargs={'fontsize': 8, 'color': 'white'})
    plt.axis('off')
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf


def create_slide(
    output_pptx_path: str,
    title_text: str = "Quarterly Business Review",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a modern Business Intelligence dashboard layout.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 245)
    
    # === Slide Title ===
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12.33), Inches(0.5))
    p = title_box.text_frame.paragraphs[0]
    p.text = title_text
    p.font.name = 'Segoe UI Semibold'
    p.font.size = Pt(24)
    p.font.color.rgb = RGBColor(0, 0, 0)

    # === Sample Data Generation ===
    np.random.seed(0)
    sales_data = pd.Series(
        (1.8 + np.random.rand(12) * 0.8) * 1_000_000,
        index=pd.to_datetime([f'2023-{i}-01' for i in range(1, 13)])
    )
    achievement_data = pd.Series(
        np.random.randint(75, 101, 6),
        index=['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank']
    )
    customer_data = pd.Series(
        [34, 30, 18, 17],
        index=['Corp A', 'Corp B', 'Startup X', 'SMB Inc.']
    )
    product_sales = pd.Series(
        np.random.randint(100000, 500000, 4),
        index=['Product Alpha', 'Product Beta', 'Service Gamma', 'Suite Delta']
    )

    # === Layout: KPI Cards ===
    total_sales = f"${sales_data.sum()/1_000_000:.2f}M"
    avg_achievement = f"{achievement_data.mean():.2f}%"
    num_customers = f"{len(customer_data)}"
    _create_kpi_card(slide, Inches(0.5), Inches(0.8), Inches(3), Inches(1.2), total_sales, "Total Sales")
    _create_kpi_card(slide, Inches(3.7), Inches(0.8), Inches(3), Inches(1.2), avg_achievement, "Avg. Perf. Rate")
    _create_kpi_card(slide, Inches(6.9), Inches(0.8), Inches(3), Inches(1.2), num_customers, "Active Customers")
    _create_kpi_card(slide, Inches(10.1), Inches(0.8), Inches(2.73), Inches(1.2), "Q4", "Current Quarter")

    # === Layout: Charts ===
    # Chart 1: Line Chart
    _add_chart_title(slide, Inches(0.5), Inches(2.2), Inches(4), "Sales Trend by Month")
    line_chart_buf = _create_line_chart(sales_data, "")
    slide.shapes.add_picture(line_chart_buf, Inches(0.5), Inches(2.5), Inches(4))

    # Chart 2: Bar Chart
    _add_chart_title(slide, Inches(4.8), Inches(2.2), Inches(4), "Team Performance Rate")
    bar_chart_buf = _create_bar_chart(achievement_data, "")
    slide.shapes.add_picture(bar_chart_buf, Inches(4.8), Inches(2.5), Inches(4))
    
    # Chart 3: Pie Chart
    _add_chart_title(slide, Inches(9.1), Inches(2.2), Inches(4), "Sales by Customer Segment")
    pie_chart_buf = _create_pie_chart(customer_data, "")
    slide.shapes.add_picture(pie_chart_buf, Inches(9.1), Inches(2.5), Inches(4))

    # Chart 4: Treemap Chart
    _add_chart_title(slide, Inches(0.5), Inches(5.1), Inches(8), "Sales by Product Line")
    treemap_buf = _create_treemap(product_sales, "")
    slide.shapes.add_picture(treemap_buf, Inches(0.5), Inches(4.8), Inches(8.3), height=Inches(2.5))
    
    prs.save(output_pptx_path)
    return output_pptx_path

