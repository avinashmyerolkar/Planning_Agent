from schemas.plan_obj_schema import Plan
from config.llm import get_llm
from langchain_core.messages import SystemMessage, HumanMessage
from utils.prompt_loader import load_prompt


def orchestrator(state):
    llm = get_llm()
    prompt = load_prompt("orchestrator")
    plan = llm.with_structured_output(Plan).invoke(
        [
            SystemMessage(content=prompt["system"]),
            HumanMessage(content=prompt["human_template"].format(topic=state["topic"])),
        ]
    )
    return {"plan": plan}
