# AI-Assisted Diagramming with Mermaid

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: AI-Assisted Diagramming with Mermaid

*   **Core Visual Mechanism**: This skill leverages **"Diagrams as Code"** using the Mermaid syntax. Instead of manually drawing shapes, you write a simple, text-based definition of the diagram's structure and content. An external renderer (like the Mermaid CLI or a web-based editor) converts this text into a clean, structured visual diagram (flowchart, Gantt chart, pie chart, etc.), which is then inserted as an image onto the slide. The aesthetic is typically clean, minimalist, and highly readable, defined by the Mermaid theme.

*   **Why Use This Skill (Rationale)**:
    *   **Efficiency & Speed**: Writing a few lines of text is significantly faster than manually drawing, aligning, and connecting shapes.
    *   **Editability**: Modifying the diagram is as simple as changing a line of text. Adding, removing, or reordering steps is trivial.
    *   **AI Synergy**: This text-based format is ideal for AI generation. You can describe a complex process in natural language and ask an AI to generate the precise Mermaid code, achieving a massive productivity boost.
    *   **Consistency & Standardization**: All diagrams share a consistent visual style, ensuring a professional and uniform look across a presentation.
    *   **Version Control**: Because the diagrams are just text, they can be stored, diffed, and managed in version control systems like Git.

*   **Overall Applicability**: This skill is a game-changer for any presentation that requires structured diagrams.
    *   **Technical & Business**: Explaining software architecture, business processes, user flows, and organizational charts.
    *   **Project Management**: Creating project timelines, Gantt charts, and dependency maps.
    *   **Conceptual**: Building mind maps and state diagrams to organize ideas.
    *   **Data Visualization**: Quickly generating simple pie charts and other data-driven visuals.

*   **Value Addition**: It transforms diagramming from a tedious, time-consuming design task into a quick, automatable content task. It allows the presenter to focus on the *logic* of the diagram, not the manual labor of drawing it, while producing clean, professional results.

### 2. Visual Breakdown

The visual style is not created in PowerPoint but is an imported asset. The breakdown describes the Mermaid syntax that generates the visual elements.

*   **Step A: Core Visual Elements (Mermaid Syntax)**
    *   **Diagram Type Declaration**: The first line defines the chart type (e.g., `flowchart TD`, `gantt`, `pie`).
    *   **Nodes**: Textual representations of shapes. The syntax defines both the shape and its content.
        *   `ID[Text]` -> Rectangle (e.g., `A[Start]`)
        *   `ID{Text}` -> Diamond / Decision (e.g., `B{Is it ready?}`)
        *   `ID(Text)` -> Rounded Rectangle
    *   **Links**: Symbols that define connections between nodes.
        *   `-->` -> Line with an arrowhead
        *   `---` -> Simple line
        *   `-.->` -> Dotted line with an arrowhead
    *   **Labels & Values**: Key-value pairs define data, such as categories and numbers for a pie chart (`"Apples" : 45`) or tasks and durations for a Gantt chart.
    *   **Color Logic**: Mermaid uses pre-defined themes (e.g., default, dark, neutral). The visuals are consistent within a theme. The default theme uses a white background, black text, and light purple/gray fills for shapes.

*   **Step B: Compositional Style**
    *   The layout is algorithmically determined by Mermaid based on the diagram type and direction (`TD` for Top-to-Down, `LR` for Left-to-Right). This ensures optimal spacing and alignment automatically. The user cedes manual layout control in exchange for speed and consistency. The final diagram is inserted as a single, centered image onto the slide.

*   **Step C: Dynamic Effects & Transitions**
    *   Since the diagram is a static image, it has no internal animations. Standard PowerPoint entrance/exit animations (e.g., "Fade," "Wipe") can be applied to the image as a whole.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Mermaid Code Rendering | Mermaid CLI (`mmdc`) via `subprocess` | This is the official, headless method for converting Mermaid text to high-quality PNG or SVG images without needing a browser. It offers the most reliable and direct path for programmatic rendering. |
| PPTX Generation & Image Insertion | `python-pptx` | The standard and most robust library for creating PowerPoint presentations, adding slides, and placing images. |
| Dependency Management | `shutil.which` and clear error handling | The code explicitly checks if the `mmdc` command-line tool is installed, providing clear instructions to the user if it's missing. This makes the skill robust. |

> **Feasibility Assessment**: **100%**. The code fully reproduces the core workflow taught in the tutorial: taking Mermaid text as input and producing a PowerPoint slide with the rendered diagram. It faithfully replicates the visual style of Mermaid-generated charts.

#### 3b. Complete Reproduction Code

