import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse

from . import handlers

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return await handlers.handle_landing_page()

@app.post("/get-signin-modal", response_class=HTMLResponse)
async def get_signin_modal():
    return await handlers.handle_signin_modal()

@app.post("/check-vibe", response_class=HTMLResponse)
async def check_vibe(request: Request, user_input: str = Form(...), challenge: str = Form(...)):
    return await handlers.handle_vibe_check(request, user_input, challenge)

def run():
    uvicorn.run(app, host="0.0.0.0", port=6969)
