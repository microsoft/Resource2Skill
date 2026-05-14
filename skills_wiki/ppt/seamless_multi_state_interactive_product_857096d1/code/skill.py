import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls, qn
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str = "Interactive_Product_Showcase.pptx",
    title_text: str = "EarPods",
    subtitle_text: str = "Immersive sound with different colours",
    body_text: str = "Experience our immersive sound with same comfort but now with the choice of colours. With our new addition of Dolby Atmos enjoy the surrounding music and forget about everything around you.",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Seamless Multi-State Interactive Product Showcase.
    Generates placeholder product assets, lays out interactive slides, and links them.
    """
    
    # 1. Setup Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Define our color palette
    product_variants = [
        {"name": "Heaven white", "color": (240, 240, 240)},
        {"name": "Hell black", "color": (30, 30, 30)},
        {"name": "Mint green", "color": (60, 179, 113)},
        {"name": "Rosy red", "color": (220, 20, 60)}
    ]
    
    # 2. Asset Generation (PIL)
    # Generate placeholder product images (stylized earbuds) so the script runs standalone
    asset_paths = []
    for variant in product_variants:
        img_w, img_h = 400, 500
        img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        main_color = variant["color"]
        # Add a subtle shading to the color
        shade_color = tuple(max(0, int(c * 0.8)) for c in main_color)
        
        # Draw a stylized floating earbud
        # Stem
        draw.rounded_rectangle([180, 200, 230, 450], radius=25, fill=main_color)
        draw.rounded_rectangle([210, 200, 230, 450], radius=10, fill=shade_color) # Fake 3D
        # Earpiece
        draw.ellipse([140, 100, 260, 240], fill=main_color)
        draw.ellipse([210, 120, 250, 220], fill=shade_color) # Shadow/Depth
        # Speaker grill
        draw.ellipse([150, 140, 170, 200], fill=(50, 50, 50))
        
        img_path = f"temp_earpod_{variant['name'].replace(' ', '_')}.png"
        img.save(img_path)
        asset_paths.append(img_path)

    # 3. Create all slides first (so we can link between them)
    slides = [prs.slides.add_slide(prs.slide_layouts[6]) for _ in range(len(product_variants))]
    
    # OpenXML helper function for Outer Shadow
    def add_outer_shadow(shape):
        spPr = shape.element.spPr
        effectLst = parse_xml(
            f'<a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            f'  <a:outerShdw blurRad="100000" dist="30000" dir="5400000" algn="ctr" rotWithShape="0">'
            f'    <a:srgbClr val="000000">'
            f'      <a:alpha val="30000"/>'
            f'    </a:srgbClr>'
            f'  </a:outerShdw>'
            f'</a:effectLst>'
        )
        spPr.append(effectLst)
        
    # OpenXML helper function for Slide Transition (Fade)
    def add_fade_transition(slide):
        transition_xml = parse_xml(
            f'<p:transition {nsdecls("p")} spd="med">'
            f'  <p:fade/>'
            f'</p:transition>'
        )
        slide.element.insert(1, transition_xml) # Insert right after timing/color maps

    # 4. Populate each slide
    for idx, slide in enumerate(slides):
        add_fade_transition(slide)
        
        # --- Background ---
        # Very light off-white background
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(245, 245, 245)
        
        # --- Typography ---
        # Main Title
        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.8), Inches(6), Inches(1))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(44)
        p.font.bold = True
        p.font.name = "Arial"
        p.font.color.rgb = RGBColor(20, 20, 20)
        
        # Subtitle
        sub_box = slide.shapes.add_textbox(Inches(1), Inches(2.2), Inches(6), Inches(0.5))
        tf_sub = sub_box.text_frame
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle_text
        p_sub.font.size = Pt(22)
        p_sub.font.bold = True
        p_sub.font.name = "Arial"
        p_sub.font.color.rgb = RGBColor(40, 40, 40)
        
        # Body text
        body_box = slide.shapes.add_textbox(Inches(1), Inches(2.8), Inches(5.5), Inches(2))
        tf_body = body_box.text_frame
        tf_body.word_wrap = True
        p_body = tf_body.paragraphs[0]
        p_body.text = body_text
        p_body.font.size = Pt(14)
        p_body.font.name = "Arial"
        p_body.font.color.rgb = RGBColor(80, 80, 80)
        
        # Variant Label
        lbl_box = slide.shapes.add_textbox(Inches(1), Inches(5.5), Inches(4), Inches(0.5))
        tf_lbl = lbl_box.text_frame
        p_lbl = tf_lbl.paragraphs[0]
        p_lbl.text = product_variants[idx]["name"]
        p_lbl.font.size = Pt(18)
        p_lbl.font.name = "Arial"
        p_lbl.font.color.rgb = RGBColor(100, 100, 100)
        
        # --- Product Image ---
        # Place the generated product image for this slide's state
        slide.shapes.add_picture(asset_paths[idx], Inches(7.5), Inches(1.5), height=Inches(5))
        
        # Fake base shadow for the product image
        base_shadow = slide.shapes.add_shape(9, Inches(8), Inches(6.2), Inches(3), Inches(0.5)) # shape 9 is ellipse
        base_shadow.fill.solid()
        base_shadow.fill.fore_color.rgb = RGBColor(150, 150, 150)
        base_shadow.line.fill.background()
        add_outer_shadow(base_shadow)
        
        # --- UI Buttons (Color Swatches) ---
        start_x = Inches(1)
        start_y = Inches(4.5)
        gap = Inches(0.6)
        
        for j, variant in enumerate(product_variants):
            # If active, shift slightly up
            y_offset = start_y - Inches(0.05) if idx == j else start_y
            
            circle = slide.shapes.add_shape(
                9, # MSO_SHAPE.OVAL
                start_x + (j * gap), 
                y_offset, 
                Inches(0.4), 
                Inches(0.4)
            )
            
            # Formatting
            circle.fill.solid()
            circle.fill.fore_color.rgb = RGBColor(*variant["color"])
            circle.line.color.rgb = RGBColor(200, 200, 200)
            circle.line.width = Pt(1)
            
            if idx == j:
                # Active button: Add shadow
                add_outer_shadow(circle)
            else:
                # Inactive button: Add Hyperlink to its respective slide
                circle.click_action.target_slide = slides[j]

    # Cleanup temporary images
    for p in asset_paths:
        if os.path.exists(p):
            os.remove(p)

    prs.save(output_pptx_path)
    return output_pptx_path

if __name__ == "__main__":
    create_slide()
