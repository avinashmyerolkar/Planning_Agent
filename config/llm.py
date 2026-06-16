from config.settings import settings
from langchain_openai import ChatOpenAI


def get_llm(model: str | None = None, temperature: float | None = None) -> ChatOpenAI:
    return ChatOpenAI(
        model=model or settings.DEFAULT_MODEL,
        temperature=temperature if temperature is not None else settings.DEFAULT_TEMPERATURE,
        api_key=settings.OPENAI_API_KEY,
    )

