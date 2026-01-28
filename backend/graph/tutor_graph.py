from langgraph.graph import StateGraph
from .state import TutorState
from .nodes import teach_node, ask_node, wait_node, evaluate_node, decide_node


def build_tutor_graph():

    builder = StateGraph(TutorState)

    builder.add_node("teach", teach_node)
    builder.add_node("ask", ask_node)
    builder.add_node("wait", wait_node)
    builder.add_node("evaluate", evaluate_node)
    builder.add_node("decide", decide_node)

    builder.set_entry_point("teach")
    builder.add_edge("teach", "ask")
    builder.add_edge("ask","wait")
    builder.add_edge("wait","evaluate")
    builder.add_edge("evaluate","decide")

    builder.add_conditional_edges(
        "decide",

        decide_node,
        {
            "ask": "ask",
            "teach": "teach"
        }
    )
    return builder.compile(interrupt_after=["wait"])

