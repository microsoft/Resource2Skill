import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.dml import MSO_THEME_COLOR

def create_slide(
    output_pptx_path: str,
    title_text: str = "PRESENTATION AGENDA",
    agenda_items: list = None,
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a 4-point staggered honeycomb agenda.

    Args:
        output_pptx_path (str): The path to save the generated PPTX file.
        title_text (str): The main title for the slide.
        agenda_items (list): A list of strings for the agenda points.
                             Should contain exactly 4 items.

    Returns:
        str: The path to the saved PPTX file.
    """
    # Use default agenda items if none are provided
    if agenda_items is None or len(agenda_items) != 4:
        agenda_items = [
            "Introduction & Overview",
            "Key Findings & Analysis",
            "Strategic Recommendations",
            "Q&A and Next Steps",
        ]

    # --- Presentation and Slide Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # --- Color and Font Definitions ---
    colors = {
        "red": RGBColor(217, 82, 88),
        "light_blue": RGBColor(163, 221, 212),
        "medium_blue": RGBColor(78, 128, 152),
        "dark_blue": RGBColor(45, 85, 122),
        "white": RGBColor(255, 255, 255),
        "black": RGBColor(0, 0, 0),
    }

    # --- Slide Background ---
    background = slide.background
    background.fill.solid()
    background.fill.fore_color.rgb = colors["white"]
    
    # --- Layer 1: Header ---
    header_bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, Inches(0.8)
    )
    header_bar.fill.solid()
    header_bar.fill.fore_color.rgb = colors["black"]
    header_bar.line.fill.background()

    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.1), prs.slide_width - Inches(1), Inches(0.6))
    p = title_box.text_frame.paragraphs[0]
    p.text = title_text
    p.font.name = "Calibri Light"
    p.font.size = Pt(32)
    p.font.color.rgb = colors["white"]
    p.alignment = PP_ALIGN.LEFT
    
    # --- Shape and Layout Definitions ---
    hex_size = Inches(2.3)
    # The overlap factor (0.75 means 25% overlap)
    x_stagger = hex_size * 0.75 
    # Vertical distance for hexagons with flat tops/bottoms
    y_stagger = hex_size * 0.866 

    start_left = Inches(1.5)
    start_top = Inches(1.5)

    # Positions for the 4 hexagons in a 2x2 staggered grid
    positions = [
        {"left": start_left, "top": start_top, "color": colors["red"]},
        {"left": start_left + x_stagger, "top": start_top, "color": colors["light_blue"]},
        {"left": start_left, "top": start_top + y_stagger, "color": colors["medium_blue"]},
        {"left": start_left + x_stagger, "top": start_top + y_stagger, "color": colors["dark_blue"]},
    ]

    banner_height = Inches(1.2)
    banner_width = Inches(7.5)
    
    # --- Layer 2: Rectangular Banners (created first to be in the back) ---
    banner_shapes = []
    for i, pos in enumerate(positions):
        banner_left = pos["left"] + hex_size * 0.5
        banner_top = pos["top"] + (hex_size - banner_height) / 2
        banner = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, banner_left, banner_top, banner_width, banner_height
        )
        banner.fill.solid()
        banner.fill.fore_color.rgb = pos["color"]
        banner.line.fill.background()
        banner_shapes.append(banner)

    # --- Layer 3: Hexagons and Numbers ---
    for i, pos in enumerate(positions):
        # Add the hexagon
        hexagon = slide.shapes.add_shape(
            MSO_SHAPE.HEXAGON, pos["left"], pos["top"], hex_size, hex_size
        )
        hexagon.fill.solid()
        hexagon.fill.fore_color.rgb = pos["color"]
        
        # Add the thick white outline
        hexagon.line.color.rgb = colors["white"]
        hexagon.line.width = Pt(4)

        # Add the number inside the hexagon
        num_box = slide.shapes.add_textbox(pos["left"], pos["top"], hex_size, hex_size)
        num_frame = num_box.text_frame
        num_frame.margin_bottom = Inches(0)
        num_frame.margin_top = Inches(0)
        num_frame.margin_left = Inches(0)
        num_frame.margin_right = Inches(0)
        p_num = num_frame.paragraphs[0]
        p_num.text = f"0{i+1}"
        p_num.font.name = "Calibri (Body)"
        p_num.font.size = Pt(40)
        p_num.font.bold = True
        p_num.font.color.rgb = colors["white"]
        p_num.alignment = PP_ALIGN.CENTER
        num_frame.vertical_anchor = PP_ALIGN.CENTER

    # --- Layer 4: Agenda Item Text on Banners ---
    for i, banner in enumerate(banner_shapes):
        text_frame = banner.text_frame
        text_frame.clear()
        p_agenda = text_frame.paragraphs[0]
        p_agenda.text = agenda_items[i]
        p_agenda.font.name = "Calibri"
        p_agenda.font.size = Pt(20)
        p_agenda.font.color.rgb = colors["white"]
        p_agenda.alignment = PP_ALIGN.LEFT
        text_frame.vertical_anchor = PP_ALIGN.CENTER
        text_frame.margin_left = hex_size * 0.7 # Add padding to avoid text overlapping the hexagon

    # --- Save the Presentation ---
    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
if __name__ == '__main__':
    file_path = "staggered_honeycomb_agenda.pptx"
    create_slide(
        file_path,
        title_text="QUARTERLY BUSINESS REVIEW",
        agenda_items=[
            "Financial Performance Review",
            "Marketing & Sales Update",
            "Product Roadmap & Development",
            "Strategic Initiatives for Next Quarter"
        ]
    )
    # On Windows, you might want to open the file automatically to check it.
    if os.name == 'nt':
        os.startfile(file_path)

