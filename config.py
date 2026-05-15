from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    OPENAI_API_KEY: str = "YOUR_OPENAI_API_KEY"

    CHUNK_SIZE: int = 500

    CHUNK_OVERLAP: int = 100

    MAX_TOKENS_PER_TENANT: int = 50000

    TOP_K: int = 5


settings = Settings()