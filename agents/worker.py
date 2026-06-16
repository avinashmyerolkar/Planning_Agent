from langchain_core.messages import SystemMessage, HumanMessage
from config.llm import get_llm
from utils.prompt_loader import load_prompt


def worker(payload):
    task = payload["task"]
    topic = payload["topic"]
    plan = payload["plan"]
    llm = get_llm()
    prompt = load_prompt("worker")

    section_md = llm.invoke(
        [
            SystemMessage(content=prompt["system"]),
            HumanMessage(
                content=prompt["human_template"].format(
                    blog_title=plan.blog_title,
                    topic=topic,
                    section_title=task.title,
                    brief=task.brief,
                )
            ),
        ]
    ).content.strip()

    return {"sections": [section_md]}
