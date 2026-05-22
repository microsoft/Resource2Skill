import urllib.request
import io
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

def qn(tag):
    """
    Stands for 'qualified name', a utility function to turn a namespace-prefixed
    tag name into a Clark-notation qualified tag name for lxml. For example,
    ``qn('p:cSld')`` returns ``'{http://schemas.openxmlformats.org/presentationml/2006/main}cSld'``.
    """
    nsmap = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    }
    prefix, tagroot = tag.split(':')
    uri = nsmap[prefix]
    return f'{{{uri}}}{tagroot}'

def create_slide(
    output_pptx_path: str,
    title_text: list = ["HOW TO MASK TEXT IN", "POWERPOINT"],
    image_url: str = "https://images.unsplash.com/photo-1552728089-57bdde30beb3?q=80&w=2525",
    font_name: str = "Impact",
    font_size: int = 80,
    **kwargs,
) -> str:
    """
    Creates a PPTX slide reproducing the 'Image-Filled Typography' effect.

    This function generates a slide where the text is "filled" with an image,
    replicating the result of PowerPoint's 'Merge Shapes -> Intersect' feature
    by directly manipulating the slide's underlying XML.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        title_text: A list of strings, where each string is a line of text.
        image_url: URL of the image to use for the text fill.
        font_name: The name of a bold, thick font to use.
        font_size: The font size in points.

    Returns:
        The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # --- Fallback Background (if image fails) ---
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = (255, 255, 255)

    # --- Download Image ---
    try:
        with urllib.request.urlopen(image_url) as response:
            image_stream = io.BytesIO(response.read())
    except Exception as e:
        print(f"Warning: Could not download image. Using fallback. Error: {e}")
        # Create a simple placeholder image if download fails
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (200, 200), color = 'gray')
        d = ImageDraw.Draw(img)
        d.text((10,10), "Image\nFailed", fill='white')
        image_stream = io.BytesIO()
        img.save(image_stream, format='PNG')
        image_stream.seek(0)


    # --- Create Text Box ---
    textbox = slide.shapes.add_textbox(
        Inches(0.5), Inches(1.5), prs.slide_width - Inches(1), Inches(4)
    )
    text_frame = textbox.text_frame
    text_frame.word_wrap = True
    
    # Add text line by line
    for i, line in enumerate(title_text):
        if i == 0:
            p = text_frame.paragraphs[0]
            p.text = line
        else:
            p = text_frame.add_paragraph()
            p.text = line
        
        p.font.name = font_name
        p.font.size = Pt(font_size)
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER

    # --- XML Manipulation for Picture Fill ---
    # 1. Add the image to the presentation's media parts to get a relationship ID (rId)
    # We add it as a hidden picture and then remove the shape, but the media part remains.
    hidden_pic = slide.shapes.add_picture(image_stream, Inches(0), Inches(0), width=Inches(1))
    
    # 2. Get the rId of the added image
    rId = hidden_pic._pic.blip_rId

    # 3. Get the <a:rPr> (run properties) element of our text
    run = text_frame.paragraphs[0].runs[0]
    rPr = run.font._rPr

    # 4. Remove the existing solid fill from the text
    solid_fill = rPr.find(qn("a:solidFill"))
    if solid_fill is not None:
        rPr.remove(solid_fill)

    # 5. Create and insert the <a:blipFill> element
    blip_fill = etree.SubElement(rPr, qn("a:blipFill"))
    etree.SubElement(blip_fill, qn("a:blip"), {qn("r:embed"): rId})
    stretch = etree.SubElement(blip_fill, qn("a:stretch"))
    etree.SubElement(stretch, qn("a:fillRect"))

    # 6. Remove the temporary hidden picture shape from the slide's shape tree
    spTree = slide.shapes._spTree
    spTree.remove(hidden_pic.element)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
if __name__ == '__main__':
    # Using the Puffin from the tutorial as an example
    puffin_image_url = "https://images.unsplash.com/photo-1610991848574-a694b476ad26?q=80&w=2574"
    
    # Or a more abstract texture
    texture_image_url = "https://images.unsplash.com/photo-1550684376-efcbd6e3f031?q=80&w=2670"

    create_slide(
        output_pptx_path="Image_Filled_Text.pptx",
        title_text=["IMAGE-FILLED", "TYPOGRAPHY"],
        image_url=puffin_image_url,
        font_name="Impact",
        font_size=100
    )
    print("PPTX file 'Image_Filled_Text.pptx' created successfully.")
