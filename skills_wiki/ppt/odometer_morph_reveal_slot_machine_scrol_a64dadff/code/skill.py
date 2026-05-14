import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.text import MSO_ANCHOR
from PIL import Image, ImageDraw
from lxml import etree

def create_slide(
    output_pptx_path: str,
    target_number: int = 86,
    bg_color: tuple = (33, 37, 41),
    accent_color: tuple = (0, 162, 237),
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Odometer Morph Reveal effect.
    Generates a 2-slide sequence that automatically morphs the numbers.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # --- 1. Helper: Generate Gradient Masks via PIL ---
    # We create cinematic fade masks instead of hard blocks
    def create_gradient_mask(filename, width_in, height_in, color, direction):
        dpi = 150
        w, h = int(width_in * dpi), int(height_in * dpi)
        img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        for y in range(h):
            if direction == 'down': # Solid at top, fades to transparent at bottom
                alpha = int(255 * (1 - (y / h)))
            else: # Solid at bottom, fades to transparent at top
                alpha = int(255 * (y / h))
            
            line_color = (color[0], color[1], color[2], alpha)
            draw.line([(0, y), (w, y)], fill=line_color)
            
        img.save(filename)
        return filename

    mask_top = create_gradient_mask("mask_top.png", 13.333, 2.5, bg_color, 'down')
    mask_bot = create_gradient_mask("mask_bot.png", 13.333, 2.5, bg_color, 'up')

    # --- 2. Calculate Number Strings & Y-Offsets ---
    target_str = f"{target_number:02d}"
    digit_1, digit_2 = int(target_str[0]), int(target_str[1])
    
    # Generate strips (e.g., 0 to 8, and a sequence ending in 6)
    strip_1 = "\n".join([str(i) for i in range(digit_1 + 1)])
    # For the second digit, make it spin more by adding a full 0-9 cycle before hitting the target
    strip_2_nums = list(range(10)) + list(range(digit_2 + 1))
    strip_2 = "\n".join([str(i) for i in strip_2_nums])

    # Constants for layout
    font_size = 200
    line_spacing_multiplier = 0.85
    # Approximate height of one line in inches based on font size and spacing
    line_height_in = (font_size * line_spacing_multiplier) / 72.0 
    
    start_y = Inches(2.2) # Base Y position for the "window"

    # --- 3. Function to Build a State Slide ---
    def build_slide(is_end_state=False):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Set Background
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(*bg_color)

        # --- A. Add Moving Number Strips ---
        # Shift Y up based on which digit we need to show
        d1_shift = digit_1 if is_end_state else 0
        d2_shift = len(strip_2_nums) - 1 if is_end_state else 0

        y_pos_1 = start_y - Inches(d1_shift * line_height_in)
        y_pos_2 = start_y - Inches(d2_shift * line_height_in)

        # Strip 1 (Tens)
        tb1 = slide.shapes.add_textbox(Inches(4.5), y_pos_1, Inches(2), Inches(10))
        tb1.text_frame.vertical_anchor = MSO_ANCHOR.TOP
        p1 = tb1.text_frame.paragraphs[0]
        p1.text = strip_1
        p1.font.size = Pt(font_size)
        p1.font.bold = True
        p1.font.color.rgb = RGBColor(*accent_color)
        p1.font.name = "Arial"
        p1.alignment = PP_ALIGN.RIGHT
        p1.line_spacing = line_spacing_multiplier # Tight spacing

        # Strip 2 (Units)
        tb2 = slide.shapes.add_textbox(Inches(6.5), y_pos_2, Inches(2), Inches(20))
        tb2.text_frame.vertical_anchor = MSO_ANCHOR.TOP
        p2 = tb2.text_frame.paragraphs[0]
        p2.text = strip_2
        p2.font.size = Pt(font_size)
        p2.font.bold = True
        p2.font.color.rgb = RGBColor(*accent_color)
        p2.font.name = "Arial"
        p2.alignment = PP_ALIGN.LEFT
        p2.line_spacing = line_spacing_multiplier

        # --- B. Add Masking Layers (PIL Gradients) ---
        slide.shapes.add_picture(mask_top, 0, 0, width=Inches(13.333), height=Inches(2.5))
        slide.shapes.add_picture(mask_bot, 0, Inches(5.0), width=Inches(13.333), height=Inches(2.5))

        # --- C. Add Static Overlays ---
        # Percentage Sign
        tb_pct = slide.shapes.add_textbox(Inches(8.5), Inches(3.2), Inches(1.5), Inches(1.5))
        p_pct = tb_pct.text_frame.paragraphs[0]
        p_pct.text = "%"
        p_pct.font.size = Pt(80)
        p_pct.font.bold = True
        p_pct.font.color.rgb = RGBColor(*accent_color)
        
        # Body Copy
        tb_body = slide.shapes.add_textbox(Inches(3), Inches(5.5), Inches(7.33), Inches(1))
        p_body = tb_body.text_frame.paragraphs[0]
        p_body.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas porttitor congue massa. Fusce posuere, magna sed pulvinar ultricies, purus lectus malesuada libero."
        p_body.font.size = Pt(16)
        p_body.font.color.rgb = RGBColor(200, 200, 200)
        p_body.alignment = PP_ALIGN.CENTER
        
        return slide

    # Build Slide 1 (00%) and Slide 2 (Target%)
    slide1 = build_slide(is_end_state=False)
    slide2 = build_slide(is_end_state=True)

    # --- 4. Inject Morph Transition via lxml ---
    try:
        # We need to add the Morph transition to Slide 2
        slide2_xml = slide2._element
        
        # Create transition element
        # <p:transition spd="slow" p14:dur="2000"> <p14:morph option="byObject"/> </p:transition>
        nsmap = {
            'p': "http://schemas.openxmlformats.org/presentationml/2006/main",
            'p14': "http://schemas.microsoft.com/office/powerpoint/2010/main"
        }
        
        transition = etree.Element(f"{{{nsmap['p']}}}transition", nsmap=nsmap)
        transition.set("spd", "slow")
        
        morph = etree.SubElement(transition, f"{{{nsmap['p14']}}}morph")
        morph.set("option", "byObject")
        
        # Insert transition into slide xml right after existing properties
        # Usually it goes before timing/color maps. Appending it generally works.
        slide2_xml.insert(0, transition)
    except Exception as e:
        print(f"Warning: Could not inject Morph transition XML. Apply Morph manually in PPT. Error: {e}")

    prs.save(output_pptx_path)
    
    # Cleanup temp images
    if os.path.exists(mask_top): os.remove(mask_top)
    if os.path.exists(mask_bot): os.remove(mask_bot)
    
    return output_pptx_path

if __name__ == "__main__":
    create_slide("odometer_reveal.pptx", target_number=56)
    print("Presentation created successfully.")
