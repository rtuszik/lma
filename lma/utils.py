import traceback
from typing import Optional, Dict, Any
from fastapi.responses import HTMLResponse
from .config import DEBUG_MODE


def handle_llm_error(error: Exception, context: str = "") -> HTMLResponse:
    error_str = str(error)
    error_type = type(error).__name__
    
    if DEBUG_MODE:
        print(f"=== ERROR in {context}: {error_type} ===")
        print(f"Error message: {error_str}")
        print(f"Error type: {error_type}")
        print(f"Traceback: {traceback.format_exc()}")
    
    if "api" in error_str.lower() or "key" in error_str.lower() or "auth" in error_str.lower():
        if DEBUG_MODE:
            error_msg = f"<p>LLM API Error ({error_type}): {error_str}</p><p>Please check your API keys and model configuration.</p>"
        else:
            error_msg = "<p>Authentication system temporarily unavailable. Please try again later.</p>"
        return HTMLResponse(content=error_msg, status_code=503)
    elif "timeout" in error_str.lower():
        return HTMLResponse(content="<p>Request timed out. Please try again.</p>", status_code=504)
    else:
        if DEBUG_MODE:
            error_msg = f"<p>Unexpected error ({error_type}): {error_str}</p>"
        else:
            error_msg = "<p>Authentication system error. Please try again later.</p>"
        return HTMLResponse(content=error_msg, status_code=500)


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
    if DEBUG_MODE:
        print(f"=== DEBUG: {message} ===")
        if data:
            for key, value in data.items():
                if isinstance(value, str) and len(value) > 100:
                    value = f"{value[:100]}..."
                print(f"{key}: {value}")


def log_request(endpoint: str, client_ip: str, user_agent: str = "") -> None:
    if DEBUG_MODE:
        print(f"=== REQUEST: {endpoint} ===")
        print(f"Client IP: {client_ip}")
        print(f"User Agent: {user_agent[:100]}..." if len(user_agent) > 100 else user_agent)


def extract_challenge_from_form(html_content: str) -> str:
    """Extract challenge value from the generated form HTML"""
    import re
    
    # Look for hidden input with name="challenge" and extract its value
    match = re.search(r'<input[^>]*name="challenge"[^>]*value="([^"]*)"', html_content)
    if match:
        return match.group(1)
    
    # Fallback: try to extract from any text that looks like a challenge
    # This is a more generic approach for different form formats
    lines = html_content.split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.startswith('<') and '?' in line:
            # Likely a challenge question
            return line.split('?')[0] + '?'
    
    return "Unknown challenge"


def add_session_to_form(html_content: str, session_id: str) -> str:
    """Add session ID as hidden input to the form"""
    import re
    
    # Look for the form tag and add session ID after it
    session_input = f'<input type="hidden" name="session_id" value="{session_id}">'
    
    # Try to add after the opening form tag
    form_match = re.search(r'(<form[^>]*>)', html_content)
    if form_match:
        form_tag = form_match.group(1)
        return html_content.replace(form_tag, form_tag + '\n' + session_input)
    
    # Fallback: add at the beginning of the content
    return session_input + '\n' + html_content
