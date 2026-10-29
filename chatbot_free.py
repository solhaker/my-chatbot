import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    timeout=30,
)

MODEL = "gemini-3.1-flash-lite"

SYSTEM_PROMPT = "You are a friendly, helpful assistant named Buddy. Keep answers clear and concise."

MAX_MESSAGES = 20
history = [{"role": "system", "content": SYSTEM_PROMPT}]

print("Chatbot ready! Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in {"quit", "exit"}:
        print("Goodbye!")
        break
    if not user_input:
        continue

    history.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[history[0]] + history[1:][-MAX_MESSAGES:],
        )
        reply = response.choices[0].message.content or ""
        if not reply:
            print("[Empty reply. Raw response below]")
            print(response)
            history.pop()
            continue
        print("Buddy:", reply, "\n")
        history.append({"role": "assistant", "content": reply})
    except Exception as e:
        print(f"\n[Error: {e}]\n")
        history.pop()