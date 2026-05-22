```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Executive Multi-Chart Dashboard Layout

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a clean visual dashboard by disabling gridlines, stashing calculation data off-screen, and generating three types of customized charts (Doughnut for KPI percentages, Line for multi-year trends, and Radar for category scoring). Explicitly styles specific chart elements (markers, lines, and slices) to form a cohesive UI without relying on floating shapes.
* **Applicability**: Ideal for executive summaries or high-level performance dashboards where multiple contrasting metrics (progress vs target, historical trends, multi-factor assessments) need to be visualized dynamically on a single, print-ready or presentation-ready sheet.

### 2. Structural Breakdown

- **Data Layout**: Off-screen data preparation (placed in column AA/27 onward) to keep the primary view completely clean for charting. 
- **Formula Logic**: Calculates "Remainder" mathematically required to generate proportion-accurate Doughnut charts for KPIs.
- **Visual Design**: Gridlines removed, strong typography applied directly to cells for titles. Fallback to a custom palette assigning dark blue, light blue, and red semantic meanings.
- **Charts/Tables**: 
  - **Doughnut Charts**: Adjusted `holeSize` to 65% for a modern look; manual injection of `DataPoint` styles to contrast complete vs. remaining sectors.
  - **Line Chart**: Custom Y-axis scaling (min/max bounding) to emphasize variance, gridlines removed, and custom circular markers added to trend lines.
  - **Radar Chart**: Used for multi-variable distribution (e.g., Customer Satisfaction attributes), styled with filled circle markers matching the primary brand color.
- **Theme Hooks**: Designed to consume `primary`, `secondary` (lighter variant for chart remainders), `accent`, and `text` from a centralized theme payload.

### 3. Reproduction Code

```python
from openpyxl.styles import Font
from openpyxl.chart import DoughnutChart, LineChart, RadarChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.chart.marker import Marker

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # Theme Configuration Hooks (Fallback values)
    primary_color = "003366"   # Dark Blue
    secondary_color = "CCDDFF" # Light Blue
    accent_color = "CC0000"    # Red
    text_color = "333333"

    # --- Data Setup (Stashed off-screen to keep the UI clean) ---
    data_col = 27 # Column AA

    # 1. KPI Data (Progress vs Remainder)
    kpi_data = [
        ("Sales", 0.85, 0.15),
        ("Profit", 0.89, 0.11),
        ("Customers", 0.87, 0.13)
    ]
    ws.cell(row=1, column=data_col, value="KPI")
    ws.cell(row=1, column=data_col+1, value="% Complete")
    ws.cell(row=1, column=data_col+2, value="Remainder")

    for r_idx, (kpi, comp, rem) in enumerate(kpi_data, start=2):
        ws.cell(row=r_idx, column=data_col, value=kpi)
        ws.cell(row=r_idx, column=data_col+1, value=comp)
        ws.cell(row=r_idx, column=data_col+2, value=rem)

    # 2. Trend Data
    trend_headers = ["Month", "2021", "2022"]
    for c_idx, h in enumerate(trend_headers):
        ws.cell(row=6, column=data_col+c_idx, value=h)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    d2021 = [201.9, 204.2, 198.6, 206.4, 209.4, 185.0, 192.4, 189.3, 195.1, 200.2, 204.3, 203.0]
    d2022 = [215.3, 217.6, 220.1, 206.4, 204.3, 200.0, 210.6, 200.6, 199.2, 201.0, 215.0, 225.8]

    for i, m in enumerate(months):
        ws.cell(row=7+i, column=data_col, value=m)
        ws.cell(row=7+i, column=data_col+1, value=d2021[i])
        ws.cell(row=7+i, column=data_col+2, value=d2022[i])

    # 3. Radar Data
    ws.cell(row=20, column=data_col, value="Category")
    ws.cell(row=20, column=data_col+1, value="Score")
    radar_cats = ["Speed", "Quality", "Hygiene", "Service", "Availability"]
    radar_scores = [54, 86, 93, 53, 95]
    for i, c in enumerate(radar_cats):
        ws.cell(row=21+i, column=data_col, value=c)
        ws.cell(row=21+i, column=data_col+1, value=radar_scores[i])


    # --- Visual Layout Configuration ---

    # Main Title
    ws['B2'] = title
    ws['B2'].font = Font(size=24, bold=True, color=primary_color)
    ws['B3'] = "Figures in millions of USD"
    ws['B3'].font = Font(size=11, color=text_color, italic=True)

    # 1. Doughnut Charts for KPIs
    def make_donut(row_idx, kpi_name):
        chart = DoughnutChart()
        labels = Reference(ws, min_col=data_col+1, min_row=1, max_col=data_col+2, max_row=1)
        data = Reference(ws, min_col=data_col+1, min_row=row_idx, max_col=data_col+2, max_row=row_idx)
        
        chart.add_data(data, titles_from_data=False)
        chart.set_categories(labels)
        chart.title = kpi_name
        chart.legend = None
        chart.holeSize = 65
        chart.width = 5.5
        chart.height = 5.5

        if len(chart.series) > 0:
            series = chart.series[0]
            # Explicitly style DataPoints for Complete vs Remainder contrast
            dp1 = DataPoint(idx=0)
            dp1.graphicalProperties.solidFill = primary_color
            dp2 = DataPoint(idx=1)
            dp2.graphicalProperties.solidFill = secondary_color
            series.dPt.append(dp1)
            series.dPt.append(dp2)
            
        return chart

    ws.add_chart(make_donut(2, "Sales"), "B5")
    ws.add_chart(make_donut(3, "Profit"), "F5")
    ws.add_chart(make_donut(4, "# of Customers"), "J5")

    # 2. Trend Line Chart
    trend_chart = LineChart()
    trend_chart.title = "2021-2022 Sales Trend"
    
    data = Reference(ws, min_col=data_col+1, min_row=6, max_col=data_col+2, max_row=18)
    cats = Reference(ws, min_col=data_col, min_row=7, max_row=18)
    trend_chart.add_data(data, titles_from_data=True)
    trend_chart.set_categories(cats)
    
    trend_chart.width = 12
    trend_chart.height = 8

    # Axis and Gridline Formatting
    trend_chart.y_axis.scaling.min = 180
    trend_chart.y_axis.scaling.max = 230
    trend_chart.y_axis.majorGridlines = None
    trend_chart.legend.position = 'b'

    if len(trend_chart.series) > 1:
        # 2021 Series (Accent styling)
        s1 = trend_chart.series[0]
        s1.graphicalProperties.line.solidFill = accent_color
        s1.marker = Marker('circle')
        s1.marker.graphicalProperties.solidFill = "FFFFFF"
        s1.marker.graphicalProperties.line.solidFill = accent_color

        # 2022 Series (Primary styling)
        s2 = trend_chart.series[1]
        s2.graphicalProperties.line.solidFill = primary_color
        s2.marker = Marker('circle')
        s2.marker.graphicalProperties.solidFill = "FFFFFF"
        s2.marker.graphicalProperties.line.solidFill = primary_color

    ws.add_chart(trend_chart, "B16")

    # 3. Radar Chart
    radar_chart = RadarChart()
    radar_chart.type = "marker"
    radar_chart.title = "Customer Satisfaction"
    
    labels = Reference(ws, min_col=data_col, min_row=21, max_row=25)
    data = Reference(ws, min_col=data_col+1, min_row=20, max_row=25)
    
    radar_chart.add_data(data, titles_from_data=True)
    radar_chart.set_categories(labels)
    radar_chart.legend = None
    radar_chart.width = 7.5
    radar_chart.height = 7.5

    if len(radar_chart.series) > 0:
        rs1 = radar_chart.series[0]
        rs1.graphicalProperties.line.solidFill = primary_color
        rs1.marker = Marker('circle')
        rs1.marker.graphicalProperties.solidFill = "FFFFFF"
        rs1.marker.graphicalProperties.line.solidFill = primary_color

    ws.add_chart(radar_chart, "I16")
```
```