"""End-to-end test of the summarizer with a realistic transcript."""
import os
from dotenv import load_dotenv
load_dotenv()

from services.summarizer import summarize_transcript, _parse_json_response

# Test 1: _parse_json_response strips thinking tokens correctly
print("=== Test 1: thinking token stripping ===")
fake_response = """
<think>
Let me think about this carefully...
The user wants JSON output.
</think>

{"summary": "Team decided to launch Friday.", "key_decisions": ["Launch on Friday"], "action_items": ["John prepares slides"]}
"""
result = _parse_json_response(fake_response)
print("Parsed OK:", result)
assert result["summary"] == "Team decided to launch Friday."
assert len(result["key_decisions"]) == 1
assert len(result["action_items"]) == 1
print("PASS")

# Test 2: Real model call with a short transcript
print()
print("=== Test 2: real model call (short transcript) ===")
short_transcript = """
Alice: Good morning everyone. Let's get started. Today we need to decide on the product launch date.
Bob: I think we should go with next Friday, the 25th.
Alice: Any objections? Great, so we'll launch on the 25th. Bob, can you prepare the launch slides?
Bob: Sure, I'll have them ready by Wednesday.
Carol: I'll send out the invitations to all stakeholders by Tuesday.
Alice: Perfect. Meeting adjourned.
"""
result = summarize_transcript(short_transcript)
print("Summary:", result["summary"])
print("Decisions:", result["key_decisions"])
print("Actions:", result["action_items"])
assert result["summary"], "Summary should not be empty"
assert isinstance(result["key_decisions"], list)
assert isinstance(result["action_items"], list)
print("PASS")
