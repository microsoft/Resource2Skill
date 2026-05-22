def create_component(
    output_dir: str,
    title_text: str = "Create Your Account",
    body_text: str = "Complete the steps below to set up your profile.",
    color_scheme: str = "dark",
    accent_color: str = "#8b5cf6",
    width_px: int = 550,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Multi-Step Progress Registration Form.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_muted_color = "#94a3b8"
        surface_color = "#1e293b"
        surface_alt_color = "#334155"
        border_color = "#475569"
    else:
        bg_color = "#f1f5f9"
        text_color = "#0f172a"
        text_muted_color = "#64748b"
        surface_color = "#ffffff"
        surface_alt_color = "#f8fafc"
        border_color = "#cbd5e1"

    css = f"""/* Multi-Step Form Component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --surface-alt: {surface_alt_color};
    --border: {border_color};
    --width: {width_px}px;
    --min-height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Inter', sans-serif;
}}

body {{
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
}}

.page-title {{
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 8px;
    text-align: center;
}}

.page-description {{
    color: var(--text-muted);
    margin-bottom: 32px;
    text-align: center;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--min-height);
    background: var(--surface);
    padding: 40px;
    border-radius: 16px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
}}

/* --- Progress Bar --- */
.progress-container {{
    position: relative;
    margin-bottom: 40px;
}}

.progress-track {{
    position: absolute;
    top: 23px; /* Center of the 50px icons */
    left: 25px; /* Offset by half icon width */
    right: 25px;
    height: 4px;
    background: var(--border);
    z-index: 1;
    border-radius: 2px;
}}

.progress-line {{
    height: 100%;
    background: var(--accent);
    width: 0%; /* Driven by JS */
    transition: width 0.4s ease;
    border-radius: 2px;
}}

.progress-bar {{
    display: flex;
    justify-content: space-between;
    list-style: none;
    position: relative;
    z-index: 2;
}}

.progress-bar li {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    width: 60px;
}}

.progress-bar .icon {{
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: var(--surface);
    border: 3px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    color: var(--text-muted);
    transition: all 0.4s ease;
}}

.progress-bar li.active .icon {{
    border-color: var(--accent);
    background: var(--accent);
    color: #fff;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
}}

.progress-bar strong {{
    font-size: 13px;
    font-weight: 500;
    color: var(--text-muted);
    transition: color 0.4s ease;
}}

.progress-bar li.active strong {{
    color: var(--text);
}}

/* --- Form Steps --- */
.form-step {{
    display: none;
    flex-grow: 1;
    animation: fadeSlideUp 0.4s ease forwards;
}}

.form-step.active {{
    display: block;
}}

@keyframes fadeSlideUp {{
    from {{ opacity: 0; transform: translateY(15px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.step-header {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 28px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--border);
}}

.step-header h2 {{
    font-size: 20px;
    font-weight: 600;
}}

.step-header span {{
    font-size: 14px;
    color: var(--text-muted);
}}

/* --- Floating Label Inputs --- */
.input-group {{
    position: relative;
    margin-bottom: 24px;
}}

.input-group input {{
    width: 100%;
    padding: 16px 14px;
    border: 1px solid var(--border);
    border-radius: 8px;
    background: transparent;
    color: var(--text);
    font-size: 15px;
    transition: all 0.3s ease;
}}

.input-group input:focus {{
    border-color: var(--accent);
    outline: none;
}}

.input-group label {{
    position: absolute;
    top: 50%;
    left: 14px;
    transform: translateY(-50%);
    background: var(--surface);
    padding: 0 4px;
    color: var(--text-muted);
    font-size: 15px;
    transition: all 0.2s ease;
    pointer-events: none;
}}

/* Trigger floating label state */
.input-group input:focus ~ label,
.input-group input:not(:placeholder-shown) ~ label {{
    top: 0;
    font-size: 12px;
    color: var(--accent);
}}

/* --- Success Step --- */
.success-message {{
    text-align: center;
    padding: 40px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
}}

.success-icon {{
    font-size: 72px;
    color: var(--accent);
    margin-bottom: 24px;
    animation: popIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}}

@keyframes popIn {{
    0% {{ transform: scale(0); opacity: 0; }}
    100% {{ transform: scale(1); opacity: 1; }}
}}

.success-message h3 {{
    font-size: 28px;
    margin-bottom: 12px;
}}

.success-message p {{
    font-size: 16px;
    color: var(--text-muted);
}}

/* --- Buttons --- */
.button-row {{
    display: flex;
    gap: 16px;
    margin-top: 32px;
}}

.button-row button {{
    flex: 1;
    padding: 14px 24px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
}}

.btn-next, .btn-submit, .btn-reset {{
    background: var(--accent);
    color: #fff;
}}

.btn-next:hover, .btn-submit:hover, .btn-reset:hover {{
    filter: brightness(1.1);
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}}

.btn-prev {{
    background: var(--surface-alt);
    color: var(--text);
    border: 1px solid var(--border);
}}

.btn-prev:hover {{
    background: var(--border);
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1 class="page-title">{title_text}</h1>
    <p class="page-description">{body_text}</p>
    
    <div class="container">
        <!-- Progress Bar -->
        <div class="progress-container">
            <div class="progress-track">
                <div class="progress-line"></div>
            </div>
            <ul class="progress-bar">
                <li class="active">
                    <div class="icon"><i class="fa-solid fa-lock"></i></div>
                    <strong>Account</strong>
                </li>
                <li>
                    <div class="icon"><i class="fa-solid fa-user"></i></div>
                    <strong>Personal</strong>
                </li>
                <li>
                    <div class="icon"><i class="fa-solid fa-share-nodes"></i></div>
                    <strong>Social</strong>
                </li>
                <li>
                    <div class="icon"><i class="fa-solid fa-check"></i></div>
                    <strong>Finish</strong>
                </li>
            </ul>
        </div>

        <!-- Forms -->
        <form id="multiStepForm">
            <!-- Step 1 -->
            <div class="form-step active">
                <div class="step-header">
                    <h2>Account Information</h2>
                    <span>Step 1 - 4</span>
                </div>
                <div class="input-group">
                    <input type="text" id="username" placeholder=" " required>
                    <label for="username">Username</label>
                </div>
                <div class="input-group">
                    <input type="email" id="email" placeholder=" " required>
                    <label for="email">Email Address</label>
                </div>
                <div class="input-group">
                    <input type="password" id="password" placeholder=" " required>
                    <label for="password">Password</label>
                </div>
                <div class="button-row">
                    <button type="button" class="btn-next">Next</button>
                </div>
            </div>

            <!-- Step 2 -->
            <div class="form-step">
                <div class="step-header">
                    <h2>Personal Details</h2>
                    <span>Step 2 - 4</span>
                </div>
                <div class="input-group">
                    <input type="text" id="firstname" placeholder=" " required>
                    <label for="firstname">First Name</label>
                </div>
                <div class="input-group">
                    <input type="text" id="lastname" placeholder=" " required>
                    <label for="lastname">Last Name</label>
                </div>
                <div class="input-group">
                    <input type="date" id="dob" placeholder=" " required>
                    <label for="dob">Date of Birth</label>
                </div>
                <div class="button-row">
                    <button type="button" class="btn-prev">Previous</button>
                    <button type="button" class="btn-next">Next</button>
                </div>
            </div>

            <!-- Step 3 -->
            <div class="form-step">
                <div class="step-header">
                    <h2>Social Presence</h2>
                    <span>Step 3 - 4</span>
                </div>
                <div class="input-group">
                    <input type="url" id="linkedin" placeholder=" ">
                    <label for="linkedin">LinkedIn Profile URL</label>
                </div>
                <div class="input-group">
                    <input type="url" id="github" placeholder=" ">
                    <label for="github">GitHub Profile URL</label>
                </div>
                <div class="button-row">
                    <button type="button" class="btn-prev">Previous</button>
                    <button type="button" class="btn-submit">Submit</button>
                </div>
            </div>

            <!-- Step 4 (Success) -->
            <div class="form-step">
                <div class="success-message">
                    <div class="success-icon"><i class="fa-solid fa-circle-check"></i></div>
                    <h3>Successfully Registered!</h3>
                    <p>Your account has been created and verified.</p>
                    <div class="button-row" style="width: 100%;">
                        <button type="button" class="btn-reset">Start New Registration</button>
                    </div>
                </div>
            </div>
        </form>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = """document.addEventListener('DOMContentLoaded', () => {
    const steps = document.querySelectorAll('.form-step');
    const nextBtns = document.querySelectorAll('.btn-next');
    const prevBtns = document.querySelectorAll('.btn-prev');
    const submitBtn = document.querySelector('.btn-submit');
    const resetBtn = document.querySelector('.btn-reset');
    const progressIndicators = document.querySelectorAll('.progress-bar li');
    const progressLine = document.querySelector('.progress-line');

    let currentStep = 0;

    function updateUI() {
        // Toggle visibility of forms with animation
        steps.forEach((step, index) => {
            step.classList.toggle('active', index === currentStep);
        });

        // Update active states on the progress bar icons
        progressIndicators.forEach((indicator, index) => {
            if (index <= currentStep) {
                indicator.classList.add('active');
            } else {
                indicator.classList.remove('active');
            }
        });

        // Calculate and set the width of the connecting progress line
        const totalSteps = progressIndicators.length;
        const progressPercentage = (currentStep / (totalSteps - 1)) * 100;
        progressLine.style.width = progressPercentage + '%';
    }

    // Next Button behavior
    nextBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            if (currentStep < steps.length - 1) {
                currentStep++;
                updateUI();
            }
        });
    });

    // Previous Button behavior
    prevBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            if (currentStep > 0) {
                currentStep--;
                updateUI();
            }
        });
    });

    // Submit Button behavior
    if (submitBtn) {
        submitBtn.addEventListener('click', () => {
            // Optional: Handle actual form submission via API here
            currentStep++; // Move to success step
            updateUI();
        });
    }

    // Reset Button behavior
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            // Clear all input fields
            document.getElementById('multiStepForm').reset();
            currentStep = 0; // Return to first step
            updateUI();
        });
    }

    // Initialize UI on load
    updateUI();
});
"""

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
