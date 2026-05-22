import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR
from lxml import etree
from pptx.oxml.ns import qn

def add_outer_shadow(shape):
    """Adds a default outer shadow to a shape's XML element."""
    spPr = shape.element.spPr
    # Create <a:effectLst> element if it doesn't exist
    effectLst = spPr.find(qn("a:effectLst"))
    if effectLst is None:
        effectLst = etree.SubElement(spPr, qn("a:effectLst"))

    # Define the outer shadow effect
    outerShdw = etree.SubElement(effectLst, qn("a:outerShdw"))
    outerShdw.set("blurRad", "50800")  # 4pt blur
    outerShdw.set("dist", "38100")     # 3pt distance
    outerShdw.set("dir", "2700000")    # 45 degrees
    outerShdw.set("algn", "bl")
    outerShdw.set("rotWithShape", "0")

    # Set shadow color (black with 40% alpha)
    srgbClr = etree.SubElement(outerShdw, qn("a:srgbClr"))
    srgbClr.set("val", "000000")
    alpha = etree.SubElement(srgbClr, qn("a:alpha"))
    alpha.set("val", "45000") # 45% transparency

def create_morphing_tab_navigation_slides(output_pptx_path: str, **kwargs) -> str:
    """
    Creates a PPTX file with slides structured to create a Morphing Tabbed Navigation effect.

    The user must manually apply the 'Morph' transition in PowerPoint to the generated slides.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)

    # --- Data for Tabs ---
    tab_data = [
        {"title": "平台", "color": RGBColor(237, 85, 89)},
        {"title": "课程", "color": RGBColor(60, 193, 185)},
        {"title": "类别", "color": RGBColor(255, 192, 0)},
        {"title": "内容", "color": RGBColor(89, 89, 89)},
        {"title": "定位", "color": RGBColor(146, 208, 80)},
        {"title": "简介", "color": RGBColor(0, 176, 185)},
    ]

    # --- Constants for Layout ---
    slide_width = prs.slide_width
    slide_height = prs.slide_height
    tab_width = Inches(1.5)
    tab_height = Inches(1.2)
    tab_overlap = Inches(0.25)
    content_page_left = Inches(1.5)
    content_page_width = slide_width - content_page_left
    offscreen_left = slide_width

    # === Main Loop to Create a Slide for Each Active Tab ===
    for i, active_tab_info in enumerate(tab_data):
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        # Set a light gray background
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(240, 240, 240)

        # Add subtle vertical stripes
        for k in range(10):
            stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                            left=Inches(1.5 + k * 1.5), top=0,
                                            width=Inches(0.75), height=slide_height)
            stripe.rotation = 15
            fill = stripe.fill
            fill.solid()
            fill.fore_color.rgb = RGBColor(220, 220, 220)
            stripe.line.fill.background()
            
            # Make stripes semi-transparent by manipulating XML
            sp = stripe.element
            sp.get_or_add_xfrm()
            fill_properties = sp.xpath('.//a:solidFill')[0]
            alpha = etree.SubElement(fill_properties.srgbClr, qn("a:alpha"))
            alpha.set("val", "20000") # 20% opacity


        # --- Draw All Tabs in their default (inactive) state ---
        base_top = (slide_height - (len(tab_data) * (tab_height - tab_overlap) + tab_overlap)) / 2
        for j, tab_info in enumerate(tab_data):
            current_top = base_top + j * (tab_height - tab_overlap)
            
            # Create the tab shape (rotated round-same-side rectangle)
            tab = slide.shapes.add_shape(MSO_SHAPE.ROUND_SAME_SIDE_RECTANGLE,
                                         left=0, top=current_top,
                                         width=tab_width, height=tab_height)
            tab.rotation = 180
            
            # Adjust position after rotation
            tab.left, tab.top = Inches(0), current_top

            # Style tab
            fill = tab.fill
            fill.solid()
            fill.fore_color.rgb = tab_info["color"]
            tab.line.fill.background()
            add_outer_shadow(tab)

            # Add text to tab
            text_frame = tab.text_frame
            text_frame.text = tab_info["title"]
            p = text_frame.paragraphs[0]
            p.font.size = Pt(18)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)

        # --- Draw the Active Tab and its Content Page ---
        # Draw the main content page for the active tab
        active_page_top = Inches(0.5)
        active_page_height = slide_height - Inches(1.0)
        
        page_left = content_page_left if i == i else offscreen_left # Redundant, but for clarity
        content_page = slide.shapes.add_shape(MSO_SHAPE.ROUND_SAME_SIDE_RECTANGLE,
                                                page_left, active_page_top,
                                                content_page_width, active_page_height)
        
        # Style the content page
        fill = content_page.fill
        fill.gradient()
        fill.gradient_stops[0].color.rgb = RGBColor(250, 250, 250)
        fill.gradient_stops[1].color.rgb = RGBColor(235, 235, 235)
        fill.gradient_angle = 0
        content_page.line.fill.background()
        add_outer_shadow(content_page)

        # Add placeholder text to content page
        content_page.text_frame.text = f"Content for {active_tab_info['title']}"

        # --- Position all other content pages off-screen ---
        for j, other_tab_info in enumerate(tab_data):
            if i == j: continue # Skip the active one
            
            inactive_page = slide.shapes.add_shape(MSO_SHAPE.ROUND_SAME_SIDE_RECTANGLE,
                                                     offscreen_left, active_page_top,
                                                     content_page_width, active_page_height)
            fill = inactive_page.fill
            fill.solid()
            fill.fore_color.rgb = RGBColor(255, 255, 255)
            inactive_page.line.fill.background()
            
    # --- Final Step: Save ---
    prs.save(output_pptx_path)
    print(f"Presentation saved to {output_pptx_path}")
    print("IMPORTANT: Open the file in PowerPoint, select all slides, and apply the 'Morph' transition.")
    return output_pptx_path

# Example Usage:
# if __name__ == '__main__':
#     create_morphing_tab_navigation_slides("morphing_tabs_presentation.pptx")

