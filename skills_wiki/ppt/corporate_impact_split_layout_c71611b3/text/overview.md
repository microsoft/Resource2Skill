# Corporate Impact Split-Layout

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Corporate Impact Split-Layout

* **Core Visual Mechanism**: This design relies on strict, block-based information compartmentalization. It features a muted, full-width header band establishing context, a prominent, centered Call-To-Action (CTA) acting as a visual anchor, and a classic 1/3 to 2/3 column split at the bottom contrasting a bold, solid-fill geometric shape (the "impact" icon) against a block of explanatory text. 

* **Why Use This Skill (Rationale)**: The layout is highly utilitarian and functional. By isolating the branding/title in a distinct gray zone, the viewer's eye is immediately drawn down to the white space where the accent color pops. The massive contrast between the large circular graphic and the paragraph text creates an unmistakable visual hierarchy: "Look at this big concept first, then read the details."

* **Overall Applicability**: Ideal for pitch decks, corporate social responsibility (CSR) summaries, program overviews, or "Next Steps/Contact Us" closing slides where you need to balance a strong CTA with supporting philosophical or structural details.

* **Value Addition**: Compared to a standard bulleted slide, this layout transforms a dense paragraph into a structured "Impact Statement." The recurring template (seen in blue, green, and orange in the tutorial) builds strong structural consistency across a presentation while using color to signify different modules or themes.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Header Band**: A full-width, light gray rectangle providing a subtle foundation for titles without overpowering the slide.
  - **Iconography**: Minimalist. A simple circular badge for the `@` symbol and a massive solid circle for the primary logo/concept (e.g., "B1G1").
  - **Color Logic**:
    - Canvas: Pure White `(255, 255, 255)`
    - Header Fill: Light Gray `(242, 242, 242)`
    - Primary Accent (varies by section, e.g., Green): `(65, 168, 95)` — Used for titles, CTA text, and the large graphic fill.
    - Body Text: Dark Charcoal `(80, 80, 80)` for readability.
  - **Text Hierarchy**: 
    1. Slide Title (Accent color, largest, ~36pt)
    2. Logo/Icon Text inside the circle (White, massive, ~54pt, bold)
    3. CTA Email (Accent color, medium, ~24pt)
    4. Body Paragraph (Dark Gray, standard, ~18pt)

* **Step B: Compositional Style**
  - **Top 20%**: Context area (Header). Left-aligned title, right-aligned generic tagline.
  - **Middle 30%**: Action area. Centered vertically and horizontally within this band.
  - **Bottom 50%**: Details area. Left column (30% width) dedicated entirely to a single oversized shape. Right column (60% width, 10% gutter) for text.

* **Step C: Dynamic Effects & Transitions**
  - The tutorial presents these as static slides. The power comes from the *cut* between slides where the layout remains perfectly rigid, but the accent color and text change, creating a flipbook-like structural consistency.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Layout & Geometry | `python-pptx` native | The design is entirely composed of standard rectangles, ovals, and text boxes. No complex rendering is required. |
| Text Styling & Alignment | `python-pptx` native | Standard paragraph formatting handles the specific center and right alignments required. |

> **Feasibility Assessment**: 100%. This is a purely structural layout that native `python-pptx` handles perfectly. The resulting slide will be structurally and stylistically identical to the core template shown in the video.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Cash Flow Strategy Sessions",
    subtitle_text: str = "By Decisions Plus Strategic",
    tagline_text: str = "Connect with us",
    cta_email: str = "hello@decisionsplusstrategic.com",
    badge_text: str = "B1G1",
    body_text: str = "Each time we hold a Cash Flow Strategy Session, we give our customers an opportunity to choose our giving project.",
    accent_color_rgb: tuple = (65, 168, 95),  # Corporate Green
) -> str:
    """
    Creates a PPTX file reproducing the 'Corporate Impact Split-Layout'.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    # Convert tuple to RGBColor object
    accent_color = RGBColor(*accent_color_rgb)
    dark_gray = RGBColor(80, 80, 80)
    white = RGBColor(255, 255, 255)

    # === 1. Header Band ===
    header_rect = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        0, 0, Inches(13.333), Inches(1.4)
    )
    header_rect.fill.solid()
    header_rect.fill.fore_color.rgb = RGBColor(245, 245, 245)
    header_rect.line.fill.background() # No border

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(6), Inches(0.6))
    tf_title = title_box.text_frame
    p_title = tf_title.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(36)
    p_title.font.color.rgb = accent_color
    p_title.font.name = "Arial"

    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(0.55), Inches(0.8), Inches(6), Inches(0.4))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.add_paragraph()
    p_sub.text = subtitle_text
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = dark_gray
    p_sub.font.name = "Arial"

    # Tagline (Right aligned)
    tagline_box = slide.shapes.add_textbox(Inches(8), Inches(0.4), Inches(4.8), Inches(0.6))
    tf_tag = tagline_box.text_frame
    p_tag = tf_tag.add_paragraph()
    p_tag.text = tagline_text
    p_tag.alignment = PP_ALIGN.RIGHT
    p_tag.font.size = Pt(28)
    p_tag.font.color.rgb = dark_gray
    p_tag.font.name = "Arial"
    p_tag.font.italic = True

    # === 2. Call to Action (Center) ===
    # Small @ badge
    at_circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, 
        Inches(3.8), Inches(2.3), Inches(0.6), Inches(0.6)
    )
    at_circle.fill.background() # Hollow
    at_circle.line.color.rgb = dark_gray
    at_circle.line.width = Pt(2)
    tf_at = at_circle.text_frame
    tf_at.text = "@"
    tf_at.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf_at.paragraphs[0].font.size = Pt(24)
    tf_at.paragraphs[0].font.color.rgb = dark_gray

    # Email Text
    email_box = slide.shapes.add_textbox(Inches(4.5), Inches(2.2), Inches(6), Inches(0.8))
    tf_email = email_box.text_frame
    p_email = tf_email.add_paragraph()
    p_email.text = cta_email
    p_email.font.size = Pt(28)
    p_email.font.color.rgb = accent_color
    p_email.font.name = "Arial"
    p_email.font.underline = True

    # Subtle horizontal divider line
    divider = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        Inches(2), Inches(3.2), Inches(9.333), Inches(0.02)
    )
    divider.fill.solid()
    divider.fill.fore_color.rgb = RGBColor(220, 220, 220)
    divider.line.fill.background()

    # === 3. Lower Split Section ===
    # Left: Big Impact Circle
    big_circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, 
        Inches(1.5), Inches(3.8), Inches(2.8), Inches(2.8)
    )
    big_circle.fill.solid()
    big_circle.fill.fore_color.rgb = accent_color
    big_circle.line.fill.background()
    
    tf_badge = big_circle.text_frame
    tf_badge.vertical_anchor = 3 # Middle alignment
    p_badge = tf_badge.paragraphs[0]
    p_badge.text = badge_text
    p_badge.alignment = PP_ALIGN.CENTER
    p_badge.font.size = Pt(54)
    p_badge.font.color.rgb = white
    p_badge.font.bold = True
    p_badge.font.name = "Arial"

    # Right: Body Text Paragraph
    body_box = slide.shapes.add_textbox(Inches(5.0), Inches(4.0), Inches(7.5), Inches(2.5))
    tf_body = body_box.text_frame
    tf_body.word_wrap = True
    p_body = tf_body.add_paragraph()
    p_body.text = body_text
    p_body.font.size = Pt(22)
    p_body.font.color.rgb = dark_gray
    p_body.font.name = "Arial"
    
    # Adjust line spacing for readability
    p_body.line_spacing = 1.2 

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
```