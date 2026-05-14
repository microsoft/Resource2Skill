from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.cell_range import CellRange

def render(ws, anchor: str, *, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Groups a range of rows to create an outline for better navigation and applies
    basic themed styling to the header of the grouped section.

    Args:
        ws: The worksheet to render on.
        anchor: The top-left cell of the header for the grouped section (e.g., "A20").
                The rows to be grouped will start from the row *below* this anchor.
        theme: The color theme for styling (default: "corporate_blue").
        **kwargs: Additional keyword arguments (not used in this specific skill).
    """
    anchor_cell = ws[anchor]
    header_row_idx = anchor_cell.row

    # Define the range for grouping (example: 20 rows of content below the header)
    # The actual grouped rows will be from header_row_idx + 1 to header_row_idx + 20
    group_min_row = header_row_idx + 1
    group_max_row = header_row_idx + 20 

    # Apply Excel's grouping feature (Alt+A+G+G in manual usage)
    ws.row_dimensions.group(min=group_min_row, max=group_max_row, outline_level=1)

    # Apply header styling mimicking the video's example (dark blue background, white bold text)
    # Theme palette simulation - in a real framework, this would be loaded from a theme helper
    if theme == "corporate_blue":
        header_bg_color = "002F4B"  # Dark Blue
        header_text_color = "FFFFFF"  # White
        border_color = "000000"     # Black
    else: # Default to corporate_blue if theme is not recognized
        header_bg_color = "002F4B"
        header_text_color = "FFFFFF"
        border_color = "000000"

    # Set header cell value and merge it across a few columns for visual appeal
    header_cell.value = "Income Statement" # Example header text
    ws.merge_cells(start_row=header_row_idx, start_column=anchor_cell.column, 
                   end_row=header_row_idx, end_column=anchor_cell.column + 5) # Span 6 columns

    header_cell.fill = PatternFill(start_color=header_bg_color, end_color=header_bg_color, fill_type="solid")
    header_cell.font = Font(color=header_text_color, bold=True, size=12)
    header_cell.alignment = Alignment(horizontal="left", vertical="center") # Align left as seen in video

    # Add a thin bottom border to the header row
    thin_border_side = Side(style='thin', color=border_color)
    for col_idx in range(anchor_cell.column, anchor_cell.column + 6):
        ws.cell(row=header_row_idx, column=col_idx).border = Border(bottom=thin_border_side)

    # Populate example data in the grouped rows (simplified for demonstration)
    data_labels = ["Revenue", "% growth", "EBIT", "% of sales", "Taxes", "% of EBIT", "Net Income"]
    years = [2013, 2014, 2015, 2016, 2017]
    
    # Fill in year headers
    for i, year in enumerate(years):
        ws.cell(row=header_row_idx, column=anchor_cell.column + 1 + i, value=year)
        ws.cell(row=header_row_idx, column=anchor_cell.column + 1 + i).font = Font(color=header_text_color, bold=True)
        ws.cell(row=header_row_idx, column=anchor_cell.column + 1 + i).fill = PatternFill(start_color=header_bg_color, end_color=header_bg_color, fill_type="solid")
        ws.cell(row=header_row_idx, column=anchor_cell.column + 1 + i).alignment = Alignment(horizontal="center", vertical="center")


    # Populate labels and some sample values in the grouped rows
    for i, label in enumerate(data_labels):
        current_row = group_min_row + i
        ws.cell(row=current_row, column=anchor_cell.column, value=label).font = Font(bold=True)
        for j, year_val in enumerate(years):
            col_offset = anchor_cell.column + 1 + j
            # Simplified data for demonstration
            if label == "Revenue":
                ws.cell(row=current_row, column=col_offset, value=70000 + j * 10000 + i * 500)
            elif label == "% growth":
                ws.cell(row=current_row, column=col_offset, value=0.15 + j * 0.01)
                ws.cell(row=current_row, column=col_offset).number_format = '0.0%' # Percentage format
            elif label == "EBIT":
                ws.cell(row=current_row, column=col_offset, value=10000 + j * 1500 + i * 100)
            elif label == "% of sales":
                ws.cell(row=current_row, column=col_offset, value=0.10 + j * 0.005)
                ws.cell(row=current_row, column=col_offset).number_format = '0.0%' # Percentage format
            elif label == "Taxes":
                ws.cell(row=current_row, column=col_offset, value=2000 + j * 300 + i * 50)
            elif label == "% of EBIT":
                ws.cell(row=current_row, column=col_offset, value=0.20 + j * 0.01)
                ws.cell(row=current_row, column=col_offset).number_format = '0.0%' # Percentage format
            elif label == "Net Income": # This would be the last row before new section, assuming end_row points here
                ws.cell(row=current_row, column=col_offset, value=8000 + j * 1000 + i * 50)
            
            # Apply italic to percentage rows as seen in the video
            if "%" in label:
                ws.cell(row=current_row, column=col_offset).font = Font(italic=True)

    # Example of removing gridlines from the entire sheet (as seen in video)
    # This is a worksheet-level setting, often done once for the whole workbook.
    ws.sheet_view.showGridLines = False

    # Example of adjusting column width for specific columns for overall aesthetic
    ws.column_dimensions['A'].width = 5 # Narrow column A for spacing
