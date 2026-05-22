```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Scenario Switcher

* **Tier**: component
* **Core Mechanism**: Creates a Data Validation dropdown to select an active scenario by index (1, 2, 3...). A primary "Live Case" table uses the `CHOOSE` function to dynamically pull assumption values from multiple scenario tables below. It implements the standard financial modeling convention: blue font for hardcoded inputs, black font for formulas.
* **Applicability**: Highly applicable for financial models, forecasting, and budgeting where analysts need to quickly toggle between multiple sets of assumptions (e.g., "Base", "Upside", and "Downside" cases) without losing data.

### 2. Structural Breakdown

- **Data Layout**: A master dropdown cell (index) at the top. A "Live Case" table directly below it. Sequentially stacked scenario tables (Scenario 1, Scenario 2, etc.) at the bottom.
- **Formula Logic**: `=CHOOSE($dropdown_index, scenario_1_cell, scenario_2_cell, ...)` applied across the entire Live Case table grid.
- **Visual Design**: The dropdown selector uses a light yellow fill (`FFF2CC`) and a solid border to indicate an input control cell. Hardcoded inputs in scenario tables are styled with `0000FF` (blue), while the live dynamic cells are `000000` (black).
- **Charts/Tables**: Standard spreadsheet data layout with bottom-bordered column headers. 
- **Theme Hooks**: Default modeling conventions utilized over specific thematic colors to strictly enforce the "Blue = Hardcoded, Black = Formula" standard.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils.cell import coordinate_to_tuple

def render(ws, anchor: str, *,
           line_items: list[str] = ["Number of Orders", "Average Order Value", "Manufacturing Cost", "Order Fulfillment"],
           periods: list[str] = ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"],
           scenarios: list[str] = ["Base Case", "Optimistic", "Pessimistic"],
           theme: str = "corporate_blue",
           **kwargs) -> None:
    
    start_row, start_col = coordinate_to_tuple(anchor)
    
    # 1. Dropdown Cell (Scenario Index)
    ws.cell(row=start_row, column=start_col, value="Active Scenario:").font = Font(bold=True)
    dropdown_cell = ws.cell(row=start_row, column=start_col + 1)
    dropdown_cell.value = 1
    # Standard input cell highlight
    dropdown_cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    dropdown_cell.border = Border(
        left=Side(style="thin", color="000000"),
        right=Side(style="thin", color="000000"),
        top=Side(style="thin", color="000000"),
        bottom=Side(style="thin", color="000000")
    )
    dropdown_cell.alignment = Alignment(horizontal="center")
    
    # Add Data Validation (List of 1, 2, 3...)
    indices = ",".join(str(i+1) for i in range(len(scenarios)))
    dv = DataValidation(type="list", formula1=f'"{indices}"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(dropdown_cell)
    
    # 2. Helper to build individual grid sections
    def build_section(start_r, title, is_live=False, scenario_idx=0):
        # Title
        title_cell = ws.cell(row=start_r, column=start_col, value=title)
        title_cell.font = Font(bold=True, italic=not is_live, color="000000" if is_live else "808080")
        
        # Headers
        for i, period in enumerate(periods):
            c = ws.cell(row=start_r + 1, column=start_col + 1 + i, value=period)
            c.font = Font(bold=True)
            c.alignment = Alignment(horizontal="center")
            c.border = Border(bottom=Side(style="thin", color="000000"))
            
        # Line Items
        item_coords = []
        for i, item in enumerate(line_items):
            r = start_r + 2 + i
            ws.cell(row=r, column=start_col, value=item)
            
            row_coords = []
            for j in range(len(periods)):
                c_idx = start_col + 1 + j
                cell = ws.cell(row=r, column=c_idx)
                if not is_live:
                    # Mock hardcoded base assumptions for the scenario grids
                    val = (scenario_idx + 1) * 1500 + (i * 25) + (j * 100)
                    cell.value = val
                    # Financial modeling convention: Blue for hardcoded inputs
                    cell.font = Font(color="0000FF") 
                row_coords.append(cell.coordinate)
            item_coords.append(row_coords)
            
        return item_coords

    table_height = 2 + len(line_items) + 1 # +1 for visual spacing
    
    # 3. Build Scenario Tables first (to obtain coordinates for the formulas later)
    scenario_block_coords = []
    
    for idx, sc_name in enumerate(scenarios):
        sc_start_row = start_row + 2 + table_height * (idx + 1)
        coords = build_section(sc_start_row, f"{sc_name} (Scenario {idx + 1})", is_live=False, scenario_idx=idx)
        scenario_block_coords.append(coords)
        
    # 4. Build Live Case Table
    live_start_row = start_row + 2
    build_section(live_start_row, "Live Case", is_live=True)
    
    # 5. Populate Live Case with CHOOSE formulas
    for i, item in enumerate(line_items):
        r = live_start_row + 2 + i
        for j in range(len(periods)):
            c_idx = start_col + 1 + j
            cell = ws.cell(row=r, column=c_idx)
            
            # Construct dynamic CHOOSE formula pointing back to the index dropdown
            refs = [sc_table[i][j] for sc_table in scenario_block_coords]
            formula = f"=CHOOSE(${dropdown_cell.column_letter}${dropdown_cell.row}, {', '.join(refs)})"
            
            cell.value = formula
            # Financial modeling convention: Black for formula-driven cells
            cell.font = Font(color="000000") 

    # Expand the label column width for readability
    ws.column_dimensions[ws.cell(row=start_row, column=start_col).column_letter].width = 25
```
```