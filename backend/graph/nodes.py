from .state import TutorState
from ..services.tutor import teach, ask_question
from ..services.evaluator import evaluate_answer

def teach_node(state: TutorState) -> TutorState:

    lesson = teach(state["topic"])
    return{
        **state,
        "phase":"ask",
        "lesson":lesson,
    }

def ask_node(state: TutorState) -> TutorState:
    question = ask_question(state["topic"])
    return{
        **state,
        "phase":"wait",
        "question":question,
    }

def wait_node(state: TutorState) -> TutorState:
    return state

def evaluate_node(state: TutorState) -> TutorState:
    result = evaluate_answer(
        question=state["question"],
        answer=state["answer"]
    )

    return{
        **state,
        "correct" : result["correct"],
        "feedback" : result["feedback"],
        "phase":"decide"
    }

def decide_node(state: TutorState) -> str:
    if state["correct"]:
        return "ask"
    else:
        return "teach"


