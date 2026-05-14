import math
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from lxml import etree

# Helper function to inject Open XML for shadow effects
def add_shadow(shape, shadow_type='outer', transparency=75, blur=15, angle=45, distance=5):
    """
    Applies a soft outer shadow to a shape.
    Note: transparency is 0-100%, angle is in degrees, distance/blur in points.
    """
    if not shape:
        return

    shape_xml = shape.element
    effect_lst = shape_xml.find('.//a:effectLst', namespaces=etree.FunctionNamespace(None))
    if effect_lst is None:
        spPr = shape_xml.find('.//p:spPr', namespaces=etree.FunctionNamespace(None))
        if spPr is not None:
            effect_lst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')

    if effect_lst is not None:
        outer_shadow = etree.SubElement(effect_lst, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw')
        outer_shadow.set('blurRad', str(Emu(Pt(blur))))
        outer_shadow.set('dist', str(Emu(Pt(distance))))
        outer_shadow.set('dir', str(int(angle * 60000)))
        outer_shadow.set('algn', 'ctr')
        outer_shadow.set('rotWithShape', '0')

        srgb_clr = etree.SubElement(outer_shadow, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
        srgb_clr.set('val', '000000')
        alpha = etree.SubElement(srgb_clr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha')
        alpha.set('val', str(int((100 - transparency) * 1000)))


# Helper function to set a radial gradient background
def set_radial_background(slide, start_color='FFFFFF', end_color='E0E0E0'):
    """Sets a radial gradient background for a slide using lxml."""
    background = slide.background
    bg_pr = background.element.get_or_add_bgPr()
    grad_fill = OxmlElement('a:gradFill')
    grad_fill.set('rotWithShape', '1')
    
    gs_lst = OxmlElement('a:gsLst')
    gs1 = OxmlElement('a:gs')
    gs1.set('pos', '0')
    srgb_clr1 = OxmlElement('a:srgbClr')
    srgb_clr1.set('val', start_color)
    gs1.append(srgb_clr1)
    
    gs2 = OxmlElement('a:gs')
    gs2.set('pos', '100000')
    srgb_clr2 = OxmlElement('a:srgbClr')
    srgb_clr2.set('val', end_color)
    gs2.append(srgb_clr2)
    
    gs_lst.append(gs1)
    gs_lst.append(gs2)
    
    path = OxmlElement('a:path')
    path.set('path', 'circle')
    fill_to_rect = OxmlElement('a:fillToRect')
    fill_to_rect.set('l', '50000')
    fill_to_rect.set('t', '50000')
    fill_to_rect.set('r', '50000')
    fill_to_rect.set('b', '50000')
    path.append(fill_to_rect)
    
    grad_fill.append(gs_lst)
    grad_fill.append(path)
    
    bg_pr.append(grad_fill)


def create_slide(output_pptx_path: str, **kwargs) -> str:
    """
    Creates a PPTX file with a Radial Petal Infographic for 8 points.
    Returns the path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    set_radial_background(slide, start_color='FFFFFF', end_color='D9D9D9')

    # === Layer 2: Visual Effect (Infographic Shapes) ===
    num_points = 8
    slide_cx = prs.slide_width / 2
    slide_cy = prs.slide_height / 2
    
    # Palette (8 colors)
    colors = [
        RGBColor(0, 176, 240),   # Light Blue
        RGBColor(0, 176, 80),   # Green
        RGBColor(34, 87, 122),  # Dark Teal
        RGBColor(199, 0, 57),   # Burgundy
        RGBColor(255, 87, 51),  # Pink/Red
        RGBColor(255, 195, 0),  # Orange
        RGBColor(128, 128, 128),# Grey
        RGBColor(56, 62, 66),   # Dark Grey
    ]
    
    # Radii for placing the center of each shape
    radius_petal = Inches(2.1)
    radius_overlap = Inches(2.2)
    radius_cap = Inches(3.2)
    
    # Shape dimensions
    petal_w, petal_h = Inches(3.0), Inches(2.8)
    overlap_w, overlap_h = Inches(2.6), Inches(2.4)
    cap_d = Inches(0.8)

    all_shapes = []

    for i in range(num_points):
        angle_deg = (i * 360 / num_points)
        angle_rad_for_pos = math.radians(angle_deg - 90)

        # -- Main Petal Shape --
        petal_cx = slide_cx + radius_petal * math.cos(angle_rad_for_pos)
        petal_cy = slide_cy + radius_petal * math.sin(angle_rad_for_pos)
        petal = slide.shapes.add_shape(
            MSO_SHAPE.PLAQUE,
            petal_cx - petal_w / 2,
            petal_cy - petal_h / 2,
            petal_w, petal_h
        )
        petal.rotation = angle_deg
        petal.adjustments[0] = 0.35  # Adjust corner roundness
        petal.fill.solid()
        petal.fill.fore_color.rgb = colors[i]
        petal.line.fill.background()
        all_shapes.append(petal)

        # -- Overlapping crescent shape --
        # We rotate this by an extra half-step to position it between petals
        overlap_angle_deg = angle_deg - (360 / num_points / 2)
        overlap_angle_rad = math.radians(overlap_angle_deg - 90)
        overlap_cx = slide_cx + radius_overlap * math.cos(overlap_angle_rad)
        overlap_cy = slide_cy + radius_overlap * math.sin(overlap_angle_rad)
        
        # This shape uses the color of the *previous* petal to create the illusion of overlap
        overlap_color = colors[i - 1 if i > 0 else num_points - 1]
        
        overlap = slide.shapes.add_shape(
            MSO_SHAPE.PLAQUE,
            overlap_cx - overlap_w / 2,
            overlap_cy - overlap_h / 2,
            overlap_w, overlap_h
        )
        overlap.rotation = overlap_angle_deg
        overlap.adjustments[0] = 0.5
        overlap.fill.solid()
        overlap.fill.fore_color.rgb = overlap_color
        overlap.line.fill.background()
        all_shapes.append(overlap)
    
    # Re-order shapes to ensure correct layering (bring overlaps to front)
    for shape in slide.shapes:
        if any(s.element == shape.element for s in all_shapes):
             shape.element.getparent().remove(shape.element)
             slide.shapes._spTree.append(shape.element)

    # Add caps and numbers after main shapes are layered
    cap_shapes = []
    for i in range(num_points):
        angle_deg = (i * 360 / num_points)
        angle_rad_for_pos = math.radians(angle_deg - 90)

        # -- Number Cap --
        cap_cx = slide_cx + radius_cap * math.cos(angle_rad_for_pos)
        cap_cy = slide_cy + radius_cap * math.sin(angle_rad_for_pos)
        cap = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            cap_cx - cap_d / 2,
            cap_cy - cap_d / 2,
            cap_d, cap_d
        )
        cap.fill.solid()
        cap.fill.fore_color.rgb = colors[i]
        cap.line.fill.background()
        
        tf = cap.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = str(i + 1)
        run.font.bold = True
        run.font.size = Pt(24)
        run.font.color.rgb = RGBColor(255, 255, 255)
        cap_shapes.append(cap)
        all_shapes.append(cap)
    
    # --- Central Hub ---
    center_hub_d = Inches(2.5)
    center_hub = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        slide_cx - center_hub_d / 2,
        slide_cy - center_hub_d / 2,
        center_hub_d, center_hub_d
    )
    center_hub.fill.solid()
    center_hub.fill.fore_color.rgb = RGBColor(255, 255, 255)
    center_hub.line.fill.background()
    all_shapes.append(center_hub)
    
    # --- Apply Shadows ---
    for shape in all_shapes:
        add_shadow(shape, transparency=70, blur=18, distance=8)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_slide("radial_petal_infographic.pptx")
