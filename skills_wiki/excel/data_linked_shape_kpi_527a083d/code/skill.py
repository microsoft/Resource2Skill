from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.units import cm_to_EMU
from openpyxl.drawing.xdr import XDRPoint2D, XDRPositiveSize2D, XDROneCellAnchor, XDRCellPos
from openpyxl.drawing.shapes import Shape, GraphicalProperties, PresetGeometry2D
from openpyxl.drawing.fill import SolidFill
from openpyxl.drawing.text import (
    TextBody,
    Paragraph,
    CharacterProperties,
    LatinFont,
    Field,
    HorizontalAlignment,
    VerticalAlignment,
    TextRun
)
import uuid
import re

# Helper function to get theme colors (simplified for this example)
def get_theme_colors(theme_name):
    if theme_name == "corporate_blue":
        return {
            "header_bg": "FF0F2B50",  # Navy dark blue from video
            "text_on_dark": "FFFFFFFF",  # White
            "accent_fill": "FFFFFFFF",  # White for market share circle
            "text_on_light": "FF000000",  # Black
        }
    # Default fallback
    return get_theme_colors("corporate_blue")

def _create_text_run(text, font_size, font_color, bold=False):
    rpr = CharacterProperties(
        solidFill=SolidFill(color=font_color),
        b=bold,
        sz=font_size * 100,  # size in 100ths of a point
        latin=LatinFont(typeface="Calibri")
    )
    return TextRun(rpr=rpr, t=text)

def _create_field_run(cell_ref, font_size, font_color, bold=False):
    rpr = CharacterProperties(
        solidFill=SolidFill(color=font_color),
        b=bold,
        sz=font_size * 100,
        latin=LatinFont(typeface="Calibri")
    )
    # The 't' attribute of Field needs the formula string (e.g., "='Sheet1'!B2")
    return Field(id=str(uuid.uuid4()), t=cell_ref, rpr=rpr)


