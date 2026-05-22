# Executive Structured Infographic Slide (結構化高階主管摘要卡片排版)

## Analysis

這段影片雖然主要是在評測不同的 AI 簡報工具（Gamma, Felo, Skywork 等），但其核心其實是在傳授**「高效率、及格線以上的商業簡報資訊架構學」**。影片中明確提出了兩大黃金準則：**「一頁只講一個核心重點」**與**「以資訊圖表代替文字」**。

我們將把影片中 AI 工具生成的最佳排版（如 Felo 或 Gamma 產出的乾淨圖文排版），萃取成一個可由 Python 重現的設計模式：**「高對比結構化圖表卡片排版」**。

---

### 1. High-level Design Pattern Extraction

> **Skill Name**: Executive Structured Infographic Slide (結構化高階主管摘要卡片排版)

*   **Core Visual Mechanism**:
    這是一種高度模組化的資訊架構視覺風格。頂部保留完整的「結論導向」（1個標題 + 1句完整結論）。下方空間嚴格按比例切割：左側配置數據視覺化（如甜甜圈圖）或抽象概念圖，右側則以「卡片化」或「帶有引導線的獨立文字塊」來呈現 3 個關鍵支持要點。摒棄傳統的深層次條列式清單（Bullet points）。
*   **Why Use This Skill (Rationale)**:
    如同影片中強調的，聽眾的大腦沒有多餘的精力去閱讀「文字海」。這種排版利用視覺動線（Z字型或F字型），先讓觀眾看到結論（Top），接著視線被左側圖表吸引（Left），最後利用右側整理好的重點區塊（Right）作為補充說明，極大化降低認知負擔。
*   **Overall Applicability**:
    極度適合商業分析報告、市場現況概覽（如影片中的電動車市場分析）、產品競品分析、以及任何需要向高階主管快速匯報的「一頁紙提案」。
*   **Value Addition**:
    將冗長、毫無頭緒的長篇大論，瞬間轉化為具有專業顧問級別（Consulting-style）的簡報頁面，兼具邏輯說服力與視覺吸引力。

---

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    *   **Typography**: 頂部標題（大字重，通常為無襯線體），副標題/核心結論（中字重，對比色或反白背景），右側內文（常規字重，行距 1.2-1.5）。
    *   **Color Logic**: 採用經典商業配色（Corporate Trust Palette）。
        *   背景色：極簡灰白 `(248, 249, 250, 255)` 或純白。
        *   主色調（標題與圖表強調色）：深海藍 `(23, 43, 77, 255)`。
        *   輔助色（結論高光區或圖表次要色）：科技青 `(0, 191, 255, 255)` 或薄荷綠 `(54, 179, 126, 255)`。
        *   內文色：深石板灰 `(94, 108, 132, 255)`。
    *   **Shapes**: 帶有微小圓角（Radius）的矩形卡片背景，左側裝飾性的細線或色塊（Accent lines）用來區分重點層級。

*   **Step B: Compositional Style**
    *   **頂部 (Top 20-25%)**: 標題與一句話總結。
    *   **左半部 (Bottom Left 40%)**: 放置視覺化圖表（Chart / SVG InfoGraphic）。
    *   **右半部 (Bottom Right 60%)**: 均勻分佈 3 個重點區塊。每個區塊帶有微灰色的背景框，營造空間層次感。

*   **Step C: Dynamic Effects & Transitions**
    *   排版已具備極高的靜態張力。若在 PowerPoint 中，適合加上原生「轉化 (Morph)」或群組元素的「淡出 (Fade)」進入動畫。

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
| :--- | :--- | :--- |
| **結構化排版與文字階層** | `python-pptx` native | 可以精確控制 TextBox 位置、字型大小、顏色與卡片背景形狀，完全符合影片中排版的嚴謹度。 |
| **資訊視覺化（數據圖表）** | `python-pptx` native charts | 影片強調用圖表取代文字。原生 API 支援生成具備互動數據屬性的圓環圖（Doughnut Chart），比起插入死圖表更加專業。 |
| **重點卡片區塊背景** | `python-pptx` native shapes | 使用帶有透明度填充的圓角矩形，在右側建立「卡片化」重點清單，模仿 Gamma / Felo 的現代化 UI 感。 |

> **Feasibility Assessment**: 95%. 原生 `python-pptx` 足以完美重現影片中強調的「1標題 + 1結論 + 數據圖表 + 重點卡片」的標準專業顧問式排版。唯一缺乏的是 Gamma 中部分特殊的網頁級陰影渲染，但透過調整形狀無邊框與淡色填充，視覺效果幾乎一致。

#### 3b. Complete Reproduction Code

以下程式碼將生成一張以「電動車市場分析」為例（呼應影片內容）的高階主管視覺化摘要簡報。

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION

