"""
llm_client.py — tiny shared helper so every exercise file can get an LLM
client the same way, regardless of which provider you configured in .env.

Supports OpenAI, Groq, and Google Gemini — all three expose an
OpenAI-compatible /chat/completions endpoint, so we only need one client
class (openai.OpenAI) with a different base_url + api_key per provider.

Usage:
    from llm_client import get_client, chat

    client, model = get_client()
    reply = chat(client, model, "Say hello in 5 words")
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Sensible default models per provider (override with MODEL in .env if you want)
DEFAULT_MODELS = {
    "openai": "gpt-4o-mini",
    "groq": "llama-3.3-70b-versatile",
    "gemini": "gemini-2.0-flash",
}

BASE_URLS = {
    "openai": None,  # default OpenAI endpoint
    "groq": "https://api.groq.com/openai/v1",
    "gemini": "https://generativelanguage.googleapis.com/v1beta/openai/",
}

API_KEY_ENV_VARS = {
    "openai": "OPENAI_API_KEY",
    "groq": "GROQ_API_KEY",
    "gemini": "GEMINI_API_KEY",
}


class SetupError(RuntimeError):
    pass


def get_client():
    """Returns (client, model_name) based on the LLM_PROVIDER in your .env"""
    from openai import OpenAI  # imported here so a missing package fails clearly

    provider = os.getenv("LLM_PROVIDER", "").strip().lower()
    if provider not in DEFAULT_MODELS:
        raise SetupError(
            f"LLM_PROVIDER must be one of {list(DEFAULT_MODELS)}, got: {provider!r}. "
            f"Set it in your .env file."
        )

    key_var = API_KEY_ENV_VARS[provider]
    api_key = os.getenv(key_var)
    if not api_key:
        raise SetupError(f"Missing {key_var} in your .env file for provider '{provider}'.")

    model = os.getenv("MODEL", DEFAULT_MODELS[provider])
    base_url = BASE_URLS[provider]

    client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
    return client, model


def chat(client, model, prompt, system=None, temperature=0.2):
    """One-shot chat call. Returns the assistant's text reply."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return resp.choices[0].message.content.strip()
