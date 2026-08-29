import os
from openai import OpenAI
from dotenv import load_dotenv
# Load environment variables from the .env file
load_dotenv()
# Initialize the OpenAI client pointing to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key = os.environ.get("OPEN_ROUTER_API_KEY")
)
# Request a completion using an OpenRouter model slug
# Example uses a free model; you can change this to any slug from openrouter.ai/models
completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "", # Optional. Site URL for rankings on openrouter.ai.
    "X-OpenRouter-Title": "", # Optional. Site title for rankings on openrouter.ai.
  },
  extra_body={},
  model="openai/gpt-4.1-mini",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What is in this image?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://www.morebusiness.com/wp-content/uploads/2016/02/free-stock-photos.jpg"
          }
        }
      ]
    }
  ]
)
print(completion.choices[0].message.content)