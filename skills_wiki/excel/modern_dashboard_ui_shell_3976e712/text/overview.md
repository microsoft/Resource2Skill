### 1. High-level Skill Pattern Extraction

> **Skill Name**: Modern Dashboard UI Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Disables native gridlines and uses contrasting background fills to create a web-like application canvas. Employs a dark-filled left column as a navigation sidebar and white-filled cell ranges with precise borders to create discrete "cards" for hosting KPIs and charts.
* **Applicability**: Use as the foundational layout for executive dashboards and summary reports to elevate the aesthetic from a standard spreadsheet to a structured, modern interface.

### 2. Structural Breakdown

- **Data Layout**: Establishes a visual grid by standardizing column widths, acting as a flex-box-like grid for placing modular components.
- **Formula Logic**: Uses intra-workbook hyperlinks on sidebar icons to simulate web navigation between different report views.
- **Visual Design**: High contrast sidebar (`#0F172A`), soft background (`#F8FAFC`), and stark white cards with subtle borders (`#E2E8F0`) to create visual depth and hierarchy.
- **Charts/Tables**: Creates pre-sized, bordered card containers (with merged header rows) ready to seamlessly host `openpyxl` Chart objects.
- **Theme Hooks**: Consumes `sidebar_bg`, `bg`, `card_bg`, `border`, and `text_primary` to allow for easy branding or dark-mode toggling.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # Theme fallbacks
    colors = {
        "sidebar_bg": "0F172A", # Slate 900
        "sidebar_fg": "FFFFFF",
        "bg": "F8FAFC",         # Slate 50
        "card_bg": "FFFFFF",
        "border": "E2E8F0",     # Slate 200
        "text_primary": "0F172A",
        "text_secondary": "64748B"
    }

    ws = wb.create_sheet(sheet_name)
    
    # 1. Base Setup: Hide gridlines to break out of the "spreadsheet" look
    ws.sheet_view.showGridLines = False
    
    # Fill background
    bg_fill = PatternFill(start_color=colors["bg"], end_color=colors["bg"], fill_type="solid")
    for row in ws.iter_rows(min_row=1, max_row=30, min_col=1, max_col=20):
        for cell in row:
            cell.fill = bg_fill
            
    # Resize columns for grid system
    for col in range(2, 21):
        ws.column_dimensions[get_column_letter(col)].width = 8

    # 2. Sidebar Navigation
    sidebar_fill = PatternFill(start_color=colors["sidebar_bg"], end_color=colors["sidebar_bg"], fill_type="solid")
    ws.column_dimensions['A'].width = 8
    for row in range(1, 31):
        ws.cell(row=row, column=1).fill = sidebar_fill
        
    sidebar_font = Font(color=colors["sidebar_fg"], size=16, bold=True)
    sidebar_items = [
        (4, "🏠"),  # Home
        (6, "📊"),  # Dashboard
        (8, "✉️"),  # Mail
        (10, "❓")  # Support
    ]
    
    for r, icon in sidebar_items:
        c = ws.cell(row=r, column=1, value=icon)
        c.font = sidebar_font
        c.alignment = Alignment(horizontal="center", vertical="center")
        # Link to self for demonstration; usually links to other sheets
        c.hyperlink = f"#'{sheet_name}'!A1" 
        
    # 3. Dashboard Title
    title_cell = ws.cell(row=2, column=3, value=title)
    title_cell.font = Font(size=24, bold=True, color=colors["text_primary"])
    subtitle_cell = ws.cell(row=3, column=3, value="Figures in millions of USD")
    subtitle_cell.font = Font(size=11, italic=True, color=colors["text_secondary"])

    # 4. Card Drawing Helper
    def draw_card(min_col, min_row, max_col, max_row, card_title):
        card_fill = PatternFill(start_color=colors["card_bg"], end_color=colors["card_bg"], fill_type="solid")
        
        # Apply fill and outer borders
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = card_fill
                
                b_left = Side(style='thin', color=colors["border"]) if c == min_col else None
                b_right = Side(style='thin', color=colors["border"]) if c == max_col else None
                b_top = Side(style='thin', color=colors["border"]) if r == min_row else None
                b_bottom = Side(style='thin', color=colors["border"]) if r == max_row else None
                cell.border = Border(left=b_left, right=b_right, top=b_top, bottom=b_bottom)
                
        # Card Header (Merge across the top row of the card)
        ws.merge_cells(start_row=min_row, start_column=min_col, end_row=min_row, end_column=max_col)
        tc = ws.cell(row=min_row, column=min_col, value=card_title)
        tc.font = Font(bold=True, color=colors["text_primary"], size=12)
        tc.alignment = Alignment(vertical="center", indent=1)
        ws.row_dimensions[min_row].height = 30

    # 5. Render KPI Cards
    # Sales Card
    draw_card(3, 5, 6, 8, "Sales")
    ws.merge_cells(start_row=6, start_column=3, end_row=7, end_column=6)
    c1 = ws.cell(row=6, column=3, value=2544)
    c1.font = Font(size=24, bold=True, color=colors["text_primary"])
    c1.number_format = '"$"#,##0'
    c1.alignment = Alignment(horizontal="center", vertical="center")
    
    # Profit Card
    draw_card(8, 5, 11, 8, "Profit")
    ws.merge_cells(start_row=6, start_column=8, end_row=7, end_column=11)
    c2 = ws.cell(row=6, column=8, value=890)
    c2.font = Font(size=24, bold=True, color=colors["text_primary"])
    c2.number_format = '"$"#,##0'
    c2.alignment = Alignment(horizontal="center", vertical="center")
    
    # Customers Card
    draw_card(13, 5, 16, 8, "# of Customers")
    ws.merge_cells(start_row=6, start_column=13, end_row=7, end_column=16)
    c3 = ws.cell(row=6, column=13, value=87.0)
    c3.font = Font(size=24, bold=True, color=colors["text_primary"])
    c3.number_format = '0.0'
    c3.alignment = Alignment(horizontal="center", vertical="center")
    
    # 6. Render Chart Cards (Placeholders ready for openpyxl Charts)
    draw_card(3, 10, 11, 24, "2021-2022 Sales Trend")
    draw_card(13, 10, 19, 24, "Customer Satisfaction")
```