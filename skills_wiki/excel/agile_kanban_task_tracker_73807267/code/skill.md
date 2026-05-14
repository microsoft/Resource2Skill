### 1. High-level Skill Pattern Extraction

> **Skill Name**: Agile Kanban Task Tracker

* **Tier**: sheet_shell
* **Core Mechanism**: Creates a single-sheet task board with distinct categorical sections (e.g., "Backlog", "In Progress"). It uses a dynamic `=SUBTOTAL(9, OFFSET(current, 1, 0):OFFSET(next, -1, 0))` formula for section headers. This allows users to physically drag and drop rows between sections (using Shift+Drag) while keeping all category totals perfectly accurate without formula adjustments. It also features drop-downs, conditional formatting tags, and an in-cell `REPT` progress bar.
* **Applicability**: Best for project management dashboards, sprint trackers, or any scenario where items are manually moved through a pipeline of stages and continuous aggregation (hours, points, costs) per stage is required.

### 2. Structural Breakdown

- **Data Layout**: 
  - Top header row with overall project stats.
  - Column headers: Type, Role, Task Description, Priority, Est. Days, Actual Days.
  - Section Headers acting as category dividers and subtotal containers.
  - Task rows nested between Section Headers.
- **Formula Logic**: 
  - Dynamic Block Sum: `=SUBTOTAL(9, OFFSET(F6, 1, 0):OFFSET(F10, -1, 0))` (Sums exactly the rows between the current section header and the next one).
  - In-cell Progress Bar: `=REPT("■", INT(H2*10)) & REPT("□", 10 - INT(H2*10))` based on completion percentage.
- **Visual Design**: 
  - Distinct background colors for section headers to separate blocks.
  - Conditional formatting on the "Type" and "Priority" columns to create pill-like colored tags.
- **Charts/Tables**: Standard ranges (not Excel Tables) to allow for easier row drag-and-drop mechanics between arbitrary header blocks.
- **Theme Hooks**: Uses `primary` for main headers, `secondary` for section dividers, and specific semantic colors (red/yellow/green) for conditional formatting tags.

### 3. Reproduction Code

