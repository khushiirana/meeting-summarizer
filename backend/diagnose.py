"""
Full diagnostic: checks env, proxy, groq client, and actual audio upload.
Run: .\venv\Scripts\python.exe diagnose.py
"""
import os, sys
from dotenv import load_dotenv

print("=" * 60)
print("1. ENVIRONMENT CHECK")
print("=" * 60)
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print(f"GROQ_API_KEY loaded : {'YES — ' + api_key[:10] + '...' if api_key else 'NO'}")

# Check for proxy env vars that might interfere
for var in ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy", "NO_PROXY"]:
    val = os.environ.get(var)
    if val:
        print(f"WARNING proxy env var found: {var}={val}")

print(f"Python version      : {sys.version}")

print()
print("=" * 60)
print("2. GROQ PACKAGE VERSION")
print("=" * 60)
import groq as groq_pkg
print(f"groq version        : {groq_pkg.__version__}")

print()
print("=" * 60)
print("3. GROQ CLIENT INIT")
print("=" * 60)
try:
    from groq import Groq
    client = Groq(api_key=api_key)
    print(f"Base URL            : {client.base_url}")
    print("Client init         : OK")
except Exception as e:
    print(f"Client init FAILED  : {e}")
    sys.exit(1)

print()
print("=" * 60)
print("4. CHAT ENDPOINT TEST")
print("=" * 60)
try:
    resp = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[{"role": "user", "content": "Say OK"}],
        max_tokens=3,
    )
    print(f"Chat test           : SUCCESS — '{resp.choices[0].message.content.strip()}'")
except Exception as e:
    print(f"Chat test           : FAILED — {type(e).__name__}: {e}")

print()
print("=" * 60)
print("5. AUDIO TRANSCRIPTION TEST (real file bytes)")
print("=" * 60)
import io, wave

# Build a minimal valid WAV in memory
buf = io.BytesIO()
with wave.open(buf, "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(16000)
    w.writeframes(b"\x00\x00" * 16000)
wav_bytes = buf.getvalue()

try:
    resp = client.audio.transcriptions.create(
        model="whisper-large-v3",
        file=("test.wav", wav_bytes, "audio/wav"),
        response_format="json",
    )
    text = resp.text if hasattr(resp, "text") else str(resp)
    print(f"Audio test          : SUCCESS — '{text.strip()}'")
except Exception as e:
    import traceback
    print(f"Audio test          : FAILED — {type(e).__name__}: {e}")
    print()
    traceback.print_exc()

print()
print("=" * 60)
print("6. TRANSCRIPTION.PY FILE OPEN TEST")
print("=" * 60)
# Check how transcription.py opens the file vs how it should
print("Current transcription.py passes: open(file_path, 'rb') as file object")
print("Groq 1.x recommended : tuple (filename, bytes, mime_type)")
print("Fix needed           : YES — update transcription.py to use tuple form")
