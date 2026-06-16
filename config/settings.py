from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    ENV: str = "dev"
    DEFAULT_MODEL: str = "gpt-4.1-mini"
    DEFAULT_TEMPERATURE: float = 0.5

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
