### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed KPI Dashboard Layout

* **Tier**: sheet_shell
* **Core Mechanism**: Creates a grid-based dashboard using merged cells to construct large-typography "KPI Cards". Applies dynamic `CellIsRule` conditional formatting to the primary metric value, coloring it green or red based on a comparison to the "Vs. Target" sub-metric cell rendered directly below it.
* **Applicability**: Best used for executive summaries, financial overviews, or monthly operational reports where stakeholders need immediate pass/fail visual cues across multiple categorized metrics. Requires pre-calculated actuals, targets, and prior-period values.

### 2. Structural Breakdown

- **Data Layout**: Categories span rows horizontally as separator bands. Each KPI card consumes a 4-column by 3-row grid (Header, Value, Sub-metrics) with a 1-column spacer between cards. Max 3 cards per row. 
- **Formula Logic**: Uses standard values mapped into cells, but links Conditional Formatting rules to adjacent cells (e.g., Value cell `<` Target cell).
- **Visual Design**: Turns off gridlines to simulate a dashboard canvas. Metric values use 24pt bold font. Employs classic solid fills (Green/Red) and dark font colors for conditional pass/fail states.
- **Charts/Tables**: Replaces traditional charts with high-contrast typographic data blocks.
- **Theme Hooks**: Consumes primary theme colors for the section banners and muted accents for the individual KPI card headers.

### 3. Reproduction Code

```python
def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", kpi_data: list = None, **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.formatting.rule import CellIsRule
    from openpyxl.utils import get_column_letter

    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # Theme palette fallback
    palettes = {
        "corporate_blue": {"header": "4F81BD", "card_hdr": "DCE6F1", "text": "000000"},
        "modern_dark": {"header": "2F2F2F", "card_hdr": "595959", "text": "FFFFFF"}
    }
    colors = palettes.get(theme, palettes["corporate_blue"])

    # Standard conditional formatting styles
    good_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    bad_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    good_font = Font(color="006100", size=24, bold=True)
    bad_font = Font(color="9C0006", size=24, bold=True)

    if not kpi_data:
        kpi_data = [
            {
                "category": "Working Capital Efficiency",
                "kpis": [
                    {"name": "DSO (Days Sales Outstanding)", "value": 31, "target": 45, "prior": 41, "is_lower_better": True, "format": "0"},
                    {"name": "DPO (Days Payables Outstanding)", "value": 89, "target": 90, "prior": 90, "is_lower_better": False, "format": "0"},
                    {"name": "Non-Current AR %", "value": 0.12, "target": 0.03, "prior": 0.12, "is_lower_better": True, "format": "0%"}
                ]
            },
            {
                "category": "Sales & Cost KPIs",
                "kpis": [
                    {"name": "CAC (Customer Acquisition Cost)", "value": 26319, "target": 15000, "prior": 17725, "is_lower_better": True, "format": "$#,##0"},
                    {"name": "Gross Margin", "value": 0.20, "target": 0.38, "prior": 0.26, "is_lower_better": False, "format": "0%"}
                ]
            }
        ]

    # Dashboard Title
    title_cell = ws["B2"]
    title_cell.value = title
    title_cell.font = Font(size=20, bold=True, color=colors["header"])

    # Month Selector Mockup
    ws["B3"] = "For the month of:"
    ws["B3"].font = Font(bold=True)
    ws["C3"] = "Aug-2023" # In a full system, this would be data validation
    ws["C3"].fill = PatternFill(start_color="FFF2CC", fill_type="solid")
    ws["C3"].border = Border(bottom=Side(style="thin", color="000000"))

    current_row = 5
    thin_border = Border(
        left=Side(style="thin", color="D9D9D9"), right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"), bottom=Side(style="thin", color="D9D9D9")
    )

    for category in kpi_data:
        # Category Banner (Spans cols 2 through 15)
        ws.merge_cells(start_row=current_row, start_column=2, end_row=current_row, end_column=15)
        sec_hdr = ws.cell(current_row, 2)
        sec_hdr.value = category["category"]
        sec_hdr.fill = PatternFill(start_color=colors["header"], fill_type="solid")
        sec_hdr.font = Font(color="FFFFFF", bold=True, size=14)
        sec_hdr.alignment = Alignment(horizontal="center", vertical="center")
        
        current_row += 2
        col_offset = 2

        for kpi in category.get("kpis", []):
            if col_offset > 12: # Wrap to next row after 3 cards (each card is 4 cols + 1 spacer)
                current_row += 5
                col_offset = 2

            # 1. KPI Name Header
            ws.merge_cells(start_row=current_row, start_column=col_offset, end_row=current_row, end_column=col_offset+3)
            name_cell = ws.cell(current_row, col_offset)
            name_cell.value = kpi["name"]
            name_cell.fill = PatternFill(start_color=colors["card_hdr"], fill_type="solid")
            name_cell.font = Font(bold=True, color=colors["text"])
            name_cell.alignment = Alignment(horizontal="center")

            # 2. Main KPI Value
            ws.merge_cells(start_row=current_row+1, start_column=col_offset, end_row=current_row+1, end_column=col_offset+3)
            val_cell = ws.cell(current_row+1, col_offset)
            val_cell.value = kpi["value"]
            val_cell.font = Font(size=24, bold=True)
            val_cell.alignment = Alignment(horizontal="center")
            val_cell.number_format = kpi["format"]

            # 3. Sub-metrics (Target & Prior)
            # Vs Target
            ws.cell(current_row+2, col_offset, "Vs. Target").font = Font(size=9, color="595959")
            tgt_cell = ws.cell(current_row+2, col_offset+1, kpi["target"])
            tgt_cell.number_format = kpi["format"]
            tgt_cell.font = Font(size=9, bold=True)

            # Vs Prior Month
            ws.cell(current_row+2, col_offset+2, "Vs. Prior").font = Font(size=9, color="595959")
            prior_cell = ws.cell(current_row+2, col_offset+3, kpi["prior"])
            prior_cell.number_format = kpi["format"]
            prior_cell.font = Font(size=9, bold=True)

            # Align and border sub-metrics
            for c in range(col_offset, col_offset+4):
                ws.cell(current_row+2, c).alignment = Alignment(horizontal="center")
                ws.cell(current_row+2, c).border = thin_border
            val_cell.border = thin_border

            # 4. Conditional Formatting Magic
            tgt_addr = f"${get_column_letter(col_offset+1)}${current_row+2}"
            val_addr = f"{get_column_letter(col_offset)}{current_row+1}"

            if kpi["is_lower_better"]:
                ws.conditional_formatting.add(val_addr, CellIsRule(operator='lessThan', formula=[tgt_addr], fill=good_fill, font=good_font))
                ws.conditional_formatting.add(val_addr, CellIsRule(operator='greaterThanOrEqual', formula=[tgt_addr], fill=bad_fill, font=bad_font))
            else:
                ws.conditional_formatting.add(val_addr, CellIsRule(operator='greaterThanOrEqual', formula=[tgt_addr], fill=good_fill, font=good_font))
                ws.conditional_formatting.add(val_addr, CellIsRule(operator='lessThan', formula=[tgt_addr], fill=bad_fill, font=bad_font))

            col_offset += 5

        current_row += 5

    # Base column width normalization to ensure cards look uniform
    for col in range(2, 16):
        ws.column_dimensions[get_column_letter(col)].width = 13.5
```