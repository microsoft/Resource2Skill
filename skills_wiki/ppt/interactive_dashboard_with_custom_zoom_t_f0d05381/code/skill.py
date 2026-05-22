import os
import io
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.oxml.ns import qn
from pptx.oxml import OxmlElement
from PIL import Image

def create_slide(
    output_pptx_path: str,
    title_text: str = "DASHBOARD SLIDE",
    subtitle_text: str = "WRITE YOUR SUBTITLE HERE",
    **kwargs,
) -> str:
    """
    Creates a PowerPoint presentation with an interactive dashboard slide using custom Slide Zoom triggers.

    This reproduces the core effect of using colored panels with icons as clickable
    buttons that zoom into other slides and back.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # --- Helper Functions ---

    def create_placeholder_slide(prs, title, bg_color):
        """Creates a simple content slide to be the target of a zoom."""
        slide = prs.slides.add_slide(prs.slide_layouts[5])
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = bg_color
        title_shape = slide.shapes.title
        title_shape.text = title
        return slide

    def add_slide_zoom(slide, target_slide, x, y, cx, cy, invisible_img_rid):
        """Injects the XML for a Slide Zoom object into a slide."""
        slide_part = slide.part
        
        # 1. Create relationship to the target slide
        target_slide_part = target_slide.part
        rId = slide_part.relate_to(target_slide_part, "http://schemas.microsoft.com/office/2019/10/relationships/slideZoom")

        # 2. Create the XML structure for the Slide Zoom
        # This structure is complex and derived from inspecting a saved PPTX file.
        
        # <p:grpSp>
        grpSp = OxmlElement('p:grpSp')
        
        # <p:nvGrpSpPr>
        nvGrpSpPr = OxmlElement('p:nvGrpSpPr')
        nvGrpSpPr.append(OxmlElement('p:cNvPr', id="10", name="Group 9"))
        nvGrpSpPr.append(OxmlElement('p:cNvGrpSpPr'))
        nvGrpSpPr.append(OxmlElement('p:nvPr'))
        grpSp.append(nvGrpSpPr)
        
        # <p:grpSpPr>
        grpSpPr = OxmlElement('p:grpSpPr')
        grpSpPr.append(OxmlElement('a:xfrm', rot="0", flipH="0", flipV="0'))
        grpSp.first_child_found_in('p:grpSpPr').append(OxmlElement('a:off', x="0", y="0"))
        grpSp.first_child_found_in('p:grpSpPr').append(OxmlElement('a:ext', cx="0", cy="0"))
        grpSp.first_child_found_in('p:grpSpPr').append(OxmlElement('a:chOff', x="0", y="0"))
        grpSp.first_child_found_in('p:grpSpPr').append(OxmlElement('a:chExt', cx="0", cy="0"))
        grpSp.append(grpSpPr)
        
        # Graphic Frame for the zoom object itself
        graphicFrame = OxmlElement('p:graphicFrame')
        nvGraphicFramePr = OxmlElement('p:nvGraphicFramePr')
        nvGraphicFramePr.append(OxmlElement('p:cNvPr', id="2", name="Slide Zoom"))
        nvGraphicFramePr.append(OxmlElement('p:cNvGraphicFramePr'))
        nvGraphicFramePr.append(OxmlElement('p:nvPr'))
        graphicFrame.append(nvGraphicFramePr)
        
        xfrm = OxmlElement('p:xfrm')
        xfrm.append(OxmlElement('a:off', x=str(x), y=str(y)))
        xfrm.append(OxmlElement('a:ext', cx=str(cx), cy=str(cy)))
        graphicFrame.append(xfrm)

        graphic = OxmlElement('a:graphic')
        graphicData = OxmlElement('a:graphicData', uri="http://schemas.microsoft.com/office/2019/10/relationships/slideZoom")
        zoom = OxmlElement('p14:zoom', xmlns_p14=qn('p14'))
        zoom.set(qn('r:id'), rId)
        zoom.set('returnToZoom', '1') # The magic attribute to return on second click
        graphicData.append(zoom)
        graphic.append(graphicData)
        graphicFrame.append(graphic)
        
        grpSp.append(graphicFrame)
        
        # Picture frame for the invisible image (the trigger)
        pic = OxmlElement('p:pic')
        nvPicPr = OxmlElement('p:nvPicPr')
        nvPicPr.append(OxmlElement('p:cNvPr', id="8", name="Picture 7"))
        nvPicPr.append(OxmlElement('p:cNvPicPr'))
        nvPicPr.append(OxmlElement('p:nvPr'))
        pic.append(nvPicPr)

        blipFill = OxmlElement('p:blipFill')
        blipFill.append(OxmlElement('a:blip', **{qn('r:embed'): invisible_img_rid}))
        blipFill.append(OxmlElement('a:stretch'))
        pic.append(blipFill)
        
        spPr = OxmlElement('p:spPr')
        spPr_xfrm = OxmlElement('a:xfrm')
        spPr_xfrm.append(OxmlElement('a:off', x=str(x), y=str(y)))
        spPr_xfrm.append(OxmlElement('a:ext', cx=str(cx), cy=str(cy)))
        spPr.append(spPr_xfrm)
        spPr.append(OxmlElement('a:prstGeom', prst="rect"))
        pic.append(spPr)
        
        grpSp.append(pic)
        
        slide.shapes._spTree.append(grpSp)


    # --- Slide Creation ---
    
    # 1. Define dashboard layout and colors
    PALETTE = {
        "Insights": RGBColor(74, 172, 255),
        "Process": RGBColor(0, 112, 192),
        "KPI": RGBColor(46, 204, 113),
        "Roadmap": RGBColor(255, 192, 0),
        "Project Status": RGBColor(91, 44, 142),
        "Comparison": RGBColor(189, 195, 199),
        "Data": RGBColor(231, 76, 60),
    }

    # 2. Create the content slides that we will zoom to
    content_slides = [
        create_placeholder_slide(prs, name, color) for name, color in PALETTE.items()
    ]
    
    # 3. Create the main dashboard slide
    dashboard_slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Add main titles
    title_box = dashboard_slide.shapes.add_textbox(Inches(0), Inches(0.25), prs.slide_width, Inches(0.5))
    p = title_box.text_frame.add_paragraph()
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(24)
    p.alignment = 1 # Center

    subtitle_box = dashboard_slide.shapes.add_textbox(Inches(0), Inches(0.6), prs.slide_width, Inches(0.4))
    p = subtitle_box.text_frame.add_paragraph()
    p.text = subtitle_text
    p.font.size = Pt(14)
    p.alignment = 1

    # 4. Create and add the invisible 1x1 PNG to the presentation package
    img_data = io.BytesIO()
    Image.new('RGBA', (1, 1), (0, 0, 0, 0)).save(img_data, 'PNG')
    img_data.seek(0)
    img_part, rId = dashboard_slide.part.add_image_part(img_data)
    invisible_img_rid = rId

    # 5. Define the grid layout and create panels
    panel_width = Inches(3)
    panel_height = Inches(2.5)
    gap = Inches(0.15)
    
    layout = [
        {"name": "Insights", "row": 0, "col": 0, "colspan": 2, "target_idx": 0},
        {"name": "Process", "row": 0, "col": 2, "target_idx": 1},
        {"name": "KPI", "row": 0, "col": 3, "target_idx": 2},
        {"name": "Roadmap", "row": 0, "col": 4, "target_idx": 3},
        {"name": "Project Status", "row": 1, "col": 0, "colspan": 2, "target_idx": 4},
        {"name": "Comparison", "row": 1, "col": 2, "colspan": 2, "target_idx": 5},
        {"name": "Data", "row": 1, "col": 4, "target_idx": 6},
    ]
    
    # Adjusting start position for centering
    total_width = (4 * panel_width) + (4 * gap)
    start_x = (prs.slide_width - total_width) / 2
    start_y = Inches(1.2)
    
    for item in layout:
        w_multiplier = item.get("colspan", 1)
        current_width = panel_width * w_multiplier + gap * (w_multiplier - 1)
        x = start_x + item["col"] * (panel_width + gap)
        y = start_y + item["row"] * (panel_height + gap)
        
        # Add colored rectangle
        rect = dashboard_slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, current_width, panel_height)
        rect.fill.solid()
        rect.fill.fore_color.rgb = PALETTE[item["name"]]
        rect.line.fill.background()
        
        # Add panel title
        title_y = y + Inches(0.2)
        tb = dashboard_slide.shapes.add_textbox(x, title_y, current_width, Inches(0.5))
        p = tb.text_frame.add_paragraph()
        p.text = item["name"].upper()
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.font.size = Pt(14)
        
        # Add the invisible slide zoom on top
        add_slide_zoom(dashboard_slide, content_slides[item['target_idx']], x, y, current_width, panel_height, invisible_img_rid)

    prs.save(output_pptx_path)
    return output_pptx_path

