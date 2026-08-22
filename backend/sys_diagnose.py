"""
Systematic connection diagnostic — mimics exactly how the background task runs.
Tests: env loading, key presence, network reachability, threading context.
Does NOT print the API key.
Run: .\venv\Scripts\python.exe sys_diagnose.py
"""
import os, sys, threading, io, wave, socket, ssl
from dotenv import load_dotenv

sep = lambda t: print(f"\n{'='*55}\n{t}\n{'='*55}")

# ── 1. ENV LOADING ─────────────────────────────────────────
sep("1. ENV LOADING")
load_dotenv()
key = os.getenv("GROQ_API_KEY", "")
print(f"Key present       : {'YES, length=' + str(len(key)) if key else 'NO'}")
print(f"Key starts gsk_   : {key.startswith('gsk_')}")
print(f"Key has whitespace: {key != key.strip()}")

# ── 2. NETWORK / DNS ───────────────────────────────────────
sep("2. NETWORK / DNS / TLS TO api.groq.com")
try:
    ip = socket.getaddrinfo("api.groq.com", 443)[0][4][0]
    print(f"DNS resolve       : OK → {ip}")
except Exception as e:
    print(f"DNS resolve       : FAILED → {e}")

try:
    ctx = ssl.create_default_context()
    with socket.create_connection(("api.groq.com", 443), timeout=10) as sock:
        with ctx.wrap_socket(sock, server_hostname="api.groq.com") as ssock:
            print(f"TLS connect       : OK (protocol={ssock.version()})")
except Exception as e:
    print(f"TLS connect       : FAILED → {e}")

# ── 3. PROXY ENV VARS ──────────────────────────────────────
sep("3. PROXY ENVIRONMENT VARIABLES")
found = False
for v in ["HTTP_PROXY","HTTPS_PROXY","ALL_PROXY","NO_PROXY",
          "http_proxy","https_proxy","all_proxy","no_proxy"]:
    if os.environ.get(v):
        print(f"  {v} = {os.environ[v]}")
        found = True
if not found:
    print("  None found (good)")

# ── 4. GROQ SDK VERSION ────────────────────────────────────
sep("4. GROQ SDK")
import groq as _g
print(f"Version           : {_g.__version__}")

# ── 5. AUDIO CALL — MAIN THREAD ───────────────────────────
sep("5. AUDIO TRANSCRIPTION — MAIN THREAD")
def make_wav():
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000)
        w.writeframes(b"\x00\x00" * 8000)
    return buf.getvalue()

def run_transcription(label):
    import traceback as tb
    from groq import Groq
    key = os.getenv("GROQ_API_KEY", "")
    print(f"[{label}] key present: {'YES len=' + str(len(key)) if key else 'NO'}")
    try:
        client = Groq(api_key=key)
        resp = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=("test.wav", make_wav(), "audio/wav"),
            response_format="json",
        )
        text = resp.text if hasattr(resp, "text") else str(resp)
        print(f"[{label}] Result    : SUCCESS — '{text.strip()}'")
    except Exception as e:
        print(f"[{label}] Result    : FAILED — {type(e).__name__}: {e}")
        tb.print_exc()

run_transcription("main-thread")

# ── 6. AUDIO CALL — BACKGROUND THREAD (like FastAPI) ──────
sep("6. AUDIO TRANSCRIPTION — BACKGROUND THREAD (FastAPI simulation)")
t = threading.Thread(target=run_transcription, args=("bg-thread",))
t.start()
t.join()

sep("DONE")
