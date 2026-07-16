from __future__ import annotations

import math
import random
from datetime import date, timedelta
from statistics import median

from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo


ACCENT = "1F4E78"
ACCENT2 = "70AD47"
WARN = "FFC000"
DANGER = "C00000"
LIGHT = "F3F6FA"
BORDER = Side(style="thin", color="D9E2F3")


def reset_workbook(wb):
    for ws in list(wb.worksheets):
        wb.remove(ws)


def style_header(ws, row=1):
    fill = PatternFill("solid", fgColor=ACCENT)
    font = Font(color="FFFFFF", bold=True)
    for cell in ws[row]:
        if cell.value is not None:
            cell.fill = fill
            cell.font = font
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = Border(bottom=BORDER)


def autosize(ws, max_width=28):
    for col in ws.columns:
        letter = get_column_letter(col[0].column)
        width = max(len(str(c.value)) if c.value is not None else 0 for c in col[:120])
        ws.column_dimensions[letter].width = min(max(width + 2, 10), max_width)
    ws.freeze_panes = "A2"


def add_table(ws, name, ref):
    table = Table(displayName=name, ref=ref)
    style = TableStyleInfo(
        name="TableStyleMedium2",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False,
    )
    table.tableStyleInfo = style
    ws.add_table(table)


def title(ws, text, width=8):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=width)
    c = ws.cell(1, 1, text)
    c.font = Font(size=18, bold=True, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor=ACCENT)
    c.alignment = Alignment(horizontal="center")
    ws.row_dimensions[1].height = 26


