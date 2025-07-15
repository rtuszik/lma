import os
import json
import logging
import litellm
from dotenv import load_dotenv

load_dotenv()

DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() in ("true", "1", "yes", "on")
if DEBUG_MODE:
    print("WARNING: DEBUG_MODE is enabled! This should NOT be used in production.")
    litellm.set_verbose = True
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
else:
    logger = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")

custom_headers = os.getenv("LITELLM_CUSTOM_HEADERS")
if custom_headers:
    setattr(litellm, "headers", json.loads(custom_headers))

base_url_mappings = {
    "openai_api_base": os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE"),
    "anthropic_api_base": os.getenv("ANTHROPIC_BASE_URL") or os.getenv("ANTHROPIC_API_BASE"),
    "cohere_api_base": os.getenv("COHERE_API_BASE"),
    "gemini_api_base": os.getenv("GEMINI_API_BASE"),
    "azure_api_base": os.getenv("AZURE_API_BASE"),
    "together_api_base": os.getenv("TOGETHER_API_BASE"),
    "huggingface_api_base": os.getenv("HUGGINGFACE_API_BASE"),
    "databricks_api_base": os.getenv("DATABRICKS_API_BASE"),
    "ollama_api_base": os.getenv("OLLAMA_API_BASE"),
}

for attr_name, base_url in base_url_mappings.items():
    if base_url:
        setattr(litellm, attr_name, base_url)
        if DEBUG_MODE:
            print(f"Set LiteLLM {attr_name} to: {base_url}")

LITELLM_PROXY_API_KEY = os.getenv("LITELLM_PROXY_API_KEY")
LITELLM_PROXY_API_BASE = os.getenv("LITELLM_PROXY_API_BASE")

if LITELLM_PROXY_API_BASE:
    setattr(litellm, "api_base", LITELLM_PROXY_API_BASE)
    if DEBUG_MODE:
        print(f"Set LiteLLM proxy base to: {LITELLM_PROXY_API_BASE}")

__all__ = [
    "logger",
    "litellm",
    "DEFAULT_MODEL",
    "LITELLM_PROXY_API_KEY",
    "LITELLM_PROXY_API_BASE",
    "DEBUG_MODE",
]
