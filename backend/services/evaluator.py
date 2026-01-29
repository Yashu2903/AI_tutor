from .llm import generate_reply
import json
import re

def evaluate_answer(question: str, answer: str) -> dict:
    """Evaluate student answer and provide feedback."""
    prompt =[
        {
            "role": "system",
            "content": (
                "You are an examiner. "
                "Evaluate the answer to the question strictly. "
                "Return JSON only with this exact format:\n"
                '{"correct": true/false, "feedback": "your feedback here"}'
            )
        },
        {
            "role": "user",
            "content": f"Question: {question}\nAnswer: {answer}"
        }
    ]

    response = generate_reply(prompt)
    
    # Try to extract JSON from response (in case LLM adds extra text)
    try:
        # Look for JSON object in the response
        json_match = re.search(r'\{[^}]+\}', response)
        if json_match:
            return json.loads(json_match.group())
        return json.loads(response)
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        return {
            "correct": False,
            "feedback": "Unable to evaluate answer. Please try again."
        }

