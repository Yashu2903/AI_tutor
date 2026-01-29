from .state import TutorState
from ..services.tutor import teach, ask_question
from ..services.evaluator import evaluate_answer

def teach_node(state: TutorState) -> TutorState:
    """Teach the topic at the current difficulty level."""
    level = state["difficulty"]
    
    # Reset mistakes if we're teaching after mistakes
    mistakes = state.get("mistakes", 0)
    if mistakes >= 2:
        level = "easy"
        mistakes = 0

    lesson = teach(f"{state['topic']} (difficulty: {level})")
    return{
        **state,
        "phase":"ask",
        "lesson":lesson,
        "difficulty": level,
        "mistakes": mistakes,
    }

def ask_node(state: TutorState) -> TutorState:
    """Ask a question and potentially adjust difficulty based on streak."""
    difficulty = state["difficulty"]
    streak = state.get("streak", 0)
    
    # Increase difficulty if student has good streak
    if streak >= 2:
        if difficulty == "easy":
            difficulty = "medium"
        elif difficulty == "medium":
            difficulty = "hard"
    
    prompt = f"{state['topic']} question at {difficulty} level"
    question = ask_question(prompt)
    return{
        **state,
        "phase":"wait",
        "question":question,
        "difficulty": difficulty,
    }

def wait_node(state: TutorState) -> TutorState:
    return state

def evaluate_node(state: TutorState) -> TutorState:
    result = evaluate_answer(
        question=state["question"],
        answer=state["answer"]
    )

    correct = result["correct"]
    mistakes = state["mistakes"]
    streak = state["streak"]

    if correct:
        streak += 1
    else:
        mistakes += 1
        streak = 0

    return{
        **state,
        "correct" : result["correct"],
        "feedback" : result["feedback"],
        "mistakes": mistakes,
        "streak": streak,
        "phase":"decide"
    }

def decide_node(state: TutorState) -> str:
    """Decide next action based on student performance."""
    # If too many mistakes, go back to teaching
    if state.get("mistakes", 0) >= 2:
        return "teach"
    
    # Otherwise, continue asking questions
    return "ask"



