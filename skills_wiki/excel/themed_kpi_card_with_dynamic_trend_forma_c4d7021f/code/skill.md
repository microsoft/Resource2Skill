### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed KPI Card with Dynamic Trend Formatting

* **Tier**: component
* **Core Mechanism**: Constructs a 2-row merged grid acting as a cohesive "card" for a key metric. Uses a powerful custom Number Format string (`[Color10]▲ 0.0%;[Color3]▼ -0.0%;"-"`) to automatically inject trend arrows and colorize the variance metric without relying on complex Conditional Formatting rules.
* **Applicability**: Essential for executive summaries and dark-themed dashboards where high-level figures (like Revenue or Traffic) must be prominently displayed alongside their period-over-period performance indicators. 

### 2. Structural Breakdown

- **Data Layout**: A 2x3 cell anchor area. The top row is merged across all 3 columns for the metric title. The second row houses the main metric (merged across the first 2 columns) and the variance/trend metric resides in the 3rd column.
- **Formula Logic**: Readily accepts static floats or dynamic formula strings linking back to pivot outputs. 
- **Visual Design**: Uses a solid block pattern fill to simulate a floating UI card. Establishes visual hierarchy using heavy font-size contrast (10pt title vs 18pt value). 
- **Charts/Tables**: N/A (replaces the need for embedded text boxes, which are commonly misused in Excel dashboards).
- **Theme Hooks**: `bg_color` (card background), `title_color` (muted secondary text), and `val_color` (prominent primary text).

### 3. Reproduction Code

