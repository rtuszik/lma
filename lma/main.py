import uvicorn
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from . import handlers
from . import utils

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
@limiter.limit("60/minute")
async def read_root(request: Request):
    utils.log_request("GET /", request.client.host, request.headers.get("user-agent", ""))
    return await handlers.handle_landing_page()

@app.post("/get-signin-modal", response_class=HTMLResponse)
@limiter.limit("60/minute")
async def get_signin_modal(request: Request):
    utils.log_request("POST /get-signin-modal", request.client.host, request.headers.get("user-agent", ""))
    return await handlers.handle_signin_modal()

@app.post("/check-vibe", response_class=HTMLResponse)
@limiter.limit("60/minute")
async def check_vibe(request: Request, user_input: str = Form(...), challenge: str = Form(...), session_id: str = Form(None)):
    utils.log_request("POST /check-vibe", request.client.host, request.headers.get("user-agent", ""))
    
    if len(user_input) > 2000:
        raise HTTPException(status_code=400, detail="Input too long (max 2000 characters)")
    if len(challenge) > 1000:
        raise HTTPException(status_code=400, detail="Challenge too long (max 1000 characters)")
    
    user_input = user_input.replace('\0', '').replace('\x00', '')
    challenge = challenge.replace('\0', '').replace('\x00', '')
    
    return await handlers.handle_vibe_check(request, user_input, challenge, session_id)

@app.get("/auth-result/{session_id}", response_class=HTMLResponse)
@limiter.limit("10/minute")
async def auth_result(request: Request, session_id: str):
    """Display authentication result (POST-redirect-GET pattern)"""
    utils.log_request(f"GET /auth-result/{session_id}", request.client.host, request.headers.get("user-agent", ""))
    return await handlers.handle_auth_result(session_id)

def run():
    uvicorn.run(app, host="0.0.0.0", port=6969)
