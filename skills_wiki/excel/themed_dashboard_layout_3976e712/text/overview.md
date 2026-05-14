### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Dashboard Layout

*   **Tier**: sheet_shell
*   **Core Mechanism**: This skill constructs a complete dashboard layout on a single worksheet using merged and styled cell ranges to define distinct visual containers for titles, key performance indicators (KPIs), and various charts. It incorporates dynamic navigation elements (hyperlinked text placeholders) in a dedicated sidebar and provides mock data for KPIs to illustrate functionality, all styled consistently with a defined theme palette.
*   **Applicability**: Use this for rapidly generating structured executive dashboards, performance summaries, or single-page reports requiring a clear, segmented, and aesthetically pleasing grid-based layout for displaying multiple metrics, trends, and visualizations. It's ideal when a consistent brand or reporting theme is desired across multiple dashboard elements.

### 2. Structural Breakdown

-   **Data Layout**:
    *   The dashboard itself uses merged cells for layout areas rather than direct data input.
    *   Column A serves as a vertical navigation bar.
    *   Cells B2:M4 are merged for the main dashboard title and subtitle.
    *   Three sets of merged cells (e.g., B6:E10, F6:I10, J6:M10) define KPI boxes.
    *   Two larger merged cell areas (e.g., B12:I22 and J12:M22) are placeholders for charts.
    *   A final vertical merged cell area (e.g., N2:Q22) serves as a placeholder for a map chart.
-   **Formula Logic**:
    *   **Hyperlinks for Navigation**: Cells in Column A are linked to other sheets or external email addresses using `=HYPERLINK("#<SheetName>!A1", "")` or `=HYPERLINK("mailto:<email_address>", "")`.
    *   **Dynamic KPI Values**: In the actual Excel dashboard (not fully reproducible in pure `openpyxl` code for linked textboxes), numbers like sales figures and percentages would be displayed in dynamic textboxes linked to specific cells in the "Inputs" sheet (e.g., `='Inputs'!D5`). The provided code simulates these with static text.
-   **Visual Design**:
    *   **Background**: Main worksheet background is implicitly white, as content boxes are white.
    *   **Navigation Bar (Column A)**: Filled with `header_bg` (dark blue). Icons are simulated with text placeholders, `text_light` (white) font, and centered alignment, each hyperlinked.
    *   **Layout Boxes (Titles, KPIs, Charts)**: Simulated using merged cell ranges.
        *   **Fill**: `content_bg` (white).
        *   **Border**: Thin `shadow_color` (light grey) border to approximate the look of distinct shapes and their shadows.
    *   **Text (Main Title)**: `title` parameter, `Calibri`, 20pt, `bold`, `accent_primary` (dark blue) color, left-aligned with indent.
    *   **Text (Subtitle)**: "Figures in millions of USD", `Calibri`, 10pt, `text_grey` color, left-aligned with indent.
    *   **Text (Section Titles within boxes)**: `Calibri`, 12pt, `bold`, `accent_primary` color, left-aligned with indent.
    *   **Text (KPI Values/Percentages within boxes)**: `Calibri`, 16pt (values) / 14pt (percentages), `bold`, `accent_primary` color, centered alignment.
-   **Charts/Tables**:
    *   The skill defines structured areas/placeholders for various chart types (e.g., donut, line, radar, map). The actual charts would be inserted into these areas in a subsequent step or as separate component skills. The code places descriptive text as a placeholder within these areas.
-   **Theme Hooks**:
    *   `header_bg`: Background color for the navigation sidebar.
    *   `content_bg`: Background color for layout boxes and overall sheet.
    *   `accent_primary`: Main text color for titles and KPI values.
    *   `text_light`: Text color for navigation icons.
    *   `text_grey`: Text color for subtitles.
    *   `shadow_color`: Border color for layout boxes (simulating shadow/separation).

