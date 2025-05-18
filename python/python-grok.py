import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client for xAI API
client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),#export this var with api key inside
    base_url="https://api.x.ai/v1"
)

# Test the API
try:
    response = client.chat.completions.create(
        model="grok-beta",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello from Grok!"}
        ],
        temperature=0.7,
        max_tokens=50
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
