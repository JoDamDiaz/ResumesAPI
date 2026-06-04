from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
