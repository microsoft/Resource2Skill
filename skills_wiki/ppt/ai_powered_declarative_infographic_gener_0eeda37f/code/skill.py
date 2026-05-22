import os
from typing import Dict, Any

def create_infographic_html(
    infographic_spec: str,
    output_html_path: str = "infographic.html",
    theme: str = "light",
    bg_color: str = "#FFFFFF"
) -> str:
    """
    Generates a self-contained HTML file to render an infographic using the AntV Infographic library.

    Args:
        infographic_spec (str): The declarative code string defining the infographic.
        output_html_path (str): The path to save the generated HTML file.
        theme (str): The visual theme to apply. Can be 'light', 'dark', or 'sketch'.
        bg_color (str): The background color of the HTML page (e.g., '#0A0A0A' for dark theme).

    Returns:
        str: The absolute path to the saved HTML file.
    
    How to Use the Output:
    1. Open the generated .html file in a web browser (Chrome, Firefox, etc.).
    2. The infographic will be rendered on the page.
    3. To save, you can:
       - Right-click the graphic -> "Save Image As..." to get an SVG file.
       - Use a screenshot tool or browser extension to capture it as a high-resolution PNG.
    4. Insert the saved SVG or PNG file into your PowerPoint presentation.
    """

    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AntV Infographic</title>
    <style>
        body {{
            background-color: {bg_color};
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
        }}
        #container {{
            width: 90%;
            height: 90%;
        }}
    </style>
</head>
<body>
    <div id="container"></div>
    <script src="https://unpkg.com/@antv/infographic@latest/dist/infographic.min.js"></script>
    <script>
        const {{ Infographic }} = window.Infographic;

        const infographic = new Infographic({{
            container: document.getElementById('container'),
            width: 1200,
            height: 800,
            theme: '{theme}',
            // Set editable to false for static viewing
            editable: false, 
        }});

        const infographicSyntax = `{infographic_spec}`;

        infographic.render(infographicSyntax);
    </script>
</body>
</html>
"""
    
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
        
    print(f"Infographic HTML generated successfully. Please open this file in a browser: {os.path.abspath(output_html_path)}")
    return os.path.abspath(output_html_path)

# --- Example Usage ---

# Example 1: Recreating the Hacker-style "2025 LLM Review" from the video
hacker_llm_spec = """
chart-wordcloud
data
    items
        - label: 强化学习
          value: 120
        - label: Midjourney
          value: 100
        - label: Transformer
          value: 150
        - label: 卷积神经网络
          value: 80
        - label: OpenAI
          value: 200
        - label: Copilot
          value: 110
        - label: 自动驾驶
          value: 70
        - label: Agent
          value: 160
        - label: 生成式AI
          value: 180
        - label: 数据标注
          value: 60
        - label: 深度学习
          value: 170
        - label: 多模态
          value: 90
        - label: Claude
          value: 130
        - label: GPT-4
          value: 190
        - label: 机器学习
          value: 175
        - label: Sora
          value: 125
        - label: Stable Diffusion
          value: 140
        - label: 自然语言处理
          value: 165
        - label: Prompt
          value: 105
        - label: RAG
          value: 115
        - label: Gemini
          value: 135
        - label: 神经网络
          value: 155
        - label: 大语言模型
          value: 210
        - label: ChatGPT
          value: 220
        - label: AIGC
          value: 185
theme
    palette: ["#8aff8a", "#00ff00", "#50c878", "#a2ffbd", "#ffffff"]
"""

# Example 2: A simple pyramid chart with a sketch/hand-drawn style
pyramid_sketch_spec = """
sequence-pyramid-simple
data
    title: 金字塔原理
    desc: 结论先行、以上统下、归类分组、逻辑递进
    items
        - label: 核心结论
          desc: 先说结论，开门见山
          icon: mdi/lightbulb-on-outline
        - label: 关键论据
          desc: 用关键论点支撑结论
          icon: mdi/key-variant
        - label: 支撑信息
          desc: 通过分类归纳组织信息
          icon: mdi/information-outline
        - label: 事实数据
          desc: 用事实和数据作为论证基础
          icon: mdi/database
"""

if __name__ == '__main__':
    # Generate the hacker-style word cloud
    create_infographic_html(
        infographic_spec=hacker_llm_spec,
        output_html_path="llm_review_dark.html",
        theme="dark",
        bg_color="#0A0A0A"
    )

    # Generate the sketch-style pyramid
    create_infographic_html(
        infographic_spec=pyramid_sketch_spec,
        output_html_path="pyramid_sketch.html",
        theme="sketch",
        bg_color="#F5F5DC" # A beige background for the sketch theme
    )

