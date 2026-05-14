### 1. High-level Skill Pattern Extraction

> **Skill Name**: Data Bar Performance Table

* **Tier**: component
* **Core Mechanism**: Renders a tabular leaderboard (e.g., multi-metric sales performance) and automatically overlays Data Bar conditional formatting onto the numeric columns. Maps individual column bar colors to distinct tokens from the theme palette for quick, side-by-side visual benchmarking.
* **Applicability**: Perfect for performance dashboards, leaderboards, or summary tables where the relative magnitude of metrics across categories needs to be grasped quickly without consuming the space of a standalone chart.

### 2. Structural Breakdown

- **Data Layout**: Categorical column (e.g., Agent Name) followed by an arbitrary number of numeric metric columns.
- **Formula Logic**: N/A (Static data rendering relying on Conditional Formatting for dynamic visual scaling).
- **Visual Design**: Themed solid header row with bold contrasting text; standard cell borders omitted for cleaner integration.
- **Charts/Tables**: Employs openpyxl's `DataBarRule` instead of standalone charts to create in-cell bar charts directly behind the numbers.
- **Theme Hooks**: Uses `primary` for the table header fill and highest priority metric, branching to `secondary`, `accent`, and `muted` for the other metric data bars.

### 3. Reproduction Code

```python
def render(ws, anchor: str, *, data: list[dict] = None, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.utils import column_index_from_string, get_column_letter
    from openpyxl.styles import Font, PatternFill
    from openpyxl.formatting.rule import DataBarRule
    import re

    # Default data based on the Sales Agent KPI leaderboard
    if not data:
        data = [
            {"Agent": "Alex", "Calls": 1031, "Reached": 56, "Closed": 27, "Value": 13519},
            {"Agent": "Alice", "Calls": 827, "Reached": 128, "Closed": 49, "Value": 41200},
            {"Agent": "Bob", "Calls": 661, "Reached": 73, "Closed": 28, "Value": 40092},
            {"Agent": "Charlie", "Calls": 610, "Reached": 86, "Closed": 67, "Value": 45236},
            {"Agent": "Chris", "Calls": 737, "Reached": 168, "Closed": 91, "Value": 11093},
            {"Agent": "Craig", "Calls": 1096, "Reached": 159, "Closed": 4, "Value": 32176},
            {"Agent": "Darren", "Calls": 262, "Reached": 167, "Closed": 75, "Value": 41186},
            {"Agent": "David", "Calls": 375, "Reached": 120, "Closed": 48, "Value": 2590},
        ]

    # Theme palette fallback loader (Replace with framework's standard loader)
    palettes = {
        "corporate_blue": {"primary": "4F81BD", "secondary": "C0504D", "accent": "9BBB59", "muted": "DCE6F1"},
        "dashboard_purple": {"primary": "5A3385", "secondary": "F2C811", "accent": "A88CDB", "muted": "FCEF9C"}
    }
    theme_colors = palettes.get(theme, palettes["corporate_blue"])

    def to_argb(hex_str: str) -> str:
        h = hex_str.replace("#", "")
        return h if len(h) == 8 else f"FF{h}"

    color_primary = to_argb(theme_colors.get("primary", "4F81BD"))
    color_secondary = to_argb(theme_colors.get("secondary", "C0504D"))
    color_accent = to_argb(theme_colors.get("accent", "9BBB59"))
    color_muted = to_argb(theme_colors.get("muted", "DCE6F1"))

    # Config for mapping keys to columns and data bar rules
    metrics = [
        {"key": "Calls", "header": "Total Calls", "color": color_muted, "num_format": "#,##0"},
        {"key": "Reached", "header": "Calls Reached", "color": color_secondary, "num_format": "#,##0"},
        {"key": "Closed", "header": "Deals Closed", "color": color_accent, "num_format": "#,##0"},
        {"key": "Value", "header": "Deal Value", "color": color_primary, "num_format": "$#,##0"}
    ]

    # Parse anchor
    match = re.match(r"([A-Z]+)(\d+)", anchor)
    if not match:
        raise ValueError(f"Invalid anchor: {anchor}")
    anchor_col_letter, anchor_row_str = match.groups()
    start_col = column_index_from_string(anchor_col_letter)
    start_row = int(anchor_row_str)

    header_fill = PatternFill(start_color=color_primary, end_color=color_primary, fill_type="solid")
    header_font = Font(color="FFFFFFFF", bold=True)

    # Write Headers
    ws.cell(row=start_row, column=start_col, value="Agent").fill = header_fill
    ws.cell(row=start_row, column=start_col, value="Agent").font = header_font
    ws.column_dimensions[get_column_letter(start_col)].width = 15
    
    for i, metric in enumerate(metrics):
        col_idx = start_col + 1 + i
        c = ws.cell(row=start_row, column=col_idx, value=metric["header"])
        c.fill = header_fill
        c.font = header_font
        ws.column_dimensions[get_column_letter(col_idx)].width = 14

    # Write Data
    for r_idx, row_data in enumerate(data, start=1):
        ws.cell(row=start_row + r_idx, column=start_col, value=row_data["Agent"])
        for i, metric in enumerate(metrics):
            c = ws.cell(row=start_row + r_idx, column=start_col + 1 + i, value=row_data[metric["key"]])
            c.number_format = metric["num_format"]

    # Apply Individual Data Bars per Column
    last_row = start_row + len(data)
    for i, metric in enumerate(metrics):
        col_letter = get_column_letter(start_col + 1 + i)
        cell_range = f"{col_letter}{start_row + 1}:{col_letter}{last_row}"
        
        # Overlays a gradient bar representing the cell's scale relative to its column min/max
        rule = DataBarRule(start_type='min', end_type='max', color=metric["color"])
        ws.conditional_formatting.add(cell_range, rule)
```