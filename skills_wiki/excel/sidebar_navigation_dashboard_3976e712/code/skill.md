### 1. High-level Skill Pattern Extraction

> **Skill Name**: Sidebar Navigation Dashboard

* **Tier**: archetype
* **Core Mechanism**: Creates an app-like multi-sheet workbook architecture. It uses a narrow, dark-filled Column A as a universal sidebar across all sheets, containing hyperlink-enabled icon cells to navigate between tabs. The main content area utilizes contrasting background fills and edge-only borders to create distinct "cards" that simulate container shapes.
* **Applicability**: Ideal for interactive reports, financial models, or executive dashboards where users need to seamlessly jump between a high-level summary view, data inputs, and settings/contacts.

### 2. Structural Breakdown

- **Data Layout**: Multi-sheet structure. Column A acts as the static sidebar (width 8). Columns B-M serve as the main canvas (width 12).
- **Formula Logic**: Utilizes `cell.hyperlink = "#'Sheet Name'!A1"` to create interactive navigation buttons.
- **Visual Design**: The sidebar uses a deep primary theme color (e.g., dark blue), with the active sheet indicated by a lighter highlight fill. The dashboard background uses a light gray fill, making white "cards" visually pop.
- **Charts/Tables**: Card areas are designated for specific elements (Top row for KPIs, bottom rows for charts).
- **Theme Hooks**: Requires `sidebar_bg`, `sidebar_active`, `dash_bg`, `card_bg`, and `text_accent` (handled via fallbacks in the code).

### 3. Reproduction Code

