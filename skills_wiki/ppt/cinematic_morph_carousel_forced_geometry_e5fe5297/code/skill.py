import os
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from lxml import etree
from PIL import Image, ImageDraw

def _create_fallback_image(filename: str, color: tuple, size: tuple = (800, 600)):
    """Creates a simple PIL image to use if web downloads fail."""
    img = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(img)
    draw.rectangle([50, 50, size[0]-50, size[1]-50], outline="white", width=10)
    img.save(filename)
    return filename

def apply_morph_transition(slide):
    """
    Injects the Morph transition XML into a python-pptx slide object.
    """
    p_ns = "http://schemas.openxmlformats.org/presentationml/2006/main"
    transition = etree.Element(f"{{{p_ns}}}transition")
    # By default, adding <p:morph/> enables the smooth transition
    morph = etree.SubElement(transition, f"{{{p_ns}}}morph")
    
    # Append the transition element to the slide's root XML element
    slide.element.append(transition)

def create_slide(
    output_pptx_path: str = "Cinematic_Morph_Effect.pptx",
    title_text: str = "TAJ MAHAL",
    body_text: str = "The Morph transition creates seamless animations. Notice how the image scales and moves, and how the circle magically turns into a triangle.",
    bg_color: tuple = (250, 215, 161), # Warm yellow/sand
    **kwargs,
) -> str:
    """
    Creates a PPTX demonstrating spatial image morphing and forced geometry (!!) morphing.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # 1. Prepare an image asset
    img_path = "temp_hero.jpg"
    try:
        req = urllib.request.Request(
            'https://images.unsplash.com/photo-1564507592208-027041530e32?q=80&w=800', 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            with open(img_path, 'wb') as out_file:
                out_file.write(response.read())
    except Exception:
        print("Image download failed. Using PIL fallback.")
        _create_fallback_image(img_path, (100, 150, 200))

    # ==========================================
    # SLIDE 1: The Setup (Centered, Large)
    # ==========================================
    blank_layout = prs.slide_layouts[6]
    slide1 = prs.slides.add_slide(blank_layout)
    slide1.background.fill.solid()
    slide1.background.fill.fore_color.rgb = RGBColor(*bg_color)
    
    # Add Title (Center)
    txbox1 = slide1.shapes.add_textbox(Inches(0), Inches(0.5), Inches(13.333), Inches(2))
    tf1 = txbox1.text_frame
    tf1.text = title_text
    tf1.paragraphs[0].alignment = 2 # Center
    tf1.paragraphs[0].font.size = Pt(80)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    # Give it a specific name for standard morphing
    txbox1.name = "MainTitle"

    # Add Image (Center, Large)
    pic1 = slide1.shapes.add_picture(img_path, Inches(3.66), Inches(2.5), width=Inches(6))
    pic1.name = "HeroImage"


    # ==========================================
    # SLIDE 2: Spatial Morph & Introduce "!!Shape"
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    slide2.background.fill.solid()
    slide2.background.fill.fore_color.rgb = RGBColor(*bg_color)
    
    # Apply Morph transition via lxml
    apply_morph_transition(slide2)

    # Title moves to top-left and gets smaller
    txbox2 = slide2.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(6), Inches(1))
    tf2 = txbox2.text_frame
    tf2.text = title_text
    tf2.paragraphs[0].font.size = Pt(50)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    txbox2.name = "MainTitle" # SAME NAME = Morph Match

    # Image scales down and moves left
    pic2 = slide2.shapes.add_picture(img_path, Inches(0.5), Inches(2), width=Inches(4.5))
    pic2.name = "HeroImage" # SAME NAME = Morph Match

    # Add new body text that fades in
    bodybox = slide2.shapes.add_textbox(Inches(5.5), Inches(2), Inches(7), Inches(3))
    bodybox.text_frame.text = body_text
    bodybox.text_frame.paragraphs[0].font.size = Pt(24)

    # Introduce a CIRCLE with the "!!" naming convention
    # This tells PPT to force a morph regardless of shape geometry
    circle = slide2.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(8), Inches(4.5), Inches(2.5), Inches(2.5)
    )
    circle.fill.solid()
    circle.fill.fore_color.rgb = RGBColor(0, 191, 255) # Cyan
    circle.line.fill.background()
    circle.name = "!!MagicMorphShape" # THE SECRET SAUCE


    # ==========================================
    # SLIDE 3: Forced Geometry Morph
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    slide3.background.fill.solid()
    slide3.background.fill.fore_color.rgb = RGBColor(*bg_color)
    
    # Apply Morph transition via lxml
    apply_morph_transition(slide3)

    # Keep text and image steady
    txbox3 = slide3.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(6), Inches(1))
    txbox3.text_frame.text = title_text
    txbox3.text_frame.paragraphs[0].font.size = Pt(50)
    txbox3.text_frame.paragraphs[0].font.bold = True
    txbox3.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    txbox3.name = "MainTitle" 

    pic3 = slide3.shapes.add_picture(img_path, Inches(0.5), Inches(2), width=Inches(4.5))
    pic3.name = "HeroImage"

    # Morph the Circle into a TRIANGLE on the right side
    triangle = slide3.shapes.add_shape(
        MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(5), Inches(2), Inches(7), Inches(5)
    )
    triangle.fill.solid()
    triangle.fill.fore_color.rgb = RGBColor(255, 99, 71) # Tomato red
    triangle.line.fill.background()
    
    # Applying the exact same !! name triggers the geometry metamorphosis
    triangle.name = "!!MagicMorphShape" 

    # Save and clean up
    prs.save(output_pptx_path)
    if os.path.exists(img_path):
        os.remove(img_path)
        
    return output_pptx_path

if __name__ == "__main__":
    out_path = create_slide()
    print(f"Presentation saved to {out_path}. Open in PowerPoint and enter Presentation Mode to see the Morph in action.")
