# Horizontal Testimonial Carousel / Social Proof Slider

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Horizontal Testimonial Carousel / Social Proof Slider

* **Core Visual Mechanism**: A horizontally aligned row of unified "card" containers, each displaying a client review. The layout relies on a strict top-to-bottom visual hierarchy within each card: a circular profile avatar, the reviewer's name, a star rating, and the text body, all center-aligned to create a clean, elegant rhythm.
* **Why Use This Skill (Rationale)**: Social proof is a critical component of persuasion in pitch decks, sales presentations, and company profiles. Presenting testimonials in a horizontal card layout breaks the monotony of standard bullet points, making the text easily digestible while lending a modern, "website-like" interface feel to the slide.
* **Overall Applicability**: Pitch deck "Traction" or "Validation" slides, sales proposals, website design mockups, and agency portfolio presentations. 
* **Value Addition**: Transforms raw review text into an authoritative, visually appealing "carousel" that builds trust. The use of circular avatars and star graphics humanizes the data and visually reinforces quality.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Background**: A soft, muted solid color (e.g., warm beige `(244, 240, 236)` or soft gray) that allows the pure white cards to pop without needing heavy drop shadows.
  * **Containers**: Rounded rectangles acting as individual cards, utilizing white fill `(255, 255, 255)` with no outline to appear clean and modern.
  * **Avatars**: Perfect circle image crops placed at the top center of each card.
  * **Typography**:
    * Main Slide Title: Large, left-aligned or centered, bold serif or clean sans-serif.
    * Reviewer Name: Bold, dark gray/black `(30, 30, 30)`, size 14pt.
    * Star Rating: Text-based unicode stars (★★★★★) in golden yellow `(255, 180, 0)`, size 16pt.
    * Review Text: Regular weight, medium gray `(80, 80, 80)`, size 11pt, center-aligned with generous line spacing.

* **Step B: Compositional Style**
  * The canvas is divided horizontally. The top 25% is reserved for the section title and optional subtitle. 
  * The bottom 75% houses the cards. 
  * Cards are distributed evenly with generous negative space (approx. 0.6 inches between cards) to prevent visual clutter.
  * Content within the card strictly follows a central vertical axis.

* **Step C: Dynamic Effects & Transitions**
  * *In Presentation*: A "Push" or "Pan" transition from the right can simulate the website slider/carousel effect shown in the Canva UI.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Base Layout & Cards** | `python-pptx` native | Ideal for precise coordinate placement of rounded rectangles and text boxes. |
