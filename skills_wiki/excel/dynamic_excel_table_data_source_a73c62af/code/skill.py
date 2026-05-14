from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter, coordinate_from_string, column_index_from_string

def render(ws, anchor: str, *, data: list[list] = None, table_name: str = "RawData", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a 2D list of data into the worksheet and wraps it in a dynamic Excel Table.
    This ensures downstream Pivot Tables auto-update when new rows are appended.
    """
    # Default dataset mimicking an e-commerce sales export
    if data is None:
        data = [
            ["Date", "Channel", "Department", "Sales Rep", "Revenue"],
            ["2023-12-14", "Online", "Dept 1", 13, 874],
            ["2023-12-15", "Offline", "Dept 1", 47, 820],
            ["2023-12-16", "Online", "Dept 2", 19, 833],
            ["2023-12-17", "Online", "Dept 1", 45, 289],
            ["2023-12-18", "Offline", "Dept 2", 28, 671],
            ["2023-12-19", "Online", "Dept 3", 21, 272],
            ["2023-12-20", "Online", "Dept 2", 49, 440]
        ]

    if not data or not data[0]:
        return

    # Determine starting coordinates
    coords = coordinate_from_string(anchor)
    start_col = column_index_from_string(coords[0])
    start_row = coords[1]
    
    # Write data to worksheet
    for r_idx, row in enumerate(data):
        for c_idx, value in enumerate(row):
            ws.cell(row=start_row + r_idx, column=start_col + c_idx, value=value)
            
    # Calculate end row and col for the table reference
    end_row = start_row + len(data) - 1
    end_col = start_col + len(data[0]) - 1
    ref = f"{anchor}:{get_column_letter(end_col)}{end_row}"
    
    # Initialize Table Object
    tab = Table(displayName=table_name, ref=ref)
    
    # Map high-level themes to Excel's native TableStyle presets
    style_map = {
        "corporate_blue": "TableStyleMedium9",
        "tech_green": "TableStyleMedium11",
        "sunset_orange": "TableStyleMedium10",
        "minimalist_gray": "TableStyleMedium1",
        "bold_red": "TableStyleMedium3"
    }
    style_name = style_map.get(theme, "TableStyleMedium9")
    
    # Configure Table Style (Banded rows, standard formatting)
    style = TableStyleInfo(
        name=style_name, 
        showFirstColumn=False,
        showLastColumn=False, 
        showRowStripes=True, 
        showColumnStripes=False
    )
    tab.tableStyleInfo = style
    
    # Register the table into the worksheet
    ws.add_table(tab)
    
    # Auto-fit column widths heuristically based on the inserted data
    for c_idx in range(start_col, end_col + 1):
        col_letter = get_column_letter(c_idx)
        max_len = 0
        for r_idx in range(start_row, end_row + 1):
            val = str(ws.cell(row=r_idx, column=c_idx).value or "")
            if len(val) > max_len:
                max_len = len(val)
        # Add padding to account for the auto-filter dropdown arrows in the header
        ws.column_dimensions[col_letter].width = max_len + 4