def render_hr(wb, title_text="Engineering People Ops Workbook"):
    random.seed(42)
    reset_workbook(wb)
    teams = ["Platform", "Infra", "ML", "Frontend", "Data", "Security", "SRE", "DX"]
    locations = ["SEA", "NYC", "LON", "remote"]
    levels = ["L3", "L4", "L5", "L6", "L7", "L8"]
    first = ["Alex", "Riley", "Jordan", "Taylor", "Morgan", "Casey", "Sam", "Avery"]
    last = ["Chen", "Patel", "Nguyen", "Smith", "Garcia", "Kim", "Brown", "Davis"]
    ws = wb.create_sheet("Headcount")
    headers = ["employee_id", "full_name", "level", "manager_id", "team", "hire_date", "location", "comp_band", "equity_vesting_pct", "gender_pay_gap_proxy"]
    ws.append(headers)
    manager_ids = []
    for i in range(1, 81):
        emp = f"E{i:03d}"
        if i <= 8:
            level = "L7" if i < 8 else "L8"
            manager = ""
            manager_ids.append(emp)
        else:
            level = random.choices(levels[:4], weights=[20, 30, 30, 20])[0]
            manager = random.choice(manager_ids)
        base = {"L3": 180000, "L4": 220000, "L5": 270000, "L6": 330000, "L7": 390000, "L8": 450000}[level]
        ws.append([
            emp,
            f"{random.choice(first)} {random.choice(last)}",
            level,
            manager,
            teams[(i - 1) % len(teams)],
            date(2018, 1, 1) + timedelta(days=random.randint(0, 2900)),
            random.choice(locations),
            base + random.randint(-15000, 20000),
            round(random.uniform(0.05, 1.0), 2),
            round(random.uniform(-0.06, 0.06), 3),
        ])
    style_header(ws)
    for row in ws.iter_rows(min_row=2, min_col=6, max_col=9):
        row[0].number_format = "yyyy-mm-dd"
        row[2].number_format = "$#,##0"
        row[3].number_format = "0%"
    add_table(ws, "HeadcountTable", "A1:J81")
    autosize(ws)

    org = wb.create_sheet("Org Tree")
    org.append(["employee_id", "employee", "manager_id", "manager_name", "level", "team", "reporting_depth", "indented_view"])
    for r in range(2, 82):
        org.append([
            f"=Headcount!A{r}", f"=Headcount!B{r}", f"=Headcount!D{r}",
            f'=IF(C{r}="","CEO",XLOOKUP(C{r},Headcount!A:A,Headcount!B:B,""))',
            f"=Headcount!C{r}", f"=Headcount!E{r}", f'=IF(C{r}="",0,1+COUNTIF(Headcount!D:D,A{r}))',
            f'=REPT("  ",G{r})&B{r}',
        ])
    style_header(org)
    autosize(org)

    comp = wb.create_sheet("Comp Analysis")
    comp.append(["team", "headcount", "min_comp", "median_proxy", "max_comp", "avg_gap_proxy", "compression_flag"])
    for i, team in enumerate(teams, 2):
        comp.append([
            team,
            f'=COUNTIF(Headcount!E:E,A{i})',
            f'=MINIFS(Headcount!H:H,Headcount!E:E,A{i})',
            f'=MEDIAN(FILTER(Headcount!H:H,Headcount!E:E=A{i}))',
            f'=MAXIFS(Headcount!H:H,Headcount!E:E,A{i})',
            f'=AVERAGEIF(Headcount!E:E,A{i},Headcount!J:J)',
            f'=IF(E{i}-C{i}<60000,"Compression","OK")',
        ])
    style_header(comp)
    for row in comp.iter_rows(min_row=2, min_col=3, max_col=5):
        for cell in row:
            cell.number_format = "$#,##0"
    for cell in comp["F"][1:]:
        cell.number_format = "0.0%"
    comp.conditional_formatting.add("G2:G9", CellIsRule(operator="equal", formula=['"Compression"'], fill=PatternFill("solid", fgColor="F4CCCC")))
    autosize(comp)

    dash = wb.create_sheet("Insights Dashboard", 0)
    title(dash, title_text, width=10)
    dash["A3"] = "Executive Callouts"
    dash["A3"].font = Font(bold=True, size=14)
    callouts = [
        "80 engineers across 8 teams",
        "L7/L8 management layer isolated for span review",
        "Comp compression flagged where spread < $60k",
        "Remote and NYC concentration tracked for planning",
        "Equity vesting mix highlights retention risk",
    ]
    for i, text in enumerate(callouts, 4):
        dash[f"A{i}"] = text
    team_chart = BarChart()
    team_chart.title = "Headcount by Team"
    team_chart.add_data(Reference(comp, min_col=2, min_row=1, max_row=9), titles_from_data=True)
    team_chart.set_categories(Reference(comp, min_col=1, min_row=2, max_row=9))
    team_chart.height = 8
    team_chart.width = 15
    dash.add_chart(team_chart, "D3")
    loc = wb.create_sheet("_LocationData")
    loc.sheet_state = "hidden"
    loc.append(["location", "headcount"])
    for loc_name in locations:
        loc.append([loc_name, f'=COUNTIF(Headcount!G:G,A{loc.max_row + 1})'])
    pie = PieChart()
    pie.title = "Headcount by Location"
    pie.add_data(Reference(loc, min_col=2, min_row=1, max_row=5), titles_from_data=True)
    pie.set_categories(Reference(loc, min_col=1, min_row=2, max_row=5))
    dash.add_chart(pie, "D20")
    autosize(dash)


