### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dark Mode Toggle Sheet

* **Tier**: sheet_shell
* **Core Mechanism**: Implements a UI toggle to switch a worksheet between light and dark modes. While the video uses a VBA/ActiveX Toggle Button, this implementation adapts the pattern to use pure-Excel Data Validation (a dropdown) linked to conditional formatting rules. This provides the exact same UX without requiring macros.
* **Applicability**: Best used in dashboards, large data tables, or reporting tools where users may prefer a low-glare dark theme for extended reading or aesthetic preference.

### 2. Structural Breakdown

- **Data Layout**: A dedicated "Theme Mode" toggle cell (e.g., `B2`) situated above the main data table. A title row that is excluded from the conditional formatting to maintain its distinct styling.
- **Formula Logic**: Conditional formatting uses the formula `=$B$2="Dark"` applied across the table ranges.
- **Visual Design**: Dark mode applies a deep blue/grey background (`#203764`) with white font for the table body, and a slightly lighter dark hue (`#2F5597`) for the headers to preserve visual hierarchy.
- **Charts/Tables**: Applies to standard cell ranges (simulating a table) to allow maximum formatting flexibility.
- **Theme Hooks**: Primary dark backgrounds, contrasting text colors, and an accent color for the static title bar.

### 3. Reproduction Code

