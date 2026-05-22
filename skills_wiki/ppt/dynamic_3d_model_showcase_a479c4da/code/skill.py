import os
import urllib.request
import uuid
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Emu
from pptx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT

# Helper function to get the correct XML namespace prefixes
def qn(tag):
    """
    Stands for 'qualified name', a utility function to turn a namespace
    prefixed tag name into a Clark-notation qualified tag name for lxml.
    """
    nsmap = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
        'am3d': 'http://schemas.microsoft.com/office/2017/06/3d/model',
        'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main',
    }
    prefix, local_name = tag.split(':')
    return f'{{{nsmap[prefix]}}}{local_name}'

def create_slide(
    output_pptx_path: str,
    model_path: str = None,
    animation_duration_ms: int = 10000,
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with an animated, rotating 3D model.

    This function reproduces the effect of inserting a 3D model and applying
    the 'Turntable' animation.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        model_path: Path to a pre-existing .glb 3D model file. If None, a
                    sample model will be downloaded. The model should already
                    have any custom branding/textures applied.
        animation_duration_ms: The duration for one full 360-degree rotation,
                               in milliseconds.

    Returns:
        Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide layout

    # --- 1. Prepare the 3D Model File ---
    local_model_path = model_path
    if not local_model_path or not os.path.exists(local_model_path):
        print("Model not provided or not found, downloading a sample.")
        sample_model_url = "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/DamagedHelmet/glTF-Binary/DamagedHelmet.glb"
        local_model_path = "sample_model.glb"
        try:
            urllib.request.urlretrieve(sample_model_url, local_model_path)
            print(f"Sample model downloaded to {local_model_path}")
        except Exception as e:
            print(f"Error downloading sample model: {e}")
            # Fallback: cannot proceed without a model
            prs.save(output_pptx_path)
            return output_pptx_path

    # --- 2. Add 3D Model to Presentation Package (python-pptx OPC layer) ---
    slide_part = slide.part
    # Define content type for the 3D model
    model_ct = "model/gltf-binary"
    # Read model data
    with open(local_model_path, 'rb') as f:
        model_blob = f.read()

    # Add the model as a new part in the package
    # Use a unique name for the media part
    image_part, rId = slide_part.add_image_part(model_blob, content_type=model_ct)
    
    # We added it as an image to get it into the package, but the relationship type is wrong.
    # We must now correct the relationship type to be for a 3D model.
    slide_part.drop_rel(rId)
    rel = slide_part.relate_to(image_part, RT.MODEL_3D)
    model_rid = rel.rId

    # --- 3. Create the 3D Model Shape XML (lxml) ---
    # This structure is required for PowerPoint to recognize the shape as a 3D model container.
    spid = "2" # A unique shape ID on the slide
    cx = Emu(Inches(6))
    cy = Emu(Inches(6))
    off_x = Emu((prs.slide_width - cx) / 2)
    off_y = Emu((prs.slide_height - cy) / 2)

    graphic_frame_xml = f"""
    <p:graphicFrame xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
                    xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                    xmlns:am3d="http://schemas.microsoft.com/office/2017/06/3d/model">
        <p:nvGraphicFramePr>
            <p:cNvPr id="{spid}" name="3D Model {spid}"/>
            <p:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></p:cNvGraphicFramePr>
            <p:nvPr/>
        </p:nvGraphicFramePr>
        <p:xfrm>
            <a:off x="{off_x}" y="{off_y}"/>
            <a:ext cx="{cx}" cy="{cy}"/>
        </p:xfrm>
        <a:graphic>
            <a:graphicData uri="http://schemas.microsoft.com/office/2017/06/3d/model">
                <am3d:model>
                    <am3d:res r:embed="{model_rid}"/>
                </am3d:model>
            </a:graphicData>
        </a:graphic>
    </p:graphicFrame>
    """
    
    # --- 4. Create the Turntable Animation XML (lxml) ---
    # This complex XML defines the "Turntable" animation targeting the 3D model.
    animation_xml = f"""
    <p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
        <p:tnLst>
            <p:par>
                <p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
                    <p:childTnLst>
                        <p:seq concurrent="1" nextAc="seek">
                            <p:cTn id="2" dur="{animation_duration_ms}" fill="hold">
                                <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                            </p:cTn>
                            <p:childTnLst>
                                <p:par>
                                    <p:cTn id="3" fill="hold">
                                        <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                                        <p:childTnLst>
                                            <p:par>
                                                <p:cTn id="4" fill="hold">
                                                    <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                                                    <p:childTnLst>
                                                        <p:anim calcmode="lin" valueType="num" repeatCount="indefinite">
                                                            <p:cBhvr>
                                                                <p:cTn id="5" dur="{animation_duration_ms}" fill="hold"/>
                                                                <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>
                                                                <p:attrNameLst><p:attrName>model.turntable.y</p:attrName></p:attrNameLst>
                                                            </p:cBhvr>
                                                            <p:tavLst>
                                                                <p:tav tm="0"><p:val><p:strVal val="0"/></p:val></p:tav>
                                                                <p:tav tm="100000"><p:val><p:strVal val="360"/></p:val></p:tav>
                                                            </p:tavLst>
                                                        </p:anim>
                                                    </p:childTnLst>
                                                </p:cTn>
                                            </p:par>
                                        </p:childTnLst>
                                    </p:cTn>
                                </p:par>
                            </p:childTnLst>
                        </p:seq>
                    </p:childTnLst>
                </p:cTn>
            </p:par>
        </p:tnLst>
    </p:timing>
    """

    # --- 5. Inject XML into the Slide ---
    slide_element = slide.element
    spTree = slide_element.get_or_add_spTree()
    
    # Add the graphic frame for the 3D model
    graphic_frame_tree = etree.fromstring(graphic_frame_xml)
    spTree.append(graphic_frame_tree)

    # Add the animation timing information
    timing_tree = etree.fromstring(animation_xml)
    slide_element.insert(slide_element.index(spTree), timing_tree)
    
    prs.save(output_pptx_path)
    print(f"Presentation with animated 3D model saved to {output_pptx_path}")
    return output_pptx_path

# Example usage:
# create_slide("animated_3d_model.pptx") # This will download a sample helmet model
# To use your own model:
# create_slide("my_branded_product.pptx", model_path="path/to/my/model.glb")

