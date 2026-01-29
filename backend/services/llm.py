import ollama
from typing import List, Dict


def generate_reply(messages: List[Dict[str, str]]) -> str:
    """
    Generate a reply using Ollama LLM with llama3.1 model.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys.
                 Example: [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
    
    Returns:
        str: The generated reply content from the LLM.
    """
    response = ollama.chat(
        model="llama3.1",
        messages=messages
    )
    return response["message"]["content"]
