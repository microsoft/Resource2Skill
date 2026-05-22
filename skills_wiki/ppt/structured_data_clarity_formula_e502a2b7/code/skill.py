import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.xmlchemy import OxmlElement


def set_cell_border(cell, border_color="C0C0C0", border_width='12700'):
    """
    Apply a bottom border to a cell using lxml.
    This provides more reliable control than the native python-pptx border API.
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    
    # Bottom border
    lnB = OxmlElement('a:lnB')
    lnB.set('w', border_width)
    lnB.set('cap', 'flat')
    lnB.set('cmpd', 'sng')
    lnB.set('algn', 'ctr')
    
    solidFill = OxmlElement('a:solidFill')
    srgbClr = OxmlElement('a:srgbClr')
    srgbClr.set('val', border_color)
    
    solidFill.append(srgbClr)
    lnB.append(solidFill)
    tcPr.append(lnB)

def create_professional_table_slide(
    output_pptx_path: str,
    title_text: str = "SOHO盈利模式",
    table_data: list = None,
    header_color: tuple = (0, 112, 192), # A professional blue
    highlight_row_index: int = 3,
    highlight_color: tuple = (220, 230, 241), # A light blue
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a professionally styled table based on the 
    Structured Data Clarity Formula.

    Args:
        output_pptx_path: Path to save the generated PPTX file.
        title_text: The title of the slide.
        table_data: A list of lists representing table rows.
        header_color: RGB tuple for the table header background.
        highlight_row_index: 1-based index of the row to highlight.
        highlight_color: RGB tuple for the highlighted row background.

    Returns:
        Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # --- Sample Data from the "SOHO 盈利模式" example ---
    if table_data is None:
        table_data = [
            ["模式", "华润模式", "万达模式", "SOHO模式"],
            ["自持比例", "100%", "视资金情况, 持有优质资源", "全部卖出"],
            ["成功因素", "商业体量大\n品牌资源丰厚\n体验型购物环境", "订单主力店保证快速复制\n以散售物业养持有物业", "潜在商业利好易挖掘\n炒作成功\n划小面积满足投资需求"],
            ["优势", "聚焦休闲及特色餐饮与消费\n保证高增长性租金\n都市资源实现住宅溢价保证现金流", "细化订单主力店缩短招商周期确保物业升值\n住宅、写字楼及散售型物业快速回现\n为千百货带来无利息现金流", "创造商业销售奇迹\n快速回笼资金"],
            ["压力", "现金流压力非常大\n需优质经营团队\n需高质商圈购买力\n价格高、竞争力小", "现金流压力较大\n主力店过多, 租金收益低", "大体量商业成活率不可控\n缺乏统一规划"],
            ["开发策略", "商业现行启动, 带动物业升值, 实现区域价值最大收益", "主力店持有, 招商经营, 带动现金流产品\n现行销售, 资金连续循环", "速战速决短期获利模式, 不利于商业长期经营, 难以实现长效收益"]
        ]

    # --- Add Slide Title ---
    title_shape = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(14), Inches(1))
    title_tf = title_shape.text_frame
    p = title_tf.paragraphs[0]
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(32)
    p.font.color.rgb = RGBColor(50, 50, 50)

    # --- Create and Position Table ---
    rows, cols = len(table_data), len(table_data[0])
    table_shape = slide.shapes.add_table(rows, cols, Inches(1), Inches(1.5), Inches(14), Inches(6))
    table = table_shape.table

    # --- Apply 4-Step Formula ---
    
    # Step 1: Clear Formatting (implicit, we will define our own style)
    # and Step 2: Optimize Alignment & Populate Data
    for r_idx, row_data in enumerate(table_data):
        for c_idx, cell_data in enumerate(row_data):
            cell = table.cell(r_idx, c_idx)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE # Vertical centering for all
            
            # Reset paragraph formatting and set text
            tf = cell.text_frame
            tf.clear()
            
            # Handle multi-line content with bullet points
            lines = str(cell_data).split('\n')
            p = tf.paragraphs[0]
            p.text = lines[0]
            p.font.size = Pt(14)
            p.font.color.rgb = RGBColor(64, 64, 64)

            # Left align by default (for text)
            p.alignment = PP_ALIGN.LEFT

            for line in lines[1:]:
                p = tf.add_paragraph()
                p.text = line
                p.level = 1 # Make it a bullet point
                p.font.size = Pt(14)
                p.font.color.rgb = RGBColor(64, 64, 64)
                p.alignment = PP_ALIGN.LEFT
            
            # Clear default fill
            cell.fill.background()

    # Step 3: Divide Sections
    # Header styling
    for c_idx in range(cols):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(*header_color)
        for p in cell.text_frame.paragraphs:
            p.font.color.rgb = RGBColor(255, 255, 255)
            p.font.bold = True
            p.alignment = PP_ALIGN.CENTER
    
    # Row dividers (thin horizontal lines)
    for r_idx in range(rows -1):
        for c_idx in range(cols):
             set_cell_border(table.cell(r_idx, c_idx), border_color="E0E0E0")


    # Step 4: Highlight Key Points
    if highlight_row_index is not None and 0 < highlight_row_index < rows:
        # Note: The video highlights the "优势" row, which is the 4th row (index 3).
        # We adjust to 0-based index.
        row_to_highlight_idx = highlight_row_index
        for c_idx in range(cols):
            cell = table.cell(row_to_highlight_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(*highlight_color)

    # Adjust column widths (make first column narrower)
    table.columns[0].width = Inches(1.5)
    for i in range(1, cols):
        table.columns[i].width = Inches(4.83)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example of how to run the function:
# create_professional_table_slide(
#     "professional_table_example.pptx",
#     title_text="SOHO盈利模式对比分析",
#     highlight_row_index=3,
#     header_color=(23, 54, 93),
#     highlight_color=(230, 237, 244)
# )
