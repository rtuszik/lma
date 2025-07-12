import os
import traceback
from typing import Optional, Dict, Any
from fastapi.responses import HTMLResponse


def handle_llm_error(error: Exception, context: str = "") -> HTMLResponse:
    error_str = str(error)
    error_type = type(error).__name__
    
    if os.getenv("DEBUG_MODE"):
        print(f"=== ERROR in {context}: {error_type} ===")
        print(f"Error message: {error_str}")
        print(f"Error type: {error_type}")
        print(f"Traceback: {traceback.format_exc()}")
    
    if "api" in error_str.lower() or "key" in error_str.lower() or "auth" in error_str.lower():
        error_msg = f"<p>LLM API Error ({error_type}): {error_str}</p><p>Please check your API keys and model configuration.</p>"
        return HTMLResponse(content=error_msg, status_code=503)
    elif "timeout" in error_str.lower():
        return HTMLResponse(content="<p>Request timed out. Please try again.</p>", status_code=504)
    else:
        return HTMLResponse(content=f"<p>Unexpected error ({error_type}): {error_str}</p>", status_code=500)


def clean_llm_response(content: str) -> str:
    return content.replace('```html', '').replace('```', '').strip()


def extract_vibe_check_message(result: str, granted: bool) -> str:
    if granted:
        default_message = "Authentication successful. Welcome!"
        prefix = "ACCESS GRANTED:"
    else:
        default_message = "Authentication failed. Please try again."
        prefix = "ACCESS DENIED:"
    
    if ":" in result and prefix in result:
        return result.split(prefix, 1)[1].strip()
    return default_message


def log_debug(message: str, data: Optional[Dict[str, Any]] = None) -> None:
    if os.getenv("DEBUG_MODE"):
        print(f"=== DEBUG: {message} ===")
        if data:
            for key, value in data.items():
                if isinstance(value, str) and len(value) > 100:
                    value = f"{value[:100]}..."
                print(f"{key}: {value}")
