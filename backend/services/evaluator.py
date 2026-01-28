from .llm import generate_reply
import json

def evaluate_answer(question: str, answer: str) -> dict:
    prompt =[
        {
            "role": "system",
            "content": (
                "You are an examiner."
                "Evaluate the answer to the question strictly."
                "Return JSON only:\n"
                "{correct: bool, feedback: str}"
            )
        },
        {
            "role": "user",
            "content": f"Question: {question}\nAnswer: {answer}"

        }

    ]

    response = generate_reply(prompt)
    return json.loads(response)

