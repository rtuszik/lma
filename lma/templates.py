def get_landing_page_html() -> str:
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VibeAuth Enterprise - Quantum-Enhanced Behavioral Authentication Platform</title>
        <script src="https://unpkg.com/htmx.org@1.9.10"></script>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #333;
            }
            
            .container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 16px;
                padding: 40px;
                max-width: 480px;
                width: 90%;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                text-align: center;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .logo {
                font-size: 2.2em;
                font-weight: 700;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 8px;
            }
            
            .tagline {
                color: #666;
                font-size: 0.95em;
                margin-bottom: 24px;
                font-weight: 500;
            }
            
            .description {
                color: #555;
                line-height: 1.6;
                margin-bottom: 32px;
                font-size: 0.9em;
            }
            
            .auth-button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 16px 32px;
                border-radius: 8px;
                font-size: 1em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                width: 100%;
                position: relative;
                overflow: hidden;
            }
            
            .auth-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }
            
            .auth-button:active {
                transform: translateY(0);
            }
            
            .auth-button.loading {
                pointer-events: none;
                opacity: 0.8;
            }
            
            .loading-spinner {
                display: none;
                width: 20px;
                height: 20px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                border-top-color: white;
                animation: spin 1s ease-in-out infinite;
                margin-right: 8px;
            }
            
            .auth-button.loading .loading-spinner {
                display: inline-block;
            }
            
            .auth-button.loading .button-text {
                opacity: 0.7;
            }
            
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            
            .modal-container {
                margin-top: 24px;
                text-align: left;
            }
            
            .features {
                margin-top: 32px;
                text-align: left;
                font-size: 0.85em;
                color: #666;
            }
            
            .feature {
                margin-bottom: 8px;
                display: flex;
                align-items: center;
            }
            
            .feature::before {
                content: "✓";
                color: #667eea;
                font-weight: bold;
                margin-right: 8px;
                width: 16px;
            }
            
            .powered-by {
                margin-top: 24px;
                padding-top: 20px;
                border-top: 1px solid #eee;
                font-size: 0.8em;
                color: #999;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">VibeAuth</div>
            <div class="tagline">Next-Generation Identity Verification</div>
            
            <div class="description">
                Advanced behavioral authentication powered by AI. Bullet-Proof Authentication for the Agentic Age.
            </div>
            
            <button 
                class="auth-button" 
                hx-post="/get-signin-modal" 
                hx-target="#modal-container"
                hx-indicator="#loading-indicator"
                onclick="showLoading(this)"
            >
                <span class="loading-spinner"></span>
                <span class="button-text">Start Authentication</span>
            </button>
            
            <div id="modal-container" class="modal-container"></div>
            
            <div class="features">
                <div class="feature">AI-powered gatekeeping analysis</div>
                <div class="feature">Zero-knowledge (No one knows whats going on)</div>
                <div class="feature">Enterprise security standards (Minutes Before Chapter 11)</div>
                <div class="feature">Fraud-resistant verification</div>
            </div>
            
            <div class="powered-by">
                Powered by hopes and dreams.
            </div>
        </div>
        
        <script>
            function showLoading(button) {
                button.classList.add('loading');
                button.querySelector('.button-text').textContent = 'Generating challenge...';
            }
            
            // Reset button state when content loads
            document.addEventListener('htmx:afterSettle', function(event) {
                const button = document.querySelector('.auth-button');
                if (button && !document.querySelector('form[action="/check-vibe"]')) {
                    button.classList.remove('loading');
                    button.querySelector('.button-text').textContent = 'Start Authentication';
                }
                
                // Add loading feedback to form submissions
                const forms = document.querySelectorAll('form[action="/check-vibe"]');
                forms.forEach(form => {
                    const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
                    if (submitBtn && !submitBtn.dataset.listenerAdded) {
                        submitBtn.dataset.listenerAdded = 'true';
                        submitBtn.addEventListener('click', function(e) {
                            // Show sophisticated loading message
                            setTimeout(() => {
                                const modalContainer = document.getElementById('modal-container');
                                if (modalContainer) {
                                    modalContainer.innerHTML = `
                                        <div style="background: linear-gradient(135deg, #4a90e2, #357abd); color: white; padding: 30px; border-radius: 12px; text-align: center; box-shadow: 0 8px 25px rgba(74,144,226,0.3);">
                                            <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
                                                <div style="width: 24px; height: 24px; border: 3px solid rgba(255,255,255,0.3); border-radius: 50%; border-top-color: white; animation: spin 1s linear infinite; margin-right: 12px;"></div>
                                                <h2 style="margin: 0; font-size: 1.5em; font-weight: 700;">Analyzing Response</h2>
                                            </div>
                                            <p style="margin: 0; font-size: 1em; opacity: 0.9;">Processing your response...</p>
                                        </div>
                                    `;
                                }
                            }, 100);
                        });
                    }
                });
            });
            
            // Handle errors
            document.addEventListener('htmx:responseError', function(event) {
                const button = document.querySelector('.auth-button');
                if (button) {
                    button.classList.remove('loading');
                    button.querySelector('.button-text').textContent = 'Error - Try Again';
                    setTimeout(() => {
                        button.querySelector('.button-text').textContent = 'Start Authentication';
                    }, 3000);
                }
            });
        </script>
    </body>
    </html>
    """


def get_hide_auth_button_script() -> str:
    return """
    <script>
        // Hide the start authentication button
        const authButton = document.querySelector('.auth-button');
        if (authButton) {
            authButton.style.display = 'none';
        }
    </script>
    """


def get_access_granted_html(message: str) -> str:
    return f"""
        <div style="background: linear-gradient(135deg, #00ff88, #00cc44); color: white; padding: 30px; border-radius: 12px; text-align: center; box-shadow: 0 8px 25px rgba(0,255,136,0.3);">
            <h1 style="margin: 0 0 15px 0; font-size: 2.2em; font-weight: 700;">Access Granted</h1>
            <p style="margin: 0; font-size: 1.1em; opacity: 0.95;">{message}</p>
        </div>
    """


def get_access_denied_html(message: str) -> str:
    return f"""
        <div style="background: linear-gradient(135deg, #ff4757, #ff3838); color: white; padding: 30px; border-radius: 12px; text-align: center; box-shadow: 0 8px 25px rgba(255,71,87,0.3);">
            <h1 style="margin: 0 0 15px 0; font-size: 2.2em; font-weight: 700;">Access Denied</h1>
            <p style="margin: 0; font-size: 1.1em; opacity: 0.95;">{message}</p>
        </div>
    """


def get_processing_html() -> str:
    return """
        <div style="background: linear-gradient(135deg, #4a90e2, #357abd); color: white; padding: 30px; border-radius: 12px; text-align: center; box-shadow: 0 8px 25px rgba(74,144,226,0.3);">
            <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
                <div style="width: 24px; height: 24px; border: 3px solid rgba(255,255,255,0.3); border-radius: 50%; border-top-color: white; animation: spin 1s linear infinite; margin-right: 12px;"></div>
                <h2 style="margin: 0; font-size: 1.5em; font-weight: 700;">Analyzing Response</h2>
            </div>
            <p style="margin: 0; font-size: 1em; opacity: 0.9;">Processing your response...</p>
        </div>
    """