def create_slide(
    output_pptx_path: str,
    title_text: str = "品牌格局：特斯拉領先，本土品牌崛起",
    core_message: str = "2024年台灣電動車市場持續成長，除了特斯拉佔據首位，本土品牌如Luxgen憑藉高性價比快速崛起。",
    chart_data_dict: dict = {"Tesla": 40.0, "Luxgen": 18.7, "BMW": 16.7, "Mercedes": 7.8, "Kia": 3.6, "Others": 13.2},
    key_points: list = None,
    primary_color: tuple = (23, 43, 77),   # Deep Navy
    accent_color: tuple = (0, 191, 255),   # Tech Blue
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Executive Structured Infographic Slide" pattern.
    """
    if key_points is None:
        key_points = [
            ("特斯拉(Tesla)持續主導", "以明顯優勢穩坐市佔率龍頭，強大充電網路與品牌力依然是消費者首選。"),
            ("納智捷(Luxgen)突圍", "主打平價親民路線，n7車型成功切入大眾市場，成為第二大品牌。"),
            ("豪華車廠佈局深化", "BMW與Mercedes等傳統豪華車廠積極導入多元純電車款，穩固高階市場。")
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Background color (very light gray for modern UI feel)
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(248, 249, 250)

    # ==========================================
    # Layer 1: Header (Title & Core Message)
    # ==========================================
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(36)
    p.font.color.rgb = RGBColor(*primary_color)
    p.font.name = "Arial"

    # Core Message Background Ribbon
    msg_bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.3), Inches(11.7), Inches(0.8))
    msg_bg.fill.solid()
    msg_bg.fill.fore_color.rgb = RGBColor(235, 244, 255) # Light blue accent bg
    msg_bg.line.fill.background() # No border
    
    # Left vertical accent line for Core Message
    accent_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.3), Inches(0.1), Inches(0.8))
    accent_line.fill.solid()
    accent_line.fill.fore_color.rgb = RGBColor(*accent_color)
    accent_line.line.fill.background()

    # Core Message Text
    msg_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.35), Inches(11.3), Inches(0.7))
    tf_msg = msg_box.text_frame
    tf_msg.word_wrap = True
    p_msg = tf_msg.paragraphs[0]
    p_msg.text = core_message
    p_msg.font.size = Pt(20)
    p_msg.font.bold = True
    p_msg.font.color.rgb = RGBColor(40, 50, 70)
    p_msg.font.name = "Arial"

    # ==========================================
    # Layer 2: Left Side - Data Visualization (Doughnut Chart)
    # ==========================================
    chart_data = CategoryChartData()
    chart_data.categories = list(chart_data_dict.keys())
    chart_data.add_series('Market Share', list(chart_data_dict.values()))

    x, y, cx, cy = Inches(0.8), Inches(2.5), Inches(5.5), Inches(4.5)
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.DOUGHNUT, x, y, cx, cy, chart_data
    ).chart

    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.BOTTOM
    chart.legend.font.size = Pt(14)
    chart.plots[0].has_data_labels = True
    data_labels = chart.plots[0].data_labels
    data_labels.font.size = Pt(12)
    data_labels.font.color.rgb = RGBColor(255, 255, 255)
    data_labels.number_format = '0.0%'

    # Custom colors for chart series (to match modern palette)
    colors = [
        RGBColor(*primary_color),      # Navy
        RGBColor(*accent_color),       # Blue
        RGBColor(54, 179, 126),        # Mint Green
        RGBColor(255, 171, 0),         # Yellow Orange
        RGBColor(101, 84, 192),        # Purple
        RGBColor(137, 147, 164)        # Gray
    ]
    for i, point in enumerate(chart.plots[0].series[0].points):
        fill = point.format.fill
        fill.solid()
        fill.fore_color.rgb = colors[i % len(colors)]

    # ==========================================
    # Layer 3: Right Side - Key Points (Card UI)
    # ==========================================
    start_x = Inches(6.8)
    start_y = Inches(2.5)
    card_width = Inches(5.7)
    card_height = Inches(1.3)
    spacing = Inches(0.2)

    for i, (kp_title, kp_desc) in enumerate(key_points):
        current_y = start_y + i * (card_height + spacing)

        # Card Background
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x, current_y, card_width, card_height)
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(255, 255, 255)
        card.line.color.rgb = RGBColor(223, 225, 230) # Subtle border
        card.line.width = Pt(1)

        # Card Accent Dot (Visual bullet point)
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, start_x + Inches(0.3), current_y + Inches(0.25), Inches(0.15), Inches(0.15))
        dot.fill.solid()
        dot.fill.fore_color.rgb = RGBColor(*accent_color) if i == 0 else RGBColor(*primary_color)
        dot.line.fill.background()

        # Key Point Title
        kp_title_box = slide.shapes.add_textbox(start_x + Inches(0.5), current_y + Inches(0.1), card_width - Inches(0.6), Inches(0.4))
        tf_kp_title = kp_title_box.text_frame
        p_kp_title = tf_kp_title.paragraphs[0]
        p_kp_title.text = kp_title
        p_kp_title.font.bold = True
        p_kp_title.font.size = Pt(18)
        p_kp_title.font.color.rgb = RGBColor(*primary_color)

        # Key Point Description
        kp_desc_box = slide.shapes.add_textbox(start_x + Inches(0.5), current_y + Inches(0.5), card_width - Inches(0.6), Inches(0.7))
        tf_kp_desc = kp_desc_box.text_frame
        tf_kp_desc.word_wrap = True
        p_kp_desc = tf_kp_desc.paragraphs[0]
        p_kp_desc.text = kp_desc
        p_kp_desc.font.size = Pt(14)
        p_kp_desc.font.color.rgb = RGBColor(94, 108, 132) # Secondary text color

    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("ai_structured_report.pptx")
```