### 1. High-level Skill Pattern Extraction

> **Skill Name**: Split-Panel KPI Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Sets up a dual-zone dashboard layout by disabling sheet gridlines and applying distinct column background fills. A narrow, dark-themed left sidebar acts as an anchor for primary KPI metrics in high-contrast, large typography, while a lighter main canvas houses detailed components like a conditionally-formatted heatmap matrix.
* **Applicability**: Use when building executive summaries or top-level dashboards that require a polished, modern application-like aesthetic without relying on external BI tools. Perfect for pairing 3-5 high-level metrics alongside detailed tables or charts.

### 2. Structural Breakdown

- **Data Layout**: The layout is split structurally using column widths. Columns A-C form the narrow sidebar (content centered in Col B). Columns D onwards serve as the main canvas, with a spacer column to breathe. 
- **Formula Logic**: Focuses on display rather than calculation. Applies specific Excel number formats (`#,##0`, `$#,##0`, `0.0%`) to ensure data readability.
- **Visual Design**: Disables gridlines completely. High contrast is achieved by filling the entire left panel with the theme's primary color. Uses cell borders sparingly (only thin borders around the matrix) to maintain a clean UI.
- **Charts/Tables**: Bypasses standard Excel charts for the detailed view by building a cell-based Heatmap Matrix, driven entirely by openpyxl's `ColorScaleRule` for a built-in interactive feel.
- **Theme Hooks**: Consumes `primary` for sidebar background and table headers, `bg` for the main canvas background, `text` for KPI labels, and `accent` for the maximum value in the heatmap color scale.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", kpis: list = None, heatmap_data: list = None, **kwargs) -> None:
    """
    Renders a split-panel dashboard layout featuring a dark KPI sidebar and a main canvas 
    with a conditionally formatted heatmap matrix.
    """
    # 1. Resolve Theme Palette
    palettes = {
        "corporate_blue": {"primary": "002060", "bg": "F0F4F8", "text": "FFFFFF", "text_dark": "1F2937", "accent": "0066CC"},
        "botanical_green": {"primary": "1B4332", "bg": "E8F5E9", "text": "FFFFFF", "text_dark": "081C15", "accent": "4CAF50"}
    }
    palette = palettes.get(theme, palettes["corporate_blue"])

    # 2. Setup Worksheet
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)

    ws.sheet_view.showGridLines = False

    # 3. Define Reusable Styles
    primary_fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    bg_fill = PatternFill(start_color=palette["bg"], end_color=palette["bg"], fill_type="solid")
    white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    
    kpi_lbl_font = Font(color=palette["text"], size=10)
    kpi_val_font = Font(color=palette["text"], size=18, bold=True)
    title_font = Font(color=palette["text_dark"], size=18, bold=True)
    header_font = Font(color=palette["text"], size=11, bold=True)
    row_lbl_font = Font(color=palette["text_dark"], size=11, bold=True)

    # 4. Color Zones & Column Widths
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 22
    ws.column_dimensions['C'].width = 3
    ws.column_dimensions['D'].width = 5  # Margin spacer
    ws.column_dimensions['E'].width = 16 # Main area first col

    for col in range(6, 12):
        ws.column_dimensions[get_column_letter(col)].width = 13

    for row in range(1, 41):
        for col in range(1, 4):  # Sidebar Zone
            ws.cell(row=row, column=col).fill = primary_fill
        for col in range(4, 20): # Main Canvas Zone
            ws.cell(row=row, column=col).fill = bg_fill

    # 5. Populate Sidebar KPIs
    if not kpis:
        kpis = [
            {"label": "Total Orders", "value": 2400, "fmt": "#,##0"},
            {"label": "Total Revenue", "value": 649019.80, "fmt": "$#,##0"},
            {"label": "Avg Rating", "value": 4.0, "fmt": "0.0"},
            {"label": "Avg Days to Ship", "value": 2.3, "fmt": "0.0"}
        ]

    # Dashboard Brand/Header in Sidebar
    brand_cell = ws.cell(row=3, column=2, value="EXECUTIVE VIEW")
    brand_cell.font = Font(color=palette["text"], size=16, bold=True)

    current_row = 6
    for kpi in kpis:
        lbl_cell = ws.cell(row=current_row, column=2, value=kpi["label"])
        lbl_cell.font = kpi_lbl_font
        
        val_cell = ws.cell(row=current_row + 1, column=2, value=kpi["value"])
        val_cell.font = kpi_val_font
        if "fmt" in kpi:
            val_cell.number_format = kpi["fmt"]
        current_row += 4

    # 6. Main Area Content (Title & Heatmap)
    ws.cell(row=3, column=5, value=title).font = title_font

    if not heatmap_data:
        heatmap_data = [
            ["Platform", "Female", "Male", "Other", "Unknown"],
            ["App", 0.189, 0.122, 0.011, 0.031],
            ["Instagram", 0.050, 0.043, 0.002, 0.018],
            ["Partner App", 0.063, 0.046, 0.002, 0.004],
            ["Target.com", 0.096, 0.068, 0.005, 0.013],
            ["Website", 0.125, 0.091, 0.006, 0.012]
        ]

    start_row_hm = 6
    start_col_hm = 5
    
    thin_border = Border(
        left=Side(style='thin', color="DDDDDD"), right=Side(style='thin', color="DDDDDD"),
        top=Side(style='thin', color="DDDDDD"), bottom=Side(style='thin', color="DDDDDD")
    )

    # Render Matrix
    for r_idx, row_data in enumerate(heatmap_data):
        for c_idx, val in enumerate(row_data):
            cell = ws.cell(row=start_row_hm + r_idx, column=start_col_hm + c_idx, value=val)
            cell.border = thin_border
            
            if r_idx == 0:  # Header Row
                cell.fill = primary_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                if c_idx == 0:  # Row Labels
                    cell.fill = white_fill
                    cell.font = row_lbl_font
                    cell.alignment = Alignment(horizontal="left", vertical="center")
                else:
                    cell.number_format = "0.0%"
                    cell.alignment = Alignment(horizontal="center", vertical="center")

    # 7. Apply Conditional Formatting (ColorScale) to Matrix Data
    end_row_hm = start_row_hm + len(heatmap_data) - 1
    end_col_hm = start_col_hm + len(heatmap_data[0]) - 1
    
    # Range covering only the numbers, skipping headers and row labels
    data_range_str = f"{get_column_letter(start_col_hm + 1)}{start_row_hm + 1}:{get_column_letter(end_col_hm)}{end_row_hm}"
    
    color_scale = ColorScaleRule(
        start_type="min", start_color="FFFFFF",
        end_type="max", end_color=palette["accent"]
    )
    ws.conditional_formatting.add(data_range_str, color_scale)
```