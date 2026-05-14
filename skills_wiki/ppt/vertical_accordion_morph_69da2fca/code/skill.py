import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.enum.text import PP_ALIGN
from lxml import etree

# Helper function to add morph transition to a slide
def add_morph_transition(slide, duration_ms=750):
    """
    Adds a morph transition to the given slide using lxml.
    """
    slide_element = slide._element
    # Find or create the <p:transition> element
    transition_tag = "{http://schemas.openxmlformats.org/presentationml/2006/main}transition"
    morph_tag = "{http://schemas.microsoft.com/office/powerpoint/2012/main}morph"
    
    transition = slide_element.find(transition_tag)
    if transition is None:
        transition = etree.Element(transition_tag)
        slide_element.insert(0, transition)
        
    transition.set("dur", str(duration_ms))
    
    # Ensure the morph sub-element exists
    morph = transition.find(morph_tag)
    if morph is None:
        # Register namespace for p14
        nsmap = {'p14': 'http://schemas.microsoft.com/office/powerpoint/2012/main'}
        morph = etree.Element(etree.QName(nsmap['p14'], 'morph'), nsmap=nsmap)
        transition.append(morph)
        
    morph.set("type", "byObject")


# Helper to add a shadow effect to a shape
def add_shadow_effect(shape):
    """
    Adds a right-offset shadow effect to a shape using lxml.
    """
    spPr = shape.element.spPr
    a_ns = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    effectLst = etree.SubElement(spPr, f"{a_ns}effectLst")
    outerShdw = etree.SubElement(effectLst, f"{a_ns}outerShdw")
    outerShdw.set("blurRad", "140000")
    outerShdw.set("dist", "30000")
    outerShdw.set("dir", "0")
    outerShdw.set("algn", "ctr")
    srgbClr = etree.SubElement(outerShdw, f"{a_ns}srgbClr")
    srgbClr.set("val", "000000")
    alpha = etree.SubElement(srgbClr, f"{a_ns}alpha")
    alpha.set("val", "50000")

# Helper to rotate text in a shape
def rotate_text(text_frame, angle_degrees=-90):
    """
    Rotates the text within a shape's text_frame. -90 = vertical bottom-to-top.
    """
    a_ns = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    rotation_value = str(int(angle_degrees * 60000))
    txBody = text_frame._txBody
    bodyPr = txBody.find(f"{a_ns}bodyPr")
    if bodyPr is None:
        bodyPr = etree.SubElement(txBody, f"{a_ns}bodyPr")
    bodyPr.set('rot', rotation_value)
    # This setting helps stack text vertically
    bodyPr.set('vert', 'wordArtVert') 

