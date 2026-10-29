import os, base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    timeout=60,
)

result = client.images.generate(
    model="gemini-2.5-flash-image",
    prompt="A sleek modern mountain bike on a sunny mountain trail, realistic",
    response_format="b64_json",
    n=1,
)

with open("bike.png", "wb") as f:
    f.write(base64.b64decode(result.data[0].b64_json))
print("Saved bike.png")