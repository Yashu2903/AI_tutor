from .llm import generate_reply

def teach(topic: str) -> str:
    prompt = [
        {
            "role": "system",
            "content": "You are a tutor. Teach the concept simply in 5-6 lines."
        },
        {
            "role": "user",
            "content": f"Teach me {topic}"
        }
    ]
    return generate_reply(prompt)


def ask_question(topic: str) -> str:
    prompt = [
        {
            "role": "system",
            "content": "You are a tutor. Ask ONE clear question to test understanding."
        },
        {
            "role": "user",
            "content": f"Ask a question about {topic}"
        }
    ]
    return generate_reply(prompt)