class AccordionPresentationBuilder:
    def __init__(self, prs, topics):
        self.prs = prs
        self.slide_width = prs.slide_width
        self.slide_height = prs.slide_height
        self.topics = topics
        self.num_topics = len(topics)
        
        self.colors = [(223, 54, 114), (176, 32, 113), (96, 21, 80), (0, 0, 0)]
        self.title_panel_color = (242, 242, 242)
        self.title_text_color = (96, 21, 80)
        self.content_text_color = (255, 255, 255)
        self.collapsed_width = Inches(0.65)
        self.title_collapsed_width = Inches(0.65)

    def _add_shared_elements(self, slide, active_topic_index=-1):
        x_pos = 0
        panel_order = list(range(self.num_topics)) # 0, 1, 2, 3
        
        # Draw panels for topics
        for i in panel_order:
            is_active = (i == active_topic_index)
            
            total_collapsed_width = self.collapsed_width * (self.num_topics - 1) + self.title_collapsed_width
            panel_width = self.slide_width - total_collapsed_width if is_active else self.collapsed_width
            
            # Create panel
            panel = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x_pos, 0, panel_width, self.slide_height)
            panel.name = f"!!panel_{i}"
            panel.fill.solid()
            panel.fill.fore_color.rgb = RGBColor(*self.colors[i])
            panel.line.fill.background()
            add_shadow_effect(panel)

            # Create number circle
            circle_dia = Inches(0.4)
            circle_x = x_pos + (self.collapsed_width - circle_dia) / 2
            circle_y = Inches(0.3)
            if is_active:
                circle_x = self.slide_width - self.title_collapsed_width - Inches(0.5)
            
            circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, circle_x, circle_y, circle_dia, circle_dia)
            circle.name = f"!!circle_{i}"
            circle.fill.solid()
            circle.fill.fore_color.rgb = RGBColor(*self.colors[i]) if not is_active else RGBColor(255, 255, 255)
            circle.line.color.rgb = RGBColor(255, 255, 255)
            circle.line.width = Pt(1.5)

            # Add number to circle
            tf = circle.text_frame
            tf.text = str(i + 1)
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.font.bold = True
            p.font.size = Pt(16)
            p.font.color.rgb = RGBColor(255, 255, 255) if not is_active else RGBColor(*self.colors[i])
            
            # Add topic heading
            if is_active:
                # Horizontal heading for active slide
                tx_box = slide.shapes.add_textbox(Inches(0.5) + x_pos, Inches(1.5), panel_width - Inches(2), Inches(1))
                tx_box.name = f"!!heading_{i}"
                tf = tx_box.text_frame
                tf.text = self.topics[i]['heading']
                p = tf.paragraphs[0]
                p.font.bold = True
                p.font.size = Pt(32)
                p.font.color.rgb = self.content_text_color
                
                # Body text for active slide
                body_box = slide.shapes.add_textbox(Inches(0.5) + x_pos, Inches(2.5), panel_width - Inches(2), Inches(4))
                tf = body_box.text_frame
                tf.text = self.topics[i]['body']
                p = tf.paragraphs[0]
                p.font.size = Pt(18)
                p.font.color.rgb = self.content_text_color
            else:
                # Vertical heading for inactive slides
                tx_box = slide.shapes.add_textbox(x_pos - Inches(1), self.slide_height - Inches(0.5) - Inches(3), Inches(3), self.collapsed_width)
                tx_box.name = f"!!heading_{i}"
                tf = tx_box.text_frame
                tf.text = self.topics[i]['heading'].replace("\n", " ")
                p = tf.paragraphs[0]
                p.font.bold = True
                p.font.size = Pt(12)
                p.font.color.rgb = self.content_text_color
                rotate_text(tf)

            if is_active:
                x_pos += panel_width

        # Rightmost (Title) panel
        title_panel = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x_pos, 0, self.slide_width - x_pos, self.slide_height)
        title_panel.name = "!!title_panel"
        title_panel.fill.solid()
        title_panel.fill.fore_color.rgb = RGBColor(*self.title_panel_color)
        title_panel.line.fill.background()
        
        # Presentation Title Text
        if active_topic_index == -1: # Title slide
            title_box = slide.shapes.add_textbox(x_pos + Inches(1), Inches(3), self.slide_width - x_pos - Inches(2), Inches(2))
            title_box.name = "!!title_text"
            tf = title_box.text_frame
            tf.text = "PRESENTATION\nTITLE GOES HERE"
            p = tf.paragraphs[0]
            p.font.bold = True
            p.font.size = Pt(36)
            p.font.color.rgb = self.title_text_color
            p.alignment = PP_ALIGN.CENTER
        else: # Topic slide (title text is vertical)
             title_box = slide.shapes.add_textbox(x_pos - Inches(1), self.slide_height - Inches(0.5) - Inches(3), Inches(3), self.collapsed_width)
             title_box.name = "!!title_text"
             tf = title_box.text_frame
             tf.text = "PRESENTATION TITLE"
             p = tf.paragraphs[0]
             p.font.bold = True
             p.font.size = Pt(12)
             p.font.color.rgb = self.title_text_color
             rotate_text(tf)


    def build(self):
        # Slide 1: Title
        title_slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        self._add_shared_elements(title_slide, active_topic_index=-1)
        
        # Topic Slides
        for i in range(self.num_topics):
            topic_slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
            self._add_shared_elements(topic_slide, active_topic_index=i)
            add_morph_transition(topic_slide)

        # Final "Thank You" Slide (same layout as title slide)
        end_slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        self._add_shared_elements(end_slide, active_topic_index=-1)
        add_morph_transition(end_slide)
        # Customize title text for the end slide
        for shape in end_slide.shapes:
            if shape.name == "!!title_text":
                shape.text_frame.text = "THANK YOU"
                break


def create_slide(output_pptx_path: str, **kwargs) -> str:
    """
    Creates a PPTX file reproducing the Vertical Accordion Morph visual effect.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    topics_data = [
        {"heading": "TOPIC #1 HEADING", "body": "Add some text here. This is the main content area for the first topic. You can add bullet points or detailed descriptions."},
        {"heading": "TOPIC #2 HEADING", "body": "This is the content for the second topic. The morph transition provides a seamless flow between sections."},
        {"heading": "TOPIC #3 HEADING", "body": "Content for the third topic. Each panel maintains a consistent look and feel throughout the presentation."},
        {"heading": "TOPIC #4 HEADING", "body": "Final topic content. This structure is excellent for organizing complex information into digestible parts."},
    ]

    builder = AccordionPresentationBuilder(prs, topics_data)
    builder.build()

    prs.save(output_pptx_path)
    return output_pptx_path
