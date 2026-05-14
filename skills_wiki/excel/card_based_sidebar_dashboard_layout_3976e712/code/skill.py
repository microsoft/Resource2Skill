from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a structural web-like dashboard shell featuring a hyperlinked side navigation 
    bar and a card-based main grid for dropping in KPIs and charts.
    """
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)
        
    ws.sheet_view.showGridLines = False

    # Standard UI Colors (can be mapped to a theme object in production)
    bg_color = "F0F2F5"      # Light gray canvas
    card_color = "FFFFFF"    # White cards
    sidebar_color = "1A2A3A" # Dark blue sidebar
    text_color = "333333"    # Dark gray text
    border_color = "DDDDDD"  # Subtle card border

    # 1. Fill entire visible canvas with background color
    canvas_fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    for row in ws.iter_rows(min_row=1, max_row=40, min_col=1, max_col=18):
        for cell in row:
            cell.fill = canvas_fill

    # 2. Sidebar Setup (Column A)
    sidebar_fill = PatternFill(start_color=sidebar_color, end_color=sidebar_color, fill_type="solid")
    ws.column_dimensions['A'].width = 16
    for row_idx in range(1, 41):
        ws.cell(row=row_idx, column=1).fill = sidebar_fill

    # Add Sidebar Menu Items
    menu_items = ["Dashboard", "Inputs", "Contacts", "Support"]
    for idx, item in enumerate(menu_items):
        # Ensure target sheets exist for hyperlinks to work seamlessly
        if item not in wb.sheetnames and item != "Dashboard":
            wb.create_sheet(item)
        
        cell = ws.cell(row=6 + (idx * 4), column=1, value=item.upper())
        cell.font = Font(color="FFFFFF", bold=True, size=11)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # Link to the appropriate sheet
        target = f"'{item}'!A1" if item != "Dashboard" else f"'{sheet_name}'!A1"
        cell.hyperlink = f"#{target}"

    # 3. Title Area
    ws.cell(row=2, column=3, value=title).font = Font(size=22, bold=True, color=text_color)
    ws.cell(row=3, column=3, value="Figures in millions of USD").font = Font(size=11, italic=True, color="666666")

    # 4. Grid & Spacing Configuration
    spacer_cols = ['B', 'G', 'L', 'Q']
    for col in spacer_cols:
        ws.column_dimensions[col].width = 3
        
    card_cols = ['C', 'D', 'E', 'F', 'H', 'I', 'J', 'K', 'M', 'N', 'O', 'P']
    for col in card_cols:
        ws.column_dimensions[col].width = 10

    # Helper function to draw modular visual "cards" on the grid
    thin_border = Border(
        left=Side(style='thin', color=border_color),
        right=Side(style='thin', color=border_color),
        top=Side(style='thin', color=border_color),
        bottom=Side(style='thin', color=border_color)
    )
    card_fill = PatternFill(start_color=card_color, end_color=card_color, fill_type="solid")

    def draw_card(min_col, min_row, max_col, max_row, title_text):
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = card_fill
                
                # Construct borders to outline only the outer edge of the card region
                cell.border = Border(
                    top=thin_border.top if r == min_row else None,
                    bottom=thin_border.bottom if r == max_row else None,
                    left=thin_border.left if c == min_col else None,
                    right=thin_border.right if c == max_col else None
                )
        # Apply Card Header
        ws.cell(row=min_row+1, column=min_col+1, value=title_text).font = Font(bold=True, size=12, color=text_color)

    # 5. Render Top KPI Cards (1/3 width each)
    draw_card(3, 5, 6, 12, "Regional Sales")
    draw_card(8, 5, 11, 12, "Net Profit")
    draw_card(13, 5, 16, 12, "Active Customers")

    # Insert Mock KPI Values inside the cards
    ws.cell(row=9, column=4, value="$2,544").font = Font(size=24, bold=True, color=sidebar_color)
    ws.cell(row=9, column=9, value="$890").font = Font(size=24, bold=True, color=sidebar_color)
    ws.cell(row=9, column=14, value="87.0M").font = Font(size=24, bold=True, color=sidebar_color)

    # 6. Render Bottom Content Cards (2/3 width and 1/3 width layout)
    draw_card(3, 14, 11, 30, "2021-2022 Sales Trend")
    draw_card(13, 14, 16, 30, "Customer Satisfaction")
