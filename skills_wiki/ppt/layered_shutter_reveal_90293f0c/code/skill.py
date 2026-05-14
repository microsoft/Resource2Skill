import os
import requests
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.dml.color import RGBColor
from lxml import etree
from pptx.oxml.ns import qn

def create_slide(
    output_pptx_path: str,
    title_text: str = "无限可能",
    subtitle_text: str = "Young",
    bg_image_url: str = "https://images.unsplash.com/photo-1549880181-56a44cf4a9a5?w=1600&h=900&fit=crop&q=80",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Layered Shutter Reveal visual effect.

    The generated slide contains all visual elements. Animations must be applied manually in PowerPoint:
    1. Select all left panels, add a "Fly Out" animation to the Left.
    2. Select all right panels, add a "Fly Out" animation to the Right.
    3. Select the text boxes, add a "Zoom" entrance animation.
    4. Set all animations to "Start With Previous" and a duration of 1.5s in the Animation Pane.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    SLIDE_WIDTH_EMU = prs.slide_width
    SLIDE_HEIGHT_EMU = prs.slide_height
    
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Utility for XML manipulation ---
    def get_shape_spPr(shape):
        return shape.element.find('.//p:spPr', namespaces=shape.element.nsmap)

    # --- Layer 1: Background Image ---
    try:
        response = requests.get(bg_image_url)
        response.raise_for_status()
        image_stream = BytesIO(response.content)
        # Add the main background image, which other fills will reference
        bg_pic = slide.shapes.add_picture(image_stream, 0, 0, width=prs.slide_width, height=prs.slide_height)
        # Get the relationship ID of the added image
        image_rId = bg_pic.part.relate_to(bg_pic.image.part, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image').rId
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image: {e}. Using a solid background.")
        # Fallback to a dark solid fill for the slide background
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(10, 20, 40)
        image_rId = None # No image to use for fills

    # --- Layer 2: Sliding Panels ---
    num_panels_per_side = 5
    panel_base_width = SLIDE_WIDTH_EMU / (num_panels_per_side * 2 - 2)
    skew_offset = panel_base_width * 0.4
    overlap = 0.5 # Percentage of overlap
    
    # Create panels from center outwards
    for i in range(num_panels_per_side):
        # --- Left Panels ---
        x_pos = (SLIDE_WIDTH_EMU / 2) - (i + 1) * panel_base_width * (1 - overlap) - panel_base_width * 0.2
        shape_width = panel_base_width
        
        # Create a freeform parallelogram
        left_panel = slide.shapes.add_freeform_shape()
        with left_panel.build() as freeform:
            freeform.move_to(x_pos + skew_offset, 0)
            freeform.line_to(x_pos + shape_width + skew_offset, 0)
            freeform.line_to(x_pos + shape_width, SLIDE_HEIGHT_EMU)
            freeform.line_to(x_pos, SLIDE_HEIGHT_EMU)
            freeform.close()

        # --- Right Panels ---
        x_pos_r = (SLIDE_WIDTH_EMU / 2) + i * panel_base_width * (1 - overlap) + panel_base_width * 0.2
        
        right_panel = slide.shapes.add_freeform_shape()
        with right_panel.build() as freeform:
            freeform.move_to(x_pos_r + skew_offset, 0)
            freeform.line_to(x_pos_r + shape_width + skew_offset, 0)
            freeform.line_to(x_pos_r + shape_width, SLIDE_HEIGHT_EMU)
            freeform.line_to(x_pos_r, SLIDE_HEIGHT_EMU)
            freeform.close()

        # Apply effects to both panels created in this loop
        for panel, x_position in [(left_panel, x_pos), (right_panel, x_pos_r)]:
            # Remove default line
            panel.line.fill.background()
            
            # Get the shape's property element
            spPr = get_shape_spPr(panel)

            if image_rId:
                # 1. Apply Picture Fill with Crop (to mimic background fill)
                # Calculate crop percentages * 100000
                crop_l = int((x_position / SLIDE_WIDTH_EMU) * 100000)
                crop_r = int((1.0 - ((x_position + shape_width) / SLIDE_WIDTH_EMU)) * 100000)

                blip_fill = etree.fromstring(f'''
                    <a:blipFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
                        <a:blip r:embed="{image_rId}"/>
                        <a:srcRect l="{crop_l}" t="0" r="{crop_r}" b="0"/>
                        <a:stretch>
                            <a:fillRect/>
                        </a:stretch>
                    </a:blipFill>
                ''')
                spPr.append(blip_fill)

            # 2. Apply Outer Shadow
            shadow_effect = etree.fromstring(f'''
                <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
                    <a:outerShdw blurRad="{Pt(12)}" dist="{Pt(6)}" dir="5400000" rotWithShape="0">
                        <a:srgbClr val="000000">
                            <a:alpha val="50000"/>
                        </a:srgbClr>
                    </a:outerShdw>
                </a:effectLst>
            ''')
            spPr.append(shadow_effect)

    # --- Layer 3: Text & Content ---
    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0), Inches(2.5), width=prs.slide_width, height=Inches(2))
    p = title_box.text_frame.paragraphs[0]
    p.text = title_text
    p.font.name = 'Microsoft YaHei'
    p.font.bold = True
    p.font.size = Pt(96)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = 1 # Center
    
    # Subtitle
    subtitle_box = slide.shapes.add_textbox(Inches(0), Inches(4.2), width=prs.slide_width, height=Inches(1.5))
    p_sub = subtitle_box.text_frame.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.name = 'Segoe Script'
    p_sub.font.bold = False
    p_sub.font.size = Pt(60)
    p_sub.font.color.rgb = RGBColor(255, 255, 255)
    p_sub.alignment = 1 # Center

    # Add shadow to text via XML
    for box in [title_box, subtitle_box]:
        for p in box.text_frame.paragraphs:
            for r in p.runs:
                rPr = r._r.get_or_add_rPr()
                shadow = etree.fromstring(f'''
                    <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
                        <a:outerShdw blurRad="12700" dist="12700" dir="2700000" algn="tl" rotWithShape="0">
                            <a:srgbClr val="000000">
                                <a:alpha val="60000"/>
                            </a:srgbClr>
                        </a:outerShdw>
                    </a:effectLst>
                ''')
                rPr.append(shadow)
    
    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
if __name__ == '__main__':
    file_path = "Layered_Shutter_Reveal.pptx"
    create_slide(file_path)
    print(f"Presentation saved to {file_path}")
    # To view the result, open the file and apply the animations as described in the docstring.
    if os.name == 'nt': # For Windows
        os.startfile(file_path)
