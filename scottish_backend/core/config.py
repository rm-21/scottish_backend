from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "scottish_backend"

    class Config:
        case_sensitive: bool = True
        env_file: str = ".env"


def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
