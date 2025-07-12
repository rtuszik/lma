import os
import json
import logging
import litellm
from dotenv import load_dotenv

load_dotenv()

if os.getenv("DEBUG_MODE"):
    litellm.set_verbose = True
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
else:
    logger = logging.getLogger(__name__)

# Note: LiteLLM automatically picks up API keys from environment variables
# Set base URLs if provided (using proper attribute access)
openai_base = os.getenv("OPENAI_API_BASE") or os.getenv("LITELLM_PROXY_API_BASE")
if openai_base:
    setattr(litellm, "openai_api_base", openai_base)
    if os.getenv("DEBUG_MODE"):
        print(f"Set LiteLLM openai_api_base to: {openai_base}")

anthropic_base = os.getenv("ANTHROPIC_API_BASE")
if anthropic_base:
    setattr(litellm, "anthropic_api_base", anthropic_base)

cohere_base = os.getenv("COHERE_API_BASE")
if cohere_base:
    setattr(litellm, "cohere_api_base", cohere_base)

gemini_base = os.getenv("GEMINI_API_BASE")
if gemini_base:
    setattr(litellm, "gemini_api_base", gemini_base)

custom_headers = os.getenv("LITELLM_CUSTOM_HEADERS")
if custom_headers:
    setattr(litellm, "headers", json.loads(custom_headers))

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")

LITELLM_PROXY_API_KEY = os.getenv("LITELLM_PROXY_API_KEY")

__all__ = [
    "logger",
    "litellm",
    "openai_base",
    "DEFAULT_MODEL",
    "LITELLM_PROXY_API_KEY",
]
