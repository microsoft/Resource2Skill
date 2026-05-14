import io
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE

def create_network_topology_diagram(
    output_pptx_path: str,
    company_name: str = "XYZ LLC",
) -> str:
    """
    Creates a PowerPoint slide with an IT network topology diagram.

    This function reproduces a standard hub-and-spoke network architecture diagram
    using open-source icons, similar to the one built in the tutorial.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        company_name: The name of the company for the slide title.

    Returns:
        The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide layout

    # Helper function to download and add images
    def add_icon(url, left, top, width):
        try:
            with urllib.request.urlopen(url) as response:
                image_stream = io.BytesIO(response.read())
                return slide.shapes.add_picture(image_stream, Inches(left), Inches(top), Inches(width))
        except Exception as e:
            print(f"Warning: Could not download icon from {url}. Error: {e}")
            # Add a placeholder rectangle if download fails
            return slide.shapes.add_shape(1, Inches(left), Inches(top), Inches(width), Inches(width))

    # Icon URLs from a reliable source (Wikimedia Commons)
    ICONS = {
        "router": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Router_Icon.svg/240px-Router_Icon.svg.png",
        "switch": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Icon_Network_Switch.svg/240px-Icon_Network_Switch.svg.png",
        "server_rack": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Gartoon-network-server-icon.svg/240px-Gartoon-network-server-icon.svg.png",
        "building": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Vector_Building_icon.svg/240px-Vector_Building_icon.svg.png",
        "internet": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Internet-cloud-big.svg/240px-Internet-cloud-big.svg.png",
        "users": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Icons8_flat_manager.svg/240px-Icons8_flat_manager.svg.png"
    }

    # === Title ===
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12.33), Inches(0.5))
    title_shape.text_frame.text = f"IT Infrastructure Diagram for {company_name}"
    title_shape.text_frame.paragraphs[0].font.size = Pt(28)
    title_shape.text_frame.paragraphs[0].font.bold = True

    # === Define Locations & Add Icons ===
    # Central Office
    co_building = add_icon(ICONS["building"], 6.16, 0.8, 1.0)
    co_router = add_icon(ICONS["router"], 6.28, 1.8, 0.75)
    co_switch = add_icon(ICONS["switch"], 6.28, 2.8, 0.75)
    co_servers = add_icon(ICONS["server_rack"], 7.5, 1.8, 1.0)
    co_users = add_icon(ICONS["users"], 9.0, 2.5, 0.75)

    # Branch Office 1
    bo1_building = add_icon(ICONS["building"], 2.16, 5.5, 1.0)
    bo1_router = add_icon(ICONS["router"], 2.28, 4.5, 0.75)
    bo1_switch = add_icon(ICONS["switch"], 2.28, 3.5, 0.75)
    bo1_users = add_icon(ICONS["users"], 0.75, 4.0, 0.75)

    # Branch Office 2
    bo2_building = add_icon(ICONS["building"], 10.16, 5.5, 1.0)
    bo2_router = add_icon(ICONS["router"], 10.28, 4.5, 0.75)
    bo2_switch = add_icon(ICONS["switch"], 10.28, 3.5, 0.75)
    bo2_users = add_icon(ICONS["users"], 12.0, 4.0, 0.75)

    # Internet
    internet_cloud = add_icon(ICONS["internet"], 1.0, 1.5, 1.5)

    # === Add Text Labels ===
    def add_label(text, shape):
        label = slide.shapes.add_textbox(
            shape.left + (shape.width / 2) - Inches(1.0),
            shape.top + shape.height - Inches(0.1),
            Inches(2.0), Inches(0.4)
        )
        p = label.text_frame.paragraphs[0]
        p.text = text
        p.font.size = Pt(14)
        p.alignment = 1 # Center

    add_label("Central Office", co_building)
    add_label("Branch Office 1", bo1_building)
    add_label("Branch Office 2", bo2_building)
    add_label("Internet", internet_cloud)


    # === Add Connectors ===
    def connect_shapes(shape1, shape2, dashed=False):
        connector = slide.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT,
            shape1.left + shape1.width / 2,
            shape1.top + shape1.height / 2,
            shape2.left + shape2.width / 2,
            shape2.top + shape2.height / 2,
        )
        line = connector.line
        line.color.rgb = RGBColor(0, 0, 0)
        line.width = Pt(1.5)
        if dashed:
            line.dash_style = MSO_LINE.DASH
        return connector

    # WAN Connections (Leased Lines - Dashed)
    connect_shapes(co_router, bo1_router, dashed=True)
    connect_shapes(co_router, bo2_router, dashed=True)
    connect_shapes(bo1_router, bo2_router, dashed=True) # Branch to Branch link

    # LAN Connections (Solid)
    connect_shapes(co_router, co_switch)
    connect_shapes(co_switch, co_servers)
    connect_shapes(co_switch, co_users)
    
    connect_shapes(bo1_router, bo1_switch)
    connect_shapes(bo1_switch, bo1_users)
    
    connect_shapes(bo2_router, bo2_switch)
    connect_shapes(bo2_switch, bo2_users)

    # Internet Connection
    connect_shapes(internet_cloud, co_router)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# if __name__ == '__main__':
#     create_network_topology_diagram("network_diagram.pptx", company_name="Global Tech Inc.")
