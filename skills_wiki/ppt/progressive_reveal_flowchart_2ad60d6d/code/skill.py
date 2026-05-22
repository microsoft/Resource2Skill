import collections
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_CONNECTOR

def create_slide(
    output_pptx_path: str,
    title_text: str = "Complex Flowchart Design: Diagnosis Algorithm",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Progressive Reveal Flowchart technique.

    The presentation includes:
    1. A title slide.
    2. An overview slide showing the complete flowchart.
    3. A detail slide highlighting and annotating a specific part of the flowchart.

    Returns:
        str: The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Define a named tuple for node properties for clarity
    Node = collections.namedtuple('Node', ['id', 'text', 'x', 'y', 'w', 'h', 'children'])

    # --- Flowchart Data and Layout ---
    # Coordinates are in Inches from the top-left corner.
    flowchart_data = {
        'start': Node('start', 'Suspicion\nof HAE', 0.5, 3.25, 1.5, 1.0, ['type1', 'type2', 'type3']),
        'type1': Node('type1', 'Type I\nC1-INH Func. ↓\nC1-INH level ↓\nC4 level ↓', 2.5, 1.0, 2.0, 1.25, ['hae1']),
        'type2': Node('type2', 'Type II\nC1-INH Func. ↓\nC1-INH level n/↑\nC4 level ↓', 2.5, 3.1, 2.0, 1.25, ['hae2']),
        'type3': Node('type3', 'Normal C1-INH3\nC1-INH Func. n\nC1-INH level n\nC4 level n', 2.5, 5.25, 2.0, 1.25, ['repeat']),
        'hae1': Node('hae1', 'HAE-I\nConfirm by repeating blood test', 5.0, 1.2, 2.5, 0.8, ['when_family']),
        'hae2': Node('hae2', 'HAE-II\nConfirm by repeating blood test', 5.0, 3.3, 2.5, 0.8, []),
        'repeat': Node('repeat', 'Repeat blood test\nduring attack', 5.0, 5.5, 1.8, 0.8, ['not_normal', 'normal']),
        'when_family': Node('when_family', 'When family history Neg\nand onset of symptoms\nafter 30 yrs old exclude', 8.0, 0.5, 2.2, 1.2, ['aae']),
        'aae': Node('aae', 'AAE-C1-INH', 10.7, 0.8, 1.5, 0.6, []),
        'not_normal': Node('not_normal', 'Not Normal', 7.3, 4.7, 1.5, 0.5, ['type2']), # Loop back
        'normal': Node('normal', 'Normal', 7.3, 6.3, 1.5, 0.5, ['family_pos', 'family_neg']),
        'family_pos': Node('family_pos', 'Family history Pos or\nFXII/ANGPT1/PLG mutation', 9.3, 5.2, 2.0, 1.0, ['hae_n']),
        'family_neg': Node('family_neg', 'Family history Neg and no\nFXII/ANGPT1/PLG mutation', 9.3, 6.7, 2.0, 1.0, ['mast_cell']),
        'hae_n': Node('hae_n', 'HAE-n-C1-INH', 11.8, 5.5, 1.3, 0.5, []),
        'mast_cell': Node('mast_cell', 'Mast cell mediator-induced AE\nIdiopathic AE\nACEi-AE', 11.8, 7.0, 1.3, 1.0, []),
    }

    # --- Color and Font Definitions ---
    NEUTRAL_FILL = RGBColor(242, 242, 242)
    HIGHLIGHT_FILL = RGBColor(255, 242, 204)
    TEXT_COLOR = RGBColor(50, 50, 50)
    HIGHLIGHT_TEXT_COLOR = RGBColor(198, 89, 17)
    LINE_COLOR = RGBColor(180, 180, 180)
    TITLE_FONT_SIZE = Pt(14)
    BODY_FONT_SIZE = Pt(10)

    # --- Helper Function to Draw the Flowchart ---
    def draw_flowchart(slide, highlight_id=None):
        shapes = {}
        # Draw all nodes first
        for node_id, node in flowchart_data.items():
            is_highlighted = node_id == highlight_id
            
            shape = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(node.x), Inches(node.y), Inches(node.w), Inches(node.h)
            )
            shapes[node_id] = shape
            
            # Text Frame properties
            tf = shape.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            p.text = node.text
            p.font.size = BODY_FONT_SIZE
            p.alignment = PP_ALIGN.CENTER
            tf.vertical_anchor = 1 # MSO_VERTICAL_ANCHOR.MIDDLE
            tf.word_wrap = True
            
            # Apply styling
            fill = shape.fill
            if is_highlighted:
                fill.solid()
                fill.fore_color.rgb = HIGHLIGHT_FILL
                p.font.color.rgb = HIGHLIGHT_TEXT_COLOR
            else:
                fill.solid()
                fill.fore_color.rgb = NEUTRAL_FILL
                p.font.color.rgb = TEXT_COLOR

            line = shape.line
            line.color.rgb = LINE_COLOR
            line.width = Pt(1)

        # Draw all connectors
        for parent_id, parent_node in flowchart_data.items():
            for child_id in parent_node.children:
                parent_shape = shapes[parent_id]
                child_shape = shapes[child_id]
                
                # Simple connector logic (from middle-right of parent to middle-left of child)
                # More complex routing would require a more advanced algorithm
                connector = slide.shapes.add_connector(
                    MSO_CONNECTOR.STRAIGHT,
                    parent_shape.left + parent_shape.width,
                    parent_shape.top + parent_shape.height / 2,
                    child_shape.left,
                    child_shape.top + child_shape.height / 2
                )
                
                connector.line.color.rgb = LINE_COLOR
                connector.line.width = Pt(1)
                connector.line.dash_style = 2 # Dotted
                
                # Add arrowhead
                connector.line.end_arrowhead_style = 2 # MSO_ARROWHEAD.TRIANGLE
    
    # === Slide 1: Title Slide ===
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    title.text = title_text
    
    # === Slide 2: Overview Flowchart ("Forest View") ===
    blank_slide_layout = prs.slide_layouts[6]
    overview_slide = prs.slides.add_slide(blank_slide_layout)
    draw_flowchart(overview_slide)

    # === Slide 3: Detailed View ("Tree View") ===
    detail_slide = prs.slides.add_slide(blank_slide_layout)
    
    # Add semi-transparent mask
    mask = detail_slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    mask.fill.solid()
    mask.fill.fore_color.rgb = RGBColor(255, 255, 255)
    mask.fill.transparency = 0.6  # 60% transparent
    mask.line.fill.background()

    # Redraw flowchart on top, with highlight
    draw_flowchart(detail_slide, highlight_id='type2')

    # Add annotation box
    txBox = detail_slide.shapes.add_textbox(Inches(8.0), Inches(3.8), Inches(4.5), Inches(2.5))
    tf = txBox.text_frame
    tf.clear()

    p1 = tf.paragraphs[0]
    p1.text = "Focus on: Type II Diagnosis"
    p1.font.bold = True
    p1.font.size = Pt(20)
    p1.font.color.rgb = TEXT_COLOR

    p2 = tf.add_paragraph()
    p2.text = "The key differentiator for Type II is the normal or elevated C1-INH level, despite a decrease in function. This distinguishes it from Type I, where both function and level are decreased."
    p2.font.size = Pt(16)
    p2.font.color.rgb = TEXT_COLOR
    p2.level = 1

    prs.save(output_pptx_path)
    return output_pptx_path

# Example of how to run the function
if __name__ == '__main__':
    output_file = "Progressive_Reveal_Flowchart.pptx"
    create_slide(output_file)
    print(f"Presentation saved to {output_file}")
