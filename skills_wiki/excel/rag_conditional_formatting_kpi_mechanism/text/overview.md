# RAG Conditional Formatting KPI Mechanism

Use this mechanism when an executive dashboard needs immediate red, amber, and
green signals while preserving the underlying numeric values. The robust
pattern is to store actual, target, and variance in adjacent cells, then apply
conditional formatting to the status or value cell. Formula rules are the most
explicit and easiest to audit. Color scales are useful for dense tables or
sensitivity grids where gradients are meaningful. Icon sets can work for
simple scorecards, but they are harder to control in generated workbooks and
can be less legible after PDF rendering.

Different KPIs need different threshold direction. Revenue, margin, and NPS
are typically higher-is-better. Churn, burn multiple, defect rate, and latency
are lower-is-better. Do not reuse one threshold formula across all metrics
unless the status code already normalizes direction. For board-style workbooks,
make the rule logic visible in helper columns or notes so reviewers understand
why a metric is red or green.

Pitfalls: percentage formatting is locale-sensitive when users type values,
but formulas should still store percentages as numbers such as `0.08`, not
strings such as `"8%"`. Use absolute references for global thresholds and
relative row references for row-wise KPI rules. Conditional formatting ranges
should start on the same row as the formulas inside the rule; otherwise a rule
like `$D2="Green"` may evaluate against the wrong row.

This page is a mechanism reference. Copy the rule pattern into your workbook’s
dashboard or summary sheet; do not use it as a full workbook template.