```python
import subprocess
import tempfile
import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from PIL import Image

def create_slide(
    output_pptx_path: str,
    mermaid_definitions: dict = None,
    **kwargs,
) -> str:
    """
    Creates a PPTX file with slides containing diagrams rendered from Mermaid code.
    
    This function requires the Mermaid CLI (mmdc) to be installed and in the system's PATH.
    Install it via npm: `npm install -g @mermaid-js/mermaid-cli`

    Args:
        output_pptx_path (str): The path to save the generated .pptx file.
        mermaid_definitions (dict): A dictionary where keys are slide titles (str) 
                                    and values are Mermaid code blocks (str).

    Returns:
        str: The path to the saved PPTX file.
    """
    # --- Dependency Check ---
    if not shutil.which("mmdc"):
        raise EnvironmentError(
            "Mermaid CLI (mmdc) not found in your system's PATH. "
            "This skill requires it to render diagrams. \n"
            "Please install it globally by running: 'npm install -g @mermaid-js/mermaid-cli'"
        )

    # --- Default example if no definitions are provided ---
    if mermaid_definitions is None:
        mermaid_definitions = {
            "Example Flowchart": """
            flowchart TD
                A[Start] --> B{Decision};
                B -- Yes --> C[Process 1];
                B -- No --> D[Process 2];
                C --> E[End];
                D --> E[End];
            """,
            "Example Gantt Chart": """
            gantt
                title Project Development Timeline
                dateFormat YYYY-MM-DD
                section Planning Phase
                Market Research :done, 2024-09-01, 7d
                Initial Design :active, 2024-09-08, 5d
                section Development Phase
                Core Feature Dev : 2024-09-15, 15d
                Testing & QA : 2024-10-01, 10d
            """,
            "Example Pie Chart": """
            pie
                title Market Share
                "Apple" : 45
                "Samsung" : 25
                "Huawei" : 15
                "Other" : 15
            """
        }

    # --- Presentation Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    # --- Process Each Diagram ---
    for title, code in mermaid_definitions.items():
        slide = prs.slides.add_slide(blank_slide_layout)
        
        # Add a title to the slide
        title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), prs.slide_width - Inches(1), Inches(0.75))
        tf = title_shape.text_frame
        tf.text = title
        p = tf.paragraphs[0]
        p.font.size = Pt(32)
        p.font.bold = True

        # Use temporary files for processing
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.mmd', encoding='utf-8') as mmd_file:
            mmd_file.write(code)
            mmd_file_path = mmd_file.name
        
        png_file_path = mmd_file_path.replace('.mmd', '.png')

        try:
            # Run the Mermaid CLI to convert the .mmd file to a .png image
            # The -b transparent flag makes the image background transparent for better integration
            subprocess.run(
                ["mmdc", "-i", mmd_file_path, "-o", png_file_path, "-b", "transparent"],
                check=True,
                capture_output=True, # Use capture_output to hide stdout/stderr unless there's an error
                text=True,
            )

            # Add the generated image to the slide, centered
            with Image.open(png_file_path) as img:
                img_width, img_height = img.size

            # Scale image to fit slide while maintaining aspect ratio
            max_width = prs.slide_width - Inches(1)
            max_height = prs.slide_height - Inches(1.5)
            
            ratio = min(max_width / img_width, max_height / img_height)
            
            display_width = int(img_width * ratio)
            display_height = int(img_height * ratio)

            left = int((prs.slide_width - display_width) / 2)
            top = Inches(1.0) # Place below the title

            slide.shapes.add_picture(png_file_path, left, top, width=display_width, height=display_height)

        except subprocess.CalledProcessError as e:
            error_message = f"Error rendering Mermaid diagram '{title}'.\nmmdc stderr: {e.stderr}"
            print(error_message)
            # Add an error message to the slide for user feedback
            err_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(11), Inches(4))
            err_box.text_frame.text = error_message
            
        finally:
            # Clean up the temporary files
            if os.path.exists(mmd_file_path):
                os.remove(mmd_file_path)
            if os.path.exists(png_file_path):
                os.remove(png_file_path)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example of how to call the function:
# if __name__ == '__main__':
#     # The function uses default examples if mermaid_definitions is not provided.
#     # You can provide your own dictionary of diagrams.
#     my_diagrams = {
#         "Morning Routine": """
#         graph TD
#             A(Start) --> B(Alarm rings);
#             B --> C{Ready to wake up?};
#             C -- No --> D(Snooze - 5 minutes);
#             D --> B;
#             C -- Yes --> E(Get out of bed);
#             E --> F(End);
#         """
#     }
#     create_slide(output_pptx_path="my_mermaid_presentation.pptx", mermaid_definitions=my_diagrams)
#     print("Presentation saved to my_mermaid_presentation.pptx")
```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback)? (N/A, renders locally)
- [x] Are all color values explicit RGBA tuples (not referencing undefined variables)? (N/A, Mermaid handles colors)
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?
- [x] Would someone looking at the output say "yes, that's the same technique"?