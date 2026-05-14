### 1. High-level Skill Pattern Extraction

> **Skill Name**: App-Like Sidebar Navigation

* **Tier**: archetype
* **Core Mechanism**: Constructs a multi-sheet workbook where the first column of every sheet acts as a fixed navigation sidebar. Uses emojis as icons, internal hyperlinks for cross-sheet navigation, and highlights the active tab's icon with a contrasting background color to mimic a standalone web application.
* **Applicability**: Multi-tab financial reports, dashboards, or data tools where users need to seamlessly toggle between summary views, raw data inputs, and settings pages without using standard Excel sheet tabs.

### 2. Structural Breakdown

- **Data Layout**: Column A is narrowed to act as the sidebar container. Rows 1-40 form the physical bar. Icons are spaced out vertically every 4 rows starting from row 4.
- **Formula Logic**: Utilizes internal workbook hyperlink syntax (`#'SheetName'!A1`) bound to the `.hyperlink` property to instantly snap the user to different views.
- **Visual Design**: Disables sheet gridlines for a clean canvas. The sidebar is painted with a primary theme color, while the currently active tab receives a lighter accent fill to indicate selection state. 
- **Charts/Tables**: N/A (creates the structural shell for placing charts/tables).
- **Theme Hooks**: Consumes `primary_bg` for the main sidebar fill, `primary_light` for the active state highlight, and `text_fg` (usually white) for the centered icons.

### 3. Reproduction Code

```python
def render_workbook(wb, *, title: str = "App Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import PatternFill, Font, Alignment

    # Standardized theme palette fallback
    theme_colors = {
        "primary_bg": "1F4E78",    # Dark Blue
        "primary_light": "2E75B6", # Lighter Blue (active state)
        "text_fg": "FFFFFF",       # White
    }

    # Define tabs and their corresponding navigation icons/links
    tabs = [
        ("Dashboard", "🏠", "#'Dashboard'!A1"),
        ("Inputs", "📊", "#'Inputs'!A1"),
        ("Contacts", "✉️", "#'Contacts'!A1"),
        ("Support", "❓", "mailto:support@example.com")
    ]

    # Ensure all defined functional tabs exist
    for tab_name, _, _ in tabs:
        if tab_name != "Support" and tab_name not in wb.sheetnames:
            wb.create_sheet(tab_name)

    # Remove default empty sheet if it's not part of our tabs
    if "Sheet" in wb.sheetnames and len(wb.sheetnames) > 1:
        wb.remove(wb["Sheet"])

    # Create reusable styles
    sidebar_fill = PatternFill(start_color=theme_colors["primary_bg"], end_color=theme_colors["primary_bg"], fill_type="solid")
    active_fill = PatternFill(start_color=theme_colors["primary_light"], end_color=theme_colors["primary_light"], fill_type="solid")
    icon_font = Font(color=theme_colors["text_fg"], size=20, bold=True)
    center_align = Alignment(horizontal="center", vertical="center")

    # Apply the sidebar shell to every sheet in the workbook
    for ws in wb.worksheets:
        # Clean dashboard look (disables the default Excel cell grid)
        ws.sheet_view.showGridLines = False

        # Set sidebar column width
        ws.column_dimensions['A'].width = 8

        # Paint the sidebar background
        for row in range(1, 40):
            ws.cell(row=row, column=1).fill = sidebar_fill

        # Place icons and attach hyperlinks
        start_row = 4
        row_spacing = 4

        for i, (tab_name, icon, link) in enumerate(tabs):
            cell_row = start_row + (i * row_spacing)
            cell = ws.cell(row=cell_row, column=1, value=icon)

            # Assign hyperlink (internal sheet link or external mailto)
            cell.hyperlink = link

            # Highlight the active tab to show the user where they are
            if ws.title == tab_name:
                cell.fill = active_fill

            # EXCEL QUIRK: openpyxl automatically applies standard hyperlink styling (blue text, underline)
            # when a hyperlink is assigned. We MUST apply our custom font styling AFTER setting the link.
            cell.font = icon_font
            cell.alignment = center_align

            # Add a subtle text label next to the active icon for better UX context
            if ws.title == tab_name:
                title_cell = ws.cell(row=cell_row, column=2, value=tab_name)
                title_cell.font = Font(size=16, bold=True, color=theme_colors["primary_bg"])
                title_cell.alignment = Alignment(vertical="center")
```