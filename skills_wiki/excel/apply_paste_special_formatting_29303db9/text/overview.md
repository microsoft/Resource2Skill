### 1. High-level Skill Pattern Extraction

> **Skill Name**: Apply Paste Special Formatting

* **Tier**: snippet
* **Core Mechanism**: This skill transfers only the visual formatting (e.g., font, color, borders, number format) from a previously copied cell or range to a target cell or range, leaving underlying values or formulas untouched. It is executed via a specific keyboard shortcut sequence, allowing for efficient application of styles.
* **Applicability**: Essential for quickly standardizing the appearance of cells in financial models, reports, or dashboards without affecting data integrity. It ensures a professional and clean presentation, particularly useful after pasting raw data, applying conditional formatting, or when striving for consistent styling across different sections of a spreadsheet. A related powerful variation is "Paste Special Values".

### 2. Structural Breakdown

- **Data Layout**: This skill applies to any cell or range within a worksheet. It does not dictate a specific data layout but rather enables efficient manipulation of existing cell attributes.
- **Formula Logic**: Not applicable for this skill, as it focuses on cell attributes (formatting or values) rather than formula construction.
- **Visual Design**: This skill directly impacts visual design elements like cell background colors, font styles (bold, italic), borders, and number formats (e.g., percentage, currency, decimal places).
- **Charts/Tables**: This skill can be used to apply consistent formatting to data ranges that feed into charts or tables, ensuring a uniform visual appearance.
- **Theme Hooks**: While the shortcut itself doesn't directly consume theme tokens, it's used to apply formatting that might be derived from a specific theme's palette.

### 3. Reproduction Code

```python
# To apply "Paste Special (Formats)" from a copied cell/range to a target cell/range:
# 1. Copy the source cell(s) or range: Ctrl+C (on Windows) or Cmd+C (on Mac)
# 2. Select the target cell(s) or range where you want to apply the formatting.
# 3. Open the "Paste Special" dialog and select "Formats": Alt+E+S+T (on Windows)
#    (On Mac: Ctrl+Cmd+V, then select 'Formats')

# To apply "Paste Special (Values)" from a copied cell/range to a target cell/range:
# 1. Copy the source cell(s) or range: Ctrl+C (on Windows) or Cmd+C (on Mac)
# 2. Select the target cell(s) or range where you want to paste the values.
# 3. Open the "Paste Special" dialog and select "Values": Alt+E+S+V (on Windows)
#    (On Mac: Ctrl+Cmd+V, then select 'Values')

# Example of other related formatting shortcuts demonstrated in the video:
# - Bold: Ctrl+B (on Windows) or Cmd+B (on Mac)
# - Italicize: Ctrl+I (on Windows) or Cmd+I (on Mac)
# - Change to Percentage Format: Alt+H+P (on Windows)
# - Change Number Formatting (e.g., General, Currency): Alt+H+N (then navigate with arrow keys)
# - Add/Decrease Decimal Places: Ctrl+'.' (add) or Ctrl+',' (decrease) (on Windows)
# - Adjust Column Width: Alt+H+O+W (then enter width)
# - Adjust Row Height: Alt+H+O+H (then enter height)
# - Remove Gridlines: Alt+W+V+G (on Windows)
# - Align Text to Center/Middle: Alt+H+A+C (on Windows)
```