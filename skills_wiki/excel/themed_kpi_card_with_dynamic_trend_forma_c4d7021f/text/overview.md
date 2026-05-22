```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed KPI Card with Dynamic Trend Formatting

* **Tier**: component
* **Core Mechanism**: Constructs a 2-row merged grid acting as a cohesive "card" for a key metric. Uses a powerful custom Number Format string (`[Color10]▲ 0.0%;[Color3]▼ -0.0%;"-"`) to automatically inject trend arrows and colorize the variance metric without relying on complex Conditional Formatting rules.
* **Applicability**: Essential for executive summaries and dark-themed dashboards where high-level figures (like Revenue or Traffic) must be prominently displayed alongside their period-over-period performance indicators. 

### 2. Structural Breakdown

- **Data Layout**: A 2x3 cell anchor area. The top row is merged across all 3 columns for the metric title. The second row houses the main metric (merged across the first 2 columns) and the variance/trend metric resides in the 3rd column.
- **Formula Logic**: Readily accepts static floats or dynamic formula strings linking back to pivot outputs. 
- **Visual Design**: Uses a solid block pattern fill to simulate a floating UI card. Establishes visual hierarchy using heavy font-size contrast (10pt title vs 18pt value). 
- **Charts/Tables**: N/A (replaces the need for embedded text boxes, which are commonly misused in Excel dashboards).
- **Theme Hooks**: `bg_color` (card background), `title_color` (muted secondary text), and `val_color` (prominent primary text).

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string

def render(ws, anchor: str, *, title: str = "Monthly Sales", value: float = 279275, pct_change: float = 0.067, theme: str = "dark", **kwargs) -> None:
    """
    Renders a styled dashboard KPI card with automatic trend arrows.
    """
    col_str, row = coordinate_from_string(anchor)
    col_idx = column_index_from_string(col_str)
    
    # Theme configuration
    if theme == "dark":
        bg_color = "222222" # Dark card background
        title_color = "A0A0A0" # Muted secondary text
        val_color = "FFFFFF" # Primary bright text
    else:
        bg_color = "F3F4F6"
        title_color = "6B7280"
        val_color = "111827"
        
    title_cell = ws.cell(row=row, column=col_idx)
    val_cell = ws.cell(row=row+1, column=col_idx)
    pct_cell = ws.cell(row=row+1, column=col_idx+2)
    
    # Insert data
    title_cell.value = title
    val_cell.value = value
    pct_cell.value = pct_change
    
    # Setup card layout dimensions
    ws.merge_cells(start_row=row, start_column=col_idx, end_row=row, end_column=col_idx+2)
    ws.merge_cells(start_row=row+1, start_column=col_idx, end_row=row+1, end_column=col_idx+1)
    
    # Apply "Card" background styling
    fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    for r in range(row, row+2):
        for c in range(col_idx, col_idx+3):
            ws.cell(row=r, column=c).fill = fill
            
    # Apply typography
    title_cell.font = Font(name="Segoe UI", size=10, color=title_color)
    title_cell.alignment = Alignment(horizontal="left", vertical="top")
    
    val_cell.font = Font(name="Segoe UI", size=18, bold=True, color=val_color)
    val_cell.alignment = Alignment(horizontal="left", vertical="center")
    val_cell.number_format = "#,##0"
    
    pct_cell.font = Font(name="Segoe UI", size=11, bold=True)
    pct_cell.alignment = Alignment(horizontal="right", vertical="center")
    
    # Apply Custom Number Format for automatic dynamic arrows and coloring
    # Format architecture: [Positive]; [Negative]; [Zero]
    pct_cell.number_format = '[Color10]▲ 0.0%;[Color3]▼ -0.0%;"-"'
```
```