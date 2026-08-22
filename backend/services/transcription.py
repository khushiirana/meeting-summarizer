import os
from dotenv import load_dotenv

load_dotenv()


def _get_client():
    from groq import Groq
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Please add it to backend/.env"
        )
    return Groq(api_key=api_key)


def transcribe_audio(file_path: str) -> str:
    """
    Transcribe an audio file using Groq Whisper-large-v3.
    """
    import groq as _g
    api_key = os.getenv("GROQ_API_KEY", "")
    file_size = os.path.getsize(file_path) if os.path.exists(file_path) else -1

    print(f"[transcribe] groq version : {_g.__version__}")
    print(f"[transcribe] key present  : {'YES len=' + str(len(api_key)) if api_key else 'NO'}")
    print(f"[transcribe] file         : {file_path}")
    print(f"[transcribe] file size    : {file_size} bytes ({file_size/1024/1024:.2f} MB)")
    print(f"[transcribe] file exists  : {os.path.exists(file_path)}")

    if file_size > 25 * 1024 * 1024:
        raise ValueError(
            f"Audio file is {file_size/1024/1024:.1f} MB — Groq's limit is 25 MB. "
            "Please trim or compress the audio before uploading."
        )

    client = _get_client()
    filename = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        audio_bytes = f.read()

    print(f"[transcribe] bytes read   : {len(audio_bytes)}")
    print(f"[transcribe] calling Groq API now...")

    response = client.audio.transcriptions.create(
        model="whisper-large-v3",
        file=(filename, audio_bytes, "audio/mpeg"),
        response_format="json",
        timeout=300,  # 5 minutes — long audio files can take a while
    )
    text = response.text if hasattr(response, "text") else str(response)
    print(f"[transcribe] SUCCESS, transcript length: {len(text)}")
    return text.strip()

