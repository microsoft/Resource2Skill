# Two-Variable Sensitivity Table Mechanism

Use this mechanism when stakeholders need to see how one output changes across
two input drivers. CFO scenario boards often use price versus volume, growth
versus gross margin, or churn versus expansion. The table should have one
driver across columns, one driver down rows, and a formula in each intersection
that directly recomputes the target output. This creates a transparent matrix
that survives PDF export and does not depend on Excel’s interactive data-table
recalculation behavior.

Excel’s `TABLE()` feature is powerful in the desktop app, but it is unreliable
to generate with openpyxl because the workbook calculation engine may not
recompute it until opened in Excel. For generated workbooks, direct formula
expansion is safer: each sensitivity cell references its row and column header
with mixed absolute/relative references, for example `(price - cost) * volume`.
This approach is verbose but auditable and works in LibreOffice/PDF previews.

Pitfalls: lock the fixed input references with `$` and leave row/column header
references relative in the correct dimension. Apply number formats to the
entire grid, not only the seed formula. Use a color scale only when higher is
clearly better; otherwise use explicit RAG rules. If the base-case output is
also shown elsewhere, link both to the same formula assumptions so reviewers
do not see inconsistent values.

This page demonstrates a mechanism only. Adapt the matrix to your workbook’s
own revenue, margin, or cash-flow logic.
