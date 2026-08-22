import os
from dotenv import load_dotenv
load_dotenv()
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
print("Testing qwen/qwen3.6-27b...")
resp = client.chat.completions.create(
    model="qwen/qwen3.6-27b",
    messages=[
        {"role": "system", "content": "You are a meeting analyst. Always reply with JSON only."},
        {"role": "user", "content": 'Summarize: Team decided to launch Friday. John will prepare slides. Reply with {"summary":"...","key_decisions":[],"action_items":[]}'}
    ],
    temperature=0.3,
    response_format={"type": "json_object"},
)
print("SUCCESS:", resp.choices[0].message.content)
