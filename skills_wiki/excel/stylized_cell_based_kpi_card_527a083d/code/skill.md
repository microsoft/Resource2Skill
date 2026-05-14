### 1. High-level Skill Pattern Extraction

> **Skill Name**: Stylized Cell-Based KPI Card

* **Tier**: component
* **Core Mechanism**: Translates the tutorial's shape-based KPI approach into a robust, cell-based component that natively supports dynamic openpyxl formula linking. Constructs a unified visual "card" by merging a 3x2 grid of cells, applying heavy outer borders, and utilizing contrasting theme fills to create a distinct "badge" area for percentage metrics.
* **Applicability**: Ideal for executive dashboards and summary sheets where high-level metrics (e.g., Regional Revenue & Market Share) need to stand out as designed elements rather than raw tabular data. 

### 2. Structural Breakdown

- **Data Layout**: A 3-row by 2-column cell block. The top row (Cols 1-2) is merged for the Title. The bottom right (Rows 2-3, Col 2) is merged vertically for the percentage badge.
- **Formula Logic**: Accepts direct cell reference strings (e.g., `'Data'!B2`) and prepends `=` to ensure the card remains dynamically linked to the source data, mimicking shape formula links.
- **Visual Design**: Uses a dark primary fill for the main body and a lighter accent fill for the percentage badge. Text is bold and white (`#FFFFFF`) for maximum contrast. A medium outer border unifies the separate cells into a single "shape".
- **Charts/Tables**: N/A
- **Theme Hooks**: Consumes `primary` for the card body, `accent` for the badge background, and `text` (white) for typography. 

### 3. Reproduction Code

