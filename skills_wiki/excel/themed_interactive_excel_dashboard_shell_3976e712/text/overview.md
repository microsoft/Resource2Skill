### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Interactive Excel Dashboard Shell

*   **Tier**: sheet_shell
*   **Core Mechanism**: This skill constructs a complete dashboard layout on an Excel sheet. It organizes key performance indicators (KPIs), trend charts, and categorical data visualizations into distinct, visually separated sections using merged cell regions that conceptually represent styled shapes. It also integrates dynamic navigation between sheets via a persistent sidebar with hyperlinks.
*   **Applicability**: This pattern is highly reusable for creating professional and interactive dashboards or summary reports in Excel. It can be adapted to present various business metrics across different domains (sales, finance, operations) by populating the pre-defined areas with specific data and charts.

### 2. Structural Breakdown

-   **Data Layout**:
    *   **Navigation Sidebar (Column A)**: A full column with a dark background, containing icon-like cells linked to other sheets (Dashboard, Inputs, Contacts, Email).
    *   **Main Header (B1:M2)**: A large merged cell area for the dashboard's main title and a subtitle (e.g., "Sales Dashboard South America 2022").
    *   **KPI Section (3 boxes)**: Three horizontally aligned merged cell areas (e.g., B6:D10, E6:G10, H6:J10) to house individual KPI summaries.
    *   **Main Trend Chart Area (B12:I27)**: A large merged cell area for a detailed line chart showing trends.
    *   **Sales by Country Map Area (J6:M19)**: A vertical merged cell area on the right for a geographical map visualization.
    *   **Customer Satisfaction Area (J21:M27)**: A smaller merged cell area below the map for a customer satisfaction chart (e.g., Radar chart).
-   **Formula Logic**:
    *   **Hyperlinks**: Cells in the navigation sidebar are set up with hyperlinks to specific sheet references (e.g., `Inputs!A1`) or external email addresses (`mailto:`).
    *   **Dynamic Textboxes (for KPIs)**: Textboxes placed within the KPI merged cell areas are dynamically linked to specific cells on the `Inputs` sheet (e.g., `=Inputs!D5` for sales actual amount, `=Inputs!D7` for sales percentage complete).
-   **Visual Design**:
    *   **Overall Theme**: Predominantly white background for content areas and a dark blue for the sidebar and main titles, giving a clean, corporate look.
    *   **Gridlines**: Hidden for a clean canvas appearance.
    *   **Navigation Sidebar**: Dark blue solid fill (from `sidebar_bg` theme token), with white, bold text for navigation labels. Hyperlinks have no underline.
    *   **Content Area Backgrounds**: Merged cells representing the "shapes" (header, KPIs, chart areas) have a white solid fill (`panel_bg` theme token).
    *   **Shape Appearance (Conceptual)**: In the tutorial, these areas are explicitly created using "Rounded Rectangle" shapes with no outline and a subtle outer shadow. In code, this is represented by merged cell areas with background fill and borders to delineate sections, with the understanding that actual complex shape rendering is done manually or via pre-rendered images in OpenPyXL.
    *   **Text Formatting**: Main titles are large (24pt), bold, and dark blue. Section titles within KPI/chart areas are smaller (11pt), bold, and dark blue. Numeric KPI values are large (20pt+), bold, and dark blue.
-   **Charts/Tables**: The skill creates containers for charts. The charts themselves (Radar, Line, Filled Map, Donut) are separate visual components placed into these structured areas. Their specific formatting (colors, markers, axes) is handled during the `VISUALS` and `CUSTOMIZE` steps in the tutorial.
-   **Theme Hooks**: `sidebar_bg`, `header_bg`, `panel_bg`, `text_dark_blue`, `shadow_color` (conceptual).

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.hyperlink import Hyperlink
from openpyxl.utils.cell import get_column_letter