def render_battery(wb, title_text="Battery Characterisation Analysis"):
    random.seed(42)
    reset_workbook(wb)
    meta = wb.create_sheet("Cell_Metadata")
    meta.append(["cell_id", "chemistry", "nominal_capacity_mAh", "manufacturer", "build_date"])
    chem = ["NMC811", "LFP", "NCA", "LMO"]
    for i in range(1, 9):
        meta.append([f"CELL-{i:02d}", chem[i % 4], 3000 + i * 80, f"Vendor {chr(64+i)}", date(2025, 1, 1) + timedelta(days=i * 11)])
    style_header(meta)
    autosize(meta)

    raw = wb.create_sheet("Raw_Cycles")
    raw.append(["cycle_idx", "cell_id", "charge_capacity_mAh", "discharge_capacity_mAh", "coulombic_efficiency", "internal_resistance_mOhm", "end_voltage_V", "ambient_temp_C"])
    for cycle in range(1, 101):
        cell = f"CELL-{((cycle - 1) % 8) + 1:02d}"
        fade = 1 - 0.03 * (cycle - 1) / 99
        nominal = 3000 + (((cycle - 1) % 8) + 1) * 80
        discharge = nominal * fade + random.gauss(0, 14)
        charge = discharge / random.uniform(0.992, 0.999)
        raw.append([cycle, cell, charge, discharge, discharge / charge, 38 + cycle * 0.045 + random.gauss(0, 0.9), 4.18 - cycle * 0.0007 + random.gauss(0, 0.008), 25 + random.gauss(0, 1.2)])
    style_header(raw)
    for row in raw.iter_rows(min_row=2, min_col=3, max_col=8):
        for cell in row:
            cell.number_format = "0.00"
        row[2].number_format = "0.00%"
    add_table(raw, "RawCyclesTable", "A1:H101")
    autosize(raw)

    derived = wb.create_sheet("Derived_Metrics")
    derived.append(["cycle_idx", "cell_id", "rolling_avg_capacity_mAh", "normalised_capacity_pct", "fade_rate_pct_from_cycle_1"])
    for r in range(2, 102):
        derived.append([
            f"=Raw_Cycles!A{r}", f"=Raw_Cycles!B{r}",
            f"=AVERAGE(FILTER(Raw_Cycles!D:D,(Raw_Cycles!B:B=B{r})*(Raw_Cycles!A:A>=A{r}-4)*(Raw_Cycles!A:A<=A{r})))",
            f'=Raw_Cycles!D{r}/XLOOKUP(B{r}&1,Raw_Cycles!B:B&Raw_Cycles!A:A,Raw_Cycles!D:D)',
            f"=1-D{r}",
        ])
    style_header(derived)
    for cell in list(derived["D"])[1:] + list(derived["E"])[1:]:
        cell.number_format = "0.00%"
    autosize(derived)

    plot = wb.create_sheet("Summary_Plots", 0)
    title(plot, title_text, width=8)
    line = LineChart()
    line.title = "Capacity vs Cycle"
    line.y_axis.title = "mAh"
    line.x_axis.title = "Cycle"
    line.add_data(Reference(raw, min_col=4, min_row=1, max_row=101), titles_from_data=True)
    line.set_categories(Reference(raw, min_col=1, min_row=2, max_row=101))
    line.height = 9
    line.width = 17
    plot.add_chart(line, "A3")
    hist = BarChart()
    hist.title = "Internal Resistance Trend"
    hist.add_data(Reference(raw, min_col=6, min_row=1, max_row=101), titles_from_data=True)
    hist.set_categories(Reference(raw, min_col=1, min_row=2, max_row=101))
    hist.height = 9
    hist.width = 17
    plot.add_chart(hist, "A22")
    autosize(plot)


