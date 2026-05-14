from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.shape import Shape
from openpyxl.drawing.text import Paragraph, RichText, TextBody, CharacterProperties, Font as DrawingFont
from openpyxl.utils.units import EMU_per_cm
from openpyxl import Workbook


# Mock get_theme_colors - in a real setup, this would be imported from skills_library.excel._helpers
def get_theme_colors(theme_name):
    """Returns a dictionary of theme-specific colors."""
    if theme_name == "corporate_blue":
        return {
            "primary_dark": "000080",  # Navy
            "text_light": "FFFFFF",  # White
            "text_dark": "000000",  # Black
            "fill_light": "FFFFFF"
        }
    # Default/fallback colors
    return {
        "primary_dark": "000080",
        "text_light": "FFFFFF",
        "text_dark": "000000",
        "fill_light": "FFFFFF"
    }


def render(ws, anchor: str, *, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a visual KPI card with shapes, mimicking the tutorial's design.

    Note: openpyxl does not support dynamic linking of shape text to cell values
    (e.g., using '=$B$2' directly in the shape's formula bar as shown in the video).
    This code simulates the visual appearance by setting static text content
    within the shapes based on the current values of the linked cells.
    To make it dynamic, you would need to implement a mechanism to re-read
    cell values and update shape text programmatically, or use VBA.
    Grouping of shapes is also an interactive Excel feature not directly supported
    by openpyxl for arbitrary shapes.

    Args:
        ws: The worksheet object to render on.
        anchor: The top-left cell where the KPI card should be placed (e.g., "D2").
        theme: The name of the theme to use for colors.
        **kwargs:
            region_name_cell (str): Cell reference for the region name (e.g., "A2").
            revenue_cell (str): Cell reference for the revenue value (e.g., "B2").
            market_share_cell (str): Cell reference for the market share value (e.g., "C2").
    """
    colors = get_theme_colors(theme)

    # Get values from linked cells
    # Provide sensible defaults if kwargs are missing to make the component runnable
    region_name = ws[kwargs.get("region_name_cell", "A2")].value
    revenue = ws[kwargs.get("revenue_cell", "B2")].value
    market_share = ws[kwargs.get("market_share_cell", "C2")].value

    # Format values as seen in the video
    region_str = str(region_name) if region_name else "Region"
    revenue_str = f"{revenue:,.0f}" if isinstance(revenue, (int, float)) else f"{revenue if revenue is not None else 'N/A'}"
    market_share_str = f"{market_share:.0%}" if isinstance(market_share, (int, float)) else f"{market_share if market_share is not None else 'N/A'}"

    # Define shape properties
    card_width_cm = 4.5
    card_height_cm = 2.5
    oval_size_cm = 1.3
    oval_offset_right_cm = 0.5
    oval_offset_bottom_cm = 0.5

    # 1. Main KPI Card (Rounded Rectangle)
    main_shape = Shape.create_rounded_rectangle()
    main_shape.width = EMU_per_cm * card_width_cm
    main_shape.height = EMU_per_cm * card_height_cm
    main_shape.fill = PatternFill(start_color=colors["primary_dark"], end_color=colors["primary_dark"], fill_type="solid")
    main_shape.border.noFill = True

    # RichText for main shape
    text_body_main = TextBody()
    # Character properties
    cp_region = CharacterProperties(latin=DrawingFont(typeface='Calibri', sz=1800), b=True, solidFill=colors["text_light"])
    cp_revenue = CharacterProperties(latin=DrawingFont(typeface='Calibri', sz=1100), b=True, solidFill=colors["text_light"])
    
    # Paragraph properties for centering
    # <a:pPr algn="ctr"/> is the XML representation for center alignment
    pp_center = Paragraph.from_xml('<a:pPr algn="ctr"/>')

    p_region_name = Paragraph(pPr=pp_center)
    p_region_name.add_run(RichText(t=region_str, rPr=cp_region))
    text_body_main.append(p_region_name)

    p_revenue_label = Paragraph(pPr=pp_center)
    p_revenue_label.add_run(RichText(t="Revenue", rPr=cp_revenue))
    text_body_main.append(p_revenue_label)

    p_revenue_value = Paragraph(pPr=pp_center)
    p_revenue_value.add_run(RichText(t=revenue_str, rPr=cp_revenue))
    text_body_main.append(p_revenue_value)

    main_shape.text = text_body_main


    # 2. Market Share Indicator (Oval)
    oval_shape = Shape.create_oval()
    oval_shape.width = EMU_per_cm * oval_size_cm
    oval_shape.height = EMU_per_cm * oval_size_cm
    oval_shape.fill = PatternFill(start_color=colors["fill_light"], end_color=colors["fill_light"], fill_type="solid")
    oval_shape.border.noFill = True

    # RichText for oval shape
    text_body_oval = TextBody()
    cp_market_share = CharacterProperties(latin=DrawingFont(typeface='Calibri', sz=1100), b=True, solidFill=colors["text_dark"])
    p_market_share_val = Paragraph(pPr=pp_center)
    p_market_share_val.add_run(RichText(t=market_share_str, rPr=cp_market_share))
    text_body_oval.append(p_market_share_val)
    oval_shape.text = text_body_oval

    # Positioning
    # Anchor shapes relative to the specified cell using its 0-indexed row/column.
    anchor_col_idx = ws[anchor].col_idx - 1  # 0-indexed
    anchor_row_idx = ws[anchor].row - 1      # 0-indexed

    # Main shape anchor (top-left of the bounding box)
    main_shape.anchor.col = anchor_col_idx
    main_shape.anchor.colOff = 0
    main_shape.anchor.row = anchor_row_idx
    main_shape.anchor.rowOff = 0

    # Oval shape anchor (offset from the main shape's top-left)
    oval_shape.anchor.col = anchor_col_idx
    oval_shape.anchor.colOff = main_shape.width - oval_shape.width - (EMU_per_cm * oval_offset_right_cm)
    oval_shape.anchor.row = anchor_row_idx
    oval_shape.anchor.rowOff = main_shape.height - oval_shape.height - (EMU_per_cm * oval_offset_bottom_cm)

    ws.add_shape(main_shape)
    ws.add_shape(oval_shape)


# Example usage (for testing this component)
if __name__ == '__main__':
    wb = Workbook()
    ws = wb.active
    ws.title = "KPI Dashboard"

    # Setup some dummy data
    ws["A1"] = "Region"
    ws["B1"] = "Revenue"
    ws["C1"] = "Market Share"
    ws["A2"] = "Asia"
    ws["B2"] = 369989
    ws["C2"] = 0.05
    ws["A3"] = "Australia and Oceania"
    ws["B3"] = 899454
    ws["C3"] = 0.12
    ws["A4"] = "Central America and the Caribbean"
    ws["B4"] = 1034818
    ws["C4"] = 0.13

    # Render a KPI card for Asia
    render(
        ws,
        "E2",
        region_name_cell="A2",
        revenue_cell="B2",
        market_share_cell="C2",
        theme="corporate_blue"
    )

    # Render a KPI card for Australia and Oceania slightly below
    render(
        ws,
        "E6", # Anchor offset to avoid overlap
        region_name_cell="A3",
        revenue_cell="B3",
        market_share_cell="C3",
        theme="corporate_blue"
    )

    wb.save("kpi_dashboard_example.xlsx")
    print("KPI example saved to kpi_dashboard_example.xlsx")
