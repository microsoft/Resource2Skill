### 1. High-level Skill Pattern Extraction

> **Skill Name**: Grid-Aligned Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Creates a structured, interactive-looking dashboard layout using cell-fill background masking, simulated 'cards' with borders for chart containers, and a left-aligned mock slicer pane. Disables gridlines to emphasize the visual hierarchy and seamlessly layers openpyxl charts over designated cell ranges.
* **Applicability**: Excellent for executive summaries and final reporting tabs. Use when you need to present aggregated KPIs and multiple charts in a polished, "BI-tool" style view. *(Note: Because openpyxl does not support interactive Pivot Slicers, this creates the visual aesthetic and static layout of a dashboard for automated PDF/email reporting).*

### 2. Structural Breakdown

- **Data Layout**: Generates a hidden `_Data` sheet holding the aggregated metrics (Trend, Category, Top States) so the presentation sheet remains completely clean.
- **Formula Logic**: Standard data mappings bridging the backend data matrix to the frontend `Reference` objects.
- **Visual Design**: Hides sheet gridlines (`showGridLines = False`), paints the entire viewport with a low-contrast background (`bg`), and carves out distinct white/dark blocks (`card`) with thin borders to act as visual containers.
- **Charts/Tables**: Slices the grid into columns, placing a `LineChart` for time-series and `BarChart`s for categorical comparisons. Charts are styled using Excel's built-in themes (e.g., `style=48` for dark mode) and their borders are disabled to blend into the card backgrounds.
- **Theme Hooks**: Consumes `bg`, `card`, `header`, `header_text`, `text`, `border`, and `accent` to ensure the dashboard seamlessly flips between light and dark modes.

### 3. Reproduction Code