### 3. Reproduction Code

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Helper function for theme
def _get_theme_palette(theme_name: str):
    if theme_name == "mcdonalds_sales_dashboard":
        return {
            "header_bg": "002060",  # Dark blue
            "content_bg": "FFFFFF", # White
            "accent_primary": "002060", # Dark blue
            "accent_secondary": "FF0000", # Red (used for chart line in video)
            "text_dark": "000000",  # Black
            "text_light": "FFFFFF", # White
            "text_grey": "36454F", # Dark Grey for subtitle
            "shadow_color": "C0C0C0" # Light grey for border simulation of shadow
        }
    else: # Default corporate_blue
        return {
            "header_bg": "002060",
            "content_bg": "FFFFFF",
            "accent_primary": "002060",
            "accent_secondary": "FF0000",
            "text_dark": "000000",
            "text_light": "FFFFFF",
            "text_grey": "36454F",
            "shadow_color": "C0C0C0"
        }

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "mcdonalds_sales_dashboard", **kwargs) -> None:
    palette = _get_theme_palette(theme)

    # Ensure Dashboard sheet exists and is active
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)

    # Create dummy sheets for hyperlinks if they don't exist
    if "Inputs" not in wb.sheetnames:
        wb.create_sheet("Inputs")
        wb["Inputs"]['D5'] = 2544 # Mock Sales Actual
        wb["Inputs"]['D6'] = 3000 # Mock Sales Target
        wb["Inputs"]['G5'] = 890 # Mock Profit Actual
        wb["Inputs"]['G6'] = 1000 # Mock Profit Target
        wb["Inputs"]['J5'] = 87 # Mock Customers Actual
        wb["Inputs"]['J6'] = 100 # Mock Customers Target
    if "Contacts" not in wb.sheetnames:
        wb.create_sheet("Contacts")

    ws.views.sheetView[0].showGridLines = False

    # Set column A width for navigation
    ws.column_dimensions['A'].width = 8

    # Set reasonable default row height for visual appeal
    for r in range(1, 60):
        ws.row_dimensions[r].height = 20

    # Navigation Bar (Column A) - fill cells
    for row in range(1, 60): # Apply fill to a fixed range for consistent look
        ws[f'A{row}'].fill = PatternFill(start_color=palette["header_bg"], end_color=palette["header_bg"], fill_type="solid")

    # McDonald's Logo (text placeholder due to no image loading rule)
    ws['A1'].value = "M"
    ws['A1'].font = Font(name='Arial', size=24, bold=True, color='FFC000') # Yellow color, as seen in video logo
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws['A1'].hyperlink = f'#{sheet_name}!A1' # Link to itself

    # Navigation icons (text placeholders with hyperlinks)
    # Using generic characters and labels. The actual icons would be images.
    nav_items = [
        ("Presentation", "P", f"{sheet_name}!A1"), # Link to dashboard for simplicity
        ("Data Grid", "G", "Inputs!A1"),
        ("Contacts List", "C", "Contacts!A1"),
        ("Email Support", "E", "mailto:info@mcdonalds.com"),
        ("Help / Info", "?", f"{sheet_name}!A1") # Link to dashboard for simplicity
    ]
    
    current_row = 5 # Starting row for navigation icons
    icon_font = Font(name='Calibri', size=10, color=palette["text_light"])
    icon_alignment = Alignment(horizontal='center', vertical='center')

    for label, char, link in nav_items:
        ws[f'A{current_row}'].value = char
        ws[f'A{current_row}'].font = icon_font
        ws[f'A{current_row}'].alignment = icon_alignment
        if link.startswith("mailto:"):
            ws[f'A{current_row}'].hyperlink = link
        else:
            ws[f'A{current_row}'].hyperlink = f'#{link}'
        current_row += 2 # Space out icons vertically

    # --- Dashboard Layout Areas (simulated with merged cells) ---
    # Top Title Area
    main_title_range = 'B2:M4'
    ws.merge_cells(main_title_range)
    title_cell = ws['B2']
    title_cell.value = title
    title_cell.font = Font(name='Calibri', size=20, bold=True, color=palette["accent_primary"])
    title_cell.alignment = Alignment(horizontal='left', vertical='center', indent=1)
    title_cell.fill = PatternFill(start_color=palette["content_bg"], end_color=palette["content_bg"], fill_type="solid")
    title_cell.border = Border(left=Side(style='thin', color=palette["shadow_color"]), right=Side(style='thin', color=palette["shadow_color"]), top=Side(style='thin', color=palette["shadow_color"]), bottom=Side(style='thin', color=palette["shadow_color"]))
    
    ws['B3'].value = "Figures in millions of USD"
    ws['B3'].font = Font(name='Calibri', size=10, color=palette["text_grey"])
    ws['B3'].alignment = Alignment(horizontal='left', vertical='center', indent=1)

    # KPI Boxes (3 boxes)
    kpi_col_starts = ['B', 'F', 'J']
    kpi_col_ends = ['E', 'I', 'M']
    kpi_row_start = 6
    kpi_row_end = 10
    kpi_titles = ["Sales", "Profit", "# of Customers"]
    
    for i in range(3):
        col_start_letter = kpi_col_starts[i]
        col_end_letter = kpi_col_ends[i]
        
        box_range = f'{col_start_letter}{kpi_row_start}:{col_end_letter}{kpi_row_end}'
        ws.merge_cells(box_range)
        box_cell = ws[f'{col_start_letter}{kpi_row_start}']
        box_cell.fill = PatternFill(start_color=palette["content_bg"], end_color=palette["content_bg"], fill_type="solid")
        box_cell.border = Border(left=Side(style='thin', color=palette["shadow_color"]), right=Side(style='thin', color=palette["shadow_color"]), top=Side(style='thin', color=palette["shadow_color"]), bottom=Side(style='thin', color=palette["shadow_color"]))

        # KPI Title inside box
        kpi_title_cell = ws[f'{col_start_letter}{kpi_row_start+1}']
        kpi_title_cell.value = kpi_titles[i]
        kpi_title_cell.font = Font(name='Calibri', size=12, bold=True, color=palette["accent_primary"])
        kpi_title_cell.alignment = Alignment(horizontal='left', vertical='center', indent=1)

        # KPI Value (Dynamic Textbox simulation, linked to Inputs sheet for illustrative purpose)
        kpi_value_cell = ws[f'{col_start_letter}{kpi_row_start+2}']
        if i == 0: kpi_value_cell.value = "=$D$5" # Sales
        elif i == 1: kpi_value_cell.value = "=$G$5" # Profit
        else: kpi_value_cell.value = "=$J$5" # Customers
        kpi_value_cell.font = Font(name='Calibri', size=16, bold=True, color=palette["accent_primary"])
        kpi_value_cell.alignment = Alignment(horizontal='center', vertical='center')

        # KPI Percentage (Donut Chart simulation - text only, linked to Inputs sheet)
        kpi_percent_cell = ws[f'{col_end_letter}{kpi_row_start+2}']
        if i == 0: kpi_percent_cell.value = "=$D$7" # Sales % Complete
        elif i == 1: kpi_percent_cell.value = "=$G$7" # Profit % Complete
        else: kpi_percent_cell.value = "=$J$7" # Customers % Complete
        kpi_percent_cell.number_format = '0%' # Apply percentage format
        kpi_percent_cell.font = Font(name='Calibri', size=14, bold=True, color=palette["accent_primary"])
        kpi_percent_cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # Add mock percentage complete formulas to Inputs for dynamic linking
        inputs_ws = wb["Inputs"]
        inputs_ws['D7'] = "=D5/D6"
        inputs_ws['G7'] = "=G5/G6"
        inputs_ws['J7'] = "=J5/J6"

    # Large Chart Area 1 (Sales Trend)
    chart1_col_range = 'B:I'
    chart1_row_start = 12
    chart1_row_end = 22
    
    chart1_box_range = f'{chart1_col_range.split(":")[0]}{chart1_row_start}:{chart1_col_range.split(":")[1]}{chart1_row_end}'
    ws.merge_cells(chart1_box_range)
    chart1_box_cell = ws[f'{chart1_col_range.split(":")[0]}{chart1_row_start}']
    chart1_box_cell.fill = PatternFill(start_color=palette["content_bg"], end_color=palette["content_bg"], fill_type="solid")
    chart1_box_cell.border = Border(left=Side(style='thin', color=palette["shadow_color"]), right=Side(style='thin', color=palette["shadow_color"]), top=Side(style='thin', color=palette["shadow_color"]), bottom=Side(style='thin', color=palette["shadow_color"]))

    chart1_title_cell = ws[f'{chart1_col_range.split(":")[0]}{chart1_row_start+1}']
    chart1_title_cell.value = "2021-2022 Sales Trend (in millions)"
    chart1_title_cell.font = Font(name='Calibri', size=12, bold=True, color=palette["accent_primary"])
    chart1_title_cell.alignment = Alignment(horizontal='left', vertical='center', indent=1)

    # Medium Chart Area 2 (Customer Satisfaction)
    chart2_col_range = 'J:M'
    chart2_row_start = 12
    chart2_row_end = 22

    chart2_box_range = f'{chart2_col_range.split(":")[0]}{chart2_row_start}:{chart2_col_range.split(":")[1]}{chart2_row_end}'
    ws.merge_cells(chart2_box_range)
    chart2_box_cell = ws[f'{chart2_col_range.split(":")[0]}{chart2_row_start}']
    chart2_box_cell.fill = PatternFill(start_color=palette["content_bg"], end_color=palette["content_bg"], fill_type="solid")
    chart2_box_cell.border = Border(left=Side(style='thin', color=palette["shadow_color"]), right=Side(style='thin', color=palette["shadow_color"]), top=Side(style='thin', color=palette["shadow_color"]), bottom=Side(style='thin', color=palette["shadow_color"]))
    
    chart2_title_cell = ws[f'{chart2_col_range.split(":")[0]}{chart2_row_start+1}']
    chart2_title_cell.value = "Customer Satisfaction"
    chart2_title_cell.font = Font(name='Calibri', size=12, bold=True, color=palette["accent_primary"])
    chart2_title_cell.alignment = Alignment(horizontal='left', vertical='center', indent=1)

    # Map Chart Area (Sales by Country)
    map_col_range = 'N:Q'
    map_row_start = 2
    map_row_end = 22

    map_box_range = f'{map_col_range.split(":")[0]}{map_row_start}:{map_col_range.split(":")[1]}{map_row_end}'
    ws.merge_cells(map_box_range)
    map_box_cell = ws[f'{map_col_range.split(":")[0]}{map_row_start}']
    map_box_cell.fill = PatternFill(start_color=palette["content_bg"], end_color=palette["content_bg"], fill_type="solid")
    map_box_cell.border = Border(left=Side(style='thin', color=palette["shadow_color"]), right=Side(style='thin', color=palette["shadow_color"]), top=Side(style='thin', color=palette["shadow_color"]), bottom=Side(style='thin', color=palette["shadow_color"]))

    map_title_cell = ws[f'{map_col_range.split(":")[0]}{map_row_start+1}']
    map_title_cell.value = "Sales by Country 2022"
    map_title_cell.font = Font(name='Calibri', size=12, bold=True, color=palette["accent_primary"])
    map_title_cell.alignment = Alignment(horizontal='left', vertical='center', indent=1)

    # Re-order sheets to ensure Dashboard is first
    if wb.sheetnames[0] != sheet_name:
        wb.move_sheet(ws, offset=-len(wb.sheetnames) + 1)
```