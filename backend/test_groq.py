"""
Run this to test your Groq API key and connection.
Usage:  python test_groq.py
"""
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print(f"API Key found: {'YES — ' + api_key[:8] + '...' if api_key else 'NO — key is missing!'}")

if not api_key:
    print("\nFix: Open backend/.env and add:  GROQ_API_KEY=gsk_...")
    exit(1)

print("\nTesting Groq chat connection...")
try:
    from groq import Groq
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": "Reply with just: OK"}],
        max_tokens=5,
    )
    print(f"Chat test: SUCCESS — response: {response.choices[0].message.content}")
except Exception as e:
    print(f"Chat test FAILED: {type(e).__name__}: {e}")

print("\nAll tests done.")
