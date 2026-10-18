"""Step 1: prove the Claude API works from this machine."""
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=200,
    messages=[{"role": "user", "content": "In two sentences, what does a purchase order contain?"}],
)

print(response.content[0].text)
print("Tokens used:", response.usage.input_tokens, "in,", response.usage.output_tokens, "out")
