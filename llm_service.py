# =========================
# FILE: app/services/llm_service.py
# =========================

import time

from openai import OpenAI

from app.config import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


async def stream_llm_response(
    question: str,
    context: str
):

    prompt = f"""
You are a helpful assistant.

Context:
{context}

Question:
{question}
"""

    stream = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True
    )

    for chunk in stream:

        delta = chunk.choices[0].delta.content

        if delta:

            yield delta