def render(ws, anchor: str, *, title: str, revenue_cell: str, market_share_cell: str, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a custom data-linked KPI card using shapes in an Excel worksheet.

    Args:
        ws: The openpyxl worksheet object.
        anchor: The top-left cell where the KPI should be anchored (e.g., "E2").
        title: The main title for the KPI (e.g., "Asia").
        revenue_cell: The cell reference for the main revenue value (e.g., "B2").
        market_share_cell: The cell reference for the market share value (e.g., "C2").
        theme: The name of the theme to use for colors (default: "corporate_blue").
        **kwargs: Additional keyword arguments (not used in this skill).
    """
    theme_palette = get_theme_colors(theme)

    # Parse anchor cell to get 0-indexed column and row for XDRCellPos
    col_letter_match = re.match(r"[A-Z]+", anchor)
    col_str = col_letter_match.group(0) if col_letter_match else "A"
    row_num_match = re.match(r"\d+", anchor[len(col_str):])
    row_num = int(row_num_match.group(0)) if row_num_match else 1

    anchor_col_idx = ws.column_dimensions[col_str].column_numeric - 1  # 0-indexed column
    anchor_row_idx = row_num - 1  # 0-indexed row

    # Shape dimensions
    main_shape_width_cm = 6.5
    main_shape_height_cm = 3.5
    oval_size_cm = 1.5

    main_shape_width_emu = cm_to_EMU(main_shape_width_cm)
    main_shape_height_emu = cm_to_EMU(main_shape_height_cm)
    oval_size_emu = cm_to_EMU(oval_size_cm)

    # --- Main KPI Background Shape (Rounded Rectangle) ---
    main_kpi_shape = Shape(
        geom=PresetGeometry2D(prst='roundRect'),
        spPr=GraphicalProperties(
            fill=SolidFill(color=theme_palette["header_bg"])
        )
    )

    # TextBody for the main KPI shape
    text_body_main = TextBody(
        bodyPr=TextBody.BodyProperties(
            vert="horz", wrap="square", anchor="t",  # Top vertical alignment
            tIns=cm_to_EMU(0.2), lIns=cm_to_EMU(0.2), rIns=cm_to_EMU(0.2), bIns=cm_to_EMU(0.2), # Padding
        ),
        lstStyle=None
    )

    # Paragraph for the main title (e.g., "Asia") - centered, large, bold
    p_title = Paragraph(pPr=Paragraph.ParagraphProperties(horzAlign=HorizontalAlignment.CENTER))
    p_title.rLst.append(_create_text_run(title, 18, theme_palette["text_on_dark"], bold=True))
    text_body_main.pLst.append(p_title)

    # Empty paragraph for spacing
    text_body_main.pLst.append(Paragraph())

    # Paragraph for "Revenue" label - left-aligned, small, bold
    p_revenue_label = Paragraph(pPr=Paragraph.ParagraphProperties(horzAlign=HorizontalAlignment.LEFT))
    p_revenue_label.rLst.append(_create_text_run("Revenue", 11, theme_palette["text_on_dark"], bold=True))
    text_body_main.pLst.append(p_revenue_label)

    # Paragraph for Revenue value - linked to cell, left-aligned, small, bold
    p_revenue_value = Paragraph(pPr=Paragraph.ParagraphProperties(horzAlign=HorizontalAlignment.LEFT))
    # Cell reference for Field requires the sheet name if not on the same sheet.
    p_revenue_value.rLst.append(_create_field_run(f"='{ws.title}'!{revenue_cell}", 11, theme_palette["text_on_dark"], bold=True))
    text_body_main.pLst.append(p_revenue_value)

    main_kpi_shape.text_frame = text_body_main
    main_kpi_shape.width = main_shape_width_emu
    main_kpi_shape.height = main_shape_height_emu

    # Create and add the main KPI shape to the worksheet
    main_shape_one_cell_anchor = XDROneCellAnchor()
    main_shape_one_cell_anchor.from_ = XDRCellPos(col=anchor_col_idx, colOff=0, row=anchor_row_idx, rowOff=0)
    main_shape_one_cell_anchor.ext = XDRPositiveSize2D(main_shape_width_emu, main_shape_height_emu)
    main_shape_one_cell_anchor.graphic.graphicData.uri = "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing"
    main_shape_one_cell_anchor.graphic.graphicData.addChild(main_kpi_shape)
    ws.add_drawing(main_shape_one_cell_anchor)

    # --- Secondary KPI Shape (Oval) ---
    secondary_kpi_shape = Shape(
        geom=PresetGeometry2D(prst='ellipse'),
        spPr=GraphicalProperties(
            fill=SolidFill(color=theme_palette["accent_fill"]),  # White fill
            ln=None  # No outline
        )
    )

    # TextBody for the secondary KPI shape (market share)
    text_body_secondary = TextBody(
        pLst=[
            # Market share value - linked to cell, centered, small, bold
            Paragraph(pPr=Paragraph.ParagraphProperties(horzAlign=HorizontalAlignment.CENTER),
                      rLst=[_create_field_run(f"='{ws.title}'!{market_share_cell}", 11, theme_palette["text_on_light"], bold=True)]
                     )
        ],
        bodyPr=TextBody.BodyProperties(
            vert="horz", wrap="square", anchor="ctr",  # Center aligned
            lIns=0, tIns=0, rIns=0, bIns=0  # No padding
        ),
        lstStyle=None
    )
    secondary_kpi_shape.text_frame = text_body_secondary
    secondary_kpi_shape.width = oval_size_emu
    secondary_kpi_shape.height = oval_size_emu

    # Calculate offset for the oval to place it in the bottom-right corner of the main shape
    # These offsets are relative to the anchor cell's top-left corner
    oval_col_offset_emu = main_shape_width_emu - oval_size_emu - cm_to_EMU(0.5)
    oval_row_offset_emu = main_shape_height_emu - oval_size_emu - cm_to_EMU(0.5)

    # Create and add the secondary KPI shape to the worksheet
    secondary_shape_one_cell_anchor = XDROneCellAnchor()
    secondary_shape_one_cell_anchor.from_ = XDRCellPos(col=anchor_col_idx, colOff=oval_col_offset_emu, row=anchor_row_idx, rowOff=oval_row_offset_emu)
    secondary_shape_one_cell_anchor.ext = XDRPositiveSize2D(oval_size_emu, oval_size_emu)
    secondary_shape_one_cell_anchor.graphic.graphicData.uri = "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing"
    secondary_shape_one_cell_anchor.graphic.graphicData.addChild(secondary_kpi_shape)
    ws.add_drawing(secondary_shape_one_cell_anchor)

    # Note: Programmatic grouping of shapes (XDROneCellAnchor objects) in openpyxl is complex
    # and not directly exposed via simple high-level APIs. The shapes are placed individually
    # and can be manually grouped in Excel if desired, as demonstrated in the tutorial.

