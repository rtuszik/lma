import os
import secrets
import time
from typing import Dict, Any, Optional
from jose import jwt, JWTError
from .config import DEBUG_MODE

_session_store: Dict[str, Dict[str, Any]] = {}

SECRET_KEY = os.getenv("SESSION_SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
SESSION_TIMEOUT = 3600

def create_session_token(data: Dict[str, Any]) -> str:
    payload = {
        **data,
        "exp": time.time() + SESSION_TIMEOUT,
        "iat": time.time(),
        "jti": secrets.token_urlsafe(16)  
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_session_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        if time.time() > payload.get("exp", 0):
            return None
            
        return payload
    except JWTError:
        return None

def create_challenge_session(challenge: str) -> str:
    session_id = secrets.token_urlsafe(16)
    session_data = {
        "challenge": challenge,
        "created_at": time.time(),
        "attempts": 0,
        "max_attempts": 3,
        "completed": False
    }
    
    _session_store[session_id] = session_data
    
    if DEBUG_MODE:
        print(f"Created challenge session: {session_id}")
    
    return session_id

def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    session = _session_store.get(session_id)
    
    if session and time.time() - session["created_at"] < SESSION_TIMEOUT:
        return session
    
    if session_id in _session_store:
        del _session_store[session_id]
    
    return None

def increment_session_attempts(session_id: str) -> bool:
    session = get_session(session_id)
    if not session:
        return False
    
    session["attempts"] += 1
    
    if session["attempts"] >= session["max_attempts"]:
        session["completed"] = True
        return False
    
    return True

def complete_session(session_id: str, success: bool) -> bool:
    session = get_session(session_id)
    if not session:
        return False
    
    session["completed"] = True
    session["success"] = success
    
    if DEBUG_MODE:
        print(f"Session {session_id} completed with success: {success}")
    
    return True

def is_session_completed(session_id: str) -> bool:
    session = get_session(session_id)
    return session and session.get("completed", False)

def cleanup_expired_sessions():
    current_time = time.time()
    expired_sessions = [
        session_id for session_id, session in _session_store.items()
        if current_time - session["created_at"] > SESSION_TIMEOUT
    ]
    
    for session_id in expired_sessions:
        del _session_store[session_id]
    
    if DEBUG_MODE and expired_sessions:
        print(f"Cleaned up {len(expired_sessions)} expired sessions")
