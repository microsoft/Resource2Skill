### 1. High-level Skill Pattern Extraction

> **Skill Name**: Keyboard-Driven Cell Formatting and Dynamic Linking

*   **Tier**: component
*   **Core Mechanism**: This skill demonstrates how to efficiently apply consistent formatting (e.g., number formats, cell fill, font styles, borders) and paste specific data (values vs. formulas) across multiple cells or ranges, primarily using keyboard shortcuts for selection, navigation, and special paste operations. It also covers dynamically linking cells and employing absolute/relative cell referencing (anchoring with F4) to build flexible and robust spreadsheet logic.
*   **Applicability**: This skill is essential for professionals in finance, business, and data analysis who need to quickly create, update, and standardize complex Excel models or reports. It significantly speeds up workflow, reduces manual errors, and ensures visual consistency, particularly when working with large or evolving datasets where precision and efficiency are paramount.

### 2. Structural Breakdown

-   **Data Layout**:
    *   Source cells are set up with initial data (percentage, number) and comprehensive formatting.
    *   Destination ranges are defined for applying formats and pasting values.
    *   An assumption "switch" cell is created to demonstrate dynamic linking.
-   **Formula Logic**:
    *   Cell linking: `= <source_cell_reference>` (e.g., `=E20`).
    *   Anchoring: `F4` key cycles through `$E$20`, `E$20`, `$E20` referencing, making parts of the reference absolute. In code, this is directly set in the formula string.
    *   Percentage calculation (example from video): `= (Current_Year_Revenue / Previous_Year_Revenue) - 1`.
-   **Visual Design**:
    *   **Cell Background Color**: Achieved via `Alt+H+H` (e.g., blue for source format, orange for source value, yellow for input switches).
    *   **Borders**: Applied using `Alt+H+B+O` (bottom border) or `Alt+H+B+S` (outside borders).
    *   **Font**: `Ctrl+B` for bold, `Ctrl+I` for italicize, `Alt+H+F+C` for font color (e.g., white for headers, green for linked cells from other sheets).
    *   **Number Formatting**: `Alt+H+P` for percentage, `Ctrl+,` (comma) to add decimals, `Ctrl+.` (period) to remove decimals. `Alt+H+N` followed by navigating with arrow keys to choose general number formats.
    *   **Alignment**: `Alt+H+A+C` for middle alignment.
-   **Charts/Tables**: Not explicitly demonstrated in the context of this skill, but the formatting principles apply.
-   **Theme Hooks**: Colors for cell fills (e.g., `HEADER_BG`, `ACCENT`, "FFF2CC" for inputs) and font colors (e.g., white text on dark backgrounds, black text on light backgrounds) are driven by a simplified theme palette.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.styles.colors import Color
from openpyxl.utils import get_column_letter

# Assume a helper for themes, mimicking the _helpers.py from other skills
class ThemeColors:
    HEADER_BG = "4472C4"  # A shade of blue
    ACCENT = "ED7D31"     # A shade of orange

def _get_theme_colors(theme: str):
    # This is a simplified helper. In a real setup, it would load from theme presets.
    return ThemeColors()

