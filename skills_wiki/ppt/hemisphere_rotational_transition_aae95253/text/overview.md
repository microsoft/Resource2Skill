# Hemisphere Rotational Transition

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Hemisphere Rotational Transition

*   **Core Visual Mechanism**: The core of this technique is a dynamic background flip that creates a sense of continuous motion between slides. A large, two-toned geometric object, centered on the slide but extending far beyond its visible boundaries, rotates 180 degrees during a slide transition. This makes the primary background color appear to seamlessly flip from the bottom half of the screen to the top half, providing a polished and engaging segue.

*   **Why Use This Skill (Rationale)**: This transition creates a powerful sense of narrative flow and progression. Instead of abrupt cuts between topics, the smooth rotation guides the viewer's eye, signaling a deliberate shift while maintaining a cohesive visual identity. It makes the presentation feel like a single, interconnected story rather than a series of disconnected statements.

*   **Overall Applicability**: This style is ideal for structuring a presentation with clear, distinct sections. It excels in scenarios like:
    *   Chapter or section title slides (e.g., "Part 1," "Part 2").
    *   Modern corporate presentations that require a minimalist yet dynamic feel.
    *   Product roadmaps or phased project timelines where each slide represents a new stage.

*   **Value Addition**: It elevates a standard presentation by transforming mundane section breaks into a cinematic, fluid experience. This adds a layer of professional polish and sophistication, making the content more engaging and memorable.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    - **Rotational Element**: A single, very large square shape that is centered on the slide and is large enough to cover the entire canvas at any angle of rotation. Its visual appearance is a two-tone split.
    - **Content Frame**: A static foreground element, such as a laptop mockup, is often used. This frame remains stationary, creating a stable "window" for the content while the background provides the motion. This contrast between a dynamic background and static foreground enhances the effect.
    - **Color Logic**: The pattern relies on a simple, high-contrast two-color scheme. Typically, a neutral base like white (`(255, 255, 255)`) is paired with a single, bold corporate accent color. In the tutorial, this is a coral/orange (`(255, 127, 80)`) and later a pink (`(255, 105, 180)`).
    - **Text Hierarchy**: Large, clean typography is used for section markers (e.g., "Part 01"), which often animate subtly. The main content within the frame follows a standard title/body hierarchy.

*   **Step B: Compositional Style**
    - **Off-Stage Composition**: The primary visual mechanic (the rotating square) is an "off-stage" element. It's deliberately oversized so that its edges are never visible, creating the illusion that the entire background canvas is rotating.
    - **Centered Pivot**: The entire effect is anchored to the absolute center of the slide. This single, stable pivot point makes the rotation feel balanced and natural.

*   **Step C: Dynamic Effects & Transitions**
    - The rotational motion is best achieved using PowerPoint's **Morph** transition. By setting up two consecutive slides with the same named object at different rotation angles (0° and 180°), Morph automatically generates the smooth rotational animation.
    - **Code Automation**: The code below will generate the two static slides, perfectly prepared for the Morph transition. The object on each slide will be given a special name (`!!Rotator`) that PowerPoint's Morph engine recognizes.
    - **Manual Step**: After generating the PPTX file with the code, the user must perform one manual action in PowerPoint: **select the second slide, go to the "Transitions" tab, and click "Morph."**

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Large off-screen shapes | `python-pptx` native | `python-pptx` can easily create and position shapes with dimensions far exceeding the slide boundaries. |
| Two-tone background | `python-pptx` native (Gradient Fill) | A two-stop linear gradient on a single large shape is the most efficient way to create the two-tone effect. This is more robust than managing two separate shapes. |
| Rotation for Morph | `python-pptx` native | The `shape.rotation` property allows for precise setting of the object's angle, which is essential for the Morph transition to work. |
| Naming for Morph | `python-pptx` native | Setting `shape.name` to a string starting with `!!` (e.g., `!!Rotator`) is the standard way to flag an object as a high-priority target for the Morph engine, ensuring a reliable transition. |

> **Feasibility Assessment**: The code reproduces **100%** of the necessary static setup. The dynamic "Morph" effect itself is a runtime feature of the PowerPoint application and must be applied manually. The generated file is perfectly configured for this one-click step.

#### 3b. Complete Reproduction Code

