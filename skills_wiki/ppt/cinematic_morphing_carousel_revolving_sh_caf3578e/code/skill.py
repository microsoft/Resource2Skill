import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml, OxmlElement
from pptx.dml.color import RGBColor
from PIL import Image, ImageDraw, ImageFont

def _create_placeholder_poster(filename: str, color: tuple, text: str):
    """Generates a dummy poster image using PIL for the carousel."""
    img = Image.new('RGB', (800, 1200), color)
    draw = ImageDraw.Draw(img)
    
    # Draw a simple border
    draw.rectangle([20, 20, 780, 1180], outline=(255, 255, 255), width=10)
    
    # Try to add text, fallback to default font if none available
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except IOError:
        font = ImageFont.load_default()
        
    # Center text
    # textbbox gives (left, top, right, bottom)
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((800-w)/2, (1200-h)/2), text, font=font, fill=(255, 255, 255))
    
    img.save(filename)
    return filename

def _inject_morph_transition(slide):
    """Injects the OOXML necessary to apply the Morph transition to a slide."""
    # PowerPoint Slide XML requires a specific order. 
    # <p:transition> must come after <p:cSld> and <p:clrMapOvr> (if present).
    # It must come before <p:timing> and <p:extLst>.
    
    # Create the transition element
    transition = OxmlElement('p:transition')
    transition.set('spd', 'med') # Speed: slow, med, fast
    
    # Create the morph sub-element
    morph = OxmlElement('p15:morph')
    morph.set('option', 'byObject')
    # Assign the required namespace for p15
    morph.nsmap['p15'] = "http://schemas.microsoft.com/office/powerpoint/2012/main"
    
    transition.append(morph)
    
    # Insert transition into the slide element tree safely
    slide_elm = slide._element
    # Find insertion point (append to end if timing/extLst don't exist)
    insert_idx = len(slide_elm)
    for i, child in enumerate(slide_elm):
        if child.tag.endswith('timing') or child.tag.endswith('extLst'):
            insert_idx = i
            break
            
    slide_elm.insert(insert_idx, transition)

def create_slide(
    output_pptx_path: str,
    title_text: str = "Cinematic Morphing Carousel",
    bg_color: tuple = (30, 30, 40),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Morphing Carousel visual effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Colors for our 3 items
    colors = [
        (0, 191, 255),    # Cyan
        (255, 127, 80),   # Coral
        (255, 215, 0)     # Yellow
    ]
    labels = ["Item A", "Item B", "Item C"]
    image_paths = []
    
    # Generate assets
    for i in range(3):
        path = f"temp_poster_{i}.png"
        _create_placeholder_poster(path, colors[i], labels[i])
        image_paths.append(path)

    # Layout Definitions (X, Y, Width)
    # Heights are auto-calculated by aspect ratio
    LAYOUTS = {
        "center_active": (Inches(4.66), Inches(1.0), Inches(4.0)),
        "left_inactive":  (Inches(1.0), Inches(2.0), Inches(2.5)),
        "right_inactive": (Inches(9.8), Inches(2.0), Inches(2.5)),
        "hidden_left":    (Inches(-4.0), Inches(3.0), Inches(1.5)),
        "hidden_right":   (Inches(15.0), Inches(3.0), Inches(1.5))
    }

    # Configuration for each slide in the carousel
    # Dictates where Item 0, Item 1, and Item 2 should be placed on Slides 1, 2, and 3
    slide_configs = [
        # Slide 1: Item 0 Center, Item 1 Right, Item 2 Hidden Right
        [LAYOUTS["center_active"], LAYOUTS["right_inactive"], LAYOUTS["hidden_right"]],
        
        # Slide 2: Item 0 Left, Item 1 Center, Item 2 Right
        [LAYOUTS["left_inactive"], LAYOUTS["center_active"], LAYOUTS["right_inactive"]],
        
        # Slide 3: Item 0 Hidden Left, Item 1 Left, Item 2 Center
        [LAYOUTS["hidden_left"], LAYOUTS["left_inactive"], LAYOUTS["center_active"]]
    ]

    for slide_idx, config in enumerate(slide_configs):
        slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
        
        # Set background
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(*bg_color)
        
        # Add Title
        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.2), Inches(11.33), Inches(0.8))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"{title_text} - View {slide_idx + 1}"
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        
        # Insert shapes based on config
        # We process them in a specific order so the Center (active) item is added LAST,
        # ensuring it has the highest Z-index (appears on top of inactive items).
        
        # Determine Z-order: we want "center_active" to be added last
        indexed_config = list(enumerate(config))
        # Sort so that the element configured as "center_active" is at the end of the list
        indexed_config.sort(key=lambda x: 1 if x[1] == LAYOUTS["center_active"] else 0)
        
        for item_idx, layout in indexed_config:
            x, y, w = layout
            pic = slide.shapes.add_picture(image_paths[item_idx], x, y, width=w)
            
            # THE MAGIC TRICK: Force Morph identification by using the "!!" prefix
            # This guarantees PowerPoint maps this specific picture to the corresponding 
            # picture on the next slide, interpolating scale and position.
            pic.name = f"!!CarouselItem_{item_idx}"
        
        # Inject Morph XML for Slide 2 and Slide 3
        if slide_idx > 0:
            _inject_morph_transition(slide)

    prs.save(output_pptx_path)
    
    # Cleanup temporary images
    for path in image_paths:
        if os.path.exists(path):
            os.remove(path)
            
    return output_pptx_path

if __name__ == "__main__":
    create_slide("morphing_carousel.pptx")
    print("Presentation created successfully with Morph transitions injected.")
