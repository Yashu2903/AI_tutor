from langgraph.graph import StateGraph, START, END

from .state import TutorState
from .nodes import teach_node, ask_node, wait_node

def build_tutor_graph():

    builder = StateGraph(TutorState)

    builder.add_node("teach", teach_node)
    builder.add_node("ask", ask_node)
    builder.add_node("wait", wait_node)

    builder.set_entry_point("teach")
    builder.add_edge("teach", "asl")
    builder.add_edge("ask","wait")

    return builder.compile(interrupt_after=["wait"])

