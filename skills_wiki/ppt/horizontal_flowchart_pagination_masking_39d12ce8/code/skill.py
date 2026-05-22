import os
import tempfile
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN
from PIL import Image

def create_slide(
    output_pptx_path: str,
    title_text: str = "Diagnostic Guideline",
    body_text: str = "Definitive diagnosis of HAE Types I and II requires measurement of C1-INH and C4 levels.\n\nC1-INH function + Genetic testing is NOT essential.",
    accent_color: tuple = (237, 125, 49),  # Orange accent
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Horizontal Flowchart Pagination & Masking" effect.
    Generates two slides:
      Slide 1: Overview of the Flowchart.
      Slide 2: Focus mode (Masked inactive areas + prominent annotation box).
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Define colors
    ACCENT_COLOR = RGBColor(*accent_color)
    BASE_FILL = RGBColor(242, 242, 242)
    BASE_LINE = RGBColor(217, 217, 217)
    TEXT_DARK = RGBColor(64, 64, 64)
    TEXT_LIGHT = RGBColor(255, 255, 255)
    
    # Define Flowchart Data (Medical Guideline Example)
    nodes = {
        "root": {"text": "Suspicion of\nHAE", "pos": (0.5, 3.25), "size": (2.0, 1.0)},
        "type1": {"text": "Type I\nC1-INH Func. ↓\nC4 level ↓", "pos": (4.0, 1.0), "size": (2.2, 1.2)},
        "type2": {"text": "Type II\nC1-INH Func. ↓\nC1-INH level Normal\nC4 level ↓", "pos": (4.0, 3.15), "size": (2.2, 1.2)},
        "normal": {"text": "Normal C1-INH\nC1-INH Func. Normal\nC4 level Normal", "pos": (4.0, 5.3), "size": (2.2, 1.2)},
        "confirm": {"text": "HAE-I\nConfirm by repeating\nblood test", "pos": (7.5, 1.0), "size": (2.5, 1.2)}
    }
    
    edges = [
        ("root", "type1"),
        ("root", "type2"),
        ("root", "normal"),
        ("type1", "confirm")
    ]
    
    active_nodes = ["root", "type1", "confirm"]
    active_edges = [("root", "type1"), ("type1", "confirm")]

    # Helper function to draw the flowchart
    def draw_flowchart(slide, draw_active=True, draw_inactive=True):
        shape_refs = {}
        
        # Draw edges
        for start_id, end_id in edges:
            is_active_edge = (start_id, end_id) in active_edges
            if (is_active_edge and not draw_active) or (not is_active_edge and not draw_inactive):
                continue
                
            n1 = nodes[start_id]
            n2 = nodes[end_id]
            
            # Calculate connection points (Right of start, Left of end)
            x1 = Inches(n1["pos"][0] + n1["size"][0])
            y1 = Inches(n1["pos"][1] + n1["size"][1] / 2)
            x2 = Inches(n2["pos"][0])
            y2 = Inches(n2["pos"][1] + n2["size"][1] / 2)
            
            connector = slide.shapes.add_connector(MSO_CONNECTOR.ELBOW, x1, y1, x2, y2)
            line = connector.line
            if is_active_edge:
                line.color.rgb = ACCENT_COLOR
                line.width = Pt(3)
            else:
                line.color.rgb = BASE_LINE
                line.width = Pt(1.5)

        # Draw nodes
        for node_id, data in nodes.items():
            is_active_node = node_id in active_nodes
            if (is_active_node and not draw_active) or (not is_active_node and not draw_inactive):
                continue

            left, top = Inches(data["pos"][0]), Inches(data["pos"][1])
            width, height = Inches(data["size"][0]), Inches(data["size"][1])
            
            shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
            
            # Adjust rounded corner radius
            shape.adjustments[0] = 0.15 
            
            shape.text = data["text"]
            tf = shape.text_frame
            tf.word_wrap = True
            
            for paragraph in tf.paragraphs:
                paragraph.alignment = PP_ALIGN.CENTER
                paragraph.font.name = "Arial"
                paragraph.font.size = Pt(14)
                if is_active_node:
                    paragraph.font.bold = True
                    paragraph.font.color.rgb = TEXT_LIGHT
                else:
                    paragraph.font.color.rgb = TEXT_DARK
            
            if is_active_node:
                shape.fill.solid()
                shape.fill.fore_color.rgb = ACCENT_COLOR
                shape.line.fill.background()
            else:
                shape.fill.solid()
                shape.fill.fore_color.rgb = BASE_FILL
                shape.line.color.rgb = BASE_LINE
                shape.line.width = Pt(1)

    # ==========================================
    # SLIDE 1: Overview Flowchart
    # ==========================================
    slide_layout = prs.slide_layouts[6] # Blank
    slide1 = prs.slides.add_slide(slide_layout)
    
    # Title
    title_box = slide1.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(8), Inches(0.8))
    title_tf = title_box.text_frame
    p = title_tf.add_paragraph()
    p.text = title_text + " - Overview"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    
    # Draw entire flowchart
    draw_flowchart(slide1, draw_active=True, draw_inactive=True)

    # ==========================================
    # SLIDE 2: Focus Mode (Masked + Annotation)
    # ==========================================
    slide2 = prs.slides.add_slide(slide_layout)
    
    # Title
    title_box2 = slide2.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(8), Inches(0.8))
    title_tf2 = title_box2.text_frame
    p2 = title_tf2.add_paragraph()
    p2.text = title_text + " - Detailed Breakdown"
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_DARK

    # 1. Draw inactive parts (Bottom Layer)
    draw_flowchart(slide2, draw_active=False, draw_inactive=True)
    
    # 2. Apply Semi-Transparent Mask using PIL
    mask_opacity = 210  # roughly 82% opacity (255 * 0.82)
    mask_img = Image.new('RGBA', (100, 100), (255, 255, 255, mask_opacity))
    
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        mask_img.save(tmp.name)
        mask_path = tmp.name
        
    # Cover the area below the title
    slide2.shapes.add_picture(mask_path, Inches(0), Inches(1), prs.slide_width, prs.slide_height - Inches(1))
    os.remove(mask_path)
    
    # 3. Draw active parts (Top Layer, over the mask)
    draw_flowchart(slide2, draw_active=True, draw_inactive=False)
    
    # 4. Add the prominent Annotation Box in the masked negative space
    ann_left = Inches(4.5)
    ann_top = Inches(3.0)
    ann_width = Inches(8.3)
    ann_height = Inches(3.5)
    
    ann_box = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, ann_left, ann_top, ann_width, ann_height)
    ann_box.fill.solid()
    ann_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
    ann_box.line.color.rgb = ACCENT_COLOR
    ann_box.line.width = Pt(4)
    
    # Add text to annotation box
    ann_tf = ann_box.text_frame
    ann_tf.word_wrap = True
    ann_tf.margin_left = Inches(0.5)
    ann_tf.margin_right = Inches(0.5)
    ann_tf.margin_top = Inches(0.5)
    
    p3 = ann_tf.paragraphs[0]
    p3.text = body_text.split('\n\n')[0]
    p3.font.size = Pt(24)
    p3.font.bold = True
    p3.font.color.rgb = TEXT_DARK
    
    if len(body_text.split('\n\n')) > 1:
        p4 = ann_tf.add_paragraph()
        p4.text = "\n" + body_text.split('\n\n')[1]
        p4.font.size = Pt(20)
        p4.font.color.rgb = ACCENT_COLOR
        p4.font.bold = True

    prs.save(output_pptx_path)
    return output_pptx_path
