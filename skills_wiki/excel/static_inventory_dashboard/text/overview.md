# Inventory Dashboard

Single-sheet inventory tracker with conditional formatting on stock-level columns (red < 10, yellow < 25, green ≥ 25), VLOOKUP for product names, and a donut chart for category distribution. Demonstrates a tight 12-row × 6-col layout that fits on screen without scrolling.

## Cells of interest
- B2:G2 — KPI tiles (Total SKUs, Reorder Count, Out-of-Stock, Avg DOS)
- B4:G16 — main inventory table with conditional fill
- I4:O14 — donut chart by category