import asyncio
from fastapi import Request, Form
from fastapi.responses import HTMLResponse

from . import prompts
from . import templates
from . import utils
from .config import (
    litellm,
    openai_base,
    DEFAULT_MODEL,
    LITELLM_PROXY_API_KEY,
)


async def handle_landing_page() -> HTMLResponse:
    return HTMLResponse(content=templates.get_landing_page_html())


async def handle_signin_modal() -> HTMLResponse:
    try:
        prompt = prompts.get_modal_generation_prompt()
        
        utils.log_debug("get_signin_modal", {
            "Model": DEFAULT_MODEL,
            "API Base": openai_base,
            "API Key (first 10 chars)": f"{LITELLM_PROXY_API_KEY[:10]}..." if LITELLM_PROXY_API_KEY else "None",
            "Prompt length": len(prompt),
            "LiteLLM module": getattr(litellm, '__file__', 'unknown'),
        })
        
        response = await litellm.acompletion(
            model=DEFAULT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            timeout=30,  
            api_base=openai_base,  
            api_key=LITELLM_PROXY_API_KEY,  
        )
        
        utils.log_debug("SUCCESS: Response received", {
            "Response type": str(type(response)),
            "Choices length": len(response.choices) if response.choices else 0,
        })
        
        content = utils.clean_llm_response(response.choices[0].message.content)
        
        content += templates.get_hide_auth_button_script()
        
        return HTMLResponse(content=content)
    except Exception as e:
        return utils.handle_llm_error(e, "get_signin_modal")


async def handle_vibe_check(request: Request, user_input: str = Form(...), challenge: str = Form(...)) -> HTMLResponse:
    try:
        await asyncio.sleep(2)
        
        prompt = prompts.get_vibe_check_prompt(challenge, user_input)
        
        utils.log_debug("COGNITIVE ANALYSIS INITIATED", {
            "Challenge": f"{challenge[:100]}...",
            "User Input": f"{user_input[:100]}...",
            "Status": "Performing quantum-enhanced psychological analysis...",
        })
        
        response = await litellm.acompletion(
            model=DEFAULT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            timeout=30,  
            api_base=openai_base,  
            api_key=LITELLM_PROXY_API_KEY,  
        )
        result = response.choices[0].message.content
        
        utils.log_debug("Assessment complete", {
            "AI Decision": result,
            "Psychological Profile": 'VALIDATED' if 'ACCESS GRANTED' in result else 'ANOMALY DETECTED',
        })
        
        if "ACCESS GRANTED" in result:
            message = utils.extract_vibe_check_message(result, granted=True)
            return HTMLResponse(content=templates.get_access_granted_html(message))
        else:
            message = utils.extract_vibe_check_message(result, granted=False)
            return HTMLResponse(content=templates.get_access_denied_html(message))
    except Exception as e:
        return utils.handle_llm_error(e, "check_vibe")
