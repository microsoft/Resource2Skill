import os
import io
import urllib.request
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image, ImageOps

# Helper function to handle XML namespaces
def qn(tag):
    """
    Stands for 'qualified name', a utility function to turn a namespace prefixed
    tag name into a Clark-notation qualified tag name for lxml. For example,
    qn('p:cSld') returns '{http://schemas.openxmlformats.org/presentationml/2006/main}cSld'.
    """
    nsmap = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main',
        'p16': 'http://schemas.microsoft.com/office/powerpoint/2016/10/main'
    }
    prefix, local = tag.split(':')
    return f'{{{nsmap[prefix]}}}{local}'

def create_slide(
    output_pptx_path: str = "interactive_zoom_dashboard.pptx",
    image_urls: list = None,
    **kwargs,
) -> str:
    """
    Creates a PowerPoint presentation with an interactive zoom dashboard,
    reproducing the "Summary Zoom" effect shown in the tutorial.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        image_urls: A list of up to 6 image URLs to use for the gallery.

    Returns:
        Path to the saved PPTX file.
    """
    if image_urls is None:
        image_urls = [
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
            "https://images.unsplash.com/photo-1519681391924-4a993425234b",
            "https://images.unsplash.com/photo-1485160497022-3e09382fb310",
            "https://images.unsplash.com/photo-1472214103451-9374bd1c798e",
            "https://images.unsplash.com/photo-1508921912186-1d1a45ebb3c1",
            "https://images.unsplash.com/photo-1470770841072-f978cf4d019e"
        ]

    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)

    # === Create Detail Slides ===
    detail_slides = []
    for url in image_urls[:6]:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        try:
            with urllib.request.urlopen(url) as response:
                image_data = io.BytesIO(response.read())
                slide.shapes.add_picture(image_data, 0, 0, width=prs.slide_width, height=prs.slide_height)
            detail_slides.append(slide)
        except Exception:
            # Fallback: add a gray background if image fails
            fill = slide.background.fill
            fill.solid()
            fill.fore_color.rgb = (200, 200, 200)

    # === Create Hub Slide ===
    hub_slide = prs.slides.add_slide(prs.slide_layouts[6])
    # Set a dark background for the hub slide
    fill = hub_slide.background.fill
    fill.solid()
    fill.fore_color.rgb = (10, 10, 10)

    # === Add Zoom Objects to Hub Slide via XML Injection ===
    spTree = hub_slide.shapes._spTree
    
    # Grid layout parameters
    cols = 3
    rows = 2
    thumb_width = Inches(4.5)
    thumb_height = Inches(2.53)
    x_margin = (prs.slide_width - cols * thumb_width) / (cols + 1)
    y_margin = (prs.slide_height - rows * thumb_height) / (rows + 1)

    for i, slide in enumerate(detail_slides):
        # Calculate position for grid
        row = i // cols
        col = i % cols
        left = x_margin * (col + 1) + thumb_width * col
        top = y_margin * (row + 1) + thumb_height * row

        # 1. Create the relationship to the target slide for the zoom effect
        zoom_rel = hub_slide.part.relate_to(
            slide.part,
            "http://schemas.microsoft.com/office/2016/10/relationships/slideZoom"
        )
        
        # 2. Generate and embed a thumbnail image
        first_shape = slide.shapes[0] if slide.shapes else None
        thumb_img_rel = None
        if first_shape and hasattr(first_shape, 'image'):
            img_stream = io.BytesIO(first_shape.image.blob)
            with Image.open(img_stream) as img:
                thumb = ImageOps.fit(img, (int(thumb_width.emu / 9525), int(thumb_height.emu / 9525)), Image.LANCZOS)
                thumb_bytes = io.BytesIO()
                thumb.save(thumb_bytes, format='PNG')
                thumb_bytes.seek(0)
                thumb_img_rel = hub_slide.part.relate_to(
                    hub_slide.part.package.image_parts.add_image(thumb_bytes),
                    "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
                )

        # 3. Build the XML for the <p:graphicFrame> containing the zoom object
        graphicFrame = etree.Element(qn('p:graphicFrame'))
        
        # Non-visual properties
        nv_props = etree.SubElement(graphicFrame, qn('p:nvGraphicFramePr'))
        etree.SubElement(nv_props, qn('p:cNvPr'), id=str(10 + i), name=f"Zoom {i}")
        etree.SubElement(nv_props, qn('p:cNvGraphicFramePr'))
        etree.SubElement(nv_props, qn('p:nvPr'))

        # Transform (position and size)
        xfrm = etree.SubElement(graphicFrame, qn('p:xfrm'))
        etree.SubElement(xfrm, qn('a:off'), x=str(int(left)), y=str(int(top)))
        etree.SubElement(xfrm, qn('a:ext'), cx=str(int(thumb_width)), cy=str(int(thumb_height)))

        # Graphic data (the zoom element itself)
        graphic = etree.SubElement(graphicFrame, qn('a:graphic'))
        graphicData = etree.SubElement(graphic, qn('a:graphicData'), uri="http://schemas.microsoft.com/office/powerpoint/2015/10/main")
        
        # Create the zoom element with relationship ID
        zoom_el = etree.Element(qn('p16:zoom'), {qn('r:id'): zoom_rel.rId, 'transitionDur': '500'})
        zoom_el.append(etree.Element(qn('p16:bmk'), {'name': f"Slide {slide.slide_id}"}))
        if thumb_img_rel:
            img_el = etree.Element(qn('p16:img'), {qn('r:embed'): thumb_img_rel.rId})
            zoom_el.append(img_el)

        graphicData.append(zoom_el)
        
        spTree.append(graphicFrame)
        
    prs.save(output_pptx_path)
    return output_pptx_path

# Example of how to run it
if __name__ == '__main__':
    file_path = "interactive_zoom_dashboard_output.pptx"
    create_slide(file_path)
    print(f"Presentation saved to: {file_path}")
    # On Windows, you can uncomment the line below to open the file automatically
    # os.startfile(file_path)

