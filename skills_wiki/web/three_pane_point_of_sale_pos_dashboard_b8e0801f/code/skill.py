def create_component(
    output_dir: str,
    title_text: str = "System-navigator",
    body_text: str = "Billing Interface",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#3498db",     # CSS hex color for active tab
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Three-Pane POS Dashboard layout.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#121212"
        surface_color = "#1e1e1e"
        border_color = "#333333"
        text_main = "#f0f0f0"
        text_muted = "#aaaaaa"
        table_header_bg = "#2d2d2d"
        table_header_text = "#ffffff"
        input_bg = "#2a2a2a"
        danger_color = "#e74c3c"
        success_color = "#27ae60"
    else:
        bg_color = "#f4f6f9"
        surface_color = "#ffffff"
        border_color = "#dee2e6"
        text_main = "#333333"
        text_muted = "#6c757d"
        table_header_bg = "#343a40"
        table_header_text = "#ffffff"
        input_bg = "#ffffff"
        danger_color = "#e74c3c"
        success_color = "#2ecc71"

    # === CSS ===
    css = f"""/* Three-Pane POS Dashboard — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --border: {border_color};
    --text-main: {text_main};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --table-header-bg: {table_header_bg};
    --table-header-text: {table_header_text};
    --input-bg: {input_bg};
    --danger: {danger_color};
    --success: {success_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #111; /* Outer canvas background */
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.app-window {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    display: flex;
    flex-direction: column;
    border-radius: 8px;
    box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    overflow: hidden;
    border: 1px solid var(--border);
}}

/* Navbar */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    height: 60px;
    background-color: var(--surface);
    border-bottom: 1px solid var(--border);
    flex-shrink: 0;
}}

.brand {{
    font-size: 1.25rem;
    font-weight: 700;
    font-style: italic;
}}

.nav-links {{
    display: flex;
    gap: 10px;
}}

.nav-links a {{
    text-decoration: none;
    color: var(--text-main);
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: 500;
    font-size: 0.9rem;
    transition: background 0.2s;
}}

.nav-links a.active {{
    background-color: var(--accent);
    color: #fff;
}}

/* Main Dashboard Grid */
.main-content {{
    display: grid;
    grid-template-columns: 1fr 1.5fr 320px;
    gap: 15px;
    padding: 15px;
    flex: 1;
    overflow: hidden;
}}

.panel {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

/* Panel 1: Product Selection */
.search-inputs {{
    display: flex;
    gap: 10px;
    padding: 15px;
    border-bottom: 1px solid var(--border);
}}

.search-inputs input {{
    flex: 1;
    padding: 10px 12px;
    border: 1px solid var(--border);
    border-radius: 4px;
    background: var(--input-bg);
    color: var(--text-main);
    outline: none;
}}

.search-inputs input:focus {{
    border-color: var(--accent);
}}

.product-grid {{
    padding: 15px;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
    gap: 10px;
    overflow-y: auto;
    align-content: start;
}}

.grid-btn {{
    padding: 20px 10px;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    cursor: pointer;
    color: var(--text-main);
    font-weight: 500;
    transition: background 0.2s;
}}

.grid-btn:hover {{
    background: var(--border);
}}

/* Panel 2: Cart Table */
.table-container {{
    flex: 1;
    overflow-y: auto;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th {{
    background: var(--table-header-bg);
    color: var(--table-header-text);
    padding: 12px;
    text-align: left;
    position: sticky;
    top: 0;
    z-index: 10;
}}

td {{
    padding: 12px;
    border-bottom: 1px solid var(--border);
    vertical-align: middle;
}}

.qty-input {{
    width: 60px;
    padding: 6px;
    border: 1px solid var(--border);
    border-radius: 4px;
    background: var(--input-bg);
    color: var(--text-main);
}}

.delete-btn {{
    background: var(--danger);
    color: white;
    border: none;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
}}

#empty-state td {{
    text-align: center;
    padding: 60px 20px;
    color: var(--text-muted);
}}

/* Panel 3: Checkout Summary */
.checkout-panel {{
    padding: 20px;
}}

.summary-container {{
    flex: 1;
    display: flex;
    flex-direction: column;
}}

.summary-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}}

.summary-row input {{
    width: 100px;
    text-align: right;
    padding: 6px 8px;
    border: 1px solid var(--border);
    border-radius: 4px;
    background: var(--input-bg);
    color: var(--text-main);
}}

.total-divider {{
    height: 1px;
    background: var(--border);
    margin: 15px 0;
}}

.total-row {{
    font-size: 1.4rem;
    font-weight: 700;
}}

.numpad {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-top: auto;
    margin-bottom: 20px;
}}

.numpad button {{
    padding: 15px;
    font-size: 1.2rem;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--text-main);
    cursor: pointer;
    transition: background 0.1s;
}}

.numpad button:active {{
    background: var(--border);
}}

.checkout-btn {{
    width: 100%;
    padding: 16px;
    font-size: 1.2rem;
    font-weight: 700;
    background: var(--success);
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: opacity 0.2s;
}}

.checkout-btn:hover {{
    opacity: 0.9;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - POS</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-window">
        
        <header class="navbar">
            <div class="brand">{title_text}</div>
            <nav class="nav-links">
                <a href="#" class="active">{body_text}</a>
                <a href="#">Stock</a>
                <a href="#">Dashboard</a>
                <a href="#">Settings</a>
            </nav>
        </header>

        <main class="main-content">
            
            <!-- Col 1: Product Selection -->
            <section class="panel product-panel">
                <div class="search-inputs">
                    <input type="text" placeholder="Barcode (Press Enter)">
                    <input type="text" placeholder="Search by name">
                </div>
                <div class="product-grid" id="product-grid">
                    <!-- Javascript populates these -->
                </div>
            </section>

            <!-- Col 2: Current Order -->
            <section class="panel order-panel">
                <div class="table-container">
                    <table id="cart-table">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Item</th>
                                <th>Price</th>
                                <th>Qty</th>
                                <th>Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr id="empty-state">
                                <td colspan="5">
                                    <strong>No items in bill</strong><br><br>
                                    <small>Click categories on the left to add items</small>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- Col 3: Checkout -->
            <section class="panel checkout-panel">
                <div class="summary-container">
                    <div class="summary-row">
                        <span>Sub Total:</span>
                        <span id="sub-total">$0.00</span>
                    </div>
                    <div class="summary-row">
                        <span>Discount ($):</span>
                        <input type="number" id="discount-input" value="0.00" min="0" step="0.01">
                    </div>
                    <div class="summary-row">
                        <span>Cash Paid:</span>
                        <input type="number" id="cash-input" value="" placeholder="0.00">
                    </div>
                    
                    <div class="total-divider"></div>
                    
                    <div class="summary-row total-row">
                        <span>Total:</span>
                        <span id="grand-total">$0.00</span>
                    </div>
                    <div class="summary-row">
                        <span>Cash:</span>
                        <span id="cash-display">$0.00</span>
                    </div>
                    <div class="summary-row">
                        <span>Balance:</span>
                        <span id="balance-display">$0.00</span>
                    </div>

                    <div class="numpad" id="numpad">
                        <button>1</button><button>2</button><button>3</button>
                        <button>4</button><button>5</button><button>6</button>
                        <button>7</button><button>8</button><button>9</button>
                        <button>C</button><button>0</button><button>⌫</button>
                    </div>

                    <button class="checkout-btn" onclick="alert('Proceeding to checkout...')">Checkout</button>
                </div>
            </section>
        </main>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Three-Pane POS Dashboard — Interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const productGrid = document.getElementById('product-grid');
    const tbody = document.querySelector('#cart-table tbody');
    const emptyState = document.getElementById('empty-state');
    const cashInput = document.getElementById('cash-input');
    const discountInput = document.getElementById('discount-input');
    const numpad = document.getElementById('numpad');

    // Dummy product categories
    const categories = [
        "Electronics", "Footwear", "Clothing", "Home", 
        "Fashion", "Beauty", "Toys", "Sports", 
        "Automotive", "Groceries", "Furniture", "Stationery"
    ];

    // Populate grid
    categories.forEach(cat => {{
        const btn = document.createElement('button');
        btn.className = 'grid-btn';
        btn.textContent = cat;
        btn.onclick = () => addItem(cat);
        productGrid.appendChild(btn);
    }});

    // Add Item to Table
    function addItem(name) {{
        // remove empty state if present
        if (emptyState.style.display !== 'none') {{
            emptyState.style.display = 'none';
        }}

        // check if item already exists
        const existingRows = Array.from(tbody.querySelectorAll('tr:not(#empty-state)'));
        const duplicate = existingRows.find(row => row.cells[1].textContent === name);
        
        if (duplicate) {{
            const qtyInput = duplicate.querySelector('.qty-input');
            qtyInput.value = parseInt(qtyInput.value) + 1;
            updateTotals();
            return;
        }}

        const price = (Math.random() * 100 + 10).toFixed(2); // Random price
        const tr = document.createElement('tr');
        
        tr.innerHTML = `
            <td><button class="delete-btn" title="Remove">✕</button></td>
            <td>${{name}}</td>
            <td class="price-cell" data-price="${{price}}">$${{price}}</td>
            <td><input type="number" class="qty-input" value="1" min="1"></td>
            <td class="row-total">$${{price}}</td>
        `;

        // Event listeners for new row elements
        tr.querySelector('.delete-btn').addEventListener('click', () => {{
            tr.remove();
            checkEmptyState();
            updateTotals();
        }});
        
        tr.querySelector('.qty-input').addEventListener('input', updateTotals);

        tbody.appendChild(tr);
        updateTotals();
    }}

    // Ensure empty state appears when cart is empty
    function checkEmptyState() {{
        const rows = tbody.querySelectorAll('tr:not(#empty-state)');
        if(rows.length === 0) {{
            emptyState.style.display = 'table-row';
        }}
    }}

    // Calculate overall totals
    function updateTotals() {{
        let subTotal = 0;
        
        const rows = tbody.querySelectorAll('tr:not(#empty-state)');
        rows.forEach(row => {{
            const price = parseFloat(row.querySelector('.price-cell').dataset.price);
            const qty = parseInt(row.querySelector('.qty-input').value) || 0;
            const rowTotal = price * qty;
            
            row.querySelector('.row-total').textContent = '$' + rowTotal.toFixed(2);
            subTotal += rowTotal;
        }});

        const discount = parseFloat(discountInput.value) || 0;
        const finalTotal = Math.max(0, subTotal - discount);
        const cashPaid = parseFloat(cashInput.value) || 0;
        const balance = cashPaid > 0 ? (cashPaid - finalTotal) : 0;

        document.getElementById('sub-total').textContent = '$' + subTotal.toFixed(2);
        document.getElementById('grand-total').textContent = '$' + finalTotal.toFixed(2);
        document.getElementById('cash-display').textContent = '$' + cashPaid.toFixed(2);
        document.getElementById('balance-display').textContent = '$' + balance.toFixed(2);
    }}

    // Add Listeners for existing inputs
    discountInput.addEventListener('input', updateTotals);
    cashInput.addEventListener('input', updateTotals);

    // Numpad Interactivity mapping strictly to Cash Input
    numpad.addEventListener('click', (e) => {{
        if(e.target.tagName === 'BUTTON') {{
            const val = e.target.textContent;
            
            if(val === '⌫') {{
                cashInput.value = cashInput.value.slice(0, -1);
            }} else if (val === 'C') {{
                cashInput.value = '';
            }} else {{
                cashInput.value += val;
            }}
            updateTotals();
        }}
    }});
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html,
        "css": css,
        "js": js,
        "files": files,
    }
