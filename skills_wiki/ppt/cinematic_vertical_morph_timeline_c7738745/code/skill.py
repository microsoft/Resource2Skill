import os
import io
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    title_text: str = "History Timeline",  # Used for fallback/meta
    **kwargs
) -> str:
    """
    Creates a PPTX file reproducing the Cinematic Vertical Morph Timeline effect.
    Generates 3 slides to demonstrate the shifting timeline structure.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Timeline Data Payload
    timeline_data = [
        {
            "year": "1899",
            "title": "The Beginning",
            "subtitle": "Foundation laid in London",
            "desc": "The initial blueprints were drawn up, establishing the core principles that would guide the project for decades.",
            "image_keyword": "blueprint"
        },
        {
            "year": "1912",
            "title": "TITANIC",
            "subtitle": "April 10th | Great Britain",
            "desc": "The monumental launch sequence. 897 members boarded the vessel on its maiden voyage across the Atlantic.",
            "image_keyword": "ship"
        },
        {
            "year": "1920",
            "title": "Revolt",
            "subtitle": "March 13th | Marine-Brigade",
            "desc": "A period of unrest and massive structural changes within the organization, leading to a new era of management.",
            "image_keyword": "crowd"
        },
        {
            "year": "1932",
            "title": "Expansion",
            "subtitle": "New Horizons",
            "desc": "Expanding beyond borders, establishing new routes and modernizing the fleet.",
            "image_keyword": "bridge"
        }
    ]

    # Style Constants
    BG_COLOR_RGB = (20, 20, 20)
    ACTIVE_COLOR = RGBColor(255, 255, 255)
    DIM_COLOR = RGBColor(150, 150, 150)
    
    CENTER_Y = Inches(3.75)
    LINE_X = Inches(1.5)
    SPACING = Inches(1.4) # Vertical distance between nodes

    def create_cinematic_bg(keyword, index):
        """Fetches an image and blends it into a dark background using PIL."""
        bg_width, bg_height = 1920, 1080
        base_img = Image.new('RGB', (bg_width, bg_height), BG_COLOR_RGB)
        
        try:
            # Fetch random image based on keyword
            url = f"https://source.unsplash.com/1000x1080/?{keyword}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                photo = Image.open(io.BytesIO(response.read())).convert("RGBA")
            
            # Resize and crop to fit right side of screen
            photo_ratio = photo.width / photo.height
            target_ratio = 1000 / 1080
            if photo_ratio > target_ratio:
                new_width = int(photo.height * target_ratio)
                left = (photo.width - new_width) // 2
                photo = photo.crop((left, 0, left + new_width, photo.height))
            else:
                new_height = int(photo.width / target_ratio)
                top = (photo.height - new_height) // 2
                photo = photo.crop((0, top, photo.width, top + new_height))
                
            photo = photo.resize((1000, 1080), Image.LANCZOS)
            
            # Create Alpha Mask for smooth gradient blend on the left edge
            mask = Image.new('L', (1000, 1080), 0)
            draw = ImageDraw.Draw(mask)
            # Fading over 600 pixels
            for x in range(600):
                alpha = int((x / 600) * 255)
                draw.line([(x, 0), (x, 1080)], fill=alpha)
            # Solid for the rest
            draw.rectangle([(600, 0), (1000, 1080)], fill=255)
            
            # Paste photo onto base using the mask
            base_img.paste(photo, (920, 0), mask)
            
        except Exception as e:
            # Fallback if download fails: Simple dark gradient
            draw = ImageDraw.Draw(base_img)
            for x in range(bg_width):
                r = int(BG_COLOR_RGB[0] + (x/bg_width)*30)
                g = int(BG_COLOR_RGB[1] + (x/bg_width)*30)
                b = int(BG_COLOR_RGB[2] + (x/bg_width)*50)
                draw.line([(x, 0), (x, bg_height)], fill=(r,g,b))

        temp_path = f"temp_bg_{index}.png"
        base_img.save(temp_path)
        return temp_path

    # Generate a slide for each of the first 3 events being the "Active" one
    for active_idx in range(len(timeline_data) - 1):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # 1. Apply Cinematic Background
        bg_path = create_cinematic_bg(timeline_data[active_idx]["image_keyword"], active_idx)
        slide.shapes.add_picture(bg_path, 0, 0, width=Inches(13.333), height=Inches(7.5))
        os.remove(bg_path) # Clean up temp image
        
        # 2. Draw Continuous Vertical Axis
        line = slide.shapes.add_shape(
            1, # MSO_SHAPE.LINE
            LINE_X, Inches(-2), LINE_X, Inches(9.5) # Extended off screen
        )
        line.line.color.rgb = DIM_COLOR
        line.line.width = Pt(1.5)

        # 3. Render Timeline Nodes and Text
        for i, event in enumerate(timeline_data):
            # Calculate Y position relative to the active index (creates scrolling effect)
            offset = i - active_idx
            node_y = CENTER_Y + (offset * SPACING)
            
            is_active = (i == active_idx)
            
            # Draw Circle
            circle_size = Inches(0.55) if is_active else Inches(0.3)
            circle = slide.shapes.add_shape(
                9, # MSO_SHAPE.OVAL
                LINE_X - (circle_size/2), 
                node_y - (circle_size/2), 
                circle_size, circle_size
            )
            
            if is_active:
                circle.fill.solid()
                circle.fill.fore_color.rgb = ACTIVE_COLOR
                circle.line.color.rgb = ACTIVE_COLOR
                circle.line.width = Pt(1.5)
            else:
                circle.fill.background() # No fill/transparent
                circle.line.color.rgb = DIM_COLOR
                circle.line.width = Pt(2)
                
            # Draw Year Text Next to Circle
            tx_box = slide.shapes.add_textbox(
                LINE_X + Inches(0.5), 
                node_y - Inches(0.4), 
                Inches(2), Inches(0.8)
            )
            tf = tx_box.text_frame
            p = tf.add_paragraph()
            p.text = event["year"]
            p.font.name = 'Arial'
            if is_active:
                p.font.size = Pt(44)
                p.font.bold = True
                p.font.color.rgb = ACTIVE_COLOR
            else:
                p.font.size = Pt(18)
                p.font.bold = False
                p.font.color.rgb = DIM_COLOR
                
        # 4. Render Active Event Content Details (Right side)
        active_event = timeline_data[active_idx]
        
        content_box = slide.shapes.add_textbox(
            LINE_X + Inches(3.5), 
            CENTER_Y - Inches(1.5), 
            Inches(7), Inches(3)
        )
        tf = content_box.text_frame
        
        # Title
        p1 = tf.paragraphs[0]
        p1.text = active_event["title"]
        p1.font.name = 'Arial'
        p1.font.size = Pt(54)
        p1.font.bold = True
        p1.font.color.rgb = ACTIVE_COLOR
        
        # Subtitle
        p2 = tf.add_paragraph()
        p2.text = active_event["subtitle"]
        p2.font.name = 'Arial'
        p2.font.size = Pt(22)
        p2.font.italic = True
        p2.font.color.rgb = RGBColor(200, 200, 200)
        
        # Spacer
        tf.add_paragraph().font.size = Pt(10)
        
        # Description
        p3 = tf.add_paragraph()
        p3.text = active_event["desc"]
        p3.font.name = 'Arial'
        p3.font.size = Pt(16)
        p3.font.color.rgb = DIM_COLOR
        p3.line_spacing = 1.2

    prs.save(output_pptx_path)
    return output_pptx_path