def render_sales(wb, title_text="B2B SaaS Sales Pipeline Tracker"):
    random.seed(42)
    reset_workbook(wb)
    reps = wb.create_sheet("Reps")
    reps.append(["rep_id", "rep_name", "quota", "region", "hire_date"])
    regions = ["West", "East", "EMEA", "Central"]
    for i in range(1, 9):
        reps.append([f"R{i:02d}", f"Rep {i}", 900000 + i * 65000, regions[i % 4], date(2022, 1, 1) + timedelta(days=i * 80)])
    style_header(reps)
    for cell in reps["C"][1:]:
        cell.number_format = "$#,##0"
    autosize(reps)

    accounts = wb.create_sheet("Accounts")
    industries = ["Fintech", "Healthcare", "Retail", "AI Infra", "Manufacturing"]
    accounts.append(["account_id", "account_name", "industry", "ICP_tier", "expansion_potential"])
    for i in range(1, 31):
        accounts.append([f"A{i:03d}", f"Account {i}", random.choice(industries), random.choice(["A", "B", "C"]), random.choice(["High", "Medium", "Low"])])
    style_header(accounts)
    autosize(accounts)

    deals = wb.create_sheet("Deals")
    stages = ["Prospect", "Qualify", "Propose", "Negotiate", "Closed-Won", "Closed-Lost"]
    probs = {"Prospect": 0.1, "Qualify": 0.25, "Propose": 0.5, "Negotiate": 0.75, "Closed-Won": 1.0, "Closed-Lost": 0.0}
    deals.append(["deal_id", "account_name", "owner", "stage", "created_date", "expected_close", "ARR_amount", "probability_pct", "last_activity_date", "next_step"])
    for i in range(1, 81):
        stage = random.choices(stages, weights=[18, 18, 22, 18, 14, 10])[0]
        created = date(2026, 1, 1) + timedelta(days=random.randint(0, 150))
        deals.append([f"D{i:04d}", f"Account {random.randint(1,30)}", f"Rep {random.randint(1,8)}", stage, created, created + timedelta(days=random.randint(20, 120)), random.randint(25000, 360000), probs[stage], created + timedelta(days=random.randint(1, 25)), random.choice(["Security review", "Exec sponsor", "Pricing", "Pilot success", "Procurement"])])
    style_header(deals)
    for row in deals.iter_rows(min_row=2, min_col=5, max_col=8):
        row[0].number_format = "yyyy-mm-dd"
        row[1].number_format = "yyyy-mm-dd"
        row[2].number_format = "$#,##0"
        row[3].number_format = "0%"
    add_table(deals, "DealsTable", "A1:J81")
    autosize(deals)

    forecast = wb.create_sheet("Forecast", 0)
    title(forecast, title_text, width=8)
    forecast.append(["month", "weighted_pipeline", "closed_won", "quota", "attainment"])
    for m in range(1, 7):
        row = m + 2
        forecast.append([
            date(2026, m, 1),
            f'=SUMPRODUCT((MONTH(Deals!F$2:F$81)={m})*(Deals!G$2:G$81)*(Deals!H$2:H$81))',
            f'=SUMIFS(Deals!G:G,Deals!D:D,"Closed-Won",Deals!F:F,">="&A{row},Deals!F:F,"<"&EDATE(A{row},1))',
            1300000,
            f"=C{row}/D{row}",
        ])
    style_header(forecast, 2)
    for row in forecast.iter_rows(min_row=3, min_col=2, max_col=4):
        for cell in row:
            cell.number_format = "$#,##0"
    for cell in forecast["E"][2:]:
        cell.number_format = "0%"
    forecast.conditional_formatting.add("E3:E8", CellIsRule(operator="lessThan", formula=["0.8"], fill=PatternFill("solid", fgColor="F4CCCC")))
    chart = BarChart()
    chart.title = "Weighted Pipeline by Month"
    chart.add_data(Reference(forecast, min_col=2, min_row=2, max_row=8), titles_from_data=True)
    chart.set_categories(Reference(forecast, min_col=1, min_row=3, max_row=8))
    chart.height = 8
    chart.width = 15
    forecast.add_chart(chart, "G3")

    heat = wb.create_sheet("Activity Heatmap")
    heat.append(["rep"] + [f"week_{i}" for i in range(1, 9)])
    for i in range(1, 9):
        heat.append([f"Rep {i}"] + [random.randint(8, 34) for _ in range(8)])
    style_header(heat)
    heat.conditional_formatting.add("B2:I9", ColorScaleRule(start_type="min", start_color="FCE4D6", mid_type="percentile", mid_value=50, mid_color="FFE699", end_type="max", end_color="70AD47"))
    autosize(heat)


