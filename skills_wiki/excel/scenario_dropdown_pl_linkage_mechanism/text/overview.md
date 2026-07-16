# Scenario Dropdown P&L Linkage Mechanism

Use this mechanism when one visible control should drive many forecast or P&L
numbers. Put a small scenario selector near the top of an Inputs or Dashboard
sheet, constrain it with Excel data validation, and make downstream rows
reference that selector through `CHOOSE`, `INDEX/MATCH`, or `XLOOKUP`.
`CHOOSE` is compact when the workbook has exactly three stable cases such as
Base, Bull, and Bear. `INDEX/MATCH` is better when scenarios are stored in a
table that analysts may extend or reorder.

The clean pattern is to separate assumptions from calculations. Keep scenario
labels and driver values in a small assumptions table, expose one selector
cell, and let the model rows pull the active driver. For dashboards, reference
the calculated output rows rather than duplicating formulas in cards or charts.
This preserves auditability: a reviewer can inspect one control and understand
why all revenue, margin, and opex outputs changed.

Pitfalls: named ranges can break or point at stale sheets after aggressive
renaming, so prefer absolute sheet-qualified references in generated
workbooks. Avoid circular references where the selector depends on an output
that itself depends on the selector. If you use numeric selector values
(`1,2,3`) for `CHOOSE`, label them clearly so users do not confuse the control
with a business metric. If you use text labels, `INDEX/MATCH` or `XMATCH` is
usually more readable than nested `IF`.

This page is reference material. Adapt the snippet into the workbook you are
building; do not use it as a complete workbook template.