def get_theme_colors(theme_name: str = "corporate_blue") -> dict:
    # A simplified theme for demonstration purposes, matching video's visual style.
    # In a full theme system, these would be loaded from a central config.
    if theme_name == "corporate_blue":
        return {
            "header_bg": "FF003366", # Dark Blue
            "panel_bg": "FFFFFFFF",  # White
            "text_dark_blue": "FF003366", # Dark Blue
            "sidebar_bg": "FF003366", # Dark Blue
            "shadow_color": "FF808080", # Gray for conceptual shadow (OpenPyXL limitation)
            "accent_red": "FFFF0000",
            "accent_blue": "FF0000FF",
            "light_blue": "FFCCCCFF"
        }
    # Fallback for other themes or missing theme
    return {
        "header_bg": "FF003366",
        "panel_bg": "FFFFFFFF",
        "text_dark_blue": "FF003366",
        "sidebar_bg": "FF003366",
        "shadow_color": "FF808080",
        "accent_red": "FFFF0000",
        "accent_blue": "FF0000FF",
        "light_blue": "FFCCCCFF"
    }

def render_workbook(wb, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    # This skill focuses on creating the primary dashboard sheet structure and navigation.
    # It sets up merged cell regions and basic styling to act as containers for visuals.
    # Actual complex shapes (rounded rectangles with shadows) are Excel-specific drawing objects
    # that OpenPyXL's direct API does not fully support with advanced formatting.
    # This code creates the underlying cell structure and styling as a reproducible shell.

    colors = get_theme_colors(theme)

    # Ensure Dashboard sheet exists and is active
    if 'Dashboard' in wb.sheetnames:
        ws = wb['Dashboard']
    else:
        ws = wb.create_sheet("Dashboard")
    wb.active = ws  # Make Dashboard the active sheet

    # Hide gridlines for a clean look
    ws.sheet_view.showGridLines = False

    # --- 1. Adjust Column Widths ---
    ws.column_dimensions['A'].width = 8  # Sidebar column
    for i in range(2, 14):  # Columns B through M for content
        col_letter = get_column_letter(i)
        ws.column_dimensions[col_letter].width = 10 # Example width, adjust as needed

    # --- 2. Navigation Sidebar (Column A) ---
    # Apply dark blue background to Column A
    for row in ws.iter_rows(min_col=1, max_col=1):
        for cell in row:
            cell.fill = PatternFill(start_color=colors["sidebar_bg"], end_color=colors["sidebar_bg"], fill_type="solid")

    # Add placeholder text for navigation items (actual icons would be images)
    # Hyperlinks are added to cells, representing the dynamic navigation shown in video.
    nav_items = {
        "📊 Dashboard": ("Dashboard", 6),
        "📝 Inputs": ("Inputs", 10),
        "📞 Contacts": ("Contacts", 14),
        "❓ Support": ("mailto:support@example.com", 18)
    }

    for text, (target, row_num) in nav_items.items():
        cell = ws[f'A{row_num}']
        cell.value = text
        cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFFFF", underline="none")
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

        if "mailto:" in target:
            cell.hyperlink = Hyperlink(ref=cell.coordinate, target=target, tooltip=f"Send email to {target.split(':')[1]}")
        else:
            # Create other sheets if they don't exist, for hyperlinks to work
            if target not in wb.sheetnames:
                wb.create_sheet(target)
            cell.hyperlink = Hyperlink(ref=cell.coordinate, location=f"'{target}'!A1", tooltip=f"Go to {target} sheet")
        # Openpyxl doesn't directly apply a "Hyperlink" style with specific color, so set font color explicitly

    # --- 3. Main Dashboard Title Area ---
    ws.merge_cells('B1:M2')
    header_title_cell = ws['B1']
    header_title_cell.value = f"Sales Dashboard South America 2022"
    header_title_cell.font = Font(name="Calibri", size=24, bold=True, color=colors["text_dark_blue"])
    header_title_cell.fill = PatternFill(start_color=colors["panel_bg"], end_color=colors["panel_bg"], fill_type="solid")
    header_title_cell.alignment = Alignment(horizontal='center', vertical='center')

    ws.merge_cells('B3:M4') # Adjusting merge to give space for subtitle
    header_subtitle_cell = ws['B3']
    header_subtitle_cell.value = "Figures in millions of USD"
    header_subtitle_cell.font = Font(name="Calibri", size=11, color=colors["text_dark_blue"])
    header_subtitle_cell.fill = PatternFill(start_color=colors["panel_bg"], end_color=colors["panel_bg"], fill_type="solid")
    header_subtitle_cell.alignment = Alignment(horizontal='center', vertical='center')

    # --- 4. Content Sections (KPIs and Charts) ---
    # Define areas where shapes would be, using merged cells and styling them as containers.
    # The actual rounded corners and shadows from the video are Excel shape properties not fully exposed in OpenPyXL.
    
    # KPI Boxes
    kpi_definitions = [
        {'title': 'Sales', 'range': 'B6:D10'},
        {'title': 'Profit', 'range': 'E6:G10'},
        {'title': '# of Customers', 'range': 'H6:J10'}
    ]

    for kpi in kpi_definitions:
        ws.merge_cells(kpi['range'])
        kpi_cell = ws[kpi['range'].split(':')[0]]
        kpi_cell.value = kpi['title']
        kpi_cell.font = Font(name="Calibri", size=11, bold=True, color=colors["text_dark_blue"])
        kpi_cell.fill = PatternFill(start_color=colors["panel_bg"], end_color=colors["panel_bg"], fill_type="solid")
        kpi_cell.alignment = Alignment(horizontal='center', vertical='top')
        # Add a simple border to visually define the container
        kpi_cell.border = Border(left=Side(style='thin', color='FFD3D3D3'),
                                 right=Side(style='thin', color='FFD3D3D3'),
                                 top=Side(style='thin', color='FFD3D3D3'),
                                 bottom=Side(style='thin', color='FFD3D3D3'))
        
    # Chart Areas
    chart_area_definitions = [
        {'title': '2021-2022 Sales Trend (in millions)', 'range': 'B12:I27'},
        {'title': 'Sales by Country 2022', 'range': 'J6:M19'}, # Adjusted range to fit video layout
        {'title': 'Customer Satisfaction', 'range': 'J21:M27'}
    ]

    for chart_area in chart_area_definitions:
        ws.merge_cells(chart_area['range'])
        chart_cell = ws[chart_area['range'].split(':')[0]]
        chart_cell.value = chart_area['title']
        chart_cell.font = Font(name="Calibri", size=11, bold=True, color=colors["text_dark_blue"])
        chart_cell.fill = PatternFill(start_color=colors["panel_bg"], end_color=colors["panel_bg"], fill_type="solid")
        chart_cell.alignment = Alignment(horizontal='center', vertical='top')
        # Add a simple border to visually define the container
        chart_cell.border = Border(left=Side(style='thin', color='FFD3D3D3'),
                                 right=Side(style='thin', color='FFD3D3D3'),
                                 top=Side(style='thin', color='FFD3D3D3'),
                                 bottom=Side(style='thin', color='FFD3D3D3'))

    # Create dummy sheets for navigation if they don't exist
    if 'Inputs' not in wb.sheetnames:
        wb.create_sheet('Inputs')
    if 'Contacts' not in wb.sheetnames:
        wb.create_sheet('Contacts')

    # Example for Inputs sheet (minimal content as placeholder)
    inputs_ws = wb['Inputs']
    inputs_ws['D5'] = 2544
    inputs_ws['D6'] = 3000
    inputs_ws['D7'] = '=D5/D6'
    inputs_ws['D7'].style = 'Percent'
    inputs_ws['G5'] = 890
    inputs_ws['G6'] = 1000
    inputs_ws['G7'] = '=G5/G6'
    inputs_ws['G7'].style = 'Percent'
    inputs_ws['J5'] = 87
    inputs_ws['J6'] = 100
    inputs_ws['J7'] = '=J5/J6'
    inputs_ws['J7'].style = 'Percent'
    inputs_ws['C5'].value = "Actual"
    inputs_ws['C6'].value = "Target"
    inputs_ws['F5'].value = "Actual"
    inputs_ws['F6'].value = "Target"
    inputs_ws['I5'].value = "Actual"
    inputs_ws['I6'].value = "Target"
    inputs_ws.sheet_view.showGridLines = False

    # Example for Contacts sheet
    contacts_ws = wb['Contacts']
    contacts_ws['A1'].value = "Country"
    contacts_ws['B1'].value = "General Manager"
    contacts_ws['C1'].value = "Email"
    contacts_ws.sheet_view.showGridLines = False

```