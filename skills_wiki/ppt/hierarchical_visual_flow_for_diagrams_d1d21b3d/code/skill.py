import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from lxml import etree

def _set_shape_alpha(shape, alpha):
    """
    Sets the alpha (transparency) of a shape's fill.
    Alpha is a float between 0 (transparent) and 1 (opaque).
    """
    if not (0 <= alpha <= 1):
        raise ValueError("Alpha must be between 0 and 1")

    ts = shape.fill._xPr.solidFill
    srgbClr = ts.get_or_add_srgbClr()
    # Add alpha element
    alpha_val = int(alpha * 100000)
    alpha_el = etree.SubElement(srgbClr, "{http://schemas.openxmlformats.org/drawingml/2006/main}alpha", val=str(alpha_val))


def create_slide(
    output_pptx_path: str,
    title_text: str = "印象山水大酒店总人员组织架构图",
    chart_data=None,
    theme_colors=None,
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a visually enhanced organizational chart.
    
    This function reproduces the hierarchical styling with varying fills,
    colors, and curved connectors as demonstrated in the tutorial.
    
    Returns: path to the saved PPTX file.
    """
    from pptx.shapes.freeform import FreeformBuilder

    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Default Data & Styling ---
    if chart_data is None:
        chart_data = {
            "总经理 ×1": {
                "children": ["财务部", "总经理助理 ×1"],
                "level": 0, "pos": (7.5, 0.5), "size": (2, 0.6)
            },
            "总经理助理 ×1": {
                "children": ["工程部主管", "人事部主管", "营销部经理", "保安部主管", "房务经理", "餐饮经理"],
                "level": 0, "pos": (7.5, 1.5), "size": (2.2, 0.6)
            },
            "财务部": {"children": ["会计", "出纳", "采购员", "网管", "收银员"], "level": 1, "pos": (1, 1.5), "size": (1.8, 0.6)},
            "工程部主管": {"children": ["水电工"], "level": 1, "pos": (3.5, 2.8)},
            "人事部主管": {"children": ["驾驶员", "人事劳资专员", "后勤专员"], "level": 1, "pos": (5.5, 2.8)},
            "营销部经理": {"children": ["营销区域经理", "美工", "网络计调"], "level": 1, "pos": (7.5, 2.8)},
            "保安部主管": {"children": ["保安员"], "level": 1, "pos": (9.5, 2.8)},
            "房务经理": {"children": ["楼层主管", "前厅主管"], "level": 1, "pos": (11.5, 2.8)},
            "餐饮经理": {"children": ["厨师长", "餐饮主管"], "level": 1, "pos": (13.5, 2.8)},
            # Level 2
            "会计": {"level": 2, "pos": (0.5, 2.8)}, "出纳": {"level": 2, "pos": (0.5, 3.5)},
            "采购员": {"level": 2, "pos": (1.5, 2.8)}, "网管": {"level": 2, "pos": (1.5, 3.5)},
            "收银员": {"level": 2, "pos": (0.5, 4.2)},
            "水电工": {"level": 2, "pos": (3.5, 4.2)},
            "驾驶员": {"level": 2, "pos": (5, 4.2)}, "人事劳资专员": {"level": 2, "pos": (6, 4.2)}, "后勤专员": {"level": 2, "pos": (5.5, 4.9)},
            "营销区域经理": {"level": 2, "pos": (7.5, 4.2)}, "美工": {"level": 2, "pos": (7, 4.9)}, "网络计调": {"level": 2, "pos": (8, 4.9)},
            "保安员": {"level": 2, "pos": (9.5, 4.2)},
            "楼层主管": {"children": ["PA技工", "PA服务员"], "level": 2, "pos": (11, 4.2)}, "前厅主管": {"children": ["前台接待员"], "level": 2, "pos": (12, 4.2)},
            "厨师长": {"children": ["厨师", "洗碗工"], "level": 2, "pos": (13.5, 4.2)}, "餐饮主管": {"children": ["厅面领班", "传菜领班"], "level": 2, "pos": (14.5, 4.2)},
            # Level 3
            "PA技工": {"level": 3, "pos": (10.8, 5.2)}, "PA服务员": {"level": 3, "pos": (10.8, 5.9)},
            "前台接待员": {"level": 3, "pos": (12, 5.2)},
            "厨师": {"level": 3, "pos": (13.3, 5.2)}, "洗碗工": {"level": 3, "pos": (13.3, 5.9)},
            "厅面领班": {"level": 3, "pos": (14.7, 5.2)}, "传菜领班": {"level": 3, "pos": (14.7, 5.9)},
        }

    if theme_colors is None:
        theme_colors = {
            0: RGBColor(18, 107, 103),  # Darkest Teal
            1: RGBColor(44, 150, 145),  # Medium Teal
            2: RGBColor(173, 212, 210), # Light Teal
            3: RGBColor(220, 235, 234)  # Lightest Teal / Outline
        }
    
    # --- Title ---
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), prs.slide_width - Inches(1), Inches(0.5))
    title_shape.text_frame.text = title_text
    title_shape.text_frame.paragraphs[0].font.size = Pt(24)
    title_shape.text_frame.paragraphs[0].font.bold = True

    # --- Draw Shapes (Nodes) ---
    nodes = {}
    for name, data in chart_data.items():
        level = data.get("level", 0)
        x, y = data.get("pos", (1, 1))
        w, h = data.get("size", (1.8, 0.5))
        
        shape = slide.shapes.add_shape(187, Inches(x), Inches(y), Inches(w), Inches(h)) # 187 is rounded rectangle
        
        # Text
        tf = shape.text_frame
        tf.text = name
        p = tf.paragraphs[0]
        p.font.size = Pt(12)
        p.alignment = 1 # Center
        
        # Styling based on level
        if level <= 1:
            shape.fill.solid()
            shape.fill.fore_color.rgb = theme_colors[level]
            p.font.color.rgb = RGBColor(255, 255, 255)
            shape.line.fill.background()
        elif level == 2:
            shape.fill.solid()
            shape.fill.fore_color.rgb = theme_colors[level]
            _set_shape_alpha(shape, 0.3)
            p.font.color.rgb = RGBColor(0, 0, 0)
            shape.line.fill.background()
        else: # level 3 and beyond
            shape.fill.background()
            shape.line.color.rgb = theme_colors[2]
            shape.line.width = Pt(1.5)
            p.font.color.rgb = RGBColor(0, 0, 0)

        nodes[name] = shape

    # --- Draw Connectors ---
    for parent_name, parent_data in chart_data.items():
        if "children" in parent_data:
            parent_node = nodes[parent_name]
            parent_cx = parent_node.left + parent_node.width / 2
            parent_cy_bottom = parent_node.top + parent_node.height
            
            for child_name in parent_data["children"]:
                child_node = nodes[child_name]
                child_cx = child_node.left + child_node.width / 2
                child_cy_top = child_node.top
                
                with FreeformBuilder(
                    slide.shapes, parent_cx, parent_cy_bottom, 1, 1
                ) as builder:
                    mid_y = parent_cy_bottom + (child_cy_top - parent_cy_bottom) / 2
                    builder.add_line_segments([(parent_cx, mid_y)])
                    builder.add_line_segments([(child_cx, mid_y)])
                    builder.add_line_segments([(child_cx, child_cy_top)])
                
                line = builder.shape
                line.line.color.rgb = RGBColor(180, 180, 180)
                line.line.width = Pt(1)

    prs.save(output_pptx_path)
    return output_pptx_path