| **Circular Profile Avatars** | `PIL/Pillow` | Native `python-pptx` cannot perfectly crop images into circles with transparency on the fly. PIL handles downloading, cropping with an alpha mask, and injecting it as a ready-to-use PNG. |
| **Star Ratings** | `python-pptx` native | Unicode text characters (★) styled with specific gold RGB colors natively provide the sharpest vector rendering. |

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Client Testimonials.",
    subtitle_text: str = "See what our partners have to say about working with us.",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing a modern Horizontal Testimonial Carousel.
    """
    import io
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image, ImageDraw

    # --- Configuration ---
    bg_color = RGBColor(244, 240, 236)         # Soft warm beige
    card_color = RGBColor(255, 255, 255)       # Pure white
    text_dark = RGBColor(40, 40, 40)           # Dark gray for names
    text_light = RGBColor(100, 100, 100)       # Medium gray for reviews
    star_color = RGBColor(255, 180, 0)         # Golden yellow
    
    # Mock data for the slider
    testimonials = [
        {
            "name": "Hannah Morales",
            "text": "Presentations are communication tools that can be used as demonstrations, lectures, speeches, reports, and more.",
            "avatar_url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=200&q=80"
        },
        {
            "name": "Olivia Wilson",
            "text": "The cleanest design templates I have ever used. They helped us close our Series A funding round with ease.",
            "avatar_url": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=200&q=80"
        },
        {
            "name": "Morgan Maxwell",
            "text": "An absolute game changer for our marketing team. We create beautiful materials in half the time.",
            "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80"
        }
    ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # === Layer 1: Background ===
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = bg_color
    bg_shape.line.fill.background() # No outline

    # === Layer 2: Main Title ===
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.333), Inches(0.8))
    tf = title_box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(36)
    p.font.color.rgb = text_dark
    p.alignment = PP_ALIGN.CENTER

    if subtitle_text:
        sub_p = tf.add_paragraph()
        sub_p.text = subtitle_text
        sub_p.font.size = Pt(14)
        sub_p.font.color.rgb = text_light
        sub_p.font.bold = False
        sub_p.alignment = PP_ALIGN.CENTER

    # === Helper Function: Generate Circular Avatar via PIL ===
    def get_circular_avatar(url, size=(200, 200)):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                img = Image.open(io.BytesIO(response.read())).convert("RGBA")
        except Exception:
            # Fallback if download fails
            img = Image.new("RGBA", size, (200, 200, 200, 255))
        
        # Crop to square
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim)/2
        top = (h - min_dim)/2
        img = img.crop((left, top, left+min_dim, top+min_dim))
        img = img.resize(size, Image.Resampling.LANCZOS)
        
        # Create circular mask
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        
        # Apply mask
        output = Image.new("RGBA", size, (0, 0, 0, 0))
        output.paste(img, (0, 0), mask=mask)
        
        img_byte_arr = io.BytesIO()
        output.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr

    # === Layer 3: Testimonial Cards ===
    num_cards = len(testimonials)
    card_width = Inches(3.4)
    card_height = Inches(4.2)
    gap = Inches(0.5)
    
    # Center the entire block of cards
    total_width = (num_cards * card_width) + ((num_cards - 1) * gap)
    start_x = (prs.slide_width - total_width) / 2
    start_y = Inches(2.2)

    for i, data in enumerate(testimonials):
        # Card X position
        curr_x = start_x + i * (card_width + gap)

        # 1. Card Container (Rounded Rectangle)
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, curr_x, start_y, card_width, card_height
        )
        card.fill.solid()
        card.fill.fore_color.rgb = card_color
        card.line.fill.background()
        card.adjustments[0] = 0.05  # Subtle rounding

        # 2. Circular Avatar Image
        avatar_size = Inches(0.8)
        avatar_x = curr_x + (card_width - avatar_size) / 2
        avatar_y = start_y + Inches(0.4)
        avatar_stream = get_circular_avatar(data["avatar_url"])
        slide.shapes.add_picture(avatar_stream, avatar_x, avatar_y, avatar_size, avatar_size)

        # 3. Name Label
        name_box = slide.shapes.add_textbox(curr_x, avatar_y + avatar_size + Inches(0.1), card_width, Inches(0.4))
        nf = name_box.text_frame
        nf.word_wrap = True
        np = nf.paragraphs[0]
        np.text = data["name"]
        np.font.size = Pt(14)
        np.font.bold = True
        np.font.color.rgb = text_dark
        np.alignment = PP_ALIGN.CENTER

        # 4. Star Ratings
        star_box = slide.shapes.add_textbox(curr_x, avatar_y + avatar_size + Inches(0.45), card_width, Inches(0.4))
        sf = star_box.text_frame
        sp = sf.paragraphs[0]
        sp.text = "★★★★★"
        sp.font.size = Pt(16)
        sp.font.color.rgb = star_color
        sp.alignment = PP_ALIGN.CENTER

        # 5. Review Text
        text_box = slide.shapes.add_textbox(
            curr_x + Inches(0.2), 
            avatar_y + avatar_size + Inches(0.9), 
            card_width - Inches(0.4), 
            Inches(2.0)
        )
        tframe = text_box.text_frame
        tframe.word_wrap = True
        tp = tframe.paragraphs[0]
        tp.text = data["text"]
        tp.font.size = Pt(11)
        tp.font.color.rgb = text_light
        tp.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx_path)
    return output_pptx_path
```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries? (Yes, `io`, `urllib.request`, `pptx`, `PIL` included).
- [x] Does it handle the case where an image download fails? (Yes, fallback `Image.new("RGBA")` acts as a solid gray placeholder).
- [x] Are all color values explicit RGBA/RGB tuples? (Yes, mapped accurately via `RGBColor`).
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes, it accurately mimics the Canva horizontal review card layout).
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes, the visual hierarchy of Profile Image -> Name -> Stars -> Text is identical).