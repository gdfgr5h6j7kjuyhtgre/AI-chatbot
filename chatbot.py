#!/usr/bin/env python3
"""Simple AI chatbot for homework help and everyday questions.

Usage:
  1) Optional: set OPENAI_API_KEY for model-powered responses.
  2) Run: python chatbot.py
"""

from __future__ import annotations

import datetime as dt
import os
import random
import re
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


FALLBACK_RESPONSES = {
    "hello": ["Hi! How can I help today?", "Hello! Ask me anything simple."],
    "how are you": ["I'm doing great and ready to help!"],
    "thanks": ["You're welcome!", "Anytime!"],
    "bye": ["Goodbye!", "See you next time!"]
}


class SimpleChatbot:
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.model = model
        self.client: Optional[OpenAI] = None
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and OpenAI is not None:
            self.client = OpenAI(api_key=api_key)

    def _local_response(self, message: str) -> str:
        text = message.strip().lower()

        for key, responses in FALLBACK_RESPONSES.items():
            if key in text:
                return random.choice(responses)

        if "time" in text:
            return f"Current UTC time is {dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}"

        if text.startswith("calculate "):
            expr = text.removeprefix("calculate ").strip()
            if not re.fullmatch(r"[0-9+\-*/(). ]+", expr):
                return "I can only calculate simple math expressions with numbers and + - * / ( )."
            try:
                # Safe because expression is strict-whitelisted above.
                result = eval(expr, {"__builtins__": {}}, {})
                return f"Result: {result}"
            except Exception:
                return "I couldn't calculate that. Try a simpler expression."

        if "homework" in text:
            return (
                "Sure — share your homework question. I can help break it into steps "
                "and explain clearly."
            )

        return (
            "I can help with simple questions, explanations, and quick calculations. "
            "Try: 'calculate 23*4' or ask a homework question."
        )

    def reply(self, message: str) -> str:
        if not self.client:
            return self._local_response(message)

        try:
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "system",
                        "content": "You are a helpful, concise assistant for homework and daily questions.",
                    },
                    {"role": "user", "content": message},
                ],
                max_output_tokens=300,
            )
            return response.output_text.strip()
        except Exception:
            # Fallback to local behavior if API call fails.
            return self._local_response(message)


def main() -> None:
    bot = SimpleChatbot()
    print("Simple AI Chatbot")
    print("Type 'exit' to quit.\n")

    while True:
        user_message = input("You: ").strip()
        if user_message.lower() in {"exit", "quit"}:
            print("Bot: Goodbye!")
            break

        answer = bot.reply(user_message)
        print(f"Bot: {answer}\n")


if __name__ == "__main__":
    main()
