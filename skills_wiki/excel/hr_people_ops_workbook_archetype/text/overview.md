# HR People-Ops Workbook Archetype

Builds a complete engineering people-ops workbook with `Headcount`, `Org Tree`,
`Comp Analysis`, and `Insights Dashboard` sheets. The mechanism is a live data
model first and a dashboard second: 80 realistic employee rows feed XLOOKUP /
COUNTIF / MINIFS / MAXIFS / MEDIAN/FILTER formulas, then the dashboard charts
read from formula-backed analysis tables.

Use this as the workbook spine for HR roster, headcount planning, engineering
org review, compensation compression, and manager-span analysis briefs. After
applying, adapt labels or add task-specific callouts with grounded
`execute_xlsx_code`; do not replace formula cells with copied literals.
