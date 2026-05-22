# Horizontal Flowchart Pagination & Masking (水平流程圖分頁遮罩法)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Horizontal Flowchart Pagination & Masking (水平流程圖分頁遮罩法)

* **Core Visual Mechanism**: This design pattern transforms complex, overwhelming vertical decision trees into digestible horizontal flows. The defining visual signature consists of three layers:
  1. A standardized **left-to-right flowchart** using a neutral gray base.
  2. A **semi-transparent white overlay (mask)** that fades out the inactive branches.
  3. A **vibrant accent color (e.g., orange)** applied only to the active path, paired with a large, clean **annotation box** positioned in the negative space created by the mask.

* **Why Use This Skill (Rationale)**: Complex flowcharts usually suffer from "information overload" because the presenter forces the audience to look at the entire system at once. By converting the flow from vertical to horizontal, it naturally fits the 16:9 screen ratio, allowing for larger text. The "masking" technique leverages the psychological principle of *progressive disclosure*—the audience sees the whole system first (context), then irrelevant parts fade away (focus), guiding their eyes exactly where they need to look without losing the mental map of the system.

* **Overall Applicability**: Perfect for medical diagnostic guidelines, corporate SOPs, technical architecture diagrams, onboarding processes, and any presentation where a complex, multi-branch decision tree needs to be explained step-by-step.

* **Value Addition**: Transforms a dense, unreadable document-style chart into a cinematic, presenter-led visual experience. It forces the presenter to explain one path at a time and provides physical space on the slide to put detailed text where it's actually readable.

---

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Base Nodes**: Light gray rectangles `(242, 242, 242)` with dark gray text `(64, 64, 64)`.
  - **Active Nodes**: High-contrast accent color rectangles, e.g., Orange `(237, 125, 49)` with white bold text `(255, 255, 255)`.
  - **Connectors**: Standard elbow connectors. Inactive ones are light gray; active ones are thick and orange.
  - **The Mask**: A full-screen semi-transparent overlay. Typically White `(255, 255, 255)` at 75%–85% opacity.
  - **Annotation Box**: A floating panel with a white background, a bold accent-colored border, and large, hierarchical text.

* **Step B: Compositional Style**
  - **Direction**: Left-to-right spanning the width of the slide.
  - **Spatial Division**: When the mask is active, the highlighted path takes up ~30% of the visual weight, while the newly introduced Annotation Box occupies ~40% of the slide (usually the bottom or right side), sitting comfortably over the faded branches.

* **Step C: Dynamic Effects & Transitions**
  - **Pagination (Whole-to-Part)**: Slide 1 shows the entire chart. Slide 2 introduces the mask and the specific annotation. If using PowerPoint's native "Morph" transition, this creates a beautiful cinematic fade.

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Flowchart Nodes & Connectors | `python-pptx` native | Standard shapes and elbow connectors natively support layout and text wrapping perfectly. |
| The Semi-Transparent Mask | `PIL/Pillow` | Generating an RGBA PNG with 80% opacity and inserting it as a picture is far more reliable across PPTX versions than trying to inject custom `a:alpha` tags into shape fills. |
| Layering Logic (Bring to Front) | Z-Order emulation via script | By drawing the base chart, adding the PIL mask, and then *re-drawing* the active nodes on top, we perfectly emulate the "fade background, pop foreground" visual effect programmatically. |

#### 3b. Complete Reproduction Code

