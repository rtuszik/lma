import asyncio
from fastapi import Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from . import prompts
from . import templates
from . import utils
from . import sessions
from .config import (
    litellm,
    DEFAULT_MODEL,
    LITELLM_PROXY_API_KEY,
    LITELLM_PROXY_API_BASE,
)


async def handle_landing_page() -> HTMLResponse:
    return HTMLResponse(content=templates.get_landing_page_html())


async def handle_signin_modal() -> HTMLResponse:
    try:
        sessions.cleanup_expired_sessions()
        
        prompt = prompts.get_modal_generation_prompt()
        
        utils.log_debug("get_signin_modal", {
            "Model": DEFAULT_MODEL,
            "LiteLLM Proxy Base": LITELLM_PROXY_API_BASE if LITELLM_PROXY_API_BASE else "None",
            "LiteLLM Proxy Key": "Present" if LITELLM_PROXY_API_KEY else "None",
            "Prompt length": len(prompt),
            "LiteLLM module": getattr(litellm, '__file__', 'unknown'),
        })
        
        completion_params = {
            "model": DEFAULT_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "timeout": 30,
        }
        
        if LITELLM_PROXY_API_BASE and LITELLM_PROXY_API_KEY:
            completion_params["api_base"] = LITELLM_PROXY_API_BASE
            completion_params["api_key"] = LITELLM_PROXY_API_KEY
        
        response = await litellm.acompletion(**completion_params)
        
        utils.log_debug("SUCCESS: Response received", {
            "Response type": str(type(response)),
            "Choices length": len(response.choices) if response.choices else 0,
        })
        
        content = utils.clean_llm_response(response.choices[0].message.content)
        
        challenge = utils.extract_challenge_from_form(content)
        
        session_id = sessions.create_challenge_session(challenge)
        
        content = utils.add_session_to_form(content, session_id)
        
        content += templates.get_hide_auth_button_script()
        
        return HTMLResponse(content=content)
    except Exception as e:
        return utils.handle_llm_error(e, "get_signin_modal")


async def handle_vibe_check(request: Request, user_input: str = Form(...), challenge: str = Form(...), session_id: str = Form(None)) -> HTMLResponse:
    try:
        if not session_id:
            return HTMLResponse(content="<p>Session expired. Please start over.</p>", status_code=400)
        
        session_data = sessions.get_session(session_id)
        if not session_data:
            return HTMLResponse(content="<p>Session expired. Please start over.</p>", status_code=400)
        
        if sessions.is_session_completed(session_id):
            return HTMLResponse(content="<p>This authentication session has already been completed. Please start over.</p>", status_code=400)
        
        if session_data["challenge"] != challenge:
            return HTMLResponse(content="<p>Challenge mismatch. Please start over.</p>", status_code=400)
        
        if not sessions.increment_session_attempts(session_id):
            sessions.complete_session(session_id, False)
            return HTMLResponse(content="<p>Too many attempts. Please start over.</p>", status_code=400)
        
        await asyncio.sleep(2)
        
        prompt = prompts.get_vibe_check_prompt(challenge, user_input)
        
        utils.log_debug("COGNITIVE ANALYSIS INITIATED", {
            "Session ID": session_id,
            "Challenge": f"{challenge[:100]}...",
            "User Input": f"{user_input[:100]}...",
            "Attempt": session_data["attempts"],
            "Status": "Performing quantum-enhanced psychological analysis...",
        })
        
        completion_params = {
            "model": DEFAULT_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "timeout": 30,
        }
        
        if LITELLM_PROXY_API_BASE and LITELLM_PROXY_API_KEY:
            completion_params["api_base"] = LITELLM_PROXY_API_BASE
            completion_params["api_key"] = LITELLM_PROXY_API_KEY
        
        response = await litellm.acompletion(**completion_params)
        result = response.choices[0].message.content
        
        utils.log_debug("Assessment complete", {
            "Session ID": session_id,
            "AI Decision": result,
            "Psychological Profile": 'VALIDATED' if 'ACCESS GRANTED' in result else 'ANOMALY DETECTED',
        })
        
        if "ACCESS GRANTED" in result:
            sessions.complete_session(session_id, True)
            message = utils.extract_vibe_check_message(result, granted=True)
            
            session_data["result"] = {"granted": True, "message": message}
            
            return RedirectResponse(url=f"/auth-result/{session_id}", status_code=303)
        else:
            if session_data["attempts"] >= session_data["max_attempts"] - 1:
                sessions.complete_session(session_id, False)
            
            message = utils.extract_vibe_check_message(result, granted=False)
            
            session_data["result"] = {"granted": False, "message": message}
            
            return RedirectResponse(url=f"/auth-result/{session_id}", status_code=303)
    except Exception as e:
        return utils.handle_llm_error(e, "check_vibe")


async def handle_auth_result(session_id: str) -> HTMLResponse:
    session_data = sessions.get_session(session_id)
    
    if not session_data:
        return HTMLResponse(content="<p>Session expired. Please start over.</p>", status_code=400)
    
    result = session_data.get("result")
    if not result:
        return HTMLResponse(content="<p>No result available. Please complete authentication first.</p>", status_code=400)
    
    if result["granted"]:
        return HTMLResponse(content=templates.get_access_granted_html(result["message"]))
    else:
        return HTMLResponse(content=templates.get_access_denied_html(result["message"]))
