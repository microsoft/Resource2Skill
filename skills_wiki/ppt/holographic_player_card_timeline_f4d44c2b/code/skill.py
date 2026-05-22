import os
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_FILL
from lxml import etree

# Helper for lxml namespace mapping
def qn(tag):
    """
    Stands for 'qualified name', a utility function to turn a namespace-prefixed
    XML tag name into a Clark-notation-style name for use with lxml.
    """
    nsmap = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
    }
    prefix, tagroot = tag.split(':')
    return f'{{{nsmap[prefix]}}}{tagroot}'

def create_player_card_slide(
    output_pptx_path: str,
    player_name: str = "TOM BRADY",
    player_image_url: str = "https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/2577.png&w=350&h=254",
    team_logo_url: str = "https://a.espncdn.com/i/teamlogos/nfl/500/tb.png",
    card_bg_color: tuple = (211, 24, 24),
    holographic_texture_url: str = "https://images.unsplash.com/photo-1572204523136-735438889972?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800",
    gold_texture_url: str = "https://images.unsplash.com/photo-1620371350502-999e9a7d80a4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800",
    grass_texture_url: str = "https://www.textures.com/system/gallery/photos/Nature/Grass/30678/Grass0137_1_S.jpg",
    yard_line_number: str = "50"
) -> str:
    """
    Creates a PPTX slide with a 'Holographic Player Card' design.

    Returns: The path to the saved PPTX file.
    """
    
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Asset Downloading ---
    image_paths = {}
    urls = {
        "player": player_image_url, "logo": team_logo_url,
        "holographic": holographic_texture_url, "gold": gold_texture_url,
        "grass": grass_texture_url
    }
    
    os.makedirs("temp_assets", exist_ok=True)
    for name, url in urls.items():
        try:
            path = f"temp_assets/{name}.png"
            urllib.request.urlretrieve(url, path)
            image_paths[name] = path
        except Exception as e:
            print(f"Could not download {name} image: {e}")
            image_paths[name] = None

    # === Layer 1: Background ===
    if image_paths.get("grass"):
        fill = slide.background.fill
        fill.solid() # Must be solid before picture
        fill.picture(image_paths["grass"])
        
        # Enable tiling
        pic = slide.background._blip.p_blip
        tile = etree.SubElement(pic, qn('a:tile'))
        tile.set('tx', '0')
        tile.set('ty', '0')
        tile.set('sx', '50000') # 50% scale
        tile.set('sy', '50000')

    # Yard Line
    line = slide.shapes.add_shape(1, Inches(12), 0, Inches(0.1), Inches(9))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(255, 255, 255)
    line.line.fill.background()

    tx_box = slide.shapes.add_textbox(Inches(12.2), Inches(7), Inches(2), Inches(1))
    p = tx_box.text_frame.paragraphs[0]
    p.text = yard_line_number
    p.font.size = Pt(88)
    p.font.bold = True
    p.font.color.rgb = RGBColor(200, 200, 200)

    # === Layer 2: Player Card ===
    card_left, card_top, card_w, card_h = Inches(2), Inches(1), Inches(5), Inches(7)
    
    # Create group shape for shadow
    group_shape = slide.shapes.add_group_shape()
    group_xml = group_shape.element
    
    # Add Shadow Effect to Group
    spPr = group_xml.find(qn('p:grpSpPr'))
    effect_list = etree.SubElement(spPr, qn('a:effectLst'))
    outer_shadow = etree.SubElement(effect_list, qn('a:outerShdw'))
    outer_shadow.set('blurRad', '152400') # 12pt blur
    outer_shadow.set('dist', '38100')     # 3pt distance
    outer_shadow.set('dir', '2700000')    # 45 degrees
    outer_shadow.set('algn', 'bl')
    outer_shadow.set('rotWithShape', '0')
    srgbClr = etree.SubElement(outer_shadow, qn('a:srgbClr'))
    srgbClr.set('val', '000000')
    alpha = etree.SubElement(srgbClr, qn('a:alpha'))
    alpha.set('val', '50000') # 50% transparent

    # Card Base (Custom Geometry)
    card_base = slide.shapes.add_shape(1, card_left, card_top, card_w, card_h)
    sp = card_base.element
    spPr = sp.find(qn('p:spPr'))
    
    # Define custom geometry
    custGeom = etree.SubElement(spPr, qn('a:custGeom'))
    avLst = etree.SubElement(custGeom, qn('a:avLst'))
    rect = etree.SubElement(custGeom, qn('a:rect'))
    rect.set('t', '0'); rect.set('l', '0'); rect.set('b', 'h'); rect.set('r', 'w')
    pathLst = etree.SubElement(custGeom, qn('a:pathLst'))
    path = etree.SubElement(pathLst, qn('a:path'))
    path.set('w', '100'); path.set('h', '100')

    # Path points for curved cutout rectangle
    etree.SubElement(path, qn('a:moveTo')).append(etree.Element(qn('a:pt'), x='25', y='0'))
    etree.SubElement(path, qn('a:lnTo')).append(etree.Element(qn('a:pt'), x='100', y='0'))
    etree.SubElement(path, qn('a:lnTo')).append(etree.Element(qn('a:pt'), x='100', y='75'))
    etree.SubElement(path, qn('a:arcTo'), wR='75', hR='75', stAng='0', swAng='-5720239')
    etree.SubElement(path, qn('a:lnTo')).append(etree.Element(qn('a:pt'), x='0', y='100'))
    etree.SubElement(path, qn('a:lnTo')).append(etree.Element(qn('a:pt'), x='0', y='25'))
    etree.SubElement(path, qn('a:arcTo'), wR='75', hR='75', stAng='10800000', swAng='-5720239')
    etree.SubElement(path, qn('a:close'))

    card_base.fill.solid()
    card_base.fill.fore_color.rgb = RGBColor(*card_bg_color)
    card_base.line.fill.background()
    group_xml.append(card_base.element) # Move shape into group

    # Holographic Swooshes
    if image_paths.get("holographic"):
        for i in range(2):
            swoosh = slide.shapes.add_shape(1, card_left, card_top, card_w, card_h)
            sp = swoosh.element
            spPr = sp.find(qn('p:spPr'))
            spPr.getparent().replace(spPr, etree.fromstring(spPr.getroottree().tostring(spPr))) # deep copy
            swoosh.fill.picture(image_paths["holographic"])
            swoosh.line.fill.background()
            
            # Adjust geometry for swoosh
            path = swoosh.element.find(f".//{{{nsmap['a']}}}path")
            for child in list(path): path.remove(child) # Clear old path
            
            if i == 0: # Top swoosh
                path.set('fill','none')
                etree.SubElement(path, qn('a:moveTo')).append(etree.Element(qn('a:pt'), x='0', y='25'))
                etree.SubElement(path, qn('a:arcTo'), wR='75', hR='75', stAng='10800000', swAng='-5720239')
                etree.SubElement(path, qn('a:arcTo'), wR='85', hR='85', stAng='5079761', swAng='5720239')
            else: # Bottom swoosh
                path.set('fill','none')
                etree.SubElement(path, qn('a:moveTo')).append(etree.Element(qn('a:pt'), x='100', y='75'))
                etree.SubElement(path, qn('a:arcTo'), wR='75', hR='75', stAng='0', swAng='-5720239')
                etree.SubElement(path, qn('a:arcTo'), wR='85', hR='85', stAng='-5720239', swAng='5720239')
            group_xml.append(swoosh.element)

    # Photo and Frame
    frame_inset = Inches(0.2)
    photo_shape = slide.shapes.add_shape(
        18, # Rounded rectangle
        card_left + frame_inset, card_top + frame_inset,
        card_w - 2 * frame_inset, card_h - 2 * frame_inset
    )
    if image_paths.get("player"):
        photo_shape.fill.picture(image_paths["player"])
    photo_shape.line.fill.background()
    group_xml.append(photo_shape.element)

    border_shape = slide.shapes.add_shape(
        18,
        card_left + frame_inset, card_top + frame_inset,
        card_w - 2 * frame_inset, card_h - 2 * frame_inset
    )
    border_shape.fill.background()
    border_shape.line.solid()
    border_shape.line.color.rgb = RGBColor(255, 255, 255)
    border_shape.line.width = Pt(2)
    group_xml.append(border_shape.element)

    if image_paths.get("logo"):
        logo_size = Inches(1)
        slide.shapes.add_picture(
            image_paths["logo"],
            card_left + card_w - logo_size - Inches(0.3),
            card_top + card_h - logo_size - Inches(0.3),
            width=logo_size
        )

    # === Layer 3: Text & Content ===
    title_box = slide.shapes.add_textbox(Inches(7.5), Inches(2), Inches(5), Inches(1))
    p = title_box.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = player_name
    run.font.name = 'Bebas Neue'
    run.font.size = Pt(60)
    run.font.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255) # Fallback color

    # Apply Gold Texture to Text
    if image_paths.get("gold"):
        rPr = run._r.get_or_add_rPr()
        blip_fill = etree.SubElement(rPr, qn('a:blipFill'))
        blip = etree.SubElement(blip_fill, qn('a:blip'))
        blip.set(qn('r:embed'), slide.part.relate_to(image_paths["gold"], "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image").rId)
        stretch = etree.SubElement(blip_fill, qn('a:stretch'))
        etree.SubElement(stretch, qn('a:fillRect'))

    body_box = slide.shapes.add_textbox(Inches(7.5), Inches(3.2), Inches(4.5), Inches(3))
    p_body = body_box.text_frame.paragraphs[0]
    p_body.text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Maecenas porttitor congue massa. Fusce posuere, magna sed pulvinar ultricies, purus lectus malesuada libero, sit amet commodo magna eros quis urna."
    p_body.font.name = 'Calibri Light'
    p_body.font.size = Pt(14)
    p_body.font.color.rgb = RGBColor(220, 220, 220)
    
    prs.save(output_pptx_path)
    
    # Clean up temp files
    for path in image_paths.values():
        if path and os.path.exists(path):
            os.remove(path)
    os.rmdir("temp_assets")
    
    return output_pptx_path

