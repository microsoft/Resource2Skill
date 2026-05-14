import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.oxml.ns import qn
from lxml import etree

def create_presentation_with_custom_theme(
    output_pptx_path: str,
    palette_name: str = "Coolors Custom Palette",
    accent_colors_rgb: list = None,
    **kwargs,
) -> str:
    """
    Creates a new PowerPoint presentation and embeds a custom color theme.

    This function directly manipulates the theme's XML to set the Accent 1-6 colors,
    which then become the default colors for shapes and charts.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        palette_name: The name for the custom color palette as it will appear in PowerPoint.
        accent_colors_rgb: A list of up to 6 RGB tuples, e.g., [(190, 202, 230), ...].

    Returns:
        The path to the saved .pptx file.
    """

    def rgb_to_hex(rgb):
        """Converts an RGB tuple to a HEX string."""
        return '%02x%02x%02x' % rgb

    # Use the default palette from the tutorial if none is provided
    if accent_colors_rgb is None:
        accent_colors_rgb = [
            (190, 202, 230),  # Accent 1: Light Blue
            (33, 158, 188),   # Accent 2: Teal
            (2, 48, 71),      # Accent 3: Dark Navy
            (255, 183, 3),    # Accent 4: Yellow
            (251, 133, 0),    # Accent 5: Orange
            (76, 175, 80),    # Accent 6: Green (complement)
        ]

    # --- Step 1: Create a base presentation ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # --- Step 2: Access and Parse the Theme XML ---
    # The theme is a part of the presentation's slide master
    theme_part = prs.slide_master.part.theme_part
    
    # Use lxml to parse the XML content of the theme
    theme_xml_tree = etree.fromstring(theme_part.blob)
    
    # --- Step 3: Find and Modify the Color Scheme ---
    # The color scheme is defined in the <a:clrScheme> element.
    # We use XPath to find it. The `qn` function resolves the namespace prefix (e.g., 'a:').
    clr_scheme_element = theme_xml_tree.find(qn('a:themeElements/a:clrScheme'))
    
    # Set the name of our new color palette
    clr_scheme_element.set('name', palette_name)
    
    # --- Step 4: Remove Existing Accent Colors ---
    # We need to remove the old accent color definitions before adding our own.
    accent_elements_to_remove = clr_scheme_element.xpath('a:accent[1-6]')
    for accent_element in accent_elements_to_remove:
        accent_element.getparent().remove(accent_element)

    # --- Step 5: Inject New Custom Accent Colors ---
    # Loop through our list of RGB colors and create the necessary XML elements.
    for i, rgb_color in enumerate(accent_colors_rgb[:6], 1):
        hex_color_val = rgb_to_hex(rgb_color).upper()
        
        # Create <a:accentX> element
        new_accent = etree.SubElement(clr_scheme_element, qn(f'a:accent{i}'))
        
        # Create <a:srgbClr> child with a 'val' attribute for the HEX code
        srgb_clr = etree.SubElement(new_accent, qn('a:srgbClr'))
        srgb_clr.set('val', hex_color_val)
        
    # --- Step 6: Update the Theme Part with Modified XML ---
    # Overwrite the original theme data with our modified XML string.
    theme_part._blob = etree.tostring(theme_xml_tree)

    # --- Step 7: Add Demonstration Slides to Prove it Worked ---
    # Add a title slide to show shapes using the new theme colors
    slide1 = prs.slides.add_slide(prs.slide_layouts[5])
    title = slide1.shapes.title
    title.text = "Custom Color Theme Applied"
    title.text_frame.paragraphs[0].font.size = Pt(44)
    title.left = Inches(1)
    title.top = Inches(0.5)
    title.width = prs.slide_width - Inches(2)
    
    # Add shapes that will automatically pick up the new accent colors
    for i in range(6):
        left = Inches(1 + i * 2)
        top = Inches(2)
        width = Inches(1.5)
        height = Inches(1.5)
        shape = slide1.shapes.add_shape(1, left, top, width, height) # 1 = Rectangle
        # By default, shape fills cycle through Accent 1, 2, 3, etc.
    
    # Add a chart slide
    slide2 = prs.slides.add_slide(prs.slide_layouts[5])
    chart_data = CategoryChartData()
    chart_data.categories = ['Category 1', 'Category 2', 'Category 3', 'Category 4']
    chart_data.add_series('Series 1', (4.3, 2.5, 3.5, 4.5))
    chart_data.add_series('Series 2', (2.4, 4.4, 1.8, 2.8))
    chart_data.add_series('Series 3', (2.0, 2.0, 3.0, 5.0))
    
    x, y, cx, cy = Inches(2), Inches(2), Inches(10), Inches(5)
    graphic_frame = slide2.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
    )
    chart = graphic_frame.chart
    chart.chart_title.text_frame.text = 'Chart Colors from New Theme'
    
    # --- Step 8: Save the Final Presentation ---
    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
if __name__ == '__main__':
    file_path = "presentation_with_custom_theme.pptx"
    create_presentation_with_custom_theme(file_path)
    print(f"Presentation saved to: {os.path.abspath(file_path)}")

