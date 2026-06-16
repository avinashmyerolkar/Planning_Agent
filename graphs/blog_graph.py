from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from state.state import State
from agents.orchestrator import orchestrator
from agents.worker import worker
from agents.reducer import reducer


def fanout(state):
    return [
        Send("worker", {"task": task, "topic": state["topic"], "plan": state["plan"]})
        for task in state["plan"].tasks
    ]


def build_graph():
    g = StateGraph(State)

    g.add_node("orchestrator", orchestrator)
    g.add_node("worker", worker)
    g.add_node("reducer", reducer)

    g.add_edge(START, "orchestrator")
    g.add_conditional_edges("orchestrator", fanout, ["worker"])
    g.add_edge("worker", "reducer")
    g.add_edge("reducer", END)

    return g.compile()
