import urllib.request
from io import BytesIO

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.shapes.freeform import FreeformBuilder

def create_slide(
    output_pptx_path: str,
    conference_title: str = "LaravelConf",
    conference_tagline: str = "Taiwan 2018",
    conference_subtitle: str = "from {{$idea}} to {{$production}}",
    section_title: str = "議程介紹",
    session_title: str = "開源之路：從解決問題到解決大家的問題",
    speaker_name: str = "周建毅 (Miles)",
    speaker_title: str = "一零四資訊科技 資深工程師",
    image_url: str = "https://images.unsplash.com/photo-1543269865-cbf427effbad?w=1200",
    accent_color_rgb: tuple = (235, 87, 87),
    **kwargs,
) -> str:
    """
    Creates a PPTX slide reproducing the 'Modern Conference Speaker Intro' style.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        conference_title: Main title of the conference.
        conference_tagline: Tagline or year for the conference.
        conference_subtitle: Subtitle for the conference.
        section_title: Title for the agenda section.
        session_title: Title of the specific talk or session.
        speaker_name: Name of the speaker.
        speaker_title: Title and affiliation of the speaker.
        image_url: URL of the speaker or event photo.
        accent_color_rgb: The main accent color (e.g., for shapes and highlights).

    Returns:
        The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Define colors
    accent_color = RGBColor(*accent_color_rgb)
    black_color = RGBColor(0, 0, 0)
    grey_color = RGBColor(136, 136, 136)
    overlay_color_rgb = (252, 246, 245) # A light pink/peach derived from the accent

    # --- Layer 1: Speaker Image ---
    try:
        with urllib.request.urlopen(image_url) as response:
            image_stream = BytesIO(response.read())
            slide.shapes.add_picture(
                image_stream, 
                left=Inches(6.6), 
                top=Inches(1.25), 
                width=Inches(5.6), 
                height=Inches(5.0)
            )
    except Exception as e:
        print(f"Warning: Could not download image. Using a placeholder. Error: {e}")
        # Add a placeholder shape if image fails
        slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 
            left=Inches(6.6), 
            top=Inches(1.25), 
            width=Inches(5.6), 
            height=Inches(5.0)
        )

    # --- Layer 2: Geometric Accents ---
    # Top-left red rotated square
    with FreeformBuilder(
        slide.shapes, Inches(0.5), Inches(0.5), Inches(1), Inches(1)
    ) as builder:
        builder.add_line_segments([(Inches(1.5), Inches(0.5)), (Inches(1.5), Inches(1.5)), (Inches(0.5), Inches(1.5)), (Inches(0.5), Inches(0.5))], close=True)
        ff_shape = builder.convert_to_shape()
        ff_shape.rotation = 45
        ff_shape.fill.solid()
        ff_shape.fill.fore_color.rgb = accent_color
        ff_shape.line.fill.background()

    # Bottom-right red rotated square (overlapping the image)
    with FreeformBuilder(
        slide.shapes, Inches(5.0), Inches(5.5), Inches(2), Inches(2)
    ) as builder:
        builder.add_line_segments([(Inches(7.0), Inches(5.5)), (Inches(7.0), Inches(7.5)), (Inches(5.0), Inches(7.5)), (Inches(5.0), Inches(5.5))], close=True)
        ff_shape_2 = builder.convert_to_shape()
        ff_shape_2.rotation = 45
        ff_shape_2.fill.solid()
        ff_shape_2.fill.fore_color.rgb = accent_color
        ff_shape_2.line.fill.background()

    # --- Layer 3: Text and Overlays ---
    # Left panel text
    # Conference Title
    txBox = slide.shapes.add_textbox(Inches(1.25), Inches(2.2), Inches(4), Inches(1))
    p = txBox.text_frame.paragraphs[0]
    p.text = conference_title
    p.font.name = 'Helvetica Neue'
    p.font.bold = True
    p.font.size = Pt(44)
    p.font.color.rgb = black_color
    p.add_run().text = f" {conference_tagline}"
    p.runs[1].font.bold = False

    # Conference Subtitle in red box
    subtitle_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.25), Inches(3.2), Inches(3.5), Inches(0.5))
    subtitle_box.fill.solid()
    subtitle_box.fill.fore_color.rgb = accent_color
    subtitle_box.line.fill.background()
    subtitle_box.text_frame.text = conference_subtitle
    subtitle_box.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    subtitle_box.text_frame.paragraphs[0].font.size = Pt(16)
    subtitle_box.text_frame.paragraphs[0].font.name = 'Courier New'

    # Section Title
    txBox2 = slide.shapes.add_textbox(Inches(1.25), Inches(4.5), Inches(4), Inches(1))
    p2 = txBox2.text_frame.paragraphs[0]
    p2.text = section_title
    p2.font.bold = True
    p2.font.size = Pt(40)
    p2.font.name = 'Microsoft JhengHei'
    p2.font.color.rgb = accent_color

    # Right panel overlay and text
    overlay = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.6), Inches(5.0), Inches(5.6), Inches(1.75))
    overlay.fill.solid()
    overlay.fill.fore_color.rgb = RGBColor(*overlay_color_rgb)
    overlay.fill.transparency = 0.15
    overlay.line.fill.background()

    # Session Title
    txBox3 = slide.shapes.add_textbox(Inches(6.8), Inches(5.1), Inches(5.2), Inches(1))
    txBox3.text_frame.word_wrap = True
    p3 = txBox3.text_frame.paragraphs[0]
    p3.text = session_title
    p3.font.bold = True
    p3.font.size = Pt(22)
    p3.font.name = 'Microsoft JhengHei'
    p3.font.color.rgb = black_color

    # Speaker Name and Title
    txBox4 = slide.shapes.add_textbox(Inches(6.8), Inches(6.1), Inches(5.2), Inches(0.5))
    p4 = txBox4.text_frame.paragraphs[0]
    p4.text = f"{speaker_name}\n{speaker_title}"
    p4.font.size = Pt(14)
    p4.font.name = 'Microsoft JhengHei'
    p4.font.color.rgb = black_color
    p4.line_spacing = 1.2
    
    # Re-order the overlapping diamond to be on top
    sp = ff_shape_2._sp
    sp.getparent().remove(sp)
    sp.getparent().append(sp)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# create_slide("modern_conference_intro.pptx")