```python
def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.chart import LineChart, BarChart, Reference

    # 1. Theme setup
    themes = {
        "corporate_blue": {
            "bg": "F3F4F6", "card": "FFFFFF", "header": "1F4E78",
            "header_text": "FFFFFF", "text": "333333", "border": "D1D5DB", "accent": "4472C4"
        },
        "dark_mode": {
            "bg": "121212", "card": "1E1E1E", "header": "000000",
            "header_text": "FFFFFF", "text": "E5E7EB", "border": "333333", "accent": "007ACC"
        }
    }
    palette = themes.get(theme, themes["corporate_blue"])

    # 2. Data Generation (Hidden backend sheet)
    data_ws = wb.create_sheet(f"{sheet_name}_Data")
    data_ws.sheet_state = 'hidden'
    
    # Trend Data
    data_ws.append(["Month", "Revenue", "Profit"])
    trend_data = [("Jan", 15, 4), ("Feb", 18, 5), ("Mar", 22, 7), ("Apr", 21, 6), ("May", 25, 8), ("Jun", 28, 9)]
    for m, r, p in trend_data:
        data_ws.append([m, r*1000, p*1000])
        
    # Category Data
    data_ws.append([])
    cat_start_row = data_ws.max_row + 1
    data_ws.append(["Category", "2023", "2024"])
    data_ws.append(["Hoodies", 7200, 8500])
    data_ws.append(["T-Shirts", 14500, 16200])
    
    # State Data
    data_ws.append([])
    state_start_row = data_ws.max_row + 1
    data_ws.append(["State", "Profit"])
    states = [("California", 35000), ("Texas", 31000), ("New York", 28000), ("Florida", 22000), ("Illinois", 19000)]
    for s, p in states:
        data_ws.append([s, p])

    # 3. Dashboard Shell Layout
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    bg_fill = PatternFill("solid", fgColor=palette["bg"])
    card_fill = PatternFill("solid", fgColor=palette["card"])
    border_side = Side(style='thin', color=palette["border"])
    
    # Set spacing column widths
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 2
    ws.column_dimensions['C'].width = 15  # Slicer column
    ws.column_dimensions['D'].width = 2
    ws.column_dimensions['E'].width = 2   # Padding
    
    # Fill master background
    for row in range(1, 40):
        for col in range(1, 26):
            ws.cell(row=row, column=col).fill = bg_fill

    # Render Header Banner
    ws.merge_cells("B2:X3")
    hdr = ws["B2"]
    hdr.value = title
    hdr.fill = PatternFill("solid", fgColor=palette["header"])
    hdr.font = Font(size=22, bold=True, color=palette["header_text"])
    hdr.alignment = Alignment(horizontal="center", vertical="center")

    def draw_card(start_col, start_row, end_col, end_row, card_title):
        """Paints a 'card' container using cell styling."""
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = card_fill
                # Apply border only to the outer perimeter of the card block
                cell.border = Border(
                    top=border_side if r == start_row else None,
                    bottom=border_side if r == end_row else None,
                    left=border_side if c == start_col else None,
                    right=border_side if c == end_col else None
                )
        
        ws.merge_cells(start_row=start_row, start_column=start_col, end_row=start_row, end_column=end_col)
        tc = ws.cell(row=start_row, column=start_col)
        tc.value = card_title
        tc.font = Font(bold=True, size=12, color=palette["text"])
        tc.alignment = Alignment(horizontal="center", vertical="center")

    # Render Cards
    draw_card(2, 5, 4, 35, "Filters")
    draw_card(6, 5, 15, 18, "Revenue Trend")
    draw_card(17, 5, 24, 18, "Units Sold by Category")
    draw_card(6, 20, 24, 35, "Top 5 States by Profit")

    # 4. Slicer UI Mocks (Static Visuals)
    def draw_slicer(col, start_row, items, label):
        ws.cell(row=start_row, column=col, value=label).font = Font(bold=True, size=10, color=palette["text"])
        for i, item in enumerate(items):
            cell = ws.cell(row=start_row + 1 + i, column=col)
            cell.value = item
            is_active = (i == 0) # Mock selection logic
            
            bg = palette["accent"] if is_active else palette["card"]
            fg = "FFFFFF" if is_active else palette["text"]
            cell.fill = PatternFill("solid", fgColor=bg)
            cell.font = Font(color=fg)
            cell.alignment = Alignment(horizontal="center")
            cell.border = Border(left=border_side, right=border_side, top=border_side, bottom=border_side)

    draw_slicer(3, 7, ["2023", "2024"], "Year")
    draw_slicer(3, 11, ["Hoodies", "T-Shirts"], "Category")
    draw_slicer(3, 15, ["California", "Texas", "New York", "Florida", "Illinois"], "State")

    # 5. Dashboard Charts
    chart_theme_idx = 13 if theme == "corporate_blue" else 48

    # Chart 1: Trend
    lc = LineChart()
    lc.title = None
    lc.style = chart_theme_idx
    data = Reference(data_ws, min_col=2, min_row=1, max_col=3, max_row=7)
    cats = Reference(data_ws, min_col=1, min_row=2, max_row=7)
    lc.add_data(data, titles_from_data=True)
    lc.set_categories(cats)
    lc.width = 18
    lc.height = 7
    lc.graphical_properties.line.noFill = True  # Disables chart bounds to blend with card
    ws.add_chart(lc, "F6")

    # Chart 2: Category Comparison
    bc1 = BarChart()
    bc1.type = "col"
    bc1.style = chart_theme_idx
    bc1.title = None
    data2 = Reference(data_ws, min_col=2, min_row=cat_start_row, max_col=3, max_row=cat_start_row+2)
    cats2 = Reference(data_ws, min_col=1, min_row=cat_start_row+1, max_row=cat_start_row+2)
    bc1.add_data(data2, titles_from_data=True)
    bc1.set_categories(cats2)
    bc1.width = 13.5
    bc1.height = 7
    bc1.graphical_properties.line.noFill = True
    ws.add_chart(bc1, "Q6")

    # Chart 3: Top States
    bc2 = BarChart()
    bc2.type = "col"
    bc2.style = chart_theme_idx
    bc2.title = None
    bc2.legend = None
    data3 = Reference(data_ws, min_col=2, min_row=state_start_row, max_col=2, max_row=state_start_row+5)
    cats3 = Reference(data_ws, min_col=1, min_row=state_start_row+1, max_row=state_start_row+5)
    bc2.add_data(data3, titles_from_data=True)
    bc2.set_categories(cats3)
    bc2.width = 33.5
    bc2.height = 8.5
    bc2.graphical_properties.line.noFill = True
    ws.add_chart(bc2, "F21")
```