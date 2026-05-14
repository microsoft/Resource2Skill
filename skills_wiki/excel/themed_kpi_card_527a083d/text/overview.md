### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed KPI Card

* **Tier**: component
* **Core Mechanism**: Creates a visually distinct KPI (Key Performance Indicator) card by merging a block of cells, applying a deep background color from the theme, and using prominent, contrasting typography. While the video demonstrates this using floating shapes, doing this via cell merging is the robust programmatic equivalent that ensures layout stability across all Excel versions without relying on fragile drawing XML. 
* **Applicability**: Best used at the top of management dashboards to highlight core metrics (e.g., Revenue, Market Share). It breaks the monotony of standard data grids by acting as a highly visible "widget".

### 2. Structural Breakdown

- **Data Layout**: A 3x3 block of cells originating from the `anchor`. Rows are merged horizontally. Top row holds the Title, middle row holds the Primary Value, and the bottom row holds the Secondary/Badge Value.
- **Formula Logic**: Directly accepts static strings or formula references (e.g., `"=B2"`) passed in via kwargs to link the card to underlying data.
- **Visual Design**: Uses a solid background fill (primary color) with white/light text. Hierarchical typography is applied: 12pt regular for the title, 22pt bold for the main number, and 12pt italic for the secondary metric. Row heights are dynamically expanded to give the card "breathing room".
- **Charts/Tables**: None.
- **Theme Hooks**: Uses `primary` for the card's background and border, and `text_light` (usually white) for the typography.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def render(ws, anchor: str, *, title: str = "Asia", main_value: str = "$369,989", sub_value: str = "5% Market Share", theme: str = "corporate_blue", **kwargs) -> None:
    # Theme palette fallback
    palettes = {
        "corporate_blue": {"primary": "002060", "text_light": "FFFFFF", "accent": "0070C0"},
        "modern_dark": {"primary": "262626", "text_light": "FFFFFF", "accent": "00B050"},
        "vibrant_navy": {"primary": "0A2540", "text_light": "FFFFFF", "accent": "635BFF"}
    }
    palette = palettes.get(theme, palettes["corporate_blue"])

    col = ws[anchor].column
    row = ws[anchor].row

    # Define card dimensions
    card_width = 3  # Spans 3 columns
    card_height = 3 # Spans 3 rows

    # Setup hierarchical typography and content
    content = [
        (title, Font(size=12, color=palette["text_light"], bold=False), Alignment(horizontal="center", vertical="center")),
        (main_value, Font(size=22, color=palette["text_light"], bold=True), Alignment(horizontal="center", vertical="center")),
        (sub_value, Font(size=12, color=palette["text_light"], italic=True), Alignment(horizontal="center", vertical="center"))
    ]

    # Style definitions
    fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    border_color = Side(style="medium", color=palette["primary"])

    # Apply styles, merges, and borders
    for r_offset in range(card_height):
        current_row = row + r_offset
        start_col_letter = get_column_letter(col)
        end_col_letter = get_column_letter(col + card_width - 1)

        # Merge the horizontal slice for the current text element
        ws.merge_cells(f"{start_col_letter}{current_row}:{end_col_letter}{current_row}")
        target_cell = ws.cell(row=current_row, column=col)

        # Inject text and typography
        text, font, alignment = content[r_offset]
        target_cell.value = text
        target_cell.font = font
        target_cell.alignment = alignment

        # Apply block formatting to ensure the "card" looks like a single unified shape
        for c_offset in range(card_width):
            c = ws.cell(row=current_row, column=col + c_offset)
            c.fill = fill
            
            # Determine outer borders to create a crisp bounding box
            top = border_color if r_offset == 0 else None
            bottom = border_color if r_offset == card_height - 1 else None
            left = border_color if c_offset == 0 else None
            right = border_color if c_offset == card_width - 1 else None
            c.border = Border(top=top, bottom=bottom, left=left, right=right)

    # Adjust row heights to simulate the padding of a shape
    ws.row_dimensions[row].height = 20     # Title spacing
    ws.row_dimensions[row + 1].height = 35 # Main value spacing
    ws.row_dimensions[row + 2].height = 20 # Sub value spacing
```