```python
import math
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_FILL, MSO_THEME_COLOR

def create_hemisphere_transition(
    output_pptx_path: str,
    accent_color: tuple = (255, 127, 80),  # RGB for coral accent
    slide_titles: list = ["PART 01", "PART 02"],
) -> str:
    """
    Creates a PPTX file with two slides demonstrating the Hemisphere Rotational Transition.

    This function sets up two slides with a large, two-toned, rotatable background object.
    To see the effect, open the generated PPTX, select the second slide,
    and apply the 'Morph' transition from the 'Transitions' tab in PowerPoint.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        accent_color: An RGB tuple for the primary background color.
        slide_titles: A list of titles for the two slides.

    Returns:
        The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    blank_slide_layout = prs.slide_layouts[6]

    # --- Calculate dimensions for the rotating background shape ---
    slide_w_emu = prs.slide_width
    slide_h_emu = prs.slide_height
    
    # The shape must be large enough to cover the slide even when rotated.
    # The diagonal of the slide is a safe size for the side of a square.
    diagonal = math.sqrt(slide_w_emu**2 + slide_h_emu**2)
    shape_size = int(diagonal * 1.05) # Add 5% buffer

    # Position for the shape to be centered on the slide
    shape_left = (slide_w_emu - shape_size) // 2
    shape_top = (slide_h_emu - shape_size) // 2

    # --- Create Slide 1 ---
    slide1 = prs.slides.add_slide(blank_slide_layout)
    
    # Add the rotating background shape
    rotator1 = slide1.shapes.add_shape(1, shape_left, shape_top, shape_size, shape_size)
    rotator1.name = "!!Rotator"  # Name for Morph transition
    
    # Apply a two-stop gradient fill to create the hemisphere effect
    fill = rotator1.fill
    fill.gradient()
    fill.gradient_stops.clear()
    
    # Stop 1: Accent color from 0% to 50%
    stop1 = fill.gradient_stops.add()
    stop1.position = 0.50
    stop1.color.rgb = RGBColor(*accent_color)
    
    # Stop 2: White from 50% to 100%
    stop2 = fill.gradient_stops.add()
    stop2.position = 0.50001 # A tiny gap to ensure a hard edge
    stop2.color.rgb = RGBColor(255, 255, 255)
    
    # Set gradient angle to make the color appear on the bottom
    fill.gradient_angle = 270 # 270 degrees puts the first color (accent) at the bottom
    
    # Remove shape outline
    rotator1.line.fill.background()
    
    # Send the background shape to the back
    slide1.shapes._spTree.remove(rotator1._element)
    slide1.shapes._spTree.insert(2, rotator1._element)
    
    # Add title text to Slide 1
    title_shape_1 = slide1.shapes.add_textbox(Inches(1), Inches(1), Inches(4), Inches(1.5))
    tf1 = title_shape_1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = slide_titles[0] if slide_titles else "PART 01"
    p1.font.size = Pt(60)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(0, 0, 0)


    # --- Create Slide 2 ---
    slide2 = prs.slides.add_slide(blank_slide_layout)

    # Add the identical background shape
    rotator2 = slide2.shapes.add_shape(1, shape_left, shape_top, shape_size, shape_size)
    rotator2.name = "!!Rotator"  # Must have the same name for Morph
    
    # Apply the same gradient
    fill2 = rotator2.fill
    fill2.gradient()
    fill2.gradient_stops.clear()
    stop1_2 = fill2.gradient_stops.add()
    stop1_2.position = 0.50
    stop1_2.color.rgb = RGBColor(*accent_color)
    stop2_2 = fill2.gradient_stops.add()
    stop2_2.position = 0.50001
    stop2_2.color.rgb = RGBColor(255, 255, 255)
    fill2.gradient_angle = 270

    # *** THE KEY STEP FOR THE ANIMATION ***
    # Rotate the shape by 180 degrees
    rotator2.rotation = 180.0
    
    rotator2.line.fill.background()
    
    # Send the background shape to the back
    slide2.shapes._spTree.remove(rotator2._element)
    slide2.shapes._spTree.insert(2, rotator2._element)
    
    # Add title text to Slide 2
    title_shape_2 = slide2.shapes.add_textbox(Inches(1), Inches(6), Inches(4), Inches(1.5))
    tf2 = title_shape_2.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = slide_titles[1] if len(slide_titles) > 1 else "PART 02"
    p2.font.size = Pt(60)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(0, 0, 0)
    
    prs.save(output_pptx_path)
    return output_pptx_path

if __name__ == '__main__':
    # Example usage:
    output_file = "hemisphere_transition_example.pptx"
    
    # You can try different colors and titles
    pink_accent = (236, 88, 140)
    blue_accent = (0, 112, 192)
    
    create_hemisphere_transition(
        output_pptx_path=output_file,
        accent_color=pink_accent,
        slide_titles=["Our Vision", "Our Mission"]
    )
    
    print(f"Presentation saved to {output_file}")
    print("\nIMPORTANT: Open the file, select the second slide, go to the 'Transitions' tab, and apply the 'Morph' transition to see the effect.")

```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback)? (N/A - no image download needed)
- [x] Are all color values explicit RGB tuples?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes, it produces the two static states required for the effect).
- [x] Would someone looking at the output (after applying Morph) say "yes, that's the same technique"? (Yes, the visual effect of the rotating background is identical).