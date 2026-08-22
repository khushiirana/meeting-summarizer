"""Test Groq audio transcription endpoint directly."""
import os, struct, wave
from dotenv import load_dotenv
load_dotenv()

# Create a minimal valid WAV file in memory for testing
import io
wav_buffer = io.BytesIO()
with wave.open(wav_buffer, 'wb') as wav_file:
    wav_file.setnchannels(1)       # mono
    wav_file.setsampwidth(2)       # 16-bit
    wav_file.setframerate(16000)   # 16kHz
    wav_file.writeframes(b'\x00\x00' * 16000)  # 1 second of silence
wav_bytes = wav_buffer.getvalue()

print(f"Test WAV size: {len(wav_bytes)} bytes")

from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("Testing Groq audio transcription...")
try:
    response = client.audio.transcriptions.create(
        model="whisper-large-v3",
        file=("test.wav", wav_bytes, "audio/wav"),
        response_format="json",
    )
    text = response.text if hasattr(response, "text") else str(response)
    print(f"SUCCESS! Transcript: '{text}'")
except Exception as e:
    print(f"FAILED: {type(e).__name__}: {e}")
