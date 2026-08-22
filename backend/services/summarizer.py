import os
import re
import json
from dotenv import load_dotenv

load_dotenv()

# ── Token budget constants ─────────────────────────────────────────────────────
# qwen/qwen3.6-27b on Groq: 8000 TPM hard limit per request
# Budget per chunk call:
#   ~150 tokens  — system prompt
#   ~50  tokens  — user message overhead
#   ~600 tokens  — reserved for model response
#   ─────────────────────────────────────────
#   7200 tokens  — available for transcript text
#   × 4 chars/token (conservative for English)
#   = 28 800 chars max — we use 24 000 to be safe
MAX_CHARS_PER_CHUNK = 24_000

# ── System prompts ─────────────────────────────────────────────────────────────
CHUNK_SYSTEM_PROMPT = """You are a meeting analyst processing one segment of a longer meeting transcript.
Extract from this segment only:
1. A brief partial summary (1-2 sentences)
2. Key decisions made (list, may be empty)
3. Action items with owners if mentioned (list, may be empty)

Respond with valid JSON only:
{"partial_summary": "...", "key_decisions": [], "action_items": []}"""

COMBINE_SYSTEM_PROMPT = """You are a meeting analyst. You have been given summaries of sequential segments of a meeting.
Combine them into one cohesive final output:
1. A concise overall summary (2-4 sentences)
2. All unique key decisions (deduplicated)
3. All unique action items (deduplicated)

Respond with valid JSON only:
{"summary": "...", "key_decisions": [], "action_items": []}"""

DIRECT_SYSTEM_PROMPT = """You are an expert meeting analyst.
Given a meeting transcript, extract:
1. A concise overall summary (2-4 sentences)
2. Key decisions made during the meeting (list)
3. Action items with owners if mentioned (list)

Respond with valid JSON only:
{"summary": "...", "key_decisions": [], "action_items": []}"""


def _get_client():
    from groq import Groq
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Please add it to backend/.env"
        )
    return Groq(api_key=api_key)


def _split_into_chunks(transcript: str) -> list:
    """
    Split transcript into chunks <= MAX_CHARS_PER_CHUNK.
    Breaks at sentence boundaries where possible.
    """
    if len(transcript) <= MAX_CHARS_PER_CHUNK:
        return [transcript]

    chunks = []
    pos = 0
    while pos < len(transcript):
        end = pos + MAX_CHARS_PER_CHUNK
        if end >= len(transcript):
            chunks.append(transcript[pos:])
            break
        # Prefer breaking at a sentence end
        break_at = transcript.rfind(". ", pos, end)
        if break_at == -1 or break_at <= pos:
            # Fall back to word boundary
            break_at = transcript.rfind(" ", pos, end)
        if break_at == -1 or break_at <= pos:
            break_at = end
        chunks.append(transcript[pos : break_at + 1])
        pos = break_at + 1

    return chunks


def _parse_json_response(content: str) -> dict:
    """
    Parse JSON from a model response that may contain <think>…</think> blocks
    or trailing text after the JSON object.

    qwen/qwen3.6-27b is a thinking model — it prepends <think>…</think> before
    the JSON. response_format=json_object causes Groq server-side validation to
    fail because the thinking tokens are included in the payload.
    We strip them client-side here instead.

    JSONDecoder.raw_decode() is used instead of json.loads() so that trailing
    text after the closing } is silently ignored (prevents JSONDecodeError).
    """
    # 1. Strip <think>…</think> block
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
    # 2. Strip markdown code fences if present
    content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip(), flags=re.MULTILINE).strip()
    # 3. Find the start of the JSON object
    start = content.find("{")
    if start == -1:
        raise ValueError(f"No JSON object found in model response: {content[:200]}")
    # 4. raw_decode parses ONE complete JSON value and ignores trailing text
    decoder = json.JSONDecoder()
    obj, _ = decoder.raw_decode(content, start)
    return obj


def _call_model(client, system: str, user: str) -> dict:
    """
    Single model call — returns parsed JSON dict.
    Does NOT use response_format because qwen/qwen3.6-27b is a thinking model
    that prepends <think>…</think> tokens; server-side JSON validation then fails.
    Instead we strip the thinking block client-side via _parse_json_response.
    """
    response = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        temperature=0.3,
        # response_format intentionally omitted — see _parse_json_response above
    )
    return _parse_json_response(response.choices[0].message.content)


def _summarize_chunk(client, chunk: str, idx: int, total: int) -> dict:
    """Summarize one chunk of the transcript."""
    user_msg = f"Meeting transcript (part {idx + 1} of {total}):\n\n{chunk}"
    result = _call_model(client, CHUNK_SYSTEM_PROMPT, user_msg)
    return {
        "partial_summary": result.get("partial_summary", ""),
        "key_decisions":   result.get("key_decisions", []),
        "action_items":    result.get("action_items", []),
    }


def _combine_chunk_summaries(client, chunk_results: list) -> dict:
    """
    Merge chunk-level summaries into a single final summary.
    The combined text is far smaller than the original transcript,
    so it always fits within the token limit.
    """
    parts = []
    for i, r in enumerate(chunk_results):
        decisions = "; ".join(r["key_decisions"]) or "none"
        actions   = "; ".join(r["action_items"])  or "none"
        parts.append(
            f"Part {i + 1} summary: {r['partial_summary']}\n"
            f"  Decisions: {decisions}\n"
            f"  Actions: {actions}"
        )
    combined = "\n\n".join(parts)
    user_msg = f"Combine these meeting segment summaries into one final output:\n\n{combined}"
    result = _call_model(client, COMBINE_SYSTEM_PROMPT, user_msg)
    return {
        "summary":       result.get("summary", ""),
        "key_decisions": result.get("key_decisions", []),
        "action_items":  result.get("action_items", []),
    }


def summarize_transcript(transcript: str) -> dict:
    """
    Summarize a meeting transcript.
    - Short transcripts  → single direct API call
    - Long transcripts   → chunk → summarize each → combine
    Output format is identical in both cases.
    """
    if not transcript or not transcript.strip():
        return {"summary": "No transcript content available.",
                "key_decisions": [], "action_items": []}

    client = _get_client()
    chunks = _split_into_chunks(transcript.strip())
    print(f"[summarize] transcript length : {len(transcript)} chars")
    print(f"[summarize] chunks            : {len(chunks)}")

    if len(chunks) == 1:
        # Short enough — single call
        user_msg = f"Summarize this meeting transcript:\n\n{transcript}"
        result = _call_model(client, DIRECT_SYSTEM_PROMPT, user_msg)
        return {
            "summary":       result.get("summary", ""),
            "key_decisions": result.get("key_decisions", []),
            "action_items":  result.get("action_items", []),
        }

    # Long transcript — chunk and combine
    chunk_results = []
    for i, chunk in enumerate(chunks):
        print(f"[summarize] processing chunk {i + 1}/{len(chunks)} ({len(chunk)} chars)...")
        chunk_results.append(_summarize_chunk(client, chunk, i, len(chunks)))

    print("[summarize] combining chunk summaries...")
    return _combine_chunk_summaries(client, chunk_results)
