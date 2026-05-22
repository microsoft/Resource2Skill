import os
import uuid
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Emu
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.opc.packuri import PackURI
from lxml import etree
from PIL import Image, ImageDraw, ImageFont

def qn(tag):
    """
    Stands for 'qualified name', a utility function to turn a namespace
    prefixed tag name into a Clark-notation qualified tag name for lxml.
    """
    nsmap = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'we': 'http://schemas.microsoft.com/office/webextensions/webextension/2010/11',
        'wetp': 'http://schemas.microsoft.com/office/webextensions/taskpanes/2010/11',
    }
    prefix, tagroot = tag.split(':')
    uri = nsmap[prefix]
    return f'{{{uri}}}{tagroot}'

def create_power_bi_slide(
    output_pptx_path: str,
    power_bi_report_url: str,
    title_text: str = "Live Power BI Dashboard",
) -> str:
    """
    Creates a PowerPoint presentation with an embedded, interactive Power BI report.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        power_bi_report_url: The full URL of the Power BI report to embed.
        title_text: Optional title to add to the slide.

    Returns:
        The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[5]) # Title Only layout

    # --- Set Slide Title ---
    title_shape = slide.shapes.title
    title_shape.text = title_text
    title_shape.text_frame.paragraphs[0].font.size = Pt(32)
    title_shape.top = Inches(0.2)
    
    # --- 1. Generate a placeholder snapshot image ---
    img_bytes = BytesIO()
    img = Image.new('RGB', (400, 300), color = (240, 240, 240))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
    d.text((10,10), "Loading Power BI Report...", fill=(0,0,0), font=font)
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # --- 2. Add the snapshot image to the presentation package ---
    image_part, rId_img = slide.part.get_or_add_image_part(img_bytes)

    # --- 3. Create the webextension.xml part ---
    ext_part_uri = PackURI('/ppt/webextensions/webextension1.xml')
    
    # Define XML for webextension part
    WE_NAMESPACE = 'http://schemas.microsoft.com/office/webextensions/webextension/2010/11'
    WE = '{%s}' % WE_NAMESPACE
    
    root = etree.Element(WE + 'webextension', nsmap={'we': WE_NAMESPACE, 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'})
    root.set('id', f"{{{str(uuid.uuid4())}}}")
    root.set('store', 'WA104380905') # This ID is for the official Microsoft Power BI add-in
    root.set('storeType', 'OMEX')
    root.set('version', '2.0.0.3')
    
    etree.SubElement(root, WE + 'reference', id='62662174-dd10-4813-9883-c5a5382346b5', version='1.0.0.0')
    etree.SubElement(root, WE + 'alternateReferences')
    
    properties = etree.SubElement(root, WE + 'properties')
    etree.SubElement(properties, WE + 'property', name='ReportUrl', value=power_bi_report_url)
    
    etree.SubElement(root, WE + 'bindings')
    etree.SubElement(root, WE + 'snapshot', attrib={qn('r:id'): rId_img})

    xml_str = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    
    # Add the webextension part to the package
    prs.package.get_or_add_part(ext_part_uri, 'application/vnd.ms-office.webextension+xml', xml_str)

    # --- 4. Create relationship from slide to webextension part ---
    rId_ext = slide.part.relate_to(
        prs.package.part_related_by(ext_part_uri),
        'http://schemas.microsoft.com/office/2011/relationships/webextension'
    )

    # --- 5. Create the graphicFrame XML to embed the add-in on the slide ---
    graphic_frame = etree.fromstring(f"""
        <p:graphicFrame xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
                        xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <p:nvGraphicFramePr>
            <p:cNvPr id="2" name="Power BI"/>
            <p:cNvGraphicFramePr/>
            <p:nvPr/>
          </p:nvGraphicFramePr>
          <p:xfrm>
            <a:off x="0" y="{Emu(Inches(1.0))}"/>
            <a:ext cx="{Emu(Inches(16))}" cy="{Emu(Inches(8))}"/>
          </p:xfrm>
          <a:graphic>
            <a:graphicData uri="http://schemas.microsoft.com/office/webextensions/2010/11">
              <we:webextension xmlns:we="http://schemas.microsoft.com/office/webextensions/webextension/2010/11"
                               xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:id="{rId_ext}"/>
            </a:graphicData>
          </a:graphic>
        </p:graphicFrame>
    """)
    
    slide.shapes._spTree.append(graphic_frame)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
if __name__ == '__main__':
    # NOTE: Replace with a valid Power BI report URL that you have access to.
    # The report must be shared appropriately for others to view it.
    # Example URL from the video tutorial's context.
    report_url = "https://app.powerbi.com/groups/me/reports/c4498fcf-b03d-44af-b0da-37e85cf8cdf5/ReportSection?bookmarkGuid=5df257d9-0c8d-4487-bec6-e7c54598a103&bookmarkUsage=1&ctid=54e697da-d06f-4376-bea3-f1a7e550c8a6"
    
    # A dummy URL if you don't have a real one, to test the file generation.
    # report_url_dummy = "https://app.powerbi.com/view?r=eyJrIjoiEXAMPLE"

    output_file = "PowerBI_Interactive_Slide.pptx"
    create_power_bi_slide(output_file, report_url)
    
    print(f"Presentation with embedded Power BI report saved to: {output_file}")
    # On Windows, you can uncomment the next line to open the file automatically
    # os.startfile(output_file)

