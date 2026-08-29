import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API key not found. Set GEMINI_API_KEY in the .env file.")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


def reactive_chatbot(user_text: str) -> str:
    response = client.chat.completions.create(
        model="models/gemini-3.6-flash",
        messages=[
            {"role": "system", "content": "You are a helpful training assistant. Keep answers short and clear."},
            {"role": "user", "content": user_text},
        ],
    )
    return response.choices[0].message.content


# try:
#     response = client.chat.completions.create(
#         model="models/gemini-3.6-flash",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": "What is the capital of Pakistan?"},
#         ],
#     )
#     print("Response from Gemini via OpenAI SDK:")
#     print(response.choices[0].message.content)
# except Exception as e:
#     print(f"Error occurred: {e}")
#     print("\nAttempting to list available models for this API key:")
#     models = client.models.list()
#     for model in models:
#         print(f"- {model.id}")

#from gemini_agent import reactive_chatbot

#print(reactive_chatbot("What is the capital of Pakistan?"))


while True:
    user_text = input("You: ")
    if user_text.strip().lower() in {"exit", "quit"}:
        print("Chat ended.")
        break
    bot_text = reactive_chatbot(user_text)
    print("Bot:", bot_text)
