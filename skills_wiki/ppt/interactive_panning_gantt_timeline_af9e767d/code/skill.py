import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.oxml import parse_xml, OxmlElement
from pptx.oxml.ns import qn

def add_morph_transition(slide):
    """Injects the Morph transition into a slide's XML."""
    # Create transition elements
    transition = OxmlElement('p:transition')
    transition.set('spd', '1500')  # Speed/duration
    morph = OxmlElement('p:morph')
    transition.append(morph)
    
    # Safely insert after cSld/clrMapOvr
    clrMapOvr = slide.element.find(qn('p:clrMapOvr'))
    if clrMapOvr is not None:
        clrMapOvr.addnext(transition)
    else:
        slide.element.insert(1, transition)

def apply_soft_shadow(shape):
    """Applies a modern, soft UI shadow to a shape via XML."""
    spPr = shape.element.spPr
    effectLst = OxmlElement('a:effectLst')
    outerShdw = OxmlElement('a:outerShdw')
    outerShdw.set('blurRad', '150000')    # Blur radius
    outerShdw.set('dist', '50000')        # Distance
    outerShdw.set('dir', '5400000')       # Angle (90 degrees down)
    outerShdw.set('algn', 'b')            # Alignment
    
    srgbClr = OxmlElement('a:srgbClr')
    srgbClr.set('val', '000000')          # Black shadow
    alpha = OxmlElement('a:alpha')
    alpha.set('val', '15000')             # 15% opacity
    srgbClr.append(alpha)
    outerShdw.append(srgbClr)
    effectLst.append(outerShdw)
    spPr.append(effectLst)

def build_timeline_view(prs, offset_inches=0):
    """
    Builds a single state of the timeline. 
    By creating multiple slides with different offset_inches, Morph handles the scrolling.
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
    
    # Base dimensions
    mask_width = Inches(2.5)
    header_height = Inches(1.5)
    row_height = Inches(0.8)
    col_width = Inches(1.0)
    
    # 1. DRAW SCROLLING BACKGROUND (Grid lines)
    # Layered at the very bottom. Affected by offset.
    num_cols = 20 # Spanning way past the screen
    for i in range(num_cols):
        x_pos = mask_width + Inches(i * col_width.inches) + Inches(offset_inches)
        # Only draw if roughly near or on screen to save resources
        if -Inches(2) < x_pos < Inches(15):
            line = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, 
                x_pos, header_height, Pt(1), Inches(6)
            )
            line.fill.solid()
            line.fill.fore_color.rgb = RGBColor(230, 230, 230)
            line.line.fill.background()
            
            # Add Month/Week headers attached to the grid
            tx_box = slide.shapes.add_textbox(x_pos, header_height - Inches(0.4), col_width, Inches(0.4))
            tf = tx_box.text_frame
            tf.text = f"Wk {i+1}"
            tf.paragraphs[0].font.size = Pt(10)
            tf.paragraphs[0].font.color.rgb = RGBColor(100, 100, 100)

    # 2. DRAW SCROLLING FOREGROUND (Task Bars)
    # Affected by offset.
    tasks = [
        {"name": "Research & Discovery", "start_wk": 1, "duration": 6, "color": (213, 245, 227)}, # Mint
        {"name": "Design Concepts",      "start_wk": 5, "duration": 8, "color": (255, 218, 185)}, # Peach
        {"name": "Production & Build",   "start_wk": 10, "duration": 7, "color": (174, 214, 241)} # Blue
    ]
    
    for idx, t in enumerate(tasks):
        y_pos = header_height + Inches(idx * row_height.inches) + Inches(0.2)
        x_pos = mask_width + Inches((t["start_wk"] - 1) * col_width.inches) + Inches(offset_inches)
        width = Inches(t["duration"] * col_width.inches)
        
        task_bar = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            x_pos, y_pos, width, Inches(0.4)
        )
        task_bar.fill.solid()
        task_bar.fill.fore_color.rgb = RGBColor(*t["color"])
        task_bar.line.fill.background()
        apply_soft_shadow(task_bar)
        
        tf = task_bar.text_frame
        tf.text = f"  {t['name']}"
        tf.paragraphs[0].font.size = Pt(12)
        tf.paragraphs[0].font.color.rgb = RGBColor(50, 50, 50)
        tf.paragraphs[0].font.bold = True

    # 3. DRAW THE MASK
    # A solid white rectangle that covers the left side of the screen.
    # Everything drawn before this step slides UNDER this mask.
    mask = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        Inches(0), header_height - Inches(0.5), mask_width, Inches(6.5)
    )
    mask.fill.solid()
    mask.fill.fore_color.rgb = RGBColor(255, 255, 255)
    mask.line.fill.background()
    
    # 4. DRAW STATIC LEFT PANEL (Row Headers over the mask)
    for idx, t in enumerate(tasks):
        y_pos = header_height + Inches(idx * row_height.inches) + Inches(0.2)
        tx_box = slide.shapes.add_textbox(Inches(0.2), y_pos, mask_width - Inches(0.4), Inches(0.4))
        tf = tx_box.text_frame
        tf.text = f"{idx+1}. {t['name']}"
        tf.paragraphs[0].font.size = Pt(14)
        tf.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
        
    # 5. DRAW STATIC TOP NAVIGATION
    nav_bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        Inches(0), Inches(0), prs.slide_width, header_height - Inches(0.5)
    )
    nav_bg.fill.solid()
    nav_bg.fill.fore_color.rgb = RGBColor(255, 255, 255)
    nav_bg.line.fill.background()

    title = slide.shapes.add_textbox(Inches(0.2), Inches(0.2), Inches(3), Inches(0.8))
    title.text_frame.text = "PROJECT TIMELINE"
    title.text_frame.paragraphs[0].font.size = Pt(24)
    title.text_frame.paragraphs[0].font.bold = True

    # Add Quarter buttons
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    for i, q in enumerate(quarters):
        btn = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(3.5 + i * 0.8), Inches(0.3), Inches(0.6), Inches(0.4)
        )
        # Highlight active quarter based on offset
        is_active = (i == 0 and offset_inches == 0) or (i == 1 and offset_inches != 0)
        
        if is_active:
            btn.fill.solid()
            btn.fill.fore_color.rgb = RGBColor(0, 0, 0)
            btn.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        else:
            btn.fill.solid()
            btn.fill.fore_color.rgb = RGBColor(240, 240, 240)
            btn.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
            
        btn.line.fill.background()
        btn.text_frame.text = q
        btn.text_frame.paragraphs[0].font.size = Pt(12)

    return slide


def create_slide(output_pptx_path: str, **kwargs) -> str:
    """
    Create a PPTX file reproducing the Interactive Panning Gantt Timeline effect.
    Generates two slides to demonstrate the Morph panning functionality.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Slide 1: Base View (Q1)
    slide_1 = build_timeline_view(prs, offset_inches=0)
    add_morph_transition(slide_1)
    
    # Slide 2: Panned View (Q2) - Grid and tasks move left by 6 inches
    slide_2 = build_timeline_view(prs, offset_inches=-6)
    add_morph_transition(slide_2)

    prs.save(output_pptx_path)
    return output_pptx_path

if __name__ == "__main__":
    create_slide("panning_timeline.pptx")
