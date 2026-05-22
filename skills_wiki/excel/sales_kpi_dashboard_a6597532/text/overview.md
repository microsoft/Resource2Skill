### 1. High-level Skill Pattern Extraction

> **Skill Name**: Sales KPI Dashboard

* **Tier**: archetype
* **Core Mechanism**: Constructs a dashboard layout using full-row background fills to create a two-tone header and body. Simulates floating UI cards for KPIs using merged cell blocks with contrasting fills and accent borders. Organizes raw data on a hidden sheet, presenting only charts and metrics on the main dashboard sheet for a clean, application-like feel.
* **Applicability**: Best for executive summaries and high-level metric overviews where visual impact is prioritized. The two-tone layout and card-based KPIs provide a modern web-app aesthetic within Excel without relying on fragile floating shapes.

### 2. Structural Breakdown

- **Data Layout**: Places aggregated data/pivot output on a secondary "Analysis" sheet (hidden), reserving the "Dashboard" sheet strictly for presentation.
- **Formula Logic**: Uses literal values or dynamic links to the Analysis sheet for the KPI numbers.
- **Visual Design**: Hides gridlines. Rows 1-5 get a dark primary fill; Rows 6-40 get a soft background fill. Merged cell blocks act as cards (white fill, thick colored top border, thin gray side borders).
- **Charts/Tables**: Clean column chart anchored below the KPI cards, styled with Excel's built-in chart themes, referencing the hidden data sheet.
- **Theme Hooks**: Consumes `primary` (header), `bg_color` (lower background), `text_on_primary` (header text), `text_main` (KPI values), and `accent1` (card top borders/subtitle).

### 3. Reproduction Code

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, Reference

def render_workbook(wb: Workbook, *, title: str = "Sales Dashboard", subtitle: str = "Evaluating Agent Performance", theme: str = "purple_gold", **kwargs) -> None:
    themes = {
        "corporate_blue": {
            "primary": "1F4E78",
            "bg_color": "D9E1F2",
            "card_bg": "FFFFFF",
            "text_on_primary": "FFFFFF",
            "text_main": "000000",
            "accent1": "4472C4"
        },
        "purple_gold": {
            "primary": "5B3178", 
            "bg_color": "E6D9F2", 
            "card_bg": "FFFFFF",
            "text_on_primary": "FFFFFF",
            "text_main": "000000",
            "accent1": "E6B800"
        }
    }
    palette = themes.get(theme, themes["corporate_blue"])
    
    # 1. Setup Data Sheet (Hidden presentation layer)
    ws_data = wb.active
    ws_data.title = "Analysis"
    
    chart_data = [
        ["Month", "Reached", "Closed"],
        ["Jan", 301, 115], ["Feb", 311, 118], ["Mar", 300, 112],
        ["Apr", 298, 113], ["May", 307, 110], ["Jun", 305, 110],
        ["Jul", 293, 104], ["Aug", 301, 98],  ["Sep", 307, 100],
        ["Oct", 299, 107], ["Nov", 306, 108], ["Dec", 315, 120]
    ]
    for row in chart_data:
        ws_data.append(row)
    
    ws_data.sheet_state = 'hidden'
    
    # 2. Setup Dashboard Sheet
    ws_dash = wb.create_sheet("Dashboard", 0)
    ws_dash.sheet_view.showGridLines = False
    
    primary_fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    bg_fill = PatternFill(start_color=palette["bg_color"], end_color=palette["bg_color"], fill_type="solid")
    card_fill = PatternFill(start_color=palette["card_bg"], end_color=palette["card_bg"], fill_type="solid")
    
    # Apply two-tone background
    for row in range(1, 6):
        for col in range(1, 20):
            ws_dash.cell(row=row, column=col).fill = primary_fill
    for row in range(6, 40):
        for col in range(1, 20):
            ws_dash.cell(row=row, column=col).fill = bg_fill
            
    # Header Titles
    ws_dash["B2"] = title
    ws_dash["B2"].font = Font(name="Arial", size=24, bold=True, color=palette["text_on_primary"])
    ws_dash["B3"] = subtitle
    ws_dash["B3"].font = Font(name="Arial", size=14, italic=True, color=palette["accent1"])
    
    # KPI Cards (Mocked aggregated metrics)
    kpi_data = [
        {"title": "TOTAL CALLS", "value": "16,749"},
        {"title": "REACHED", "value": "3,328"},
        {"title": "DEALS CLOSED", "value": "1,203"},
        {"title": "DEAL VALUE", "value": "$646,979"}
    ]
    
    # (start_col, end_col) for each card, spanning 3 columns each
    card_anchors = [(3, 5), (7, 9), (11, 13), (15, 17)] 
    
    for idx, (sc, ec) in enumerate(card_anchors):
        # Merge cells for Value (rows 5-6) and Title (row 7)
        ws_dash.merge_cells(start_row=5, start_column=sc, end_row=6, end_column=ec)
        ws_dash.merge_cells(start_row=7, start_column=sc, end_row=7, end_column=ec)
        
        val_cell = ws_dash.cell(row=5, column=sc)
        val_cell.value = kpi_data[idx]["value"]
        val_cell.font = Font(name="Arial", size=20, bold=True, color=palette["text_main"])
        val_cell.alignment = Alignment(horizontal="center", vertical="center")
        
        title_cell = ws_dash.cell(row=7, column=sc)
        title_cell.value = kpi_data[idx]["title"]
        title_cell.font = Font(name="Arial", size=10, bold=True, color=palette["primary"])
        title_cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # Style the merged block to look like a floating web card
        for r in range(5, 8):
            for c in range(sc, ec + 1):
                cell = ws_dash.cell(row=r, column=c)
                cell.fill = card_fill
                
                # Apply borders cleanly to the outer edges only
                b_args = {}
                if r == 5: b_args['top'] = Side(style='thick', color=palette["accent1"])
                if r == 7: b_args['bottom'] = Side(style='thin', color="DDDDDD")
                if c == sc: b_args['left'] = Side(style='thin', color="DDDDDD")
                if c == ec: b_args['right'] = Side(style='thin', color="DDDDDD")
                cell.border = Border(**b_args)

    # Adjust spacing columns for better gutter layout
    for col_letter in ["A", "B", "F", "J", "N"]:
        ws_dash.column_dimensions[col_letter].width = 4

    # 3. Add Main Chart below the KPI cards
    chart = BarChart()
    chart.title = "Reached vs Closed by Month"
    chart.style = 11 # Clean default bar chart style
    chart.height = 12
    chart.width = 22
    
    data = Reference(ws_data, min_col=2, min_row=1, max_col=3, max_row=13)
    cats = Reference(ws_data, min_col=1, min_row=2, max_row=13)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    
    ws_dash.add_chart(chart, "C10")
```