# backend/client.py
import os
from openai import AsyncOpenAI
# SDK wrapper used earlier in our plan
from agents import OpenAIChatCompletionsModel

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY is required in env")

# Gemini-compatible OpenAI-style client
client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

# Model wrapper used by agents
gemini_model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-1.5-flash"
)
