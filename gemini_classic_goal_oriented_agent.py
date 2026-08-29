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
""" flowchart TD
  A[Goal] --> B[Plan]
  B --> C[Draft from goal + plan]
  C --> D{Evaluator: DONE?}
  D -->|yes| E[Return state]
  D -->|no| F[Rewrite plan]
  F --> C
  """


def call_llm(system_msg: str, user_msg: str, model: str = "models/gemini-3.6-flash") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
    )
    return response.choices[0].message.content

def goal_oriented_agent(goal: str, max_iters: int = 3) -> dict:
    state = {
        "goal": goal,
        "plan": None,
        "draft": None,
        "status": "NOT_DONE",
        "iterations_used": 0
    }

    # 1) PLAN
    state["plan"] = call_llm(
        system_msg="You are a planning assistant. Create short practical plans.",
        user_msg=(
            f"GOAL:\n{goal}\n\n"
            "Create a plan with 3-5 bullet steps. Keep it simple and actionable."
        )
    )
    # 2) LOOP: DRAFT -> CHECK -> REFINE
    for i in range(1, max_iters + 1):
        state["iterations_used"] = i

        # ACT (Draft)
        state["draft"] = call_llm(
            system_msg="You generate structured outputs that follow the goal strictly.",
            user_msg=(
                f"GOAL:\n{state['goal']}\n\n"
                f"PLAN:\n{state['plan']}\n\n"
                "Produce the final answer that satisfies the goal. Keep it structured."
            )
        )
        # EVALUATE (Goal check)
        verdict = call_llm(
            system_msg="You are a strict evaluator. Reply ONLY with DONE or NOT_DONE.",
            user_msg=(
                f"Check if the DRAFT fully satisfies the GOAL.\n\n"
                f"GOAL:\n{state['goal']}\n\n"
                f"DRAFT:\n{state['draft']}\n\n"
                "Reply with exactly one word: DONE or NOT_DONE."
            )
        )

        if verdict == "DONE":
            state["status"] = "DONE"
            break

        # REFINE plan if not done
        state["plan"] = call_llm(
            system_msg="You improve plans to better meet goals.",
            user_msg=(
                f"The draft did NOT fully meet the goal.\n\n"
                f"GOAL:\n{state['goal']}\n\n"
                f"OLD PLAN:\n{state['plan']}\n\n"
                "Rewrite an improved 3-5 bullet plan focusing on what was missing."
            )
        )

    return state

result = goal_oriented_agent(
    goal="Create a 3-day travel plan for Montreal  from Torontowith all the details.",
    max_iters=3
)

print("STATUS:", result["status"])
print("\nPLAN:\n", result["plan"])
print("\nFINAL OUTPUT:\n", result["draft"])
print("\nITERATIONS USED:", result["iterations_used"])








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

