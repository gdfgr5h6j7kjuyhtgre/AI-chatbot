# Simple AI Chatbot (Python)

A beginner-friendly chatbot you can run locally for:
- Homework-style questions
- Everyday Q&A
- Quick calculations

It works in **two modes**:
1. **AI mode** (best): uses OpenAI API when `OPENAI_API_KEY` is set.
2. **Offline fallback mode**: still answers simple prompts without any API key.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python chatbot.py
```

## Optional: enable AI mode

```bash
export OPENAI_API_KEY="your_api_key_here"
python chatbot.py
```

## Example prompts

- `hello`
- `calculate 45 * 8`
- `help me with my homework on photosynthesis`
- `what is the time right now?`

## Notes

- If API mode fails (network/key issue), the bot automatically falls back to offline responses.
- For safety, calculator mode only accepts numbers and basic math operators.
