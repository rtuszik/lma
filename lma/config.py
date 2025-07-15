import os
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

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")

__all__ = [
    "logger",
    "litellm",
    "DEFAULT_MODEL",
    "DEBUG_MODE",
]