def render_cfo(wb, title_text="Board-Ready CFO Scenario Workbook"):
    random.seed(42)
    reset_workbook(wb)
    inputs = wb.create_sheet("Inputs")
    inputs.append(["input", "value", "notes"])
    rows = [
        ["ARR_baseline", 24000000, "$24M ARR baseline"],
        ["monthly_growth_base", 0.055, "base case"],
        ["gross_margin", 0.68, "usage-based infra blended margin"],
        ["sales_marketing_pct", 0.22, "of revenue"],
        ["rd_pct", 0.28, "of revenue"],
        ["g_and_a_pct", 0.12, "of revenue"],
    ]
    for row in rows:
        inputs.append(row)
    style_header(inputs)
    for cell in inputs["B"][1:]:
        if isinstance(cell.value, float):
            cell.number_format = "0.0%"
        else:
            cell.number_format = "$#,##0"
    autosize(inputs)

    revenue = wb.create_sheet("Revenue Build")
    revenue.append(["month", "base_revenue", "upside_revenue", "downside_revenue"])
    for m in range(1, 13):
        row = m + 1
        revenue.append([
            date(2026, m, 1),
            f"=Inputs!B2/12*(1+Inputs!B3)^{m-1}",
            f"=B{row}*1.18",
            f"=B{row}*0.82",
        ])
    style_header(revenue)
    for row in revenue.iter_rows(min_row=2, min_col=2, max_col=4):
        for cell in row:
            cell.number_format = "$#,##0"
    autosize(revenue)

    cost = wb.create_sheet("Cost Model")
    cost.append(["month", "revenue", "COGS", "sales_marketing", "R&D", "G&A", "operating_income"])
    for m in range(1, 13):
        row = m + 1
        cost.append([
            f"=Revenue Build!A{row}",
            f"='Revenue Build'!B{row}",
            f"=B{row}*(1-Inputs!B4)",
            f"=B{row}*Inputs!B5",
            f"=B{row}*Inputs!B6",
            f"=B{row}*Inputs!B7",
            f"=B{row}-SUM(C{row}:F{row})",
        ])
    style_header(cost)
    for row in cost.iter_rows(min_row=2, min_col=2, max_col=7):
        for cell in row:
            cell.number_format = "$#,##0"
    autosize(cost)

    matrix = wb.create_sheet("Scenario Matrix")
    matrix.append(["scenario", "FY revenue", "gross profit", "op income", "status"])
    for i, scen in enumerate(["Base", "Upside", "Downside"], 2):
        col = {"Base": "B", "Upside": "C", "Downside": "D"}[scen]
        matrix.append([scen, f"=SUM('Revenue Build'!{col}2:{col}13)", f"=B{i}*Inputs!B4", f'=CHOOSE(MATCH(A{i},{{"Base","Upside","Downside"}},0),SUM(\'Cost Model\'!G2:G13),SUM(\'Cost Model\'!G2:G13)*1.35,SUM(\'Cost Model\'!G2:G13)*0.55)', f'=IF(D{i}>0,"Green",IF(D{i}>-2500000,"Yellow","Red"))'])
    style_header(matrix)
    for row in matrix.iter_rows(min_row=2, min_col=2, max_col=4):
        for cell in row:
            cell.number_format = "$#,##0"
    autosize(matrix)

    dash = wb.create_sheet("KPI Dashboard", 0)
    title(dash, title_text, width=10)
    dash["A3"] = "Base FY Revenue"
    dash["B3"] = "='Scenario Matrix'!B2"
    dash["B3"].number_format = "$#,##0"
    dash["A4"] = "Base Op Income"
    dash["B4"] = "='Scenario Matrix'!D2"
    dash["B4"].number_format = "$#,##0"
    line = LineChart()
    line.title = "Monthly Revenue Trend"
    line.add_data(Reference(revenue, min_col=2, min_row=1, max_row=13), titles_from_data=True)
    line.set_categories(Reference(revenue, min_col=1, min_row=2, max_row=13))
    line.height = 8
    line.width = 16
    dash.add_chart(line, "D3")
    bars = BarChart()
    bars.title = "Scenario Comparison"
    bars.add_data(Reference(matrix, min_col=2, min_row=1, max_row=4), titles_from_data=True)
    bars.set_categories(Reference(matrix, min_col=1, min_row=2, max_row=4))
    dash.add_chart(bars, "D20")
    summary = wb.create_sheet("Board Summary")
    summary.append(["callout", "detail"])
    for row in [
        ["Growth", "Base case compounds from a $24M ARR run-rate with upside/downside stress."],
        ["Margin", "Gross margin assumption is centralized in Inputs for live board sensitivity."],
        ["Spend", "COGS and opex roll forward from revenue, not static copied values."],
        ["Decision", "Scenario Matrix uses live formulas for board-ready tradeoff discussion."],
    ]:
        summary.append(row)
    style_header(summary)
    autosize(summary)
    autosize(dash)
