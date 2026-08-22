import os, sys
from dotenv import load_dotenv
load_dotenv()
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Call WITHOUT response_format to see raw output including any thinking tokens
resp = client.chat.completions.create(
    model="qwen/qwen3.6-27b",
    messages=[{"role": "user", "content": 'Reply ONLY with this JSON: {"x": 1}'}],
    max_tokens=300,
    temperature=0,
)
raw = resp.choices[0].message.content
print("RAW OUTPUT:")
sys.stdout.buffer.write(repr(raw[:600]).encode("utf-8") + b"\n")