def render(ws, anchor: str, *, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Demonstrates efficient cell formatting and dynamic linking using common practices.
    This function sets properties directly via openpyxl to represent the *result*
    of using keyboard shortcuts for formatting, pasting special, and linking.

    Args:
        ws: The worksheet to render on.
        anchor: The top-left cell where the component should be rendered (e.g., "A1").
        theme: The visual theme to use for colors.
    """
    colors = _get_theme_colors(theme)
    start_col_idx = openpyxl.utils.column_index_from_string(anchor.split('R')[0] if 'R' in anchor else anchor[0])
    start_row_idx = int(anchor[len(openpyxl.utils.get_column_letter(start_col_idx)):])

    # --- Setup Source Cells for demonstration ---
    # Source for Format (Percentage)
    source_format_cell = ws.cell(row=start_row_idx + 1, column=start_col_idx)
    source_format_cell.value = 0.1954
    source_format_cell.number_format = '0.0%'
    source_format_cell.fill = PatternFill(start_color=colors.HEADER_BG, end_color=colors.HEADER_BG, fill_type="solid")
    source_format_cell.font = Font(color=Color("FFFFFF"), bold=True)
    source_format_cell.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    source_format_cell.alignment = Alignment(horizontal='center', vertical='center')

    # Source for Value (Number)
    source_value_cell = ws.cell(row=start_row_idx + 3, column=start_col_idx)
    source_value_cell.value = 88988
    source_value_cell.number_format = '#,##0'
    source_value_cell.fill = PatternFill(start_color=colors.ACCENT, end_color=colors.ACCENT, fill_type="solid")
    source_value_cell.font = Font(color=Color("FFFFFF"), bold=True)
    source_value_cell.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    source_value_cell.alignment = Alignment(horizontal='center', vertical='center')

    # Simulate an input cell (for dynamic linking)
    input_switch_cell = ws.cell(row=start_row_idx + 7, column=start_col_idx + 1)
    input_switch_cell.value = 1
    input_switch_cell.number_format = '0'
    input_switch_cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    input_switch_cell.alignment = Alignment(horizontal='center', vertical='center')
    input_switch_cell.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

    # --- Labels for demonstration ---
    ws.cell(row=start_row_idx, column=start_col_idx).value = "Source Format Cell (19.54%)"
    ws.cell(row=start_row_idx + 2, column=start_col_idx).value = "Source Value Cell (88,988)"
    ws.cell(row=start_row_idx + 6, column=start_col_idx).value = "Input Switch:"
    ws.cell(row=start_row_idx + 8, column=start_col_idx).value = "Linked (F4)"
    ws.cell(row=start_row_idx + 9, column=start_col_idx).value = "Format Destination"
    ws.cell(row=start_row_idx + 10, column=start_col_idx).value = "Value Destination"
    ws.cell(row=start_row_idx + 11, column=start_col_idx).value = "Dynamic Link Demo"
    ws.cell(row=start_row_idx + 12, column=start_col_idx).value = "F2 Check"


    # --- Simulate Paste Special (Formats) ---
    # Result of Ctrl+C (source_format_cell), Alt+E+S+T
    formats_dest_start_col = start_col_idx + 3
    for col_offset in range(4): # 4 cells to the right
        dest_cell = ws.cell(row=start_row_idx + 9, column=formats_dest_start_col + col_offset)
        dest_cell.number_format = source_format_cell.number_format
        dest_cell.fill = source_format_cell.fill
        dest_cell.font = source_format_cell.font
        dest_cell.border = source_format_cell.border
        dest_cell.alignment = source_format_cell.alignment
        dest_cell.value = 0.05 + col_offset * 0.03 # Just some values to show format applies

    # --- Simulate Paste Special (Values) ---
    # Result of Ctrl+C (source_value_cell), Alt+E+S+V
    values_dest_start_col = start_col_idx + 3
    for col_offset in range(4): # 4 cells to the right
        dest_cell = ws.cell(row=start_row_idx + 10, column=values_dest_start_col + col_offset)
        dest_cell.value = source_value_cell.value + col_offset * 1000 # Add some value for distinction
        dest_cell.number_format = source_value_cell.number_format # Copy number format explicitly
        dest_cell.fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid") # Neutral fill
        dest_cell.alignment = Alignment(horizontal='center', vertical='center')

    # --- Simulate Dynamic Linking with Anchoring ---
    # Result of typing '=', then Ctrl+Up/Right to input_switch_cell, then F4
    linked_cell_col = start_col_idx + 3
    linked_cell_row = start_row_idx + 8

    # Formula that links to the input switch.
    # The anchoring ($) is manually added here to represent the F4 key action.
    ws.cell(row=linked_cell_row, column=linked_cell_col).value = "=$%s$%d" % (get_column_letter(input_switch_cell.column), input_switch_cell.row)
    ws.cell(row=linked_cell_row, column=linked_cell_col).number_format = '0'
    ws.cell(row=linked_cell_row, column=linked_cell_col).font = Font(color=Color("0000FF"), bold=True) # Blue font for links
    ws.cell(row=linked_cell_row, column=linked_cell_col).alignment = Alignment(horizontal='center', vertical='center')

    # --- Check Cell Links (F2) Demo ---
    # Represents selecting a cell and pressing F2 to see linked cells highlighted.
    # Openpyxl doesn't "simulate" F2, but we can set the formula that F2 would reveal.
    # The description of F2's function is in the structural breakdown.
    ws.cell(row=start_row_idx + 12, column=start_col_idx + 3).value = '=E%d * 2' % (start_row_idx + 11)
    ws.cell(row=start_row_idx + 12, column=start_col_idx + 3).comment = openpyxl.comments.Comment("Select this cell and press F2 to see linked cells", "Skill Distiller")


    # --- General Formatting ---
    ws.column_dimensions[get_column_letter(start_col_idx)].width = 25
    ws.column_dimensions[get_column_letter(start_col_idx + 1)].width = 10
    ws.column_dimensions[get_column_letter(start_col_idx + 2)].width = 5 # Spacer
    for col_offset in range(4):
        ws.column_dimensions[get_column_letter(formats_dest_start_col + col_offset)].width = 15

    # Hide gridlines (Result of Alt+W+V+G)
    ws.sheet_view.showGridLines = False
```