```python
import os
import tempfile
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN
from PIL import Image

def create_slide(
    output_pptx_path: str,
    title_text: str = "Diagnostic Guideline",
    body_text: str = "Definitive diagnosis of HAE Types I and II requires measurement of C1-INH and C4 levels.\n\nC1-INH function + Genetic testing is NOT essential.",
    accent_color: tuple = (237, 125, 49),  # Orange accent
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Horizontal Flowchart Pagination & Masking" effect.
    Generates two slides:
      Slide 1: Overview of the Flowchart.
      Slide 2: Focus mode (Masked inactive areas + prominent annotation box).
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Define colors
    ACCENT_COLOR = RGBColor(*accent_color)
    BASE_FILL = RGBColor(242, 242, 242)
    BASE_LINE = RGBColor(217, 217, 217)
    TEXT_DARK = RGBColor(64, 64, 64)
    TEXT_LIGHT = RGBColor(255, 255, 255)
    
    # Define Flowchart Data (Medical Guideline Example)
    nodes = {
        "root": {"text": "Suspicion of\nHAE", "pos": (0.5, 3.25), "size": (2.0, 1.0)},
        "type1": {"text": "Type I\nC1-INH Func. ↓\nC4 level ↓", "pos": (4.0, 1.0), "size": (2.2, 1.2)},
        "type2": {"text": "Type II\nC1-INH Func. ↓\nC1-INH level Normal\nC4 level ↓", "pos": (4.0, 3.15), "size": (2.2, 1.2)},
        "normal": {"text": "Normal C1-INH\nC1-INH Func. Normal\nC4 level Normal", "pos": (4.0, 5.3), "size": (2.2, 1.2)},
        "confirm": {"text": "HAE-I\nConfirm by repeating\nblood test", "pos": (7.5, 1.0), "size": (2.5, 1.2)}
    }
    
    edges = [
        ("root", "type1"),
        ("root", "type2"),
        ("root", "normal"),
        ("type1", "confirm")
    ]
    
    active_nodes = ["root", "type1", "confirm"]
    active_edges = [("root", "type1"), ("type1", "confirm")]

    # Helper function to draw the flowchart
    def draw_flowchart(slide, draw_active=True, draw_inactive=True):
        shape_refs = {}
        
        # Draw edges
        for start_id, end_id in edges:
            is_active_edge = (start_id, end_id) in active_edges
            if (is_active_edge and not draw_active) or (not is_active_edge and not draw_inactive):
                continue
                
            n1 = nodes[start_id]
            n2 = nodes[end_id]
            
            # Calculate connection points (Right of start, Left of end)
            x1 = Inches(n1["pos"][0] + n1["size"][0])
            y1 = Inches(n1["pos"][1] + n1["size"][1] / 2)
            x2 = Inches(n2["pos"][0])
            y2 = Inches(n2["pos"][1] + n2["size"][1] / 2)
            
            connector = slide.shapes.add_connector(MSO_CONNECTOR.ELBOW, x1, y1, x2, y2)
            line = connector.line
            if is_active_edge:
                line.color.rgb = ACCENT_COLOR
                line.width = Pt(3)
            else:
                line.color.rgb = BASE_LINE
                line.width = Pt(1.5)

        # Draw nodes
        for node_id, data in nodes.items():
            is_active_node = node_id in active_nodes
            if (is_active_node and not draw_active) or (not is_active_node and not draw_inactive):
                continue

            left, top = Inches(data["pos"][0]), Inches(data["pos"][1])
            width, height = Inches(data["size"][0]), Inches(data["size"][1])
            
            shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
            
            # Adjust rounded corner radius
            shape.adjustments[0] = 0.15 
            
            shape.text = data["text"]
            tf = shape.text_frame
            tf.word_wrap = True
            
            for paragraph in tf.paragraphs:
                paragraph.alignment = PP_ALIGN.CENTER
                paragraph.font.name = "Arial"
                paragraph.font.size = Pt(14)
                if is_active_node:
                    paragraph.font.bold = True
                    paragraph.font.color.rgb = TEXT_LIGHT
                else:
                    paragraph.font.color.rgb = TEXT_DARK
            
            if is_active_node:
                shape.fill.solid()
                shape.fill.fore_color.rgb = ACCENT_COLOR
                shape.line.fill.background()
            else:
                shape.fill.solid()
                shape.fill.fore_color.rgb = BASE_FILL
                shape.line.color.rgb = BASE_LINE
                shape.line.width = Pt(1)

    # ==========================================
    # SLIDE 1: Overview Flowchart
    # ==========================================
    slide_layout = prs.slide_layouts[6] # Blank
    slide1 = prs.slides.add_slide(slide_layout)
    
    # Title
    title_box = slide1.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(8), Inches(0.8))
    title_tf = title_box.text_frame
    p = title_tf.add_paragraph()
    p.text = title_text + " - Overview"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    
    # Draw entire flowchart
    draw_flowchart(slide1, draw_active=True, draw_inactive=True)

    # ==========================================
    # SLIDE 2: Focus Mode (Masked + Annotation)
    # ==========================================
    slide2 = prs.slides.add_slide(slide_layout)
    
    # Title
    title_box2 = slide2.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(8), Inches(0.8))
    title_tf2 = title_box2.text_frame
    p2 = title_tf2.add_paragraph()
    p2.text = title_text + " - Detailed Breakdown"
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_DARK

    # 1. Draw inactive parts (Bottom Layer)
    draw_flowchart(slide2, draw_active=False, draw_inactive=True)
    
    # 2. Apply Semi-Transparent Mask using PIL
    mask_opacity = 210  # roughly 82% opacity (255 * 0.82)
    mask_img = Image.new('RGBA', (100, 100), (255, 255, 255, mask_opacity))
    
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        mask_img.save(tmp.name)
        mask_path = tmp.name
        
    # Cover the area below the title
    slide2.shapes.add_picture(mask_path, Inches(0), Inches(1), prs.slide_width, prs.slide_height - Inches(1))
    os.remove(mask_path)
    
    # 3. Draw active parts (Top Layer, over the mask)
    draw_flowchart(slide2, draw_active=True, draw_inactive=False)
    
    # 4. Add the prominent Annotation Box in the masked negative space
    ann_left = Inches(4.5)
    ann_top = Inches(3.0)
    ann_width = Inches(8.3)
    ann_height = Inches(3.5)
    
    ann_box = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, ann_left, ann_top, ann_width, ann_height)
    ann_box.fill.solid()
    ann_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
    ann_box.line.color.rgb = ACCENT_COLOR
    ann_box.line.width = Pt(4)
    
    # Add text to annotation box
    ann_tf = ann_box.text_frame
    ann_tf.word_wrap = True
    ann_tf.margin_left = Inches(0.5)
    ann_tf.margin_right = Inches(0.5)
    ann_tf.margin_top = Inches(0.5)
    
    p3 = ann_tf.paragraphs[0]
    p3.text = body_text.split('\n\n')[0]
    p3.font.size = Pt(24)
    p3.font.bold = True
    p3.font.color.rgb = TEXT_DARK
    
    if len(body_text.split('\n\n')) > 1:
        p4 = ann_tf.add_paragraph()
        p4.text = "\n" + body_text.split('\n\n')[1]
        p4.font.size = Pt(20)
        p4.font.color.rgb = ACCENT_COLOR
        p4.font.bold = True

    prs.save(output_pptx_path)
    return output_pptx_path
```