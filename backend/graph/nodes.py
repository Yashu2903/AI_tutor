from .state import TutorState
from ..services.tutor import teach, ask_question

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

